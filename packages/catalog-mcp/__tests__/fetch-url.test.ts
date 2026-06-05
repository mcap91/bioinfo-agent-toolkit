// packages/catalog-mcp/__tests__/fetch-url.test.ts
import { describe, it, expect } from 'vitest';
import { validateUrl } from '../src/core/fetch-url.js';

describe('SSRF guards', () => {
  it('allows https URLs', () => {
    expect(() => validateUrl('https://github.com/org/tool')).not.toThrow();
  });

  it('allows http URLs', () => {
    expect(() => validateUrl('http://example.com')).not.toThrow();
  });

  it('blocks file:// scheme', () => {
    expect(() => validateUrl('file:///etc/passwd')).toThrow(/scheme/);
  });

  it('blocks data: scheme', () => {
    expect(() => validateUrl('data:text/html,<h1>hi</h1>')).toThrow(/scheme/);
  });

  it('blocks ftp:// scheme', () => {
    expect(() => validateUrl('ftp://evil.com/file')).toThrow(/scheme/);
  });

  it('blocks localhost', () => {
    expect(() => validateUrl('http://localhost/admin')).toThrow(/blocked/);
  });

  it('blocks 127.0.0.1', () => {
    expect(() => validateUrl('http://127.0.0.1/admin')).toThrow(/blocked/);
  });

  it('blocks 169.254.169.254 (cloud metadata)', () => {
    expect(() => validateUrl('http://169.254.169.254/latest/meta-data')).toThrow(/blocked/);
  });

  it('blocks 10.x.x.x', () => {
    expect(() => validateUrl('http://10.0.0.1/internal')).toThrow(/blocked/);
  });

  it('blocks 192.168.x.x', () => {
    expect(() => validateUrl('http://192.168.1.1/router')).toThrow(/blocked/);
  });

  it('blocks 0.0.0.0', () => {
    expect(() => validateUrl('http://0.0.0.0/')).toThrow(/blocked/);
  });

  it('blocks IPv6 loopback [::1]', () => {
    expect(() => validateUrl('http://[::1]/')).toThrow(/blocked/);
  });

  it('blocks IPv6 unique local (fc00::/7)', () => {
    expect(() => validateUrl('http://[fc00::1]/')).toThrow(/blocked/);
    expect(() => validateUrl('http://[fd12::1]/')).toThrow(/blocked/);
  });

  it('blocks IPv4-mapped IPv6', () => {
    expect(() => validateUrl('http://[::ffff:127.0.0.1]/')).toThrow(/blocked/);
  });

  it('allows normal domains starting with fc/fd (not IPv6 ULAs)', () => {
    expect(() => validateUrl('https://fdroid.org/packages')).not.toThrow();
    expect(() => validateUrl('https://fc2.com/page')).not.toThrow();
  });
});
