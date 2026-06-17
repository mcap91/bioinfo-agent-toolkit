// packages/catalog-mcp/src/core/annotate-entry.ts
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { catalogPaths } from './config.js';
import { persistEntry } from './entry-io.js';

interface AnnotateOptions { dir: string; name: string; section: string; body: string; }
interface AnnotateResult { path: string; section: string; created: boolean; }

/** Append `body` under `## <section>` in entries/<name>.md, creating the section if absent.
 * Frontmatter and every other section are byte-preserved: the file is split textually and the
 * frontmatter is NEVER round-tripped through serializeFrontmatter (which would reorder/reflow it). */
export async function annotateEntry(options: AnnotateOptions): Promise<AnnotateResult> {
  const { dir, name, section, body } = options;
  const filePath = path.join(catalogPaths(dir).entries, `${name}.md`);

  let content: string;
  try { content = await readFile(filePath, 'utf-8'); }
  catch { throw new Error(`Entry ${name}.md not found`); }
  content = content.replace(/\r\n/g, '\n');

  const fm = content.match(/^(---\n[\s\S]*?\n---\n)([\s\S]*)$/);
  if (!fm) throw new Error(`Entry ${name}.md has no frontmatter`);
  const head = fm[1];
  const sectionName = section.trim();
  const { body: newBody, created } = appendToSection(fm[2], sectionName, body.trim());

  const result = await persistEntry({ dir, name, markdown: head + newBody, overwrite: true });
  return { path: result.path, section: sectionName, created };
}

function appendToSection(body: string, section: string, addition: string): { body: string; created: boolean } {
  const lines = body.split('\n');
  const headingRe = new RegExp(`^##\\s+${escapeRegExp(section)}\\s*$`);
  let headingIdx = -1;
  for (let i = 0; i < lines.length; i++) { if (headingRe.test(lines[i])) { headingIdx = i; break; } }

  if (headingIdx === -1) {
    const trimmed = body.replace(/\n+$/, '');
    return { body: `${trimmed}\n\n## ${section}\n\n${addition}\n`, created: true };
  }

  let endIdx = lines.length;
  for (let i = headingIdx + 1; i < lines.length; i++) { if (/^##\s+/.test(lines[i])) { endIdx = i; break; } }
  let insertAt = endIdx;
  while (insertAt - 1 > headingIdx && lines[insertAt - 1].trim() === '') insertAt--;

  const out = [...lines.slice(0, insertAt), '', addition, ...lines.slice(insertAt)].join('\n');
  return { body: out, created: false };
}

function escapeRegExp(s: string): string { return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }
