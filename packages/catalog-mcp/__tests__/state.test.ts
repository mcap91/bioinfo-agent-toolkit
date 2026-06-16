// packages/catalog-mcp/__tests__/state.test.ts
import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { mkdtemp, rm, mkdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import { loadState, saveState } from '../src/core/config.js';

describe('state', () => {
  let tmpDir: string;

  beforeEach(async () => {
    tmpDir = await mkdtemp(path.join(os.tmpdir(), 'catalog-state-'));
    await mkdir(path.join(tmpDir, 'catalog'), { recursive: true });
  });

  afterEach(async () => {
    await rm(tmpDir, { recursive: true, force: true });
  });

  it('returns defaults when state.json does not exist', async () => {
    const state = await loadState(tmpDir);
    expect(state.gmail_last_pull_iso).toBeNull();
  });

  it('reads existing state file', async () => {
    await writeFile(
      path.join(tmpDir, 'catalog', 'state.json'),
      JSON.stringify({ gmail_last_pull_iso: '2026-06-10T14:30:00Z' }),
      'utf-8',
    );
    const state = await loadState(tmpDir);
    expect(state.gmail_last_pull_iso).toBe('2026-06-10T14:30:00Z');
  });

  it('saves state and persists to disk', async () => {
    const result = await saveState(tmpDir, { gmail_last_pull_iso: '2026-06-16T09:00:00Z' });
    expect(result.gmail_last_pull_iso).toBe('2026-06-16T09:00:00Z');

    const raw = JSON.parse(
      await readFile(path.join(tmpDir, 'catalog', 'state.json'), 'utf-8'),
    );
    expect(raw.gmail_last_pull_iso).toBe('2026-06-16T09:00:00Z');
  });

  it('merges with existing state on save', async () => {
    await saveState(tmpDir, { gmail_last_pull_iso: '2026-06-10T00:00:00Z' });
    const updated = await saveState(tmpDir, { gmail_last_pull_iso: '2026-06-16T12:00:00Z' });
    expect(updated.gmail_last_pull_iso).toBe('2026-06-16T12:00:00Z');
  });

  it('allows setting state to null', async () => {
    await saveState(tmpDir, { gmail_last_pull_iso: '2026-06-10T00:00:00Z' });
    const cleared = await saveState(tmpDir, { gmail_last_pull_iso: null });
    expect(cleared.gmail_last_pull_iso).toBeNull();
  });

  it('rejects invalid datetime format', async () => {
    await expect(
      saveState(tmpDir, { gmail_last_pull_iso: 'not-a-date' as any }),
    ).rejects.toThrow();
  });

  it('returns defaults for corrupted state file', async () => {
    await writeFile(
      path.join(tmpDir, 'catalog', 'state.json'),
      'not json',
      'utf-8',
    );
    const state = await loadState(tmpDir);
    expect(state.gmail_last_pull_iso).toBeNull();
  });
});
