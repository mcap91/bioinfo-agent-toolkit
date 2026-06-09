import { describe, it, expect } from 'vitest';
import { queueItemSchema, configSchema } from '../src/core/schema.js';

describe('queueItemSchema (phase 2)', () => {
  const base = { source: 'manual', added: '2026-06-08T00:00:00.000Z', key: 'k' };

  it('accepts a url-only item', () => {
    expect(queueItemSchema.safeParse({ ...base, url: 'https://x.com/a' }).success).toBe(true);
  });
  it('accepts a content-only item (no url)', () => {
    expect(queueItemSchema.safeParse({ ...base, content: 'free text' }).success).toBe(true);
  });
  it('rejects an item with neither url nor content', () => {
    expect(queueItemSchema.safeParse({ ...base }).success).toBe(false);
  });
  it('accepts status: parked', () => {
    expect(queueItemSchema.safeParse({ ...base, url: 'https://x.com/a', status: 'parked' }).success).toBe(true);
  });
});

describe('configSchema (phase 2)', () => {
  it('defaults blocked_domains/min_clean_chars/gmail_fallback', () => {
    const r = configSchema.parse({ url_patterns: [] });
    expect(r.blocked_domains).toEqual([]);
    expect(r.min_clean_chars).toBe(200);
    expect(r.gmail_fallback).toBe(true);
  });
});
