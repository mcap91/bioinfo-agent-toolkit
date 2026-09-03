# Reading Documents — Isaac Flath
OCR, parsing, layout, tables, images, and document structure.

---
# Speculative Decoding for Faster OCR
**URL:** https://isaacflath.com/writing/speculative-decoding

Note from Isaac: I hosted Joe Barrow for a talk on reducing latency in LLM-based OCR using speculative decoding. What follows is a transcript of Joe's presentation, condensed and edited for clarity.

Why latency matters for OCR
This demo is running on my local machine. On the left, Chandra 2 is running with speculative decoding. On the right, it is running without speculative decoding. We're getting a 2x speedup in OCRing the document by enabling speculative decoding in vLLM with the jbarrow/joecr-chandra-2-eagle3.1 model.

Why is it important to think about latency with respect to OCR? You have this triangle when selling OCR as a service: latency, quality, and cost. Users typically want all three, and they won't settle for optimizing one at the expense of the others. This is challenging when you're serving big VLMs for OCR. Normally, you have one big model where you take in the page, send it through your vision encoder, and then send it through your big LLM to generate all of your output text.

That output text can contain structure. For instance, Chandra 2 returns a format called QwenHTML, which returns the bounding boxes and content of all the blocks. It is one big model generating the page content and structure from start to finish.

In a big autoregressive decode, we feed our page and prompt into the model, then generate text one token at a time. Every token requires an entire forward pass through the model. Qwen only has the numbers 0 through 9 in the tokenizer, so each digit in these output HTML coordinates is one token.
That's 13 tokens for one bounding box.

How speculative decoding works
Speculative decoding allows you to decode or verify many tokens at once instead of doing one token at a time. You can imagine the input is your page and prompt. A small draft model proposes many tokens, then a big model verifies all of them in parallel. We verify them left to right and say, "I like" is correct, but "cooking" is incorrect, so we'll swap it with "playing."

In this case, you get 3 tokens on a single forward pass instead of 1.
We lose all the tokens after the incorrect token and replace it with one new bonus token from our big model.

One of the most important aspects of speculative decoding is that you're not losing quality compared with normal decoding. Other approaches for speeding up LLM inference are lossy. For instance, if you converted your model to a diffusion language model, you would trade quality for latency. But with speculative decoding, you're guaranteed that your output is drawn from the same distribution as it would be without speculative decoding. It is lossless.

My favorite meme of late is: "I'm processing 1,000 pages per second and they're all wrong." This applies to lossy speedups or generally low-quality OCR models like Tesseract.

Three ways to draft tokens
There are 3 classes of approaches.

1. Same-family draft models
With a same-family draft model, you might use Llama 7B to generate draft tokens and Llama 70B to verify them. They have the same distribution over the tokens and the same vocabulary, which is important for speculative decoding.
You're not just running Llama 70B using tensor parallelism. You're running Llama 70B and Llama 7B. There may be GPU contention, so this requires more engineering to get the configuration right.
You're also ignoring the internals of the big model. The big model has a rich representation in its hidden state, and you're throwing that away when you use the Llama 7B representation to track the state. That's why people turned to another technique called multi-token prediction, which is conceptually simple.

2. Multi-token prediction
In a transformer architecture, you have an LM head that takes the hidden state and outputs the next token. With multi-token prediction, you add more language modeling heads to the same pass: t+1 predicts the next token, t+2 predicts the second token, t+3 predicts the third token, and so on for as many MTP heads as you want. Then you jointly train all of them on your data.
To be accurate, this requires jointly training the heads with the model. You can train MTP heads on a frozen model, but I think it's best practice to train them jointly so the representations contain more future information. Interestingly, MTP wasn't originally invented for speculative decoding. The paper asked whether forcing the model to think a few tokens ahead could produce better representations and language modeling. It turns out that you can reuse the same technique for lower-latency LLM runs with speculative decoding.

3. Post-hoc draft models
There's a basket of post-hoc techniques: Medusa; NVIDIA's Eagle 1, 2, 3, and 3.1; D-Flash; and DeepSeek's D-Spark. You typically train a small decoder model that uses the big model's internal hidden states plus the last generated token to predict the next token.
The big model is frozen, and you're training the small output language model, which is typically its own decoder language model. Eagle is a one-layer decoder transformer that autoregressively generates tokens left to right, just like a big LLM. D-Flash is a diffusion language model that generates all the tokens in parallel. D-Spark is a hybrid.
D-Spark does a big D-Flash step and has a little autoregressive head on top. These models tend to be on the order of 100 million to a billion parameters, much smaller than a Llama 7B draft model. They don't require training the big model, and they create much less GPU contention than a large Llama 7B draft model.
I've been open sourcing speculative decoding models recently, starting with an Eagle 3.1 head for Chandra 2. I'm also working on D-Flash and D-Spark for a similar-size model.

Training and evaluating a draft model
Training
How do you train a speculative decoding model? It's 3 steps. You collect 500,000 diverse page images. That's a good order of magnitude, especially if you're constraining yourself to one or a few languages. You run your OCR model over those images and save the hidden states.
You can do it without saving hidden states, but saving them is typically the fastest approach when you're GPU-poor, which is my case. It requires a lot of storage, but it works. Then you train your small decoder—Eagle, D-Flash, etc.—on that data.

I pulled open data from FinePDFs, which includes language IDs, and CCPDF, which requires doing language ID yourself. CCPDF has a million visually diverse PDF image pages. Training took a weekend.
When I trained the original Eagle 3.1 head, the question was: how far can I push this from Friday evening to Monday morning? The released head is undertrained compared with what it should be, and I think D-Flash would be even better for Chandra. I'm hoping to spend more time on it and release better models.
Evaluating
To evaluate it, look at how many tokens are correctly verified by the big model. If the big model says tokens 1, 2, 3, and 4 are correct, that's an acceptance length of 4. If I'm speculating 8 tokens out and my average acceptance length is 1.5, I'm wasting a lot of compute.
If I'm speculating 8 tokens out and my average acceptance length is 7.5, that's incredible. Almost everything generated by my small model is being verified correctly by the big model.

Then you run it in vLLM. It's important to test in a real system. A lot of early speculative decoding papers report speedups over a Transformers generation loop. That's some P-hacking to me because I can give you free speedups over that loop by using anything with decent kernels.
Run it in vLLM at different batch sizes and concurrency levels. Another thing some papers do is evaluate only at concurrency 1. Nobody does that except for agent decoding on a home machine. That's one of my pet peeves: if a paper evaluates concurrency 1 with a Transformers generation loop, I don't trust its results.
The way to do it is to measure actual speedups in vLLM at various throughput levels. As throughput goes up, the speedup tends toward 1 and, in the worst case, dips below 1. That's why you have to change the vLLM configuration for your workload.
Inspecting drafts with SpecSpecs
You can look at all the drafts for a sequence. In this case, I'm using a D-Flash head and generating 8 tokens out. I can see which tokens were accepted, which were rejected, and which are bonus tokens from the big model. This gives you a lot of insight into how good your speculative decoding model is.

