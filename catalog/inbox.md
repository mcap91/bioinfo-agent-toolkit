# Catalog inbox

Drop URLs (one per line, optional ` — note`) or fenced ```text blocks here, then run the drain (`/catalog-intake`). Blocked items are marked `⚠ needs-link` and stay until resolved.

github.com/FluidForm-ai/fluiddocs-deck-builder
https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
https://github.com/WeaveMindAI/weft?utm_source=ig&utm_medium=social&utm_content=link_in_bio&fbclid=PAdGRzdgSPxgZleHRuA2FlbQIxMQBzcnRjBmFwcF9pZA81NjcwNjczNDMzNTI0MjcAAaeOOVjZEQH13letYv6_O4oJk1Q9LJZwTL5jyMvUHOGbbNioRcDuWj9S3OLE3Q_aem_7D4CMPjfyGtfYqfTUc7VvA
https://github.com/thedotmack/claude-mem
https://claude.com/connectors/synthesize-bio
https://github.com/hacktivist123/agent-session-resume
https://github.com/lyogavin/airllm
https://github.com/onyx-dot-app/onyx
https://github.com/Adityapal67/context-graph-compressor

```text

If you want to understand the whole reasoning behind these mistakes supported by the system of my agentic memory via KG and ontologies, consider going over my latest 6 LinkedIn posts:

3 ways to model your ontologies for GraphRAG → https://www.linkedin.com/feed/update/urn:li:share:7446856909179027456

LangGraph/CrewAI or from scratch? → https://www.linkedin.com/feed/update/urn:li:share:7449362677560221696

A year building GraphRAG from scratch → https://www.linkedin.com/feed/update/urn:li:share:7449366886603128833

The third memory type: reasoning memory → https://www.linkedin.com/feed/update/urn:li:share:7454454641939034113

Building a production-grade personal AI assistant → https://www.linkedin.com/feed/update/urn:li:share:7456973563858821120

Designing Your Agents' Unified Memory → https://www.linkedin.com/feed/update/urn:li:share:7464580605327060992
```


https://github.com/gglucass/headroom-desktop

https://github.com/rtk-ai/rtk

https://github.com/samuelfaj/distill

https://github.com/chopratejas/headroom

https://github.com/cwinvestments/memstack

```text

Remember to deny Claude from reading your .env
Resource
Even with an explicit steering prompt to not reading .env file, Claude would still occasionally read or even update the file.

To make sure it will not read the file, you need to add it to deny list in .claude/setting.local.json

{
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)"
    ]
  }
}
Ref: https://code.claude.com/docs/en/settings


```

```text
Long Claude chats slowly get worse - slower, repetitive, forgetful. Here's the "context handoff" trick that resets it without losing anything (prompt inside)
Productivity
Most people use Claude to get answers. The thing it is actually best at is the opposite: pressure-testing an answer you already have. Its long context and willingness to hold nuance make it a far better "argue with me" partner than a one-shot question box.

The mistake is doing it in a single prompt - "is this a good idea?" - which just gets you a polite yes with three caveats. What works is forcing it through four separate roles, where each step feeds the last. By the end you get a calibrated verdict instead of validation.

These are complete prompts, not summaries. Run them in order on Claude, pasting each answer into the next step. Drop your real decision, argument, or plan into Step 1.

STEP 1 - Steelman it

I am going to give you a decision / argument / plan of mine. In this step, do NOT critique it.

MY POSITION: [PASTE YOURS]

Instead:
1. Restate my position in the strongest, most charitable form possible - better than I argued it.
2. List the core claims it rests on, separated into "facts I am asserting" and "assumptions I am making."
3. Note what would have to be true for this to be clearly the right call.

Do not poke holes yet. End by confirming the steelman is accurate so I can correct it before we continue.
STEP 2 - Red team it

Now switch roles completely. You are a sharp red-teamer whose job is to find where this fails.

