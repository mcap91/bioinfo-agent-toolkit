source: https://www.reddit.com/r/LocalLLM/comments/1xgqyz4/125_tokens_per_second_on_an_rtx_4070_ti_super_how/
captured: 2026-10-29
playwright: 1.64.1
chromium: 156.0.8078.4

Skip to main content
125 Tokens per Second on an RTX 4070 Ti SUPER: How I Got a Local LLM Working as a Full-Fledged Coding Agent : r/LocalLLM
Sign Up
Log In
Expand user menu
Go to LocalLLM
r/LocalLLM
•
2d ago
u/ievkz
125 Tokens per Second on an RTX 4070 Ti SUPER: How I Got a Local LLM Working as a Full-Fledged Coding Agent
Discussion

Based on statistics, among regular desktop PC users, the most common graphics card has 16 GB of video memory. According to GaugeDB surveys, such cards make up 27.21% of the market. I happen to have an NVIDIA GeForce RTX 4070 Ti SUPER with 16 GB of GDDR6X video memory, which currently costs $900. Until now, the main problem was that it was impossible to run an LLM agent on a graphics card of this class that was smart enough and fast enough. If you run a smart model like Qwen 3.8 27B (Dense architecture), you get 10-20 tokens per second. And for comfortable work with a coding agent, you need 100-150 tokens per second.

