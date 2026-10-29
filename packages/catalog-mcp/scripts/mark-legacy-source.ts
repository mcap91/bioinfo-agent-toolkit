// packages/catalog-mcp/scripts/mark-legacy-source.ts
// One-off (WK-0086 OR-4): every catalog entry written before provenance tracking existed
// lacks a `source` field, which `entrySchema` now requires. This is NOT a backfill — the
// operator ruled out guessing real provenance ("i dont think we can backfill"). It marks each
// such entry `source: unknown` so it stays schema-valid. New entries never get `unknown`
// (write-entry rejects it) — only this one-time pass may write it.
//
// Textual insert only (no YAML round-trip): adds exactly one `source: unknown` line as the
// last frontmatter field and otherwise leaves the file byte-for-byte unchanged, so key order
// and formatting the original writer chose are preserved.
import { readFile, writeFile, readdir } from 'node:fs/promises';
import path from 'node:path';

const entriesDir = path.resolve('catalog/entries');

const files = (await readdir(entriesDir)).filter((f) => f.endsWith('.md'));
let changed = 0;
for (const file of files) {
  const p = path.join(entriesDir, file);
  const original = await readFile(p, 'utf-8');

  const match = original.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  if (!match) {
    console.error(`${file}: no YAML frontmatter block found, skipped`);
    continue;
  }
  const [, yaml, body] = match;
  if (/^source:\s*/m.test(yaml)) continue; // already has a source field

  const out = `---\n${yaml}\nsource: unknown\n---\n${body}`;
  await writeFile(p, out, 'utf-8');
  changed++;
}
console.log(`marked ${changed}/${files.length} entries with source: unknown`);