For a string of zeros, all 8 draft tokens were accepted, plus a free bonus token. In another example, only the left parenthesis was accepted. The word "short" was the bonus token, and everything after the parenthesis was rejected. That prediction probably wasn't worth it, but the zeros were.
This is how you should look at speculative decoding data if you're a researcher generating heads, which is why I built SpecSpecs. You can see the graphs and identify what was easy or hard for the model to predict.
When speculative decoding pays off
Whether it pays off depends on the shape of your service. If you're running huge batches of OCR documents and only care about cost, you probably don't want speculative decoding. If I know all the documents in advance and don't care whether each page comes back in 600 milliseconds or 4 seconds, speculative decoding is probably a waste of FLOPs.
On the other hand, if you are latency sensitive, willing to pay for wasted compute, and value any 10-millisecond speedup, speculate out to 32 tokens. Even a 0.1 or 0.2 increase in average acceptance length might be worthwhile if you only care about latency.
What other OCR teams are doing
Reducto seems to be doing MTP-1, which means they predict one additional token each time. They still have to verify that second token, but they have a 98% acceptance rate. That means their average acceptance length is 0.98.

An average acceptance length of 0.98 feels low compared with 3.43 for the model I showed earlier, but those numbers represent different maximum speculation lengths. Reducto is wasting effectively nothing. DeepSeek trained MTP-1 with DeepSeek V3 and reported a 90% acceptance rate in the technical report.
Reducto has an even higher acceptance rate than DeepSeek. Conversely, DataLab wrote a year ago that they trained Eagle 3 on Chandra. I don't know what acceptance rate they reported, but they lowered P99 and P50 latency while improving throughput.

Typically, you would use Eagle 3 for longer acceptance lengths and MTP for a small number of highly accurate predictions.
Using speculative decoding for OCR
Running Chandra 2 with EAGLE 3.1
You can experiment with this easily. This single command runs Chandra 2 with the Eagle 3.1 head I released and speculates out to 5 tokens. You can go shorter if you're trying to improve latency without sacrificing too much throughput. At low concurrency, I'm seeing roughly a 2x speedup on this 5B VLM, which you can run on your machine, on GPUs, or on Modal.
Loading...
Where this fits in a product
Speculative decoding heads are tied to the underlying model they're trained on. Right now I'm only releasing heads trained on Chandra, but hopefully we'll get others out.
If you are satisfied with Chandra's quality and want better latency, consider an agentic document-processing task where you only need to OCR the pages most relevant to your agent. You can do that just in time and get a 2x speedup. If I have a million pages to run through a system, I would probably turn it off.
vLLM can dynamically turn off speculative decoding at large batch sizes. You can turn it on by default and disable it when the batch size goes above a threshold, maximizing throughput and minimizing latency in either regime.
Speculation versus diffusion
The Chinese lab MinerU has a diffusion-based model that generates entire blocks of 81 tokens at once. That can deliver low latency, but you see a big drop in quality—about 10%. I'm not currently a huge fan of diffusion for low latency, and I'm writing a blog post called "Don't Diffuse, Speculate" that goes into more detail. Diffusion can reach much lower latency than speculative decoding at an even greater cost to throughput.

Other OCR-specific speedups
I've been working on other possibly free ways to speed up speculative decoding for OCR. Can you use the document's language to speed up drafting? Baidu's Unlimited OCR Works uses Reference Sliding Window Attention for OCR. Could you use a sliding window for drafting as well?

Why more work can still be faster
Why is speculative decoding fast? It's somewhat counterintuitive. With normal generation, you're paying the FLOPs it takes to run the model for every generation step. If your model has a billion parameters and generates 1,000 tokens, you can hand-wave and say you're doing a billion FLOPs 1,000 times.
With speculative decoding, you might think, "I'm saving compute because I'm drafting those 1,000 tokens and verifying them with the big model." But you're spending more compute. You pay the extra draft compute plus the same compute for running 1,000 tokens through the big model. That's true even with a 100% acceptance rate and a speculation length of 10.

If you're doing more work, why does speculative decoding reduce latency? It has to do with how GPUs work and something called the roofline model. Given the amount of data you load and compute you perform, a workload is typically either memory-bound or compute-bound.

For a dot product between two vectors, you load both vectors and then do simple math: multiply and sum. That operation is memory-bound because most of the time goes into loading the vectors. But when you multiply two 1,000 by 1,000 matrices, you load the matrices and then do a lot of math. That operation is typically compute-bound.

Generating one token for one sequence is typically memory-bound because you load the entire model weights for a one-token forward pass. You're wasting a lot of compute. Speculative decoding tries to move you toward optimal compute saturation for your GPU. If you speculate too far, especially with a high batch size, you become compute-bound instead. The forward passes take longer because you're doing too much work.
That's why vLLM can turn speculative decoding off at high batch sizes or concurrency. At low batch sizes or concurrency, speculative decoding helps move the service toward the hardware ridge point: the right balance between loading data from memory and performing floating-point operations on it.

D-Spark tries to stay at this hardware ridge point. At high throughput, it dynamically stops speculating. At low throughput, it speculates more. If you're dynamically allocating the number of tokens to speculate, how do you know which ones to include? You predict a confidence: is this token going to be accepted or not?
At low concurrency, speculation uses compute that would otherwise sit idle. As concurrency rises, shorten the speculation length or turn it off.
Questions from the talk
Coding with an open model on a plane

Audience question: What was it like using a small open model locally without internet access?

I was flying home from SFDCC this weekend. No Wi-Fi, my MacBook Air, and 5 hours—a perfect time to do this. I knew the core: write a bunch of stuff to Parquet, analyze it with DuckDB, and instrument the generation loop. Before heading to the airport, I downloaded Qwen3-4B, the D-Flash head, and all the packages I would need.
On the flight, I ran into an issue saving everything to Parquet and didn't have the docs downloaded. I didn't want to pay for Wi-Fi to ask a question. But I had just finished building the D-Flash generation loop with Qwen3-4B, and the code was open on my laptop. I swapped the demo prompt for my actual question: how do I create a pa.timestamp when using PyArrow?
Qwen3-4B answered. I asked it 5 or 6 questions. It was wrong for 2, but right enough on 3 that I could use the answer in my code. For anything it got wrong, I could experiment right there.
I'm sitting on a plane with Python open. I can type the code and find out that .x doesn't exist on this object. It was a very cool experience to get value from Qwen3-4B running on a MacBook Air while I was writing instrumentation to observe it running.
The cool part is that it generated 521 tokens in only 168 forward passes. Even on the MacBook Air, D-Flash reduces forward passes and accelerates generation. I could literally feel the difference with and without D-Flash.

Where Medusa fits

Audience question: How does Medusa relate to multi-token prediction and post-hoc draft models?

I would say Medusa is a post-hoc small model in a weird place between MTP and Eagle. It lets you generate many tokens at once for each position.
With normal MTP, you're generating one token per position. You take the argmax or sample from your LM head. With Medusa, you generate multiple tokens per prediction, construct trees, and verify all of them in parallel. Instead of feeding your single best sequence to the model, you feed it a tree-structured attention pattern. This can vastly improve average acceptance length at the cost of effective acceptance length. With a sequence length of 8, you might go from an average acceptance length of 4 to 6.
But you're no longer verifying 8 tokens. You could be verifying 24, so you're accepting 6 out of 24 instead of 4 out of 8. Is that worth it for you?
I don't think Medusa is super common anymore. Eagle 2 took the tree idea and combined it with a small decoder model that can look at the big model's internals. Eagle 2 has now been supplanted by D-Flash and Eagle 3. D-Spark is probably the next common way to do speculative decoding.

