// packages/catalog-mcp/src/core/ingest.ts
import { readAllEntries } from './frontmatter.js';
import { catalogPaths } from './config.js';
import { readQueue, addToQueue } from './queue.js';

interface IngestItem {
  url: string;
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
  skipped: { url: string; reason: string }[];
  count: number;
}

export async function ingest(options: IngestOptions): Promise<IngestResult> {
  const { dir, items, deduplicate = true } = options;
  const added: string[] = [];
  const skipped: { url: string; reason: string }[] = [];
  const toAdd: IngestItem[] = [];

  if (deduplicate) {
    const paths = catalogPaths(dir);
    const queue = await readQueue(dir);
    const queueUrls = new Set(queue.items.map((i) => i.url));

    const entries = await readAllEntries(paths.entries);
    const entryUrls = new Set<string>();
    for (const [, entry] of entries) {
      const url = entry.frontmatter.url;
      if (typeof url === 'string' && url) entryUrls.add(url);
    }

    for (const item of items) {
      if (queueUrls.has(item.url)) {
        skipped.push({ url: item.url, reason: 'already in queue' });
      } else if (entryUrls.has(item.url)) {
        skipped.push({ url: item.url, reason: 'already cataloged' });
      } else {
        toAdd.push(item);
        added.push(item.url);
      }
    }
  } else {
    toAdd.push(...items);
    added.push(...items.map((i) => i.url));
  }

  if (toAdd.length > 0) {
    await addToQueue(
      dir,
      toAdd.map((item) => ({
        url: item.url,
        source: item.source || 'manual',
        notes: item.notes,
        context: item.context,
      })),
    );
  }

  return { added, skipped, count: added.length };
}
