import { describe, it, expect } from 'vitest';
import { parseInbox } from '../src/core/inbox.js';

describe('parseInbox', () => {
  it('parses a bare url line with a note', () => {
    const items = parseInbox('https://github.com/org/tool — a note\n');
    expect(items).toEqual([
      { kind: 'url', url: 'https://github.com/org/tool', note: 'a note', blocked: false, raw: 'https://github.com/org/tool — a note' },
    ]);
  });

  it('flags a line carrying the needs-link marker as blocked', () => {
    const items = parseInbox('⚠ needs-link https://instagram.com/p/abc\n');
    expect(items[0].blocked).toBe(true);
  });

  it('parses a fenced text block with a source line', () => {
    const md = '```text\nsource: https://linkedin.com/posts/x\nLine one\nLine two\n```\n';
    const items = parseInbox(md);
    expect(items[0]).toMatchObject({ kind: 'text', source: 'https://linkedin.com/posts/x', content: 'Line one\nLine two' });
  });

  it('ignores blank lines, headers, and prose', () => {
    const items = parseInbox('# inbox\n\njust a note to self\n');
    expect(items).toEqual([]);
  });

  it('warns and skips an unterminated fence', () => {
    const items = parseInbox('```text\nno closing fence\n');
    expect(items.find((i) => i.kind === 'text')).toBeUndefined();
  });
});
