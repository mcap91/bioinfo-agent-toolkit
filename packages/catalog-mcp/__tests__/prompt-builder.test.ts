// packages/catalog-mcp/__tests__/prompt-builder.test.ts
import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { mkdtemp, rm, mkdir, readFile } from 'node:fs/promises';
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
