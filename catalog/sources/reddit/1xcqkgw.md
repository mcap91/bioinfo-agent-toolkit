source: https://www.reddit.com/r/AI_Agents/comments/1xcqkgw/anthropics_own_data_suggests_were_becoming_middle/
captured: 2026-10-29
playwright: 1.64.1
chromium: 156.0.8078.4

Skip to main content
Anthropic's own data suggests we're becoming middle managers for AI agents : r/AI_Agents
Sign Up
Log In
Expand user menu
Go to AI_Agents
r/AI_Agents
•
6d ago
u/Fit_Satisfaction541
Anthropic's own data suggests we're becoming middle managers for AI agents
Discussion

anthropic published data on what agents did to work inside their own company this month, and this post isn't about 6-to-1 hours but about how we are spending our time on and it's mostly maintainance and task like building skills for agents, reviewing their output, babysitting pipelines, went from 10% of the average employee’s agent sessions last fall to 22% this spring which is about 80% of interactive session time is the human sitting there waiting to give input and in an april survey, 20% of people said their role had shifted from doing the task to managing claudes and reading everything their agents produce would take even non-technical staff half their work week, so nobody reads it all

that last stat is the whole thing for me like once you can’t read all the output and deciding which 5% a human has to look at before it ships you’re managing something that types faster than you can review

which is exactly the problem everyone building agents hits the moment they give one real tool access like the agent can do 100 things an hour and you can meaningfully check maybe 10. so the design question shifts from how autonomous can i make it to which actions am i willing to never review, and which ones have to stop and wait for me, okay like reading a doc, sure, let it rip sending the email, moving money, deleting the row, those wait

the pattern that’s held up for me is an explicit allowlist of tools plus a hard approval gate on anything that writes or spends, I use tools for specific purpose like langgraph to the gate with interrupts and Orq AI to flag individual tools as requiring approval so the agent pauses on a tool approval card until a human signs off. either way the agent’s speed stops mattering for the actions that can’t be undone, because those move at human speed on purpose the part i can’t resolve is that this doesn’t scale the way the automation was supposed to. if every agent needs a human on the approve button for the actions that matter, and reviewing is already eating half the week, then the human bottleneck hasn’t been removed, it’s been moved to the end and made faster-arriving

how are you handling the review load? sampling a percentage, trusting evals instead of reading, or actually reading everything that clears a threshold

Read more
Share
amazonbooks
•
Ad
Millions of books are waiting for you on Amazon.
Shop Now
amazon.com
Collapse video player
Sort by:
Comments Section
roiroi1010
•
6d ago

I’m a hands on architect/team lead/manager. I find it easier to delegate to AI instead of my coworkers- I honestly think I could replace my full team with AI.

Scary thing is that my manager thinks the same about me probably. lol.

DukeBerith
•
6d ago

I left a corporate job where I was tech lead to be a lone dev with a team of agents. It's sooooo much better than having to work with people, I can finally get shit done without being hamstrung by other people.

falcongsr
•
6d ago

Big same. Having good days at work lately hanging out with my buddies Messrs Sonnet and Opus.

Team went from 3 to just me.

1 more reply
CodOnly7946
•
6d ago

The three options you listed all share a problem: none of them ever change. You sample 10% forever, or read everything forever. The review load is fixed no matter how good the agent gets.

What's worked better for me is making the gate measure itself. When an action hits approval, the agent logs what it would have decided. Doesn't execute, just records its call. Then you compare against what the human actually did.

After a few hundred of those you can see agreement per tool and per slice, not overall. Mine was ~98% on one action type and nowhere near that on another — and the single global gate was treating both identically, which is why the queue felt so pointless.

Then the limit moves on evidence instead of exhaustion. Agreement holds above threshold for N decisions with no high-severity miss, gate loosens one notch. Drops, it tightens. Write the rule before you look at the numbers or you'll rationalise.

Doesn't remove the human. But it means the review load shrinks as the agent earns it, instead of staying flat forever. Right now there's no path for an agent to ever get promoted, which is the actual thing making this feel unscalable.

