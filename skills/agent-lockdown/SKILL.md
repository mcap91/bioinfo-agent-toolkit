---
name: agent-lockdown
description: Lock down an interactive coding agent CLI — version pin, model pin, env hardening, secrets deny rules, model selector, and integrity checkup with injection detection. Modes — lockdown (default), checkup (integrity audit), upgrade-check (diff CLI versions).
---

# Agent lockdown

Lock an interactive coding agent CLI to a reproducible, hardened state. Four
layers: **harness version** (the CLI binary), **model** (exact slug),
**environment** (telemetry, feature flags, injection channels), and **session
permissions** (secrets deny rules).

Three modes: **lockdown** (default), **checkup**, and **upgrade-check** (pass
as arg).

Currently implements: **Claude Code**. The pattern is CLI-agnostic — version
freeze, model pin, env hardening, secrets deny, and a non-default model
selector apply to any coding agent CLI.

---

## Lockdown (default)

### Step 1 — Install the pinned CLI version

Tell the user to run this themselves (it requires global npm access):

```
npm install -g @anthropic-ai/claude-code@2.1.162
```

### Step 2 — Write user-level settings

Read `~/.claude/settings.json` (Windows: `C:\Users\<user>\.claude\settings.json`).
**Merge** the following keys into `env` and top-level — do not clobber existing
keys like `permissions`, `statusLine`, `enabledPlugins`, etc.

Required keys to merge:

```json
{
  "env": {
    "DISABLE_AUTOUPDATER": "1",
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1",
    "DISABLE_GROWTHBOOK": "1",
    "ANTHROPIC_CUSTOM_MODEL_OPTION": "claude-opus-4-6[1m]",
    "ANTHROPIC_CUSTOM_MODEL_OPTION_NAME": "Opus 4.6 (1M)",
    "ANTHROPIC_CUSTOM_MODEL_OPTION_DESCRIPTION": "Opus 4.6 with 1M context"
  },
  "model": "claude-opus-4-6[1m]"
}
```

### What each key does

**Version freeze:**

| Key | Purpose |
|-----|---------|
| `DISABLE_AUTOUPDATER` | Prevents the CLI from auto-updating past the pinned version — blocks supply-chain upgrades to compromised versions |

**Env hardening:**

| Key | Purpose |
|-----|---------|
| `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` | Blocks telemetry and bootstrap traffic |
| `DISABLE_GROWTHBOOK` | Blocks feature-flag injection from changing behavior between sessions |

**Model pin:**

| Key | Purpose |
|-----|---------|
| `model` | Pins the default model to Opus 4.6 with 1M context window |

**Model selector (keeps a non-default model accessible in the `/model` picker):**

| Key | Purpose |
|-----|---------|
| `ANTHROPIC_CUSTOM_MODEL_OPTION` | Full model slug for the custom picker entry |
| `ANTHROPIC_CUSTOM_MODEL_OPTION_NAME` | Display name shown in the picker |
| `ANTHROPIC_CUSTOM_MODEL_OPTION_DESCRIPTION` | Description shown in the picker |

### Traps to avoid

- The `ANTHROPIC_CUSTOM_MODEL_OPTION` trio is critical: without it, switching to
  Opus 4.8 via `/model` **evicts** the 4.6 option from the picker permanently
  (it was never a standard alias). With it, the custom entry persists
  independently of the `model` field and `/model` auto-save.
- Do **not** use `availableModels` to surface specific model versions — it
  filters by family alias only (`opus`/`sonnet`/`haiku`). Full model IDs
  silently collapse the picker to just "Default."
- Only **one** custom model option is supported (no comma-separated list).
- `env` keys are read at launch — a new terminal/session is required after
  changes.

### Step 3 — Project-level hardening

Apply these to the **project-level** `.claude/settings.json` (or
`.claude/settings.local.json` for machine-specific rules that shouldn't be
committed).

#### Secrets deny rules

Prevent the agent from reading secrets files, even if prompted or
prompt-injected to do so. Merge into `permissions.deny`:

```json
{
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)"
    ]
  }
}
```

Steering prompts alone ("do not read .env") are insufficient — the agent will
occasionally read or update these files anyway. The deny list is enforced by
the harness at the permission layer, not by the model. Use
`.claude/settings.local.json` if the deny paths are machine-specific and should
not be committed.

#### Subagent model override (optional)

Set Sonnet as the default subagent model to control cost:

```json
{
  "env": {
    "CLAUDE_CODE_SUBAGENT_MODEL": "sonnet"
  }
}
```

