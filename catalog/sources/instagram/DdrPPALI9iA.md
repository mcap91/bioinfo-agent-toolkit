reel: https://www.instagram.com/reel/DdrPPALI9iA/
captured: 2026-10-29
yt-dlp: 2026.10.26
ffmpeg: 7.0.2-static
faster-whisper: 1.2.1
ctranslate2: 4.8.4
claude: 2.1.281 (Claude Code)

## Caption

Nvidia model optimizer repo is a gold mine if you’re getting into hosting and deploying lambs or want to play around with local source models, this will really help you be able to run much larger models on your local hardware without having to buy GPU user anything else this is how I run Qwen 3.8 27b on my laptop #llms #ai #opensourcesoftware

## Transcript

[   0.0] If you're running actual LLMs, I think you should check this out.
[   4.1] So NVIDIA's model optimizer here, this is an open source repo that gives you all the tools
[   9.3] and their own internal testing and benchmarks around how to optimize a model.
[  13.6] So it's like making the model smaller, but not just making the model smaller,
[  16.8] but making the model faster. You'd think those two are connected, but they're not.
[  20.2] So this is like quantization, pruning, all kinds of shit in here.
[  24.5] I, if you're really wanting to get into actually building LLMs,
[  28.9] I highly recommend you read through this and use it because this is, I use quantization,
[  34.7] struggling this morning. I use it to be able to run Quen 3.8 on my laptop, right?
[  41.6] I have that running locally, the 27 billion parameter model just on my laptop.
[  46.4] And it's cut down my coding costs to near zero, pushing billions of tokens a month.
[  52.5] So highly recommend you try it out. Link's going to be in the comments below.
[  57.7] You don't have to comment anything.

## On-screen text

README | Code of conduct | More | NVIDIA Model Optimizer | Documentation latest | Release v0.47.0 | License Apache 2.0 | Documentation | Roadmap | Announcement Blogs | NVIDIA Model Optimizer (referred to as Model Optimizer, or ModelOpt) is a library comprising state-of-the-art model optimization techniques including quantization, pruning, Neural Architecture Search (NAS), distillation, speculative decoding, and sparsity to accelerate... [Input] Model Optimizer consumes a checkpoint of a Hugging Face, PyTorch... [Optimize] Model Optimizer provides Python APIs for users to easily compose the above model optimization techniques and export an optimized quantized checkpoint. Model Optimizer is also integrated with NVIDIA Megatron-Bridge, Megatron-LM and Hugging Face Accelerate for training required inference optimization techniques.

## Key claims

- NVIDIA Model Optimizer is an open source repo with tools, internal testing, and benchmarks for optimizing LLMs
- Optimization makes models smaller and faster, and these are not the same thing
- The repo includes quantization, pruning, and other optimization techniques
- The creator used quantization to run a 27 billion parameter model (referred to as 'Qwen 3.8'/'Quen 3.8') locally on their laptop
- Running the model locally cut the creator's coding costs to near zero while pushing billions of tokens a month
- The link to the repo is in the comments

## Info channel

spoken

## Mentioned (unverified hints)

- NVIDIA Model Optimizer: (no url)
