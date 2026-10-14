import { describe, it, expect } from 'vitest';
import { execFile } from 'node:child_process';
import path from 'node:path';
import { existsSync } from 'node:fs';

const REPO_DIR = path.resolve(__dirname, '..', '..', '..');
const VENV_PYTHON = path.join(REPO_DIR, 'packages', 'catalog-embedder', '.venv', 'bin', 'python');

function runSearch(query: string, extra: string[] = []): Promise<{ stdout: string; code: number }> {
  return new Promise((resolve) => {
    execFile(
      VENV_PYTHON,
      ['-m', 'catalog_embedder', 'search', '--query', query, '--dir', REPO_DIR, '--limit', '5', ...extra],
      { maxBuffer: 1024 * 1024 },
      (error, stdout) => {
        resolve({ stdout, code: error && 'code' in error && typeof error.code === 'number' ? error.code : (error ? 1 : 0) });
      },
    );
  });
}

describe.skipIf(!existsSync(VENV_PYTHON))('search integration (Python subprocess)', () => {
  it('returns valid JSON with expected shape', async () => {
    const { stdout, code } = await runSearch('pdf');
    expect(code).toBe(0);
    const data = JSON.parse(stdout);
    expect(data).toHaveProperty('results');
    expect(data).toHaveProperty('total');
    expect(data).toHaveProperty('truncated');
    expect(Array.isArray(data.results)).toBe(true);
    expect(data.results.length).toBeGreaterThan(0);
    const r = data.results[0];
    expect(r).toHaveProperty('name');
    expect(r).toHaveProperty('score');
    expect(typeof r.score).toBe('number');
  });

  it('does not pass --alpha (removed arg would cause exit 2)', async () => {
    const { stdout, code } = await runSearch('test');
    expect(code).toBe(0);
    const data = JSON.parse(stdout);
    expect(data.results).toBeDefined();
  });

  it('accepts --threshold and --method args', async () => {
    const { stdout, code } = await runSearch('pdf', ['--threshold', '0.1', '--method', 'bm25']);
    expect(code).toBe(0);
    const data = JSON.parse(stdout);
    expect(Array.isArray(data.results)).toBe(true);
  });

  it('empty query returns results with score 0', async () => {
    const { stdout, code } = await runSearch('');
    expect(code).toBe(0);
    const data = JSON.parse(stdout);
    expect(data.total).toBeGreaterThan(0);
    for (const r of data.results) {
      expect(r.score).toBe(0);
    }
  });

  it('BM25 rescue: exact name ranks first', async () => {
    const { stdout, code } = await runSearch('markitdown');
    expect(code).toBe(0);
    const data = JSON.parse(stdout);
    expect(data.results[0].name).toBe('markitdown');
    expect(data.results[0].score).toBeGreaterThan(0);
  });
});
