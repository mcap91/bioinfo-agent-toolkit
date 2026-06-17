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
  skipped: { url: string; reason: string }[];
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

function urlUnfetchable(url: string): boolean {
  let parsed: URL;
  try { parsed = new URL(url); } catch { return false; }
  const host = parsed.hostname.replace(/^www\./, '');
  if ((host === 'reddit.com' || host === 'old.reddit.com') && /^\/r\/[^/]+\/s\//.test(parsed.pathname)) {
    return true;
  }
  return false;
}

/** Parse inbox.md, ingest ready items, keep/mark blocked items, rewrite the file (LF). */
export async function drainInbox(dir: string): Promise<DrainResult> {
  const inboxPath = path.join(dir, 'catalog', 'inbox.md');
  const config = await loadConfig(dir);

  let text: string;
  try { text = await readFile(inboxPath, 'utf-8'); } catch { return { ingested: 0, blocked: 0, skipped: [] }; }

  const lines = text.replace(/\r\n/g, '\n').split('\n');
  const items = parseInbox(text);

  let ingested = 0;
  let blocked = 0;
  const skipped: { url: string; reason: string }[] = [];

  // Classify every item and build a map of line-index → what to do with it.
  // Actions: 'drop' (remove), 'keep-marked' (replace line with marked version), 'keep' (verbatim).
  // Line indices not touched stay verbatim (prose, blanks, headers, scratch).
  type LineAction =
    | { action: 'drop' }
    | { action: 'keep-marked'; replacement: string };

  const lineActions = new Map<number, LineAction>();

  for (const item of items) {
    const ruleBlocked = item.kind === 'url' && item.url
      ? hostBlocked(item.url, config.blocked_domains) || urlUnfetchable(item.url)
      : false;
    const isBlocked = item.blocked || ruleBlocked;

    if (isBlocked) {
      blocked++;
      if (item.kind === 'text') {
        // Already a ⚠ marker line + fence — keep every line verbatim (no action).
        continue;
      }
      lineActions.set(item.startLine, {
        action: 'keep-marked',
        replacement: ensureMarker(item, item.reason ?? 'needs-link'),
      });
      continue;
    }

    const r = await ingest({
      dir,
      items: [item.kind === 'url'
        ? { url: item.url, source: 'manual' as const, notes: item.note }
        : { content: item.content, source: 'manual' as const, context: item.source ? { source: item.source } : undefined }],
    });

    const success = r.count > 0;
    if (success) {
      ingested++;
    } else {
      for (const s of r.skipped) skipped.push({ url: s.key, reason: s.reason });
    }

    // Drop all lines belonging to this item regardless of ingestion result.
    for (let ln = item.startLine; ln <= item.endLine; ln++) {
      lineActions.set(ln, { action: 'drop' });
    }
  }

  // Build output by walking original lines and applying actions.
  const outLines: string[] = [];
  for (let ln = 0; ln < lines.length; ln++) {
    const action = lineActions.get(ln);
    if (!action) {
      // No action — keep verbatim (prose, blanks, headers, scratch).
      outLines.push(lines[ln]);
    } else if (action.action === 'keep-marked') {
      outLines.push(action.replacement);
    }
    // action === 'drop' → skip line.
  }

  // Normalize: LF only, collapse runs of blank lines, trim, single trailing newline.
  let out = outLines.join('\n').replace(/\r\n/g, '\n').replace(/\n{3,}/g, '\n\n').trimEnd() + '\n';

  // Atomic-ish rewrite.
  const tmp = inboxPath + '.tmp';
  await writeFile(tmp, out, 'utf-8');
  await rename(tmp, inboxPath);

  return { ingested, blocked, skipped };
}

function ensureMarker(item: InboxItem, reason: string): string {
  const base = item.raw.replace(/^\s*⚠\s*\S*\s*/, '').trim();
  return `⚠ ${reason} ${base}`;
}
