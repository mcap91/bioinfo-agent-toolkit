// packages/catalog-mcp/src/core/lint.ts
import { readFile, writeFile, readdir } from 'node:fs/promises';
import path from 'node:path';
import { entrySchema } from './schema.js';
import { parseFrontmatter, serializeFrontmatter } from './frontmatter.js';
import { catalogPaths } from './config.js';

interface LintResult {
  errors: string[];
  warnings: string[];
}

interface LintFileResult extends LintResult {
  file: string;
}

export function lintEntry(
  filename: string,
  frontmatter: Record<string, unknown>,
  body: string,
): LintResult {
  const errors: string[] = [];
  const warnings: string[] = [];

  const result = entrySchema.safeParse(frontmatter);
  if (!result.success) {
    for (const issue of result.error.issues) {
      errors.push(`${issue.path.join('.')}: ${issue.message}`);
    }
  }

  if (frontmatter.name && frontmatter.name !== filename) {
    errors.push(
      `name "${frontmatter.name}" does not match filename "${filename}"`,
    );
  }

  if (!frontmatter.acquired) {
    warnings.push('missing acquired field (migration: backfill from git log)');
  }

  if (!body.includes('## Security')) {
    warnings.push('missing ## Security section (migration: not required for existing entries)');
  }

  return { errors, warnings };
}

interface LintOptions {
  dir: string;
  files?: string[];
  fix?: boolean;
}

export async function lint(options: LintOptions): Promise<LintFileResult[]> {
  const paths = catalogPaths(options.dir);
  let files = options.files;
  if (!files) {
    const allFiles = await readdir(paths.entries);
    files = allFiles.filter((f) => f.endsWith('.md'));
  }

  const results: LintFileResult[] = [];

  for (const file of files) {
    const filePath = path.join(paths.entries, file);
    const content = await readFile(filePath, 'utf-8');
    const name = file.replace('.md', '');

    try {
      const parsed = parseFrontmatter(content);
      const result = lintEntry(name, parsed.frontmatter, parsed.body);

      if (options.fix && result.errors.length > 0) {
        const fixed = applyFixes(parsed.frontmatter);
        const newContent = serializeFrontmatter(fixed, parsed.body);
        await writeFile(filePath, newContent, 'utf-8');
      }

      results.push({ file, ...result });
    } catch (err) {
      results.push({
        file,
        errors: [`Parse error: ${err}`],
        warnings: [],
      });
    }
  }

  return results;
}

function applyFixes(fm: Record<string, unknown>): Record<string, unknown> {
  const fixed = { ...fm };
  if (!fixed.status) fixed.status = 'approved';
  if (fixed.url === '') delete fixed.url;
  if (fixed.tags && !Array.isArray(fixed.tags)) fixed.tags = [];
  if (fixed.supersedes && !Array.isArray(fixed.supersedes)) fixed.supersedes = [];
  if (fixed.overlaps && !Array.isArray(fixed.overlaps)) fixed.overlaps = [];
  if (fixed.security_flags && !Array.isArray(fixed.security_flags))
    fixed.security_flags = [];
  return fixed;
}
