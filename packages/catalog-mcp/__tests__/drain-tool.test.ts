// packages/catalog-mcp/__tests__/drain-tool.test.ts
import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { mkdtemp, rm, mkdir, writeFile } from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import { tools } from '../src/tools.js';
import { readQueue } from '../src/core/queue.js';

// Mirror drain.test.ts's CONFIG exactly.
const CONFIG = JSON.stringify({
  url_patterns: [],
  blocked_domains: [{ host: 'instagram.com' }, { host: 'linkedin.com', allow_paths: ['/pulse/'] }],
  min_clean_chars: 200,
  gmail_fallback: true,
});

describe('drain tool wiring', () => {
  let dir: string;

  beforeEach(async () => {
    dir = await mkdtemp(path.join(os.tmpdir(), 'catalog-drain-tool-'));
    await mkdir(path.join(dir, 'catalog', 'entries'), { recursive: true });
    await writeFile(path.join(dir, 'catalog', 'queue.json'), '{"items":[]}\n', 'utf-8');
    await writeFile(path.join(dir, 'catalog', 'config.json'), CONFIG, 'utf-8');
    // One fetchable URL in the inbox.
    await writeFile(
      path.join(dir, 'catalog', 'inbox.md'),
      'https://github.com/org/tool\n',
      'utf-8',
    );
  });

  afterEach(async () => {
    await rm(dir, { recursive: true, force: true });
  });

  it('drain tool is registered in tools array', () => {
    const drainTool = tools.find((t) => t.name === 'drain');
    expect(drainTool).toBeDefined();
  });

  it('drain tool returns { ingested, blocked, skipped } with ingested === 1 for a fetchable URL', async () => {
    const drainTool = tools.find((t) => t.name === 'drain')!;
    const result = await drainTool.handler({ dir }) as {
      ingested: number;
      blocked: number;
      skipped: { url: string; reason: string }[];
    };

    // Shape check.
    expect(typeof result.ingested).toBe('number');
    expect(typeof result.blocked).toBe('number');
    expect(Array.isArray(result.skipped)).toBe(true);

    // One fetchable URL should be ingested.
    expect(result.ingested).toBe(1);
  });

  it('drain tool results in queue having 1 item after ingesting a fetchable URL', async () => {
    const drainTool = tools.find((t) => t.name === 'drain')!;
    await drainTool.handler({ dir });

    const queue = await readQueue(dir);
    expect(queue.items).toHaveLength(1);
  });
});
