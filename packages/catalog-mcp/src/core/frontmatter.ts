// packages/catalog-mcp/src/core/frontmatter.ts
import { readFile, readdir } from 'node:fs/promises';
import path from 'node:path';
import { parse as yamlParse, stringify as yamlStringify } from 'yaml';

export interface ParsedEntry {
  frontmatter: Record<string, unknown>;
  body: string;
  raw: string;
}

export function parseFrontmatter(content: string): ParsedEntry {
  const normalized = content.replace(/\r\n/g, '\n');
  const match = normalized.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  if (!match) {
    throw new Error('No YAML frontmatter found');
  }
  const yamlStr = match[1];
  const body = match[2];
  const parsed = yamlParse(yamlStr) ?? {};
  if (typeof parsed !== 'object' || parsed === null || Array.isArray(parsed)) {
    throw new Error('YAML frontmatter must be a mapping');
  }
  const frontmatter = parsed as Record<string, unknown>;
  return { frontmatter, body, raw: normalized };
}

export function serializeFrontmatter(
  frontmatter: Record<string, unknown>,
  body: string,
): string {
  const yamlStr = yamlStringify(frontmatter, { lineWidth: 0 });
  return `---\n${yamlStr}---\n${body}`;
}

export async function readAllEntries(
  entriesDir: string,
): Promise<Map<string, ParsedEntry>> {
  const entries = new Map<string, ParsedEntry>();
  let files: string[];
  try {
    files = await readdir(entriesDir);
  } catch {
    return entries;
  }
  for (const file of files.sort()) {
    if (!file.endsWith('.md')) continue;
    const content = await readFile(path.join(entriesDir, file), 'utf-8');
    try {
      entries.set(file.replace('.md', ''), parseFrontmatter(content));
    } catch {
      // Skip unparseable files — lint will catch them
    }
  }
  return entries;
}
