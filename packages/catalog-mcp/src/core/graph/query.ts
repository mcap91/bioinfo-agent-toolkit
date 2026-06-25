// packages/catalog-mcp/src/core/graph/query.ts
import type { GraphExport } from './types.js';

export interface NeighborResult {
  name: string;
  title: string;
  relation: string;
  sharedLabels: string[];
  hops: number;
}

const DIRECT_RELATIONS = new Set(['overlaps', 'supersedes', 'related']);

export function queryNeighbors(
  graph: GraphExport,
  entryName: string,
  opts?: { limit?: number },
): NeighborResult[] {
  const entryNode = graph.nodes.find((n) => n.id === entryName && n.kind === 'entry');
  if (!entryNode) return [];

  const nodeMap = new Map(graph.nodes.map((n) => [n.id, n]));
  const seen = new Map<string, NeighborResult>();

  // Pass 1: direct edges (hop 1) — bidirectional
  for (const edge of graph.edges) {
    if (!DIRECT_RELATIONS.has(edge.relation)) continue;
    let targetName: string | null = null;
    if (edge.source === entryName) targetName = edge.target;
    if (edge.target === entryName) targetName = edge.source;
    if (!targetName || targetName === entryName) continue;

    if (!seen.has(targetName)) {
      const targetNode = nodeMap.get(targetName);
      seen.set(targetName, {
        name: targetName,
        title: targetNode?.title ?? targetName,
        relation: edge.relation,
        sharedLabels: [],
        hops: 1,
      });
    }
  }

  // Pass 2: shared tags (hop 2)
  const myTags = graph.edges
    .filter((e) => e.source === entryName && e.relation === 'tagged')
    .map((e) => e.target);

  const tagNeighbors = new Map<string, string[]>();
  for (const tagId of myTags) {
    const tagLabel = tagId.replace(/^tag:/, '');
    for (const edge of graph.edges) {
      if (edge.target === tagId && edge.relation === 'tagged' && edge.source !== entryName) {
        const list = tagNeighbors.get(edge.source) ?? [];
        list.push(tagLabel);
        tagNeighbors.set(edge.source, list);
      }
    }
  }

  const tagEntries = [...tagNeighbors.entries()].sort((a, b) => b[1].length - a[1].length);
  for (const [name, labels] of tagEntries) {
    if (seen.has(name)) continue;
    const node = nodeMap.get(name);
    seen.set(name, {
      name,
      title: node?.title ?? name,
      relation: 'shared-tag',
      sharedLabels: labels,
      hops: 2,
    });
  }

  // Pass 3: shared category (hop 2)
  const myCat = graph.edges.find(
    (e) => e.source === entryName && e.relation === 'categorized',
  )?.target;

  if (myCat) {
    const catLabel = myCat.replace(/^cat:/, '');
    for (const edge of graph.edges) {
      if (edge.target === myCat && edge.relation === 'categorized' && edge.source !== entryName) {
        if (seen.has(edge.source)) continue;
        const node = nodeMap.get(edge.source);
        seen.set(edge.source, {
          name: edge.source,
          title: node?.title ?? edge.source,
          relation: 'shared-category',
          sharedLabels: [catLabel],
          hops: 2,
        });
      }
    }
  }

  const results = [...seen.values()];
  return results.slice(0, opts?.limit ?? 50);
}

export interface TopicResult {
  name: string;
  title: string;
  score: number;
  matchedNodes: string[];
}

export function queryTopic(
  graph: GraphExport,
  term: string,
  opts?: { limit?: number },
): TopicResult[] {
  const termLower = term.toLowerCase();

  const matchingNodes = graph.nodes
    .filter((n) => {
      if (n.kind === 'tag') return n.id.replace(/^tag:/, '').toLowerCase().includes(termLower);
      if (n.kind === 'category') return n.id.replace(/^cat:/, '').toLowerCase().includes(termLower);
      return false;
    })
    .map((n) => n.id);

  if (matchingNodes.length === 0) return [];

  const matchSet = new Set(matchingNodes);
  const entryScores = new Map<string, { score: number; matchedNodes: string[] }>();

  for (const edge of graph.edges) {
    if ((edge.relation === 'tagged' || edge.relation === 'categorized') && matchSet.has(edge.target)) {
      const entry = entryScores.get(edge.source) ?? { score: 0, matchedNodes: [] };
      entry.score++;
      entry.matchedNodes.push(edge.target);
      entryScores.set(edge.source, entry);
    }
  }

  const nodeMap = new Map(graph.nodes.map((n) => [n.id, n]));
  const results: TopicResult[] = [...entryScores.entries()]
    .map(([name, data]) => ({
      name,
      title: nodeMap.get(name)?.title ?? name,
      score: data.score,
      matchedNodes: data.matchedNodes,
    }))
    .sort((a, b) => b.score - a.score || (a.name < b.name ? -1 : 1));

  return results.slice(0, opts?.limit ?? 50);
}
