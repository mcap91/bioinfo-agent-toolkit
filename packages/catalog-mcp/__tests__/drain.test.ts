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
  gmail_fallback: true,
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

  it('blocks Reddit /s/ share links as unfetchable', async () => {
    await writeInbox('https://www.reddit.com/r/AI_Agents/s/kClxACXOyp\n');
    const r = await drainInbox(dir);
    expect(r.ingested).toBe(0);
    expect(r.blocked).toBe(1);
    const inbox = await readInbox();
    expect(inbox).toContain('reddit.com/r/AI_Agents/s/kClxACXOyp');
    expect(inbox).toContain('⚠ needs-link');
  });

  it('allows normal Reddit /comments/ urls through', async () => {
    await writeInbox('https://www.reddit.com/r/AI_Agents/comments/abc123/some_title\n');
    const r = await drainInbox(dir);
    expect(r.ingested).toBe(1);
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
