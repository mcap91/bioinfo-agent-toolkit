---
name: skills-cli
title: Skills CLI (skills.sh)
url: "https://github.com/vercel-labs/skills"
category: cli-tool
tags: [skills, package-manager, discovery, CLI, agent-skills, vercel]
reviewed: 2026-07-03
security_flags: []
summary: ">-"
acquired: 2026-07-04
---

## What It Does

The Skills CLI (`npx skills`) is a package manager for agent skills — modular SKILL.md
packages that extend AI coding agent capabilities with specialized knowledge, workflows,
and tools. It provides discovery, installation, update checking, and scaffolding for new
skills.

## Key Commands

- `npx skills find [query] [--owner <owner>]` — search for skills by keyword
- `npx skills add <owner/repo@skill>` — install a skill from GitHub
- `npx skills add <package> -g -y` — install globally, skip confirmation
- `npx skills check` — check for updates
- `npx skills update` — update all installed skills
- `npx skills init <name>` — scaffold a new skill
- `npx skills list` — list installed skills

## Registry (skills.sh)

The skills.sh leaderboard ranks skills by total installs. Quality verification uses
install count (prefer 1K+), source reputation (vercel-labs, anthropics, microsoft are
trusted), and GitHub stars. Top sources include vercel-labs/agent-skills and
anthropics/skills (100K+ installs each).

## find-skills Meta-Skill

The repository includes a `find-skills` skill that teaches agents how to discover and
recommend skills to users — it handles leaderboard lookup, CLI search, quality
verification, and installation within conversation flow.

## Links

- GitHub: https://github.com/vercel-labs/skills
- Registry: https://skills.sh/
- find-skills: https://www.skills.sh/vercel-labs/skills/find-skills