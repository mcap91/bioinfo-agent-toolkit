// packages/catalog-mcp/src/core/fetch-url.ts
import { lookup } from 'node:dns/promises';
import { parseHTML } from 'linkedom';
import { Readability } from '@mozilla/readability';

export interface ExtractResult {
  text: string;
  title: string;
  belowThreshold: boolean;
}

/** HTML → main article text via Readability over a lightweight DOM. */
export function extractReadable(html: string, minChars: number): ExtractResult {
  let text = '';
  let title = '';
  try {
    const { document } = parseHTML(html);
    const article = new Readability(document as unknown as Document).parse();
    text = (article?.textContent || '').replace(/\n{3,}/g, '\n\n').trim();
    title = article?.title || '';
  } catch {
    text = '';
  }
  if (!title) {
    const m = html.match(/<title[^>]*>(.*?)<\/title>/is);
    title = m ? m[1].trim() : '';
  }
  return { text, title, belowThreshold: text.length < minChars };
}

/** Pick the content to return and the park signal, consistently.
 * belowThreshold reflects the RETURNED content, not only the Readability result,
 * so the signal and payload always agree. */
export function resolveCleanContent(
  extracted: ExtractResult,
  raw: string,
  minChars: number,
): { content: string; belowThreshold: boolean } {
  const content = extracted.text || raw;
  return { content, belowThreshold: content.length < minChars };
}

const ALLOWED_SCHEMES = new Set(['http:', 'https:']);

const BLOCKED_HOSTS = new Set([
  'localhost',
  '0.0.0.0',
  '[::1]',
  'metadata.google.internal',
]);

interface FetchResult {
  content: string;
  title: string;
  metadata: Record<string, unknown>;
}

export function validateUrl(urlStr: string): URL {
  let parsed: URL;
  try {
    parsed = new URL(urlStr);
  } catch {
    throw new Error(`Invalid URL: ${urlStr}`);
  }

  if (!ALLOWED_SCHEMES.has(parsed.protocol)) {
    throw new Error(`Blocked scheme "${parsed.protocol}" — only http and https allowed`);
  }

  if (BLOCKED_HOSTS.has(parsed.hostname)) {
    throw new Error(`blocked host "${parsed.hostname}" — private/reserved address`);
  }

  if (isBlockedIp(parsed.hostname)) {
    throw new Error(`blocked host "${parsed.hostname}" — private/reserved IP range`);
  }

  return parsed;
}

function isBlockedIp(host: string): boolean {
  // Strip brackets from IPv6 addresses (e.g. "[::1]" -> "::1")
  const h = host.startsWith('[') && host.endsWith(']') ? host.slice(1, -1) : host;
  const lc = h.toLowerCase();

  // IPv4
  const ipv4Match = h.match(/^(\d+)\.(\d+)\.(\d+)\.(\d+)$/);
  if (ipv4Match) {
    const [, a, b] = ipv4Match.map(Number);
    if (a === 0) return true;                        // 0.0.0.0/8
    if (a === 10) return true;                       // 10.0.0.0/8
    if (a === 127) return true;                      // 127.0.0.0/8
    if (a === 169 && b === 254) return true;         // 169.254.0.0/16
    if (a === 172 && b >= 16 && b <= 31) return true; // 172.16.0.0/12
    if (a === 192 && b === 168) return true;         // 192.168.0.0/16
  }

  // IPv6 loopback
  if (lc === '::1') return true;

  // IPv4-mapped IPv6: ::ffff:w.x.y.z  or  ::ffff:hex:hex
  if (lc.startsWith('::ffff:')) {
    const rest = lc.slice(7);
    // dotted decimal form: ::ffff:127.0.0.1
    if (/^\d+\.\d+\.\d+\.\d+$/.test(rest)) return isBlockedIp(rest);
    // hex form from Node URL parser: ::ffff:7f00:1 -> convert to dotted
    const hexMatch = rest.match(/^([0-9a-f]+):([0-9a-f]+)$/);
    if (hexMatch) {
      const high = parseInt(hexMatch[1], 16);
      const low = parseInt(hexMatch[2], 16);
      const a = (high >> 8) & 0xff;
      const b = high & 0xff;
      const c = (low >> 8) & 0xff;
      const d = low & 0xff;
      return isBlockedIp(`${a}.${b}.${c}.${d}`);
    }
    return true; // block all IPv4-mapped IPv6 as a safe default
  }

  // IPv6 unique local addresses (fc00::/7 = fc00:: through fdff::).
  // Guard on ':' so this only matches IPv6 literals — otherwise it would
  // false-block ordinary domains that happen to start with "fc"/"fd"
  // (e.g. fdroid.org, fc2.com). All IPv6 addresses contain a colon.
  if (lc.includes(':') && (lc.startsWith('fc') || lc.startsWith('fd'))) return true;

  return false;
}

async function validateResolvedIp(hostname: string): Promise<void> {
  try {
    const { address } = await lookup(hostname);
    if (isBlockedIp(address)) {
      throw new Error(
        `DNS resolved "${hostname}" to blocked IP ${address} — possible DNS rebinding`,
      );
    }
  } catch (err) {
    if ((err as Error).message.includes('blocked')) throw err;
    // DNS resolution failed — let fetch handle it
  }
}

const MAX_REDIRECTS = 5;
const TIMEOUT_MS = 30_000;
const MAX_BODY_BYTES = 5 * 1024 * 1024;

export async function fetchUrl(
  urlStr: string,
  opts: { clean?: boolean; minChars?: number } = {},
): Promise<FetchResult & { belowThreshold?: boolean }> {
  const parsed = validateUrl(urlStr);
  await validateResolvedIp(parsed.hostname);

  let currentUrl = urlStr;
  let redirectCount = 0;

  while (redirectCount < MAX_REDIRECTS) {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), TIMEOUT_MS);

    try {
      const response = await fetch(currentUrl, {
        signal: controller.signal,
        redirect: 'manual',
        headers: {
          'User-Agent': 'catalog-mcp/0.0.1 (tool catalog intake)',
        },
      });

      if (response.status >= 300 && response.status < 400) {
        const location = response.headers.get('location');
        if (!location) throw new Error('Redirect with no Location header');
        const nextUrl = new URL(location, currentUrl);
        validateUrl(nextUrl.href);
        await validateResolvedIp(nextUrl.hostname);
        currentUrl = nextUrl.href;
        redirectCount++;
        continue;
      }

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const contentLength = response.headers.get('content-length');
      if (contentLength && parseInt(contentLength) > MAX_BODY_BYTES) {
        throw new Error(`Response too large: ${contentLength} bytes (max ${MAX_BODY_BYTES})`);
      }

      const text = await response.text();
      if (text.length > MAX_BODY_BYTES) {
        throw new Error(`Response body too large (max ${MAX_BODY_BYTES} bytes)`);
      }

      const title = extractTitle(text) || parsed.pathname.split('/').pop() || '';
      const metadata = {
        url: currentUrl,
        contentType: response.headers.get('content-type'),
        status: response.status,
      };
      if (opts.clean === false) {
        return { content: text, title, metadata };
      }
      const extracted = extractReadable(text, opts.minChars ?? 200);
      const { content, belowThreshold } = resolveCleanContent(extracted, text, opts.minChars ?? 200);
      return { content, title: extracted.title || title, metadata, belowThreshold };
    } finally {
      clearTimeout(timeout);
    }
  }

  throw new Error(`Too many redirects (max ${MAX_REDIRECTS})`);
}

function extractTitle(html: string): string | null {
  const match = html.match(/<title[^>]*>(.*?)<\/title>/is);
  return match ? match[1].trim() : null;
}
