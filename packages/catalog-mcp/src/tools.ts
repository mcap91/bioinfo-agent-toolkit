// packages/catalog-mcp/src/tools.ts
import { z } from 'zod';
import { dirSchema, CATEGORIES, VERDICTS, STATUSES } from './core/schema.js';
import { resolveDir, loadConfig } from './core/config.js';
import { generateAndWriteIndex } from './core/index-gen.js';
import { lint } from './core/lint.js';
import { searchEntries } from './core/search.js';
import { scaffoldEntry } from './core/scaffold.js';

export interface ToolDef {
  name: string;
  description: string;
  inputSchema: z.ZodType;
  handler: (input: Record<string, unknown>) => Promise<unknown>;
}

export const tools: ToolDef[] = [
  {
    name: 'index',
    description: 'Regenerate catalog/index.md from all entry files',
    inputSchema: dirSchema.extend({
      format: z.enum(['full', 'verdict', 'workflow', 'category']).default('full'),
      include_drafts: z.boolean().default(false),
    }),
    handler: async (input) => {
      const dir = resolveDir(input.dir as string | undefined);
      const result = await generateAndWriteIndex({
        dir,
        format: input.format as 'full' | 'verdict' | 'workflow' | 'category',
        includeDrafts: input.include_drafts as boolean,
      });
      return {
        path: result.path,
        entryCount: result.entryCount,
        verdictCounts: result.verdictCounts,
      };
    },
  },
  {
    name: 'lint',
    description: 'Validate entry frontmatter against the catalog schema',
    inputSchema: dirSchema.extend({
      files: z.array(z.string()).optional(),
      fix: z.boolean().default(false),
    }),
    handler: async (input) => {
      const dir = resolveDir(input.dir as string | undefined);
      const results = await lint({
        dir,
        files: input.files as string[] | undefined,
        fix: input.fix as boolean,
      });
      const hasErrors = results.some((r) => r.errors.length > 0);
      return { results, clean: !hasErrors };
    },
  },
  {
    name: 'search',
    description: 'Query catalog entries by field values or freeform text',
    inputSchema: dirSchema.extend({
      query: z.string(),
      fields: z.array(z.string()).optional(),
      verdict: z.enum(VERDICTS).optional(),
      category: z.string().optional(),
      status: z.enum(STATUSES).optional(),
      limit: z.number().default(20),
    }),
    handler: async (input) => {
      const dir = resolveDir(input.dir as string | undefined);
      return searchEntries({
        dir,
        query: input.query as string,
        fields: input.fields as string[] | undefined,
        verdict: input.verdict as string | undefined,
        category: input.category as string | undefined,
        status: input.status as string | undefined,
        limit: input.limit as number,
      });
    },
  },
  {
    name: 'scaffold',
    description: 'Create a blank catalog entry from the template',
    inputSchema: dirSchema.extend({
      name: z.string(),
      category: z.enum(CATEGORIES),
      url: z.string().url().optional(),
    }),
    handler: async (input) => {
      const dir = resolveDir(input.dir as string | undefined);
      return scaffoldEntry({
        dir,
        name: input.name as string,
        category: input.category as string as import('./core/schema.js').Category,
        url: input.url as string | undefined,
      });
    },
  },
  {
    name: 'config',
    description: 'View and update catalog configuration',
    inputSchema: dirSchema.extend({
      action: z.enum(['get', 'set', 'check']),
      key: z.string().optional(),
      value: z.union([z.string(), z.array(z.string())]).optional(),
    }),
    handler: async (input) => {
      const dir = resolveDir(input.dir as string | undefined);
      const action = input.action as string;
      if (action === 'get') {
        const config = await loadConfig(dir);
        const redditId = process.env['REDDIT_CLIENT_ID'] ? 'set' : 'not set';
        const redditSecret = process.env['REDDIT_CLIENT_SECRET'] ? 'set' : 'not set';
        const redditUser = process.env['REDDIT_USERNAME'] ? 'set' : 'not set';
        return {
          config,
          credentials: {
            REDDIT_CLIENT_ID: redditId,
            REDDIT_CLIENT_SECRET: redditSecret,
            REDDIT_USERNAME: redditUser,
          },
        };
      }
      if (action === 'check') {
        const config = await loadConfig(dir);
        const missing: string[] = [];
        if (!process.env['REDDIT_CLIENT_ID']) missing.push('REDDIT_CLIENT_ID');
        if (!process.env['REDDIT_CLIENT_SECRET']) missing.push('REDDIT_CLIENT_SECRET');
        if (!process.env['REDDIT_USERNAME']) missing.push('REDDIT_USERNAME');
        return {
          configValid: true,
          config,
          missingCredentials: missing,
        };
      }
      // action === 'set'
      if (!input.key) throw new Error('key is required for set action');
      const VALID_KEYS = new Set(['url_patterns']);
      if (!VALID_KEYS.has(input.key as string)) {
        throw new Error(`Unknown config key "${input.key}". Valid keys: ${[...VALID_KEYS].join(', ')}`);
      }
      const { readFile, writeFile } = await import('node:fs/promises');
      const { catalogPaths } = await import('./core/config.js');
      const paths = catalogPaths(dir);
      const raw = JSON.parse(await readFile(paths.config, 'utf-8'));
      raw[input.key as string] = input.value;
      await writeFile(paths.config, JSON.stringify(raw, null, 2) + '\n', 'utf-8');
      return { updated: input.key, value: input.value };
    },
  },
];
