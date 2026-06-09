// packages/catalog-mcp/src/core/force-draft.ts
/** True when the catalog server runs in force-draft mode (headless processor).
 *  When set, no tool path may publish or approve drafts (write-entry clamps,
 *  index forces include_drafts=false, review refuses approve/reject). */
export function isForceDraft(): boolean {
  return !!process.env['CATALOG_FORCE_DRAFT'];
}
