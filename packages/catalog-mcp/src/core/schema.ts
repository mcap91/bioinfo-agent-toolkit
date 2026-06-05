// packages/catalog-mcp/src/core/schema.ts
import { z } from 'zod';

export const CATEGORIES = [
  'skill',
  'hook',
  'plugin',
  'mcp-server',
  'agent-pattern',
  'cli-tool',
  'framework',
  'skill-generator',
  'meta-skill',
  'reference',
] as const;

export const VERDICTS = ['adopt', 'pilot', 'watch', 'note', 'skip'] as const;

export const STATUSES = ['approved', 'draft'] as const;

export const SOURCES = ['manual', 'reddit', 'slack', 'email', 'other'] as const;

export type Category = (typeof CATEGORIES)[number];
export type Verdict = (typeof VERDICTS)[number];
export type Status = (typeof STATUSES)[number];

export const entrySchema = z.object({
  name: z.string().regex(/^[a-z0-9]+(-[a-z0-9]+)*$/, 'Must be kebab-case'),
  title: z.string().min(1),
  url: z.string().url().optional(),
  category: z.enum(CATEGORIES),
  verdict: z.enum(VERDICTS),
  verdict_reason: z.string().min(1),
  status: z.enum(STATUSES).default('approved'),
  install: z.string().optional(),
  tags: z.array(z.string()).min(1),
  workflows: z.array(z.string()).optional(),
  reviewed: z.string().regex(/^\d{4}-\d{2}-\d{2}$/),
  acquired: z.string().regex(/^\d{4}-\d{2}-\d{2}$/).optional(),
  license: z.string().optional(),
  security_flags: z.array(z.string()).optional(),
  supersedes: z.array(z.string()).optional(),
  overlaps: z.array(z.string()).optional(),
});

export type CatalogEntry = z.infer<typeof entrySchema>;

export const queueItemSchema = z.object({
  url: z.string().url(),
  source: z.enum(SOURCES).default('manual'),
  notes: z.string().optional(),
  context: z.record(z.string(), z.unknown()).optional(),
  added: z.string(),
  status: z.enum(['pending', 'error']).default('pending'),
  error_message: z.string().optional(),
});

export type QueueItem = z.infer<typeof queueItemSchema>;

export const queueSchema = z.object({
  items: z.array(queueItemSchema),
});

export const configSchema = z.object({
  url_patterns: z.array(z.string()),
});

export type CatalogConfig = z.infer<typeof configSchema>;

export const dirSchema = z.object({
  dir: z.string().optional().describe('Target repo directory (auto-resolved if omitted)'),
});
