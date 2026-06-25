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
  score: number;
}

interface SearchResponse {
  results: SearchResult[];
  total: number;
  truncated: boolean;
}

const DEFAULT_TEXT_FIELDS = ['title', 'summary', 'name', 'body'];

const FIELD_WEIGHT: Record<string, number> = {
  title: 10,
  name: 5,
  summary: 3,
  body: 1,
};
const TAG_WEIGHT = 5;

export async function searchEntries(options: SearchOptions): Promise<SearchResponse> {
  const paths = catalogPaths(options.dir);
  const raw = await readAllEntries(paths.entries);
  const taxIndex = buildIndex(await loadTaxonomy(options.dir));

  const textFields = options.fields ?? DEFAULT_TEXT_FIELDS;
  const queryTerms = options.query.toLowerCase().split(/\s+/).filter(Boolean);

  const scored: { entry: SearchResult; score: number }[] = [];

  for (const [name, parsed] of raw) {
    const fm = parsed.frontmatter;
    const status = (fm.decision_status as string | undefined) ?? 'open';
    if (options.decision_status && status !== options.decision_status) continue;
    if (options.category && fm.category !== options.category) continue;

    // Build per-field token sets for weighted scoring.
    const fieldTokens = new Map<string, Set<string>>();
    for (const f of textFields) {
      const val = f === 'body' ? parsed.body : fm[f];
      const text = Array.isArray(val) ? val.join(' ') : String(val ?? '');
      fieldTokens.set(f, new Set(tokenize(text)));
    }

    // Tags are always searched regardless of the fields option.
    const tags = (fm.tags as string[]) ?? [];
    const tagTokens = new Set<string>();
    for (const tag of tags) {
      tagTokens.add(tag.toLowerCase());
      for (const t of tokenize(tag)) tagTokens.add(t);
    }

    let score = 0;
    if (queryTerms.length > 0) {
      for (const term of queryTerms) {
        const candidates = new Set<string>([...expandTerm(term, taxIndex), ...tokenize(term)]);

        for (const [field, tokens] of fieldTokens) {
          for (const c of candidates) {
            if (tokens.has(c)) {
              score += FIELD_WEIGHT[field] ?? 1;
              break; // one match per field per term
            }
          }
        }

        for (const c of candidates) {
          if (tagTokens.has(c)) {
            score += TAG_WEIGHT;
            break;
          }
        }
      }
      if (score === 0) continue;
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
        score,
      },
      score,
    });
  }

  scored.sort(
    (a, b) =>
      b.score - a.score ||
      cmpTitleLower(a.entry.title, b.entry.title) ||
      cmpTitleLower(a.entry.name, b.entry.name),
  );

  const limit = options.limit ?? 200;
  const total = scored.length;

  return {
    results: scored.slice(0, limit).map((s) => s.entry),
    total,
    truncated: total > limit,
  };
}
