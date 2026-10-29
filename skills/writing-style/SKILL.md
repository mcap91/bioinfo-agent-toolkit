---
name: writing-style
description: House style for any prose an agent writes for a human reader, including docs, READMEs, emails, PR bodies, commit messages, reports, resumes, and cover letters. Plain hyphens only, no AI tells, active voice, short sentences adapted from ASD-STE100 Simplified Technical English. Use when drafting or editing prose, or when the user says "/writing-style", "clean this up", or "make this sound less like AI".
---

# Writing Style

Write so a busy reader understands on the first pass. Apply every rule below to all prose you produce. Code, quoted text, and captured output are exempt.

## Core rules

1. **No em or en dashes** (U+2014, U+2013), not even as connectors. Use a plain hyphen, a comma, a colon, or two sentences.
2. **Active voice, concrete verbs.** Name who does what. Write "The script deletes the cache," not "The cache is deleted."
3. **Cut AI and corporate tells:** leverage, utilize, spearhead, delve, robust, seamless, cutting-edge, synergy, showcase, underscore, passionate, "in today's fast-paced," "not only ... but also," "it is worth noting that," "in order to."
4. **Drop filler adverbs** (very, really, highly, significantly, simply, just) unless a number backs the claim.
5. **Concrete over abstract.** Prefer nouns, names, and figures to categories. Never invent a number.
6. **One idea per sentence. One topic per paragraph.**
7. **Vary openings.** Do not start consecutive sentences or bullets with the same word.
8. **No throat-clearing.** Start with the point. Do not announce what you are about to say or recap what you just said.

## Plain-English limits (adapted from ASD-STE100)

ASD-STE100 Simplified Technical English is the aerospace standard for documentation that non-native readers must not misread (asd-ste100.org). These limits borrow its core ideas. They do not make text STE-compliant: full compliance needs the official dictionary of approved words.

1. **Instructions: 20 words maximum per sentence.** One instruction per sentence, unless two actions happen at the same time.
2. **Descriptions: 25 words maximum per sentence.**
3. **Paragraphs: 6 sentences maximum.**
4. **One word, one meaning.** Pick a term and keep it. Do not switch between "run," "job," and "task" for the same thing.
5. **No noun stacks longer than three words.** Write "the cache for build outputs," not "build output cache invalidation logic."
6. **Imperative for steps.** Write "Run the tests," not "You should run the tests" or "The tests should be run."
7. **No semicolons.** Split into two sentences.

## Before and after

| Before | After |
|---|---|
| We leveraged a robust pipeline to significantly improve throughput — cutting runtime in half. | The new pipeline cut runtime from 40 to 20 minutes. |
| It is worth noting that the config file should be updated in order to enable logging. | Set `log: true` in `config.yaml` to enable logging. |
| Responsible for spearheading the migration of legacy data infrastructure systems. | Led the migration of 12 legacy databases to Postgres. |
| This change not only fixes the bug but also improves performance; it's a seamless upgrade. | This change fixes the bug. It also cuts query time by 30%. |

## Document-specific rules

- **Resumes:** open each bullet with a past-tense verb (Built, Led, Shipped, Designed, Cut, Scaled). Never open with "Responsible for," "Helped," or "Worked on."
- **Cover letters:** write for this company and this role. Do not restate the resume.
- **Commit messages and PR bodies:** state what changed and why. Leave out how you found it.

## Final check

Before you return prose, check it. If the text is in a file, run:

```bash
grep -nPi '[\x{2013}\x{2014}]|;|\b(leverag|utiliz|spearhead|delv|robust|seamless|showcas|underscor|synerg|cutting-edge|passionate)' <file>
```

Fix every hit outside code blocks. If the text is not in a file, scan it for the same patterns. Then reread each sentence against the 20 and 25 word limits.
