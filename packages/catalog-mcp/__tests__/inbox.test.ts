import { describe, it, expect } from 'vitest';
import { parseInbox } from '../src/core/inbox.js';

describe('parseInbox', () => {
  it('parses a bare url line with a note', () => {
    const items = parseInbox('https://github.com/org/tool — a note\n');
    expect(items).toMatchObject([
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

  it('parses a bare url without protocol and normalizes to https', () => {
    const items = parseInbox('github.com/org/tool\n');
    expect(items).toMatchObject([
      { kind: 'url', url: 'https://github.com/org/tool', blocked: false },
    ]);
  });

  it('parses a bare url with a note', () => {
    const items = parseInbox('github.com/org/tool — check this out\n');
    expect(items).toMatchObject([
      { kind: 'url', url: 'https://github.com/org/tool', note: 'check this out' },
    ]);
  });

  it('does not match prose lines as bare urls', () => {
    const items = parseInbox('Remember to deny Claude from reading your .env\n');
    expect(items).toEqual([]);
  });

  it('ignores blank lines, headers, and prose', () => {
    const items = parseInbox('# inbox\n\njust a note to self\n');
    expect(items).toEqual([]);
  });

  it('warns and skips an unterminated fence', () => {
    const items = parseInbox('```text\nno closing fence\n');
    expect(items.find((i) => i.kind === 'text')).toBeUndefined();
  });

  it('parses a fence with trailing apostrophe (```text\')', () => {
    const md = "```text'\nsome content\n```\n";
    const items = parseInbox(md);
    expect(items).toMatchObject([{ kind: 'text', content: 'some content' }]);
  });

  it('parses a fence with trailing garbage after text', () => {
    const md = '```text123\nsome content\n```\n';
    const items = parseInbox(md);
    expect(items).toEqual([]);
  });

  it('parses an arbitrary kebab reason on a url line as blocked', () => {
    const items = parseInbox('⚠ fetch-error https://github.com/o/r\n');
    expect(items[0]).toMatchObject({ kind: 'url', blocked: true, reason: 'fetch-error' });
  });
  it('a standalone marker line marks the following text block blocked', () => {
    const items = parseInbox('⚠ empty-fetch\n```text\na tip\n```\n');
    expect(items[0]).toMatchObject({ kind: 'text', content: 'a tip', blocked: true, reason: 'empty-fetch' });
  });
  it('an unmarked text block is not blocked (still ingestable)', () => {
    const items = parseInbox('```text\na tip\n```\n');
    expect(items[0]).toMatchObject({ kind: 'text', blocked: false });
  });
  it('a dangling marker with no following fence attaches to nothing', () => {
    const items = parseInbox('⚠ empty-fetch\n\njust prose\n');
    expect(items).toEqual([]);
  });
});
