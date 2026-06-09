// packages/catalog-mcp/src/core/drain.ts
import { readFile, writeFile, rename } from 'node:fs/promises';
import path from 'node:path';
import { loadConfig } from './config.js';
import { parseInbox, type InboxItem } from './inbox.js';
import { ingest } from './ingest.js';
import type { BlockedDomain } from './schema.js';

interface DrainResult {
  ingested: number;
  blocked: number;
  skipped: number;
}

function hostBlocked(url: string, blocked: BlockedDomain[]): boolean {
  let parsed: URL;
  try { parsed = new URL(url); } catch { return false; }
  const host = parsed.hostname.replace(/^www\./, '');
  for (const b of blocked) {
    if (host === b.host || host.endsWith(`.${b.host}`)) {
      if (b.allow_paths?.some((p) => parsed.pathname.startsWith(p))) return false;
      return true;
    }
  }
  return false;
}

/** Parse inbox.md, ingest ready items, keep/mark blocked items, rewrite the file (LF). */
export async function drainInbox(dir: string): Promise<DrainResult> {
  const inboxPath = path.join(dir, 'catalog', 'inbox.md');
  const config = await loadConfig(dir);

  let text: string;
  try { text = await readFile(inboxPath, 'utf-8'); } catch { return { ingested: 0, blocked: 0, skipped: 0 }; }

  const header = text.split('\n').slice(0, headerLineCount(text)).join('\n');
  const items = parseInbox(text);

  let ingested = 0;
  let blocked = 0;
  let skipped = 0;
  const keepLines: string[] = [];

  for (const item of items) {
    const isBlocked =
      item.blocked || (item.kind === 'url' && item.url ? hostBlocked(item.url, config.blocked_domains) : false);

    if (isBlocked) {
      blocked++;
      keepLines.push(ensureMarker(item));
      continue;
    }
    const r = await ingest({
      dir,
      items: [item.kind === 'url'
        ? { url: item.url, source: 'manual' as const, notes: item.note }
        : { content: item.content, source: 'manual' as const, context: item.source ? { source: item.source } : undefined }],
    });
    if (r.count > 0) ingested++;
    else skipped++;
  }

  // Atomic-ish rewrite: header + kept (blocked) lines, LF only.
  const body = [header.trimEnd(), '', ...keepLines].filter((l, idx, a) => !(l === '' && a[idx - 1] === '')).join('\n');
  const out = body.endsWith('\n') ? body : body + '\n';
  const tmp = inboxPath + '.tmp';
  await writeFile(tmp, out.replace(/\r\n/g, '\n'), 'utf-8');
  await rename(tmp, inboxPath);

  return { ingested, blocked, skipped };
}

function ensureMarker(item: InboxItem): string {
  const base = item.raw.replace(/⚠\s*needs-link\s*/g, '').trim();
  return `⚠ needs-link ${base}`;
}

/** Number of leading lines that are the human header (until first blank line). */
function headerLineCount(text: string): number {
  const lines = text.replace(/\r\n/g, '\n').split('\n');
  if (!lines[0]?.startsWith('#')) return 0;
  const blank = lines.indexOf('');
  return blank === -1 ? lines.length : blank;
}
