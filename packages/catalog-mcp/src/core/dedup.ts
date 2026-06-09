import { createHash } from 'node:crypto';

/** Normalize free-form content so whitespace variants hash identically. */
export function normalizeContent(s: string): string {
  return s.replace(/\r\n/g, '\n').replace(/\s+/g, ' ').trim();
}

/** 16-hex-char (64-bit) content hash. Collision space documented in the spec. */
export function contentHash(content: string): string {
  return createHash('sha256').update(normalizeContent(content)).digest('hex').slice(0, 16);
}

/** Stable dedup/queue key: the URL when present, else `content:<hash>`. */
export function dedupKey(item: { url?: string; content?: string }): string {
  if (item.url) return item.url;
  if (item.content) return `content:${contentHash(item.content)}`;
  throw new Error('dedupKey: item needs a url or content');
}
