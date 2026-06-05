// packages/catalog-mcp/src/core/reddit.ts
import { extractUrls } from './urls.js';
import { loadConfig } from './config.js';

interface RedditCredentials {
  clientId: string;
  clientSecret: string;
  username: string;
}

interface RedditExtractOptions {
  dir: string;
  url?: string;
  subreddit?: string;
  sort?: 'hot' | 'new' | 'top';
  time?: 'hour' | 'day' | 'week' | 'month' | 'year' | 'all';
  limit?: number;
  extraPatterns?: string[];
}

interface ExtractedUrl {
  url: string;
  subreddit: string;
  post_title: string;
  author: string;
  score: number;
  comment_snippet?: string;
}

function getCredentials(): RedditCredentials {
  const clientId = process.env['REDDIT_CLIENT_ID'];
  const clientSecret = process.env['REDDIT_CLIENT_SECRET'];
  const username = process.env['REDDIT_USERNAME'];

  const missing: string[] = [];
  if (!clientId) missing.push('REDDIT_CLIENT_ID');
  if (!clientSecret) missing.push('REDDIT_CLIENT_SECRET');
  if (!username) missing.push('REDDIT_USERNAME');

  if (missing.length > 0) {
    throw new Error(
      `Missing env vars: ${missing.join(', ')}. ` +
      'Register a "script" app at https://www.reddit.com/prefs/apps. ' +
      'See catalog/config.env.example.',
    );
  }

  return { clientId: clientId!, clientSecret: clientSecret!, username: username! };
}

async function getAccessToken(creds: RedditCredentials): Promise<string> {
  const auth = Buffer.from(`${creds.clientId}:${creds.clientSecret}`).toString('base64');
  const response = await fetch('https://www.reddit.com/api/v1/access_token', {
    method: 'POST',
    headers: {
      Authorization: `Basic ${auth}`,
      'Content-Type': 'application/x-www-form-urlencoded',
      'User-Agent': `catalog-mcp/0.0.1 (by /u/${creds.username})`,
    },
    body: 'grant_type=client_credentials',
  });

  if (!response.ok) {
    throw new Error(`Reddit OAuth failed: ${response.status} ${response.statusText}`);
  }

  const data = (await response.json()) as { access_token: string };
  return data.access_token;
}

async function redditGet(
  path: string,
  token: string,
  username: string,
): Promise<unknown> {
  const response = await fetch(`https://oauth.reddit.com${path}`, {
    headers: {
      Authorization: `Bearer ${token}`,
      'User-Agent': `catalog-mcp/0.0.1 (by /u/${username})`,
    },
  });

  const remaining = response.headers.get('x-ratelimit-remaining');
  if (remaining && parseFloat(remaining) < 5) {
    const resetSec = parseFloat(response.headers.get('x-ratelimit-reset') || '60');
    await new Promise((r) => setTimeout(r, resetSec * 1000));
  }

  if (response.status === 429) {
    const resetSec = parseFloat(response.headers.get('x-ratelimit-reset') || '60');
    await new Promise((r) => setTimeout(r, resetSec * 1000));
    return redditGet(path, token, username);
  }

  if (!response.ok) {
    throw new Error(`Reddit API error: ${response.status} ${response.statusText}`);
  }

  return response.json();
}

export async function redditExtract(
  options: RedditExtractOptions,
): Promise<ExtractedUrl[]> {
  const creds = getCredentials();
  const token = await getAccessToken(creds);
  const config = await loadConfig(options.dir);
  const patterns = config.url_patterns;
  const extraPatterns = options.extraPatterns || [];
  const results: ExtractedUrl[] = [];
  const seen = new Set<string>();

  if (options.url) {
    // Single post mode
    const postId = extractPostId(options.url);
    if (!postId) throw new Error(`Cannot parse Reddit post URL: ${options.url}`);

    const data = (await redditGet(
      `/comments/${postId}?limit=500`,
      token,
      creds.username,
    )) as unknown[];

    const postListing = data[0] as { data: { children: Array<{ data: RedditPost }> } };
    const commentListing = data[1] as {
      data: { children: Array<{ data: RedditComment }> };
    };
    const post = postListing.data.children[0].data;

    // Extract from post body
    const postText = post.selftext || '';
    for (const url of extractUrls(postText, patterns, extraPatterns)) {
      if (!seen.has(url)) {
        seen.add(url);
        results.push({
          url,
          subreddit: post.subreddit,
          post_title: post.title,
          author: post.author,
          score: post.score,
        });
      }
    }

    // Extract from comments (top-level + 2 levels deep)
    processComments(commentListing.data.children, post, patterns, extraPatterns, seen, results, 0, 2);
  } else if (options.subreddit) {
    // Subreddit scan mode
    const sort = options.sort || 'hot';
    const limit = options.limit || 25;
    const timePart = sort === 'top' ? `&t=${options.time || 'week'}` : '';
    const data = (await redditGet(
      `/r/${options.subreddit}/${sort}?limit=${limit}${timePart}`,
      token,
      creds.username,
    )) as { data: { children: Array<{ data: RedditPost }> } };

    for (const child of data.data.children) {
      const post = child.data;
      const postText = `${post.title} ${post.selftext || ''} ${post.url || ''}`;
      for (const url of extractUrls(postText, patterns, extraPatterns)) {
        if (!seen.has(url)) {
          seen.add(url);
          results.push({
            url,
            subreddit: post.subreddit,
            post_title: post.title,
            author: post.author,
            score: post.score,
          });
        }
      }
    }
  } else {
    throw new Error('Either url or subreddit is required');
  }

  return results;
}

interface RedditPost {
  title: string;
  selftext: string;
  url: string;
  author: string;
  score: number;
  subreddit: string;
  id: string;
}

interface RedditComment {
  body?: string;
  author?: string;
  score?: number;
  replies?: { data: { children: Array<{ data: RedditComment }> } } | '';
}

function processComments(
  children: Array<{ data: RedditComment }>,
  post: RedditPost,
  patterns: string[],
  extraPatterns: string[],
  seen: Set<string>,
  results: ExtractedUrl[],
  depth: number,
  maxDepth: number,
): void {
  for (const child of children) {
    const comment = child.data;
    if (!comment.body) continue;

    for (const url of extractUrls(comment.body, patterns, extraPatterns)) {
      if (!seen.has(url)) {
        seen.add(url);
        results.push({
          url,
          subreddit: post.subreddit,
          post_title: post.title,
          author: comment.author || '[deleted]',
          score: comment.score || 0,
          comment_snippet: comment.body.slice(0, 200),
        });
      }
    }

    if (depth < maxDepth && comment.replies && typeof comment.replies === 'object') {
      processComments(
        comment.replies.data.children,
        post,
        patterns,
        extraPatterns,
        seen,
        results,
        depth + 1,
        maxDepth,
      );
    }
  }
}

function extractPostId(url: string): string | null {
  const match = url.match(/\/comments\/([a-z0-9]+)/);
  return match ? match[1] : null;
}
