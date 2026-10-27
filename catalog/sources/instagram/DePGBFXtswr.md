reel: https://www.instagram.com/reel/DePGBFXtswr/
captured: 2026-10-27
yt-dlp: 2026.10.26
ffmpeg: 7.0.2-static
faster-whisper: 1.2.1
ctranslate2: 4.8.4
claude: 2.1.281 (Claude Code)

## Caption

These are my essential AI coding skills I use to keep code quality high and not bloated when AI writes and merges my code for me.

This is video 5 of 7 in my “how to become a 10x ai-native developer” series, and in the first 4 videos I talked about how I use cloud agents be a 24/7 on call engineer for me that fixes bugs for me while I sleep by using verification skills to verify all the code changes actually work as intended and how they merge the code for me without me reviewing the code, and as a result I have a lot of code being merged without my supervision.

I know a lot of you are wondering, how do you keep the code quality high when letting AI write so much code?
I do so by deferring to skills to do that.
I use the cursor team’s thermo nuclear code quality review (excessive, I know) in conjunction with framework specific tools like a react best practices skill and with , one of my personal favorites, the ponytail skill. Highly recommend you check out the ponytail.dev website which is the home for the skill it is so funny and I’ll show a little screenshot right here, but essentially I have these sets of skills to point out common pitfalls of overly verbose and complicated code and I tell all my coding agents to run these skills before making the PR and sometimes I tell them to run these simplification skills multiple times in a row. Due to the non deterministic nature of LLMs, forcing them to run these simplification skills multiple times allow these models to uncover new simplification methods that it didn’t catch the previous try.

#coding #ai #developer

## Transcript

[   0.0] These are the AI coding skills I use to ship 30 PRs a day while keeping the code quality
[   4.3] high and not bloated.
[   5.6] This is video five of seven in my how to become a 10x AI native developer series.
[   9.7] And in the first four videos, we talked a lot about the creating verification skills
[  13.5] that you can create cloud agents that autonomously write, test and verify and merge code
[  18.1] for you.
[  19.1] And the number one question that I've been getting asked is how do you keep the
[  21.4] code quality high when so much code is getting merged.
[  24.1] And the way that I do that is with skills.
[  26.2] So here are some of the AI coding skills that I use to make sure my code is not
[  29.8] bloated, simple and clean and easy to read.
[  32.6] So my first and favorite skill that I want to talk about is called ponytail.
[  35.6] And you can check it out at ponytail.dev.
[  37.4] And the landing page is actually hilarious because it's all about this little
[  40.4] avatar right here.
[  41.6] It's that one senior staff engineer that gets paged when things are really bad
[  44.8] and broken comes in, fixes it with like two lines of code and goes back to sleep.
[  48.4] And the skill is essentially a gigantic D bloating tool that will call out design
[  52.6] paradigms that are bad, simplify things down as much as possible,
[  55.9] refactor into reusable code modules.
[  58.2] It's pretty great and really keeps the code quality pretty high.
[  61.0] So that's the first one that I want to talk about.
[  62.5] But we have two more that I want to call out.
[  64.2] So next up is within P stack.
[  66.1] I've talked a lot about P stack in the first four videos of the series,
[  68.8] but essentially P stack is a plugin, not just an individual skill that a
[  72.6] SpaceX engineer created who goes by potato on X.
[  76.4] And it's a giant engineering system on creating a software factory and
[  79.9] shipping code at a really high quality and shipping a lot of it.
[  82.8] And it's what powers probably a 90% of the PRs that I write on a daily basis.
[  86.9] And P stack itself actually has a lot of great D bloating simplification
[  91.0] skills built into it, such as this no comments skill right here,
[  94.4] the type script best practices and unslop.
[  97.2] And basically every single time I use P stack, it automatically calls these
[ 100.5] tools and then I also externally call this ponytail skill.
[ 103.7] And then last but not least, the third skill that it also calls is
[ 106.7] this thermal nuclear code quality review skill, which is another skill created
[ 110.8] by the team at cursor slash SpaceX AI.
[ 113.7] And it pretty much does the same thing as the first two skills that we mentioned
[ 116.8] with ponytail and some of the other sub skills that the P stack offers.
[ 120.3] So essentially with every single PR I write, I condense all of this into
[ 123.6] one single simplified command that will call all the simplification
[ 127.0] commands within ponytail within P stack and within the thermonuclear
[ 131.8] code quality review skill to keep my code changes as minimal as possible
[ 136.2] and keep the quality high in the next video in this series.
[ 139.0] I'm going to be talking about how to write really effective prompts so
[ 142.1] that you can have full confidence to significantly improve the quality
[ 145.2] of work that your agents do so that you no longer have to supervise
[ 148.0] and manage them and instead you can trust that they're actually
[ 150.2] getting the work done by themselves without you involved.

## On-screen text

How To Become a 10x AI-Native Developer Ep. 5 of 7 | These are the AI | Last Turn +285 | apps/yorby-web/lib/billing/parse-sufficient-credit-even ... have some that already ... that we use ... edit deduction ... the Account ... tent Coach, Chat Spy ... Carousel ... ch tracks credit ... is in, like, p ... able for audit logging, as well ... sure that ... ters that are ... app don't get ... educated when the app on a ... taskId: string, ... 5 unmodified lines ... message: GPMessage ... 5 unmodified lines ... p_task_id: input.taskId, ... p_user_message_id: double_IhB_listing_body ... magic ... async plan(){} ... const chart_active_forecast ... reuses the existing ... calculation, ... ledger. Admin use ... rem cost without ... 30 PRs a day | How To Become a 10x AI-Native Developer Ep. 5 of 7 | while keeping the code | this is video 5 of 7 in my | who goes by a poteto on X | in the next video

## Key claims

- The creator uses AI coding skills to ship 30 PRs a day while keeping code quality high and not bloated
- This is video 5 of 7 in a 'how to become a 10x AI-native developer' series
- Previous videos covered using cloud agents to autonomously write, test, verify, and merge code without human review
- Code quality is maintained despite high-volume autonomous merging by relying on 'skills'
- The 'ponytail' skill (ponytail.dev) is a favorite tool described as a 'gigantic de-bloating tool' that calls out bad design paradigms, simplifies code, and refactors into reusable modules
- P-stack is a plugin/engineering system created by an engineer who goes by 'poteto' on X, said to be a SpaceX engineer, and powers ~90% of the creator's PRs
- P-stack includes built-in de-bloating/simplification skills: a 'no comments' skill, TypeScript best practices, and 'unslop'
- The 'thermonuclear code quality review' skill, created by the Cursor/SpaceX AI team, performs similar de-bloating/simplification functions
- The creator combines ponytail, P-stack's built-in skills, and the thermonuclear code quality review into one condensed command run before every PR
- Simplification skills are sometimes run multiple times in a row because LLM non-determinism lets repeated runs catch additional simplifications missed on prior passes
- The next video (6 of 7) will cover writing effective prompts to improve agent work quality without needing supervision

## Info channel

spoken

## Mentioned (unverified hints)

- ponytail: ponytail.dev
- P-stack: (no url)
- thermonuclear code quality review: (no url)
- no comments skill: (no url)
- TypeScript best practices: (no url)
- unslop: (no url)
- react best practices skill: (no url)
