# VS Code & Claude Code CLI Setup (Windows 11)

Setup and theme configuration for running Claude Code CLI inside VS Code on
Windows 11. This is a living document — adjust values as needed.

---

## Claude Code Custom Theme: `mcap91_dark`

Install to `~/.claude/themes/mcap91_dark.json`, then activate with `/theme` in
Claude Code.

Based on `dark-ansi` for better ANSI blue rendering on Windows. Overrides UI
chrome to grey tones, tunes diff and status colors for readability.

```json
{
  "name": "mcap91_dark",
  "base": "dark-ansi",
  "overrides": {
    "claude": "ansi:blackBright",
    "text": "ansi:whiteBright",
    "inactive": "ansi:blackBright",
    "subtle": "ansi:blackBright",
    "suggestion": "ansi:blackBright",
    "promptBorder": "ansi:blackBright",
    "selectionBg": "ansi:blackBright",
    "success": "#22c55e",
    "error": "#ef4444",
    "warning": "#eab308",
    "diffAdded": "#16a34a",
    "diffRemoved": "#dc2626",
    "diffAddedWord": "#22c55e",
    "diffRemovedWord": "#ef4444",
    "diffAddedDimmed": "#14532d",
    "diffRemovedDimmed": "#450a0a",
    "userMessageBackground": "#1c1c1c",
    "userMessageBackgroundHover": "#222222"
  }
}
```

### Available theme keys reference

| Category | Keys |
|---|---|
| UI | `claude`, `text`, `inactive`, `subtle`, `promptBorder`, `permission`, `suggestion`, `selectionBg` |
| Status | `success`, `error`, `warning` |
| Modes | `planMode`, `autoAccept`, `fastMode` |
| Diffs | `diffAdded`, `diffRemoved`, `diffAddedWord`, `diffRemovedWord`, `diffAddedDimmed`, `diffRemovedDimmed` |
| Messages | `userMessageBackground`, `userMessageBackgroundHover`, `bashMessageBackgroundColor`, `memoryBackgroundColor`, `messageActionsBackground` |
| Subagents | `{color}_FOR_SUBAGENTS_ONLY` where color is `red`, `blue`, `green`, `yellow`, `purple`, `orange`, `pink`, `cyan` |
| Usage | `rate_limit_fill`, `rate_limit_empty`, `briefLabelYou`, `briefLabelClaude` |

Color formats: `#rrggbb`, `rgb(r,g,b)`, `ansi256(n)`, `ansi:<name>` (e.g. `ansi:cyanBright`)

**Limitation:** File path link colors are hardcoded in the Claude Code extension
and cannot be overridden via themes.

---

## VS Code Settings

These settings complement the Claude Code theme. Add to
`%APPDATA%\Code\User\settings.json` under `workbench.colorCustomizations`.

### UI backgrounds and foreground

Dark backgrounds matched to `mcap91_dark`, with softened foreground text:

```json
"workbench.colorCustomizations": {
    "editor.background": "#111111",
    "sideBar.background": "#0e0e0e",
    "activityBar.background": "#0a0a0a",
    "titleBar.activeBackground": "#0a0a0a",
    "statusBar.background": "#0a0a0a",
    "tab.activeBackground": "#111111",
    "tab.inactiveBackground": "#0a0a0a",
    "terminal.background": "#161616",
    "panel.background": "#161616",
    "terminal.foreground": "#c0c0c0",
    "foreground": "#c0c0c0"
}
```

### Terminal environment (ANSI color support)

Force proper color capability detection for Windows terminals:

```json
"terminal.integrated.env.windows": {
    "TERM": "xterm-256color",
    "COLORTERM": "truecolor",
    "FORCE_COLOR": "3"
}
```

### Terminal rendering

```json
"terminal.integrated.gpuAcceleration": "off",
"terminal.integrated.windowsEnableConpty": true
```

---

## Troubleshooting: Dull/Desaturated Colors

If Claude Code colors appear faint or washed out in VS Code on Windows, this is
a known rendering issue. Claude Code renders in a **webview**, not a VS Code
terminal — most terminal-level color settings do not affect it.

### What does NOT fix Claude Code colors

| Setting | Why it doesn't work |
|---|---|
| `terminal.ansi*` in `workbench.colorCustomizations` | Claude Code is a webview, not a terminal |
| `textLink.foreground` | Does not reach the extension webview |
| `TERM` / `COLORTERM` / `FORCE_COLOR` env vars | Only affect terminal-based apps |
| Node version changes | No effect on webview rendering |
| `disable-hardware-acceleration` in `argv.json` | Made terminal background grey |
| `force-color-profile: "srgb"` in `argv.json` | No visible improvement |
| `code --disable-gpu` | Minor improvement to terminal, not Claude Code |
| VS Code theme change (Tokyo Night Storm, etc.) | No effect on Claude Code webview colors |
| `windowsEnableConpty` | No effect on Claude Code |
| UTF-8 encoding override in PowerShell | Made colors worse |

### What DOES help

| Fix | Effect |
|---|---|
| Claude Code `dark-ansi` theme (or custom theme based on it) | Better ANSI blue rendering |
| Claude Code custom theme overrides | Controls all UI colors except hardcoded link color |
| `panel.background` / `terminal.background` in VS Code | Controls the background behind Claude Code |
| `foreground` / `terminal.foreground` in VS Code | Controls default text brightness |
| `editor.background`, `sideBar.background`, etc. | Matches the full VS Code UI to the darker palette |
