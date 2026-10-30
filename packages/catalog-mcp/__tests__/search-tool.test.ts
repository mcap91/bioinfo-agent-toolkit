// packages/catalog-mcp/__tests__/search-tool.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { fileURLToPath } from 'node:url';

const THIS_FILE = fileURLToPath(import.meta.url);
const MISSING_FILE = '/nonexistent/catalog-embedder/.venv/bin/python';

vi.mock('../src/core/embedder-subprocess.js', () => ({
  runCatalogEmbedder: vi.fn(),
  venvPythonPath: vi.fn(),
  codeRoot: vi.fn(),
}));

import { tools } from '../src/tools.js';
import { runCatalogEmbedder, venvPythonPath, codeRoot } from '../src/core/embedder-subprocess.js';

const searchTool = tools.find((t) => t.name === 'search')!;
const mockRunCatalogEmbedder = vi.mocked(runCatalogEmbedder);
const mockVenvPythonPath = vi.mocked(venvPythonPath);
const mockCodeRoot = vi.mocked(codeRoot);

const EMPTY_RESPONSE = { results: [], swept_terms: [], lexical_total: 0, total: 0 };

describe('search tool', () => {
  beforeEach(() => {
    mockRunCatalogEmbedder.mockReset();
    mockVenvPythonPath.mockReset();
    mockCodeRoot.mockReset();
    mockCodeRoot.mockReturnValue('/code/root');
    mockVenvPythonPath.mockReturnValue(THIS_FILE); // real file on disk — existsSync passes
    mockRunCatalogEmbedder.mockResolvedValue({
      stdout: JSON.stringify(EMPTY_RESPONSE),
      stderr: '',
      code: 0,
    });
  });

  it('builds argv for a query-only call: no --term, --semantic-n 10 (backward compat)', async () => {
    const input = searchTool.inputSchema.parse({ dir: '/repo', query: 'ocr' });
    await searchTool.handler(input);

    expect(mockRunCatalogEmbedder).toHaveBeenCalledTimes(1);
    const args = mockRunCatalogEmbedder.mock.calls[0]![1];
    expect(args).toEqual(
      expect.arrayContaining(['--query', 'ocr', '--semantic-n', '10']),
    );
    expect(args).not.toContain('--term');
  });

  it('builds argv for a full call: repeated --term, --semantic-n, --category', async () => {
    const input = searchTool.inputSchema.parse({
      dir: '/repo',
      query: 'ocr',
      terms: ['ocr', 'text extraction'],
      semantic_n: 5,
      category: 'skill',
    });
    await searchTool.handler(input);

    const args = mockRunCatalogEmbedder.mock.calls[0]![1];
    expect(args).toEqual(
      expect.arrayContaining([
        '--term', 'ocr',
        '--term', 'text extraction',
        '--semantic-n', '5',
        '--category', 'skill',
      ]),
    );
    // Multi-word term passes as ONE argv element, not split across two.
    expect(args).toContain('text extraction');
  });

  it('rejects out-of-bounds input via Zod', () => {
    const base = { dir: '/repo', query: 'ocr' };
    expect(searchTool.inputSchema.safeParse({ ...base, terms: Array(51).fill('x') }).success).toBe(false);
    expect(searchTool.inputSchema.safeParse({ ...base, terms: ['x'.repeat(250)] }).success).toBe(false);
    expect(searchTool.inputSchema.safeParse({ ...base, semantic_n: 0 }).success).toBe(false);
    expect(searchTool.inputSchema.safeParse(base).success).toBe(true);
  });

  it('returns the setup-instruction error object when the venv is missing', async () => {
    mockVenvPythonPath.mockReturnValue(MISSING_FILE);
    const input = searchTool.inputSchema.parse({ dir: '/repo', query: 'ocr' });
    const result = await searchTool.handler(input) as { error: string };

    expect(result.error).toMatch(/not available/i);
    expect(mockRunCatalogEmbedder).not.toHaveBeenCalled();
  });

  it('WK-0097 D2: looks up the embedder venv under the code root, not the catalog dir — an out-of-repo CATALOG_ROOT (an isolated --root pilot copy) has no venv of its own, so a pilot without this would report search as unavailable even though the code checkout has a working venv', async () => {
    const input = searchTool.inputSchema.parse({ dir: '/outside/pilot-catalog', query: 'ocr' });
    await searchTool.handler(input);

    expect(mockCodeRoot).toHaveBeenCalled();
    expect(mockVenvPythonPath).toHaveBeenCalledWith('/code/root');
    // The catalog data root is unchanged: the embedder still searches the pilot's own entries.
    const args = mockRunCatalogEmbedder.mock.calls[0]![1];
    expect(args).toEqual(expect.arrayContaining(['--dir', '/outside/pilot-catalog']));
  });

  it('returns a Search failed error when the subprocess exits non-zero', async () => {
    mockRunCatalogEmbedder.mockResolvedValue({ stdout: '', stderr: 'boom', code: 1 });
    const input = searchTool.inputSchema.parse({ dir: '/repo', query: 'ocr' });
    const result = await searchTool.handler(input) as { error: string; stderr: string };

    expect(result.error).toBe('Search failed');
    expect(result.stderr).toBe('boom');
  });
});
