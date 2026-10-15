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
      ['-m', 'catalog_embedder', 'search', '--query', query, '--dir', REPO_DIR, ...extra],
      { maxBuffer: 1024 * 1024 * 64 },
      (error, stdout) => {
        resolve({ stdout, code: error && 'code' in error && typeof error.code === 'number' ? error.code : (error ? 1 : 0) });
      },
    );
  });
}

describe.skipIf(!existsSync(VENV_PYTHON))('search integration (Python subprocess)', () => {
  it('returns valid JSON with the survey shape and no scores', async () => {
    const { stdout, code } = await runSearch('pdf');
    expect(code).toBe(0);
    const data = JSON.parse(stdout);
    expect(data).toHaveProperty('results');
    expect(data).toHaveProperty('swept_terms');
    expect(data).toHaveProperty('lexical_total');
    expect(data).toHaveProperty('total');
    expect(Array.isArray(data.results)).toBe(true);
    expect(data.results.length).toBeGreaterThan(0);
    for (const r of data.results) {
      expect(r).not.toHaveProperty('score');
      expect(r.match).toHaveProperty('type');
    }
  });

  it('lookup regression: exact name ranks first in the lexical block', async () => {
    const { stdout, code } = await runSearch('markitdown');
    expect(code).toBe(0);
    const data = JSON.parse(stdout);
    expect(data.results[0].name).toBe('markitdown');
    expect(data.results[0].match.type).toBe('lexical');
  });

  it('repeated --term flags sweep multiple terms', async () => {
    const { stdout, code } = await runSearch('ocr', ['--term', 'ocr', '--term', 'agent memory']);
    expect(code).toBe(0);
    const data = JSON.parse(stdout);
    expect(data.swept_terms.length).toBe(2);
  });

  it('retired flags are rejected', async () => {
    const { code } = await runSearch('pdf', ['--threshold', '0.1']);
    expect(code).toBe(2);
  });

  it('empty query lists every entry as match.type listing', async () => {
    const { stdout, code } = await runSearch('');
    expect(code).toBe(0);
    const data = JSON.parse(stdout);
    expect(data.total).toBeGreaterThan(0);
    expect(data.swept_terms).toEqual([]);
    for (const r of data.results) {
      expect(r.match.type).toBe('listing');
    }
  });

  it('prose fallback stays narrow: one AND term, lexical_total under 50', async () => {
    const { stdout, code } = await runSearch('tools for parsing scanned PDFs?');
    expect(code).toBe(0);
    const data = JSON.parse(stdout);
    expect(data.swept_terms.length).toBe(1);
    expect(data.lexical_total).toBeLessThan(50);
  });
});
