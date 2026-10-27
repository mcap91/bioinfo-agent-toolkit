// packages/catalog-mcp/__tests__/queue.test.ts
import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { mkdtemp, rm, mkdir, writeFile, readFile } from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath } from 'node:url';
import { readQueue, addToQueue, removeFromQueue, clearQueue, returnToInbox } from '../src/core/queue.js';
import { parseInbox } from '../src/core/inbox.js';

// Real WK-0054 own-engine capture (golden fixture, shared with packages/catalog-capture).
const GOLDEN_FIXTURE = path.join(
  path.dirname(fileURLToPath(import.meta.url)),
  '..', '..', 'catalog-capture', 'tests', 'fixtures', 'JNjEe87YeN.txt',
);
async function goldenCaptureText(): Promise<string> {
  const raw = await readFile(GOLDEN_FIXTURE, 'utf-8');
  return raw.split('\n').slice(4).join('\n'); // drop the `final/title/shreddit-post/body text:` header lines
}

describe('queue', () => {
  let tmpDir: string;

  beforeEach(async () => {
    tmpDir = await mkdtemp(path.join(os.tmpdir(), 'catalog-queue-'));
    await mkdir(path.join(tmpDir, 'catalog'), { recursive: true });
    await writeFile(
      path.join(tmpDir, 'catalog', 'queue.json'),
      JSON.stringify({ items: [] }),
      'utf-8',
    );
  });

  afterEach(async () => {
    await rm(tmpDir, { recursive: true, force: true });
  });

  it('reads empty queue', async () => {
    const queue = await readQueue(tmpDir);
    expect(queue.items).toEqual([]);
  });

  it('adds items to queue', async () => {
    await addToQueue(tmpDir, [
      { key: 'https://github.com/org/tool', url: 'https://github.com/org/tool', source: 'manual' as const },
    ]);
    const queue = await readQueue(tmpDir);
    expect(queue.items).toHaveLength(1);
    expect(queue.items[0].url).toBe('https://github.com/org/tool');
    expect(queue.items[0].url).toBe('https://github.com/org/tool');
  });

  it('removes items by URL', async () => {
    await addToQueue(tmpDir, [
      { key: 'https://github.com/org/a', url: 'https://github.com/org/a', source: 'manual' as const },
      { key: 'https://github.com/org/b', url: 'https://github.com/org/b', source: 'manual' as const },
    ]);
    await removeFromQueue(tmpDir, ['https://github.com/org/a']);
    const queue = await readQueue(tmpDir);
    expect(queue.items).toHaveLength(1);
    expect(queue.items[0].url).toBe('https://github.com/org/b');
  });

  it('clears all items', async () => {
    await addToQueue(tmpDir, [
      { key: 'https://github.com/org/a', url: 'https://github.com/org/a', source: 'manual' as const },
    ]);
    await clearQueue(tmpDir);
    const queue = await readQueue(tmpDir);
    expect(queue.items).toEqual([]);
  });

  it('sets added timestamp', async () => {
    await addToQueue(tmpDir, [
      { key: 'https://github.com/org/tool', url: 'https://github.com/org/tool', source: 'reddit' as const },
    ]);
    const queue = await readQueue(tmpDir);
    expect(queue.items[0].added).toBeDefined();
    expect(new Date(queue.items[0].added).getTime()).not.toBeNaN();
  });

  it('readQueue returns an empty queue when queue.json is missing (first run, S1)', async () => {
    await rm(path.join(tmpDir, 'catalog', 'queue.json'));
    const queue = await readQueue(tmpDir);
    expect(queue.items).toEqual([]);
  });

  it('readQueue throws (never silently empties) on malformed JSON in an existing file (S1)', async () => {
    await writeFile(path.join(tmpDir, 'catalog', 'queue.json'), '{not valid json', 'utf-8');
    await expect(readQueue(tmpDir)).rejects.toThrow();
  });

  it('readQueue throws (never silently empties) on a schema-violating queue.json (S1)', async () => {
    // A bare `https://` fails z.string().url() — the exact S1 shape (a bad url
    // slipping past a naive check and landing in queue.json).
    await writeFile(
      path.join(tmpDir, 'catalog', 'queue.json'),
      JSON.stringify({ items: [{ key: 'x', url: 'https://', source: 'manual', added: new Date().toISOString() }] }),
      'utf-8',
    );
    await expect(readQueue(tmpDir)).rejects.toThrow();
  });
});

