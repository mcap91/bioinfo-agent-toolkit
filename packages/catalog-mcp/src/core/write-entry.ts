// packages/catalog-mcp/src/core/write-entry.ts
import { writeFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { catalogPaths } from './config.js';
import { validateEntry } from './validate-entry.js';
import { parseFrontmatter, serializeFrontmatter } from './frontmatter.js';

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
  const { dir, entry, name, status = 'approved', overwrite = false } = options;
  const paths = catalogPaths(dir);
  const filePath = path.join(paths.entries, `${name}.md`);

  if (!overwrite && existsSync(filePath)) {
    throw new Error(`Entry ${name}.md already exists. Pass overwrite: true to replace.`);
  }

  // Inject status and acquired if not present
  let content = entry;
  try {
    const parsed = parseFrontmatter(content);
    if (!parsed.frontmatter.status) {
      parsed.frontmatter.status = status;
    }
    if (!parsed.frontmatter.acquired) {
      parsed.frontmatter.acquired = new Date().toISOString().split('T')[0];
    }
    content = serializeFrontmatter(parsed.frontmatter, parsed.body);
  } catch {
    // If we can't parse, validate will catch it below
  }

  const validation = validateEntry(content);
  if (!validation.valid) {
    throw new Error(`Invalid entry:\n${validation.errors.join('\n')}`);
  }

  await writeFile(filePath, content, 'utf-8');
  return { path: filePath, status };
}
