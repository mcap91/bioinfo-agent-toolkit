// packages/catalog-mcp/__tests__/ingest.test.ts
import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { mkdtemp, rm, mkdir, writeFile } from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import { ingest } from '../src/core/ingest.js';

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
