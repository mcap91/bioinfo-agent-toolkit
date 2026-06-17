// packages/catalog-mcp/src/core/taxonomy.ts
import { readFile } from 'node:fs/promises';
import { z } from 'zod';
import { catalogPaths } from './config.js';

export const taxonomySchema = z.object({
  canonical: z.record(z.string(), z.array(z.string())),
});
export type Taxonomy = z.infer<typeof taxonomySchema>;

export interface TaxonomyIndex {
  groups: Map<string, Set<string>>;   // term -> {canonical, ...aliases}
  canonicalOf: Map<string, string>;   // alias|canonical -> canonical
  knownTerms: Set<string>;            // every key + alias
}

export function tokenize(s: string): string[] {
  return s.toLowerCase().split(/[^a-z0-9]+/).filter(Boolean);
}

export async function loadTaxonomy(dir: string): Promise<Taxonomy> {
  try {
    const raw = await readFile(catalogPaths(dir).taxonomy, 'utf-8');
    return taxonomySchema.parse(JSON.parse(raw));
  } catch {
    return { canonical: {} };
  }
}

export function buildIndex(tax: Taxonomy): TaxonomyIndex {
  const groups = new Map<string, Set<string>>();
  const canonicalOf = new Map<string, string>();
  const knownTerms = new Set<string>();
  for (const [canonicalRaw, aliasesRaw] of Object.entries(tax.canonical)) {
    const canonical = canonicalRaw.toLowerCase();
    const members = new Set<string>([canonical, ...aliasesRaw.map((a) => a.toLowerCase())]);
    for (const m of members) {
      groups.set(m, members);
      canonicalOf.set(m, canonical);
      knownTerms.add(m);
    }
  }
  return { groups, canonicalOf, knownTerms };
}

export function expandTerm(term: string, index: TaxonomyIndex): string[] {
  const t = term.toLowerCase();
  const group = index.groups.get(t);
  return group ? [...group] : [t];
}

export function canonicalForTag(tag: string, index: TaxonomyIndex): string | null {
  return index.canonicalOf.get(tag.toLowerCase()) ?? null;
}

export function unclassifiedTags(tags: string[], index: TaxonomyIndex): string[] {
  return tags.filter((t) => !index.knownTerms.has(t.toLowerCase()));
}
