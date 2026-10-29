reel: https://www.instagram.com/reel/Devav4iBMF5/
captured: 2026-10-29
yt-dlp: 2026.10.26
ffmpeg: 7.0.2-static
faster-whisper: 1.2.1
ctranslate2: 4.8.4
claude: 2.1.281 (Claude Code)

## Caption

First LLMs took over. Then Jev. Now CDMs just dropped 🤯

ScaleDown released 3 tiny “constrained decoding models” on Oct 13, 2026. They don’t chat. They do one job each.

01 · Classify: a label + its probability (plus a one-line reason, if you want it)
02 · Extract: the fields you need as JSON, from text or images (a bill → name + total)
03 · Summarize: short, consistent summaries of inputs up to 1M tokens

Jev (TypeSafe, Sep 15) proved the idea: decide, don’t write. OpenAI, AWS and Cloudflare shipped their own within about two weeks.

ScaleDown claims 200× faster than frontier models on these narrow tasks (their own figure, not an independent benchmark).

💬 Comment CDM and I’ll DM you the setup
➡️ Send this to the friend who still uses GPT for everything
📌 Save it for the next time your app only needs a label or a JSON

Sources: ScaleDown launch (Oct 13, 2026) · TypeSafe’s Jev launch (Sep 15, 2026) · LangChain docs (langchain-scaledown)

#AI #LLM #AItools #MachineLearning #Developers

## Transcript

[   0.0] First, LLMs took over. Then, Jeff showed up. Now, CDMs just dropped. Ask a friend,
[   7.3] bro, is this spam? One word would do. You get a whole speech. That's an LLM.
[  13.5] It builds answers word by word, and you pay for every word. Jeff is the friend who says,
[  19.7] yes, 97% sure. Done. He doesn't write a single word. He just decides. His creator?
[  26.6] One of the people behind ChatGPT. Two weeks later, OpenAI, Amazon and Cloudflare all built their own.
[  33.9] But ask him for the total on a bill or a PDF summary? Not his job. That's where CDMs come in.
[  40.3] Constrained decoding models from ScaleDown. Instead of one all-rounder, three specialists.
[  46.6] One job each, one fixed format, no speeches. Classify. Like Jeff, but it also tells you why.
[  53.8] Extract. Snap a bill. Name and total as JSON plus exactly where it found them.
[  59.4] Summarize. Giant PDF in. Short, consistent summary out. The kicker?
[  65.0] ScaleDown claims they're 200 times faster than frontier models.
[  69.1] So here's the rule. If your app only needs a label or a JSON, stop paying for speeches.
[  74.6] Comment CDM, and I'll DM you the setup. Send this to the friend who still uses GPT
[  79.7] for everything. LLM's talk. Jeff decides. CDMs do one job.

## On-screen text

@pragmaticcoder.ai FIRST, LLMs TOOK OVER. ChatGPT · Claude · Gemini ... + a whole speech THEN JEV SHOWED UP. TypeSafe · Sep 15 · 2026 YES · 97% + just a decision NOW, CDMs ? ? ?

## Key claims

- LLMs generate full word-by-word responses, which costs more even for simple yes/no questions
- Jev, launched by TypeSafe on Sep 15, 2026, gives a single decision (e.g. 'YES · 97%') instead of writing text
- Jev's creator previously worked on ChatGPT
- Within about two weeks of Jev's launch, OpenAI, Amazon (AWS), and Cloudflare each shipped their own similar decision tools
- ScaleDown released three 'constrained decoding models' (CDMs) on Oct 13, 2026: Classify, Extract, and Summarize
- Classify returns a label, probability, and optionally a one-line reason
- Extract pulls fields (e.g. name and total from a bill) as JSON from text or images
- Summarize produces short, consistent summaries from inputs up to 1M tokens
- ScaleDown claims its CDMs are 200x faster than frontier models on these narrow tasks (self-reported, not an independent benchmark)

## Info channel

caption

## Mentioned (unverified hints)

- Jev: (no url)
- ScaleDown CDMs (Classify, Extract, Summarize): (no url)
- ChatGPT: (no url)
- Claude: (no url)
- Gemini: (no url)
- LangChain (langchain-scaledown): (no url)
