// packages/catalog-mcp/__tests__/force-draft.test.ts
import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { mkdtemp, rm, mkdir, writeFile, readFile } from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import { tools } from '../src/tools.js';
import { approveEntry, rejectEntry } from '../src/core/review.js';
import { scaffoldEntry } from '../src/core/scaffold.js';
import { lint } from '../src/core/lint.js';

// Mirrors review.test.ts's draft() helper.
const draft = (name: string) =>
  `---\nname: ${name}\ntitle: "${name}"\nurl: https://x.com/${name}\ncategory: skill\nverdict: pilot\nverdict_reason: looks ok\nstatus: draft\ntags: [t]\nreviewed: 2026-06-08\n---\nbody\n`;

const approved = (name: string) =>
  `---\nname: ${name}\ntitle: "approved-${name}"\nurl: https://x.com/${name}\ncategory: skill\nverdict: adopt\nverdict_reason: great\nstatus: approved\ntags: [t]\nreviewed: 2026-06-08\n---\nbody\n`;

describe('B-1: index clamp under force-draft', () => {
  let dir: string;

  beforeEach(async () => {
    dir = await mkdtemp(path.join(os.tmpdir(), 'catalog-fd-idx-'));
    await mkdir(path.join(dir, 'catalog', 'entries'), { recursive: true });
    // One draft entry, one approved entry.
    await writeFile(path.join(dir, 'catalog', 'entries', 'd1.md'), draft('d1'), 'utf-8');
    await writeFile(path.join(dir, 'catalog', 'entries', 'a1.md'), approved('a1'), 'utf-8');
    // Set force-draft env.
    process.env['CATALOG_FORCE_DRAFT'] = '1';
  });

  afterEach(async () => {
    delete process.env['CATALOG_FORCE_DRAFT'];
    await rm(dir, { recursive: true, force: true });
  });

  it('with CATALOG_FORCE_DRAFT=1, index({include_drafts:true}) excludes draft entries and includes only approved', async () => {
    const indexTool = tools.find((t) => t.name === 'index')!;
    expect(indexTool).toBeDefined();

    const result = await indexTool.handler({ dir, format: 'full', include_drafts: true }) as {
      entryCount: number;
      path: string;
    };

    // entryCount should be 1 (only approved), not 2.
    expect(result.entryCount).toBe(1);

    // Read the written index file.
    const indexContent = await readFile(path.join(dir, 'catalog', 'index.md'), 'utf-8');

    // Draft title must NOT appear.
    expect(indexContent).not.toContain('"d1"');
    expect(indexContent).not.toContain('status: draft');

    // Approved title MUST appear.
    expect(indexContent).toContain('approved-a1');
  });
});

describe('B-2: review refuses approve/reject under force-draft', () => {
  let dir: string;

  beforeEach(async () => {
    dir = await mkdtemp(path.join(os.tmpdir(), 'catalog-fd-rev-'));
    await mkdir(path.join(dir, 'catalog', 'entries'), { recursive: true });
    await writeFile(path.join(dir, 'catalog', 'entries', 'd1.md'), draft('d1'), 'utf-8');
    process.env['CATALOG_FORCE_DRAFT'] = '1';
  });

  afterEach(async () => {
    delete process.env['CATALOG_FORCE_DRAFT'];
    await rm(dir, { recursive: true, force: true });
  });

  it('approveEntry throws with /force-draft/ message', async () => {
    await expect(approveEntry(dir, 'd1')).rejects.toThrow(/force-draft/);
  });

  it('rejectEntry throws with /force-draft/ message', async () => {
    await expect(rejectEntry(dir, 'd1', 'some reason')).rejects.toThrow(/force-draft/);
  });

  it('entry remains status: draft after failed approve', async () => {
    await approveEntry(dir, 'd1').catch(() => {});
    const md = await readFile(path.join(dir, 'catalog', 'entries', 'd1.md'), 'utf-8');
    expect(md).toContain('status: draft');
    expect(md).not.toContain('status: approved');
  });

  it('entry remains status: draft after failed reject', async () => {
    await rejectEntry(dir, 'd1', 'reason').catch(() => {});
    const md = await readFile(path.join(dir, 'catalog', 'entries', 'd1.md'), 'utf-8');
    expect(md).toContain('status: draft');
    expect(md).not.toContain('status: approved');
  });
});

describe('scaffold clamps to draft under force-draft', () => {
  let dir: string;

  beforeEach(async () => {
    dir = await mkdtemp(path.join(os.tmpdir(), 'catalog-fd-scaf-'));
    await mkdir(path.join(dir, 'catalog', 'entries'), { recursive: true });
    process.env['CATALOG_FORCE_DRAFT'] = '1';
  });

  afterEach(async () => {
    delete process.env['CATALOG_FORCE_DRAFT'];
    await rm(dir, { recursive: true, force: true });
  });

  it('scaffoldEntry writes status: draft under CATALOG_FORCE_DRAFT (not approved)', async () => {
    await scaffoldEntry({ dir, name: 's1', category: 'skill' });
    const md = await readFile(path.join(dir, 'catalog', 'entries', 's1.md'), 'utf-8');
    expect(md).toContain('status: draft');
    expect(md).not.toContain('status: approved');
  });

  it('scaffoldEntry still writes status: approved when NOT in force-draft', async () => {
    delete process.env['CATALOG_FORCE_DRAFT'];
    await scaffoldEntry({ dir, name: 's2', category: 'skill' });
    const md = await readFile(path.join(dir, 'catalog', 'entries', 's2.md'), 'utf-8');
    expect(md).toContain('status: approved');
  });
});

describe('B-4: lint --fix clamps default status to draft under force-draft (final writer)', () => {
  let dir: string;

  // Entry with a lint error (no tags -> schema fails) AND no status -> triggers applyFixes.
  const erroredNoStatus = (name: string) =>
    `---\nname: ${name}\ntitle: "${name}"\nurl: https://x.com/${name}\ncategory: skill\nverdict: pilot\nverdict_reason: ok\nreviewed: 2026-06-08\n---\nbody\n`;

  beforeEach(async () => {
    dir = await mkdtemp(path.join(os.tmpdir(), 'catalog-fd-lint-'));
    await mkdir(path.join(dir, 'catalog', 'entries'), { recursive: true });
    await writeFile(path.join(dir, 'catalog', 'entries', 'e1.md'), erroredNoStatus('e1'), 'utf-8');
    process.env['CATALOG_FORCE_DRAFT'] = '1';
  });

  afterEach(async () => {
    delete process.env['CATALOG_FORCE_DRAFT'];
    await rm(dir, { recursive: true, force: true });
  });

  it('lint({fix:true}) on a status-less errored entry writes status: draft, never approved, under force-draft', async () => {
    await lint({ dir, fix: true });
    const md = await readFile(path.join(dir, 'catalog', 'entries', 'e1.md'), 'utf-8');
    expect(md).toContain('status: draft');
    expect(md).not.toContain('status: approved');
  });

  it('lint({fix:true}) still defaults to approved when NOT in force-draft', async () => {
    delete process.env['CATALOG_FORCE_DRAFT'];
    await lint({ dir, fix: true });
    const md = await readFile(path.join(dir, 'catalog', 'entries', 'e1.md'), 'utf-8');
    expect(md).toContain('status: approved');
  });
});
