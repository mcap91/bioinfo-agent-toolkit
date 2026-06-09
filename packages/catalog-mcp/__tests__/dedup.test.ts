import { describe, it, expect } from 'vitest';
import { normalizeContent, contentHash, dedupKey } from '../src/core/dedup.js';

describe('normalizeContent', () => {
  it('trims, collapses whitespace, normalizes EOL', () => {
    expect(normalizeContent('  a\r\n b   c \n')).toBe('a b c');
  });
});

describe('contentHash', () => {
  it('is stable across whitespace-only variants', () => {
    expect(contentHash('hello   world')).toBe(contentHash('hello world\n'));
  });
  it('differs for different content', () => {
    expect(contentHash('a')).not.toBe(contentHash('b'));
  });
  it('returns a 16-char hex slice', () => {
    expect(contentHash('x')).toMatch(/^[0-9a-f]{16}$/);
  });
});

describe('dedupKey', () => {
  it('uses url when present', () => {
    expect(dedupKey({ url: 'https://x.com/a', content: 'hi' })).toBe('https://x.com/a');
  });
  it('uses content hash when url absent', () => {
    expect(dedupKey({ content: 'hi there' })).toBe(`content:${contentHash('hi there')}`);
  });
  it('throws when neither present', () => {
    expect(() => dedupKey({})).toThrow(/url or content/);
  });
});
