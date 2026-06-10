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
  try {
    const parsed = parseFrontmatter(content);
    if (!parsed.frontmatter.acquired) {
      parsed.frontmatter.acquired = new Date().toISOString().split('T')[0];
    }
    content = serializeFrontmatter(parsed.frontmatter, parsed.body);
  } catch {
    // persistEntry's validation will surface the parse error.
  }

  const result = await persistEntry({ dir, name, markdown: content, overwrite });
  return { path: result.path };
}
