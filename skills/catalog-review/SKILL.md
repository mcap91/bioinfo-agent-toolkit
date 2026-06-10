---
name: catalog-review
description: Review autonomously-generated catalog drafts and approve or reject them. Use after a processing run produces drafts.
---

# Catalog review

1. `review {action:list}` → the pending drafts. **Check this first** — if the count is 0,
   there is nothing to review.
2. For each draft, read `catalog/entries/<name>.md` with the user. Check the verdict,
   reasoning, tags, and `security_flags`. This is the validation gate — drafts come from
   untrusted fetched content.
3. Decide:
   - Approve: `review {action:approve, name:<name>}` (flips to approved, re-indexes).
   - Reject: `review {action:reject, name:<name>, reason:"…"}` (records verdict: skip,
     keeps it as a tech-radar entry, suppresses re-ingest).
4. Never bulk-approve without reading. The point of the gate is your eyes.
