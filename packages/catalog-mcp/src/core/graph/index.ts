// packages/catalog-mcp/src/core/graph/index.ts
export type { NodeKind, EdgeRelation, GraphNode, GraphEdge, GraphExport } from './types.js';
export { scanEntries } from './scan.js';
export { buildGraph, buildAndWriteGraph } from './build.js';
export { queryNeighbors, queryTopic } from './query.js';
export type { NeighborResult, TopicResult } from './query.js';
