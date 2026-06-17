// packages/catalog-mcp/src/core/search.ts
import { readAllEntries } from './frontmatter.js';
import { catalogPaths } from './config.js';

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
  category: string;
  decision_status: string;
  summary: string;
  tags: string[];
}

export async function searchEntries(options: SearchOptions): Promise<SearchResult[]> {
  const paths = catalogPaths(options.dir);
  const raw = await readAllEntries(paths.entries);
  const results: SearchResult[] = [];

  for (const [name, parsed] of raw) {
    const fm = parsed.frontmatter;

    if (options.decision_status && ((fm.decision_status as string | undefined) ?? 'open') !== options.decision_status) continue;
    if (options.category && fm.category !== options.category) continue;

    if (options.query) {
      const searchFields = options.fields || [
        'title',
        'summary',
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
      decision_status: (fm.decision_status as string) ?? 'open',
      summary: fm.summary as string,
      tags: (fm.tags as string[]) || [],
    });
  }

  results.sort((a, b) => a.title.localeCompare(b.title));
  return results.slice(0, options.limit || 20);
}
