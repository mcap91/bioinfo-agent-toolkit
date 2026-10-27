// I7 evidence harness: same shape as check_unfetchable.ts, but seeds the temp
// catalog's config.json with the REAL repo's `catalog/config.json`
// `blocked_domains` (which has `{ "host": "instagram.com" }`, no `allow_paths`)
// instead of an empty array. check_unfetchable.ts's empty blocked_domains is
// correct for the Reddit parity test (Reddit blocking comes from the
// hardcoded `urlUnfetchable()` rule, not config), but it would make every
// Instagram URL look unblocked here regardless of path — not evidence of
// what drain.ts actually does against the real config this repo ships.
import { readFileSync } from 'node:fs';
import { mkdtemp, mkdir, writeFile, rm } from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import { drainInbox } from '../../catalog-mcp/src/core/drain.js';

const REPO_ROOT = path.resolve(__dirname, '../../..');
const realConfig = JSON.parse(readFileSync(path.join(REPO_ROOT, 'catalog', 'config.json'), 'utf-8'));
const CONFIG = JSON.stringify({
  url_patterns: [],
  blocked_domains: realConfig.blocked_domains,
  min_clean_chars: 200,
});

async function checkOne(url: string): Promise<boolean> {
  const dir = await mkdtemp(path.join(os.tmpdir(), 'catalog-capture-ig-parity-'));
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
