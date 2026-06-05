// packages/catalog-mcp/src/core/queue.ts
import { readFile, writeFile, rename, unlink } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { catalogPaths } from './config.js';
import { queueSchema, type QueueItem } from './schema.js';

const LOCK_STALE_MS = 60_000;

interface QueueData {
  items: QueueItem[];
}

interface AddItem {
  url: string;
  source: 'manual' | 'reddit' | 'slack' | 'email' | 'other';
  notes?: string;
  context?: Record<string, unknown>;
}

export async function readQueue(dir: string): Promise<QueueData> {
  const paths = catalogPaths(dir);
  try {
    const raw = await readFile(paths.queue, 'utf-8');
    return queueSchema.parse(JSON.parse(raw));
  } catch {
    return { items: [] };
  }
}

export async function addToQueue(dir: string, items: AddItem[]): Promise<QueueItem[]> {
  return withLock(dir, async () => {
    const queue = await readQueue(dir);
    const added: QueueItem[] = [];

    for (const item of items) {
      const queueItem: QueueItem = {
        url: item.url,
        source: item.source,
        notes: item.notes,
        context: item.context,
        added: new Date().toISOString(),
        status: 'pending',
      };
      queue.items.push(queueItem);
      added.push(queueItem);
    }

    await writeQueueAtomic(dir, queue);
    return added;
  });
}

export async function removeFromQueue(
  dir: string,
  urls: string[],
): Promise<number> {
  return withLock(dir, async () => {
    const queue = await readQueue(dir);
    const urlSet = new Set(urls);
    const before = queue.items.length;
    queue.items = queue.items.filter((item) => !urlSet.has(item.url));
    await writeQueueAtomic(dir, queue);
    return before - queue.items.length;
  });
}

export async function clearQueue(dir: string): Promise<void> {
  return withLock(dir, async () => {
    await writeQueueAtomic(dir, { items: [] });
  });
}

async function writeQueueAtomic(dir: string, data: QueueData): Promise<void> {
  const paths = catalogPaths(dir);
  const tmpPath = paths.queue + '.tmp';
  await writeFile(tmpPath, JSON.stringify(data, null, 2) + '\n', 'utf-8');
  await rename(tmpPath, paths.queue);
}

async function withLock<T>(dir: string, fn: () => Promise<T>): Promise<T> {
  const paths = catalogPaths(dir);
  const lockPath = paths.queueLock;

  // Reclaim stale lock
  if (existsSync(lockPath)) {
    try {
      const lockData = JSON.parse(await readFile(lockPath, 'utf-8'));
      const age = Date.now() - lockData.timestamp;
      if (age > LOCK_STALE_MS) {
        await unlink(lockPath);
      } else {
        throw new Error('Queue is locked by another process. Try again shortly.');
      }
    } catch (err) {
      if ((err as Error).message.includes('locked')) throw err;
      // Lock file corrupt — remove it
      await unlink(lockPath).catch(() => {});
    }
  }

  await writeFile(
    lockPath,
    JSON.stringify({ pid: process.pid, timestamp: Date.now() }),
    'utf-8',
  );

  try {
    return await fn();
  } finally {
    await unlink(lockPath).catch(() => {});
  }
}
