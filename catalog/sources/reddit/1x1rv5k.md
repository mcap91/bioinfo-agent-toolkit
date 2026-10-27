source: https://www.reddit.com/r/LocalLLM/comments/1x1rv5k/comment/pew7oqh/
captured: 2026-10-27
playwright: 1.64.1
chromium: 156.0.8078.4

Skip to main content
Mirai S 70 tok/s, 262k context, 12GB GPU : r/LocalLLM
Sign Up
Log In
Expand user menu
Go to LocalLLM
r/LocalLLM
•
17d ago
u/ProfessorPalmer
Mirai S 70 tok/s, 262k context, 12GB GPU
Model

Mirai S from Mirai Labs is stronger and faster than ever! This is my agentic workflow patch for 27b quants applied to Mirai on my RTX4070

- 12gb+ users get the full 262k context at 70tok/s AND the agentic improvement patch!

- 16gb+ users get all of these AND all positions in vram so even better numbers.

Speed + quality supercharges on a 12gb Facebook Marketplace GPU.

Ridiculous time for "Little Local" AI!

Original model : https://huggingface.co/trymirai/Qwen3.8-27B-S-experimental

Quality + speed patch : https://github.com/professorpalmer/mirai-s-ada/

What does the quality patch solve?

Three things:

Code tool. For a chat request that brings no tools of its own, the proxy appends one OpenAI-style function definition, run_python(code, stdin), to the request. If the model answers with a tool call, the proxy runs the code in a WASI sandbox (CPython 3.12 under wasmtime: no host files, no network, no processes, 128 MB, 10 s), appends the result as a tool message, asks the model again, and loops (12 rounds max). The client sees one normal response. The user's prompt text is also dropped into the sandbox as input.txt so the model reads data instead of retyping it. Streaming works the same way: tokens relayed live, tool-call deltas withheld and executed between rounds.

API cards. For coding requests (a coding tool is offered, or Python in the prompt), the proxy introspects the modules the task mentions inside that same sandbox runtime (signatures, docstrings, constants, class methods) and appends the text to the end of the first user message, plus one sentence: "use the library functions listed above instead of implementing these formats by hand." Nothing hand-written; the card is whatever the runtime actually exports. Placement mattered a lot: same cards in the system message did nothing.

API check. Code the model wrote in earlier tool calls is parsed and checked against the real runtime (names, kwargs); mistakes get a one-line note on the tool result.

Pass-through rules keep it safe: requests with client tools get cards only (the tool offer hurt there), and conversations that already carry fenced code (agents that execute code themselves) are forwarded untouched. All of it is just the OpenAI chat schema, so it works on any server with a tool-calling template

Read more
Share
Sort by:
Comments Section
FaatmanSlim
•
17d ago

As someone who owns a 16 GB GPU - thank you! Glad to see more options for us GPU-mid/poor these days. Curious what people think is the best option for 12 and 16 GB GPUs now:

Qwen 3.8 Flash Next on Strata

Qwen 3.8 27B GSO RCQ on llama.cpp

Ternary Bonsai - though seems like this is not usable for long-running or agentic tasks

ninfer for 4080 and 5060

Mirai, from this post

Any other alternatives?

Reply
Share
ProfessorPalmer
•
17d ago

I actually fixed Bonsai first! 100 tok/s 262k on 12gb. The quality patch fixes the agentic issues.

I haven't played with anything on the list except for Mirai S and Bonsai but Mirai is reallllly good. I'll test the others soon i hope!

https://github.com/professorpalmer/bonsai-ada-surgery

Anstellos
•
16d ago

trued bonsai it was always way dumber than orignal qwen 27b... so fast but stupid. did you really fixed it?

1 more reply
Life-Screen-9923
•
17d ago

Underdog-Saluki-27B-1.0-IQ2-mix.gguf, 7.89 GB without MTP, for stock llama.cpp

llamAmpere for rtx 3060/3090, supports low memory (12gb) configs for 200k+ ctx

1 more reply
u/anthropic-ai
•
Ad
Hand Claude the whole social post, landing page, or layout. It does the work. You keep, edit, or steer any piece.
Learn More
claude.com
Collapse video player
CaptainBloodEz
•
17d ago

For those who care about quant and don’t want to read: it’s 2.4 bit.

_bani_
•
17d ago

the mods really need to start requiring the quant in the post title.

CaptainBloodEz
•
17d ago

I swear to Christ.

