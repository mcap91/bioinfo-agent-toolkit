// packages/catalog-mcp/src/core/frontmatter.ts
import { readFile, readdir } from 'node:fs/promises';
import path from 'node:path';

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
  const frontmatter = parseSimpleYaml(yamlStr);
  return { frontmatter, body, raw: normalized };
}

/**
 * Minimal YAML parser sufficient for catalog entry frontmatter.
 * Handles: strings, quoted strings, arrays (flow [...] and block - item),
 * numbers, booleans, empty strings, null.
 * Does NOT handle nested objects, multi-line strings, or anchors.
 */
function parseSimpleYaml(yaml: string): Record<string, unknown> {
  const result: Record<string, unknown> = {};
  const lines = yaml.split('\n');
  let i = 0;

  while (i < lines.length) {
    const line = lines[i];
    const kvMatch = line.match(/^([a-z_]+):\s*(.*)$/);
    if (!kvMatch) {
      i++;
      continue;
    }

    const key = kvMatch[1];
    let value = kvMatch[2].trim();

    // Flow array: [item1, item2]
    if (value.startsWith('[')) {
      result[key] = parseFlowArray(value);
      i++;
      continue;
    }

    // Check for block array on next lines
    if (value === '' && i + 1 < lines.length && lines[i + 1].match(/^\s+-\s/)) {
      const items: string[] = [];
      i++;
      while (i < lines.length && lines[i].match(/^\s+-\s/)) {
        const itemMatch = lines[i].match(/^\s+-\s+(.*)$/);
        if (itemMatch) items.push(unquote(itemMatch[1].trim()));
        i++;
      }
      result[key] = items;
      continue;
    }

    // Scalar
    result[key] = parseScalar(value);
    i++;
  }

  return result;
}

function parseFlowArray(value: string): string[] {
  const inner = value.slice(1, value.lastIndexOf(']'));
  if (inner.trim() === '') return [];
  return inner.split(',').map((s) => unquote(s.trim()));
}

function parseScalar(value: string): unknown {
  if (value === '' || value === 'null' || value === '~') return undefined;
  if (value === 'true') return true;
  if (value === 'false') return false;
  if (/^-?\d+$/.test(value)) return parseInt(value, 10);
  if (/^-?\d+\.\d+$/.test(value)) return parseFloat(value);
  return unquote(value);
}

function unquote(s: string): string {
  if ((s.startsWith('"') && s.endsWith('"')) || (s.startsWith("'") && s.endsWith("'"))) {
    return s.slice(1, -1);
  }
  return s;
}

export function serializeFrontmatter(
  frontmatter: Record<string, unknown>,
  body: string,
): string {
  const yaml = Object.entries(frontmatter)
    .map(([key, value]) => {
      if (value === undefined || value === null) return null;
      if (Array.isArray(value)) {
        if (value.length === 0) return `${key}: []`;
        return `${key}: [${value.map((v) => quoteIfNeeded(String(v))).join(', ')}]`;
      }
      if (typeof value === 'string' && value === '') return `${key}: ""`;
      if (typeof value === 'string') return `${key}: ${quoteIfNeeded(value)}`;
      return `${key}: ${value}`;
    })
    .filter(Boolean)
    .join('\n');
  return `---\n${yaml}\n---\n${body}`;
}

function quoteIfNeeded(s: string): string {
  if (/[:#\[\]{},>|&*!%@`]/.test(s) || s.includes("'") || s === '') {
    return `"${s.replace(/"/g, '\\"')}"`;
  }
  return s;
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