---
# OCR Examples Gallery
**URL:** https://isaacflath.com/writing/ocr-examples-gallery

A comparison of OCR tools and vision-language models on document pages: dense tables, forms, charts, maps, scanned equations, and diagrams. Every model sees the same page and (for VLMs) the same doc-type prompt.
The six models represent six ways someone might build a production document system. This is a curated comparison rather than an exhaustive model ranking:

ApproachRepresentativeWhy it is hereSimilar modelsConventional OCRPaddleOCR PP-OCRv5A direct text-recognition engine without a document or language-model layerRapidOCR, Tesseract, EasyOCRManaged document OCRAWS TextractThe baseline for a team that wants to buy an API rather than operate OCR infrastructureGoogle Document AI, Azure AI Document Intelligence, ABBYY VantageDocument pipelineMinerUA packaged system that combines recognition, layout, and document reconstructionDocling, Unstructured, MarkerOCR-specific vision modelChandra OCR 2A vision model built specifically for document transcriptionSurya OCR 2, Nanonets-OCR2-3B, DeepSeek-OCROpen general VLMQwen3-VL 32BA self-hostable general vision-language model prompted for extractionQwen3-VL 8B, InternVL, MolmoHosted general VLMGemini 3.5 FlashA general multimodal model consumed as a managed APIOpenAI GPT, Anthropic Claude, Gemini Pro
Models in the last column cover the same broad role.  This gallery should help you pick a general class, then you need to evaluate models on your own pdfs to narrow it down further.
This is not meant to be an instructive guide, for that start with these 2 articles:

How to Choose an OCR Model
VLMs for Hard OCR Tasks

Hope you enjoy!

Government financial statement
Source: Financial Report of the United States Government, FY2024, page 68 (page PDF) · doc type: table

AWS Textract AnalyzeDocument (boto3 1.43.67); no task prompt.

1950 census questionnaire grid
Source: 1950 Census population questionnaire, page 1 (page PDF) · doc type: table

AWS Textract AnalyzeDocument (boto3 1.43.67); no task prompt.

Coastal chart with coordinates
Source: NOAA United States Coast Pilot 2, page 240 (page PDF) · doc type: map

AWS Textract AnalyzeDocument (boto3 1.43.67); no task prompt.

United States v. Banque Pictet & Cie SA — Deferred Prosecution Agreement
Source: United States v. Banque Pictet & Cie SA — Deferred Prosecution Agreement, page 12 (page PDF) · doc type: generic

AWS Textract AnalyzeDocument (boto3 1.43.67); no task prompt.

US 11,335,153 B1 — Fully Autonomous System for Grading, Stamping and Encapsulating a Collectible Object
Source: US 11,335,153 B1 — Fully Autonomous System for Grading, Stamping and Encapsulating a Collectible Object, page 5 (page PDF) · doc type: diagram

AWS Textract AnalyzeDocument (boto3 1.43.67); no task prompt.

Alameda County — Official Retail Food Inspection Report
Source: Alameda County — Official Retail Food Inspection Report, page 1 (page PDF) · doc type: form

AWS Textract AnalyzeDocument (boto3 1.43.67); no task prompt.

Financial Accounts of the United States: Second Quarter 2025 (Z.1)
Source: Financial Accounts of the United States: Second Quarter 2025 (Z.1), page 84 (page PDF) · doc type: table

AWS Textract AnalyzeDocument (boto3 1.43.67); no task prompt.

Berkshire Hathaway Inc. 2024 Annual Report
Source: Berkshire Hathaway Inc. 2024 Annual Report, page 90 (page PDF) · doc type: table

AWS Textract AnalyzeDocument (boto3 1.43.67); no task prompt.

FDIC Quarterly Banking Profile, Fourth Quarter 2025
Source: FDIC Quarterly Banking Profile, Fourth Quarter 2025, page 11 (page PDF) · doc type: chart

AWS Textract AnalyzeDocument (boto3 1.43.67); no task prompt.

Apple Inc. Form 10-K, fiscal 2024
Source: Apple Inc. Form 10-K, fiscal 2024, page 34 (page PDF) · doc type: table

AWS Textract AnalyzeDocument (boto3 1.43.67); no task prompt.

Health Insurance Claim Form — CMS-1500 (02-12)
Source: Health Insurance Claim Form — CMS-1500 (02-12), page 1 (page PDF) · doc type: form

AWS Textract AnalyzeDocument (boto3 1.43.67); no task prompt.

GOPRELTO (cocaine hydrochloride) Nasal Solution — Prescribing Information
Source: GOPRELTO (cocaine hydrochloride) Nasal Solution — Prescribing Information, page 3 (page PDF) · doc type: table

AWS Textract AnalyzeDocument (boto3 1.43.67); no task prompt.

RITALIN and RITALIN-SR (methylphenidate hydrochloride) — Prescribing Information
Source: RITALIN and RITALIN-SR (methylphenidate hydrochloride) — Prescribing Information, page 1 (page PDF) · doc type: generic

AWS Textract AnalyzeDocument (boto3 1.43.67); no task prompt.

Fictional discharge summary, 'John Doe' (GeriSage teaching example)
Source: Fictional discharge summary, 'John Doe' (GeriSage teaching example), page 1 (page PDF) · doc type: generic

AWS Textract AnalyzeDocument (boto3 1.43.67); no task prompt.

Cheney Brothers, 'Art in Fashion' typescript draft (Library of Congress)
Source: Cheney Brothers, 'Art in Fashion' typescript draft (Library of Congress), page 43 (page PDF) · doc type: generic

AWS Textract AnalyzeDocument (boto3 1.43.67); no task prompt.

Calvin Coolidge, speech before the American Classical Association, typescript (Library of Congress)
Source: Calvin Coolidge, speech before the American Classical Association, typescript (Library of Congress), page 21 (page PDF) · doc type: generic

AWS Textract AnalyzeDocument (boto3 1.43.67); no task prompt.

Attention Is All You Need (arXiv:1706.03762)
Source: Attention Is All You Need (arXiv:1706.03762), page 4 (page PDF) · doc type: equations

AWS Textract AnalyzeDocument (boto3 1.43.67); no task prompt.

Source: First Bus Glasgow — Service 4/4A Timetable, page 1 (page PDF) · doc type: table

AWS Textract AnalyzeDocument (boto3 1.43.67); no task prompt.

Vanguard S&P 500 Index ETF (VFV) fact sheet
Source: Vanguard S&P 500 Index ETF (VFV) fact sheet, page 2 (page PDF) · doc type: table

chandra-ocr 0.2.0 (Chandra OCR 2, hf method); no task prompt.

---
# How to Choose an OCR Model
**URL:** https://isaacflath.com/writing/how-to-choose-an-ocr-model

I invited Joe Barrow to give a public talk on how to choose an OCR model. This post covers what he shared about choosing between OCR APIs, open pipelines, and self-hosted vision-language models.
Prices and license terms were current when Joe gave the talk.

