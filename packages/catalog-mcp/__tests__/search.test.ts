// packages/catalog-mcp/__tests__/search.test.ts
import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import path from 'node:path';
import { searchEntries } from '../src/core/search.js';
import { mkdtemp, rm, mkdir, writeFile } from 'node:fs/promises';
import os from 'node:os';

const repoRoot = path.resolve(import.meta.dirname, '..', '..', '..');

describe('searchEntries', () => {
  it('finds entries by freeform text in tags', async () => {
    const { results } = await searchEntries({ dir: repoRoot, query: 'dispatch' });
    expect(results.length).toBeGreaterThan(0);
    expect(results.some((r) => r.name === 'agent-teams')).toBe(true);
  });

  it('filters by decision_status', async () => {
    const { results } = await searchEntries({
      dir: repoRoot,
      query: '',
      decision_status: 'open',
    });
    expect(results.every((r) => r.decision_status === 'open')).toBe(true);
  });

  it('filters by category', async () => {
    const { results } = await searchEntries({
      dir: repoRoot,
      query: '',
      category: 'reference',
    });
    expect(results.every((r) => r.category === 'reference')).toBe(true);
  });

  it('respects limit and signals truncation', async () => {
    const { results, total, truncated } = await searchEntries({
      dir: repoRoot,
      query: '',
      limit: 3,
    });
    expect(results.length).toBeLessThanOrEqual(3);
    expect(total).toBeGreaterThan(3);
    expect(truncated).toBe(true);
  });

  it('signals no truncation when all results fit', async () => {
    const { truncated } = await searchEntries({
      dir: repoRoot,
      query: '',
      limit: 9999,
    });
    expect(truncated).toBe(false);
  });

  it('includes score on every result', async () => {
    const { results } = await searchEntries({ dir: repoRoot, query: 'dispatch' });
    for (const r of results) {
      expect(typeof r.score).toBe('number');
      expect(r.score).toBeGreaterThan(0);
    }
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
    const { results } = await searchEntries({ dir, query: '' });
    expect(results.some((e) => e.name === 'plain-one')).toBe(true);
    expect(results.some((e) => e.name === 'legacy-draft')).toBe(true);
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
    const { results } = await searchEntries({ dir: tmp, query: 'optimization' });
    expect(results.map((e) => e.name)).toContain('skillopt');
  });
  it('evolve (alias) returns the whole meta-skill cluster', async () => {
    const { results } = await searchEntries({ dir: tmp, query: 'evolve' });
    const names = results.map((e) => e.name);
    expect(names).toEqual(expect.arrayContaining(['skillopt', 'openspace']));
  });
  it('multi-word query orders by score (more fields matched first)', async () => {
    const { results } = await searchEntries({ dir: tmp, query: 'skill optimization microsoft' });
    expect(results[0].name).toBe('skillopt'); // matches in more fields
  });
  it('decision_status filter accepts open for unset entries', async () => {
    const { results } = await searchEntries({ dir: tmp, query: '', decision_status: 'open' });
    expect(results.every((e) => e.decision_status === 'open')).toBe(true);
  });
  it("fields:['title'] still matches on tags", async () => {
    const { results } = await searchEntries({ dir: tmp, query: 'optimization', fields: ['title'] });
    expect(results.map((e) => e.name)).toContain('skillopt');
  });
  it('returns empty results for no match, never throws', async () => {
    const { results } = await searchEntries({ dir: tmp, query: 'zzzznotahit' });
    expect(results).toEqual([]);
  });
});

describe('field-weighted ranking', () => {
  let tmp: string;
  const mk = (dir: string, name: string, opts: { title?: string; summary?: string; tags?: string; body?: string }) =>
    writeFile(
      path.join(dir, 'catalog', 'entries', `${name}.md`),
      [
        '---',
        `name: ${name}`,
        `title: "${opts.title ?? name}"`,
        'category: skill',
        `summary: "${opts.summary ?? 'generic summary'}"`,
        `tags: [${opts.tags ?? ''}]`,
        'reviewed: 2026-06-25',
        '---',
        opts.body ?? 'generic body content',
      ].join('\n'),
      'utf-8',
    );

  beforeEach(async () => {
    tmp = await mkdtemp(path.join(os.tmpdir(), 'catalog-rank-'));
    await mkdir(path.join(tmp, 'catalog', 'entries'), { recursive: true });
  });
  afterEach(async () => { await rm(tmp, { recursive: true, force: true }); });

  it('title match ranks above body-only match', async () => {
    await mk(tmp, 'title-hit', { title: 'A2A Protocol Reference', body: 'nothing here' });
    await mk(tmp, 'body-hit', { title: 'Some Other Tool', body: 'mentions a2a briefly in passing' });
    const { results } = await searchEntries({ dir: tmp, query: 'a2a' });
    expect(results[0].name).toBe('title-hit');
    expect(results[0].score).toBeGreaterThan(results[1].score);
  });

  it('tag match ranks above body-only match', async () => {
    await mk(tmp, 'tagged', { title: 'Protocol Lib', tags: 'a2a, grpc', body: 'nothing' });
    await mk(tmp, 'body-only', { title: 'Some Lib', body: 'uses a2a internally for stuff' });
    const { results } = await searchEntries({ dir: tmp, query: 'a2a' });
    expect(results[0].name).toBe('tagged');
    expect(results[0].score).toBeGreaterThan(results[1].score);
  });

  it('multi-field match accumulates score', async () => {
    await mk(tmp, 'deep-match', {
      title: 'A2A Gateway',
      summary: 'agent-to-agent a2a protocol',
      tags: 'a2a',
      body: 'full a2a implementation',
    });
    await mk(tmp, 'title-only', { title: 'A2A Reference', body: 'nothing relevant' });
    const { results } = await searchEntries({ dir: tmp, query: 'a2a' });
    expect(results[0].name).toBe('deep-match');
    expect(results[0].score).toBeGreaterThan(results[1].score);
  });

  it('empty query returns all entries with score 0', async () => {
    await mk(tmp, 'one', {});
    await mk(tmp, 'two', {});
    const { results } = await searchEntries({ dir: tmp, query: '' });
    expect(results).toHaveLength(2);
    expect(results.every((r) => r.score === 0)).toBe(true);
  });

  it('truncation reports correct total', async () => {
    await mk(tmp, 'one', {});
    await mk(tmp, 'two', {});
    await mk(tmp, 'three', {});
    const { results, total, truncated } = await searchEntries({ dir: tmp, query: '', limit: 2 });
    expect(results).toHaveLength(2);
    expect(total).toBe(3);
    expect(truncated).toBe(true);
  });
});
