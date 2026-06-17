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
  key: string;
  url?: string;
  content?: string;
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
        key: item.key,
        url: item.url,
        content: item.content,
        source: item.source,
        notes: item.notes,
        context: item.context,
        added: new Date().toISOString(),
      };
      queue.items.push(queueItem);
      added.push(queueItem);
    }
    await writeQueueAtomic(dir, queue);
    return added;
  });
}

export async function removeFromQueue(dir: string, keys: string[]): Promise<number> {
  return withLock(dir, async () => {
    const queue = await readQueue(dir);
    const keySet = new Set(keys);
    const before = queue.items.length;
    queue.items = queue.items.filter((item) => !keySet.has(item.key));
    await writeQueueAtomic(dir, queue);
    return before - queue.items.length;
  });
}

export async function clearQueue(dir: string): Promise<void> {
  return withLock(dir, async () => {
    await writeQueueAtomic(dir, { items: [] });
  });
}

/** Move a queue item back to catalog/inbox.md marked `⚠ <reason>`, then drop it from the queue.
 * The inverse of ingest; keeps the queue to pending-only. */
export async function returnToInbox(dir: string, key: string, reason: string): Promise<boolean> {
  const queue = await readQueue(dir);
  const item = queue.items.find((i) => i.key === key);
  if (!item) return false;

  const token = (reason || 'returned').trim().replace(/\s+/g, '-');
  const block = formatInboxWriteback(item, token);

  const inboxPath = path.join(dir, 'catalog', 'inbox.md');
  let existing = '';
  try { existing = await readFile(inboxPath, 'utf-8'); } catch { /* new inbox */ }
  existing = existing.replace(/\r\n/g, '\n');
  const sep = existing === '' || existing.endsWith('\n') ? '' : '\n';
  const next = `${existing}${sep}${block}\n`;
  const tmp = inboxPath + '.tmp';
  await writeFile(tmp, next, 'utf-8');
  await rename(tmp, inboxPath);

  await removeFromQueue(dir, [key]);
  return true;
}

function formatInboxWriteback(item: QueueItem, token: string): string {
  if (item.url) return `⚠ ${token} ${item.url}`;
  const src = item.context?.['source'] ? `source: ${item.context['source']}\n` : '';
  return `⚠ ${token}\n\`\`\`text\n${src}${item.content ?? ''}\n\`\`\``;
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
