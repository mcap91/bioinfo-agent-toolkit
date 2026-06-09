// packages/catalog-mcp/src/core/search.ts
import { readAllEntries } from './frontmatter.js';
import { catalogPaths } from './config.js';

interface SearchOptions {
  dir: string;
  query: string;
  fields?: string[];
  verdict?: string;
  category?: string;
  status?: string;
  limit?: number;
}

interface SearchResult {
  name: string;
  title: string;
  category: string;
  verdict: string;
  verdict_reason: string;
  tags: string[];
}

export async function searchEntries(options: SearchOptions): Promise<SearchResult[]> {
  const paths = catalogPaths(options.dir);
  const raw = await readAllEntries(paths.entries);
  const results: SearchResult[] = [];

  for (const [name, parsed] of raw) {
    const fm = parsed.frontmatter;

    if (options.verdict && fm.verdict !== options.verdict) continue;
    if (options.category && fm.category !== options.category) continue;
    if (options.status !== 'any') {
      const wanted = options.status ?? 'approved';
      if ((fm.status || 'approved') !== wanted) continue;
    }

    if (options.query) {
      const searchFields = options.fields || [
        'title',
        'verdict_reason',
        'tags',
        'name',
      ];
      const haystack = searchFields
        .map((f) => {
          const val = fm[f];
          if (Array.isArray(val)) return val.join(' ');
          return String(val || '');
        })
        .join(' ')
        .toLowerCase();

      if (!haystack.includes(options.query.toLowerCase())) {
        // Also check body text
        if (!parsed.body.toLowerCase().includes(options.query.toLowerCase())) {
          continue;
        }
      }
    }

    results.push({
      name,
      title: fm.title as string,
      category: fm.category as string,
      verdict: fm.verdict as string,
      verdict_reason: fm.verdict_reason as string,
      tags: (fm.tags as string[]) || [],
    });
  }

  results.sort((a, b) => a.title.localeCompare(b.title));
  return results.slice(0, options.limit || 20);
}