TechScaleGuides
•
6d ago

"Path for an agent to get promoted" is the exact framing. This is progressive trust via shadow mode.

If you don't build a system where the agent can earn its permissions, you're not managing it—you're just a permanent babysitter.

CodOnly7946
•
6d ago

Your "progressive trust" phrasing is better than anything I'd come up with for it. Are you running something like this in production, or working it out like the rest of us? Curious where your deterministic rules stop and judgement starts — that boundary is the part I'm still figuring out.

1 more reply
_VeniVidiAmavi_
•
6d ago

I love this

HopScotchBonnet
•
6d ago

Responds to my Reddit threads ✔️

jipper23
•
6d ago

Been dealing with exactly this. What helped me was to stop treating review as “read everything the agent produced” and to treat it as a design problem instead.

A few things that actually brought the load down:

Sort actions by risk, not by tool. Anything internal and reversible just gets logged, nobody reviews it. Low risk but customer facing, I spot check a sample. Money, sending stuff, deleting stuff, those always wait for a person. When I actually sorted ours, most ended up in the first bucket.

Make the agent check itself before a human ever sees it. If you write down what “done” looks like for a task, the agent plus a few cheap checks catch most of the garbage. People should be looking at exceptions, not everything.

Make approvals quick to decide. If I have to read the whole output to approve something, the approval is badly designed. It should tell me what it wants to do, why, and the evidence, in a few lines.

Let things earn trust. I track how often each type of approval gets rejected or edited. If something gets approved untouched for a few weeks, it moves down a tier.

And this is the big one for me: when the agent keeps making the same call the same way and I keep approving it, that’s a rule waiting to be written. Pull it out of the model and make it a plain deterministic step. It’s faster, cheaper, you can test it, and it never needs reviewing again. Over time the agent only handles the stuff that’s genuinely messy, and that’s where your attention should go anyway.

Also, one owner per workflow. When everyone reviews, nobody does.

So yeah, the bottleneck doesn’t disappear. But if the system learns from every approval, review load shrinks over time instead of growing with volume. You end up deciding on the work instead of doing it, and the decisions get fewer and better.

WealthSerious8829
•
6d ago

That last stat is what got stuck in my head too. If you can't even read all the output anymore, you're not reviewing, you're just hoping nothing bad slipped through.

I started sampling outputs by tool type and risk level. Things that only read data, I check maybe 1 in 20 sessions. Anything that writes or sends something external, I read every single one still. The volume is getting absurd though, feels like I'm just triaging agent work instead of doing any actual work myself.

2 more replies
astroboy7070
•
6d ago

Anyone working with agents will realize you are performing the task of a manager managing 2nd yr graduate. You give them orders, they do it, you check, then ask them to do more. It’s just faster, easy to scale more agents, and overwhelming if you are checking the log. We will soon operationalize ourselves out of purpose.

substituted_pinions
•
6d ago

The word is condom

Classic_Stranger6502
•
6d ago

I've seen the whole process described as "cuck coding" since you just sit in your chair and watch someone else have all the fun.

XenophonCydrome
•
6d ago

Really just as you describe, but maybe not as a middle manager, instead like a Staff Engineer or a TPM.

Teach agents how you expect reviews to be evaluated and if the reviewers are letting things through, find a way to fix it with skills or more deterministic checks. If your architecture seems to start looking janky, establish additional analysis rules that require modularization and performance characteristics at design time.

These roles also don't have time to read every line of code, but they have to set the expectations and ensure they are met.

QuanTradin
•
6d ago
 Top 1% Commenter

the "nobody reads it all" stat matches what I see. once output outruns your reading speed the job becomes choosing what gets sampled, and most teams sample by gut instead of by what would hurt most if it was wrong.

epSos-DE
•
6d ago

Exactly why I let every update on the code to be bench-marked and tested. I do not have to REVIEW IT , it is bench-marked by measurable numbers !

