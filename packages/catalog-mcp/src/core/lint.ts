// packages/catalog-mcp/src/core/lint.ts
import { readFile, writeFile, readdir } from 'node:fs/promises';
import path from 'node:path';
import { entrySchema } from './schema.js';
import { parseFrontmatter, serializeFrontmatter } from './frontmatter.js';
import { catalogPaths } from './config.js';
import { loadTaxonomy, buildIndex, canonicalForTag, unclassifiedTags, type TaxonomyIndex } from './taxonomy.js';

interface LintResult {
  errors: string[];
  warnings: string[];
  missingCanonical: string[];
}

interface LintFileResult extends LintResult {
  file: string;
}

const RETIRED_FIELDS: Record<string, string> = {
  verdict: 'decision_status',
  verdict_reason: 'summary',
  status: '(removed)',
};

const EMPTY_TAX_INDEX: TaxonomyIndex = buildIndex({ canonical: {} });

export function lintEntry(
  filename: string,
  frontmatter: Record<string, unknown>,
  body: string,
  taxIndex: TaxonomyIndex = EMPTY_TAX_INDEX,
): LintResult {
  const errors: string[] = [];
  const warnings: string[] = [];
  const missingCanonical: string[] = [];

  // Retired-field detection — a friendly message ahead of the generic strict error.
  for (const [retired, target] of Object.entries(RETIRED_FIELDS)) {
    if (retired in frontmatter) {
      errors.push(`retired field "${retired}" — migrate to ${target}`);
    }
  }

  const result = entrySchema.safeParse(frontmatter);
  if (!result.success) {
    for (const issue of result.error.issues) {
      errors.push(`${issue.path.join('.')}: ${issue.message}`);
    }
  }

  if (frontmatter.name && frontmatter.name !== filename) {
    errors.push(`name "${frontmatter.name}" does not match filename "${filename}"`);
  }

  if (!frontmatter.acquired) {
    warnings.push('missing acquired field (migration: backfill from git log)');
  }

  if (!body.includes('## Security')) {
    warnings.push('missing ## Security section (migration: not required for existing entries)');
  }

  // Taxonomy audit: an alias tag should also carry its canonical umbrella.
  const tags = (frontmatter.tags as string[]) ?? [];
  for (const tag of tags) {
    const c = canonicalForTag(tag, taxIndex);
    if (c && !tags.includes(c) && !missingCanonical.includes(c)) {
      warnings.push(`tag "${tag}" should also carry canonical "${c}"`);
      missingCanonical.push(c);
    }
  }

  return { errors, warnings, missingCanonical };
}

interface LintOptions {
  dir: string;
  files?: string[];
  fix?: boolean;
}

interface TaxonomySummary {
  aliasWithoutCanonical: number;
  unclassified: string[];
}

interface LintRunResult {
  results: LintFileResult[];
  taxonomy: TaxonomySummary;
}

export async function lint(options: LintOptions): Promise<LintRunResult> {
  const paths = catalogPaths(options.dir);
  const taxIndex = buildIndex(await loadTaxonomy(options.dir));
  let files = options.files;
  if (!files) {
    const allFiles = await readdir(paths.entries);
    files = allFiles.filter((f) => f.endsWith('.md'));
  }

  const results: LintFileResult[] = [];
  let aliasWithoutCanonical = 0;
  const unclassifiedSet = new Set<string>();

  for (const file of files) {
    const filePath = path.join(paths.entries, file);
    const content = await readFile(filePath, 'utf-8');
    const name = file.replace('.md', '');

    try {
      const parsed = parseFrontmatter(content);
      const result = lintEntry(name, parsed.frontmatter, parsed.body, taxIndex);

      if (options.fix && (result.errors.length > 0 || result.missingCanonical.length > 0)) {
        const fixed = applyFixes(parsed.frontmatter, result.missingCanonical);
        const newContent = serializeFrontmatter(fixed, parsed.body);
        await writeFile(filePath, newContent, 'utf-8');
      }

      if (result.missingCanonical.length > 0) aliasWithoutCanonical++;
      const tags = (parsed.frontmatter.tags as string[]) ?? [];
      for (const t of unclassifiedTags(tags, taxIndex)) unclassifiedSet.add(t);

      results.push({ file, ...result });
    } catch (err) {
      results.push({ file, errors: [`Parse error: ${err}`], warnings: [], missingCanonical: [] });
    }
  }

  return {
    results,
    taxonomy: { aliasWithoutCanonical, unclassified: [...unclassifiedSet].sort() },
  };
}

function applyFixes(
  fm: Record<string, unknown>,
  missingCanonical: string[] = [],
): Record<string, unknown> {
  const fixed = { ...fm };
  if (fixed.url === '') delete fixed.url;
  if (fixed.tags && !Array.isArray(fixed.tags)) fixed.tags = [];
  if (fixed.supersedes && !Array.isArray(fixed.supersedes)) fixed.supersedes = [];
  if (fixed.overlaps && !Array.isArray(fixed.overlaps)) fixed.overlaps = [];
  if (fixed.security_flags && !Array.isArray(fixed.security_flags)) fixed.security_flags = [];
  // Append missing canonical umbrella tags (dedup, preserve order).
  if (missingCanonical.length > 0) {
    const tags = Array.isArray(fixed.tags) ? [...(fixed.tags as string[])] : [];
    for (const c of missingCanonical) if (!tags.includes(c)) tags.push(c);
    fixed.tags = tags;
  }
  return fixed;
}
