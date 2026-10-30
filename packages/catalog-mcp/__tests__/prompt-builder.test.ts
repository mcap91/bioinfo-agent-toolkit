// packages/catalog-mcp/__tests__/prompt-builder.test.ts
import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { mkdtemp, rm, mkdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath } from 'node:url';
import { buildPrompt } from '../src/core/prompt-builder.js';

const FIXTURES_DIR = path.join(path.dirname(fileURLToPath(import.meta.url)), 'fixtures', 'wk-0084');

describe('buildPrompt — content-only items (WK-0084 R2)', () => {
  let dir: string;
  beforeEach(async () => {
    dir = await mkdtemp(path.join(os.tmpdir(), 'catalog-prompt-'));
    await mkdir(path.join(dir, 'catalog', 'entries'), { recursive: true });
  });
  afterEach(async () => { await rm(dir, { recursive: true, force: true }); });

  // Golden fixture: the real, unedited fenced ```text block that sat at catalog/inbox.md:5-25
  // on 2026-10-26 (git commit 5421671's parent) — a plain Instagram-caption paste with no
  // `source:` line, so drain ingests it as a queue item with `content` and no `url`. This is
  // exactly the shape WK-0084 found build-prompt unable to accept (url was required).
  it('builds a prompt with no url, from the real url-less inbox text block', async () => {
    const content = await readFile(path.join(FIXTURES_DIR, 'vector-db-reel-caption.txt'), 'utf-8');

    const result = await buildPrompt({ dir, content });

    // No url was passed, so the prompt must not promise one — an agent asked to read a
    // "## URL" section with nothing under it would have no way to tell "absent" from "empty".
    expect(result.prompt).not.toContain('## URL');
    // The real content still reaches the prompt verbatim.
    expect(result.prompt).toContain('Mixpeek turns video, images, audio and docs into features you can search.');
    expect(result.prompt).toContain('## Fetched Content');
  });

  it('still includes a "## URL" section when a url is given (unchanged behavior)', async () => {
    const result = await buildPrompt({ dir, url: 'https://github.com/org/repo', content: 'some content' });
    expect(result.prompt).toContain('## URL\n\nhttps://github.com/org/repo');
  });
});

// WK-0095: the result used to embed one table row per catalog entry (`## Current Catalog
// (compact)` inside `prompt`, duplicated again as `catalog_summary`) — 739 entries measured at
// ~297k characters, and Claude Code rejected the 600k-character result outright. `search` now
// does dedup/overlap detection instead, so the result must not grow with the entry count at all.
describe('buildPrompt result size (WK-0095)', () => {
  let smallDir: string;
  let bigDir: string;
  beforeEach(async () => {
    smallDir = await mkdtemp(path.join(os.tmpdir(), 'catalog-prompt-small-'));
    bigDir = await mkdtemp(path.join(os.tmpdir(), 'catalog-prompt-big-'));
    await mkdir(path.join(smallDir, 'catalog', 'entries'), { recursive: true });
    await mkdir(path.join(bigDir, 'catalog', 'entries'), { recursive: true });
    await writeFile(path.join(smallDir, 'catalog', 'entries', 'only-entry.md'), entryFixture(0), 'utf-8');
    for (let i = 0; i < 1000; i++) {
      await writeFile(path.join(bigDir, 'catalog', 'entries', `generated-entry-${i}.md`), entryFixture(i), 'utf-8');
    }
  });
  afterEach(async () => {
    await rm(smallDir, { recursive: true, force: true });
    await rm(bigDir, { recursive: true, force: true });
  });

  it('returns the same result size against a 1-entry catalog and a 1,000-entry catalog, given identical input', async () => {
    const content = 'X'.repeat(500);
    const small = await buildPrompt({ dir: smallDir, content });
    const big = await buildPrompt({ dir: bigDir, content });
    expect(JSON.stringify(big).length).toBe(JSON.stringify(small).length);
    // None of the 1,000 generated entries' titles leak into the result.
    expect(big.prompt).not.toContain('generated-entry-500');
    expect(big.prompt).not.toContain('Generated Entry 500');
  });

  it('result does not grow when content length is held constant, regardless of catalog size (direct 1k-entry check)', async () => {
    const content = 'fixed content body';
    const result = await buildPrompt({ dir: bigDir, content });
    // No whole-catalog table of any kind remains in the prompt.
    expect(result.prompt).not.toContain('Current Catalog');
    expect(result.prompt).not.toContain('| Title | Category |');
    expect(JSON.stringify(result).length).toBeLessThan(10_000);
  });

  it('result has only the `prompt` field — entry_schema/security_checklist/catalog_summary are not duplicated as separate top-level fields', async () => {
    const result = await buildPrompt({ dir: smallDir, content: 'c' });
    expect(Object.keys(result)).toEqual(['prompt']);
    expect(result.prompt).toContain('## Entry Schema');
    expect(result.prompt).toContain('## Security Assessment');
  });
});

function entryFixture(i: number): string {
  return `---
name: generated-entry-${i}
title: "Generated Entry ${i}"
url: https://example.com/tool-${i}
source: text
category: cli-tool
summary: "generated fixture entry number ${i} for the WK-0095 size test"
tags: [fixture]
reviewed: 2026-01-01
acquired: 2026-01-01
---

## What it is

Fixture entry ${i}, generated only to pad out the catalog for a size test.

## Security

No flags.
`;
}
