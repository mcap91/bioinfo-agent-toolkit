import { describe, it, expect } from 'vitest';
import { cmpTitleLower, cmpRaw } from '../src/core/sort.js';

describe('sort comparators', () => {
  it('cmpTitleLower is case-insensitive ordinal', () => {
    expect(['banana', 'Apple', 'cherry'].sort(cmpTitleLower)).toEqual(['Apple', 'banana', 'cherry']);
  });
  it('cmpRaw is code-point ordinal', () => {
    expect(cmpRaw('Z', 'a')).toBe(-1); // uppercase sorts before lowercase
  });
});
