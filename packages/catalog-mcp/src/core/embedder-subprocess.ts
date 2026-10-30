// packages/catalog-mcp/src/core/embedder-subprocess.ts
import { execFile } from 'node:child_process';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

/** WK-0097 D2: the embedder venv belongs to the code checkout, not to whatever catalog data
 * directory a caller passes around (e.g. an isolated `--root` pilot copy, or an out-of-repo
 * `CATALOG_ROOT`) — installing it twice per catalog copy was never the design. Self-resolves from
 * this module's own location by walking up for a `catalog/` sibling, the same check
 * run-processing.ts's `repoRoot()` already uses to find the server source, so it always lands on
 * the real repo checkout regardless of `dir`/`CATALOG_ROOT`. */
export function codeRoot(): string {
  let dir = path.dirname(fileURLToPath(import.meta.url));
  for (let i = 0; i < 10; i++) {
    if (existsSync(path.join(dir, 'catalog'))) return dir;
    const parent = path.dirname(dir);
    if (parent === dir) break;
    dir = parent;
  }
  throw new Error('code root not found');
}

export function venvPythonPath(dir: string): string {
  return path.join(dir, 'packages', 'catalog-embedder', '.venv', 'bin', 'python');
}

export function runCatalogEmbedder(venvPython: string, args: string[]): Promise<{ stdout: string; stderr: string; code: number }> {
  return new Promise((resolve) => {
    execFile(venvPython, ['-m', 'catalog_embedder', ...args], { maxBuffer: 1024 * 1024 * 64 }, (error, stdout, stderr) => {
      if (stderr) process.stderr.write(stderr);
      resolve({ stdout, stderr, code: error && 'code' in error && typeof error.code === 'number' ? error.code : (error ? 1 : 0) });
    });
  });
}