Pass `model: "opus"` on individual `Agent()` calls only when complex reasoning
is needed.

### Step 4 — Verify

Tell the user to open a **new terminal** (env vars are read at launch), then:

1. Check CLI version:
   ```
   claude --version
   ```
   Expected: `2.1.162`

2. Check model pin — open Claude Code and type `/model`. The picker should show:
   - **Default** (Opus 4.8 — the current tier default)
   - **Opus 4.6 (1M)** (the custom entry)

3. Check served model — verify the pinned model is still alive on the API.
   Read the OAuth token from `~/.claude/.credentials.json` (the
   `claudeAiOauth.accessToken` field) and run:
   ```bash
   curl -s -H "Authorization: Bearer <TOKEN>" \
        -H "anthropic-version: 2023-06-01" \
        https://api.anthropic.com/v1/models \
     | python3 -c "import sys,json; models=json.load(sys.stdin)['data']; print('ALIVE' if any(m['id']=='claude-opus-4-6' for m in models) else 'RETIRED')"
   ```
   If `RETIRED`: warn the user and follow the recovery procedure below.

### Recovery — if the pinned model is retired

If Anthropic retires `claude-opus-4-6`, Claude Code may fail to start or error
on API calls. Recovery:

1. Open `~/.claude/settings.json` in a text editor
2. Delete the `"model"` line (or set it to the current tier default, e.g.
   `"claude-opus-4-8[1m]"`)
3. The `/model` picker's **Default** entry always works — select it
4. Remove or update the three `ANTHROPIC_CUSTOM_MODEL_OPTION*` env vars

### Extending — additional protections

This skill is the single place to add new hardening as protections are
discovered (e.g. from catalog research, supply-chain advisories). To add:

1. **Env key:** add to the merge block in step 2, add a row to the table
2. **Deny rule:** add to the deny list in step 3
3. **Checkup coverage:** add to the expected-keys or known-safe lists in
   the checkup section below

---

## Checkup (pass "checkup" as arg)

Full integrity audit of the settings files. Two-sided diff: are the
**expected** keys correct, and is there anything **unexpected** that shouldn't
be there.

### Step 1 — Read the settings files

Read both files:
- **User-level:** `~/.claude/settings.json`
  (Windows: `C:\Users\<user>\.claude\settings.json`)
- **Project-level:** `.claude/settings.json` and `.claude/settings.local.json`
  (if they exist)

Parse the full JSON for each.

### Step 2 — Check expected keys (user-level)

Compare every pinned key against its expected value. Report each as OK, DRIFTED
(present but wrong value), or MISSING.

**Expected env keys:**

| Key | Expected value |
|-----|----------------|
| `DISABLE_AUTOUPDATER` | `"1"` |
| `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` | `"1"` |
| `DISABLE_GROWTHBOOK` | `"1"` |
| `ANTHROPIC_CUSTOM_MODEL_OPTION` | `"claude-opus-4-6[1m]"` |
| `ANTHROPIC_CUSTOM_MODEL_OPTION_NAME` | `"Opus 4.6 (1M)"` |
| `ANTHROPIC_CUSTOM_MODEL_OPTION_DESCRIPTION` | `"Opus 4.6 with 1M context"` |

**Expected top-level keys:**

| Key | Expected value |
|-----|----------------|
| `model` | `"claude-opus-4-6[1m]"` |

### Step 3 — Check project-level deny rules

Verify the project `.claude/settings.json` or `.claude/settings.local.json`
contains the secrets deny rules:

| Deny rule | Purpose |
|-----------|---------|
| `Read(./.env)` | Blocks reading the primary env file |
| `Read(./.env.*)` | Blocks reading env variants (.env.local, .env.production, etc.) |
| `Read(./secrets/**)` | Blocks reading anything under a secrets directory |

Report each as OK or MISSING. If the project has no `.claude/settings.json` or
no deny rules at all, report as MISSING and offer to create them.

### Step 4 — Check CLI version

Run `claude --version` and compare to `2.1.162`. Report OK or DRIFTED.

### Step 5 — Flag unexpected entries (user-level)

This is the injection and mutation detection pass. Categorize every key in the
user-level settings file.

**Critical — flag these with highest severity:**

- **`hooks.SessionStart`** — the primary persistence mechanism used by
  supply-chain attacks (e.g. Miasma/TeamPCP). A `SessionStart` hook you did
  not set is the single highest-risk mutation in this file. If found, **warn
  the user immediately** and recommend disconnecting from the network before
  investigating.