Why you should care about OCR
Your users care about OCR. Until about a year ago, Claude could only handle PDFs that were text based.
If you uploaded a scan, Claude couldn't see it at all. This is a large company with a product that wasn't handling OCR, and users noticed. They complained a lot about Anthropic's poor PDF handling.
Documents are also heterogeneous. For a recent project, Joe's team processed ~7 million pages of local laws. Many were scans or multi-column layouts where reading order wasn't present in the PDF. A good OCR model gives you a homogeneous version of those heterogeneous documents.
PDFs themselves are pretty evil. Vic Parachuri from Datalab made a website called WTF PDF, where you can upload a PDF and see whether it hits any bad edge cases. For instance, TeX-compiled PDFs don't have spaces in them. They use a system called glue that prints glyphs at specific locations.
If you pull the text from a PDF with a PDFium wrapper such as pypdfium2 but without post-processing heuristics, you get an entire run of characters with no spaces. In an AI-powered app, everything is downstream of OCR quality. You start with documents and extract the information before doing the actual task.
OCR quality becomes a bottleneck for the business logic and everything you display to users. Once you've built your app on top of a specific OCR model, you are locked into a vendor.
OCR is very sticky. Joe learned this at Pattern. Once everything was built on a specific OCR model or set of models, it was difficult to rip it out and replace it with something better or something that could do better layout analysis.
Joe's background
Joe has an NLP PhD from Maryland.
He led ML at Pattern Data until recently and is now at Adobe Research in the Document Intelligence Lab. He gave this talk as an independent researcher.
The opinions are his own and are not cosigned by Adobe.
What does OCR mean?
OCR output falls into four rough levels:

Raw text: Get all the text runs out of a PDF and concatenate them with spaces.
Markdown: Preserve headers, paragraph spacing, subheadings, and parsed tables.
Grounded text: Return word or line bounding boxes so you can highlight a line and show where the relevant evidence came from.
Full document structure: Return reading order, layout, semantic roles, rotation information, and parsed tables.

Concatenating raw text was a common way to build AI-powered document apps: pull the text out, throw it into the LLM context, and hope something good happened. It creates quality problems, so you may need something richer from the PDF.
All of these outputs count as OCR. The one you choose depends on what your product needs.
The OCR landscape

Two axes guide how you build OCR into a product. The first is whether you need text blocks from the PDF or semantic roles such as headings and paragraphs.
Do you need the full structure, including tables and figures? That choice determines much of the cost and quality.
The second axis is whether to self-host a model, which can lower costs but takes more engineering time, or rely on an API. These two axes cluster the models into four groups. Big cloud providers include Amazon with AWS Textract and Google with Google Cloud Vision.
Startups such as Reducto, DataLab, Extend, and LlamaIndex are building fully featured OCR models. On the self-hosted side, open pipelines such as PaddleOCR, Nemotron OCR, and Tesseract provide cheap, fast text blocks.
Open VLMs that produce more structure include LightOnOCR, GLM-OCR, Chandra, Chandra 2, Docling, and Surya OCR. There are probably 50 to 60 open models, but only a few you might want to consider.
Do you need text blocks or document structure?

Do you need text blocks or structure for the downstream app? Text blocks from APIs can ground LLM output to a specific line or set of words using word bounding boxes. Structure gives the downstream LLM a semantic representation of the document in reading order.
Document structure groups lines into the paragraphs they belong to and assigns semantic roles such as paragraphs, headings, and tables.
It also gives you reading order, which line-level OCR doesn't guarantee. Some models include layout: the bounding boxes of each element.
Models may also return parsed tables, figure alt text, and, more recently, chart de-rendering. A model can de-render a chart into a CSV of the data used to construct it.
These features aren't present in every model. Choose text blocks when you need word-level grounding or the app needs to show evidence.
Text blocks are also the cheapest option. Models that return only text blocks are almost an order of magnitude cheaper because they are typically simple pipelines. The same difference appears between cloud APIs and document startups.
Choose structure when you want to preserve the document's visual semantics: where the paragraphs are and how the content appears in the document.
We noticed at Pattern that preserving document semantics is a free performance improvement for downstream information extraction, AI-powered question answering, and other tasks.
Giving the LLM runs of text from Textract may be cheap and fast, but it typically leaves performance on the table. RAG and information extraction pipelines usually benefit from preserving document structure because LLMs are trained on plenty of Markdown and similar structured text.
Complex document layouts reduced to lines give the LLM jumbled-up garbage, even from good providers such as Textract.
Should you use an API or self-host?
Use an API for ease and support
With an API, you're paying for ease of use and personal support. If documents don't work well with a startup's API, you can tell them, "I have this set of documents and I'm getting bad output." They may consider those documents when retraining their models and pipelines, especially for a larger enterprise customer.
Self-hosting doesn't provide that support. You have to fine-tune the model yourself. Use an API when you want to minimize the time spent handling OCR for the app.
Self-host for control and scale
Building an OCR pipeline is doable at scale, but time-consuming when you're focused on the product. Self-host when you need to control throughput or concurrency.
An API typically limits you to fixed concurrency. At Pattern, the number of simultaneous documents its OCR providers allowed in flight often became the bottleneck. With a model hosted on Modal or similar infrastructure, you can pay for more throughput instead of asking a provider to raise the limit. You also control the weights.
Your OCR model will not change underneath you. You can fine-tune it for your domain or add speculative decoding. Self-hosting can also be cheaper.
The math generally works only if you value your time at 0,buthostingaVLMcancostmuchlessthanastartupAPIcharging0, but hosting a VLM can cost much less than a startup API charging 5 or $10 per 1,000 pages. Bulk processing lowers that number further.
For a huge enterprise batch job, the math can work even when your time isn't free. For an AI product still looking for product-market fit, self-hosting will not be cheaper, though it avoids vendor lock-in.
Solving batch and online OCR with high throughput is a neat engineering challenge. You can get a first pass with a weekend's effort, but a system that handles large throughput takes longer.
Big cloud providers or document startups?
Big-cloud services such as AWS Textract typically cost 0.60to0.60 to 1.50 per 1,000 pages. Textract starts at about $1.50, and Google Cloud and Azure are in a similar range.
Volume pricing lowers the cost as monthly usage climbs into the millions of pages. Textract bottoms out at about 60 cents per thousand pages, but typically returns only word and line boxes with their text.
It does not include semantic structure. You may need to add table parsing, grouping or clustering, and reliable reading order downstream.
AWS sells some of these features à la carte. Form or table processing can cost 10or10 or 15 per 1,000 pages for each feature.
Startups such as Reducto, Extend, DataLab, and LlamaIndex cost about 5to5 to 20 per 1,000 pages, with volume discounts. The lower end is typically called "fast" and the upper end "accurate," though each company uses different names.
They return table processing, figure bounding boxes, grouping, and the page's Markdown or HTML. That output can be much more useful to a downstream LLM.
Open pipelines or open VLMs?
Open pipelines
Open pipelines such as Tesseract and PaddleOCR are fast and cheap to run.
They typically have 10 to 100 million parameters. PaddleOCR has a version that runs on a phone. Devices such as the Boox writing tablet, similar to a Remarkable, run PaddleOCR locally.
These devices typically run a model such as PaddleOCR and get text lines only. Paddle recently released a DocLayout model for layout, which you can use to aggregate text lines into paragraphs after the fact.

