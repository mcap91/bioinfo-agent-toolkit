// packages/catalog-mcp/src/core/config.ts
import { readFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { configSchema, type CatalogConfig } from './schema.js';

export function resolveDir(inputDir?: string): string {
  if (inputDir) return path.resolve(inputDir);

  const envDir = process.env['CATALOG_ROOT'];
  if (envDir) return path.resolve(envDir);

  // Self-resolve: walk up from this file to find catalog/ directory
  let current = path.dirname(fileURLToPath(import.meta.url));
  for (let i = 0; i < 10; i++) {
    if (existsSync(path.join(current, 'catalog'))) return current;
    const parent = path.dirname(current);
    if (parent === current) break;
    current = parent;
  }

  throw new Error(
    'Cannot resolve repo root. Pass dir explicitly or set CATALOG_ROOT env var.',
  );
}

export async function loadConfig(dir: string): Promise<CatalogConfig> {
  const configPath = path.join(dir, 'catalog', 'config.json');
  const raw = await readFile(configPath, 'utf-8');
  const parsed = JSON.parse(raw);
  return configSchema.parse(parsed);
}

export function catalogPaths(dir: string) {
  return {
    entries: path.join(dir, 'catalog', 'entries'),
    index: path.join(dir, 'catalog', 'index.md'),
    searchIndex: path.join(dir, 'catalog', '.search-index.json'),
    queue: path.join(dir, 'catalog', 'queue.json'),
    config: path.join(dir, 'catalog', 'config.json'),
    queueLock: path.join(dir, 'catalog', '.queue.lock'),
  };
}
