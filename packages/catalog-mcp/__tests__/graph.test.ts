// packages/catalog-mcp/__tests__/graph.test.ts
import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import path from 'node:path';
import { mkdtemp, rm, mkdir, writeFile, readFile } from 'node:fs/promises';
import os from 'node:os';
import { scanEntries } from '../src/core/graph/scan.js';
import { buildGraph, buildAndWriteGraph } from '../src/core/graph/build.js';
import { queryNeighbors, queryTopic } from '../src/core/graph/query.js';

const repoRoot = path.resolve(import.meta.dirname, '..', '..', '..');

function mkEntry(
  dir: string,
  name: string,
  opts: { title?: string; tags?: string[]; category?: string; overlaps?: string[]; supersedes?: string[] },
) {
  const fm = [
    '---',
    `name: ${name}`,
    `title: "${opts.title ?? name}"`,
    `category: ${opts.category ?? 'skill'}`,
    `summary: "test entry"`,
    `tags: [${(opts.tags ?? ['test']).join(', ')}]`,
    `reviewed: 2026-06-25`,
  ];
  if (opts.overlaps?.length) fm.push(`overlaps: [${opts.overlaps.join(', ')}]`);
  if (opts.supersedes?.length) fm.push(`supersedes: [${opts.supersedes.join(', ')}]`);
  fm.push('---', 'body');
  return writeFile(path.join(dir, 'catalog', 'entries', `${name}.md`), fm.join('\n'), 'utf-8');
}

// ── scanEntries ─────────────────────────────────────────────────────

describe('scanEntries', () => {
  let tmp: string;

  beforeEach(async () => {
    tmp = await mkdtemp(path.join(os.tmpdir(), 'catalog-graph-'));
    await mkdir(path.join(tmp, 'catalog', 'entries'), { recursive: true });
    await mkEntry(tmp, 'alpha', { tags: ['multi-agent', 'orchestration'], category: 'framework', overlaps: ['beta'] });
    await mkEntry(tmp, 'beta', { tags: ['multi-agent', 'local'], category: 'framework', overlaps: ['alpha'] });
    await mkEntry(tmp, 'gamma', { tags: ['orchestration', 'visualization'], category: 'cli-tool' });
    await mkEntry(tmp, 'delta', { tags: ['local', 'llm'], category: 'reference', supersedes: ['epsilon'] });
  });

  afterEach(async () => { await rm(tmp, { recursive: true, force: true }); });

  it('creates entry nodes for each catalog entry', async () => {
    const { nodes } = await scanEntries(tmp);
    const entries = nodes.filter((n) => n.kind === 'entry' && n.exists);
    expect(entries.map((n) => n.id).sort()).toEqual(['alpha', 'beta', 'delta', 'gamma']);
  });

  it('creates tag nodes for each unique tag', async () => {
    const { nodes } = await scanEntries(tmp);
    const tags = nodes.filter((n) => n.kind === 'tag').map((n) => n.id).sort();
    expect(tags).toEqual(['tag:llm', 'tag:local', 'tag:multi-agent', 'tag:orchestration', 'tag:visualization']);
  });

  it('creates category nodes for each unique category', async () => {
    const { nodes } = await scanEntries(tmp);
    const cats = nodes.filter((n) => n.kind === 'category').map((n) => n.id).sort();
    expect(cats).toEqual(['cat:cli-tool', 'cat:framework', 'cat:reference']);
  });

  it('creates tagged edges from entries to tags', async () => {
    const { edges } = await scanEntries(tmp);
    const tagged = edges.filter((e) => e.relation === 'tagged');
    expect(tagged).toContainEqual({ source: 'alpha', target: 'tag:multi-agent', relation: 'tagged' });
    expect(tagged).toContainEqual({ source: 'alpha', target: 'tag:orchestration', relation: 'tagged' });
  });

  it('creates categorized edges from entries to categories', async () => {
    const { edges } = await scanEntries(tmp);
    const catEdges = edges.filter((e) => e.relation === 'categorized');
    expect(catEdges).toContainEqual({ source: 'alpha', target: 'cat:framework', relation: 'categorized' });
    expect(catEdges).toContainEqual({ source: 'gamma', target: 'cat:cli-tool', relation: 'categorized' });
  });

  it('creates overlaps edges between entries', async () => {
    const { edges } = await scanEntries(tmp);
    const overlaps = edges.filter((e) => e.relation === 'overlaps');
    expect(overlaps).toContainEqual({ source: 'alpha', target: 'beta', relation: 'overlaps' });
    expect(overlaps).toContainEqual({ source: 'beta', target: 'alpha', relation: 'overlaps' });
  });

  it('creates supersedes edges and ghost nodes for missing targets', async () => {
    const { nodes, edges } = await scanEntries(tmp);
    expect(edges).toContainEqual({ source: 'delta', target: 'epsilon', relation: 'supersedes' });
    const ghost = nodes.find((n) => n.id === 'epsilon');
    expect(ghost).toBeDefined();
    expect(ghost!.kind).toBe('entry');
    expect(ghost!.exists).toBe(false);
  });

  it('entry nodes carry title, category, decision_status', async () => {
    const { nodes } = await scanEntries(tmp);
    const alpha = nodes.find((n) => n.id === 'alpha');
    expect(alpha!.title).toBe('alpha');
    expect(alpha!.category).toBe('framework');
    expect(alpha!.decision_status).toBe('open');
  });
});

