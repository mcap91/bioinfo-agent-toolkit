// packages/catalog-mcp/src/core/review.ts
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { catalogPaths } from './config.js';
import { searchEntries } from './search.js';
import { parseFrontmatter, serializeFrontmatter } from './frontmatter.js';
import { persistEntry } from './entry-io.js';

/** Convenience wrapper over search(status:'draft') — no parallel query path. */
export async function listDrafts(dir: string) {
  const drafts = await searchEntries({ dir, query: '', status: 'draft', limit: 1000 });
  return drafts.map((d) => ({
    name: d.name,
    title: d.title,
    verdict: d.verdict,
    verdict_reason: d.verdict_reason,
    tags: d.tags,
  }));
}

async function mutateEntry(
  dir: string,
  name: string,
  mutate: (fm: Record<string, unknown>) => void,
): Promise<{ path: string }> {
  const file = path.join(catalogPaths(dir).entries, `${name}.md`);
  const parsed = parseFrontmatter(await readFile(file, 'utf-8'));
  mutate(parsed.frontmatter);
  const markdown = serializeFrontmatter(parsed.frontmatter, parsed.body);
  return persistEntry({ dir, name, markdown, overwrite: true });
}

export async function approveEntry(dir: string, name: string): Promise<{ path: string }> {
  return mutateEntry(dir, name, (fm) => { fm.status = 'approved'; });
}

export async function rejectEntry(dir: string, name: string, reason: string): Promise<{ path: string }> {
  return mutateEntry(dir, name, (fm) => {
    fm.verdict = 'skip';
    fm.status = 'approved';
    fm.verdict_reason = `[rejected] ${reason}`;
  });
}
