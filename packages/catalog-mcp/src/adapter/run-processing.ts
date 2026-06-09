// packages/catalog-mcp/src/adapter/run-processing.ts
// Headless one-shot: run the catalog processing recipe under `claude -p`, with the
// catalog MCP server attached in force-draft mode so no entry can reach `approved`.
//
// VERIFIED against `claude 2.1.162 (Claude Code)` on 2026-06-09:
//   --print                    non-interactive mode
//   --mcp-config <file>        attach MCP servers from a JSON file (flag is variadic:
//                              `--mcp-config <configs...>`)
//   --allowedTools <tools...>  scoped tool allowlist (variadic); in --print mode the run
//                              cannot answer permission prompts, so the tools the recipe
//                              needs must be pre-authorized here.
//   prompt via STDIN           because --mcp-config and --allowedTools are variadic, a
//                              positional prompt would be swallowed as another value —
//                              pipe the recipe to stdin instead.
// Re-verify with `claude --help` and bump this pin if the CLI is upgraded.
import { spawn } from 'node:child_process';
import { readFile, writeFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

// Scoped allowlist: only the catalog MCP tools the recipe calls plus the agent's own web
// search/fetch. The catalog server runs force-draft, so even these cannot emit `approved`.
const ALLOWED_TOOLS = [
  'mcp__catalog__queue',
  'mcp__catalog__fetch-url',
  'mcp__catalog__build-prompt',
  'mcp__catalog__validate-entry',
  'mcp__catalog__write-entry',
  'mcp__catalog__index',
  'WebSearch',
  'WebFetch',
];

function repoRoot(): string {
  let dir = path.dirname(fileURLToPath(import.meta.url));
  for (let i = 0; i < 10; i++) {
    if (existsSync(path.join(dir, 'catalog'))) return dir;
    const parent = path.dirname(dir);
    if (parent === dir) break;
    dir = parent;
  }
  throw new Error('repo root not found');
}

async function main(): Promise<void> {
  const root = repoRoot();
  const recipe = await readFile(path.join(root, 'catalog', 'recipe.md'), 'utf-8');

  // MCP config attaching the catalog server (stdio) with the force-draft guarantee in env.
  const mcpConfig = JSON.stringify({
    mcpServers: {
      catalog: {
        command: 'npx',
        args: ['tsx', path.join(root, 'packages', 'catalog-mcp', 'src', 'server.ts')],
        env: { CATALOG_FORCE_DRAFT: '1', CATALOG_ROOT: root },
      },
    },
  });
  const mcpConfigPath = path.join(root, '.catalog-mcp.run.json');
  await writeFile(mcpConfigPath, mcpConfig, 'utf-8');

  // --mcp-config <file> then --allowedTools (both variadic); the recipe is piped via stdin.
  const args = [
    '--print',
    '--mcp-config', mcpConfigPath,
    '--allowedTools', ...ALLOWED_TOOLS,
  ];
  const child = spawn('claude', args, {
    cwd: root,
    stdio: ['pipe', 'inherit', 'inherit'],
    env: { ...process.env, CATALOG_FORCE_DRAFT: '1', CATALOG_ROOT: root },
  });
  child.stdin?.write(recipe);
  child.stdin?.end();
  child.on('exit', (code) => process.exit(code ?? 1));
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
