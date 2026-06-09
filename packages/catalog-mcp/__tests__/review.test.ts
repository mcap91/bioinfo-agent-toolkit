import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { mkdtemp, rm, mkdir, writeFile, readFile } from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import { listDrafts, approveEntry, rejectEntry } from '../src/core/review.js';

const draft = (name: string) =>
  `---\nname: ${name}\ntitle: "${name}"\nurl: https://x.com/${name}\ncategory: skill\nverdict: pilot\nverdict_reason: looks ok\nstatus: draft\ntags: [t]\nreviewed: 2026-06-08\n---\nbody\n`;

describe('review', () => {
  let dir: string;
  beforeEach(async () => {
    dir = await mkdtemp(path.join(os.tmpdir(), 'catalog-r-'));
    await mkdir(path.join(dir, 'catalog', 'entries'), { recursive: true });
    await writeFile(path.join(dir, 'catalog', 'entries', 'd1.md'), draft('d1'), 'utf-8');
  });
  afterEach(async () => { await rm(dir, { recursive: true, force: true }); });

  const read = (n: string) => readFile(path.join(dir, 'catalog', 'entries', `${n}.md`), 'utf-8');

  it('lists only drafts', async () => {
    const items = await listDrafts(dir);
    expect(items.map((i) => i.name)).toContain('d1');
  });

  it('approve flips status to approved', async () => {
    await approveEntry(dir, 'd1');
    const md = await read('d1');
    expect(md).toContain('status: approved');
    expect(md).not.toContain('status: draft');
  });

  it('reject writes verdict skip + approved + [rejected] reason', async () => {
    await rejectEntry(dir, 'd1', 'not relevant');
    const md = await read('d1');
    expect(md).toContain('verdict: skip');
    expect(md).toContain('status: approved');
    expect(md).toContain('verdict_reason: "[rejected] not relevant"');
  });
});