Open pipelines are typically composed of many small models. PaddleOCR first detects page orientation to determine whether the page is rotated.
They dewarp the page if it's a scan. They identify all the lines on the page and rotate individual lines when needed. In the arXiv paper on the slide, there's a header on the left in a different orientation and a line across the top. The pipeline then recognizes the text in each identified line.
Open pipelines therefore return line bounding boxes and the text within each line, but not necessarily reading order or document structure.
Open VLMs
VLMs are much heavier, normally 600 million to about 8 billion parameters, so cost follows model size.
VLMs natively produce document structure. Chandra and Surya return structure rather than text lines. They can carry more hallucination risk.
Passing an empty page into some open models can produce a boilerplate hallucination. But after looking at probably a million pages of OCR output from the big clouds, Joe has seen that risk there too with crusty scans. Textract detects the text lines, then recognizes their text.
He has seen the word "the" repeated 100 times when the scan is effectively noise. With VLMs, you're paying at the compute rate. A 600-million-to-1-billion-parameter model costs about 20 cents per 1,000 pages on an H100, assuming you keep the H100 saturated.
For an 8-billion-parameter model, you might be looking at $3 or more per 1,000 pages on an H100.

VLMs are typically one big honkin' model trained end-to-end. You feed in the page and prompt, then get output text, perhaps as HTML with bounding boxes. That's what Chandra and Surya do.
They use the Qwen-HTML format, typically in a single shot. Multi-shot and pipeline VLMs are outside the scope of this talk. If you over-index on cost and latency, choose pipeline models for handwriting, and ignore quality, the models can be fast while the whole app suffers.
Paying more can be worth it. Processing a thousand pages per second does not help if they're all wrong and the app's output is garbage.
Two different use cases
Seven million pages of local laws
Joe and a friend at Berkeley collected ~7 million pages of laws from every city and county around the United States that they could get their hands on.
They needed to do it on the cheap because they didn't have huge resources to process all ~7 million pages. At 5per1,000pages,itwouldcostmorethantheBerkeleylabwaswillingtopay.ItwasalsoahobbyforJoe,sohevaluedhistimeat5 per 1,000 pages, it would cost more than the Berkeley lab was willing to pay. It was also a hobby for Joe, so he valued his time at 0 but wasn't willing to put a bunch of money into it.
They needed the text, headers, and reading order. Then they could split the data into individual laws and make sure each law was coherent.
On a two- or three-column page, the laws had to remain grouped and coherent. They didn't need graphics, figures, or tables because they planned to throw away the raw PDF after finding the laws and releasing the dataset.
The right option was to self-host a VLM that outputs Markdown: LightOnOCR-2 from LightOn AI, a strong 1B model near the top of olmOCR-Bench.
They ran it for about 30 cents per 1,000 pages, all in, including reprocessing.
The run took between a weekend and a week.

Now consider a vertical startup doing information extraction for legal companies, hospitals, or financial records. A user uploads PDFs, asks questions, and extracts information live. That creates a different set of constraints.
This is a common startup setup: build on an existing OCR model, then add value with AI-powered information extraction and business logic. This is not a fixed dataset or batch job.
The system has to scale with live users. If the output is grounded to the PDF, you need word bounding boxes to highlight the words relevant to the AI output.
You might also want structure to feed the LLM, which requires some post-processing.
At a startup, engineering time is very much not free. Tinkering with OCR takes time away from the app, business logic, and customer value. A good decision might be Textract with a post-processing layer that aggregates its output into structure for the LLM.
There is no best OCR model. The right choice depends on your needs and the outputs of different approaches on your data.
Most of you should not self-host
Most of you should not self-host. Only ~5% of teams should.
If you're product-focused and trying to find product-market fit, use an API. Self-hosting isn't worth your time. You are not the OCR person.
You're trying to build a startup for financial records. If you are in that ~5%, hosting is easier than you might think and fun as hell. The rest of this talk is for you.
How to choose an open model
Test candidates on your data
First, look at the actual data. Do you have crusty scans, handwriting, or medical terminology?
Popular OCR benchmarks such as OmniDocBench and olmOCR-Bench are indicative, but they won't tell you how models perform on your data.
The only way to choose an open OCR model is to test it on your data.

Manually build a set of 50 to 100 representative pages. The easiest way (this sounds stupid) is to open several PDFs and copy and paste pages into one new PDF with Apple Preview or Adobe Acrobat. One PDF is easier to send through each cloud API or hosted server.
Choose five to 10 candidate models from the grid and run the same PDF through each. Diff the returned text between candidates.
Inspect the failures and visualize the boxes. This makes it easy to see that one model returns junk on handwriting, which many pipeline models do. You can Claude up a visualizer for the OCR outputs.

This should take about a day, including looking at the outputs and standing up some vLLM instances.
Check the license
Look at the model's license before choosing candidates. Chandra and Surya from Datalab are good models, but their model weights are free only if your organization stays under $2 million in both annual revenue and total funding and does not compete with Datalab. Broader commercial use requires a license.
Conversely, there are good open licenses you can use at any stage of commercialization. LightOnOCR is Apache licensed. GLM-OCR is MIT licensed and relies on PaddlePaddle's DocLayout model, which is Apache licensed.
You have to adhere to both licenses. Do not put your company at risk by using a model you don't have the license for. Plus, it's good karma to adhere to software licenses.
How to host the model
Choose a model and inference engine
You need three things. First, decide on a model.
Second, decide on an inference engine. Joe prefers vLLM, and many OCR models are released with vLLM as the default system, though SGLang is also very good. ~50% of the models released with an inference engine have SGLang support as well.
Choose infrastructure
Third, choose infrastructure to run that model on. Joe has enjoyed using Modal. Pattern moved everything over to it.
For the laws work, Joe and his collaborator built the OCR on Modal. There are other good infrastructure and inference providers, such as Baseten. You can also use a big cloud such as AWS, though the shape of your needs will determine what you want.
AWS is great for a huge batch of data you need to process once, but SageMaker scale-in and scale-out is clunky compared with Modal's scaling based on the number of requests in the queue. You can get surprisingly far by running either billion-parameter model through vLLM in a Modal container.
You're exposing an OpenAI-style client and need to pass in the GLM-OCR prompt. For LightOnOCR, there is no prompt. You pass in the image as a user message.
Check throughput and cost
Both models run on an H100, assuming you saturate it in batch. In Joe's experience, they cost around 20 to 30 cents per 1,000 pages, even at Modal prices. That gives you about 10,000 pages an hour on an H100.
The math is about three pages a second times 3,600 seconds in an hour. Joe has also served LightOnOCR on his local rig of four 3090s. You get close to three or four pages a second, assuming you can saturate the GPUs. Four 3090s are roughly equal to one H100.
The decision matrix

The decision process is:

Decide whether the downstream product needs text blocks or full document structure.
Decide whether the workload belongs on an API or a self-hosted model.
Run a small set of candidates against the same 50-to-100 representative pages.
Inspect the raw outputs, compare failure modes, and check the license before choosing.

Those first two decisions tell you which quadrant to start in. With full-structure document startups, you're paying a lot of money, but you're getting high-quality, feature-complete output that you can feed into an LLM.
Open VLMs are typically heavyweight and roughly feature-complete, though usually a little worse than the document startups. Many open VLMs are released by startups. Chandra and Surya are from Datalab, which has a stronger in-house model.
Open pipelines such as PaddleOCR can be very high quality but are still limited compared with the niceties you get from open VLMs. They are fast, very cheap, and can even run on an edge device, which would be free for you. Big cloud providers are typically quite cheap at scale.
Big cloud providers return word- and line-level bounding boxes.
You can reach Joe on X at @barrowjoseph.

