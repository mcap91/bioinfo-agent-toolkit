// packages/catalog-mcp/src/core/write-entry.ts
import { parseFrontmatter, serializeFrontmatter } from './frontmatter.js';
import { persistEntry } from './entry-io.js';

interface WriteEntryOptions {
  dir: string;
  entry: string;
  name: string;
  overwrite?: boolean;
}

interface WriteEntryResult {
  path: string;
}

export async function writeEntry(options: WriteEntryOptions): Promise<WriteEntryResult> {
  const { dir, entry, name, overwrite = false } = options;

  let content = entry;
  let parsed: ReturnType<typeof parseFrontmatter> | undefined;
  try {
    parsed = parseFrontmatter(content);
  } catch {
    parsed = undefined; // persistEntry's validation will surface the parse error.
  }

  if (parsed) {
    // "unknown" is legacy-only (OR-4): it marks pre-existing entries with no recorded
    // provenance. A new entry must always derive a real source from source_url, or be "text".
    if (parsed.frontmatter.source === 'unknown') {
      throw new Error(
        'source: "unknown" is reserved for legacy entries with no recorded provenance. ' +
          'Set source_url, or source: "text" for a url-less item.',
      );
    }
    if (!parsed.frontmatter.acquired) {
      parsed.frontmatter.acquired = new Date().toISOString().split('T')[0];
    }
    content = serializeFrontmatter(parsed.frontmatter, parsed.body);
  }

  const result = await persistEntry({ dir, name, markdown: content, overwrite });
  return { path: result.path };
}
