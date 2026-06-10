// packages/catalog-mcp/__tests__/scaffold.test.ts
import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { mkdtemp, readFile, rm, mkdir } from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import { scaffoldEntry } from '../src/core/scaffold.js';

describe('scaffoldEntry', () => {
  let tmpDir: string;

  beforeEach(async () => {
    tmpDir = await mkdtemp(path.join(os.tmpdir(), 'catalog-test-'));
    await mkdir(path.join(tmpDir, 'catalog', 'entries'), { recursive: true });
  });

  afterEach(async () => {
    await rm(tmpDir, { recursive: true, force: true });
  });

  it('creates an entry file with correct frontmatter', async () => {
    const result = await scaffoldEntry({
      dir: tmpDir,
      name: 'my-tool',
      category: 'skill',
    });
    const content = await readFile(result.path, 'utf-8');
    expect(content).toContain('name: my-tool');
    expect(content).toContain('category: skill');
    expect(content).toContain('## What it does');
  });

  it('does not emit a status field (removed in v2.1.0)', async () => {
    const result = await scaffoldEntry({
      dir: tmpDir,
      name: 'my-tool',
      category: 'skill',
    });
    const content = await readFile(result.path, 'utf-8');
    expect(content).not.toContain('status:');
  });

  it('sets acquired to today', async () => {
    const result = await scaffoldEntry({
      dir: tmpDir,
      name: 'my-tool',
      category: 'skill',
    });
    const content = await readFile(result.path, 'utf-8');
    const today = new Date().toISOString().split('T')[0];
    expect(content).toContain(`acquired: ${today}`);
  });

  it('includes url when provided', async () => {
    const result = await scaffoldEntry({
      dir: tmpDir,
      name: 'my-tool',
      category: 'skill',
      url: 'https://github.com/org/my-tool',
    });
    const content = await readFile(result.path, 'utf-8');
    expect(content).toContain('url: https://github.com/org/my-tool');
  });

  it('refuses to overwrite existing file', async () => {
    await scaffoldEntry({ dir: tmpDir, name: 'my-tool', category: 'skill' });
    await expect(
      scaffoldEntry({ dir: tmpDir, name: 'my-tool', category: 'skill' }),
    ).rejects.toThrow(/already exists/);
  });

  it('uses reference body template for reference category', async () => {
    const result = await scaffoldEntry({
      dir: tmpDir,
      name: 'my-ref',
      category: 'reference',
    });
    const content = await readFile(result.path, 'utf-8');
    expect(content).toContain('## What it says');
    expect(content).not.toContain('## What it does');
  });
});
