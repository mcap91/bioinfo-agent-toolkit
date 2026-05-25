---
name: pii-detection
title: "PII Detection / Compliance Skills"
url: ""
category: skill
verdict: pilot
verdict_reason: "HIPAA/CCPA/PCI-DSS coverage; pilot if handling sensitive data"
tags: [pii, compliance, hipaa, ccpa, security]
reviewed: 2026-05-25
supersedes: []
---

## What it does

Automatically fires during planning, code generation, and repo audits to detect personally identifiable information and flag regulatory compliance gaps. Covers eight regulatory frameworks: CCPA, HIPAA, PCI-DSS, COPPA, GLBA, BIPA, FERPA, and the FTC Act. Operates as a background check rather than an on-demand command — it intercepts risky operations before they complete. Source is `gosprinto/compliance-skills/pii-detector`, discovered via Reddit r/claudeskills.

## Why this verdict

Clinical and genomic datasets in bioinformatics frequently carry HIPAA obligations. A skill that intercepts PII exposure automatically during code generation and repo audits reduces the risk of accidental data leakage without requiring developers to manually audit every operation. Pilot is conditional on handling sensitive data — not needed for purely synthetic or public datasets.

## Mechanical details

Source is `gosprinto/compliance-skills/pii-detector`. No public repo URL confirmed at review time. Keep behind a review gate (human confirmation before any flagged action proceeds) until the repo is directly fetched and the skill behavior is verified. Pilot trigger: when the workflow touches clinical data, patient identifiers, or datasets with HIPAA/CCPA obligations.
