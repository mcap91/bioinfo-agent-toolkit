// packages/catalog-mcp/src/core/scaffold.ts
import { writeFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { catalogPaths } from './config.js';
import type { Category } from './schema.js';

const REFERENCE_CATEGORIES = new Set(['reference', 'agent-pattern']);

const INSTALLABLE_BODY = `\n## What it does\n\n## Why this verdict\n\n## Mechanical details\n\n## Security\n`;
const REFERENCE_BODY = `\n## What it says\n\n## Why this verdict\n\n## What to adopt\n\n## Security\n`;

interface ScaffoldOptions {
  dir: string;
  name: string;
  category: Category;
  url?: string;
}

interface ScaffoldResult {
  path: string;
}

export async function scaffoldEntry(options: ScaffoldOptions): Promise<ScaffoldResult> {
  const paths = catalogPaths(options.dir);
  const filePath = path.join(paths.entries, `${options.name}.md`);

  if (existsSync(filePath)) {
    throw new Error(`Entry ${options.name}.md already exists at ${filePath}`);
  }

  const today = new Date().toISOString().split('T')[0];
  const lines = [
    '---',
    `name: ${options.name}`,
    `title: ""`,
  ];

  if (options.url) {
    lines.push(`url: ${options.url}`);
  }

  lines.push(
    `category: ${options.category}`,
    `verdict: pilot`,
    `verdict_reason: ""`,
    `status: approved`,
    `tags: []`,
    `reviewed: ${today}`,
    `acquired: ${today}`,
    `supersedes: []`,
    `overlaps: []`,
    '---',
  );

  const body = REFERENCE_CATEGORIES.has(options.category)
    ? REFERENCE_BODY
    : INSTALLABLE_BODY;

  await writeFile(filePath, lines.join('\n') + body, 'utf-8');
  return { path: filePath };
}
