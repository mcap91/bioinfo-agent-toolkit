import { describe, it, expect } from 'vitest';
import { tokenize, buildIndex, expandTerm, canonicalForTag, unclassifiedTags } from '../src/core/taxonomy.js';

const tax = { canonical: { 'meta-skill': ['skill-evolution', 'evolve'] } };
const idx = buildIndex(tax);

describe('taxonomy', () => {
  it('tokenize splits on non-alphanumeric, lowercases', () => {
    expect(tokenize('Skill-Evolution Engine')).toEqual(['skill', 'evolution', 'engine']);
  });
  it('expandTerm returns the whole group for an alias', () => {
    expect(new Set(expandTerm('evolve', idx))).toEqual(new Set(['meta-skill', 'skill-evolution', 'evolve']));
  });
  it('expandTerm returns just the term when unknown', () => {
    expect(expandTerm('unrelated', idx)).toEqual(['unrelated']);
  });
  it('canonicalForTag maps alias -> canonical', () => {
    expect(canonicalForTag('skill-evolution', idx)).toBe('meta-skill');
    expect(canonicalForTag('nope', idx)).toBeNull();
  });
  it('unclassifiedTags returns tags not in the taxonomy', () => {
    expect(unclassifiedTags(['evolve', 'random'], idx)).toEqual(['random']);
  });
});
