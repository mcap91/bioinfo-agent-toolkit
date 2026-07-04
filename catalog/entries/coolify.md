---
name: coolify
title: Coolify
url: "https://github.com/coollabsio/coolify"
category: framework
tags: [PaaS, self-hosted, deployment, Docker, databases, infrastructure]
reviewed: 2026-07-03
security_flags: [prior-cves]
summary: ">-"
acquired: 2026-07-04
---

## What It Does

Coolify manages servers, applications, and databases on your own hardware via SSH. It
provides a web dashboard for deployments, resource monitoring, log streaming, and
one-click rollback. Supports VPS, bare metal, and Raspberry Pi.

## Key Features

- **Git-push deployments**: push to a connected branch, Coolify builds and deploys
  automatically with Let's Encrypt SSL
- **Database provisioning**: one-click Postgres, MySQL, Redis, MongoDB with connection
  details auto-injected as env vars
- **Preview deployments**: PR-based preview URLs, replicating the Vercel/Netlify workflow
- **Build system**: GitHub/GitLab webhooks, Docker Compose, Dockerfiles, Nixpacks,
  Heroku buildpacks
- **Multi-server**: manage deployments across multiple servers from one dashboard
- **280+ one-click services**: pre-configured templates for common applications
- **No vendor lock-in**: all configuration stays on your server

## Limitations

- No auto-scaling — scaling is manual
- Multi-node HA requires manual glue work
- You own all ops (patching, backups, security updates)
- Had several critical CVEs in 2025/2026 — consistent patch management required

## Deployment Options

- **Self-hosted**: `curl -fsSL https://cdn.coollabs.io/coolify/install.sh | bash`
- **Cloud**: managed version at app.coolify.io (paid)

## Links

- GitHub: https://github.com/coollabsio/coolify
- Site: https://coolify.io/