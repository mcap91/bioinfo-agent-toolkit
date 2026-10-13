// packages/catalog-mcp/__tests__/frontmatter.test.ts
import { describe, it, expect } from 'vitest';
import { parseFrontmatter, serializeFrontmatter } from '../src/core/frontmatter.js';

describe('parseFrontmatter', () => {
  it('parses basic frontmatter with scalar fields', () => {
    const content = '---\nname: test\ntitle: "Test Tool"\n---\nBody text\n';
    const result = parseFrontmatter(content);
    expect(result.frontmatter.name).toBe('test');
    expect(result.frontmatter.title).toBe('Test Tool');
    expect(result.body).toBe('Body text\n');
  });

  it('parses flow arrays', () => {
    const content = '---\ntags: [a, b, c]\n---\n';
    const result = parseFrontmatter(content);
    expect(result.frontmatter.tags).toEqual(['a', 'b', 'c']);
  });

  it('parses empty flow arrays', () => {
    const content = '---\ntags: []\n---\n';
    const result = parseFrontmatter(content);
    expect(result.frontmatter.tags).toEqual([]);
  });

  it('parses block arrays', () => {
    const content = '---\ntags:\n  - alpha\n  - beta\n---\n';
    const result = parseFrontmatter(content);
    expect(result.frontmatter.tags).toEqual(['alpha', 'beta']);
  });

  it('handles unquoted URLs as scalar values', () => {
    const content = '---\nurl: https://github.com/org/tool\n---\n';
    const result = parseFrontmatter(content);
    expect(result.frontmatter.url).toBe('https://github.com/org/tool');
  });

  it('returns null for empty values', () => {
    const content = '---\nurl: \n---\n';
    const result = parseFrontmatter(content);
    expect(result.frontmatter.url).toBeNull();
  });

  it('handles CRLF line endings', () => {
    const content = '---\r\nname: test\r\n---\r\nBody\r\n';
    const result = parseFrontmatter(content);
    expect(result.frontmatter.name).toBe('test');
  });

  it('throws on missing frontmatter', () => {
    expect(() => parseFrontmatter('No frontmatter here')).toThrow();
  });
});

describe('serializeFrontmatter round-trip', () => {
  it('preserves content through parse-serialize cycle', () => {
    const original = '---\nname: test\ntitle: "Test Tool"\ntags: [a, b]\n---\nBody\n';
    const parsed = parseFrontmatter(original);
    const serialized = serializeFrontmatter(parsed.frontmatter, parsed.body);
    const reparsed = parseFrontmatter(serialized);
    expect(reparsed.frontmatter).toEqual(parsed.frontmatter);
    expect(reparsed.body).toBe(parsed.body);
  });

  it('round-trips values containing double quotes', () => {
    const fm = {
      name: 'quoted-tool',
      install: 'pip install "some-pkg[extra]"',
      summary: 'Has "quotes" inside',
    };
    const serialized = serializeFrontmatter(fm, 'Body\n');
    const reparsed = parseFrontmatter(serialized);
    expect(reparsed.frontmatter.install).toBe('pip install "some-pkg[extra]"');
    expect(reparsed.frontmatter.summary).toBe('Has "quotes" inside');
  });

  it('round-trips values containing backslashes and special YAML characters', () => {
    const fm = {
      name: 'special-chars',
      summary: 'path: C:\\Users\\test # comment-like',
      tags: ["it's-a-test", 'key: value'],
    };
    const serialized = serializeFrontmatter(fm, '');
    const reparsed = parseFrontmatter(serialized);
    expect(reparsed.frontmatter).toEqual(fm);
  });
});
