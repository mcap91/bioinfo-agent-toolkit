// packages/catalog-mcp/src/tools.ts
import { z } from 'zod';
import { dirSchema, CATEGORIES } from './core/schema.js';
import { resolveDir, loadConfig, loadState, saveState } from './core/config.js';
import { generateAndWriteIndex, buildSearchIndex } from './core/index-gen.js';
import { lint } from './core/lint.js';
import { searchEntries } from './core/search.js';
import { scaffoldEntry } from './core/scaffold.js';
import { readQueue, removeFromQueue, returnToInbox, clearQueue } from './core/queue.js';
import { ingest } from './core/ingest.js';
import { fetchUrl } from './core/fetch-url.js';
import { redditExtract } from './core/reddit.js';
import { buildPrompt } from './core/prompt-builder.js';
import { validateEntry } from './core/validate-entry.js';
import { writeEntry } from './core/write-entry.js';
import { annotateEntry } from './core/annotate-entry.js';
import { listGoals, getGoal, addGoal, updateGoal, removeGoal } from './core/goals.js';
import { PROJECT_STATUSES, PRIORITIES } from './core/schema.js';
import { drainInbox } from './core/drain.js';

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
      format: z.enum(['full', 'decision_status', 'workflow', 'category']).default('full'),
    }),
    handler: async (input) => {
      const dir = resolveDir(input.dir as string | undefined);
      const result = await generateAndWriteIndex({
        dir,
        format: input.format as 'full' | 'decision_status' | 'workflow' | 'category',
      });
      const searchResult = await buildSearchIndex(dir);
      return {
        path: result.path,
        searchIndexPath: searchResult.path,
        entryCount: result.entryCount,
        decisionStatusCounts: result.decisionStatusCounts,
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
      const { results, taxonomy } = await lint({
        dir,
        files: input.files as string[] | undefined,
        fix: input.fix as boolean,
      });
      const hasErrors = results.some((r) => r.errors.length > 0);
      return { results, taxonomy, clean: !hasErrors };
    },
  },
  {
    name: 'search',
    description: 'Query catalog entries by field values or freeform text',
    inputSchema: dirSchema.extend({
      query: z.string(),
      fields: z.array(z.string()).optional(),
      decision_status: z.enum(['adopted', 'rejected', 'open']).optional(),
      category: z.string().optional(),
      limit: z.number().int().positive().default(200),
    }),
    handler: async (input) => {
      const dir = resolveDir(input.dir as string | undefined);
      return searchEntries({
        dir,
        query: input.query as string,
        fields: input.fields as string[] | undefined,
        decision_status: input.decision_status as string | undefined,
        category: input.category as string | undefined,
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
    description: 'View and update catalog configuration and persistent state (e.g. Gmail pull cursor)',
    inputSchema: dirSchema.extend({
      action: z.enum(['get', 'set', 'check', 'get-state', 'set-state']),
      key: z.string().optional(),
      value: z.union([z.string(), z.array(z.string()), z.null()]).optional(),
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
      if (action === 'get-state') {
        return { state: await loadState(dir) };
      }
      if (action === 'set-state') {
        if (!input.key) throw new Error('key is required for set-state action');
        const VALID_STATE_KEYS = new Set(['gmail_last_pull_iso']);
        if (!VALID_STATE_KEYS.has(input.key as string)) {
          throw new Error(
            `Unknown state key "${input.key}". Valid keys: ${[...VALID_STATE_KEYS].join(', ')}`,
          );
        }
        const state = await saveState(dir, { [input.key as string]: input.value ?? null });
        return { updated: input.key, state };
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
  {
    name: 'queue',
    description: 'Manage the catalog intake queue (list/remove/return/clear). Holds only pending work; return sends an item back to inbox.md marked ⚠ <reason>.',
    inputSchema: dirSchema.extend({
      action: z.enum(['list', 'remove', 'return', 'clear']),
      keys: z.array(z.string()).optional(),
      key: z.string().optional(),
      reason: z.string().optional(),
    }),
    handler: async (input) => {
      const dir = resolveDir(input.dir as string | undefined);
      const action = input.action as string;
      if (action === 'list') {
        const queue = await readQueue(dir);
        return { items: queue.items, count: queue.items.length };
      }
      if (action === 'remove') {
        const keys = input.keys as string[];
        if (!keys?.length) throw new Error('keys required for remove action');
        return { removed: await removeFromQueue(dir, keys) };
      }
      if (action === 'return') {
        const key = input.key as string;
        if (!key) throw new Error('key required for return action');
        if (!input.reason) throw new Error('reason required for return action');
        return { returned: await returnToInbox(dir, key, input.reason as string) };
      }
      await clearQueue(dir);
      return { cleared: true };
    },
  },
  {
    name: 'drain',
    description: 'Drain catalog/inbox.md into the queue: ingest ready items, keep+mark blocked items (⚠ needs-link)',
    inputSchema: dirSchema,
    handler: async (input) => {
      const dir = resolveDir(input.dir as string | undefined);
      return drainInbox(dir);
    },
  },
  {
    name: 'ingest',
    description: 'Add URLs or free-form text items to the intake queue, with dedup',
    inputSchema: dirSchema.extend({
      items: z.array(z.object({
        url: z.string().url().optional(),
        content: z.string().optional(),
        source: z.enum(['manual', 'reddit', 'slack', 'email', 'other']).default('manual'),
        notes: z.string().optional(),
        context: z.record(z.string(), z.unknown()).optional(),
      })),
      deduplicate: z.boolean().default(true),
    }),
    handler: async (input) => {
      const dir = resolveDir(input.dir as string | undefined);
      return ingest({
        dir,
        items: input.items as Array<{ url?: string; content?: string; source?: 'manual' | 'reddit' | 'slack' | 'email' | 'other'; notes?: string; context?: Record<string, unknown> }>,
        deduplicate: input.deduplicate as boolean,
      });
    },
  },
  {
    name: 'fetch-url',
    description: 'Fetch a URL and extract readable content (SSRF-guarded). clean=false returns raw HTML.',
    inputSchema: dirSchema.extend({
      url: z.string().url(),
      clean: z.boolean().default(true),
    }),
    handler: async (input) => {
      const dir = resolveDir(input.dir as string | undefined);
      const config = await loadConfig(dir).catch(() => ({ min_clean_chars: 200 } as { min_clean_chars: number }));
      return fetchUrl(input.url as string, {
        clean: input.clean as boolean,
        minChars: config.min_clean_chars,
      });
    },
  },
  {
    name: 'reddit-extract',
    description: 'Extract tool URLs from Reddit posts or subreddits',
    inputSchema: dirSchema.extend({
      url: z.string().url().optional(),
      subreddit: z.string().optional(),
      sort: z.enum(['hot', 'new', 'top']).default('hot'),
      time: z.enum(['hour', 'day', 'week', 'month', 'year', 'all']).default('week'),
      limit: z.number().default(25),
      extra_patterns: z.array(z.string()).optional(),
      auto_ingest: z.boolean().default(false),
    }),
    handler: async (input) => {
      const dir = resolveDir(input.dir as string | undefined);
      const urls = await redditExtract({
        dir,
        url: input.url as string | undefined,
        subreddit: input.subreddit as string | undefined,
        sort: input.sort as 'hot' | 'new' | 'top',
        time: input.time as 'hour' | 'day' | 'week' | 'month' | 'year' | 'all',
        limit: input.limit as number,
        extraPatterns: input.extra_patterns as string[] | undefined,
      });
      if (input.auto_ingest) {
        const ingestResult = await ingest({
          dir,
          items: urls.map((u) => ({
            url: u.url,
            source: 'reddit' as const,
            notes: `r/${u.subreddit}: "${u.post_title}" (${u.author}, ${u.score} upvotes)`,
            context: u as unknown as Record<string, unknown>,
          })),
        });
        return { extracted: urls, ingest: ingestResult };
      }
      return { extracted: urls };
    },
  },
  {
    name: 'build-prompt',
    description: 'Build a structured research prompt for the calling agent',
    inputSchema: dirSchema.extend({
      url: z.string().url(),
      content: z.string(),
      source_metadata: z.record(z.string(), z.unknown()).optional(),
    }),
    handler: async (input) => {
      const dir = resolveDir(input.dir as string | undefined);
      return buildPrompt({
        dir,
        url: input.url as string,
        content: input.content as string,
        sourceMetadata: input.source_metadata as Record<string, unknown> | undefined,
      });
    },
  },
  {
    name: 'validate-entry',
    description: 'Validate a catalog entry against the schema',
    inputSchema: dirSchema.extend({
      entry: z.string(),
    }),
    handler: async (input) => {
      return validateEntry(input.entry as string);
    },
  },
  {
    name: 'write-entry',
    description: 'Write a validated catalog entry to disk',
    inputSchema: dirSchema.extend({
      entry: z.string(),
      name: z.string(),
    }),
    handler: async (input) => {
      const dir = resolveDir(input.dir as string | undefined);
      return writeEntry({
        dir,
        entry: input.entry as string,
        name: input.name as string,
      });
    },
  },
  {
    name: 'annotate-entry',
    description: 'Append a note under a ## section of an existing entry (deterministic; frontmatter + other sections byte-preserved). Use to add usage tips to a tool without rewriting it.',
    inputSchema: dirSchema.extend({
      name: z.string(),
      section: z.string(),
      body: z.string(),
    }),
    handler: async (input) => {
      const dir = resolveDir(input.dir as string | undefined);
      return annotateEntry({
        dir,
        name: input.name as string,
        section: input.section as string,
        body: input.body as string,
      });
    },
  },
  {
    name: 'goals',
    description: 'Read and update active projects and priorities',
    inputSchema: dirSchema.extend({
      action: z.enum(['list', 'get', 'add', 'update', 'remove']),
      name: z.string().optional(),
      status: z.enum(PROJECT_STATUSES).optional(),
      project: z.object({
        name: z.string().min(1),
        status: z.enum(PROJECT_STATUSES).default('active'),
        workflows: z.array(z.string()).optional(),
        priority: z.enum(PRIORITIES).default('medium'),
        notes: z.string().optional(),
      }).optional(),
      updates: z.record(z.string(), z.unknown()).optional(),
    }),
    handler: async (input) => {
      const dir = resolveDir(input.dir as string | undefined);
      const action = input.action as string;
      if (action === 'list') return listGoals(dir, input.status as string | undefined);
      if (action === 'get') {
        if (!input.name) throw new Error('name required for get');
        return getGoal(dir, input.name as string);
      }
      if (action === 'add') {
        if (!input.project) throw new Error('project required for add');
        return addGoal(dir, input.project as any);
      }
      if (action === 'update') {
        if (!input.name) throw new Error('name required for update');
        if (!input.updates) throw new Error('updates required for update');
        return updateGoal(dir, input.name as string, input.updates as any);
      }
      if (action === 'remove') {
        if (!input.name) throw new Error('name required for remove');
        await removeGoal(dir, input.name as string);
        return { removed: input.name };
      }
    },
  },
];
