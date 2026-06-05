// packages/catalog-mcp/__tests__/index-gen.test.ts
import { describe, it, expect } from 'vitest';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { generateIndex } from '../src/core/index-gen.js';

const repoRoot = path.resolve(import.meta.dirname, '..', '..', '..');

describe('generateIndex', () => {
  it('produces byte-identical output to current catalog/index.md', async () => {
    const expected = (await readFile(
      path.join(repoRoot, 'catalog', 'index.md'),
      'utf-8',
    )).replace(/\r\n/g, '\n');
    const result = await generateIndex({
      dir: repoRoot,
      format: 'full',
      includeDrafts: false,
    });
    expect(result.content).toBe(expected);
  });

  it('reports correct entry count', async () => {
    const { readdir } = await import('node:fs/promises');
    const entryFiles = (await readdir(path.join(repoRoot, 'catalog', 'entries'))).filter(f => f.endsWith('.md'));
    const result = await generateIndex({
      dir: repoRoot,
      format: 'full',
      includeDrafts: false,
    });
    expect(result.entryCount).toBe(entryFiles.length);
  });
});
