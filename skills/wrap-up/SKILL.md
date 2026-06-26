---
name: wrap-up
description: End-of-session housekeeping. Runs available checks (typecheck, wiki lint/generate), detects dual-repo setup, commits and pushes safely. Use when the user says "/wrap-up" or wants to wrap up a session.
---

# Wrap Up

End-of-session housekeeping. Adapts to what the repo has available.

## Steps

Execute these steps in order. Stop and report if a step marked **[abort on failure]** fails.

### 1. Typecheck **[abort on failure]**

Check if `package.json` exists **and** has a `typecheck` script.

- If yes: run `npm run typecheck`. If this fails, stop immediately — report the errors and do not continue.
- If no: skip. Print "Typecheck: n/a (no package.json or no typecheck script)".

### 2. Wiki operations

Check if `wiki/` exists and `kb` is available (look for `../kb/package.json`).

- If both exist: run wiki lint and generate from the kb directory, targeting this repo:
  ```
  cd ../kb && npm run wiki -- lint --dir <this-repo>
  cd ../kb && npm run wiki -- generate --dir <this-repo>
  ```
  Report any lint errors but do NOT abort — let the user decide whether to fix them.
- If wiki/ exists but kb is not found: skip. Print "Wiki: wiki/ exists but kb not found — skipping lint/generate".
- If wiki/ does not exist: skip silently.

### 3. Detect dual-repo setup

Check whether `wiki/.git` exists (i.e., `wiki/` is its own git repository, not just a subdirectory).

- If `wiki/.git` exists: this is a **dual-repo** setup. Steps 4 and 5 both apply.
- If `wiki/.git` does not exist: this is a **single-repo** setup. Only step 4 applies (wiki changes are part of the main repo).

**Safety check (dual-repo only):** Run `git check-ignore wiki/` in the main repo. If `wiki/` is NOT gitignored, **abort immediately** — the `.gitignore` is misconfigured and wiki files could be committed to the public repo.

### 4. Commit and push the main repo

- Run `git status` to check for changes (staged + unstaged + untracked).
- If there are no changes, print "Main repo: nothing to commit" and skip ahead.
- If there are changes:
  - Run `git diff` and `git diff --cached` to review.
  - Stage relevant files. Do NOT stage `.mcp.json`, `.env*`, `scratch_space/`, `.claude/`, or (in dual-repo mode) `wiki/`.
  - Auto-generate a commit message from the changed files, or ask the user if the changes are ambiguous.
  - **Do NOT include wiki record IDs** (`WK-*`, `IN-*`, `DEC-*`, `PLN-*`, `SRC-*`, `AREA-*`, `HO-*`) in commit messages for the main repo. These reference private wiki content. Describe the change itself, not the tracking item.
  - Create the commit. Do NOT amend. Do NOT force-push.
  - `git push`.

### 5. Commit and push wiki/ (dual-repo only)

Skip this step if `wiki/.git` does not exist.

- Run `git -C wiki status` to check for changes.
- If there are no changes, print "Wiki repo: nothing to commit" and skip ahead.
- If there are changes:
  - Run `git -C wiki diff` and `git -C wiki diff --cached` to review.
  - Stage relevant files inside `wiki/`.
  - Auto-generate a commit message from the changed files, or ask the user if the changes are ambiguous. Wiki record IDs are fine here — this is the private repo.
  - Create the commit inside `wiki/`. Do NOT amend. Do NOT force-push.
  - `git -C wiki push`.

### 6. Summary

Print a summary:

```
## Wrap-up summary

- **Typecheck**: passed / n/a
- **Wiki lint**: clean / N warnings / n/a
- **Wiki views**: regenerated / n/a
- **Main repo**: <committed and pushed / nothing to commit>
- **Wiki repo**: <committed and pushed / nothing to commit / n/a>
```

## Important

- Never force-push or amend commits.
- Never commit `.mcp.json`, `.env*`, `scratch_space/`, `.claude/`, or `wiki/` to the main repo (in dual-repo mode).
- In dual-repo mode, the main repo and wiki repo are independent git repositories. Do not mix their commits.
- In dual-repo mode, do not include wiki record IDs in main-repo commit messages.
- Before staging main-repo changes in dual-repo mode, verify `wiki/` is gitignored. Abort if not.
