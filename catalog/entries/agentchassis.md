---
name: agentchassis
title: "AgentChassis — multi-agent code-orchestration system with durable work-record contracts"
url: https://github.com/node-bio/portfolio-wiki-tools
category: framework
summary: "Splits agentic coding into orchestrator/worker/reviewer roles governed by durable work-record contracts. The agent that defines the work cannot implement it — every task carries scope, acceptance criteria, and validation before any code is written. Workers are kernel-confined to declared file scope via Linux bubblewrap. Git-committed dispatch state enables crash-resumable coordination, exact-slice review at frozen SHAs, deterministic squash candidates independent of main, and automatic forge handoff (PR creation). Supports Claude and Codex families; Agy fails closed. Source-available under Elastic License 2.0; optional hosted Chassis Control Engine (CCE) adds org-level admission and signed attestation."
tags:
  - multi-agent
  - orchestration
  - code-agent
  - work-records
  - sandbox
  - a2a
  - mcp
  - git-native
  - elv2
reviewed: 2026-07-29
acquired: 2026-07-29
supersedes: []
overlaps: []
---
## What it does

AgentChassis installs into your repository and enforces a separation-of-concerns rule: the agent that plans the work cannot implement it, and the agent that implements it cannot review it. Three non-overlapping roles — orchestrator (plans, never writes product code), worker (implements one scoped task, confined to declared files), and reviewer (checks the change against the task contract, read-only) — coordinate through durable **work-record contracts** committed to Git.

Every task is a work record stating scope, acceptance criteria, and validation commands before any code runs. A task missing these fields is rejected by a deterministic shape check — no model call needed. The work-record graph drives parallel dispatch: tasks declare which files they may touch, so non-overlapping workers run concurrently without collision.

The system publishes to npm as `@agent-chassis/core` (pulls the full `@agent-chassis/*` set). Requires Node.js 22+. Install with `npm install --save-dev @agent-chassis/core`, run `npx agent-chassis setup`, build the code index, and launch an orchestrator with `npx agent-launch orchestrator IN-0001 --model opus`.

## Differentiators

**Kernel-level file confinement.** Workers run inside Linux bubblewrap (`bwrap`) sandboxes. The repo is mounted read-only except the task's declared `write_scope`. Claude gets native tool-use permission gates (Edit only within scope); Codex gets exact-file kernel binds. `wiki/decisions/` is reimposed read-only as the final mount overlay — no worker can self-authorize a decision regardless of scope.

**Exact-slice review lifecycle.** Commit → freeze at exact SHA → reviewer bound to that SHA → auto-integrate into WK branch → terminal whole-WK findings review. The terminal candidate is a deterministic squash (`tree(C) === tree(W)`, sole parent is the fork-point `B`), independent of current `main`. Review never blocks on landing-branch movement.

**Crash-resumable dispatch.** All coordination state is Git-committed work records + launcher-private durable identity records. A stalled task carries its full definition; another agent or the operator picks it up without reconstructing context. Managed worker identity uses `(pid, starttime, boot_id)` tuples — no bare-pid liveness checks.

**Honest enforcement provenance.** Every run records `enforced=true/false` and `isolation_backend=bwrap|none` from the launcher (observer), never from the dispatched agent (subject). The system never claims containment it does not have. Unenforced runs are loud, not silent.

**Multi-family support.** Claude and Codex are supported implementation families with family-specific sandbox adapters. Agy is explicitly unsupported and fails closed before any model call.

**Forge handoff.** `workspace_wk_forge_handoff` publishes the exact terminal candidate and opens/recovers a PR via host-side `gh`. Credentials stay on the host; merge readiness stays with git/forge and human actors.

## Mechanical details

**Packages:** `@agent-chassis/wiki-core` (contract implementation), `@agent-chassis/wiki-mcp` (MCP server for agent tools), `@agent-chassis/wiki-cli` (human/CI CLI), `@agent-chassis/agent-launch-core` (launcher), `@agent-chassis/agent-launch-cli` (operator entrypoints), `@agent-chassis/core` (meta-package). Current version: 0.5.4.

**Agent interface:** MCP over stdio — spawned per-session, no hosted endpoint. Workers get closed-input commit delivery and scoped shell (`Bash`/`exec_command`); reviewers get full-repo read-only visibility. The launcher verifies exact role-derived tool lists after MCP `initialize` + `tools/list`.

**Operator commands:**
- `npx agent-launch orchestrator IN-0001 --model opus` — interactive, stays attached
- `npx agent-launch worker --app claude WK-1234#SLICE-001` — dispatch a confined worker
- `npx agent-launch review --app codex WK-1234` — findings-only reviewer
- `npx agent-launch redteam --app codex IN-0001` — initiative-scoped red team

**Wiki surfaces:** `wiki/work-records/` (canonical JSON), `wiki/issues/` (Markdown projections), `wiki/initiatives/`, `wiki/decisions/`, `wiki/sources/`, `wiki/areas/`. Generated views: `catalog.md`, `now.md`, `inbox.md`, `backlog.md`, `archive.md`.

## Security

**Threat model:** "Better than full privileges, not perfect." The system is correctness/provenance/honest-agent workflow machinery — not same-user security infrastructure. A malicious same-user actor or compromised host process can defeat every local mechanism; the baseline comparison is "agent with full host privileges and no tooling at all."

**What the sandbox buys:** writes confined to canonical `write_scope`; launcher secrets masked (`.env` → `/dev/null`, `.agent-launch/` → empty tmpfs); repo read-only except write scope; `wiki/decisions/` kernel-enforced read-only overlay.

**Known limits:** Worker network egress (`shareNet: true`) — required for hosted model APIs, no worse than baseline. No managed-worker command classifier — `Bash`/`exec_command` are available, bwrap is the boundary. Orchestrator sessions are operator-trusted and outside the enforcement envelope.

**License caution:** Elastic License 2.0 is source-available, not open-source. If implementing similar patterns, mirror designs; do not copy code. The hosted CCE tier is a paid control plane (private beta) — local/free use never requires it.

**decision_status: open** — Candidate the operator may implement a similar system for. kb compared itself to this upstream in kb WK-0045 (adopt backlog) and decided in kb DEC-0002 not to rebuild its own dispatch into this model for the solo-operator case. The operator is separately interested in a standalone multi-agent orchestration system.

**security_flags:** Linux-only bwrap sandbox (no macOS Seatbelt yet — on roadmap); hosted CCE is a paid control plane (private beta, requires form signup); worker network egress is shared (shareNet: true); ELv2 license prohibits providing it as a managed service.

**license_note:** Elastic License 2.0 — source-available, not OSI-approved open-source. Permits use, modification, and redistribution but prohibits providing the software as a managed service or circumventing license key functionality. If adopting patterns, design independently; do not copy implementation code.
