// packages/catalog-mcp/__tests__/validate-entry.test.ts
import { describe, it, expect } from 'vitest';
import { validateEntry } from '../src/core/validate-entry.js';

const validMarkdown = `---
name: test-tool
title: "Test Tool"
url: https://github.com/org/test-tool
category: skill
verdict: pilot
verdict_reason: "looks promising"
tags: [testing]
reviewed: 2026-06-03
acquired: 2026-06-03
---

## What it does

A test tool.

## Why this verdict

It looks good.

## Mechanical details

Install with npm.

## Security

MIT license. No flags.
`;

describe('validateEntry', () => {
  it('accepts valid entry', () => {
    const result = validateEntry(validMarkdown);
    expect(result.valid).toBe(true);
    expect(result.errors).toEqual([]);
  });

  it('rejects entry with no frontmatter', () => {
    const result = validateEntry('Just some text');
    expect(result.valid).toBe(false);
    expect(result.errors.length).toBeGreaterThan(0);
  });

  it('rejects entry with invalid verdict', () => {
    const bad = validMarkdown.replace('verdict: pilot', 'verdict: maybe');
    const result = validateEntry(bad);
    expect(result.valid).toBe(false);
  });

  it('warns on missing acquired for existing entries', () => {
    const noAcquired = validMarkdown.replace('acquired: 2026-06-03\n', '');
    const result = validateEntry(noAcquired);
    expect(result.valid).toBe(true);
    expect(result.warnings.some((w) => w.includes('acquired'))).toBe(true);
  });

  it('warns on missing Security section', () => {
    const noSecurity = validMarkdown.replace('## Security\n\nMIT license. No flags.\n', '');
    const result = validateEntry(noSecurity);
    expect(result.valid).toBe(true);
    expect(result.warnings.some((w) => w.includes('Security'))).toBe(true);
  });
});
