# direct-output-style

A Claude Code [output style](https://code.claude.com/docs/en/output-styles.md) that merges the Output Register, Response Shape, and Coding Discipline rules into a single Markdown file. Activates via the `outputStyle` system — no bash installer, no hooks.

## Install

```bash
mkdir -p ~/.claude/output-styles
cp direct.md ~/.claude/output-styles/
```

Then activate one of two ways:

**Option A — settings.json:**
```json
{
  "outputStyle": "direct"
}
```

**Option B — in-session:**
```
/config → Output style → direct
```

## Clean up the old installation

If `setup-behavioral-baseline.sh` was previously installed, remove its components:

```bash
# Remove hook scripts
rm -f ~/.claude/fable-mode/reinject.sh ~/.claude/fable-mode/leak_test.py
rmdir ~/.claude/fable-mode 2>/dev/null || true

# Remove the hooks.UserPromptSubmit block from ~/.claude/settings.json
# (delete the "hooks" key or just its "UserPromptSubmit" entry)

# Remove the behavioral-baseline markers from ~/.claude/CLAUDE.md
# (delete the block between <!-- BEGIN behavioral-baseline --> and <!-- END behavioral-baseline -->)
```

The output style delivers the same rules through the system prompt (highest priority, never compressed away), so the re-injection hook is no longer needed.
