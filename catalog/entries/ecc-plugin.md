---
name: ecc-plugin
title: "Everything Claude Code (ECC)"
url: https://www.claudepluginhub.com/plugins/affaan-m-everything-claude-code
category: plugin
verdict: watch
verdict_reason: "rate-limited (429 errors); trial when accessible"
install: "npx claudepluginhub affaan-m/ecc --plugin ecc"
tags: [plugin, hub, all-in-one]
reviewed: 2026-05-25
supersedes: []
---

## What it does

An all-in-one plugin package distributed through the Claude Plugin Hub. Bundles multiple capabilities into a single install command. Encountered 429 rate limit errors across three attempts in two separate sessions during the review period, preventing content verification.

## Why this verdict

Cannot fully evaluate without access. The bundled approach may introduce conflicts with the existing superpowers stack similar to the concerns with claude-spellbook. Rate limiting suggests high demand but also infrastructure instability. Low priority — trial when the plugin hub rate limit clears and the content can be verified.

## Mechanical details

Install: `npx claudepluginhub affaan-m/ecc --plugin ecc`. If the rate limit has cleared, trial in an isolated project before adding to the main stack. Evaluate for overlap with superpowers and existing skills before enabling broadly.
