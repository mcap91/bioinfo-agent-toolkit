// packages/catalog-mcp/src/core/group-items.ts
import type { QueueItem } from './schema.js';

// Header the Instagram capture writes before its hint list (catalog_capture/instagram_rewrite.py,
// render_instagram_block): one `- <name>: <url or "(no url)">` line per tool the read spotted.
const HINTS_HEADER = 'Mentioned (unverified hints):\n';
const HINT_LINE = /^- (.+): (\(no url\)|\S+)$/;
const GITHUB_REPO = /github\.com\/([^/\s#?]+)\/([^/\s#?]+)/i;

function normName(name: string): string {
  return name.replace(/\([^)]*\)/g, '').toLowerCase().replace(/[^a-z0-9]+/g, '');
}

function normUrl(url: string): string {
  return url.toLowerCase().replace(/^https?:\/\//, '').replace(/^www\./, '').replace(/[/#?]+$/, '');
}

/** The keys that tie an item to a tool: its own URL, each hinted tool name and URL, and any
 * GitHub repo among them. Two items sharing any key may write or annotate the same entry. */
export function linkKeys(item: QueueItem): string[] {
  const keys = new Set<string>();
  const addUrl = (url: string) => {
    keys.add(`url:${normUrl(url)}`);
    const gh = url.match(GITHUB_REPO);
    if (gh) keys.add(`gh:${gh[1].toLowerCase()}/${gh[2].toLowerCase().replace(/\.git$/, '')}`);
  };
  if (item.url) addUrl(item.url);

  const content = item.content ?? '';
  const at = content.indexOf(HINTS_HEADER);
  if (at !== -1) {
    for (const line of content.slice(at + HINTS_HEADER.length).split('\n')) {
      const m = line.match(HINT_LINE);
      if (!m) continue;
      const name = normName(m[1]);
      if (name.length > 2) keys.add(`name:${name}`);
      if (m[2] !== '(no url)') addUrl(m[2]);
    }
  }
  return [...keys];
}

/** Split items into groups that share no link key (union-find over `linkKeys`). Groups are
 * ordered by their first item's queue position; items inside a group keep queue order. Run each
 * group in one session slot, one item after another, so two items about the same tool never run
 * at once — the second one's `search` sees the first one's entry. Hints are unverified and
 * unhinted items get only their URL, so this lowers the duplicate risk; it does not remove it. */
export function groupItems(items: QueueItem[]): QueueItem[][] {
  const parent = items.map((_, i) => i);
  const find = (x: number): number => (parent[x] === x ? x : (parent[x] = find(parent[x])));
  const owner = new Map<string, number>();
  items.forEach((item, i) => {
    for (const key of linkKeys(item)) {
      const j = owner.get(key);
      if (j === undefined) owner.set(key, i);
      else parent[find(i)] = find(j);
    }
  });

  const groups = new Map<number, QueueItem[]>();
  items.forEach((item, i) => {
    const root = find(i);
    const group = groups.get(root);
    if (group) group.push(item);
    else groups.set(root, [item]);
  });
  // Map insertion order is first-item order, because items are visited in queue order.
  return [...groups.values()];
}