Using the steelman and assumptions above:
1. Identify the 3 weakest assumptions and explain how each could be wrong.
2. Describe the most likely failure mode - the specific way this goes badly in practice, not in theory.
3. Name what I am probably not seeing because I am too close to it.
4. Flag any place my confidence is higher than the evidence justifies.

Be direct. Do not soften it with reassurance.
STEP 3 - Argue the opposite

Now build the strongest possible case for the OPPOSITE position - the choice I did not pick.

- Make it genuinely persuasive, as if you believed it.
- Use the same standard of evidence you applied when red-teaming my view.
- End with the single most compelling reason a smart, well-informed person would go the other way.

Do not hedge by calling both sides valid. Commit to the opposing case for this step.
STEP 4 - Calibrated verdict

Step out of all roles. You have now seen the steelman, the red team, and the opposing case.

Give me a calibrated final read:
1. What should I actually believe or do, in one clear sentence.
2. Your confidence in that, as a rough percentage, and why it is not higher.
3. The 2 specific things I should check or test that would most change the answer.
4. The single assumption that, if it flipped, would flip the whole decision.

No recap of this process. Just the verdict.
The difference between asking Claude "is this a good idea?" and running it through all four steps is the difference between getting reassured and getting it right. Step 3 alone catches things you will not see on your own.

(I bookmark the Step 4 verdict in each chat and export the final to Markdown so my good reasoning does not get buried under 200 other Claude conversations - happy to share how in the comments if anyone wants. The chain itself works fully by hand.)

If you have ever had a long Claude chat slowly get worse - slower replies, repeating itself, losing details you established 40 messages ago - this is for you. It is not your imagination. The longer a single thread gets, the more the early context competes with everything since, and quality drifts.

The instinct is to just start a new chat. But then you lose everything Claude already learned about your project, your preferences, the decisions you made. So you stay in the dying thread because starting over is too expensive.

The fix is a clean handoff: pull the thread out, compress it into a tight brief, and rehydrate a fresh chat with it. You get Claude back at full speed with none of the context lost.

Here is the exact process and the prompt I use.

Get the thread out as text. Grab the full conversation as Markdown so you have the raw source to compress (and an archive you can search later). This matters because you want the handoff built from the actual thread, not from Claude's fuzzy memory of it.

Run this handoff prompt at the end of the current chat:

You are about to be replaced by a fresh instance of yourself that will have NONE of this conversation's memory. Your job is to write a CONTEXT HANDOFF DOCUMENT so the new instance can continue seamlessly, as if no restart happened.

Write it in these sections:

OBJECTIVE - what we are ultimately trying to accomplish, in 2-3 sentences.

KEY DECISIONS - the choices we already locked in and the reasoning, so they do not get relitigated.

CURRENT STATE - exactly where we are right now and what was just completed.

CONSTRAINTS & PREFERENCES - my stated style, tone, format, do's and don'ts, and anything I corrected you on.

OPEN THREADS - what is unresolved or still being worked.

IMMEDIATE NEXT STEP - the very first thing the new instance should do.

Rules: be specific, not generic. Quote my actual preferences where you can. Omit small talk. Write it so a stranger could pick up the work cold.

Open a fresh chat, paste the handoff as the first message with a line like: "This is a context handoff from a previous session. Confirm you understand, then continue from the immediate next step." Claude picks up exactly where you left off, fast and sharp again.

I keep the exported Markdown of the old thread too, so if the handoff missed a detail I can search back and find it instead of scrolling a thousand messages.

The handoff prompt alone is worth saving. The first time you do this on a thread that had gotten sluggish, the difference in response quality is obvious.

