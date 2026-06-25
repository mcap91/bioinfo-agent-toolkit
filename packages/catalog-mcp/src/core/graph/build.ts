// packages/catalog-mcp/src/core/graph/build.ts
import { writeFile } from 'node:fs/promises';
import { catalogPaths } from '../config.js';
import { scanEntries } from './scan.js';
import type { GraphExport } from './types.js';

export async function buildGraph(dir: string): Promise<GraphExport> {
  const { nodes, edges } = await scanEntries(dir);

  nodes.sort((a, b) => (a.id < b.id ? -1 : a.id > b.id ? 1 : 0));
  edges.sort((a, b) => {
    const ka = `${a.source}|${a.target}|${a.relation}`;
    const kb = `${b.source}|${b.target}|${b.relation}`;
    return ka < kb ? -1 : ka > kb ? 1 : 0;
  });

  const incident = new Set<string>();
  for (const e of edges) {
    incident.add(e.source);
    incident.add(e.target);
  }
  const orphans = nodes.filter((n) => !incident.has(n.id)).map((n) => n.id);

  return { generated_at: new Date().toISOString(), nodes, edges, orphans };
}

export interface BuildResult {
  path: string;
  nodeCount: number;
  edgeCount: number;
  orphanCount: number;
}

export async function buildAndWriteGraph(dir: string): Promise<BuildResult> {
  const graph = await buildGraph(dir);
  const graphPath = catalogPaths(dir).graph;
  await writeFile(graphPath, JSON.stringify(graph, null, 2) + '\n', 'utf-8');
  return {
    path: graphPath,
    nodeCount: graph.nodes.length,
    edgeCount: graph.edges.length,
    orphanCount: graph.orphans.length,
  };
}
