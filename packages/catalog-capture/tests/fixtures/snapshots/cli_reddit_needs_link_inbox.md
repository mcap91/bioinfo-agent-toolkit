```text
source: https://www.reddit.com/r/LocalLLaMA/comments/1x9gfnb/google_open_sources_harness2_for_self_improving/
•
8d ago
u/chemist_slime
Google Open Sources Harness2 for Self Improving AI Agents
Resources

Google just released Harness2 as open source. It turns any AI harness into a system that improves itself over time.

A harness is everything around the model. System prompt, tools, memory, skills, and subagents. Normally a person designs it once and the agent uses that fixed setup for every new task.

With Harness2 the agent itself refines the harness for each task. It proposes changes, runs a few candidate versions, and picks a better one by comparing how they perform. No correct answers or graders are needed. The model weights stay the same.

What it learns on one task carries over to the next. After finishing a task it saves the improved harness and useful lessons so future edits start smarter instead of from scratch.

Google tested it with Gemini 3.5 Flash and GLM-5 on legal, office, and professional work benchmarks. Even one round of edits beat the original harnesses. More rounds pushed scores higher.

GitHub https://github.com/google-research/harness2

Read more
WithoutReason1729
•
8d ago
•
Edited 5d ago

Your post is getting popular and we just featured it on our Discord! Come check it out!

You've also been given a special flair for your contribution. We appreciate your post!

Stylome classified this post's text as human-written. View analysis

I am a bot and this action was performed automatically.

abhi91
•
8d ago

This is great in theory. Poetiq proved it makes benchmarks essentially useless as the harness can "overfit" to the task. Repetitive tasks like customer service are now exceptional for enterprise

Ylsid
•
7d ago
 Top 1% Commenter

But not for customers!

5 more replies
9 more replies
CoolConfusion434
•
8d ago

To paraphrase Mr Krabs: I got a bad feeling in the pit of me context.

All that "self-refinement" has to go somewhere, and that will be right into context. I'm sure it won't be an issue to the 1M context of cloud guys but us locals might be squeezed a little.

Other than that, glad to see another open-source harness, especially from giants like Google.

NineThreeTilNow
•
8d ago
 Top 1% Commenter

All that "self-refinement" has to go somewhere, and that will be right into context.

It runs parallel agents for this purpose. So really the self refinement comes from examining the tasks, seeing where the harness fell short, and then improving on the harness.

Did it need a new tool call? A better explanation of the tool call? Etc.

That will mildly bloat context but harnesses do this already. It's trying to find how it can improve the harness.

Will it increase total context? Probably, but not substantially over the existing harness.

FaceDeer
•
8d ago

It'd be changing the context, but not necessarily growing the context. Indeed, I expect part of its mandate would be to trim redundant or unnecessary stuff from it.

BannedGoNext
•
8d ago
 Top 1% Poster

Wouldn't that be like what the Hermes agent does?

1 more reply
typical-predditor
•
8d ago

I still don't trust LLMs to understand what is redundant or unnecessary. Or even what is, ahem, load bearing and necessary.

4 more replies
1 more reply
tossit97531
•
8d ago

I don't understand how this is any different than any other harness when you give an agent access to source, and I don't know why you wouldn't do that. I bolted on a whole persistent-session web UI on top of a harness core and ditched the stock CLI interface. I don't know how far I've strayed from upstream because I don't care, it's far more useful than upstream will ever be now (especially since the project kind of died).

4 more replies
catinterpreter
•
8d ago

It doesn't take much to stash the odd sentence on an SSD that encapsulates some key, formative insight. Very few words can have an immense impact.

6 more replies
u/adobe
•
Ad
Unleash your potential with Premiere, Illustrator, Photoshop & 20+ apps in Creative Cloud Pro
Learn More
adobe.com
acoolglassofwater
•
8d ago

Could someone with high LLM expertise (not just trust-me-bro) explain the significance of this? I get the general idea, but the comment section is always highly opinionated on self-improving agents. Is this release just a nothing-burger or does it represent something interesting and significant?

itsmebenji69
•
8d ago
•
Edited 8d ago

I’d say it’s mid interesting

The harness can limit the agent in tasks. So perpetually modifying the harness to make it better suited to a task is useful, it removes that ceiling (if harness was limiting the task, it won’t anymore after a few rounds of improvement).

The obvious problem is that better suited to task A may degrade performance in task B. Basically over fitting.

Simple example: task A is to compute x+y and task B is to compute x times y.

Harness version one just gives you x and y, and the llm has to do the calculation. After a few rounds of improvement on task A, the harness only gives the model x+y, and the llm just reads that result. But now it doesn’t know x and y. So it will be great at adding them, perfect even, it will be right every time. Because it will know the accurate result directly. For task A alone, this is a great harness, it ensures that the model will never be wrong about the result of x+y or hallucinate or whatever.

But now on task b, if you want to know x*y, say that’s 2 times 3, the harness will only show the model 5 (2+3, x+y), so it will miserably fail at giving you the multiplication result. It simply won’t be able to know what x and y were, so it won’t know what to do with the result of the A optimized harness. It will just see 5, and from that it can’t infer what x and y are, or infer what x times y is.

And vice versa if you start optimizing on task b

9 more replies
FoxSideOfTheMoon
•
8d ago

I can find no practical use for this FWIW

1 more reply
9 more replies
Paradigmind
•
8d ago

So if we use this on Hermes we get Inception?

1 more reply
HotAverage1749
•
8d ago

Used Qwen to make an extension for pi

1 more reply
Holiday_Point_603
•
8d ago
 Top 1% Commenter

Interesting that google uses models that are like half a year old to show off their new software lol

Spara-Extreme
•
8d ago

Google is a massive company so the team that did this isn’t the team that’s working on Gemini 4

5 more replies
-p-e-w-
•
8d ago
 Top 1% Commenter

Research takes time to prepare for publication. These experiments were likely conducted many months ago.

u/novasourcerenal
•
Ad
TIL: Novasource® Renal comes in Strawberry, Vanilla AND Café Mocha flavors. Try now at Amazon!
Learn More
amazon.com
_-mg-_
•
8d ago

anyone actually tried using this?

suhive
•
8d ago

Harness Self-benchmaxxxing lol

SnooPuppers7882
•
5d ago

Been playing with this and it's promising...

Have a 6 multitask corpus to calibrate Qwen 3.8 flash next as a coding worker...you need to know what you can reliably expect it to be able to do, everytime, so a coordinator model with a capabilities lookup index knows exactly how to split up a task assignment between a local model and a cheap, more capable cloud model.

Baseline (10 repeat runs), QFN would fail all tasks 100% of the time except task 5 (20% pass rate), with individual steps within a task (wide array of coding taxonomy chained in different orders and degrees of difficulty) solved around 50-60%.

After 3 loops under the methodology in Google's paper (Harness² is a LOOP orchestration, NOT an actual harness), Task 1 got 10%, task 3 10%, task 4 20%, task 5 100%, an average total steps increased to the 65 to 72% solve range.

Currently in runs of a modified methodology:

For one arm, QFN goes through claude code as the tester, sol 6.1 max reviews as a coach, opus 5.5 high reviews the coach recommendations to check bias gaps before auto-implementation of changes to the harness configuration. Arm 2 does the same except Opus is the coach and sol is the reviewer...tests are clones of the original t1 through t6 tests but with altered variables, files, and sequencing to maintain difficulty but not bias improvements to one benchmark.

Going through 10 runs each with both arms in parallel, then amalgamating the best changes that yielded the best scores, then the final trained setup run 10 times on the original test again.

Should take 2 days roughly for the results, I'll report back with detailed findings.

2 more replies
Limp_Classroom_2645
•
8d ago

Self refinements mean loss of consistency and control

TemporaryInk
•
8d ago

That’s great and all, but is anyone going to point out the prolific use of Comic Sans in the graphic? 😂

2 more replies
Dany0
•
8d ago
 Top 1% Commenter

Soooo autoresearch again

...

David23G1
•
8d ago

What the different from other harness e.g herems,openclaw,pi

3 more replies
```
⚠ capture-failed https://www.reddit.com/r/AI_Agents/s/forcedFailure1 — net::ERR_NAME_NOT_RESOLVED (forced, snapshot test)
