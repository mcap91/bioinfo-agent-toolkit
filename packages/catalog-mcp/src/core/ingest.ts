// packages/catalog-mcp/src/core/ingest.ts
import { readAllEntries } from './frontmatter.js';
import { catalogPaths } from './config.js';
import { readQueue, addToQueue } from './queue.js';
import { dedupKey } from './dedup.js';

interface IngestItem {
  url?: string;
  content?: string;
  source?: 'manual' | 'reddit' | 'slack' | 'email' | 'other';
  notes?: string;
  context?: Record<string, unknown>;
}

interface IngestOptions {
  dir: string;
  items: IngestItem[];
  deduplicate?: boolean;
}

interface IngestResult {
  added: string[];
  skipped: { key: string; reason: string }[];
  count: number;
}

export async function ingest(options: IngestOptions): Promise<IngestResult> {
  const { dir, items, deduplicate = true } = options;
  const added: string[] = [];
  const skipped: { key: string; reason: string }[] = [];
  const toAdd: Array<IngestItem & { key: string }> = [];

  const paths = catalogPaths(dir);
  const queue = await readQueue(dir);
  const queueKeys = new Set(queue.items.map((i) => i.key.toLowerCase()));

  const entries = await readAllEntries(paths.entries);
  const entryUrls = new Set<string>();
  for (const [, entry] of entries) {
    const url = entry.frontmatter.url;
    if (typeof url === 'string' && url) entryUrls.add(url.toLowerCase());
  }

  const seenThisBatch = new Set<string>();

  for (const item of items) {
    let key: string;
    try {
      key = dedupKey(item);
    } catch {
      skipped.push({ key: '(invalid)', reason: 'item has neither url nor content' });
      continue;
    }

    if (deduplicate) {
      const keyLower = key.toLowerCase();
      if (queueKeys.has(keyLower) || seenThisBatch.has(keyLower)) {
        skipped.push({ key, reason: 'already in queue' });
        continue;
      }
      if (item.url && entryUrls.has(item.url.toLowerCase())) {
        skipped.push({ key, reason: 'already cataloged' });
        continue;
      }
      seenThisBatch.add(keyLower);
    } else {
      seenThisBatch.add(key);
    }
    toAdd.push({ ...item, key });
    added.push(key);
  }

  if (toAdd.length > 0) {
    await addToQueue(
      dir,
      toAdd.map((item) => ({
        key: item.key,
        url: item.url,
        content: item.content,
        source: item.source || 'manual',
        notes: item.notes,
        context: item.context,
      })),
    );
  }

  return { added, skipped, count: added.length };
}
