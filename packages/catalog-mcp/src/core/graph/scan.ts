// packages/catalog-mcp/src/core/graph/scan.ts
import { readAllEntries } from '../frontmatter.js';
import { catalogPaths } from '../config.js';
import type { GraphNode, GraphEdge, EdgeRelation } from './types.js';

export interface ScanResult {
  nodes: GraphNode[];
  edges: GraphEdge[];
}

const ENTRY_EDGE_FIELDS: { field: string; relation: EdgeRelation }[] = [
  { field: 'overlaps', relation: 'overlaps' },
  { field: 'supersedes', relation: 'supersedes' },
  { field: 'related', relation: 'related' },
];

export async function scanEntries(dir: string): Promise<ScanResult> {
  const paths = catalogPaths(dir);
  const raw = await readAllEntries(paths.entries);

  const nodes: GraphNode[] = [];
  const edges: GraphEdge[] = [];
  const tagsSeen = new Set<string>();
  const catsSeen = new Set<string>();

  for (const [name, parsed] of raw) {
    const fm = parsed.frontmatter;

    nodes.push({
      id: name,
      kind: 'entry',
      title: fm.title as string,
      url: fm.url as string | undefined,
      summary: fm.summary as string,
      category: fm.category as string,
      decision_status: (fm.decision_status as string | undefined) ?? 'open',
      exists: true,
    });

    const tags = (fm.tags as string[]) ?? [];
    for (const tag of tags) {
      const tagId = `tag:${tag}`;
      tagsSeen.add(tag);
      edges.push({ source: name, target: tagId, relation: 'tagged' });
    }

    const cat = fm.category as string;
    const catId = `cat:${cat}`;
    catsSeen.add(cat);
    edges.push({ source: name, target: catId, relation: 'categorized' });

    for (const { field, relation } of ENTRY_EDGE_FIELDS) {
      const targets = (fm[field] as string[] | undefined) ?? [];
      for (const target of targets) {
        edges.push({ source: name, target, relation });
      }
    }
  }

  for (const tag of tagsSeen) {
    nodes.push({ id: `tag:${tag}`, kind: 'tag', exists: true });
  }
  for (const cat of catsSeen) {
    nodes.push({ id: `cat:${cat}`, kind: 'category', exists: true });
  }

  // Ghost nodes for edge targets not on disk
  const nodeIds = new Set(nodes.map((n) => n.id));
  for (const edge of edges) {
    if (!nodeIds.has(edge.target)) {
      nodes.push({ id: edge.target, kind: 'entry', exists: false });
      nodeIds.add(edge.target);
    }
  }

  return { nodes, edges };
}
