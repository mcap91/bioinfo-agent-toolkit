// packages/catalog-mcp/__tests__/run-processing.test.ts
// WK-0092: one fresh `claude --print` session per queue item, looped by code. `cross-spawn` is
// mocked throughout — these tests never launch a real `claude` process. The usage-parsing tests
// run against real, unedited captures (fixtures/wk-0092/*.json) per AGENTS evidence discipline
// (22-24): the shape is never hand-invented.
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { EventEmitter } from 'node:events';
import { mkdtemp, rm, mkdir, writeFile, readFile } from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath } from 'node:url';

vi.mock('cross-spawn', () => ({ default: vi.fn() }));
vi.mock('../src/core/rebuild-indexes.js', () => ({ rebuildCatalogIndexes: vi.fn().mockResolvedValue({}) }));

import spawn from 'cross-spawn';
import { rebuildCatalogIndexes } from '../src/core/rebuild-indexes.js';
import {
  buildItemPrompt,
  buildClaudeArgs,
  parseSessionUsage,
  processItem,
  runProcessing,
  CATALOG_MCP_TOOLS,
  BUILTIN_TOOLS,
} from '../src/adapter/run-processing.js';
import type { QueueItem } from '../src/core/schema.js';

const mockSpawn = vi.mocked(spawn);
const mockRebuildCatalogIndexes = vi.mocked(rebuildCatalogIndexes);

const FIXTURES_DIR = path.join(path.dirname(fileURLToPath(import.meta.url)), 'fixtures', 'wk-0092');

async function readFixture(name: string): Promise<string> {
  return readFile(path.join(FIXTURES_DIR, name), 'utf-8');
}

// ---------------------------------------------------------------------------
// Fake `claude` child process. Keyed by the `key:` line in the prompt the
// production code writes to stdin (buildItemPrompt always emits that line),
// so each test can script per-item behavior without depending on call order.
// ---------------------------------------------------------------------------
interface ChildBehavior {
  removeFromQueue?: boolean; // simulate the session having removed this item (queue {action:remove})
  stdout?: string; // what the --output-format json session "printed"
  exitCode?: number | null;
  hang?: boolean; // never exits on its own — only resolves if the production code calls kill()
}

function queueFilePath(dir: string): string {
  return path.join(dir, 'catalog', 'queue.json');
}

async function removeKeyFromQueueFile(dir: string, key: string): Promise<void> {
  const raw = await readFile(queueFilePath(dir), 'utf-8');
  const data = JSON.parse(raw);
  data.items = data.items.filter((i: QueueItem) => i.key !== key);
  await writeFile(queueFilePath(dir), JSON.stringify(data), 'utf-8');
}

function installFakeSpawn(dir: string, behaviors: Record<string, ChildBehavior>) {
  mockSpawn.mockImplementation(((_cmd: string, _args: string[], _opts: unknown) => {
    const child = new EventEmitter() as unknown as {
      stdout: EventEmitter;
      stderr: EventEmitter;
      stdin: { write: (d: string) => void; end: () => void };
      kill: (signal?: string) => void;
    } & EventEmitter;
    child.stdout = new EventEmitter();
    child.stderr = new EventEmitter();

    let promptBuf = '';
    child.stdin = {
      write: vi.fn((d: string) => { promptBuf += d; }),
      end: vi.fn(() => {
        const m = promptBuf.match(/^key: (.+)$/m);
        const key = m ? m[1] : '';
        const behavior = behaviors[key] ?? {};
        if (behavior.hang) return; // only resolves via kill() below
        setImmediate(async () => {
          if (behavior.removeFromQueue) await removeKeyFromQueueFile(dir, key);
          if (behavior.stdout) child.stdout.emit('data', Buffer.from(behavior.stdout));
          child.emit('exit', behavior.exitCode ?? 0);
        });
      }),
    } as unknown as typeof child.stdin;

    child.kill = vi.fn((_signal?: string) => {
      child.emit('exit', null); // SIGTERM makes the real process exit; the mock does too
    });

    return child;
  }) as unknown as typeof spawn);
}