But recently I came across 2 models: Tiel-Coder-35B-A3B-GGUF-MTP (built for coding) and Cyber-Tiel-Coder-35B-A3B-GGUF-MTP (an uncensored abliterated model that doesn't refuse to write exploits or carry out active hacks on anything you ask it to). And what else is notable about them? First, they use MTP (Multi-Token Prediction), a technology that lets an LLM predict several next tokens at once instead of one, which increases inference speed by 20%. Second, they use the MoE (Mixture of Experts) architecture, which makes it possible to get the quality of a large model while performing computations for each token with only part of its parameters. Token generation speed increases by +200-450%. Third, there's Sharp Template, an optimized Chat Template (Jinja) with a system prompt that makes the LLM spend fewer tokens on reasoning and answers without losing necessary information. It cuts inference by 59%, which ultimately makes a coding agent work 2 times faster.

So, on my graphics card, I run the following versions of these models: Cyber-Tiel-Coder-35B-A3B-MTP-UD-Q2_K_XL.gguf and Tiel-Coder-35B-A3B-MTP-UD-Q2_K_XL.gguf, and the launch parameters look like this:

As a result, I get a speed of 125 tokens per second!

This is a very good start, but as you may have noticed, the context window is only 65535 tokens, which is a bit too small for agent-assisted coding. That's why I use 3 approaches.

First, I don't use heavy coding agents, such as Codex or Claude Code, because right out of the box, with the slightest interaction, they consume 10 to 14 thousand tokens for the system prompt and so on. That is, 15-20% of the context is taken up immediately, and local models also lose context more easily, while such large system instructions distract them even more from the task the user describes. I use the Pi coding agent. It requires 1.5 thousand tokens to run, which is 10 times less than Codex or Claude Code, and this noticeably affects the capabilities and quality of work on the user's local GPU. Here's Pi's configuration file for adding these 2 models that will run on your GPU: ~/.pi/agent/models.json

{
  "providers": {
    "lmstudio": {
      "baseUrl": "http://YOUR_LOCAL_IP:1234/v1",
      "api": "openai-completions",
      "apiKey": "lmstudio",
      "models": [
        { "id": "peculiar-ragdoll/tiel-coder-35b-a3b-mtp@q2_k_xl" ,
          "contextWindow": 65536,
          "maxTokens": 32768,
          "input": ["text", "image"]
       },
        { "id": "peculiar-ragdoll/cyber-tiel-coder-35b-a3b-mtp" ,
          "contextWindow": 65536,
          "maxTokens": 32768,
          "input": ["text", "image"]
       }
     ]
   }
  }
}

Second, I never ask the coding agent to try to make a large code change directly. I start a new session with the "/new" command and ask the coding agent to write a plan.md file describing what needs to be changed in the code to implement the task I gave it. That way, the 65535-token context window is enough for me, since, essentially, I split the task into two phases: planning and implementation. Then, if the task isn't too large, after creating plan.md I clear the coding agent's context window with the "/new" command and ask it to make the code changes based on plan.md and record the results in plan.md when it's done.

Third, for very large plan.md files, I use my SKILL called subtask4llm-pi, which breaks a task into no more than 10 subtasks and runs them sequentially. Each subtask runs in a separate coding agent instance, which receives only what is relevant to that subtask, so its 65535-token context window is almost empty. The subtask results flow into the main Pi instance without overflowing its main context window, which handles coordination, planning, and checking. You can install the skill with the command "npx skills add https://github.com/evgenyigumnov/subtask4llm --skill subtask4llm-pi". There is also a version for Codex, subtask4llm-codex. By the way, if anyone wants to add support for Claude or help in some other way, send pull requests: https://github.com/evgenyigumnov/subtask4llm

Fourth, I use the approach of Robert Martin, author of "Clean Code", who recently said that he had stopped reading code generated by coding agents. He managed that by putting LLMs in a tight box. Using these constraints, you can offset the fact that the models in use are heavily compressed to the UD-Q2_K_XL level. That is, they make more mistakes than 4-, 6-, or 8-bit models. To create these constraints, I suggest using AGENTS.md, which controls the size of every file being created, makes you write unit tests, clearly spells out decomposition and responsibility in the code, and ultimately requires running the tests. Since we don't pay for every token on a local GPU, we can easily afford a couple of extra iterations while the model sees its mistakes and fixes them. Here is a basic example of an AGENTS.md file for this:

# AGENTS.md

## Code Writing Rules

- Maximum size of one code file: 300-500 lines. If a file gets bigger, break it down.
- The main principle: one cohesive responsibility per module.
- Don't sacrifice logical cohesion or code readability to comply with arbitrary line-count limits.
- Split files based on their functional purpose, not just their line count.
- All functions must be covered by unit tests.
- When adding or changing functionality, or fixing bugs, always add the corresponding unit tests.

## Checks Before Submission

- All tests and the build must pass without errors or warnings.
- Don't weaken checks or delete tests just to get them to pass.

## Main Rule

**Never commit changes without a direct request from the user.**

In the end, we got a synergistic effect, or you could even call it emergence. MTP + Quantization + MoE + AGENTS.md (Clean Code) + Sharp Template + Pi agent + subtask4llm skill + plan.md = a workflow with a coding agent, running on your home graphics card. Now your source code is under your control, and big corporations won't get their dirty paws on it! And you can also run an abliterated model for White Hat hacking without putting up with constant refusals from proprietary models when you're trying to hack something.

Read more
Share
Roblox
•
Ad
The best sports games are played together. Team up with friends and claim game-winning victories.
Play Now
roblox.com
Collapse video player
Sort by:
Comments Section
Any_Flounder8768
•
2d ago

With 96 GB of RAM you can skip IQ3_XXS and go straight to the GSQ-RCO IQ3_S: on my 12 GB 4070 Ti + 64 GB it peaks at ~51 GiB RAM and does ~2,400 t/s prefill / ~50 t/s decode at 16K, and it's closer to BF16 (KLD 0.087 vs 0.136 for IQ3_XXS). Keep the n-gram table on a fast NVMe. Your 16 GB card will do better than mine.

ievkz
•
2d ago

wow! cool!

Any_Flounder8768
•
1d ago

For a massive context window, try https://github.com/lastreload/mnemonic-proxy — but shhh! 🤫 Don't tell anyone! My AI says I'm not allowed to share it because it's spam! 😂

jessepence
•
2d ago

I'm glad you're proud of it, but I find it hard to believe that a 2 bit quant of a 35b model would lead to anything other than frustration.

Gold-Produce9591
•
2d ago

yeah, with 16gb vram, op should be running Q4 or Q5 at least, they would get much better results

ievkz
•
2d ago

I just heard about Strata, which lets you run Qwen3.8-Flash-Next on a GPU with only 16 GB of VRAM by offloading the rest to system RAM and SSD. I have 96 GB of RAM, so I'm about to give it a try. Depending on the quantization, it needs roughly 35–50 GB of RAM and around 80 GB of SSD space, including a 29 GB lookup table that stays on disk. People are reporting around 70 tokens per second. And this is a completely different class of model 125B parameters. I'm hoping it'll be noticeably smarter at coding.

11 more replies
Zaic
•
1d ago

yep same card I am able to run 3.8 coder next at q3s at 140k context with decent 40-60tks. would most likely come up with 3x better solution at 3x shorter time compared to ops setup.

notheresnolight
•
1d ago

apparently its enough to generate a 2 page word salad for a reddit post

No_Total_423
•
2d ago

You shouldn't be obsessed with tps while you can run the same model with much better quality. You're just sacrificing so much quality. You can even run QFN if you have enough ram.

ievkz
•
2d ago

Do you mean Niko1221/Strata project on github?

No_Total_423
•
2d ago

Yes. Also for other moe models such as Tiel you can use PolyStrata with much more tps. https://github.com/VecSzn/PolyStrata

2 more replies
u/Smartwool
•
Ad
Nothing hits like nature. Get out there and run wild in the cold weather activewear collection from Smartwool. 
Shop Now
smartwool.com
smashcat666
•
1d ago

I find it VERY hard to believe that 27% of PC users have a 16GB GPU. Even amongst gamers (who would tend to focus most on GPU performance) the average is 8-12GB. Your average office worker, or home-worker isn't going to be running an RTX GPU for spreadsheets and web browsing.

ievkz
•
1d ago

Could GaugeDB be referring specifically to gamers, rather than everyone in general?

Gobblerpl
•
19h ago

Don't tell him about strata

ievkz
•
19h ago

I already know

subszeroo
•
17h ago

I lost you at Q2

ievkz
•
15h ago

lol

MaxP69420
•
1d ago

is it okay if i borrow post to ask, when people say they load apart of a model into vram and offload it to ram for still decent speeds but when i do it the whole model just only goes into my system ram. What am i doing wrong?

pic for example i tried making the gpu only take like 14GB and the rest offload it but when i run the model it dosent use the gpu.

johnzadok
•
2d ago

Since you have an nvidia card you can try the llama kv streaming fork to get more ctx.

halfercode
•
2d ago

Props to you for having the patience to wade through this stuff. I'm still on Claude Code, and would be happy to swap to remote (non-local) open-weight models, but I have a dim view of the performance/behaviour of anything other than frontier, closed-weight models for now.

I tried GLM-5.3 remotely and it ate my OCG quota in an hour. I tried GPT-6-something and its reasoning was just poor. I've had a rec for DeepSeek v4.1 but finding the energy to give a new model a proper try is hard when a cheap closed model works OOTB.

ansibleloop
•
1d ago

You can use Claude to build a useful local setup

Thinking about it, I could do with a skill that creates new docker deployments as my Ansible config - that way I wouldn't need a powerful model

Outrageous_Band9708
•
6h ago

aaaaaand... its Q2

niugnep24
•
5h ago

I'd rather have 20tps of solid coding than 100tps of slop... I've never heard of "Tiel Coder" but 35B-A3B makes it look like a finetune of Qwen3.6...

Actually looking it up, it's a quant of "Orinth 1.5" which they claim is "developed on top of Qwen3.5 and Gemma 4" which is a strange statement as those are different architectures. Seems like it's Qwen3.5 with extra RL training and maybe some distillation. Can't imagine this would actually out-perform 3.8, even with its suspiciously high benchmark scores....

kfallah15
•
2h ago

Nicely done! Could be cool to build a feedback system and fine-tune the model locally too.

More posts you may like
Related posts
4070 super outperforming 85% of 4070Ti's!!
r/overclocking
•
5d ago
4070 super outperforming 85% of 4070Ti's!!
23 upvotes · 20 comments
Nintendo_America
•
Ad
Grab your controller & step up to the net in Table Tennis! Nintendo Switch Sports Resort is available now on the Nintendo Switch 2 system!
nintendo.com
Shop Now
Thoughts of buying a 4070 ti super in 2026?
r/nvidia
•
1mo ago
Thoughts of buying a 4070 ti super in 2026?
13 upvotes · 55 comments
Repasted my RTX 4070 Ti Super after 1.5 years because it sounded like a jet engine. Results with Duronaut are insane!
r/pcmasterrace
•
4mo ago
Repasted my RTX 4070 Ti Super after 1.5 years because it sounded like a jet engine. Results with Duronaut are insane!
54 upvotes · 55 comments
What I learned running a local coding agent on an RTX 4070 Super
r/LocalLLM
•
5mo ago
What I learned running a local coding agent on an RTX 4070 Super
8 upvotes · 3 comments
Which local LLMs can I realistically run on 14700K + 128GB RAM + RTX 4070 Super 12GB? Mainly for Hermes Agentic Coding
r/LocalLLM
•
1mo ago
Which local LLMs can I realistically run on 14700K + 128GB RAM + RTX 4070 Super 12GB? Mainly for Hermes Agentic Coding
10 upvotes · 11 comments
Worth Upgrading the RTX 4070 (Non Ti/Super) in 2026?
r/nvidia
•
3mo ago
Worth Upgrading the RTX 4070 (Non Ti/Super) in 2026?
6 upvotes · 95 comments
Best Local Models for RTX 4050 6GB?
r/LocalLLM
•
13d ago
Best Local Models for RTX 4050 6GB?
4 upvotes · 18 comments
WTB: RTX 4070 Super / 4070 Ti - Kolkata
r/IndianPCHardware
•
2mo ago
WTB: RTX 4070 Super / 4070 Ti - Kolkata
8 upvotes · 42 comments
PTM7950 on RTX 4070TI Super
r/nvidia
•
4mo ago
PTM7950 on RTX 4070TI Super
26 upvotes · 16 comments
4070ti Super pros & cons
r/gpu
•
2mo ago
4070ti Super pros & cons
57 upvotes · 51 comments
Happy with 20-30 Tokens Per Second
r/LocalLLM
•
8d ago
Happy with 20-30 Tokens Per Second
28 upvotes · 65 comments
USED 4070Ti Super or NEW RTX 5070?
r/nvidia
•
1y ago
USED 4070Ti Super or NEW RTX 5070?
3 upvotes · 31 comments
[GPU] (Grade A Refurbished) MSI GeForce RTX 4070 Ti SUPER VENTUS 3X Black OC 16GB GDDR6X - $749
r/buildapcsales
•
20d ago
[GPU] (Grade A Refurbished) MSI GeForce RTX 4070 Ti SUPER VENTUS 3X Black OC 16GB GDDR6X - $749
112 upvotes · 62 comments
Worth Upgrading the RTX 4070 (Non Ti/Super) in 2026?
r/buildapc
•
3mo ago
Worth Upgrading the RTX 4070 (Non Ti/Super) in 2026?
6 upvotes · 33 comments
Rtx 4070 ti super for 4k
r/nvidia
•
2mo ago
Rtx 4070 ti super for 4k
8 upvotes · 22 comments
Thinking of purchasing this 4070 Ti super for $550 do you guys think that’s a reasonable price? Going to upgrade my 3060 Ti to it.
r/PcBuild
•
8mo ago
Thinking of purchasing this 4070 Ti super for $550 do you guys think that’s a reasonable price? Going to upgrade my 3060 Ti to it.
60 upvotes · 142 comments
Just got my New Rtx 4070 Super Ti
r/pcmasterrace
•
1mo ago
Just got my New Rtx 4070 Super Ti
76 upvotes · 26 comments
Bro spend 919K Token for nothing ☠️☠️☠️
r/LocalLLM
•
6d ago
Bro spend 919K Token for nothing ☠️☠️☠️
94 upvotes · 71 comments
RTX 4070 Super in 2025 | Is It Still Worth for 1440P Gaming | 20 Latest AAA Games Tested | RT On
r/OptimizedGaming
•
10mo ago
RTX 4070 Super in 2025 | Is It Still Worth for 1440P Gaming | 20 Latest AAA Games Tested | RT On
8 comments
Is the RTX 4070 Ti Still Good for 1440p Gaming?
r/pcmasterrace
•
9mo ago
Is the RTX 4070 Ti Still Good for 1440p Gaming?
3 upvotes · 27 comments
Shout out to my 4070Ti SUPER gang
r/nvidia
•
4mo ago
Shout out to my 4070Ti SUPER gang
135 upvotes · 33 comments
My $350 RTX 4070 Ti actually arrived... but I'm lowkey terrified to plug it in.
r/gpu
•
3mo ago
My $350 RTX 4070 Ti actually arrived... but I'm lowkey terrified to plug it in.
13 upvotes · 85 comments
RTX 4070 Ti Super quietly became the GTX 1080 Ti of the 2020s, and Nvidia couldn't beat its own offering
r/TechHardware
•
4mo ago
RTX 4070 Ti Super quietly became the GTX 1080 Ti of the 2020s, and Nvidia couldn't beat its own offering
119 upvotes · 59 comments
I have 4090 and 5070ti
r/LocalLLM
•
1mo ago
I have 4090 and 5070ti
4 upvotes · 18 comments
Is it worth to buy this 4070Ti super for $630??
r/gpu
•
5mo ago
Is it worth to buy this 4070Ti super for $630??
92 upvotes · 267 comments
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
