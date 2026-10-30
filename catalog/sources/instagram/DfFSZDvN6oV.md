reel: https://www.instagram.com/reel/DfFSZDvN6oV/
captured: 2026-10-30
yt-dlp: 2026.10.26
ffmpeg: 7.0.2-static
faster-whisper: 1.2.1
ctranslate2: 4.8.4
claude: 2.1.281 (Claude Code)

## Caption

So can we stop talking about LLM wikis now and just accept karpathy wasn’t right. 🤣 he moved on - why haven’t you? 
#ai #artificialintelligence #openai

## Transcript

[   0.0] You've all heard about Karpathy's LLM Wiki and if you saw my knowledge graph post you know I've
[   6.0] called most of it bullshit because an obsidian graph is just a visualizer. A real knowledge
[  12.3] graph is incredible but very hard to model and obsidian has none of that machinery.
[  17.8] So what about when the LLM Wiki is done properly? Is it worth it and which repos actually do
[  25.1] First, a little history. In April Karpathy posted a simple idea. Instead of searching your files
[  31.2] every time a model reads them once and writes a wiki it keeps up to date. Within days the version
[  37.4] that went viral was an obsidian vault with a pretty graph while underneath the model still
[  42.8] just runs a keyword search with grep. But a few people built the idea properly. There's a desktop
[  49.5] app by Nashu that merges new sources into its pages and follows the links. There's a clod code
[  55.5] plugin by NVK that won't let a page exist without a source behind it. And there's one by Lukastorian
[  62.4] that makes your own agent cite a source for every single claim. So how do they perform?
[  67.4] I said each one up exactly as the author says and marked every answer blind against plain
[  73.4] old clod code. NVK got more right than plain clod code but it cost about twice as much per answer.
[  82.5] Lukastorian did no better and spent more than three times as many tokens and Nashu the one
[  88.2] that actually follows its graph did no better either even with vectors. It's also the most
[  94.7] starred of the lot. So that's what you can say about GitHub stars. So what are you actually
[ 100.5] trying to do? If like one of my community members you just want the right answer from
[ 105.0] across your repos, what about leaning on native memory architecture? Organize with something
[ 111.1] like Jake van Cleef's interpretable context methodology as ICM which is in its essence
[ 116.9] just somewhere organized folders. Well what a surprise it was as accurate as the best of
[ 123.1] them at half the cost and the labs agree because Anthropic and OpenAI both built
[ 127.8] their coding agents on plain files. Look if it was me I'd keep plain clod code, give it a structure
[ 134.3] like ICM, add a hook that makes it cited sources, keep it simple, stupid. Hopefully that puts LLM
[ 142.2] wikis to bed. Next time you see a fancy graph know it's bullshit. You don't need a rocket ship to
[ 148.5] go to a corner store. Time to level up friends. Chemical Cat Club signing out.

## On-screen text

LLM WIKI /wiki:compile --local List ✓ sources checked

## Key claims

- The viral Obsidian-based version of Karpathy's LLM Wiki is just a pretty graph visualizer underneath, running plain keyword search (grep)
- A few projects implemented the LLM Wiki idea properly: Nashu's desktop app, NVK's clod code plugin, and Lukastorian's source-citing agent
- NVK's plugin got more right answers than plain clod code, but cost about twice as much per answer
- Lukastorian's agent did no better than plain clod code and used more than three times as many tokens
- Nashu's app (the most GitHub-starred of the three) did no better than plain clod code even with vector search
- GitHub stars don't correlate with actual performance
- Using plain clod code organized with Jake van Cleef's ICM (essentially organized folders) was as accurate as the best LLM Wiki tools at half the cost
- Anthropic and OpenAI both built their coding agents on plain files, supporting the simpler approach
- The author's recommendation: keep plain clod code, add an ICM-like structure, add a hook for citing sources, keep it simple
- Fancy knowledge graphs for LLM wikis are unnecessary ('bullshit') compared to simpler file-based approaches

## Info channel

spoken

## Mentioned (unverified hints)

- Karpathy's LLM Wiki (original idea): (no url)
- Obsidian vault (viral version): (no url)
- Nashu's desktop app: (no url)
- NVK's clod code plugin: (no url)
- Lukastorian's agent (source-citing): (no url)
- Jake van Cleef's ICM (Interpretable Context Methodology): (no url)
- Clod Code: (no url)
