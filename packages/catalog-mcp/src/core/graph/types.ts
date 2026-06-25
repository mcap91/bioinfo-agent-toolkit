// packages/catalog-mcp/src/core/graph/types.ts
export type NodeKind = 'entry' | 'tag' | 'category';

export type EdgeRelation =
  | 'tagged'
  | 'categorized'
  | 'overlaps'
  | 'supersedes'
  | 'related';

export interface GraphNode {
  id: string;
  kind: NodeKind;
  title?: string;
  url?: string;
  summary?: string;
  category?: string;
  decision_status?: string;
  exists: boolean;
}

export interface GraphEdge {
  source: string;
  target: string;
  relation: EdgeRelation;
}

export interface GraphExport {
  generated_at: string;
  nodes: GraphNode[];
  edges: GraphEdge[];
  orphans: string[];
}
