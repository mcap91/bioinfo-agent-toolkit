// packages/catalog-mcp/src/core/write-entry.ts
import { parseFrontmatter, serializeFrontmatter } from './frontmatter.js';
import { persistEntry } from './entry-io.js';

interface WriteEntryOptions {
  dir: string;
  entry: string;
  name: string;
  status?: 'approved' | 'draft';
  overwrite?: boolean;
}

interface WriteEntryResult {
  path: string;
  status: string;
}

export async function writeEntry(options: WriteEntryOptions): Promise<WriteEntryResult> {
  const { dir, entry, name, status = 'draft', overwrite = false } = options;

  // Force-draft mode (headless processor): clamp to draft regardless of caller.
  const forceDraft = !!process.env['CATALOG_FORCE_DRAFT'];
  const effectiveStatus: 'approved' | 'draft' = forceDraft ? 'draft' : status;

  let content = entry;
  try {
    const parsed = parseFrontmatter(content);
    // Always set status to the effective status (clamp wins over file content too).
    parsed.frontmatter.status = forceDraft ? 'draft' : (parsed.frontmatter.status as string) || status;
    if (!parsed.frontmatter.acquired) {
      parsed.frontmatter.acquired = new Date().toISOString().split('T')[0];
    }
    content = serializeFrontmatter(parsed.frontmatter, parsed.body);
  } catch {
    // persistEntry's validation will surface the parse error.
  }

  const result = await persistEntry({ dir, name, markdown: content, overwrite });
  return { path: result.path, status: effectiveStatus };
}
