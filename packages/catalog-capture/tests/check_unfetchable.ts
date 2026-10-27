// Tiny cross-check harness: run catalog-mcp's real `drainInbox()` against one
// URL at a time (a fresh temp catalog dir each time, same shape drain.test.ts
// uses), so Python tests can assert parity between drain's blocking rule and
// NEEDS_LINK_RE without reimplementing either (not a reimplementation of
// drain.ts — the actual function, per repo convention — see parse_inbox.ts).
// Takes a file path to a JSON array of URLs on argv[2]; writes a JSON array
// of booleans to stdout (true = drain blocked that URL with ⚠ needs-link).
import { readFileSync } from 'node:fs';
import { mkdtemp, mkdir, writeFile, rm } from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import { drainInbox } from '../../catalog-mcp/src/core/drain.js';

const CONFIG = JSON.stringify({ url_patterns: [], blocked_domains: [], min_clean_chars: 200 });

async function checkOne(url: string): Promise<boolean> {
  const dir = await mkdtemp(path.join(os.tmpdir(), 'catalog-capture-parity-'));
  try {
    await mkdir(path.join(dir, 'catalog', 'entries'), { recursive: true });
    await writeFile(path.join(dir, 'catalog', 'queue.json'), '{"items":[]}\n', 'utf-8');
    await writeFile(path.join(dir, 'catalog', 'config.json'), CONFIG, 'utf-8');
    await writeFile(path.join(dir, 'catalog', 'inbox.md'), `${url}\n`, 'utf-8');
    const r = await drainInbox(dir);
    return r.blocked === 1;
  } finally {
    await rm(dir, { recursive: true, force: true });
  }
}

async function main() {
  const listPath = process.argv[2];
  const urls: string[] = JSON.parse(readFileSync(listPath, 'utf-8'));
  const results: boolean[] = [];
  for (const url of urls) results.push(await checkOne(url));
  process.stdout.write(JSON.stringify(results));
}

main();
