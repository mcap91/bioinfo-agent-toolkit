// packages/catalog-mcp/__tests__/search.test.ts
import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import path from 'node:path';
import { searchEntries } from '../src/core/search.js';
import { mkdtemp, rm, mkdir, writeFile } from 'node:fs/promises';
import os from 'node:os';

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

describe('search ignores legacy status frontmatter (status removed in v2.1.0)', () => {
  let dir: string;
  beforeEach(async () => {
    dir = await mkdtemp(path.join(os.tmpdir(), 'catalog-s-'));
    await mkdir(path.join(dir, 'catalog', 'entries'), { recursive: true });
    const mk = (name: string, extra = '') =>
      writeFile(
        path.join(dir, 'catalog', 'entries', `${name}.md`),
        `---\nname: ${name}\ntitle: "${name}"\ncategory: skill\nverdict: pilot\nverdict_reason: x\n${extra}tags: [t]\nreviewed: 2026-06-08\n---\nbody\n`,
        'utf-8',
      );
    await mk('plain-one');
    await mk('legacy-draft', 'status: draft\n');
  });
  afterEach(async () => { await rm(dir, { recursive: true, force: true }); });

  it('returns all entries regardless of any legacy status line', async () => {
    const r = await searchEntries({ dir, query: '' });
    expect(r.some((e) => e.name === 'plain-one')).toBe(true);
    expect(r.some((e) => e.name === 'legacy-draft')).toBe(true);
  });
});
