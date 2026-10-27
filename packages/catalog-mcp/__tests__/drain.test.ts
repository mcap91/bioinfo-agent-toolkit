import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { mkdtemp, rm, mkdir, writeFile, readFile } from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import { drainInbox } from '../src/core/drain.js';
import { readQueue } from '../src/core/queue.js';

const CONFIG = JSON.stringify({
  url_patterns: [],
  blocked_domains: [{ host: 'instagram.com' }, { host: 'linkedin.com', allow_paths: ['/pulse/'] }],
  min_clean_chars: 200,
});

describe('drainInbox', () => {
  let dir: string;
  beforeEach(async () => {
    dir = await mkdtemp(path.join(os.tmpdir(), 'catalog-d-'));
    await mkdir(path.join(dir, 'catalog', 'entries'), { recursive: true });
    await writeFile(path.join(dir, 'catalog', 'queue.json'), '{"items":[]}\n', 'utf-8');
    await writeFile(path.join(dir, 'catalog', 'config.json'), CONFIG, 'utf-8');
  });
  afterEach(async () => { await rm(dir, { recursive: true, force: true }); });

  const writeInbox = (s: string) => writeFile(path.join(dir, 'catalog', 'inbox.md'), s, 'utf-8');
  const readInbox = () => readFile(path.join(dir, 'catalog', 'inbox.md'), 'utf-8');

  it('ingests a fetchable url and removes it from inbox', async () => {
    await writeInbox('https://github.com/org/tool\n');
    const r = await drainInbox(dir);
    expect(r.ingested).toBe(1);
    expect((await readQueue(dir)).items).toHaveLength(1);
    expect(await readInbox()).not.toContain('github.com/org/tool');
  });

  it('marks a blocked-domain url and keeps it in inbox', async () => {
    await writeInbox('https://instagram.com/p/abc\n');
    const r = await drainInbox(dir);
    expect(r.ingested).toBe(0);
    expect(r.blocked).toBe(1);
    const inbox = await readInbox();
    expect(inbox).toContain('instagram.com/p/abc');
    expect(inbox).toContain('⚠ needs-link');
  });

  it('treats a LinkedIn pulse url as fetchable (allow_paths)', async () => {
    await writeInbox('https://linkedin.com/pulse/some-article\n');
    const r = await drainInbox(dir);
    expect(r.ingested).toBe(1);
  });

  it('ingests a fenced text block as a content item', async () => {
    await writeInbox('```text\nsource: https://linkedin.com/posts/x\nprose here\n```\n');
    const r = await drainInbox(dir);
    expect(r.ingested).toBe(1);
    expect((await readQueue(dir)).items[0].content).toContain('prose here');
  });

  it('writes inbox.md with LF endings after rewrite', async () => {
    await writeInbox('https://github.com/org/a\r\nhttps://instagram.com/p/b\r\n');
    await drainInbox(dir);
    expect(await readInbox()).not.toContain('\r\n');
  });

  it('returns per-item skip details when items are deduped', async () => {
    await writeInbox('https://github.com/org/tool\n');
    await drainInbox(dir);
    // Drain again — same URL is now in queue, should be skipped with detail.
    await writeInbox('https://github.com/org/tool\n');
    const r = await drainInbox(dir);
    expect(r.ingested).toBe(0);
    expect(r.skipped).toHaveLength(1);
    expect(r.skipped[0]).toMatchObject({ url: 'https://github.com/org/tool', reason: expect.stringContaining('already') });
  });

  it('collapses consecutive blank lines left by removed items', async () => {
    const inbox = [
      '# Inbox',
      '',
      'https://github.com/org/a',
      'https://github.com/org/b',
      'https://github.com/org/c',
      '',
      'a scratch note',
    ].join('\n') + '\n';
    await writeInbox(inbox);
    await drainInbox(dir);
    const out = await readInbox();
    // Should not have 3+ consecutive newlines (i.e., 2+ blank lines in a row).
    expect(out).not.toMatch(/\n{3,}/);
    expect(out).toContain('# Inbox');
    expect(out).toContain('a scratch note');
  });

  // G1/WK-0080: one blocking rule must cover every Reddit post/share host+path
  // shape catalog-capture's NEEDS_LINK_RE can resolve (rewrite.py) — a line
  // blocked here but unmatched there would stay `⚠ needs-link` forever. URLs
  // are real (toolkit-workbench/web-capture/results.csv), with host/scheme
  // variants derived from them; the /user/ and bare /comments/ cases keep the
  // same real post id in the other path shapes the unified rule documents.
  it.each([
    ['share link', 'https://www.reddit.com/r/AI_Agents/s/kClxACXOyp'],
    ['canonical post, www.reddit.com', 'https://www.reddit.com/r/LocalLLaMA/comments/1x9gfnb/google_open_sources_harness2_for_self_improving/'],
    ['canonical post, old.reddit.com', 'https://old.reddit.com/r/LocalLLaMA/comments/1x9gfnb/google_open_sources_harness2_for_self_improving/'],
    ['canonical post, new.reddit.com', 'https://new.reddit.com/r/LocalLLaMA/comments/1x9gfnb/google_open_sources_harness2_for_self_improving/'],
    ['canonical post, np.reddit.com', 'https://np.reddit.com/r/LocalLLaMA/comments/1x9gfnb/google_open_sources_harness2_for_self_improving/'],
    ['canonical post, m.reddit.com', 'https://m.reddit.com/r/LocalLLaMA/comments/1x9gfnb/google_open_sources_harness2_for_self_improving/'],
    ['canonical post, bare reddit.com', 'https://reddit.com/r/LocalLLaMA/comments/1x9gfnb/google_open_sources_harness2_for_self_improving/'],
    ['canonical post, scheme-less', 'www.reddit.com/r/LocalLLaMA/comments/1x9gfnb/google_open_sources_harness2_for_self_improving/'],
    ['comment-target canonical', 'https://www.reddit.com/r/LocalLLM/comments/1x1rv5k/comment/pew7oqh/'],
    ['/user/<u>/comments/ shape', 'https://www.reddit.com/user/someuser/comments/1x9gfnb/google_open_sources_harness2_for_self_improving/'],
    ['bare /comments/ shorthand', 'https://www.reddit.com/comments/1x9gfnb/google_open_sources_harness2_for_self_improving/'],
  ])('blocks a Reddit post/share url as needs-link: %s', async (_label, url) => {
    await writeInbox(`${url}\n`);
    const r = await drainInbox(dir);
    expect(r.ingested).toBe(0);
    expect(r.blocked).toBe(1);
    expect(await readInbox()).toContain('⚠ needs-link');
  });

  it('leaves a subreddit home page unblocked (no post id to capture)', async () => {
    await writeInbox('https://www.reddit.com/r/LocalLLaMA/\n');
    const r = await drainInbox(dir);
    expect(r.ingested).toBe(1);
  });

  it('leaves a subreddit wiki page unblocked (no post id to capture)', async () => {
    await writeInbox('https://www.reddit.com/r/LocalLLaMA/wiki/index\n');
    const r = await drainInbox(dir);
    expect(r.ingested).toBe(1);
  });

  it('keeps a ⚠-marked text block through a re-drain without re-ingesting it', async () => {
    await writeInbox('⚠ empty-fetch\n```text\nsome tip\n```\n');
    const r = await drainInbox(dir);
    expect(r.ingested).toBe(0);
    expect(r.blocked).toBe(1);
    const inbox = await readInbox();
    expect(inbox).toContain('⚠ empty-fetch');
    expect(inbox).toContain('some tip');
    expect((await readQueue(dir)).items).toHaveLength(0);
  });
  it('preserves a non-needs-link reason on a blocked url across re-drain', async () => {
    await writeInbox('⚠ fetch-error https://github.com/o/r\n');
    await drainInbox(dir);
    expect(await readInbox()).toContain('⚠ fetch-error https://github.com/o/r');
  });

  it('ingests a text block whose source is an http(s) URL using that URL as the queue key (R4)', async () => {
    await writeInbox('```text\nsource: https://www.reddit.com/r/AI_Agents/comments/abc123/some_title/\ncaptured reddit post text\n```\n');
    const r = await drainInbox(dir);
    expect(r.ingested).toBe(1);
    const items = (await readQueue(dir)).items;
    expect(items).toHaveLength(1);
    expect(items[0].key).toBe('https://www.reddit.com/r/AI_Agents/comments/abc123/some_title/');
    expect(items[0].url).toBe('https://www.reddit.com/r/AI_Agents/comments/abc123/some_title/');
    expect(items[0].content).toContain('captured reddit post text');
  });

  it('skips a text block whose source URL is already cataloged (R4)', async () => {
    await writeFile(
      path.join(dir, 'catalog', 'entries', 'existing.md'),
      '---\nname: existing\ntitle: Existing\nurl: https://www.reddit.com/r/AI_Agents/comments/abc123/some_title/\ncategory: skill\nverdict: adopt\nverdict_reason: good\ntags: [test]\nreviewed: 2026-06-03\n---\n',
      'utf-8',
    );
    await writeInbox('```text\nsource: https://www.reddit.com/r/AI_Agents/comments/abc123/some_title/\ncaptured reddit post text\n```\n');
    const r = await drainInbox(dir);
    expect(r.ingested).toBe(0);
    expect(r.skipped).toHaveLength(1);
    expect(r.skipped[0].reason).toMatch(/already cataloged/);
  });

  it('leaves a sourceless text block ingested by content key, unaffected by R4', async () => {
    await writeInbox('```text\nprose here with no source line\n```\n');
    const r = await drainInbox(dir);
    expect(r.ingested).toBe(1);
    const items = (await readQueue(dir)).items;
    expect(items[0].url).toBeUndefined();
    expect(items[0].key).toMatch(/^content:[0-9a-f]{16}$/);
    expect(items[0].content).toContain('prose here with no source line');
  });

  it('falls back to content-only when source looks like a url but fails URL validation (S1)', async () => {
    // "https://" starts with http(s):// but fails z.string().url() — the queue
    // schema's own check, not just a prefix test. Must never reach addToQueue
    // as `url`, or a later readQueue would throw on this file (S1).
    await writeInbox('```text\nsource: https://\nsome captured text\n```\n');
    const r = await drainInbox(dir);
    expect(r.ingested).toBe(1);
    const items = (await readQueue(dir)).items; // throws if the written file is invalid
    expect(items[0].url).toBeUndefined();
    expect(items[0].key).toMatch(/^content:[0-9a-f]{16}$/);
    expect(items[0].content).toContain('some captured text');
  });

  it('preserves header prose and scratch notes; removes processed urls; keeps+marks blocked', async () => {
    const inbox = [
      '# Catalog inbox',
      '',
      'Drop URLs here, then run the drain.',
      '',
      'https://github.com/org/tool',
      'a scratch note to self',
      'https://instagram.com/p/abc',
    ].join('\n') + '\n';
    await writeInbox(inbox);
    const r = await drainInbox(dir);
    const out = await readInbox();
    // prose and scratch survive
    expect(out).toContain('Drop URLs here');
    expect(out).toContain('a scratch note to self');
    // processed url removed
    expect(out).not.toContain('github.com/org/tool');
    // blocked url kept and marked
    expect(out).toContain('instagram.com/p/abc');
    expect(out).toContain('⚠ needs-link');
    // LF only
    expect(out).not.toContain('\r\n');
    expect(r.ingested).toBe(1);
    expect(r.blocked).toBe(1);
  });
});
