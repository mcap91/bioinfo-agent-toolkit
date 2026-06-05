// packages/catalog-mcp/src/core/index-gen.ts
import { writeFile } from 'node:fs/promises';
import { readAllEntries } from './frontmatter.js';
import { catalogPaths } from './config.js';
import { VERDICTS } from './schema.js';

interface IndexOptions {
  dir: string;
  format: 'full' | 'verdict' | 'workflow' | 'category';
  includeDrafts: boolean;
}

interface IndexResult {
  content: string;
  path: string;
  entryCount: number;
  verdictCounts: Record<string, number>;
}

interface EntryData {
  name: string;
  title: string;
  category: string;
  verdict: string;
  verdict_reason: string;
  tags: string[];
  workflows: string[];
  status: string;
}

// Ordinal comparator on lowercased strings — matches Python's
// sorted(key=lambda x: x["title"].lower()) that generated catalog/index.md.
// Do NOT use localeCompare here; it diverges from Python's code-point order.
function cmpTitleLower(a: string, b: string): number {
  const al = a.toLowerCase();
  const bl = b.toLowerCase();
  return al < bl ? -1 : al > bl ? 1 : 0;
}

// Ordinal comparator on raw strings (case-sensitive) — matches Python's
// sorted() on workflow/category keys (which are NOT lowercased).
function cmpRaw(a: string, b: string): number {
  return a < b ? -1 : a > b ? 1 : 0;
}

export async function generateIndex(options: IndexOptions): Promise<IndexResult> {
  const paths = catalogPaths(options.dir);
  const raw = await readAllEntries(paths.entries);
  const entries: EntryData[] = [];

  for (const [name, parsed] of raw) {
    const fm = parsed.frontmatter;
    const status = (fm.status as string) || 'approved';
    if (!options.includeDrafts && status === 'draft') continue;

    entries.push({
      name,
      title: fm.title as string,
      category: fm.category as string,
      verdict: fm.verdict as string,
      verdict_reason: fm.verdict_reason as string,
      tags: (fm.tags as string[]) || [],
      workflows: (fm.workflows as string[]) || [],
      status,
    });
  }

  const verdictCounts: Record<string, number> = {};
  for (const e of entries) {
    verdictCounts[e.verdict] = (verdictCounts[e.verdict] || 0) + 1;
  }

  const sections: string[] = [];

  if (options.format === 'full' || options.format === 'verdict') {
    sections.push(renderByVerdict(entries));
  }
  if (options.format === 'full' || options.format === 'workflow') {
    sections.push(renderByWorkflow(entries));
  }
  if (options.format === 'full' || options.format === 'category') {
    sections.push(renderByCategory(entries));
  }

  const header = `# Catalog Index\n\nGenerated from ${entries.length} entries in \`catalog/entries/\`. Regenerate with the catalog \`index\` tool.\n`;
  const content = header + '\n' + sections.join('\n\n') + '\n';

  return { content, path: paths.index, entryCount: entries.length, verdictCounts };
}

export async function generateAndWriteIndex(options: IndexOptions): Promise<IndexResult> {
  const result = await generateIndex(options);
  await writeFile(result.path, result.content, 'utf-8');
  return result;
}

function sortByTitle(entries: EntryData[]): EntryData[] {
  return [...entries].sort((a, b) => cmpTitleLower(a.title, b.title));
}

function renderByVerdict(entries: EntryData[]): string {
  const sorted = VERDICTS.flatMap((v) =>
    sortByTitle(entries.filter((e) => e.verdict === v)),
  );
  const rows = sorted.map(
    (e) =>
      `| [${e.title}](entries/${e.name}.md) | ${e.category} | ${e.verdict} | ${e.verdict_reason} | ${e.tags.join(', ')} |`,
  );
  return [
    '## By Verdict',
    '',
    '| Item | Category | Verdict | Reason | Tags |',
    '|---|---|---|---|---|',
    ...rows,
  ].join('\n');
}

function renderByWorkflow(entries: EntryData[]): string {
  const groups = new Map<string, EntryData[]>();
  for (const e of entries) {
    const workflows = e.workflows.length > 0 ? e.workflows : ['General'];
    for (const w of workflows) {
      if (!groups.has(w)) groups.set(w, []);
      groups.get(w)!.push(e);
    }
  }

  const sortedKeys = [...groups.keys()].sort((a, b) => {
    if (a === 'General') return 1;
    if (b === 'General') return -1;
    return cmpRaw(a, b);
  });

  const sections: string[] = ['## By Workflow'];
  for (const key of sortedKeys) {
    sections.push('');
    sections.push(`### ${key}`);
    sections.push('');
    for (const e of sortByTitle(groups.get(key)!)) {
      sections.push(
        `- [${e.title}](entries/${e.name}.md) — ${e.verdict} — ${e.verdict_reason}`,
      );
    }
  }
  return sections.join('\n');
}

function renderByCategory(entries: EntryData[]): string {
  const groups = new Map<string, EntryData[]>();
  for (const e of entries) {
    if (!groups.has(e.category)) groups.set(e.category, []);
    groups.get(e.category)!.push(e);
  }

  const sortedKeys = [...groups.keys()].sort(cmpRaw);

  const sections: string[] = ['## By Category'];
  for (const key of sortedKeys) {
    sections.push('');
    sections.push(`### ${key}`);
    sections.push('');
    for (const e of sortByTitle(groups.get(key)!)) {
      sections.push(
        `- [${e.title}](entries/${e.name}.md) — ${e.verdict} — ${e.verdict_reason}`,
      );
    }
  }
  return sections.join('\n');
}
