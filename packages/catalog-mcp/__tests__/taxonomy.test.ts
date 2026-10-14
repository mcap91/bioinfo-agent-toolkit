import { describe, it, expect } from 'vitest';
import { buildIndex, canonicalForTag, unclassifiedTags } from '../src/core/taxonomy.js';

const tax = { canonical: { 'meta-skill': ['skill-evolution', 'evolve'] } };
const idx = buildIndex(tax);

describe('taxonomy', () => {
  it('canonicalForTag maps alias -> canonical', () => {
    expect(canonicalForTag('skill-evolution', idx)).toBe('meta-skill');
    expect(canonicalForTag('nope', idx)).toBeNull();
  });
  it('unclassifiedTags returns tags not in the taxonomy', () => {
    expect(unclassifiedTags(['evolve', 'random'], idx)).toEqual(['random']);
  });
});
