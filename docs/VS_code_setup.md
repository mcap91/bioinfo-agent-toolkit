# VS Code & Claude Code CLI Setup (Windows 11)

Setup and theme configuration for running Claude Code CLI inside VS Code on
Windows 11. Theme v2 — Dark 2026 (default) with minimal overrides.

---

## Theme

**VS Code:** Dark 2026 (default) — the built-in dark theme, no extension needed.

**Claude Code:** stock `dark` theme (set via `/theme` in Claude Code).

Claude Code renders in a webview, not a VS Code terminal. The VS Code theme
controls the editor, sidebar, tabs, and terminal. Claude Code text colors are
controlled entirely by its own theme system. The only crossover is
`panel.background`, which sets the container behind the Claude Code panel.

---

## VS Code Settings

Portable settings for `%APPDATA%\Code\User\settings.json`. Excludes
machine-specific entries like `remote.SSH.remotePlatform`.

### Editor preferences

```json
"git.autofetch": true,
"editor.minimap.enabled": false,
"workbench.startupEditor": "none",
"explorer.confirmDragAndDrop": false
```

### Terminal configuration

```json
"terminal.integrated.profiles.windows": {
    "PowerShell": {
        "source": "PowerShell",
        "icon": "terminal-powershell"
    },
    "Command Prompt": {
        "path": [
            "${env:windir}\\Sysnative\\cmd.exe",
            "${env:windir}\\System32\\cmd.exe"
        ],
        "args": [],
        "icon": "terminal-cmd"
    },
    "Git Bash": {
        "source": "Git Bash"
    },
    "Ubuntu (WSL)": {
        "path": "C:\\Windows\\System32\\wsl.exe",
        "args": ["-d", "Ubuntu"]
    }
},
"terminal.integrated.scrollback": 800,
"terminal.integrated.fontSize": 14,
"terminal.integrated.initialHint": false,
"terminal.integrated.gpuAcceleration": "off",
"terminal.integrated.windowsEnableConpty": true
```

### Terminal environment (ANSI color support)

```json
"terminal.integrated.env.windows": {
    "TERM": "xterm-256color",
    "COLORTERM": "truecolor",
    "FORCE_COLOR": "3"
}
```

### UI color overrides

Minimal overrides on top of Dark 2026 — brighter explorer text, darker
terminal/sidebar, and a distinct active tab:

```json
"workbench.colorCustomizations": {
    "sideBar.foreground": "#e0e0e0",
    "sideBar.background": "#111315",
    "tab.activeForeground": "#f0f0f0",
    "tab.activeBackground": "#1e2025",
    "terminal.background": "#111315",
    "panel.background": "#111315"
}
```

---

## Keybindings

Custom keybindings for `%APPDATA%\Code\User\keybindings.json`:

```json
[
    {
        "key": "ctrl+r",
        "command": "workbench.action.reloadWindow"
    },
    {
        "key": "shift+enter",
        "command": "workbench.action.terminal.sendSequence",
        "args": { "text": "\r" },
        "when": "terminalFocus"
    }
]
```

---

## Extensions

Install all with:

```bash
code --install-extension anthropic.claude-code
code --install-extension google.gemini-cli-vscode-ide-companion
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension ms-python.vscode-python-envs
code --install-extension ms-python.debugpy
code --install-extension reditorsupport.r
code --install-extension reditorsupport.r-syntax
code --install-extension rdebugger.r-debugger
code --install-extension ikuyadeu.r-pack
code --install-extension ms-vscode-remote.remote-ssh
code --install-extension ms-vscode-remote.remote-ssh-edit
code --install-extension ms-vscode.remote-explorer
code --install-extension ms-vscode.remote-repositories
code --install-extension github.remotehub
code --install-extension github.codespaces
code --install-extension ms-vscode.azure-repos
code --install-extension mechatroner.rainbow-csv
code --install-extension repreng.csv
code --install-extension ms-toolsai.jupyter-keymap
code --install-extension foam.foam-vscode
code --install-extension ms-vscode.live-server
code --install-extension ms-vscode.powershell
code --install-extension tomoki1207.pdf
```