async function writeQueueFile(dir: string, items: QueueItem[]): Promise<void> {
  await mkdir(path.join(dir, 'catalog'), { recursive: true });
  await writeFile(queueFilePath(dir), JSON.stringify({ items }), 'utf-8');
}

function item(key: string, extra: Partial<QueueItem> = {}): QueueItem {
  return { key, url: `https://example.com/${key}`, source: 'manual', added: new Date().toISOString(), ...extra } as QueueItem;
}

describe('buildItemPrompt', () => {
  const recipe = 'RECIPE TEXT\n\nStep 1. Do the thing.\n';

  it('embeds only the one given item (key, url, content) — the agent never sees another item or a queue{list} call', () => {
    const prompt = buildItemPrompt(recipe, item('k1', { url: 'https://x/k1', content: 'k1 body text' }));
    expect(prompt).toContain('key: k1');
    expect(prompt).toContain('url: https://x/k1');
    expect(prompt).toContain('k1 body text');
    // No other item's data, and no instruction to list the whole queue.
    expect(prompt).not.toContain('action:list');
    expect(prompt).not.toContain('action: list');
    expect(prompt).not.toContain('k2 body text');
  });

  it('marks the item data as untrusted, between fenced BEGIN/END markers', () => {
    const prompt = buildItemPrompt(recipe, item('k1'));
    expect(prompt).toContain('UNTRUSTED DATA');
    const begin = prompt.indexOf('===BEGIN ITEM DATA===');
    const end = prompt.indexOf('===END ITEM DATA===');
    expect(begin).toBeGreaterThan(-1);
    expect(end).toBeGreaterThan(begin);
  });

  it('renders "(none)" for a url-less or content-less item instead of the literal undefined', () => {
    const prompt = buildItemPrompt(recipe, item('k1', { url: undefined, content: 'only text' }));
    expect(prompt).toContain('url: (none)');
  });
});

describe('buildClaudeArgs', () => {
  it('always pins --model sonnet (WK-0092 OR-1: never the inherited default)', () => {
    const args = buildClaudeArgs('/tmp/mcp.json');
    const i = args.indexOf('--model');
    expect(i).toBeGreaterThan(-1);
    expect(args[i + 1]).toBe('sonnet');
  });

  it('always passes --strict-mcp-config, so only the catalog MCP server loads (no kb-wiki leak)', () => {
    expect(buildClaudeArgs('/tmp/mcp.json')).toContain('--strict-mcp-config');
  });

  it('restricts the built-in tool set to WebSearch, WebFetch, Read via --tools (removes Edit/Write/Bash/Task*)', () => {
    const args = buildClaudeArgs('/tmp/mcp.json');
    const i = args.indexOf('--tools');
    expect(i).toBeGreaterThan(-1);
    expect(args[i + 1]).toBe(BUILTIN_TOOLS.join(','));
    expect(args[i + 1]).toBe('WebSearch,WebFetch,Read');
  });

  it('pre-authorizes exactly the 3 built-ins plus the catalog MCP tools the single-item recipe calls, and nothing else', () => {
    const args = buildClaudeArgs('/tmp/mcp.json');
    const i = args.indexOf('--allowedTools');
    const j = args.indexOf('--output-format'); // next flag after the variadic --allowedTools list
    const allowed = args.slice(i + 1, j);
    expect(allowed.sort()).toEqual([...BUILTIN_TOOLS, ...CATALOG_MCP_TOOLS].sort());
    // The recipe no longer calls `index` (code calls the index function directly, decision 6).
    expect(allowed).not.toContain('mcp__catalog__index');
  });
});

