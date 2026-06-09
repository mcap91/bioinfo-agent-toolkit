// packages/catalog-mcp/__tests__/write-entry.test.ts
import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { mkdtemp, rm, mkdir, readFile, writeFile as fsWriteFile } from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import { writeEntry } from '../src/core/write-entry.js';

const validEntry = `---
name: test-tool
title: "Test Tool"
url: https://github.com/org/test-tool
category: skill
verdict: pilot
verdict_reason: "looks promising"
tags: [testing]
reviewed: 2026-06-03
---

## What it does

A test tool.

## Why this verdict

Looks good.

## Mechanical details

Install with npm.

## Security

MIT license. No flags.
`;

describe('writeEntry', () => {
  let tmpDir: string;

  beforeEach(async () => {
    tmpDir = await mkdtemp(path.join(os.tmpdir(), 'catalog-write-'));
    await mkdir(path.join(tmpDir, 'catalog', 'entries'), { recursive: true });
    await fsWriteFile(path.join(tmpDir, 'catalog', 'config.json'), '{"url_patterns":[]}', 'utf-8');
  });

  afterEach(async () => {
    await rm(tmpDir, { recursive: true, force: true });
  });

  it('writes a valid entry to disk', async () => {
    const result = await writeEntry({ dir: tmpDir, entry: validEntry, name: 'test-tool' });
    expect(result.path).toContain('test-tool.md');
    const content = await readFile(result.path, 'utf-8');
    expect(content).toContain('name: test-tool');
  });

  it('injects acquired date if missing', async () => {
    const result = await writeEntry({ dir: tmpDir, entry: validEntry, name: 'test-tool' });
    const content = await readFile(result.path, 'utf-8');
    expect(content).toContain('acquired:');
  });

  it('rejects invalid entry', async () => {
    const badEntry = '---\nname: test\n---\nNo required fields\n';
    await expect(
      writeEntry({ dir: tmpDir, entry: badEntry, name: 'test' }),
    ).rejects.toThrow(/Invalid entry/);
  });

  it('refuses to overwrite without flag', async () => {
    await writeEntry({ dir: tmpDir, entry: validEntry, name: 'test-tool' });
    await expect(
      writeEntry({ dir: tmpDir, entry: validEntry, name: 'test-tool' }),
    ).rejects.toThrow(/already exists/);
  });

  it('allows overwrite with flag', async () => {
    await writeEntry({ dir: tmpDir, entry: validEntry, name: 'test-tool' });
    await expect(
      writeEntry({ dir: tmpDir, entry: validEntry, name: 'test-tool', overwrite: true }),
    ).resolves.toBeDefined();
  });
});

const entryNoStatus = `---\nname: w\ntitle: "W"\nurl: https://x.com/w\ncategory: skill\nverdict: pilot\nverdict_reason: ok\ntags: [a]\nreviewed: 2026-06-08\n---\nbody\n`;

describe('write-entry force-draft', () => {
  let dir: string;
  beforeEach(async () => {
    dir = await mkdtemp(path.join(os.tmpdir(), 'catalog-w-'));
    await mkdir(path.join(dir, 'catalog', 'entries'), { recursive: true });
    delete process.env.CATALOG_FORCE_DRAFT;
  });
  afterEach(async () => { await rm(dir, { recursive: true, force: true }); delete process.env.CATALOG_FORCE_DRAFT; });

  it('defaults to draft when status omitted', async () => {
    await writeEntry({ dir, entry: entryNoStatus, name: 'w' });
    expect(await readFile(path.join(dir, 'catalog', 'entries', 'w.md'), 'utf-8')).toContain('status: draft');
  });

  it('clamps to draft under CATALOG_FORCE_DRAFT even if approved requested', async () => {
    process.env.CATALOG_FORCE_DRAFT = '1';
    await writeEntry({ dir, entry: entryNoStatus, name: 'w', status: 'approved' });
    const onDisk = await readFile(path.join(dir, 'catalog', 'entries', 'w.md'), 'utf-8');
    expect(onDisk).toContain('status: draft');
    expect(onDisk).not.toContain('status: approved');
  });
});
