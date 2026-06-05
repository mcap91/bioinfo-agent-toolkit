// packages/catalog-mcp/src/core/urls.ts

const SKIP_HOSTS = new Set([
  'reddit.com',
  'www.reddit.com',
  'old.reddit.com',
  'i.redd.it',
  'v.redd.it',
  'preview.redd.it',
  'imgur.com',
  'i.imgur.com',
  'gfycat.com',
  'streamable.com',
  'youtu.be',
  'youtube.com',
  'www.youtube.com',
]);

const URL_REGEX = /https?:\/\/[^\s<>\[\](),"'`]+/g;

export function extractUrls(
  text: string,
  patterns: string[],
  extraPatterns?: string[],
): string[] {
  const allPatterns = [...patterns, ...(extraPatterns || [])];
  const matchers = allPatterns.map(patternToRegex);
  const seen = new Set<string>();
  const results: string[] = [];

  const rawUrls = text.match(URL_REGEX) || [];

  for (let raw of rawUrls) {
    // Strip trailing punctuation that's not part of the URL
    raw = raw.replace(/[.),:;!?]+$/, '');

    let parsed: URL;
    try {
      parsed = new URL(raw);
    } catch {
      continue;
    }

    const host = parsed.hostname.replace(/^www\./, '');
    if (SKIP_HOSTS.has(parsed.hostname) || SKIP_HOSTS.has(host)) continue;

    const hostPath = host + parsed.pathname;
    if (!matchers.some((m) => m.test(hostPath))) continue;

    if (seen.has(raw)) continue;
    seen.add(raw);
    results.push(raw);
  }

  return results;
}

function patternToRegex(pattern: string): RegExp {
  const escaped = pattern
    .replace(/[.+?^${}()|[\]\\]/g, '\\$&')
    .replace(/\*/g, '.*');
  return new RegExp('^' + escaped);
}
