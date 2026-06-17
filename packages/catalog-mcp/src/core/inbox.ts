// packages/catalog-mcp/src/core/inbox.ts
export interface InboxItem {
  kind: 'url' | 'text';
  url?: string;
  content?: string;
  source?: string;
  note?: string;
  blocked: boolean;
  reason?: string;
  raw: string;
  /** 0-based index of the first line that belongs to this item (inclusive). */
  startLine: number;
  /** 0-based index of the last line that belongs to this item (inclusive). */
  endLine: number;
}

const WARN = '⚠';
const URL_LINE = /^\s*((?:https?:\/\/)?(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\/\S*)(?:\s+—\s+(.*))?\s*$/;
const FENCE_OPEN = /^\s*```text\b.*$/;
const FENCE_CLOSE = /^\s*```\s*$/;
const SOURCE_LINE = /^source:\s*(\S+)\s*$/;

/** Split a ⚠-marked line into its reason token and the remainder after it. */
function splitMarker(line: string): { reason: string; rest: string } {
  const after = line.slice(line.indexOf(WARN) + WARN.length).trim();
  const m = after.match(/^(\S+)?\s*([\s\S]*)$/);
  return { reason: (m?.[1] ?? '').trim(), rest: (m?.[2] ?? '').trim() };
}

/** Parse inbox.md into structured items. Lines that match nothing are ignored. */
export function parseInbox(text: string): InboxItem[] {
  const lines = text.replace(/\r\n/g, '\n').split('\n');
  const items: InboxItem[] = [];
  let pending: { reason: string; line: number } | null = null;
  let i = 0;

  while (i < lines.length) {
    const line = lines[i];

    // Fenced text block.
    if (FENCE_OPEN.test(line)) {
      const fenceStart = i;
      const block: string[] = [];
      let closed = false;
      i++;
      while (i < lines.length) {
        if (FENCE_CLOSE.test(lines[i])) { closed = true; i++; break; }
        block.push(lines[i]);
        i++;
      }
      if (!closed) {
        // eslint-disable-next-line no-console
        console.warn('inbox: unterminated ```text block — skipped');
        pending = null;
        continue;
      }
      const fenceEnd = i - 1;
      let source: string | undefined;
      const contentLines = [...block];
      const sm = block[0]?.match(SOURCE_LINE);
      if (sm) { source = sm[1]; contentLines.shift(); }
      const content = contentLines.join('\n').trim();
      if (content) {
        items.push({
          kind: 'text',
          content,
          source,
          blocked: pending !== null,
          reason: pending?.reason,
          raw: block.join('\n'),
          startLine: pending ? pending.line : fenceStart,
          endLine: fenceEnd,
        });
      }
      pending = null;
      continue;
    }

    // A ⚠-marked line.
    if (line.includes(WARN)) {
      const { reason, rest } = splitMarker(line);
      const um = rest.match(URL_LINE);
      if (um) {
        const rawUrl = um[1];
        items.push({
          kind: 'url',
          url: rawUrl.match(/^https?:\/\//) ? rawUrl : `https://${rawUrl}`,
          note: um[2]?.trim(),
          blocked: true,
          reason,
          raw: line.trim(),
          startLine: i,
          endLine: i,
        });
        pending = null;
      } else {
        // Standalone marker — attaches to the immediately-following text block.
        pending = { reason, line: i };
      }
      i++;
      continue;
    }

    // A plain (unmarked) url line.
    const m = line.match(URL_LINE);
    if (m) {
      const rawUrl = m[1];
      items.push({
        kind: 'url',
        url: rawUrl.match(/^https?:\/\//) ? rawUrl : `https://${rawUrl}`,
        note: m[2]?.trim(),
        blocked: false,
        raw: line.trim(),
        startLine: i,
        endLine: i,
      });
    }
    // Any non-fence line breaks a dangling marker (it only attaches to an
    // immediately-following text block).
    if (pending && !FENCE_OPEN.test(line)) pending = null;
    i++;
  }
  return items;
}