// ── buildGraph ──────────────────────────────────────────────────────

describe('buildGraph', () => {
  let tmp: string;

  beforeEach(async () => {
    tmp = await mkdtemp(path.join(os.tmpdir(), 'catalog-graph-b-'));
    await mkdir(path.join(tmp, 'catalog', 'entries'), { recursive: true });
    await mkEntry(tmp, 'alpha', { tags: ['multi-agent'], category: 'framework', overlaps: ['beta'] });
    await mkEntry(tmp, 'beta', { tags: ['multi-agent'], category: 'framework' });
  });

  afterEach(async () => { await rm(tmp, { recursive: true, force: true }); });

  it('produces deterministically sorted nodes and edges', async () => {
    const g = await buildGraph(tmp);
    const nodeIds = g.nodes.map((n) => n.id);
    expect(nodeIds).toEqual([...nodeIds].sort());
    const edgeKeys = g.edges.map((e) => `${e.source}|${e.target}|${e.relation}`);
    expect(edgeKeys).toEqual([...edgeKeys].sort());
  });

  it('identifies orphan nodes', async () => {
    const g = await buildGraph(tmp);
    expect(Array.isArray(g.orphans)).toBe(true);
  });

  it('writes .graph.json to catalog/', async () => {
    const result = await buildAndWriteGraph(tmp);
    expect(result.path).toContain('.graph.json');
    const raw = await readFile(result.path, 'utf-8');
    const parsed = JSON.parse(raw);
    expect(parsed.nodes).toBeDefined();
    expect(parsed.edges).toBeDefined();
    expect(parsed.generated_at).toBeDefined();
  });

  it('returns node and edge counts', async () => {
    const result = await buildAndWriteGraph(tmp);
    // 2 entries + 1 tag + 1 category = 4 nodes
    expect(result.nodeCount).toBe(4);
    // 2 tagged + 2 categorized + 1 overlaps = 5 edges
    expect(result.edgeCount).toBe(5);
  });
});

// ── queryNeighbors ──────────────────────────────────────────────────

describe('queryNeighbors', () => {
  let tmp: string;

  beforeEach(async () => {
    tmp = await mkdtemp(path.join(os.tmpdir(), 'catalog-graph-q-'));
    await mkdir(path.join(tmp, 'catalog', 'entries'), { recursive: true });
    await mkEntry(tmp, 'alpha', { tags: ['multi-agent', 'orchestration'], category: 'framework', overlaps: ['beta'] });
    await mkEntry(tmp, 'beta', { tags: ['multi-agent', 'local'], category: 'framework', overlaps: ['alpha'] });
    await mkEntry(tmp, 'gamma', { tags: ['orchestration', 'visualization'], category: 'cli-tool' });
    await mkEntry(tmp, 'delta', { tags: ['local', 'llm'], category: 'reference' });
  });

  afterEach(async () => { await rm(tmp, { recursive: true, force: true }); });

  it('returns direct edge neighbors first', async () => {
    const graph = await buildGraph(tmp);
    const results = queryNeighbors(graph, 'alpha');
    expect(results[0].name).toBe('beta');
    expect(results[0].relation).toBe('overlaps');
    expect(results[0].hops).toBe(1);
  });

  it('returns shared-tag neighbors at hop 2', async () => {
    const graph = await buildGraph(tmp);
    const results = queryNeighbors(graph, 'alpha');
    const gamma = results.find((r) => r.name === 'gamma');
    expect(gamma).toBeDefined();
    expect(gamma!.relation).toBe('shared-tag');
    expect(gamma!.sharedLabels).toContain('orchestration');
    expect(gamma!.hops).toBe(2);
  });

  it('direct edge wins over shared-category for same entry', async () => {
    const graph = await buildGraph(tmp);
    const results = queryNeighbors(graph, 'alpha');
    const betaResult = results.find((r) => r.name === 'beta');
    expect(betaResult!.relation).toBe('overlaps');
  });

  it('ranks direct > shared-tag > shared-category', async () => {
    const graph = await buildGraph(tmp);
    const results = queryNeighbors(graph, 'alpha');
    const relations = results.map((r) => r.relation);
    const directIdx = relations.indexOf('overlaps');
    const tagIdx = relations.indexOf('shared-tag');
    const catIdx = relations.indexOf('shared-category');
    if (directIdx >= 0 && tagIdx >= 0) expect(directIdx).toBeLessThan(tagIdx);
    if (tagIdx >= 0 && catIdx >= 0) expect(tagIdx).toBeLessThan(catIdx);
  });

  it('does not include the queried entry in results', async () => {
    const graph = await buildGraph(tmp);
    const results = queryNeighbors(graph, 'alpha');
    expect(results.every((r) => r.name !== 'alpha')).toBe(true);
  });

  it('returns empty array for unknown entry', async () => {
    const graph = await buildGraph(tmp);
    expect(queryNeighbors(graph, 'nonexistent')).toEqual([]);
  });

  it('respects limit', async () => {
    const graph = await buildGraph(tmp);
    const results = queryNeighbors(graph, 'alpha', { limit: 1 });
    expect(results).toHaveLength(1);
  });
});

