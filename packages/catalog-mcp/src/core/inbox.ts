// packages/catalog-mcp/src/core/inbox.ts
export interface InboxItem {
  kind: 'url' | 'text';
  url?: string;
  content?: string;
  source?: string;
  note?: string;
  blocked: boolean;
  raw: string;
  /** 0-based index of the first line that belongs to this item (inclusive). */
  startLine: number;
  /** 0-based index of the last line that belongs to this item (inclusive). */
  endLine: number;
}

const URL_LINE = /^\s*(https?:\/\/\S+)(?:\s+—\s+(.*))?\s*$/;
const NEEDS_LINK = /⚠\s*needs-link/;
const FENCE_OPEN = /^\s*```text\s*$/;
const FENCE_CLOSE = /^\s*```\s*$/;
const SOURCE_LINE = /^source:\s*(\S+)\s*$/;

/** Parse inbox.md into structured items. Lines that match nothing are ignored. */
export function parseInbox(text: string): InboxItem[] {
  const lines = text.replace(/\r\n/g, '\n').split('\n');
  const items: InboxItem[] = [];
  let i = 0;

  while (i < lines.length) {
    const line = lines[i];

    if (FENCE_OPEN.test(line)) {
      const fenceStart = i;
      // Collect until closing fence.
      const block: string[] = [];
      let closed = false;
      i++;
      while (i < lines.length) {
        if (FENCE_CLOSE.test(lines[i])) { closed = true; i++; break; }
        block.push(lines[i]);
        i++;
      }
      if (!closed) {
        // Unterminated fence — warn (caller can surface) and skip.
        // eslint-disable-next-line no-console
        console.warn('inbox: unterminated ```text block — skipped');
        continue;
      }
      // fenceEnd is i - 1 (the closing ```)
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
          blocked: false,
          raw: block.join('\n'),
          startLine: fenceStart,
          endLine: fenceEnd,
        });
      }
      continue;
    }

    const blocked = NEEDS_LINK.test(line);
    const stripped = line.replace(NEEDS_LINK, '').trim();
    const m = stripped.match(URL_LINE);
    if (m) {
      items.push({
        kind: 'url',
        url: m[1],
        note: m[2]?.trim(),
        blocked,
        raw: line.trim(),
        startLine: i,
        endLine: i,
      });
    }
    i++;
  }
  return items;
}
