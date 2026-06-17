// packages/catalog-mcp/__tests__/schema.test.ts
import { describe, it, expect } from 'vitest';
import { entrySchema, CATEGORIES, DECISION_STATUSES } from '../src/core/schema.js';

describe('entrySchema', () => {
  const validEntry = {
    name: 'test-tool',
    title: 'Test Tool',
    url: 'https://github.com/org/test-tool',
    category: 'skill' as const,
    summary: 'looks promising',
    tags: ['testing'],
    reviewed: '2026-06-03',
  };

  it('accepts a valid entry with all required fields', () => {
    const result = entrySchema.safeParse(validEntry);
    expect(result.success).toBe(true);
  });

  it('accepts entry without url (reference material)', () => {
    const { url, ...noUrl } = validEntry;
    const result = entrySchema.safeParse(noUrl);
    expect(result.success).toBe(true);
  });

  it('accepts entry with optional fields', () => {
    const full = {
      ...validEntry,
      install: 'npm install test-tool',
      workflows: ['scRNA-seq'],
      acquired: '2026-06-01',
      license: 'MIT',
      security_flags: ['no-tests'],
      supersedes: ['old-tool'],
      overlaps: ['similar-tool'],
    };
    const result = entrySchema.safeParse(full);
    expect(result.success).toBe(true);
  });

  it('rejects entry missing required name', () => {
    const { name, ...noName } = validEntry;
    const result = entrySchema.safeParse(noName);
    expect(result.success).toBe(false);
  });

  it('rejects invalid category', () => {
    const result = entrySchema.safeParse({ ...validEntry, category: 'banana' });
    expect(result.success).toBe(false);
  });

  it('does not include a status field (removed in v2.1.0)', () => {
    const result = entrySchema.safeParse(validEntry);
    expect(result.success).toBe(true);
    if (result.success) {
      expect('status' in result.data).toBe(false);
    }
    // .strict() also rejects a stray status key
    expect(entrySchema.safeParse({ ...validEntry, status: 'approved' }).success).toBe(false);
  });
});

describe('entrySchema decision_status migration', () => {
  const base = {
    name: 'foo-bar',
    title: 'Foo Bar',
    category: 'skill',
    summary: 'one-line take',
    tags: ['x'],
    reviewed: '2026-06-16',
  };

  it('accepts an entry with no decision_status (open)', () => {
    expect(entrySchema.safeParse(base).success).toBe(true);
  });
  it('accepts decision_status adopted/rejected', () => {
    for (const s of DECISION_STATUSES) {
      expect(entrySchema.safeParse({ ...base, decision_status: s }).success).toBe(true);
    }
  });
  it('rejects the retired verdict field via .strict()', () => {
    expect(entrySchema.safeParse({ ...base, verdict: 'adopt' }).success).toBe(false);
  });
  it('rejects the retired verdict_reason field', () => {
    expect(entrySchema.safeParse({ ...base, verdict_reason: 'x' }).success).toBe(false);
  });
  it('requires summary', () => {
    const { summary, ...noSummary } = base;
    expect(entrySchema.safeParse(noSummary).success).toBe(false);
  });
});