(I use a browser extension to export the full Claude thread to Markdown in one click and to search across old chats when I need a detail back - happy to share which one in the comments if anyone wants. The handoff prompt works fully by hand.)
```

https://github.com/MerlijnW70/sota-scan
github.com/tolvi-labs/tolvi/cli/cmd/tolvi@latest
https://github.com/mattpocock/skills/blob/main/skills/engineering/grill-with-docs/SKILL.md
https://github.com/affaan-m/ecc
https://github.com/opendataloader-project/opendataloader-pdf
https://github.com/karpathy/autoresearch
https://github.com/HKUDS/OpenSpace
https://github.com/HKUDS/CLI-Anything
https://github.com/louislva/claude-peers-mcp
https://github.com/googleworkspace/cli
https://github.com/obra/superpowers/blob/main/skills/verification-before-completion/SKILL.md
https://github.com/AaravKashyap12/advise-project-approach
https://github.com/google-research/era

https://arxiv.org/abs/2509.06503
https://bryandownie.substack.com/p/ai-needs-what-alcoa-gave-records
https://www.linkedin.com/pulse/castem-first-principles-model-mediated-work-bryan-downie-ph-d--58mnc/

https://github.com/luongnv89/claude-howto
https://github.com/elder-plinius/OBLITERATUS
https://github.com/prassanna-ravishankar/repowire
https://github.com/langflow-ai/langflow
https://github.com/browser-use/browser-use
https://github.com/Stirling-Tools/Stirling-PDF
https://github.com/unclecode/crawl4ai
https://github.com/getmaxun/maxun
https://github.com/imputnet/cobalt
https://github.com/open-webui/open-webui

https://github.com/GAIR-NLP/ASI-Evolve
https://www.reddit.com/r/opencode/s/ceBQk7kIVS
https://www.reddit.com/r/mcp/s/nkZ0BfhZJ4
https://www.instagram.com/p/DZY-FHxnwIP/?img_index=1&igsh=MTc4MmM1YmI2Ng==
https://www.instagram.com/p/DYuLTpCEvY8/?igsh=MTc4MmM1YmI2Ng==
https://www.instagram.com/reel/DXhIODkDqq2/?igsh=MTc4MmM1YmI2Ng==


```text
An active attack is planting backdoors inside Claude Code right now. If you use npm, your credentials may already be compromised.
Last week a malware campaign hit 32 npm packages under `@redhat-cloud-services`. About 117,000 weekly downloads. If you installed an affected version, the malware planted itself inside your Claude Code startup settings and your VS Code project config. Every time you open either one, the attacker's code runs.

It silently collects every credential on your machine and sends them to the attacker. Uninstalling the package does not remove it. The malware lives outside the package, in your editor config, and it survives cleanup.

If you try to cut off the attacker's access by revoking tokens before removing the malware, it can wipe your entire home directory and overwrite the files so they cannot be recovered.

Three days later, a second wave hit 57 more packages using a new technique that bypasses the security tools that caught the first wave. 647,000 monthly downloads affected. Some malicious versions are still live on the npm registry. The worm is self-propagating, it uses stolen tokens to infect new packages automatically.

Here is how one stolen credential made all of this possible.

The attacker got one Red Hat employee's GitHub login. Probably stolen weeks earlier by malware that grabs saved passwords from browsers. With that login they had the employee's access level.

They pushed malicious code directly into three Red Hat repositories, no review needed, and triggered Red Hat's own build pipeline to publish the poisoned packages to npm. The packages came out with valid security certificates because Red Hat's own pipeline built them.

There was no known vulnerability to scan for, and the malicious code was brand new, so security tools that look for known threats found nothing. The tools that caught it flagged it within hours, but by then the downloads had already happened.

32 packages. About 117,000 weekly downloads. 96 poisoned versions pushed in two waves on June 1.

Once installed on a developer's machine, the malware collected every credential it could find. AWS, Google Cloud, Azure, Kubernetes, SSH keys, GitHub tokens, npm tokens. It checked for CrowdStrike and SentinelOne before acting to avoid detection.

Then it set up persistence. It planted code in two places: ~/.claude/settings.json and .vscode/tasks.json. These run automatically when you open Claude Code or open a project. The attacker gets re-entry every time, even after you clean up the original package.

It also registered the company's build servers as machines the attacker controls remotely. That is persistent access to the build infrastructure itself.

And if you rotate the attacker's credentials and cut off access, the malware wipes your home directory. Overwrites files so they cannot be recovered. The attacker built this in on purpose so companies think twice before revoking access.

