// packages/catalog-mcp/__tests__/queue.test.ts
import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { mkdtemp, rm, mkdir, writeFile, readFile } from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import { readQueue, addToQueue, removeFromQueue, clearQueue, updateQueueItem } from '../src/core/queue.js';

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
    expect(queue.items[0].status).toBe('pending');
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
});

describe('queue phase 2', () => {
  let dir: string;
  beforeEach(async () => {
    dir = await mkdtemp(path.join(os.tmpdir(), 'catalog-q-'));
    await mkdir(path.join(dir, 'catalog'), { recursive: true });
    await writeFile(path.join(dir, 'catalog', 'queue.json'), '{"items":[]}\n', 'utf-8');
  });
  afterEach(async () => { await rm(dir, { recursive: true, force: true }); });

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

  it('updates an item status + message by key', async () => {
    await addToQueue(dir, [{ key: 'k1', url: 'https://x/a', source: 'manual' }]);
    await updateQueueItem(dir, 'k1', { status: 'parked', error_message: 'too short' });
    const item = (await readQueue(dir)).items[0];
    expect(item.status).toBe('parked');
    expect(item.error_message).toBe('too short');
  });
});
