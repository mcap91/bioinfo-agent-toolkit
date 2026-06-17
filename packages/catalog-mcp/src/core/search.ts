// packages/catalog-mcp/src/core/search.ts
import { readAllEntries } from './frontmatter.js';
import { catalogPaths } from './config.js';
import { loadTaxonomy, buildIndex, expandTerm, tokenize } from './taxonomy.js';
import { cmpTitleLower } from './sort.js';

interface SearchOptions {
  dir: string;
  query: string;
  fields?: string[];
  decision_status?: string;
  category?: string;
  limit?: number;
}

interface SearchResult {
  name: string;
  title: string;
  url?: string;
  category: string;
  decision_status: string; // normalized: 'open' when unset
  summary: string;
  tags: string[];
}

const DEFAULT_TEXT_FIELDS = ['title', 'summary', 'name', 'body'];

export async function searchEntries(options: SearchOptions): Promise<SearchResult[]> {
  const paths = catalogPaths(options.dir);
  const raw = await readAllEntries(paths.entries);
  const taxIndex = buildIndex(await loadTaxonomy(options.dir));

  const textFields = options.fields ?? DEFAULT_TEXT_FIELDS;
  const queryTerms = options.query.toLowerCase().split(/\s+/).filter(Boolean);

  const scored: { entry: SearchResult; coverage: number }[] = [];

  for (const [name, parsed] of raw) {
    const fm = parsed.frontmatter;
    const status = (fm.decision_status as string | undefined) ?? 'open';
    if (options.decision_status && status !== options.decision_status) continue;
    if (options.category && fm.category !== options.category) continue;

    // entryTokens: tokenized text fields + whole tags + tokenized tags.
    const tokens = new Set<string>();
    for (const f of textFields) {
      const val = f === 'body' ? parsed.body : fm[f];
      const text = Array.isArray(val) ? val.join(' ') : String(val ?? '');
      for (const t of tokenize(text)) tokens.add(t);
    }
    const tags = (fm.tags as string[]) ?? [];
    for (const tag of tags) {
      tokens.add(tag.toLowerCase());            // whole tag (always — clustering)
      for (const t of tokenize(tag)) tokens.add(t);
    }

    let coverage = 0;
    if (queryTerms.length > 0) {
      for (const term of queryTerms) {
        const candidates = new Set<string>([...expandTerm(term, taxIndex), ...tokenize(term)]);
        for (const c of candidates) { if (tokens.has(c)) { coverage++; break; } }
      }
      if (coverage === 0) continue; // not a hit
    }

    scored.push({
      entry: {
        name,
        title: fm.title as string,
        ...(fm.url ? { url: fm.url as string } : {}),
        category: fm.category as string,
        decision_status: status,
        summary: fm.summary as string,
        tags,
      },
      coverage,
    });
  }

  scored.sort(
    (a, b) =>
      b.coverage - a.coverage ||
      cmpTitleLower(a.entry.title, b.entry.title) ||
      cmpTitleLower(a.entry.name, b.entry.name),
  );

  return scored.slice(0, options.limit ?? 200).map((s) => s.entry);
}
