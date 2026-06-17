// packages/catalog-mcp/__tests__/lint.test.ts
import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { mkdtemp, rm, mkdir, writeFile, readFile } from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import { lintEntry, lint } from '../src/core/lint.js';

describe('lintEntry', () => {
  const validFrontmatter = {
    name: 'test-tool',
    title: 'Test Tool',
    url: 'https://github.com/org/test-tool',
    category: 'skill',
    summary: 'looks promising',
    tags: ['testing'],
    reviewed: '2026-06-03',
  };

  it('returns no errors for valid entry', () => {
    const result = lintEntry('test-tool', validFrontmatter, '## What it does\n## Why this verdict\n## Mechanical details\n## Security\n');
    expect(result.errors).toEqual([]);
  });

  it('errors on missing required field', () => {
    const { title, ...noTitle } = validFrontmatter;
    const result = lintEntry('test-tool', noTitle, '');
    expect(result.errors.length).toBeGreaterThan(0);
    expect(result.errors[0]).toContain('title');
  });

  it('errors on a retired verdict key', () => {
    const result = lintEntry('test-tool', { ...validFrontmatter, verdict: 'maybe' }, '');
    expect(result.errors.length).toBeGreaterThan(0);
  });

  it('warns on missing acquired (migration)', () => {
    const result = lintEntry('test-tool', validFrontmatter, '## What it does\n');
    expect(result.warnings.some((w: string) => w.includes('acquired'))).toBe(true);
  });

  it('warns on missing Security section (migration)', () => {
    const result = lintEntry('test-tool', validFrontmatter, '## What it does\n## Why this verdict\n');
    expect(result.warnings.some((w: string) => w.includes('Security'))).toBe(true);
  });

  it('errors on name mismatch with filename', () => {
    const result = lintEntry('wrong-name', validFrontmatter, '');
    expect(result.errors.some((e: string) => e.includes('name'))).toBe(true);
  });
});

describe('lint --fix no longer adds a status field (removed in v2.1.0)', () => {
  let dir: string;
  // Errored (no tags -> schema fails) AND no status -> previously triggered the status default.
  const erroredNoStatus = (name: string) =>
    `---\nname: ${name}\ntitle: "${name}"\nurl: https://x.com/${name}\ncategory: skill\nsummary: ok\nreviewed: 2026-06-08\n---\nbody\n`;

  beforeEach(async () => {
    dir = await mkdtemp(path.join(os.tmpdir(), 'catalog-lint-'));
    await mkdir(path.join(dir, 'catalog', 'entries'), { recursive: true });
    await writeFile(path.join(dir, 'catalog', 'entries', 'e1.md'), erroredNoStatus('e1'), 'utf-8');
  });
  afterEach(async () => { await rm(dir, { recursive: true, force: true }); });

  it('lint({fix:true}) does not write a status line', async () => {
    await lint({ dir, fix: true });
    const md = await readFile(path.join(dir, 'catalog', 'entries', 'e1.md'), 'utf-8');
    expect(md).not.toContain('status:');
  });
});