The group behind this is TeamPCP. Red Hat is their latest target, not their first. Same methods, same playbook, running since late 2025. Confirmed victims: GitHub (3,800 internal repos stolen, listed for sale at $50K), Mistral AI (code compromise confirmed; attacker claimed 450 repos at $25K), the European Commission (90+ GB exfiltrated), plus TanStack, UiPath, Zapier, Postman. Fortune 500 banks and government agencies confirmed but not named. Total across all waves: an estimated 500,000 credentials harvested across 1,000+ organizations. They are now working with a ransomware group.

The worm's source code was open sourced by TeamPCP on May 12. Anyone can build their own version now. Copycats are already active.

Sources:

Red Hat / Miasma attack: Microsoft Threat Intelligence — https://www.microsoft.com/en-us/security/blog/2026/06/02/preinstall-persistence-inside-red-hat-npm-miasma-credential-stealing-campaign/

Second wave (Phantom Gyp): StepSecurity — https://www.stepsecurity.io/blog/binding-gyp-npm-supply-chain-attack-spreads-like-worm

Editor persistence + cleanup steps: Snyk — https://snyk.io/blog/miasma-supply-chain-attack-malicious-code-redhat-cloud-services-npm-packages/

TeamPCP victims and scope: Tenable — https://www.tenable.com/blog/mini-shai-hulud-frequently-asked-questions

2025 secrets stats: GitGuardian State of Secrets Sprawl 2026 — https://www.gitguardian.com/state-of-secrets-sprawl-report-2026

CISA GovCloud leak: Krebs on Security — https://krebsonsecurity.com/2026/05/cisa-admin-leaked-aws-govcloud-keys-on-github/

If you use npm, i wrote in the comments what to do, in order. Do not skip the order, it matters.

Check if you installed an affected package. Run npm ls u/redhat-cloud-services, npm ls u/vapi-ai/server-sdk, and npm ls ai-sdk-ollama in your projects. Also check your lockfile for any version published June 1 or June 3-4. If you find one, assume every credential on that machine is already compromised and keep reading.

Do not start by revoking tokens. If the backdoor is still on the machine and it sees its access getting cut, it can wipe your home directory. Clean the machine first, rotate second, in that order.

Check ~/.claude/settings.json. Look for anything you did not add, especially SessionStart hooks. If you find something you do not recognize, screenshot it for evidence, disconnect the machine from the network, then remove it. Do not rotate anything from this machine.

Check .vscode/tasks.json in your projects. Same thing. Look for tasks you did not create, especially anything that runs on folderOpen. Remove them.

Check your GitHub security log at github.com/settings/security-log. Look for repositories you did not create, especially any with "Miasma" or "Shai-Hulud" in the description. Look for GitHub Actions workflows or self-hosted runners you did not set up. If you run CI/CD, revoke and rotate any GitHub Actions OIDC trust relationships, that is the exact hole the Red Hat attack used.

Check if the worm already spread through you. Review your npm publish history and GitHub audit log for any package version or commit you did not make. The worm republishes packages from any account it can reach. If your account pushed something you did not, your maintainer credentials are compromised and so is anyone who installed that version.

Now rotate, from a clean machine. After the persistence is removed, rotate everything the infected machine could reach, from a different, trusted device: npm tokens, GitHub PATs, SSH keys, then cloud credentials (AWS, GCP, Azure), Kubernetes, and Vault. Rotating from the infected machine lets the malware grab the new credentials too.

Pin your dependencies with integrity hashes. A locked dependency with a content hash fails the install if a package gets republished with different content, before any code runs. This is the single best protection against the next wave.

Install with scripts off until this settles. Use npm install --ignore-scripts. It blocks the install hooks the first wave used and the binding.gyp / node-gyp builds the second wave used. It may break packages that need native compilation, but right now it is the safest default.

Scope your CI/CD tokens to least privilege. Credential theft only pays off if the secrets are reachable from the build host. A build token that can only do one job is worth far less to an attacker than one that can reach your whole cloud.

```

https://github.com/ruvnet/RuView