describe('queue phase 2', () => {
  let dir: string;
  beforeEach(async () => {
    dir = await mkdtemp(path.join(os.tmpdir(), 'catalog-q-'));
    await mkdir(path.join(dir, 'catalog'), { recursive: true });
    await writeFile(path.join(dir, 'catalog', 'queue.json'), '{"items":[]}\n', 'utf-8');
  });
  afterEach(async () => { await rm(dir, { recursive: true, force: true }); });

  const writeInbox = (s: string) => writeFile(path.join(dir, 'catalog', 'inbox.md'), s, 'utf-8');
  const readInbox = () => readFile(path.join(dir, 'catalog', 'inbox.md'), 'utf-8');

  it('stores content-only items keyed by content', async () => {
    await addToQueue(dir, [{ key: 'content:abc', content: 'hello', source: 'manual' }]);
    const q = await readQueue(dir);
    expect(q.items[0].content).toBe('hello');
    expect(q.items[0].url).toBeUndefined();
    expect(q.items[0].key).toBe('content:abc');
  });

  it('removes by key', async () => {
    await addToQueue(dir, [{ key: 'https://x/a', url: 'https://x/a', source: 'manual' }]);
    const removed = await removeFromQueue(dir, ['https://x/a']);
    expect(removed).toBe(1);
    expect((await readQueue(dir)).items).toHaveLength(0);
  });

  it('returnToInbox writes a marked url item and removes it from the queue', async () => {
    await addToQueue(dir, [{ key: 'https://x/a', url: 'https://x/a', source: 'manual' }]);
    await writeInbox('# inbox\n');
    expect(await returnToInbox(dir, 'https://x/a', 'fetch error')).toBe(true); // slugified
    expect((await readQueue(dir)).items).toHaveLength(0);
    expect(await readInbox()).toContain('⚠ fetch-error https://x/a');
  });
  it('returnToInbox writes a content item as a marked ```text block', async () => {
    await addToQueue(dir, [{ key: 'content:1', content: 'a tip', source: 'manual' }]);
    await writeInbox('# inbox\n');
    await returnToInbox(dir, 'content:1', 'not-cataloguable');
    expect(await readInbox()).toContain('⚠ not-cataloguable\n```text\na tip\n```');
  });
  it('returnToInbox returns false for an unknown key', async () => {
    await writeInbox('# inbox\n');
    expect(await returnToInbox(dir, 'nope', 'x')).toBe(false);
  });

  it('returnToInbox keeps captured content for a url+content item (R4 root cause)', async () => {
    const text = await goldenCaptureText();
    const url = 'https://www.reddit.com/r/LocalLLaMA/comments/1x9gfnb/google_open_sources_harness2_for_self_improving/';
    await addToQueue(dir, [{ key: url, url, content: text, source: 'manual' }]);
    await writeInbox('# inbox\n');
    expect(await returnToInbox(dir, url, 'empty-fetch')).toBe(true);
    const inboxText = await readInbox();

    // Fenced block, not a bare `⚠ token url` line — the content must survive.
    expect(inboxText).toContain(`source: ${url}`);
    expect(inboxText).toContain('Google Open Sources Harness2 for Self Improving AI Agents');

    // Round trip: parseInbox recovers the same source and content, still blocked.
    const items = parseInbox(inboxText);
    const item = items.find((i) => i.kind === 'text');
    expect(item).toBeDefined();
    expect(item?.blocked).toBe(true);
    expect(item?.reason).toBe('empty-fetch');
    expect(item?.source).toBe(url);
    expect(item?.content).toBe(text.trim());
  });

  it('returnToInbox leaves a url-only item (no content) as a bare marked line', async () => {
    await addToQueue(dir, [{ key: 'https://x/url-only', url: 'https://x/url-only', source: 'manual' }]);
    await writeInbox('# inbox\n');
    await returnToInbox(dir, 'https://x/url-only', 'fetch-error');
    const inboxText = await readInbox();
    expect(inboxText).toContain('⚠ fetch-error https://x/url-only');
    expect(inboxText).not.toContain('```text');
  });

  it('returnToInbox leaves a content-only item (no url) as an unsourced fenced block', async () => {
    await addToQueue(dir, [{ key: 'content:1', content: 'a tip', source: 'manual' }]);
    await writeInbox('# inbox\n');
    await returnToInbox(dir, 'content:1', 'not-cataloguable');
    const inboxText = await readInbox();
    expect(inboxText).toContain('⚠ not-cataloguable\n```text\na tip\n```');
    expect(inboxText).not.toContain('source:');
  });
});
