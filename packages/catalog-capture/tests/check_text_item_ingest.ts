// I1/I7 evidence: a fenced ```text block (the shape this package's Instagram
// needs-link rewrite produces) is a `kind: 'text'` InboxItem, and drain.ts's
// `ruleBlocked` check only applies to `kind: 'url'` items — so a text block
// whose `source:` line is an instagram.com reel URL must NOT be blocked by
// the real config's `instagram.com` entry, even though a bare instagram.com
// URL line is. Seeded with the repo's real catalog/config.json, same as
// check_unfetchable_real_config.ts, so this is evidence against the actual
// shipped rule, not a reimplementation of it.
import { readFileSync } from 'node:fs';
import { mkdtemp, mkdir, writeFile, readFile, rm } from 'node:fs/promises';
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

async function main() {
  const sourceUrl = process.argv[2];
  const body = process.argv[3];
  const dir = await mkdtemp(path.join(os.tmpdir(), 'catalog-capture-ig-text-item-'));
  try {
    await mkdir(path.join(dir, 'catalog', 'entries'), { recursive: true });
    await writeFile(path.join(dir, 'catalog', 'queue.json'), '{"items":[]}\n', 'utf-8');
    await writeFile(path.join(dir, 'catalog', 'config.json'), CONFIG, 'utf-8');
    const inbox = `\`\`\`text\nsource: ${sourceUrl}\n${body}\n\`\`\`\n`;
    await writeFile(path.join(dir, 'catalog', 'inbox.md'), inbox, 'utf-8');
    const result = await drainInbox(dir);
    const queue = JSON.parse(await readFile(path.join(dir, 'catalog', 'queue.json'), 'utf-8'));
    process.stdout.write(JSON.stringify({ result, queue }));
  } finally {
    await rm(dir, { recursive: true, force: true });
  }
}

main();
