// packages/catalog-mcp/__tests__/lint.test.ts
import { describe, it, expect } from 'vitest';
import { lintEntry } from '../src/core/lint.js';

describe('lintEntry', () => {
  const validFrontmatter = {
    name: 'test-tool',
    title: 'Test Tool',
    url: 'https://github.com/org/test-tool',
    category: 'skill',
    verdict: 'pilot',
    verdict_reason: 'looks promising',
    tags: ['testing'],
    reviewed: '2026-06-03',
  };

  it('returns no errors for valid entry', () => {
    const result = lintEntry('test-tool', validFrontmatter, '## What it does\n## Why this verdict\n## Mechanical details\n## Security\n');
    expect(result.errors).toEqual([]);
  });

  it('errors on missing required field', () => {
    const { title, ...noTitle } = validFrontmatter;
    const result = lintEntry('test-tool', noTitle, '');
    expect(result.errors.length).toBeGreaterThan(0);
    expect(result.errors[0]).toContain('title');
  });

  it('errors on invalid verdict', () => {
    const result = lintEntry('test-tool', { ...validFrontmatter, verdict: 'maybe' }, '');
    expect(result.errors.length).toBeGreaterThan(0);
  });

  it('warns on missing acquired (migration)', () => {
    const result = lintEntry('test-tool', validFrontmatter, '## What it does\n');
    expect(result.warnings.some((w: string) => w.includes('acquired'))).toBe(true);
  });

  it('warns on missing Security section (migration)', () => {
    const result = lintEntry('test-tool', validFrontmatter, '## What it does\n## Why this verdict\n');
    expect(result.warnings.some((w: string) => w.includes('Security'))).toBe(true);
  });

  it('errors on name mismatch with filename', () => {
    const result = lintEntry('wrong-name', validFrontmatter, '');
    expect(result.errors.some((e: string) => e.includes('name'))).toBe(true);
  });
});
