// packages/catalog-mcp/scripts/migrate-classification.ts
// One-off: migrate catalog entries verdict/verdict_reason -> decision_status/summary.
import { readFile, writeFile, readdir } from 'node:fs/promises';
import path from 'node:path';

const STATUS_MAP: Record<string, string | null> = {
  adopt: 'adopted',
  skip: 'rejected',
  note: null, // unset (open)
  watch: null,
  pilot: null,
};

const entriesDir = path.resolve('catalog/entries');

const files = (await readdir(entriesDir)).filter((f) => f.endsWith('.md'));
let changed = 0;
for (const file of files) {
  const p = path.join(entriesDir, file);
  const original = await readFile(p, 'utf-8');
  // Normalize to LF first so output is LF-clean (repo is LF-blobs / CRLF-worktree).
  let out = original.replace(/\r\n/g, '\n');

  // verdict: <value>  ->  decision_status: <mapped>  (or remove the line for open)
  out = out.replace(/^verdict:\s*(\w+)\s*$/m, (_m, v: string) => {
    if (!(v in STATUS_MAP)) throw new Error(`${file}: unknown verdict "${v}"`);
    const mapped = STATUS_MAP[v];
    return mapped === null ? ' REMOVE ' : `decision_status: ${mapped}`;
  });
  out = out.replace(/^ REMOVE \n/m, ''); // drop the line for open entries

  // verdict_reason: ...  ->  summary: ...   (value preserved verbatim)
  out = out.replace(/^verdict_reason:/m, 'summary:');

  // body heading
  out = out.replace(/^##\s*Why this verdict\s*$/m, '## Assessment');

  if (out !== original) { await writeFile(p, out, 'utf-8'); changed++; }
}
console.log(`migrated ${changed}/${files.length} entries`);
