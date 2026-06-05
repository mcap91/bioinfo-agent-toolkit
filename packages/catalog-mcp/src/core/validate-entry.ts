// packages/catalog-mcp/src/core/validate-entry.ts
import { parseFrontmatter } from './frontmatter.js';
import { lintEntry } from './lint.js';

interface ValidationResult {
  valid: boolean;
  errors: string[];
  warnings: string[];
}

export function validateEntry(markdown: string): ValidationResult {
  try {
    const parsed = parseFrontmatter(markdown);
    const name = (parsed.frontmatter.name as string) || '';
    const result = lintEntry(name, parsed.frontmatter, parsed.body);
    return {
      valid: result.errors.length === 0,
      errors: result.errors,
      warnings: result.warnings,
    };
  } catch (err) {
    return {
      valid: false,
      errors: [`Parse error: ${err}`],
      warnings: [],
    };
  }
}
