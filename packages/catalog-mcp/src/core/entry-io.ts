// packages/catalog-mcp/src/core/entry-io.ts
import { writeFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { catalogPaths } from './config.js';
import { validateEntry } from './validate-entry.js';

interface PersistOptions {
  dir: string;
  name: string;
  markdown: string;
  overwrite?: boolean;
}

/** Validate `markdown` and write it to entries/<name>.md with LF endings. */
export async function persistEntry(options: PersistOptions): Promise<{ path: string }> {
  const { dir, name, markdown, overwrite = false } = options;
  const filePath = path.join(catalogPaths(dir).entries, `${name}.md`);

  if (!overwrite && existsSync(filePath)) {
    throw new Error(`Entry ${name}.md already exists. Pass overwrite: true to replace.`);
  }
  const validation = validateEntry(markdown);
  if (!validation.valid) {
    throw new Error(`Invalid entry:\n${validation.errors.join('\n')}`);
  }
  // Server always writes LF; autocrlf reconciles the working tree for git.
  await writeFile(filePath, markdown.replace(/\r\n/g, '\n'), 'utf-8');
  return { path: filePath };
}
