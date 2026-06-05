// packages/catalog-mcp/__tests__/goals.test.ts
import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { mkdtemp, rm, mkdir, writeFile, readFile } from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import { listGoals, getGoal, addGoal, updateGoal, removeGoal } from '../src/core/goals.js';

describe('goals', () => {
  let tmpDir: string;

  beforeEach(async () => {
    tmpDir = await mkdtemp(path.join(os.tmpdir(), 'catalog-goals-'));
    await mkdir(path.join(tmpDir, 'catalog'), { recursive: true });
    await writeFile(
      path.join(tmpDir, 'catalog', 'goals.json'),
      JSON.stringify({ projects: [] }),
      'utf-8',
    );
  });

  afterEach(async () => {
    await rm(tmpDir, { recursive: true, force: true });
  });

  it('lists empty projects', async () => {
    const result = await listGoals(tmpDir);
    expect(result.projects).toEqual([]);
  });

  it('adds a project', async () => {
    await addGoal(tmpDir, {
      name: 'scrna-pipeline',
      status: 'active',
      workflows: ['scRNA-seq'],
      priority: 'high',
    });
    const result = await listGoals(tmpDir);
    expect(result.projects).toHaveLength(1);
    expect(result.projects[0].name).toBe('scrna-pipeline');
  });

  it('rejects duplicate project name', async () => {
    await addGoal(tmpDir, { name: 'my-project', status: 'active' });
    await expect(
      addGoal(tmpDir, { name: 'my-project', status: 'active' }),
    ).rejects.toThrow(/already exists/);
  });

  it('gets a project by name', async () => {
    await addGoal(tmpDir, { name: 'my-project', status: 'active', priority: 'medium' });
    const project = await getGoal(tmpDir, 'my-project');
    expect(project.name).toBe('my-project');
    expect(project.priority).toBe('medium');
  });

  it('updates a project', async () => {
    await addGoal(tmpDir, { name: 'my-project', status: 'active' });
    await updateGoal(tmpDir, 'my-project', { status: 'paused', notes: 'on hold' });
    const project = await getGoal(tmpDir, 'my-project');
    expect(project.status).toBe('paused');
    expect(project.notes).toBe('on hold');
  });

  it('removes a project', async () => {
    await addGoal(tmpDir, { name: 'my-project', status: 'active' });
    await removeGoal(tmpDir, 'my-project');
    const result = await listGoals(tmpDir);
    expect(result.projects).toEqual([]);
  });

  it('filters by status', async () => {
    await addGoal(tmpDir, { name: 'active-one', status: 'active' });
    await addGoal(tmpDir, { name: 'paused-one', status: 'paused' });
    const result = await listGoals(tmpDir, 'active');
    expect(result.projects).toHaveLength(1);
    expect(result.projects[0].name).toBe('active-one');
  });

  it('persists to disk', async () => {
    await addGoal(tmpDir, { name: 'persisted', status: 'active' });
    const raw = JSON.parse(
      await readFile(path.join(tmpDir, 'catalog', 'goals.json'), 'utf-8'),
    );
    expect(raw.projects).toHaveLength(1);
    expect(raw.projects[0].name).toBe('persisted');
  });
});