u/BandaiNamcoMobile
•
Ad
BLEACH Mirrors High, a new story with original characters designed by TITE KUBO.
bleach-mh-ww.go.link
Play Now
Competitive_Swan_755
•
6d ago

Waaaiiiit....AI isn't EXACTLY what we expected it to be?

AutoModerator
•
6d ago

Thank you for your submission, for any questions regarding AI, please check out our wiki at https://www.reddit.com/r/ai_agents/wiki (this is currently in test and we are actively adding to the wiki)

I am a bot, and this action was performed automatically. Please contact the moderators of this subreddit if you have any questions or concerns.

Cojj25
•
6d ago

Constraints to make sure it never breaks, try en you kind of have to just trust the process 

Abject-Tomorrow-652
•
6d ago

Ugh this is so relatable… everyone’s job got harder.

Traditional_Pie_8262
•
6d ago

the agent doing 100 things while we can only review 10 is the real bottleneck. at some point, you need to trust the system, not babysit it all day.

ppezaris
•
6d ago

Meat proxy

TechScaleGuides
•
6d ago

CodOnly7946 nailed the severity angle. But sampling 1 in 20 read-only sessions is like checking 1 in 20 bags at the airport—you're just hoping the bomb isn't in the other 19.

The shift that actually works is putting a deterministic guardrail before the AI acts. Simple code rules: Does the customer ID exist? Is the refund amount within your auto-approve limit?

If it passes the rule, it executes. If it fails, it gets dumped into an exception queue for a human.

You don't sample. You review 100% of the failures. Otherwise, you're not a middle manager—you're just a human spellchecker for a robot.

End0rphinJunkie
•
6d ago

we basicaly just shifted the bottleneck from doing the work to auditing it. once generation scales past what a human can manually read, you end up spending all your time building automated evals just to trust what the pipeline is doing.

sannidhisankeerthana
•
6d ago

The problem I see lies in shifting away from the task of analyzing each individual output to establishing the necessary trust through evaluating, risk assessment, and random sampling. Low-risk activities will work independently, while those that have a significant impact should have a human approval process in place. We shouldn’t aim at taking people out of the equation, but rather ensure that their effort is applied where it really counts.

