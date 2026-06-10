// packages/catalog-mcp/__tests__/schema.test.ts
import { describe, it, expect } from 'vitest';
import { entrySchema, CATEGORIES, VERDICTS } from '../src/core/schema.js';

describe('entrySchema', () => {
  const validEntry = {
    name: 'test-tool',
    title: 'Test Tool',
    url: 'https://github.com/org/test-tool',
    category: 'skill' as const,
    verdict: 'pilot' as const,
    verdict_reason: 'looks promising',
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

  it('rejects invalid verdict', () => {
    const result = entrySchema.safeParse({ ...validEntry, verdict: 'maybe' });
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
  });

  it('ignores a stray legacy status key (zod strips unknown keys)', () => {
    const result = entrySchema.safeParse({ ...validEntry, status: 'approved' });
    expect(result.success).toBe(true);
    if (result.success) {
      expect('status' in result.data).toBe(false);
    }
  });
});
