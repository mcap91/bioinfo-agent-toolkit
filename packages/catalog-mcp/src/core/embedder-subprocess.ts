// packages/catalog-mcp/src/core/embedder-subprocess.ts
import { execFile } from 'node:child_process';
import path from 'node:path';

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