- **Unknown `env` vars** — an injected env var can redirect traffic, change
  model behavior, disable protections, or exfiltrate credentials.

**Known safe** — expected pins (step 2) plus these user-configured keys that
are normal to see:

- `env.CLAUDE_CODE_SUBAGENT_MODEL`
- `statusLine` (any value)
- `enabledPlugins` (any value)
- `effortLevel` (any value)
- `skipWorkflowUsageWarning` (any value)
- `theme` (any value)
- `permissions` (any structure)
- `hooks` (any key EXCEPT `SessionStart` — user-configured workflow hooks)
- `alwaysThinkingEnabled` (any value)

**Unexpected** — anything NOT in the expected or known-safe lists. For each:

- The full key path (e.g. `env.SOME_NEW_VAR`, `hooks.SessionStart`)
- Its current value
- Severity: CRITICAL for `hooks.SessionStart` and unknown env vars, WARNING for other keys

### Step 6 — Flag unexpected entries (project-level)

Repeat step 5 for the project-level settings. Additionally check
`.vscode/tasks.json` if it exists — look for tasks the user did not create,
especially anything with `runOn: folderOpen` (same persistence vector as
`SessionStart` hooks, used by the same attacks).

**Known safe** (project-level):

- `env.CLAUDE_CODE_SUBAGENT_MODEL`
- `permissions.allow` / `permissions.deny` (any entries)
- Any MCP-related permissions (e.g. `mcp__*`)
- `enabledMcpjsonServers` (any value)

### Step 7 — Report

Present to the user:

```
=== Agent Lockdown Checkup ===

CLI version:  2.1.162  ✓

--- User-level settings ---

Expected keys:
  model .......................... claude-opus-4-6[1m]  ✓
  DISABLE_AUTOUPDATER ........... 1                    ✓
  DISABLE_GROWTHBOOK ............ 1                    ✓
  ...

Unexpected keys:
  hooks.SessionStart ............ [command]  !! CRITICAL
  env.SOMETHING_NEW ............. "true"     !! CRITICAL
  newTopLevelKey ................. {...}      ⚠ WARNING

--- Project-level settings ---

Deny rules:
  Read(./.env) .................. ✓
  Read(./.env.*) ................ ✓
  Read(./secrets/**) ............ MISSING

.vscode/tasks.json:
  No unexpected tasks found.     ✓

No critical findings.  ✓   (or list them)
```

If anything is DRIFTED or MISSING, offer to re-apply (with user confirmation —
never silently fix). If unexpected but not critical, ask whether it's intentional.

If anything is CRITICAL, **stop and alert the user before any other action.**
Present this recovery order — the sequence matters:

1. **Do NOT rotate tokens or revoke credentials yet.** Known supply-chain
   malware (Miasma/TeamPCP) retaliates by wiping the home directory if it
   detects its access being cut while persistence is still active.
2. **Disconnect from the network** (pull cable / disable Wi-Fi).
3. **Screenshot the suspicious entries** for evidence.
4. **Remove the persistence** — delete the hook/task/env var from the file.
5. **Now rotate credentials** from a **different, trusted machine**: npm tokens,
   GitHub PATs, SSH keys, cloud credentials (AWS, GCP, Azure). Do not rotate
   from the potentially compromised machine.
6. Check `github.com/settings/security-log` for repos, runners, or publishes
   you did not create.

### Step 8 — Served model check

Run the served-model API check from the lockdown verify step (step 4.3) to
confirm the pinned model is still alive.

---

## Upgrade check (pass "upgrade-check" as arg)

Before upgrading the CLI, diff what changed between versions. Ask the user which
two versions to compare — default is `current` vs `latest`.

### Step 1 — Get version metadata

Run:

```bash
npm view @anthropic-ai/claude-code time --json
```

This returns publish timestamps for every version. Identify the two target
versions and all versions between them.

### Step 2 — Fetch the changelog

Fetch the raw changelog:

```
https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md
```

Extract the sections between the two target versions.

### Step 3 — Report

Present a summary highlighting:

- **Breaking changes** or behavioral shifts
- **Platform-specific** entries (Windows, Linux — ask the user's platform or
  check the OS)
- **Model or version-gate changes** (anything affecting pins —
  `requiredMinimumVersion`/`requiredMaximumVersion`, model slug changes, picker
  behavior)
- **Security fixes** worth taking
- Publish dates for both versions

End with a clear recommendation: **upgrade**, **hold**, or **wait** for a
specific fix. If upgrading, the user re-runs this skill in lockdown mode with
the new version — an upgrade is a deliberate re-pin, never a silent drift.
