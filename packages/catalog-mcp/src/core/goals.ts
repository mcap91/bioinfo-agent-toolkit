// packages/catalog-mcp/src/core/goals.ts
import { readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { catalogPaths } from './config.js';
import { goalsSchema, projectSchema, type Project, type Goals } from './schema.js';

function goalsPath(dir: string): string {
  return path.join(dir, 'catalog', 'goals.json');
}

async function readGoals(dir: string): Promise<Goals> {
  try {
    const raw = await readFile(goalsPath(dir), 'utf-8');
    return goalsSchema.parse(JSON.parse(raw));
  } catch {
    return { projects: [] };
  }
}

async function writeGoals(dir: string, goals: Goals): Promise<void> {
  await writeFile(goalsPath(dir), JSON.stringify(goals, null, 2) + '\n', 'utf-8');
}

export async function listGoals(
  dir: string,
  status?: string,
): Promise<Goals> {
  const goals = await readGoals(dir);
  if (status) {
    return { projects: goals.projects.filter((p) => p.status === status) };
  }
  return goals;
}

export async function getGoal(dir: string, name: string): Promise<Project> {
  const goals = await readGoals(dir);
  const project = goals.projects.find((p) => p.name === name);
  if (!project) throw new Error(`Project "${name}" not found`);
  return project;
}

export async function addGoal(
  dir: string,
  project: Omit<Project, 'priority'> & { priority?: string },
): Promise<Project> {
  const goals = await readGoals(dir);
  if (goals.projects.some((p) => p.name === project.name)) {
    throw new Error(`Project "${project.name}" already exists`);
  }
  const parsed = projectSchema.parse(project);
  goals.projects.push(parsed);
  await writeGoals(dir, goals);
  return parsed;
}

export async function updateGoal(
  dir: string,
  name: string,
  updates: Partial<Omit<Project, 'name'>>,
): Promise<Project> {
  const goals = await readGoals(dir);
  const idx = goals.projects.findIndex((p) => p.name === name);
  if (idx === -1) throw new Error(`Project "${name}" not found`);
  const updated = projectSchema.parse({ ...goals.projects[idx], ...updates });
  goals.projects[idx] = updated;
  await writeGoals(dir, goals);
  return updated;
}

export async function removeGoal(dir: string, name: string): Promise<void> {
  const goals = await readGoals(dir);
  const idx = goals.projects.findIndex((p) => p.name === name);
  if (idx === -1) throw new Error(`Project "${name}" not found`);
  goals.projects.splice(idx, 1);
  await writeGoals(dir, goals);
}

export async function activeGoalsSummary(dir: string): Promise<string> {
  const goals = await listGoals(dir, 'active');
  if (goals.projects.length === 0) return '';
  const lines = ['## Active Projects', ''];
  for (const p of goals.projects) {
    const workflows = p.workflows?.length ? ` (${p.workflows.join(', ')})` : '';
    lines.push(`- **${p.name}**${workflows} — ${p.priority} priority`);
    if (p.notes) lines.push(`  ${p.notes}`);
  }
  return lines.join('\n');
}
