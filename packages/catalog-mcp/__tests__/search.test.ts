// packages/catalog-mcp/__tests__/search.test.ts
import { describe, it, expect } from 'vitest';
import path from 'node:path';
import { searchEntries } from '../src/core/search.js';

const repoRoot = path.resolve(import.meta.dirname, '..', '..', '..');

describe('searchEntries', () => {
  it('finds entries by freeform text in tags', async () => {
    const results = await searchEntries({ dir: repoRoot, query: 'dispatch' });
    expect(results.length).toBeGreaterThan(0);
    expect(results.some((r) => r.name === 'agent-teams')).toBe(true);
  });

  it('filters by verdict', async () => {
    const results = await searchEntries({
      dir: repoRoot,
      query: '',
      verdict: 'adopt',
    });
    expect(results.every((r) => r.verdict === 'adopt')).toBe(true);
  });

  it('filters by category', async () => {
    const results = await searchEntries({
      dir: repoRoot,
      query: '',
      category: 'reference',
    });
    expect(results.every((r) => r.category === 'reference')).toBe(true);
  });

  it('respects limit', async () => {
    const results = await searchEntries({
      dir: repoRoot,
      query: '',
      limit: 3,
    });
    expect(results.length).toBeLessThanOrEqual(3);
  });
});
