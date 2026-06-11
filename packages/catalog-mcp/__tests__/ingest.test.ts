// packages/catalog-mcp/__tests__/ingest.test.ts
import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { mkdtemp, rm, mkdir, writeFile } from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import { ingest } from '../src/core/ingest.js';
import { readQueue } from '../src/core/queue.js';

describe('ingest', () => {
  let tmpDir: string;

  beforeEach(async () => {
    tmpDir = await mkdtemp(path.join(os.tmpdir(), 'catalog-ingest-'));
    await mkdir(path.join(tmpDir, 'catalog', 'entries'), { recursive: true });
    await writeFile(
      path.join(tmpDir, 'catalog', 'queue.json'),
      JSON.stringify({ items: [] }),
      'utf-8',
    );
  });

  afterEach(async () => {
    await rm(tmpDir, { recursive: true, force: true });
  });

  it('adds new URLs to queue', async () => {
    const result = await ingest({
      dir: tmpDir,
      items: [{ url: 'https://github.com/org/new-tool' }],
    });
    expect(result.added).toHaveLength(1);
    expect(result.skipped).toHaveLength(0);
  });

  it('skips URLs already in queue', async () => {
    await ingest({
      dir: tmpDir,
      items: [{ url: 'https://github.com/org/tool' }],
    });
    const result = await ingest({
      dir: tmpDir,
      items: [{ url: 'https://github.com/org/tool' }],
    });
    expect(result.added).toHaveLength(0);
    expect(result.skipped).toHaveLength(1);
  });

  it('skips URLs already in catalog entries', async () => {
    await writeFile(
      path.join(tmpDir, 'catalog', 'entries', 'existing.md'),
      '---\nname: existing\ntitle: Existing\nurl: https://github.com/org/existing\ncategory: skill\nverdict: adopt\nverdict_reason: good\ntags: [test]\nreviewed: 2026-06-03\n---\n',
      'utf-8',
    );
    const result = await ingest({
      dir: tmpDir,
      items: [{ url: 'https://github.com/org/existing' }],
    });
    expect(result.added).toHaveLength(0);
    expect(result.skipped).toHaveLength(1);
  });

  it('skips dedup when deduplicate is false', async () => {
    await ingest({
      dir: tmpDir,
      items: [{ url: 'https://github.com/org/tool' }],
    });
    const result = await ingest({
      dir: tmpDir,
      items: [{ url: 'https://github.com/org/tool' }],
      deduplicate: false,
    });
    expect(result.added).toHaveLength(1);
  });
});

describe('ingest phase 2', () => {
  let dir: string;
  beforeEach(async () => {
    dir = await mkdtemp(path.join(os.tmpdir(), 'catalog-i-'));
    await mkdir(path.join(dir, 'catalog', 'entries'), { recursive: true });
    await writeFile(path.join(dir, 'catalog', 'queue.json'), '{"items":[]}\n', 'utf-8');
  });
  afterEach(async () => { await rm(dir, { recursive: true, force: true }); });

  it('ingests a content-only item and assigns a content key', async () => {
    const r = await ingest({ dir, items: [{ content: 'a free-form note', source: 'email' }] });
    expect(r.count).toBe(1);
    const item = (await readQueue(dir)).items[0];
    expect(item.url).toBeUndefined();
    expect(item.key).toMatch(/^content:[0-9a-f]{16}$/);
  });

  it('dedups identical content (whitespace variants)', async () => {
    await ingest({ dir, items: [{ content: 'same  thing' }] });
    const r = await ingest({ dir, items: [{ content: 'same thing\n' }] });
    expect(r.skipped[0].reason).toMatch(/already in queue/);
  });

  it('dedups url items by url (existing behavior)', async () => {
    await ingest({ dir, items: [{ url: 'https://x.com/a' }] });
    const r = await ingest({ dir, items: [{ url: 'https://x.com/a' }] });
    expect(r.skipped).toHaveLength(1);
  });

  it('dedups urls case-insensitively against queue', async () => {
    await ingest({ dir, items: [{ url: 'https://github.com/Org/Tool' }] });
    const r = await ingest({ dir, items: [{ url: 'https://github.com/org/tool' }] });
    expect(r.skipped).toHaveLength(1);
    expect(r.skipped[0].reason).toMatch(/already in queue/);
  });

  it('dedups urls case-insensitively against existing entries', async () => {
    await writeFile(
      path.join(dir, 'catalog', 'entries', 'existing.md'),
      '---\nname: existing\ntitle: Existing\nurl: https://github.com/Org/Existing\ncategory: skill\nverdict: adopt\nverdict_reason: good\ntags: [test]\nreviewed: 2026-06-03\n---\n',
      'utf-8',
    );
    const r = await ingest({ dir, items: [{ url: 'https://github.com/org/existing' }] });
    expect(r.skipped).toHaveLength(1);
    expect(r.skipped[0].reason).toMatch(/already cataloged/);
  });
});
