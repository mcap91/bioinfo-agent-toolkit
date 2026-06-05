// packages/catalog-mcp/__tests__/queue.test.ts
import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { mkdtemp, rm, mkdir, writeFile, readFile } from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import { readQueue, addToQueue, removeFromQueue, clearQueue } from '../src/core/queue.js';

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
      { url: 'https://github.com/org/tool', source: 'manual' as const },
    ]);
    const queue = await readQueue(tmpDir);
    expect(queue.items).toHaveLength(1);
    expect(queue.items[0].url).toBe('https://github.com/org/tool');
    expect(queue.items[0].status).toBe('pending');
  });

  it('removes items by URL', async () => {
    await addToQueue(tmpDir, [
      { url: 'https://github.com/org/a', source: 'manual' as const },
      { url: 'https://github.com/org/b', source: 'manual' as const },
    ]);
    await removeFromQueue(tmpDir, ['https://github.com/org/a']);
    const queue = await readQueue(tmpDir);
    expect(queue.items).toHaveLength(1);
    expect(queue.items[0].url).toBe('https://github.com/org/b');
  });

  it('clears all items', async () => {
    await addToQueue(tmpDir, [
      { url: 'https://github.com/org/a', source: 'manual' as const },
    ]);
    await clearQueue(tmpDir);
    const queue = await readQueue(tmpDir);
    expect(queue.items).toEqual([]);
  });

  it('sets added timestamp', async () => {
    await addToQueue(tmpDir, [
      { url: 'https://github.com/org/tool', source: 'reddit' as const },
    ]);
    const queue = await readQueue(tmpDir);
    expect(queue.items[0].added).toBeDefined();
    expect(new Date(queue.items[0].added).getTime()).not.toBeNaN();
  });
});
