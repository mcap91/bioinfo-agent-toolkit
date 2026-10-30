// packages/catalog-mcp/src/core/file-lock.ts
import { open, stat, unlink } from 'node:fs/promises';

const STALE_MS = 60_000;
const TIMEOUT_MS = 30_000;
const RETRY_MIN_MS = 20;
const RETRY_MAX_MS = 120;

/** Run `fn` while holding an exclusive lock file at `lockPath`. Safe across processes:
 * catalog:process --concurrency runs several sessions, each with its own MCP server process,
 * all writing the same queue, inbox, and entries.
 *
 * The lock is created with O_EXCL (`wx`), so exactly one process wins. Others wait and retry
 * with jitter instead of failing. A lock older than STALE_MS (its holder crashed — holders keep
 * it for milliseconds) is removed and the wait continues. Throws after `timeoutMs`. */
export async function withFileLock<T>(
  lockPath: string,
  fn: () => Promise<T>,
  opts: { timeoutMs?: number; staleMs?: number } = {},
): Promise<T> {
  const timeoutMs = opts.timeoutMs ?? TIMEOUT_MS;
  const staleMs = opts.staleMs ?? STALE_MS;
  const deadline = Date.now() + timeoutMs;

  for (;;) {
    try {
      const handle = await open(lockPath, 'wx');
      try {
        await handle.writeFile(JSON.stringify({ pid: process.pid, timestamp: Date.now() }), 'utf-8');
      } finally {
        await handle.close();
      }
      break;
    } catch (err) {
      if ((err as NodeJS.ErrnoException).code !== 'EEXIST') throw err;
    }

    if (await isStale(lockPath, staleMs)) {
      await unlink(lockPath).catch(() => {});
      continue;
    }
    if (Date.now() >= deadline) {
      throw new Error(`Timed out after ${timeoutMs}ms waiting for lock ${lockPath}`);
    }
    await sleep(RETRY_MIN_MS + Math.random() * (RETRY_MAX_MS - RETRY_MIN_MS));
  }

  try {
    return await fn();
  } finally {
    await unlink(lockPath).catch(() => {});
  }
}

/** A lock is stale when its file is older than `staleMs` (by mtime, so a holder that crashed
 * before writing the lock's contents still ages out). */
async function isStale(lockPath: string, staleMs: number): Promise<boolean> {
  try {
    return Date.now() - (await stat(lockPath)).mtimeMs > staleMs;
  } catch {
    return false; // released between our open and stat — just retry
  }
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
