// packages/catalog-mcp/src/core/queue.ts
import { readFile, writeFile, rename } from 'node:fs/promises';
import path from 'node:path';
import { catalogPaths } from './config.js';
import { withFileLock } from './file-lock.js';
import { queueSchema, type QueueItem } from './schema.js';

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

/** Read and validate queue.json. A missing file is an empty queue (first run).
 * Any other failure (malformed JSON, schema violation) throws — silently
 * returning `{items:[]}` for an existing-but-broken file would make the next
 * write permanently drop every queued item. */
export async function readQueue(dir: string): Promise<QueueData> {
  const paths = catalogPaths(dir);
  let raw: string;
  try {
    raw = await readFile(paths.queue, 'utf-8');
  } catch (err) {
    if ((err as NodeJS.ErrnoException).code === 'ENOENT') return { items: [] };
    throw err;
  }
  return queueSchema.parse(JSON.parse(raw));
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
  // One lock over the whole move: the inbox is a read-modify-write too, and parallel sessions
  // (catalog:process --concurrency) can return items at the same moment.
  return withLock(dir, async () => {
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

    queue.items = queue.items.filter((i) => i.key !== key);
    await writeQueueAtomic(dir, queue);
    return true;
  });
}

function formatInboxWriteback(item: QueueItem, token: string): string {
  // An item with content (R4: including a captured text item whose dedup key is a
  // URL) must keep that content — the bare `⚠ token url` line would drop it, and
  // needs-link capture tools match only `/s/` share links, so it could never be
  // recaptured. Only a true url-only item (no content) gets the bare line.
  if (item.content) {
    const sourceValue = item.url ?? (item.context?.['source'] as string | undefined);
    const src = sourceValue ? `source: ${sourceValue}\n` : '';
    return `⚠ ${token}\n\`\`\`text\n${src}${item.content}\n\`\`\``;
  }
  if (item.url) return `⚠ ${token} ${item.url}`;
  return `⚠ ${token}`;
}

async function writeQueueAtomic(dir: string, data: QueueData): Promise<void> {
  const paths = catalogPaths(dir);
  const tmpPath = paths.queue + '.tmp';
  await writeFile(tmpPath, JSON.stringify(data, null, 2) + '\n', 'utf-8');
  await rename(tmpPath, paths.queue);
}

function withLock<T>(dir: string, fn: () => Promise<T>): Promise<T> {
  return withFileLock(catalogPaths(dir).queueLock, fn);
}
