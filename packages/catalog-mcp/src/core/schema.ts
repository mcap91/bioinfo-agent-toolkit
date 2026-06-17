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

export const DECISION_STATUSES = ['adopted', 'rejected'] as const;
export type DecisionStatus = (typeof DECISION_STATUSES)[number];

export const SOURCES = ['manual', 'reddit', 'slack', 'email', 'other'] as const;

export type Category = (typeof CATEGORIES)[number];

export const entrySchema = z.object({
  name: z.string().regex(/^[a-z0-9]+(-[a-z0-9]+)*$/, 'Must be kebab-case'),
  title: z.string().min(1),
  url: z.string().url().optional(),
  category: z.enum(CATEGORIES),
  decision_status: z.enum(DECISION_STATUSES).optional(),
  summary: z.string().min(1),
  install: z.string().optional(),
  tags: z.array(z.string()).min(1),
  workflows: z.array(z.string()).optional(),
  reviewed: z.string().regex(/^\d{4}-\d{2}-\d{2}$/),
  acquired: z.string().regex(/^\d{4}-\d{2}-\d{2}$/).optional(),
  license: z.string().optional(),
  security_flags: z.array(z.string()).optional(),
  supersedes: z.array(z.string()).optional(),
  overlaps: z.array(z.string()).optional(),
}).strict();

export type CatalogEntry = z.infer<typeof entrySchema>;

export const queueItemSchema = z
  .object({
    url: z.string().url().optional(),
    content: z.string().optional(),
    key: z.string(),
    source: z.enum(SOURCES).default('manual'),
    notes: z.string().optional(),
    context: z.record(z.string(), z.unknown()).optional(),
    added: z.string(),
    status: z.enum(['pending', 'error', 'parked']).default('pending'),
    error_message: z.string().optional(),
  })
  .refine((i) => Boolean(i.url) || Boolean(i.content), {
    message: 'queue item requires a url or content',
  });

export type QueueItem = z.infer<typeof queueItemSchema>;

export const queueSchema = z.object({
  items: z.array(queueItemSchema),
});

const blockedDomainSchema = z.object({
  host: z.string(),
  allow_paths: z.array(z.string()).optional(),
});

export const configSchema = z.object({
  url_patterns: z.array(z.string()),
  blocked_domains: z.array(blockedDomainSchema).default([]),
  min_clean_chars: z.number().default(200),
  gmail_fallback: z.boolean().default(true),
});

export type BlockedDomain = z.infer<typeof blockedDomainSchema>;

export type CatalogConfig = z.infer<typeof configSchema>;

export const stateSchema = z.object({
  gmail_last_pull_iso: z.string().datetime().nullable().default(null),
});

export type CatalogState = z.infer<typeof stateSchema>;

export const dirSchema = z.object({
  dir: z.string().optional().describe('Target repo directory (auto-resolved if omitted)'),
});

export const PROJECT_STATUSES = ['active', 'paused', 'completed'] as const;
export const PRIORITIES = ['high', 'medium', 'low'] as const;

export const projectSchema = z.object({
  name: z.string().min(1),
  status: z.enum(PROJECT_STATUSES),
  workflows: z.array(z.string()).optional(),
  priority: z.enum(PRIORITIES).default('medium'),
  notes: z.string().optional(),
});

export type Project = z.infer<typeof projectSchema>;

export const goalsSchema = z.object({
  projects: z.array(projectSchema),
});

export type Goals = z.infer<typeof goalsSchema>;
