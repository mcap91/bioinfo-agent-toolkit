reel: https://www.instagram.com/reel/Dd2UVU_sVNH/
captured: 2026-10-29
yt-dlp: 2026.10.26
ffmpeg: 7.0.2-static
faster-whisper: 1.2.1
ctranslate2: 4.8.4
claude: 2.1.281 (Claude Code)

## Caption

On September 23, Stanford and NVIDIA released CLM-8B, a Contrastive Language Model. Like Jev, it doesn’t generate text. It turns the situation and each possible action into vectors and picks the closest match. Under the hood it is a frozen Qwen3-8B with a small 20M-parameter layer trained on top.

The speed comes from caching. When the list of actions stays the same, like tools in an agent or buttons in a game, CLM encodes them once and only re-reads the new state. The team reports up to 9x faster than Jev on computer-use, gaming and tool-calling, and 13x at around 1,000 options.

On coding, Opus 5 and Fable 5 wrote several attempts per task and each model picked one. CLM’s picks scored 81.6% on DeepSWE and 87.6% on Terminal-Bench 2.1, against 71.1% and 83.1% for Jev. The team also says Jev did worse than random selection on these long tasks. All of this is self-reported on 38 and 30 held-out tasks, with no outside replication yet.

Weights, data and code are open under Apache 2.0, and a multimodal 35B version is due next month.

## Transcript

[   0.0] It's barely been 2 weeks and Stanford has already open sourced a competitor for Jev.
[   4.6] If you've been living under a rock, Jev is basically a decision model.
[   7.7] It takes a state and a set of candidate actions that you can take in that state as the input
[  12.0] and classifies which actions to take and gives it as the output.
[  15.1] CLM which stands for Contrastive Language Model is developed by Stanford and NVIDIA
[  19.2] and it does the same job but with a dual encoder architecture.
[  22.7] A state encoder and an action encoder that map their inputs into a shared embedding
[  27.2] space and every state action pair is scored by cosine similarity.
[  31.5] The highest scoring action is the final output.
[  33.8] Each encoder is a frozen 8 billion parameter coin 3 model with a trainable projection head
[  38.3] on top which means that during training only those 20 million parameters are fine tuned
[  42.8] so a full pre-training takes only about an hour.
[  44.9] The training itself is divided into three stages.
[  47.4] The pre-training is done on 60 million question answer pairs.
[  50.5] The mid-training is done on 30 million synthetically generated hard negative examples.
[  55.0] And the post-training is done on about a million agent trajectories with 40% of the pre-training
[  59.4] data replayed to avoid any forgetting.
[  61.9] And because the states and the actions are separate, their embeddings can be cached independently.
[  66.9] This makes CLM up to 13 times faster than Jeff.
[  69.7] And when it comes to benchmarks, these are the results compared to Jeff.
[  72.8] I take is that you'll probably never see models like these but they'll end up
[  76.0] inside the agents that you use making the small calls like which tools to use and
[  80.2] which files to read.
[  81.5] This will make the models more deterministic in their behavior than what they are today.
[  84.8] And I think it is worth understanding how these decisions are made.
[  87.9] I hope this video helped with that.
[  89.4] Follow me for more and I'll catch you guys in the next one.

## On-screen text

DID STANFORD JUST KILL JEV? build. ship. repeat.

## Key claims

- On September 23, Stanford and NVIDIA released CLM-8B, a Contrastive Language Model.
- CLM doesn't generate text; it turns the situation and each possible action into vectors and picks the closest match via cosine similarity, using a dual encoder (state encoder and action encoder) architecture.
- Under the hood it is a frozen Qwen3-8B with a small ~20M-parameter trainable projection head on top, so full pre-training takes about an hour.
- Training has three stages: pre-training on 60 million question-answer pairs, mid-training on 30 million synthetic hard negatives, and post-training on about a million agent trajectories, replaying 40% of pre-training data to avoid forgetting.
- Because states and actions are encoded separately, their embeddings can be cached independently — when the action list stays the same (tools, buttons), CLM encodes once and only re-reads new state.
- CLM is reported up to 9x faster than Jev on computer-use, gaming, and tool-calling tasks, and 13x faster at around 1,000 options.
- On coding tasks, Opus 5 and Fable 5 generated multiple attempts per task and CLM picked the best one, scoring 81.6% on DeepSWE and 87.6% on Terminal-Bench 2.1, versus 71.1% and 83.1% for Jev.
- Jev reportedly performed worse than random selection on these long coding tasks.
- Results are self-reported on 38 and 30 held-out tasks respectively, with no outside replication yet.
- Weights, data, and code are released open under Apache 2.0, with a multimodal 35B version expected next month.
- The creator predicts these models will largely be invisible, embedded inside agents to make small decisions (like tool/file selection) more deterministic.

## Info channel

spoken

## Mentioned (unverified hints)

- CLM-8B (Contrastive Language Model): (no url)
- Jev: (no url)
- Qwen3-8B: (no url)
- DeepSWE: (no url)
- Terminal-Bench 2.1: (no url)