describe('parseSessionUsage (golden capture)', () => {
  // Real, unedited `claude --print --model sonnet --tools "" --strict-mcp-config
  // --output-format json` captures (2026-10-28). See the module-level "Usage source" comment in
  // run-processing.ts for why the result object's usage, not the session JSONL, is parsed.
  it('parses the single-turn capture: a trivial 1-turn reply', async () => {
    const stdout = await readFixture('single-turn-result.json');
    const usage = parseSessionUsage(stdout);
    expect(usage).toEqual({
      sessionId: '27d70b74-c06f-40fc-b479-d0260abb15df',
      model: 'claude-sonnet-5',
      input: 2,
      cacheRead: 0,
      cacheWrite: 17014,
      output: 4,
    });
  });

  it('parses the multi-turn capture: usage is cumulative across both turns, matching the session JSONL sum byte-for-byte (verified by hand against the transcript, cited in run-processing.ts)', async () => {
    const stdout = await readFixture('multi-turn-result.json');
    const usage = parseSessionUsage(stdout);
    expect(usage).toEqual({
      sessionId: '85446442-2755-4275-81a8-1b8732705236',
      model: 'claude-sonnet-5',
      input: 4,
      cacheRead: 18317,
      cacheWrite: 18477,
      output: 66,
    });
  });

  it('returns null for text that is not a parsable result object, instead of throwing (a crashed session prints nothing usable)', () => {
    expect(parseSessionUsage('not json')).toBeNull();
    expect(parseSessionUsage('{"type":"system"}')).toBeNull();
  });
});

describe('processItem', () => {
  let dir: string;
  beforeEach(async () => {
    dir = await mkdtemp(path.join(os.tmpdir(), 'catalog-run-processing-'));
    mockSpawn.mockReset();
  });
  afterEach(async () => { await rm(dir, { recursive: true, force: true }); });

  it('status "done": the session removes the item from the queue, so the code-side check finds it gone', async () => {
    await writeQueueFile(dir, [item('k1')]);
    const stdout = await readFixture('single-turn-result.json');
    installFakeSpawn(dir, { k1: { removeFromQueue: true, stdout } });

    const outcome = await processItem(dir, item('k1'), 'RECIPE', '/tmp/mcp.json', { timeoutMs: 5000 });

    expect(outcome.status).toBe('done');
    expect(outcome.timedOut).toBe(false);
    expect(outcome.usage?.model).toBe('claude-sonnet-5');
  });

  it('status "failed": the item is still in the queue after its session exits 0 — outcome is decided by queue state, not exit code (design decision 4)', async () => {
    await writeQueueFile(dir, [item('k1')]);
    const stdout = await readFixture('single-turn-result.json');
    installFakeSpawn(dir, { k1: { removeFromQueue: false, stdout, exitCode: 0 } });

    const outcome = await processItem(dir, item('k1'), 'RECIPE', '/tmp/mcp.json', { timeoutMs: 5000 });

    expect(outcome.status).toBe('failed');
    expect(outcome.timedOut).toBe(false);
  });

  it('timeout path: a session that never exits is killed once the per-item timeout elapses, and is logged failed (item never left the queue)', async () => {
    await writeQueueFile(dir, [item('k1')]);
    installFakeSpawn(dir, { k1: { hang: true } });

    const outcome = await processItem(dir, item('k1'), 'RECIPE', '/tmp/mcp.json', { timeoutMs: 20 });

    expect(outcome.timedOut).toBe(true);
    expect(outcome.status).toBe('failed');
  });
});

