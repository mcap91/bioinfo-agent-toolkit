---
name: gstack
title: "gstack"
url: https://github.com/garrytan/gstack
category: framework
verdict: skip
verdict_reason: "kb dispatch covers the relevant orchestration patterns; browser/deployment out of scope"
tags: [workflow, orchestration, browser, kb]
reviewed: 2026-05-25
acquired: 2026-05-25
supersedes: []
---

## What it does

An opinionated workflow stack with browser control, code reviews, and deployment helpers. Bundles many moving parts into a single orchestration framework targeting full application development workflows including browser automation and deployment pipelines.

## Why this verdict

gstack's orchestration overlaps with kb dispatch's launch/review/status lifecycle. The additions gstack makes — browser automation and deployment tooling — are outside kb's scope. kb is a knowledge management and agent orchestration system, not an application deployment framework.

## Mechanical details

Do not install. kb dispatch covers the relevant orchestration patterns (launch, review, status lifecycle for child agent runs). gstack's browser and deployment features are out of scope for kb. No concepts identified as worth adopting.
