// packages/catalog-mcp/__tests__/urls.test.ts
import { describe, it, expect } from 'vitest';
import { extractUrls } from '../src/core/urls.js';

const defaultPatterns = ['github.com/*', 'npmjs.com/package/*', 'pypi.org/project/*'];

describe('extractUrls', () => {
  it('extracts GitHub URLs from text', () => {
    const text = 'Check out https://github.com/org/cool-tool for this feature';
    const urls = extractUrls(text, defaultPatterns);
    expect(urls).toEqual(['https://github.com/org/cool-tool']);
  });

  it('extracts npm URLs', () => {
    const text = 'Install from https://www.npmjs.com/package/my-tool';
    const urls = extractUrls(text, defaultPatterns);
    expect(urls).toEqual(['https://www.npmjs.com/package/my-tool']);
  });

  it('extracts PyPI URLs', () => {
    const text = 'pip install from https://pypi.org/project/my-lib/';
    const urls = extractUrls(text, defaultPatterns);
    expect(urls).toEqual(['https://pypi.org/project/my-lib/']);
  });

  it('skips Reddit internal links', () => {
    const text = 'See https://www.reddit.com/r/claudeskills/comments/abc and https://github.com/org/tool';
    const urls = extractUrls(text, defaultPatterns);
    expect(urls).toEqual(['https://github.com/org/tool']);
  });

  it('skips image hosts', () => {
    const text = 'Image: https://i.redd.it/abc.png and https://imgur.com/gallery/xyz and https://github.com/org/tool';
    const urls = extractUrls(text, defaultPatterns);
    expect(urls).toEqual(['https://github.com/org/tool']);
  });

  it('deduplicates URLs', () => {
    const text = 'https://github.com/org/tool is great. I love https://github.com/org/tool';
    const urls = extractUrls(text, defaultPatterns);
    expect(urls).toEqual(['https://github.com/org/tool']);
  });

  it('supports extra patterns', () => {
    const text = 'Check https://crates.io/crates/my-crate';
    const urls = extractUrls(text, defaultPatterns, ['crates.io/crates/*']);
    expect(urls).toEqual(['https://crates.io/crates/my-crate']);
  });

  it('returns empty for text with no matching URLs', () => {
    const text = 'No URLs here, just some text';
    const urls = extractUrls(text, defaultPatterns);
    expect(urls).toEqual([]);
  });
});