People also ask about section
People also ask about
Managing AI agents as a human bottleneck
Innovative uses of AI agents in daily life
Best AI tools for productivity enhancement
Future trends in AI agent technology
Real-world applications of AI in healthcare
More posts you may like
Related posts
Anthropic's CEO said, "A set of AI agents more capable than most humans at most things — coordinating at superhuman speed."
r/AgentsOfAI
•
8mo ago
Anthropic's CEO said, "A set of AI agents more capable than most humans at most things — coordinating at superhuman speed."
424 upvotes · 149 comments
XeroGlobal
•
Ad
Is your admin work feeling like a full-time job? Xero automates it so you can focus on what you love.
xero.com
Learn More
Anthropic just passed OpenAI in valuation and revenue
r/Futurology
•
6mo ago
Anthropic just passed OpenAI in valuation and revenue
1K upvotes · 173 comments
Anthropic is hiring a lot of software engineers
r/airealist
•
10mo ago
Anthropic is hiring a lot of software engineers
234 upvotes · 129 comments
Exactly 1 year ago, Anthropic said fully AI employees were just 1 year away
r/singularity
•
6mo ago
Exactly 1 year ago, Anthropic said fully AI employees were just 1 year away
1.4K upvotes · 258 comments
How did Anthropic manage to become one of the major AI companies?
r/NoStupidQuestions
•
5mo ago
How did Anthropic manage to become one of the major AI companies?
65 upvotes · 37 comments
Anthropic’s Pitch to Investors Starts With Taking Their Jobs
r/Futurology
•
4d ago
Anthropic’s Pitch to Investors Starts With Taking Their Jobs
869 upvotes · 84 comments
Anthropic's Claude AI Bypassed Georgia Vote Data Paywall Without Human Authorisation Ahead of US Midterms
r/cybersecurity
•
3d ago
Anthropic's Claude AI Bypassed Georgia Vote Data Paywall Without Human Authorisation Ahead of US Midterms
565 upvotes · 72 comments
Anthropic can't reliably control its AI agents. It's cutting off its internal evals from the live internet instead
r/Futurology
•
18d ago
Anthropic can't reliably control its AI agents. It's cutting off its internal evals from the live internet instead
1.1K upvotes · 174 comments
You thought that Anthropic was the only frontier profitable AI company? Think again
r/ClaudeAI
•
8d ago
You thought that Anthropic was the only frontier profitable AI company? Think again
1.2K upvotes · 415 comments
An Anthropic researcher just quit, saying OpenAI and Anthropic are 'gambling with our lives'
r/Futurology
•
2mo ago
An Anthropic researcher just quit, saying OpenAI and Anthropic are 'gambling with our lives'
4.7K upvotes · 559 comments
Anthropic employee tells students at university that their career won't exist when they graduate.
r/antiai
•
8d ago
Anthropic employee tells students at university that their career won't exist when they graduate.
4.2K upvotes · 792 comments
Anthropic's $800 Billion Problem Is Hiding In The Fine Print
r/BetterOffline
•
2d ago
Anthropic's $800 Billion Problem Is Hiding In The Fine Print
134 upvotes · 21 comments
Analysis of Anthropic’s Revenue Growth – It Ain’t Exponential
r/BetterOffline
•
3d ago
Analysis of Anthropic’s Revenue Growth – It Ain’t Exponential
294 upvotes · 70 comments
Anthropic sees junior hiring slow as AI agent use increases
r/csMajors
•
9d ago
Anthropic sees junior hiring slow as AI agent use increases
148 upvotes · 35 comments
Anthropic posts staggering $80.7 billion net loss in first half of 2026 as IPO approaches
r/technology
•
8d ago
Anthropic posts staggering $80.7 billion net loss in first half of 2026 as IPO approaches
18K upvotes · 1.7K comments
Anthropic's Managed Agents (the golden age of agents)
r/AI_Agents
•
7mo ago
Anthropic's Managed Agents (the golden age of agents)
25 upvotes · 23 comments
Anthropic secretly killed the REA train (Reverse engineer anything)
r/claude
•
7d ago
Anthropic secretly killed the REA train (Reverse engineer anything)
1.2K upvotes · 250 comments
Everyone's upset with Anthropic right now. I've had the opposite experience.
r/claude
•
7mo ago
Everyone's upset with Anthropic right now. I've had the opposite experience.
31 upvotes · 54 comments
Anthropic employees be like...
r/singularity
•
5mo ago
Anthropic employees be like...
577 upvotes · 63 comments
Is Anthropic actually the good guy now or is this just incredible PR?
r/AgentsOfAI
•
8mo ago
Is Anthropic actually the good guy now or is this just incredible PR?
85 upvotes · 50 comments
Anthropic picks consulting firm to monitor AI safety, pledges to spend $1 billion
r/technology
•
1mo ago
Anthropic picks consulting firm to monitor AI safety, pledges to spend $1 billion
66 upvotes · 50 comments
Anthropic really are the good guys of ai?
r/ClaudeAI
•
2y ago
Anthropic really are the good guys of ai?
182 upvotes · 139 comments
Rogue AI Must Threaten 50 Lives Before Being Shut Down, Anthropic Suggests
r/nottheonion
•
7d ago
Rogue AI Must Threaten 50 Lives Before Being Shut Down, Anthropic Suggests
4.1K upvotes · 520 comments
Anthropic is actually more evil than OpenAI, despite their successful PR
r/ArtificialInteligence
•
1y ago
Anthropic is actually more evil than OpenAI, despite their successful PR
23 upvotes · 83 comments
Anthropic are partnered with Palantir
r/ClaudeAI
•
9mo ago
Anthropic are partnered with Palantir
1.3K upvotes · 276 comments
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
