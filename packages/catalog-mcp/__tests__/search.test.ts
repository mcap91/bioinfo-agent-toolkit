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

  it('filters by decision_status', async () => {
    const results = await searchEntries({
      dir: repoRoot,
      query: '',
      decision_status: 'open',
    });
    expect(results.every((r) => r.decision_status === 'open')).toBe(true);
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
        `---\nname: ${name}\ntitle: "${name}"\ncategory: skill\nsummary: x\n${extra}tags: [t]\nreviewed: 2026-06-08\n---\nbody\n`,
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

describe('searchEntries coverage + taxonomy', () => {
  let tmp: string;
  beforeEach(async () => {
    tmp = await mkdtemp(path.join(os.tmpdir(), 'catalog-cov-'));
    await mkdir(path.join(tmp, 'catalog', 'entries'), { recursive: true });
    await writeFile(
      path.join(tmp, 'catalog', 'taxonomy.json'),
      JSON.stringify({ canonical: { 'meta-skill': ['skill-optimization', 'skill-evolution', 'evolve', 'evolution'] } }),
      'utf-8',
    );
    const mk = (name: string, summary: string, tags: string) =>
      writeFile(
        path.join(tmp, 'catalog', 'entries', `${name}.md`),
        `---\nname: ${name}\ntitle: "${name}"\ncategory: skill\nsummary: "${summary}"\ntags: [${tags}]\nreviewed: 2026-06-16\n---\nbody\n`,
        'utf-8',
      );
    // skillopt: tag skill-optimization (-> tokens skill, optimization) + 'microsoft' in summary
    await mk('skillopt', 'microsoft skill optimizer', 'skill-optimization');
    // openspace: tag skill-evolution
    await mk('openspace', 'self-evolving skills', 'skill-evolution');
  });
  afterEach(async () => { await rm(tmp, { recursive: true, force: true }); });

  it('optimization finds skill-optimization via tokenized tag (non-alias)', async () => {
    const r = await searchEntries({ dir: tmp, query: 'optimization' });
    expect(r.map((e) => e.name)).toContain('skillopt');
  });
  it('evolve (alias) returns the whole meta-skill cluster', async () => {
    const r = await searchEntries({ dir: tmp, query: 'evolve' });
    const names = r.map((e) => e.name);
    expect(names).toEqual(expect.arrayContaining(['skillopt', 'openspace']));
  });
  it('multi-word query orders by coverage (more terms matched first)', async () => {
    const r = await searchEntries({ dir: tmp, query: 'skill optimization microsoft' });
    expect(r[0].name).toBe('skillopt'); // matches all three
  });
  it('decision_status filter accepts open for unset entries', async () => {
    const r = await searchEntries({ dir: tmp, query: '', decision_status: 'open' });
    expect(r.every((e) => e.decision_status === 'open')).toBe(true);
  });
  it("fields:['title'] still matches on tags", async () => {
    const r = await searchEntries({ dir: tmp, query: 'optimization', fields: ['title'] });
    expect(r.map((e) => e.name)).toContain('skillopt');
  });
  it('returns [] for no match, never throws', async () => {
    expect(await searchEntries({ dir: tmp, query: 'zzzznotahit' })).toEqual([]);
  });
});