Intrepid_Inspection8
•
17d ago

does it run on AMD? how well does it compare to the original Qwen3.8?

2 more replies
69420trashpanda69420
•
17d ago

It's just a quant of an already fine model. No need to market it as something new.

1 more reply
No-Business5854
•
17d ago
 Top 1% Commenter

KillerX629
•
17d ago

Whats the perplexity like?

u/Depop
•
Ad
Anyone else got the urge to clear out their closet and sell everything on Depop? Sell your style on Depop with no selling fees. Payment processing & Boosting fees apply.
Download
depop.com
Collapse video player
drazyan22
•
17d ago

How about benchmark compared to orgin qwen3.8-27b?

ProfessorPalmer
•
17d ago
drazyan22
•
17d ago

That mean it's higher then base model?

2 more replies
nenecaliente69
•
17d ago

can it run on my system? i just wanna run it smooth like the video! its always laggy even on "smaller" models, maybe its my LMstudio bad/default settings?

ProfessorPalmer
•
17d ago

Oh yeah def. Llama.cpp and all the settings and stuff are included!

ProfessorPalmer
•
17d ago

This is not my model, for the record... im not here to claim it's the best or anything I'm just providing a recipe that makes the existing model faster and smarter

baron_von_noseboop
•
14d ago
•
Edited 13d ago

I had all but given up on getting a decent local LLM agent. Everything was either too dumb (3.6 35b), too slow (3.8 27b), or required too small of a context window.

This is getting me 50-70 t/s sustained on my 12GB rtx 4070 even with DDR4. Thank you! I think the bitchy little snipers in this thread should go touch grass.

Edit: Ah, now I'm sad again. I was getting high throughput in initial tests even with high context, but this was with an artificial inputs. With actual agentic coding work, throughput drops to ~15 tok/s.

ProfessorPalmer
•
10d ago

Should check the updates in the last few days! Solved a ton of problems.

former_farmer
•
17d ago

The quant...

mike4080s
•
17d ago

Where exactly is that 98% number coming from? I can't find it in either link.

Also, the repo's own table shows 72.6 tok/s at 16k context, which drops to 11tok/s at 180k.

16 more replies
allOfTheB4conAndEggs
•
17d ago

Very cool. What harness is that?

ProfessorPalmer
•
17d ago

Marionette, my own.

