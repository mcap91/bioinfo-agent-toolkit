// packages/catalog-mcp/__tests__/file-lock.test.ts
import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { mkdtemp, rm, writeFile, readFile, utimes } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { spawn } from 'node:child_process';
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath } from 'node:url';
import { withFileLock } from '../src/core/file-lock.js';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const LOCK_MODULE = path.join(HERE, '..', 'src', 'core', 'file-lock.ts');

/** Unprotected read-modify-write with a yield in the middle — loses updates unless serialized. */
async function slowIncrement(counterPath: string): Promise<void> {
  const n = Number(await readFile(counterPath, 'utf-8'));
  await new Promise((r) => setTimeout(r, 2));
  await writeFile(counterPath, String(n + 1), 'utf-8');
}

describe('withFileLock', () => {
  let dir: string;
  let lockPath: string;
  let counterPath: string;
  beforeEach(async () => {
    dir = await mkdtemp(path.join(os.tmpdir(), 'catalog-lock-'));
    lockPath = path.join(dir, '.test.lock');
    counterPath = path.join(dir, 'counter');
    await writeFile(counterPath, '0', 'utf-8');
  });
  afterEach(async () => { await rm(dir, { recursive: true, force: true }); });

  it('serializes concurrent callers: 20 overlapping read-modify-writes all land (the old lock threw "Queue is locked" here instead of waiting)', async () => {
    await Promise.all(Array.from({ length: 20 }, () => withFileLock(lockPath, () => slowIncrement(counterPath))));
    expect(await readFile(counterPath, 'utf-8')).toBe('20');
    expect(existsSync(lockPath)).toBe(false);
  });

  it('serializes across processes — the real case: each parallel session has its own MCP server process', async () => {
    const script = `
      import { withFileLock } from ${JSON.stringify(LOCK_MODULE)};
      import { readFile, writeFile } from 'node:fs/promises';
      const [lockPath, counterPath] = process.argv.slice(-2);
      for (let i = 0; i < 10; i++) {
        await withFileLock(lockPath, async () => {
          const n = Number(await readFile(counterPath, 'utf-8'));
          await new Promise((r) => setTimeout(r, 2));
          await writeFile(counterPath, String(n + 1), 'utf-8');
        });
      }
    `;
    const runChild = () => new Promise<number | null>((resolve) => {
      const child = spawn(process.execPath, ['--import', 'tsx', '--input-type=module', '-e', script, lockPath, counterPath], {
        stdio: ['ignore', 'ignore', 'inherit'],
      });
      child.on('exit', resolve);
    });
    const codes = await Promise.all(Array.from({ length: 4 }, runChild));
    expect(codes).toEqual([0, 0, 0, 0]);
    expect(await readFile(counterPath, 'utf-8')).toBe('40');
  }, 30_000);

  it('releases the lock when fn throws, so the next caller is not blocked', async () => {
    await expect(withFileLock(lockPath, async () => { throw new Error('boom'); })).rejects.toThrow('boom');
    expect(existsSync(lockPath)).toBe(false);
    await expect(withFileLock(lockPath, async () => 'ok')).resolves.toBe('ok');
  });

  it('reclaims a stale lock left by a crashed holder (old mtime, even if empty)', async () => {
    await writeFile(lockPath, '', 'utf-8');
    const old = new Date(Date.now() - 120_000);
    await utimes(lockPath, old, old);
    await expect(withFileLock(lockPath, async () => 'ok')).resolves.toBe('ok');
  });

  it('times out instead of waiting forever on a fresh lock held by someone else', async () => {
    await writeFile(lockPath, JSON.stringify({ pid: 1, timestamp: Date.now() }), 'utf-8');
    await expect(withFileLock(lockPath, async () => 'never', { timeoutMs: 200 })).rejects.toThrow(/Timed out/);
    expect(existsSync(lockPath)).toBe(true); // not ours to remove
  });
});
