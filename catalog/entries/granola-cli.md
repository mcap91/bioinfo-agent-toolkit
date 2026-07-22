---
name: granola-cli
title: Granola CLI
url: "https://github.com/theantichris/granola"
category: cli-tool
tags: [meeting-notes, export, backup, markdown, transcripts, granola, data-portability]
reviewed: 2026-07-21
summary: ">-"
acquired: 2026-07-22
---

## What it does

A Go CLI that exports data from the Granola meeting note-taking app to
local files for backup, migration, or offline access.

### Notes export (API-based)

Reads Supabase credentials from Granola's local config, authenticates
with the Granola API, fetches all documents as JSON, converts ProseMirror
JSON to Markdown, and writes files with YAML frontmatter (ID, timestamps,
tags).

### Transcripts export (cache-based)

Reads Granola's local cache file (double-JSON encoded), extracts transcript
segments by document ID, formats with timestamps and speaker labels
("System" for others, "You" for the user's microphone), and writes text
files with metadata headers.

### Features

- Incremental export — only processes new or changed content
- Cross-platform — macOS, Linux, Windows
- Configurable via `.granola.toml` or CLI flags
- Pre-built binaries for all platforms via GoReleaser
