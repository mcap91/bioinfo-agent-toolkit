// packages/catalog-mcp/__tests__/group-items.test.ts
import { describe, it, expect } from 'vitest';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { groupItems, linkKeys } from '../src/core/group-items.js';
import type { QueueItem } from '../src/core/schema.js';

// Real queue items (2026-10-29, from the WK-0092 parked set), unedited: two Instagram reels that
// both hint Docling, one GitHub item, and one reel with no hints.
const FIXTURE = path.join(path.dirname(fileURLToPath(import.meta.url)), 'fixtures', 'group-items', 'real-queue-items.json');
const load = async (): Promise<QueueItem[]> => JSON.parse(await readFile(FIXTURE, 'utf-8'));

describe('groupItems (real captured items)', () => {
  it('puts the two reels that both hint Docling in one group, so they never run in parallel and write two Docling entries', async () => {
    const items = await load();
    expect(linkKeys(items[0])).toContain('name:docling');
    expect(linkKeys(items[2])).toContain('name:docling');
    const groups = groupItems(items);
    expect(groups.map((g) => g.map((i) => i.key))).toEqual([
      [items[0].key, items[2].key],
      [items[1].key],
      [items[3].key],
    ]);
  });

  it('an item with no hints is linked only by its own URL', async () => {
    const items = await load();
    expect(linkKeys(items[3])).toEqual([`url:${items[3].url!.toLowerCase().replace(/^https?:\/\/(www\.)?/, '').replace(/\/+$/, '')}`]);
  });

  it('links a GitHub item to a reel that hints the same repo URL', () => {
    const repo: QueueItem = { key: 'https://github.com/Org/Tool', url: 'https://github.com/Org/Tool', source: 'manual', added: '2026-10-29T00:00:00Z' } as QueueItem;
    const reel: QueueItem = {
      key: 'https://www.instagram.com/reel/X/', url: 'https://www.instagram.com/reel/X/', source: 'manual', added: '2026-10-29T00:00:00Z',
      content: 'Caption:\nx\n\nMentioned (unverified hints):\n- The Tool (by Org): https://github.com/org/tool',
    } as QueueItem;
    expect(groupItems([repo, reel])).toHaveLength(1);
  });
});