// ── queryTopic ──────────────────────────────────────────────────────

describe('queryTopic', () => {
  let tmp: string;

  beforeEach(async () => {
    tmp = await mkdtemp(path.join(os.tmpdir(), 'catalog-graph-t-'));
    await mkdir(path.join(tmp, 'catalog', 'entries'), { recursive: true });
    await mkEntry(tmp, 'alpha', { tags: ['multi-agent', 'orchestration'], category: 'framework' });
    await mkEntry(tmp, 'beta', { tags: ['multi-agent', 'local'], category: 'framework' });
    await mkEntry(tmp, 'gamma', { tags: ['orchestration', 'visualization'], category: 'cli-tool' });
    await mkEntry(tmp, 'delta', { tags: ['local', 'llm'], category: 'reference' });
  });

  afterEach(async () => { await rm(tmp, { recursive: true, force: true }); });

  it('finds entries by matching tag', async () => {
    const graph = await buildGraph(tmp);
    const results = queryTopic(graph, 'multi-agent');
    const names = results.map((r) => r.name);
    expect(names).toContain('alpha');
    expect(names).toContain('beta');
    expect(names).not.toContain('gamma');
  });

  it('finds entries by matching category', async () => {
    const graph = await buildGraph(tmp);
    const results = queryTopic(graph, 'framework');
    const names = results.map((r) => r.name);
    expect(names).toContain('alpha');
    expect(names).toContain('beta');
  });

  it('ranks by connection count', async () => {
    const graph = await buildGraph(tmp);
    const results = queryTopic(graph, 'multi');
    expect(results[0].matchedNodes).toContain('tag:multi-agent');
  });

  it('does substring matching on tag/category labels', async () => {
    const graph = await buildGraph(tmp);
    const results = queryTopic(graph, 'orch');
    const names = results.map((r) => r.name);
    expect(names).toContain('alpha');
    expect(names).toContain('gamma');
  });

  it('is case-insensitive', async () => {
    const graph = await buildGraph(tmp);
    const results = queryTopic(graph, 'MULTI-AGENT');
    expect(results.map((r) => r.name)).toContain('alpha');
  });

  it('returns empty array for no match', async () => {
    const graph = await buildGraph(tmp);
    expect(queryTopic(graph, 'zzzznotahit')).toEqual([]);
  });

  it('includes score and matchedNodes in results', async () => {
    const graph = await buildGraph(tmp);
    const results = queryTopic(graph, 'orchestration');
    for (const r of results) {
      expect(typeof r.score).toBe('number');
      expect(r.score).toBeGreaterThan(0);
      expect(r.matchedNodes.length).toBeGreaterThan(0);
    }
  });

  it('respects limit', async () => {
    const graph = await buildGraph(tmp);
    const results = queryTopic(graph, 'local', { limit: 1 });
    expect(results).toHaveLength(1);
  });
});

// ── Integration: real catalog ───────────────────────────────────────

describe('integration: real catalog', () => {
  it('builds a graph from the actual catalog entries', async () => {
    const graph = await buildGraph(repoRoot);
    const entries = graph.nodes.filter((n) => n.kind === 'entry');
    expect(entries.length).toBeGreaterThan(100);
    expect(graph.nodes.some((n) => n.kind === 'tag')).toBe(true);
    expect(graph.nodes.some((n) => n.kind === 'category')).toBe(true);
    expect(graph.edges.length).toBeGreaterThan(entries.length);
  });

  it('queryNeighbors returns results for a known entry', async () => {
    const graph = await buildGraph(repoRoot);
    const results = queryNeighbors(graph, 'mycelium');
    expect(results.length).toBeGreaterThan(0);
    expect(results.some((r) => r.relation === 'shared-category' || r.relation === 'shared-tag')).toBe(true);
  });

  it('queryTopic finds entries for multi-agent', async () => {
    const graph = await buildGraph(repoRoot);
    const results = queryTopic(graph, 'multi-agent');
    expect(results.length).toBeGreaterThan(0);
    expect(results.every((r) => r.score > 0)).toBe(true);
    expect(results.every((r) => r.matchedNodes.length > 0)).toBe(true);
  });

  it('queryTopic finds entries for orchestration', async () => {
    const graph = await buildGraph(repoRoot);
    const results = queryTopic(graph, 'orchestration');
    expect(results.length).toBeGreaterThan(0);
  });
});
