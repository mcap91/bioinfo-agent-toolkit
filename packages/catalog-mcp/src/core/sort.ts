// packages/catalog-mcp/src/core/sort.ts
// Ordinal comparators (code-point order). Do NOT use localeCompare — it diverges
// from the Python-generated catalog/index.md ordering and is locale-dependent.
export function cmpTitleLower(a: string, b: string): number {
  const al = a.toLowerCase();
  const bl = b.toLowerCase();
  return al < bl ? -1 : al > bl ? 1 : 0;
}
export function cmpRaw(a: string, b: string): number {
  return a < b ? -1 : a > b ? 1 : 0;
}