describe('runProcessing', () => {
  let dir: string;
  beforeEach(async () => {
    dir = await mkdtemp(path.join(os.tmpdir(), 'catalog-run-processing-loop-'));
    await mkdir(path.join(dir, 'catalog'), { recursive: true });
    await writeFile(path.join(dir, 'catalog', 'recipe.md'), 'RECIPE TEXT', 'utf-8');
    mockSpawn.mockReset();
    mockRebuildCatalogIndexes.mockClear();
  });
  afterEach(async () => { await rm(dir, { recursive: true, force: true }); });

  it('a failed item does not stop the loop: the next item is still processed and logged', async () => {
    await writeQueueFile(dir, [item('k1'), item('k2')]);
    const stdout = await readFixture('single-turn-result.json');
    installFakeSpawn(dir, {
      k1: { removeFromQueue: false, stdout }, // fails — left in queue
      k2: { removeFromQueue: true, stdout }, // succeeds
    });

    await runProcessing({ dir, timeoutMs: 5000 });

    expect(mockSpawn).toHaveBeenCalledTimes(2);
    const log = (await readFile(path.join(dir, 'catalog', 'process-log.jsonl'), 'utf-8'))
      .trim().split('\n').map((l) => JSON.parse(l));
    expect(log).toHaveLength(2);
    expect(log[0]).toMatchObject({ key: 'k1', status: 'failed' });
    expect(log[1]).toMatchObject({ key: 'k2', status: 'done' });
  });

  it('--limit processes only the first N items in stored queue order, leaving the rest untouched', async () => {
    await writeQueueFile(dir, [item('k1'), item('k2'), item('k3')]);
    const stdout = await readFixture('single-turn-result.json');
    installFakeSpawn(dir, {
      k1: { removeFromQueue: true, stdout },
      k2: { removeFromQueue: true, stdout },
      k3: { removeFromQueue: true, stdout },
    });

    await runProcessing({ dir, limit: 2, timeoutMs: 5000 });

    expect(mockSpawn).toHaveBeenCalledTimes(2);
    const remaining = JSON.parse(await readFile(queueFilePath(dir), 'utf-8'));
    expect(remaining.items.map((i: QueueItem) => i.key)).toEqual(['k3']); // never touched by this run
    const log = (await readFile(path.join(dir, 'catalog', 'process-log.jsonl'), 'utf-8'))
      .trim().split('\n').map((l) => JSON.parse(l));
    expect(log.map((r) => r.key)).toEqual(['k1', 'k2']);
  });

  it('calls the shared rebuildCatalogIndexes function exactly once after the loop, never per item, and with no LLM step — the same function the `index` MCP tool calls, so the search index/graph/vectors stay in sync too (not just index.md)', async () => {
    await writeQueueFile(dir, [item('k1'), item('k2')]);
    const stdout = await readFixture('single-turn-result.json');
    installFakeSpawn(dir, {
      k1: { removeFromQueue: true, stdout },
      k2: { removeFromQueue: true, stdout },
    });

    await runProcessing({ dir, timeoutMs: 5000 });

    expect(mockRebuildCatalogIndexes).toHaveBeenCalledTimes(1);
    expect(mockRebuildCatalogIndexes).toHaveBeenCalledWith({ dir, format: 'full' });
  });

  it('writes one cost-log JSON line per item with the designed fields (ts, key, status, wall_s, model, input, cache_read, cache_write, output, session_id)', async () => {
    await writeQueueFile(dir, [item('k1')]);
    const stdout = await readFixture('multi-turn-result.json');
    installFakeSpawn(dir, { k1: { removeFromQueue: true, stdout } });

    await runProcessing({ dir, timeoutMs: 5000 });

    const [record] = (await readFile(path.join(dir, 'catalog', 'process-log.jsonl'), 'utf-8'))
      .trim().split('\n').map((l) => JSON.parse(l));
    expect(Object.keys(record).sort()).toEqual(
      ['cache_read', 'cache_write', 'input', 'key', 'model', 'output', 'session_id', 'status', 'ts', 'wall_s'].sort(),
    );
    expect(record.model).toBe('claude-sonnet-5');
    expect(record.cache_read).toBe(18317);
    expect(record.cache_write).toBe(18477);
    expect(record.input).toBe(4);
    expect(record.output).toBe(66);
    expect(record.session_id).toBe('85446442-2755-4275-81a8-1b8732705236');
  });
});