People also ask about section
People also ask about
Mirai S agentic workflow patch for local LLM
Best local LLM for coding with 12GB VRAM
Best graphics card for local LLM
Local LLM benchmarks for RTX 3060
Best practices for training local LLMs
More posts you may like
Related posts
Qwen 3.8 27B on dual RTX 5060 Ti - 130 tok/s - full 256k context
r/LocalLLM
•
1mo ago
Qwen 3.8 27B on dual RTX 5060 Ti - 130 tok/s - full 256k context
141 upvotes · 141 comments
Roblox
•
Ad
Precise aim and fast reactions decide the winner in Roblox's intense FPS experiences.
roblox.com
Play Now
Is anyone still playing Mirai?
r/ProjectDiva
•
10mo ago
Is anyone still playing Mirai?
373 upvotes · 68 comments
Qeen 3.6 35b a3b pruned violently to 27b.
r/LowEndLocalAI
•
17d ago
Qeen 3.6 35b a3b pruned violently to 27b.
49 upvotes · 11 comments
Breaking VRAM Barrier: Qwen 3.8 27B at 262K Context with Adaptive KV-Cache Streaming on a 16GB VRAM GPU
r/LocalLLM
•
2mo ago
Breaking VRAM Barrier: Qwen 3.8 27B at 262K Context with Adaptive KV-Cache Streaming on a 16GB VRAM GPU
243 upvotes · 109 comments
Ternary Bonsai 2 27B, near top performance while fitting entirely in 8GB VRAM
r/LocalLLM
•
1mo ago
Ternary Bonsai 2 27B, near top performance while fitting entirely in 8GB VRAM
241 upvotes · 179 comments
Re: SSI new model
r/singularity
•
3mo ago
Re: SSI new model
317 upvotes · 68 comments
I tested 9 LLMs on the exact same web-dev prompt for ~8 hours — RTX 3060 12GB results (Rate the best!)
r/LocalLLaMA
•
1mo ago
I tested 9 LLMs on the exact same web-dev prompt for ~8 hours — RTX 3060 12GB results (Rate the best!)
154 upvotes · 52 comments
I got Mirai Mail!!
r/smartdoll
•
8mo ago
I got Mirai Mail!!
199 upvotes · 11 comments
New Mira selfie
r/ladytron
•
4mo ago
New Mira selfie
72 upvotes · 11 comments
Frustration with Mira’s AI
r/Mirafertility
•
18d ago
Frustration with Mira’s AI
18 upvotes · 14 comments
My 1070s in SLI have retired!
r/pcmasterrace
•
5mo ago
My 1070s in SLI have retired!
5.9K upvotes · 201 comments
Ternary Bonsai 2 (27B) just released on Hugging Face. At <6GB in size, it can even run locally in-browser on WebGPU.
r/LocalLLaMA
•
1mo ago
Ternary Bonsai 2 (27B) just released on Hugging Face. At <6GB in size, it can even run locally in-browser on WebGPU.
1.7K upvotes · 344 comments
What do you think about MoneroOcean.stream and THEIR version of XMRIG?
r/MoneroMining
•
5y ago
What do you think about MoneroOcean.stream and THEIR version of XMRIG?
14 upvotes · 15 comments
It’s too quiet. Send your favorite Mira images.
r/okaybuddydemonhunters
•
3mo ago
It’s too quiet. Send your favorite Mira images.
176 upvotes · 56 comments
28.9M LLM running on a ESP32-S3 (~9 tok/s), no cloud (open source)
r/arduino
•
3mo ago
28.9M LLM running on a ESP32-S3 (~9 tok/s), no cloud (open source)
839 upvotes · 88 comments
I'm so intrigued by the Mirai - I keep telling myself it would be a terrible decision, but it's such a nice car for $23K OTD + free fuel for 3-4 years
r/Toyota
•
4mo ago
I'm so intrigued by the Mirai - I keep telling myself it would be a terrible decision, but it's such a nice car for $23K OTD + free fuel for 3-4 years
81 upvotes · 67 comments
What is your opinion to the Mirai Guardian ?
r/starcitizen
•
2y ago
What is your opinion to the Mirai Guardian ?
699 upvotes · 285 comments
Bonsai 2 27B on a 12 GB Arc B580: 128K context, ~80-90 t/s writing code, 250+ on edits (open source, Windows build too)
r/IntelArc
•
1mo ago
Bonsai 2 27B on a 12 GB Arc B580: 128K context, ~80-90 t/s writing code, 250+ on edits (open source, Windows build too)
10 upvotes · 9 comments
Qwen3.8-27B at 262k context on a single RTX 5090, with ~24 GB VRAM usage
r/LocalLLM
•
2mo ago
Qwen3.8-27B at 262k context on a single RTX 5090, with ~24 GB VRAM usage
30 upvotes · 33 comments
New Toyota Mirai hydrogen fuel cell car review
r/electricvehicles
•
6y ago
New Toyota Mirai hydrogen fuel cell car review
7 comments
Why People use Moneroocean since everyone knows it's clone of nicehash.
r/MoneroMining
•
5y ago
Why People use Moneroocean since everyone knows it's clone of nicehash.
41 comments
Which LLM should I use with an 8 GB Nvidia RTX 4060?
r/unsloth
•
17d ago
Which LLM should I use with an 8 GB Nvidia RTX 4060?
17 upvotes · 34 comments
1-bit 27B in the browser: 25–30 tok/s on a 6 GB RTX 3060 Laptop (WebGPU, no install)
r/LocalLLaMA
•
2mo ago
1-bit 27B in the browser: 25–30 tok/s on a 6 GB RTX 3060 Laptop (WebGPU, no install)
69 upvotes · 28 comments
Mira is so easily entertained 😂
r/Hololive
•
6d ago
Mira is so easily entertained 😂
1.1K upvotes · 30 comments
Is it worth upgrading from Myvi to S70?
r/kereta
•
1mo ago
Is it worth upgrading from Myvi to S70?
51 upvotes · 87 comments
VIEW POST IN
Français
Português (Brasil)
See more
Public
Home
Popular
News
Explore
Best of Reddit
Best of Reddit in Portuguese
Best of Reddit in German
Reddit Rules
Privacy Policy
User Agreement
Your Privacy Choices
Accessibility
Reddit, Inc. © 2026. All rights reserved.

Join the most real place on the internet

 Sign in with Apple
Continue with Phone Number
Continue with Email

By continuing, you agree to our User Agreement and acknowledge that you understand the Privacy Policy.