---
# VLM OCR for Hard Documents
**URL:** https://isaacflath.com/writing/vlm-ocr-for-hard-documents

I hosted Joe Barrow for a talk on VLM for Hard OCR Documents. This post covers what he shared about how these models work, where they fail, and how to choose one. Questions and comments from me and other attendees are set off as blockquotes.
OCR is not just getting the text on a page. Depending on the downstream task, you may also need text structure. Is this a heading, part of a paragraph, or a cell in a table row?
The reading order and document layout could matter as well. Two paragraphs might be in a two-column layout. Data might be in figures, charts, and tables.
You can ignore figures, capture their bounding boxes, deconstruct a chart into a pandas DataFrame or another useful format, or add a caption.
OCR also has to handle all kinds of document crap: multiple pages embedded in one page, scans, handwriting, and general document crust. Medical records often contain a printed and scanned page inside another printed and scanned page. At some point, you lose most of the original content, and the OCR engine still has to handle it.
This is a more research-heavy discussion of VLMs for OCR: how to deploy them and figure out when and where to use them. There's another talk on how to choose an OCR model, set up the infrastructure, and decide when to self-host versus call an API.
VLMs for OCR are what Joe does and also a passion of his. He used to be the head of machine learning at Pattern Data, where the team processed several hundred million pages of documents. He is now a research scientist in Adobe's PDF research lab (Adobe is THE document company).

Why VLMs for OCR?
Until 2022 or 2023, the most popular OCR engines were pipelines. Think Tesseract, PaddleOCR from Baidu, or the first Surya model that Vic released from Datalab. PaddleOCR is five models. The first detects page orientation: is it upright, rotated 90 degrees, or rotated 180 degrees? If it's a scan, you can dewarp the page and get it square again. Then text-line detection finds rectangles of text, and the pipeline makes sure each line has the right orientation.
Many pages contain text in multiple orientations, so the pipeline must determine the orientation of each line before recognition. AWS Textract doesn't allow text in multiple orientations. AWS Rekognition, its scene text recognition engine, returns up to 100 words per page but supports lines in multiple orientations up to 90 degrees apart from the upright orientation.
That means a page can have text at 0, 90, and 270 degrees.

Isaac: Is that primarily for charts and graphs and legends and labels and things like that?

You would think so, but many documents have text in places and orientations you wouldn't expect. A simple example is an arXiv page with an arXiv header running along the side at 90 degrees. Charts are another common example, or pictures of medical devices. A device could have serial numbers in two orientations while the whole image was upside down. You need to handle the upside-down image and both orientations of text.
Traditional pipelines run these models one after another and return raw text grouped by line. Depending on how you train them, they can handle different languages, scans, handwriting, and document crust. They don't provide text structure, reading order, document layout, or handling for figures, charts, and tables.
These models end up being very fast, because they're ~ 10 to 25 million parameters, but they're very limited. There's no global view at decoding time. There's also a risk of cascading pipeline errors. If your text recognizer is wrong, then your detector is going to be very wrong because it's looking at something that's not text.  Then you need more stages to handle the document structure described above.
To extract a table, you need a table detector followed by a table structure detector. The IBM Docling pipeline uses a table structure parser that examines chunks of a table and predicts whether each cell merges with the cell to its right or below it. It uses those predictions to reconstruct the full table.
Each capability adds another stage to the pipeline. VLMs can handle them as a single run of structured text, which gives the model a global view at decoding time.
The VLM always sees the whole page. If someone writes the same word slightly differently on two lines, the model can use the rest of the page to infer that they are probably the same word. It may get both right or both wrong.
A pipelined recognizer doesn't see the rest of the page and can get one instance wrong simply because it is less clear. Most VLMs are not pipelined. Some newer approaches introduce pipelines to reduce latency, but most models released since 2025 take a single image and return structured text.
The VLM can be trained to generate Markdown headers, parse tables, and return bounding boxes around figures. Its output already contains the document structure. That comes at a cost: pipeline components might have 15 million parameters each, while VLMs start around a billion parameters. The best model on olmOCR-Bench has 32 billion parameters. Joe questioned whether a model that large still counts as an OCR model and could not think of a case when he would want to use one.
As an example of what this looks like, Chandra from Datalab takes a single image and outputs a structured representation of the page. It uses a format called Qwen-HTML with a data-bbox attribute on each HTML tag. That attribute outputs the location on the page normed to 0 to 1000 and then the text in that location.
The sideways archive box becomes a div with a bounding box and role. The page title becomes an h1. One long run of HTML captures the page structure, location of each element, and reading order.
The same output can parse tables, locate figures, and caption them.

Isaac: When you say reading order, do you mean the first column on the left comes before the second column rather than reading straight down the page?

Reading order is how you handle complex layouts. This case isn't a particularly complex layout, and you could use a simple layout engine to identify two columns. But then you get into old newspapers with three, four, or five columns, article chunks that start in one column and end in another, and different articles on the top and bottom of the page. Suddenly reading order becomes a much harder problem that needs some semantic understanding of the page.
Reading order can also be ambiguous, and sometimes you don't want things like a header on the side. Those are considerations for how you train the VLM, but training normally pretends that the model can generate one ground-truth reading order from the image of a page.
How VLMs work
A VLM divides an image into patches sized for the ViT, or vision transformer. These can range from 16 x 16 down to 4 x 4. The transformer generates a vector for each patch.
Those vectors are projected into the LLM decoder's token space and treated as normal tokens. With a Qwen backbone, for example, you can fine-tune the ViT to generate tokens for Qwen. You can also include a prompt telling the OCR model whether to output layout or figure bounding boxes.
The model then generates its output autoregressively, usually token by token. The result can be plain page text, bounding boxes, or a structured layout.

Isaac: If you don't need the architecture details, think of the model as a black box. The page is broken into small pieces and fed in along with your prompt. Magic happens, and the output comes out. Focus on how the input is broken up, what gets sent in, and what comes out.

That black-box view is useful: these models take in patches and generate tokens in the ViT space, or take in tokens and generate tokens in the LM case. Many interesting research questions fall out of this. The DeepSeek-OCR paper, for example, asked whether the number of tokens output by the vision transformer could be compressed.
If the vision transformer generates 16 x 16 patches and one token per patch, an image can become one or two thousand tokens, which can be expensive. Do you need all of those tokens? Can you reduce that number with a projection or attention layer? That's what the paper examined.
Three representative OCR VLMs
Three models show the main architectural patterns. LightOnOCR-2 comes from LightOn AI, a French company that works on retrieval and also has this family of OCR models. Chandra comes from Datalab, which has a hosted OCR pipeline that accepts PDFs.
MonkeyOCR comes from a Chinese lab and takes a different approach.
LightOnOCR-2
LightOnOCR follows the VLM architecture described above: the ViT patchifies an image, generates tokens, and feeds them to a standard Qwen3-0.6B decoder with 600 million parameters.
They took the ViT from Mistral, specifically the Ministral model. VLMs are normally jointly trained, with a fixed decoder and ViT trained on billions of image-text pairs. LightOnOCR instead Frankensteined two independent models together. It works because the Mistral ViT is strong on documents and Qwen 3 is a strong decoder. They trained it on 16 million pages to output Markdown in reading order.
The output contains the Markdown header, its content, and then the H2 that declares the content type. Because it's a 1B model that only outputs Markdown, it is cheap and efficient to run. In Joe's experience, it cost about 30 cents per thousand pages. LightOn claims about 10 cents, but Joe thinks that requires several tricks and cheaper compute than he had access to. The model takes in a single page image and outputs Markdown token by token.

Isaac: Okay. So it's just Markdown. Is it also inferring the reading order and putting the content in that order? Is it putting tables into Markdown tables? Does it handle images somehow?

It converts tables into HTML as part of the training pipeline. For images, the model can mark the image and include a caption. A variant called LightOnOCR-2-1B-bbox generates only the image bounding boxes. LightOnOCR also converts formulas into LaTeX. Everything is generated in the model's best-guess reading order.
Joe has run this on many different reading orders and found it robust and high quality, especially for the size. It does have issues. The kinds of errors that happen with VLMs are very different from pipeline OCR models. Even though it was trained to handle blank pages, a semi-blank page will sometimes trick the model into hallucinating boilerplate HTML.
That becomes a question of how to fine-tune the behavior out of LightOnOCR. This error generally wouldn't happen in a pipelined model because the text recognizer would fail. But if the text detector doesn't fail and detects fake text on the page, you get a lot of crap as well. Joe saw this often in crusty scans at Pattern, where Textract would return only the word "the" from a non-textual region.
Chandra 2

Chandra 2 follows the same formula as LightOnOCR, but starts with raw Qwen 3.5. They use several tricks to reduce it to a 5B model. The model outputs a Qwen-HTML structure where each HTML element has a data-bbox attribute and a data-label describing its semantic role on the page.
The labels distinguish page headers from section headers, and the bounding boxes are quite accurate when mapped back onto the page. The training recipe is straightforward: send in a page image and train against its HTML representation. For tens of millions of pages, those representations can come from a combination of existing OCR models, born-digital page information, and heuristics.
Humans may clean up the validation set. The underlying VLM is still straightforward: page image in, tokens out. Qwen-HTML generates many more tokens than LightOnOCR's sparse representation of the page text. In return, Chandra produces richer structure grounded in regions of the page.
That structure requires generating all of the additional HTML tokens. Qwen doesn't have tokens for two-digit numbers, so each digit in a bounding box can become an individual token. In return, you get the page text, text structure, reading order, document layout, and handling for figures, charts, and tables.
Chandra captions figures and charts and parses tables into HTML. With good training, it also handles different languages, scans, and crusty content. A traditional OCR pipeline would need additional stages for document layout, figures, charts, and tables.
When rendered on the page, each block contains its text and content. The localization is surprisingly good. For several years, Joe did not believe VLMs could localize as well as object detectors, despite a co-worker arguing that they could. His co-worker was right. He is now convinced that VLMs can localize and detect objects well as long as the page isn't too dense. You won't get word or character bounding boxes, but you can get content-block bounding boxes.
MonkeyOCR

MonkeyOCR v1.5 comes from a Chinese lab and uses an approach Joe has so far seen only from Chinese labs. One issue with VLMs, especially for OCR, is that the cost of generating tokens isn't linear.
Cost and memory are closer to quadratic because each new token must attend to every previous token. Several architectural changes try to address this. Qwen 3.5 uses linear retention in some layers, but using it in every layer hurts performance.
Another option is to turn the VLM into a pipeline and recover much of that latency. MonkeyOCR first sends the document image through the VLM with a prompt to generate typed regions in reading order and ground them to the page.
The model returns crop locations for tables, images, paragraphs, headers, and formulas. You crop each region and send it back to the same model with a new prompt: OCR this content, parse this formula, or convert this table into HTML. Instead of processing the entire page at once, the model handles one paragraph, formula, or table at a time.
You lose the global view of the document and some performance relative to single-shot OCR VLMs. Latency drops because the model can generate all of the paragraphs in parallel instead of one after another.
MonkeyOCR v1.5 is not the only model to use this approach. The Dolphin OCR family does as well. These models tend to perform worse and have become less popular as people move toward more efficient straight-decoder architectures, but they offer substantial speed gains. A paper on hierarchical speculative decoding uses this approach to speed up single-shot OCR models.

ModelPassesOutputMain tradeoffLightOnOCR-2SingleMarkdown, HTML tables, captions, and LaTeXCheap and fast, with little page groundingChandra 2SingleGrounded Qwen-HTML with semantic labelsRich structure and localization require more output tokensMonkeyOCR v1.5MultipleGrounded regions followed by cropped recognitionLower latency, but loses the global view and some quality
How to choose a VLM

Downstream needs
The biggest consideration for running a VLM for OCR is the needs of the downstream task. Do you need grounding on the page, such as bounding boxes? Some companies are convinced they need character-level bounding boxes. In Joe's experience, content-level bounding boxes, or at worst line-level boxes, are almost always enough.
Ask whether you even need grounding on the page, because you're paying for all those extra tokens. Are you okay with just getting all the content from the page? For instance, Joe's team recently released a big dataset where they collected nearly all the local laws in the United States and processed them from millions of PDF pages. In that case, they knew they were never going to touch those PDFs again.
They needed only the content, so they chose LightOnOCR because it was cheap, fast, and provided structured content in reading order. If the output is going to an LLM, you almost never need the grounding. The next question is what type of data you're processing.
How quickly does it need to be ingested? A real-time document system that needs results within seconds sharply constrains your model choice. With a one-hour, two-hour, or even 24-hour SLA, you can batch large quantities of documents and run a larger, higher-quality VLM.

Test your own data
Another consideration is in-domain quality. Many open VLMs are trained exclusively on born-digital documents because the training data is easy to generate. You can scrape millions of PDFs, pull out their text, approximate each page in HTML, and train an OCR model.
That works until you feed the model handwriting, a bad scan, medical documents, or something else that isn't common on the open internet. To decide whether a VLM is useful in your case, run it on your data and inspect the outputs.
Looking at 50 to 100 pages will tell you whether the model is likely to work. If you do that, you're ahead of 99% of people who are yoloing whatever API is cheapest or easiest to set up. If Textract is poor in your domain, feeding all your documents through it can cost substantial downstream performance in a RAG system.
Looking at your data is also valuable for researchers. Many of the best research ideas come from seeing exactly where a model fails. AI2 noticed that formula parsing into LaTeX is difficult to evaluate because multiple TeX equations can render identically, while two similar-looking equations can render very differently. They developed a rendering-based reward for OCRing formulas and TeX equations and got a large boost in formula parsing. LightOnOCR used the same reward structure in training and handles formulas much better.
Looking at the data can reveal research techniques that other people haven't considered because they haven't seen how badly the model handles formulas or empty pages.
Cost and latency
Prices and licenses in this section were current when Joe gave the talk.
For cost, PP-OCRv6, PaddlePaddle's Apache-licensed pipeline OCR, is as close to free as you can get.
It will run on your phone, much like the OCR built into a Mac. If you want the page structure, a fine-tuned one-billion-parameter model on good infrastructure should cost 10 to 30 cents per thousand pages. That's what Joe's team saw with LightOnOCR-2-1B on Modal, which typically costs about twice as much as prepaying for H100s through AWS. Cloud APIs from Google, AWS Textract, and Azure's OCR service cost between roughly 50 cents and $2 per thousand pages.
Textract is 1.50perthousandpagesatlowvolumes.Afteramillionpagesinonemonth,itdropsto60centsperthousandpages.HostedVLMproviderstypicallyofferhigh−qualityOCRatahigherAPIprice.Mistral′s[OCR4](https://docs.mistral.ai/models/model−cards/ocr−4−0)cost1.50 per thousand pages at low volumes. After a million pages in one month, it drops to 60 cents per thousand pages. Hosted VLM providers typically offer high-quality OCR at a higher API price. Mistral's [OCR 4](https://docs.mistral.ai/models/model-cards/ocr-4-0) cost 4 per thousand pages.
Datalab, which makes the open Chandra and Surya models, charges 4perthousandpagesforitsfastservice.Itsaccurateservicecosts4 per thousand pages for its fast service. Its accurate service costs 10 per thousand pages, the highest price in this comparison. Before paying that, consider whether your task needs that level of accuracy or can tolerate errors from a cheaper model or API.
A self-hosted VLM typically takes a few seconds per page, slower than a pipeline model. Joe has been working on faster decoding and gets about a 1.5x speedup with LightOnOCR without degrading quality. He hopes to write a paper on that soon.
He also released a speculative decoding head for Chandra 2 that gets about a 1.5 to 2x speedup at small batch sizes. You can plug that into Chandra from Hugging Face and get a pretty free latency speedup.
Licenses and hosting
License is a major consideration because each VLM is released under different terms.
For instance, the models released from Datalab, Chandra and Surya, have an OpenRAIL-M license. It is free for you if your organization makes less than 2millionayearorhasraisedlessthan2 million a year or has raised less than 4 million. But once you pass that, you have to pay pretty high prices even to self-host your OCR engine, because at that point you're competing with their own hosted models.
Many other open VLMs use Apache or MIT licenses. LightOnOCR is Apache licensed. GLM-OCR, a recent popular model, is MIT licensed. A startup does not want to end up on the wrong side of a non-commercial license. Some people have an "it's totally okay" attitude, but check the licenses of every model and piece of software you use.
If you are not cost-constrained, use an API. Self-hosting can still make sense, and infrastructure companies such as Modal, Baseten, and Lambda have lowered the bar. Joe has extensive experience with Modal, where containers scale to zero.
Modal makes it easy to self-host many of these models. Joe and Pattern's founders have discussed what they would do if they started over knowing the scale Pattern would reach. They would probably self-host. When Pattern started, transformers and BERT existed, but almost none of today's OCR VLMs did. He has tracked roughly 50 VLM releases over the last six years.
Questions
How do newer OCR models compare?

Isaac: You mentioned tracking about 50 releases. Is that something you can show? What are you tracking them against, and what are these releases getting better at—cost, latency, or accuracy?

Joe is writing a survey of VLM OCR and trying to release a friendly version chunk by chunk. He has tracked models since 2021, starting with TrOCR, the first transformer OCR model. That replaced the text recognizer with a transformer, but since then the field has seen real OCR models that do the full page thing.
Many are built on the Qwen2.5-VL releases. Two main benchmarks compare them. Some models report performance on AI2's olmOCR-Bench. A different, almost disjoint subset reports on OmniDocBench v1.5. OmniDocBench is a Chinese and English benchmark, whereas olmOCR-Bench may be English only.
For models that report both scores, and models he has run on the other benchmark himself, the correlation is strong. A model that performs well on one typically performs well on the other.
The survey also tracks cost, localization, whether the model is multi-stage, performance, and training. MonkeyOCR and Dolphin are multi-stage. Most models with localization return layout boxes, but an older Microsoft model called Kosmos could return line boxes. It came from a period when OCR pipelines commonly used line boxes.
Training is one of the biggest variables: how you collect the data, what size it is, and how you do it efficiently.
What should you store from a large OCR batch?

Question: Could you tell us more about the corpus of local laws and how you store it? You mentioned it went through LightOnOCR, so did you keep the Markdown?

Joe recommends taking all the PDFs, rendering all the pages at once, and storing those rendered images long enough to process them. His team stored seven million images, which ended up being a few terabytes of image data, before running them through LightOnOCR.
Once you've done that, as long as you retain the PDFs, you can delete the images and save those several terabytes. Keep all the Markdown per page and the post-processing that merges pages and extracts the laws separate. That pipeline is not fixed. The dataset contains cases where two laws were merged but should not have been.
Which PDF renderer should you use?

Question: How did you go from PDF to image? What did you use for that processing?

This choice also involves software licensing. Many people looking for PDF-to-image software reach for PyMuPDF. Joe would not use it inside a company without understanding the license. PyMuPDF is maintained by Artifex and uses AGPL-3.0 for open-source projects, with separate commercial licenses for proprietary applications.
There is a better open option called pypdfium2, which wraps Google's PDFium. It has a Python API and is easy to use. You render a bitmap and use Pillow to convert it to a JPEG. It is slower than PyMuPDF, but avoids that AGPL licensing issue.
Are VLMs a good fit for architectural drawings?

Question: We are dealing with architectural drawings and PDFs of home plans. A plan could have 100 pages, but these are one-off jobs, so scale is not a major constraint. The plans can change over time, and some feel like detailed drawings layered on top of each other. Have you worked with anything similar?

Architectural drawings are the bane of Joe's existence. He used to work on form-field detection, including automatically placing PDF form fields. Architectural drawings trigger vision systems constantly because they contain so many lines. You have to add a lot of negative examples to stop that from happening.
Some drawings also have checklists that you need to catch. A VLM for OCR might put you at a disadvantage here because many models will return the whole drawing as one figure box and omit its contents. dots.ocr from RedNote attempts to deconstruct and caption images and turn charts into structured output. At a small enough scale, you may be better off taking the figure box and sending the crop to Gemini or another larger VLM with a good prompt.
In Joe's experience, Gemini is a surprisingly good document processor. He has experiments from his job that he can't show, but it is far better at handling document images than Claude and GPT. It might be bad at agent coding, but it is good with documents. Gemini 3.5 Flash was even better than 3.1 Pro, so you could save money and use Flash.
How should OCR handle slides with text and images?

Isaac: Another member needs to process medical slides and find the relevant flashcards. The slides contain text, images, and repeated cruft such as logos and headers. Some images matter only in the context of the nearby medical material, and the output has to remain scoped to what the student should study. How would you approach this document?

Document layout analysis typically classifies page numbers, repeated logos, and templates as artifacts. Whether they appear in the output depends on the model. LightOnOCR tries to remain faithful to the page and returns all of them.
Chandra and Surya drop artifacts by default and are tested on their ability to do so. For slides with repeated cruft, one of those models may save you from removing it later.
The harder choice is whether to OCR the content inside an image or return only the image's bounding box. A pipeline can detect the full image, then send any crop containing text through PaddleOCR to recover the text boxes that the original VLM omitted.
dots.ocr attempts to return text from inside images by deconstructing them, so you may have a better shot with that. When you aggregate the content, you're limited by the quality of the orchestrator model. The image of the eye will probably have a caption. You can feed that caption to the orchestrator and let it reason about whether the eye belongs with the nearby material about jaundice.
Instead of working only with the images, you can pass the caption or the cropped region and say, "Any of these image crops could become a flashcard."
