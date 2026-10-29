reel: https://www.instagram.com/reel/DfAVR6MtdFR/
captured: 2026-10-29
yt-dlp: 2026.10.26
ffmpeg: 7.0.2-static
faster-whisper: 1.2.1
ctranslate2: 4.8.4
claude: 2.1.281 (Claude Code)

## Caption

What does an OCR router look like? How do you do error analysis on an multi-step OCR router?

I walk through a simple LiteParse → Docling → Qwen router, and inspect traces to evaluate how the routing steps and models do. We'll look at both successes and failures.

Then we'll discuss a more advances approach using small regression models to predict when a bigger model is worth using.

## Transcript

[   0.0] When extracting information from PDFs, generally a big more expensive model gives more accuracy
[   5.0] but it costs more money and time. OCR routing setups give you the best of both worlds.
[  10.3] Cheap and fast models for all the easy stuff, and then route to a larger, more accurate model
[  15.3] when it makes a difference. For example, some pages need a quick text extraction and don't
[  20.7] even need OCR at all. Others have really dense tables, scans, charts, and images.
[  25.7] So we can start with a cheap method, check the output, and then decide whether to stop
[  30.3] or send the page or just part of the page to another model that is more expensive.
[  35.4] We'll look at every step of a simple router through a document,
[  39.0] and then we'll look at examples that show common router failure modes.
[  42.2] After that, we'll look at how OCR lamps often train small regression models
[  46.6] for more accurate routing. We're going to start with this two page PDF.
[  50.5] Page one is basically all text, so it should be extremely simple.
[  54.2] And then this next page of the document is a fairly complicated table with
[  58.4] merge cells and different hierarchies. Let's start with page one PDFs can contain both images
[  63.9] or the actual text. If the text is there, we can pull it straight out of the file without
[  68.1] needing an OCR model. An open source tool called light parse can do this and it's a great first
[  73.2] step for a router light parse will extract the text from documents and optionally OCR
[  79.0] with test track. We don't need the OCR part. So we'll leave that off. And this is a great
[  84.3] place to start here. We see our PDF side by side with the output from light parse.
[  90.2] As we annotate, we can see that light parse extracts the text almost perfectly.
[  94.9] It's missing the page number. And there's also one missing dash.
[  98.6] But overall, this would work great for almost every use case. And importantly,
[ 102.6] it's extremely fast and cheap. In this view we see on the left is our original PDF
[ 108.6] with bounding boxes highlighting where the errors are. On the middle, we still have our light parse
[ 114.4] output. And on the right, we have our notes where we're writing what the issue is that goes to these
[ 119.2] bounding boxes. We'll do this for more and more steps of the router so we can see exactly what
[ 124.5] problems there are in each step, and whether it makes sense to escalate it to a bigger model.
[ 129.2] After light parse, it goes to the routing step, we can see at the top, we're at the page
[ 133.7] routing step in the three step router. Since we're happy with the light parse outputs,
[ 137.4] we wanted to decide not to send it to a larger model. In this router, the rules are deterministic
[ 142.8] checks code. In addition to light parse extracting the text, it also does fast checks to kind of
[ 148.2] guesstimate if there's tables, cells, if you have embedded images or if there's a complex
[ 152.6] layout. If we see those, then we'll want to escalate it to an OCR model. In this case,
[ 157.8] it correctly identified that it's just a simple parge and light parse outputs are
[ 162.3] sufficient. That's why they all say not triggered. Now let's go to page two and walk
[ 166.4] through the same steps. This is the table. So it's a lot more complicated. First, our router processes
[ 171.8] it with light parse. As we look at the output, we see that creditor, multilateral, World Bank,
[ 177.6] total, all of those are not in the table. This should be in the left column of the table,
[ 183.4] but they're showing as text above it. In addition, cells get mangled, and it also
[ 188.8] incorrectly breaks the table into two and makes some cells of the header a new table.
[ 193.3] This is just totally broken for a lot of reasons. And there really isn't any use case
[ 197.7] where this would be okay to use. Now we can look at the page routing checks. In this case,
[ 202.4] we wanted to decide that it needs an OCR model, because the text extraction failed,
[ 207.2] we got the information, but it was too mangled. Our rules do trigger it due to sparse text,
[ 213.7] complex layout, and a table presence, several of these simple checks triggered. So the page
[ 218.7] gets routed to the next step. So page one was simple enough, didn't need another step,
[ 223.4] it stayed with light parse. And page two is being correctly identified as needing additional work.
[ 228.7] The next step in our router is docking, which is a document processing pipeline by IBM.
[ 234.3] Dockling did a much better job at keeping the table together, as we see, but there's
[ 238.8] still some issues. For example, the 0.1 and 100 should be in two different cells,
[ 245.4] but the output put them in the same cell. And even when we go to the raw output instead of the
[ 250.5] rendered version, we see it here with two values in one cell separated by a space. While this is much
[ 256.4] better, and we're seeing more targeted errors, it still isn't good enough to be useful. So
[ 262.2] hopefully our router is going to decide to send it somewhere else. In this case, we have different
[ 267.0] routing criteria. It ran with dockling. So we need to look at docklings output for the
[ 271.2] routing decision, instead of the light parse output. In this router, there's a deterministic step,
[ 277.0] looking for multiple numbers in one cell. This triggered based on the exact error we saw in the
[ 282.7] table, a number, a white space, and then another number in the same cell. So we move on to the
[ 287.9] next step. The next step crops the table based on the bounding box. So this is the most expensive
[ 293.7] model that needs a GPU that only is used to process problemaries and not the entire page.
[ 301.4] The text above the table isn't in this crop. This is just the area with the problem. And we send
[ 306.6] that to Quinn. In this case, it happens to be most of the page because the table takes up most of the
[ 311.4] page. But it could be a much smaller crop in different examples. And now we look at Quinn's
[ 316.1] output, we've gotten much better results than dockling. But we still have a small error,
[ 320.8] which could be a big deal. The values 8.2 and 9.8 should be in the 20 47 row,
[ 328.2] they're moved up one row. And this could be easy to miss if you weren't checking carefully.
[ 332.6] But this router has reduced our costs significantly from using Quinn on every page. And it's
[ 338.1] increased the accuracy significantly from using light parse on dockling alone. Even with the router,
[ 345.0] we still need error analysis, because there's just no silver bullet. Well, you can check out
[ 349.4] my video on error analysis and OCR, as well as my guide on formative and summative evals
[ 354.8] for deeper dives on that. Once Quinn has crossed the crop, its table gets put together with the
[ 360.5] surrounding text. The Quinn table replaces the one from dockling or light parse. So that's the
[ 365.7] routing flow, you process it, check it, decide whether it needs another step. So we've seen
[ 370.6] one page stop right after text extraction. And another page goes through every step. So
[ 376.2] now we're going to look at some cases where router breaks. These are like common failure
[ 380.2] cases I see in commercial systems. Here's a bill where I would have expected the router to try Quinn.
[ 386.6] There's so much visual structure and a complex layout, it seems very clear a vision model is
[ 391.0] going to be needed. light parse extracted the text and it totally failed. But that's fine. It's
[ 396.1] fast and it's cheap. That's why it's the first step. The routing step correctly identified
[ 400.2] that it needed to go to the next step. And that's the correct routing decision. So it did
[ 404.6] go to dockling. After dockling, it went straight to the final output. And this is because
[ 409.3] all the information is there but it is super weird. We should be looking at all the information on
[ 415.0] the top card before going down the bottom card. But it goes down the left side before jumping
[ 420.9] back up to the first card. And also the service address needs to be connected to the actual
[ 425.5] address but it's not. They're broken up by a lot of stuff same error on most other values.
[ 430.8] We see service address and then it goes into load zone. This 705 999 ID pay this amount and then now
[ 441.0] we have the actual service address. And so it's very hard to connect service address label
[ 447.9] to the actual address. There are many more issues but these two are already deal breakers.
[ 454.6] So from here, this is where you'd say, Okay, how do I create a routing rule for this?
[ 460.1] In some cases you could be very deterministic. For example, if you're working for National Electric
[ 466.2] and you are OCRing historical invoices to reconstruct history, you can identify National
[ 472.5] Electric invoices have a very targeted rule because you know you're going to get a ton of
[ 477.3] these formats. If you're building a product where anyone can upload any kind of invoice,
[ 482.9] then you need to scan it accurately and you need to be a bit more creative.
[ 487.0] We're going to look at regression models for advanced routing soon. But as always,
[ 491.4] the end use case matters for these decisions. So let's look at one more error and then we'll
[ 496.2] go into regression models. In this table, the final output looks great. Dockling did a perfect job.
[ 503.0] This means the rule to skip Quinn was a good call because it would have been
[ 506.7] extra cost when docking did good enough. So now we need to know was going to dockling
[ 511.8] required. To do that, we need to look at light parse and see if light parse did good
[ 516.2] enough light parses output is a little bit less structured than docklings if you look really carefully.
[ 521.4] But it's all very clearly in a table without errors. It preserved the information without OCR
[ 527.0] at all. Like par said, there was sparse text in a table with a complex layout. And that complex
[ 532.4] table check was made a trigger. But this was simple enough that light parse did just fine.
[ 537.1] We did not need to go to dockling. So this type of error didn't hurt accuracy,
[ 542.1] but it increased your cost and latency. And that covers the two main routing errors. The first
[ 547.5] was it didn't escalated when it needed to and escalating when it didn't need to. Okay, so what
[ 554.5] I showed you was a basic deterministic rule based router. To improve it, we could keep adjusting
[ 558.8] those rules to handle more edge cases, and fix these errors. But another option is to learn
[ 564.2] from examples, using a small traditional regression model. To do a routing properly,
[ 569.6] what I really need to know is how much more time will the next step take? And what's the accuracy
[ 576.3] improvement I will get for that. If I knew those two things, I could define a nice trade off an
[ 581.4] almost perfect one. And so that's what we're going to try and predict. To train a model,
[ 585.4] we need labeled data, which is basically just model inputs with the correct answer attached to
[ 590.4] them. To create the correct answers, we can process the same source documents with two models.
[ 595.5] First, we run them through a small model like Tesla act, and we measure accuracy and latency for
[ 601.3] each document. Then we're going to do the same thing with a large model like Quinn, and we're
[ 606.2] going to measure accuracy and latency for each document again. So every document in our data set
[ 612.3] went through both models, and we have latency and accuracy for both models on on every document.
[ 618.1] The goal is to end up with a small table like this. For every document, we have the small
[ 623.0] model's latency and accuracy and the large models latency and accuracy. In this case,
[ 628.7] document a goes from 60% to 80% accuracy. And so 80% minus 60% means there is a 20 percentage
[ 637.0] point gain. And it goes from one second to two second latency, so that accuracy costs us one
[ 642.4] second in latency, document B goes from 70 to 75% accuracy for a five pp gain,
[ 648.5] and also costs two seconds of latency, so two seconds to four seconds. And that's what we
[ 653.4] want to predict. If I get a new document and process it through a small model, how much improvement
[ 659.4] will I get from running it through a large one and how much more time will it take? Now that we
[ 664.9] have our targets, we need features we can use cheaply. If the routing model takes anywhere
[ 670.2] close to the time or cost of the larger OCR model, we lose all the benefits of routing,
[ 675.1] and we may as well just use the expensive OCR model. So we need inputs that we can use
[ 680.1] very cheaply when we're processing a document. So we take the document and the small model's output
[ 686.3] and we extract features we can use to make those predictions. For example, we could use page width
[ 692.2] and height aspect ratio, we can use confidence scores from Kesseract, or simple test statistics
[ 698.1] like word count line count awards per line. We can also use guesses at structure like we saw
[ 703.6] with light pores, row and column counts, whether the merge spans are present in the fraction of
[ 708.8] empty cells. All of this is described in a blog post that reducto recently did talking about
[ 713.7] their OCR routing setup. And so these are features that dedicated OCR labs are using to create
[ 719.4] these routers. And those features are our inputs. The improvements and at a time we measured
[ 724.8] are our training targets. We can use that data set to train a very small regression model
[ 729.7] like a gradient boost to tree, it's kind of like data science ML staff back from the
[ 733.9] pre agentic LLM days. If you were in data science, it's time. So we train two predictors,
[ 739.6] one to predict the accuracy gain, and one to predict the added time and document a we're
[ 744.9] predicting that 20 percentage point gain the 80% minus 60%. If we've already run a small model,
[ 751.4] and the larger model takes another two seconds, the added time is two seconds. So to recap,
[ 756.9] we want to model, we have our inputs, text count, confidence scores, tabular data, and our output
[ 764.8] is the increased accuracy and increased latency, it will cost. Now we've trained these regression
[ 771.5] models, our router looks like this. For each new page, we run the cheap step the small model,
[ 776.9] and we use that output to create the features that are fed into our small regression model
[ 782.3] routers. We use the predictions to decide whether that expected improvement is worse
[ 786.4] that extra time for our budget. If so, we route it to the larger model. If not, we're done. The
[ 791.8] routing model being super small and fast is important. We could make a more accurate router by
[ 797.2] taking the entire output of step one is text, or even the whole PDF is an image to predict the
[ 802.8] gain. But if we do that, then the routing step is so expensive, we could have just run the
[ 807.2] bigger OCR model to begin with. That's why we use these light tabular data statistics
[ 812.5] and use those as features. With this new router, we still need to do error analysis just like we
[ 817.6] did by looking at real examples and annotating the deterministic router. We do the same thing
[ 824.3] with this better model. The annotation is where you're going to build all the intuition and get
[ 829.4] the best and most successful ideas for how to improve your OCR process. I would recommend
[ 834.5] going through the process several times because this is where you're going to build intuition about
[ 838.9] is dockling the wrong step in this pipeline or is it close? What are the issues that dockling has
[ 844.6] had with this? When does it need to escalate? What other patterns or routing steps should I
[ 848.8] add? For example, if you see clear enough patterns in dockling the Quinn exclation,
[ 854.1] can you skip the routing step and go straight from light parts to Quinn? Or do you need
[ 858.1] dockling output to identify those patterns? I'll leave the OCR annotation and formative
[ 862.7] and summative eval posts that I mentioned earlier in the description. I hope you enjoyed this,
[ 868.2] and if you want to stay up to date on all my upcoming material, subscribe at IsaacFlath.com
[ 873.0] slash subscribe

## On-screen text

SUMMARY ... [PDF page 1 text] ... [PDF page 2: table with creditor/multilateral/World Bank/total rows] ... customerelectric [utility bill with red-boxed annotated regions] ... [trace/diff view with highlighted text lines] ... When is a bigger model actually better? A practical framework for model routing ... Output -> Features -> Regression Models -> Accuracy gain -> Added time

## Key claims

- A bigger, more expensive OCR/model generally gives more accuracy but costs more money and time; routing lets you combine cheap/fast models with accurate/expensive ones.
- A 3-step router (LiteParse -> Docling -> Qwen) is demonstrated on a 2-page PDF: a simple text page stops at LiteParse, while a complex table page escalates through all three steps.
- LiteParse extracts native PDF text without OCR and is extremely fast/cheap; it worked almost perfectly on the simple text page (missed only a page number and a dash).
- Deterministic routing rules use fast checks (sparse text, complex layout, table presence, merged cells, embedded images) to decide whether to escalate a page.
- On the complex table page, LiteParse badly mangled the table (misplaced row labels, split the table), triggering escalation to Docling.
- Docling preserved the table structure much better than LiteParse but still merged two numeric values into a single cell, triggering escalation to Qwen.
- Qwen is the most expensive step and is only run on a cropped bounding box (e.g., just the table) rather than the whole page, to save cost.
- Qwen produced much better results than Docling but still had a minor error (two values shifted to the wrong row), showing no step is perfect and error analysis is still required even with a router.
- Common router failure modes include: failing to escalate when needed (e.g., a visually complex bill where Docling output looked structurally plausible but mixed up label-to-value associations) and escalating when not needed (e.g., a table where LiteParse's output was already correct, so routing to Docling added cost/latency without accuracy benefit).
- For narrow, known document types (e.g., one company's invoices) deterministic rules can be targeted; for open-ended/general document types a more flexible approach is needed.
- A more advanced approach trains small regression models (e.g., gradient boosted trees) to predict accuracy gain and added latency from escalating to a larger model, using cheap features (page dimensions, OCR confidence scores, word/line counts, row/column counts, merged-cell presence, empty-cell fraction) derived from the small model's output.
- Training data for these regressors is built by running the same documents through both a small model and a large model and recording the accuracy and latency delta for each.
- The routing/regression model itself must be cheap and fast relative to the OCR models, otherwise the benefit of routing is lost.
- Reducto's blog post describes similar lightweight features used by dedicated OCR labs for routing decisions.
- Iterative error analysis/annotation of router traces is essential for building intuition about which steps are failing, which escalation rules to add, and whether intermediate steps (like Docling) can sometimes be skipped entirely.

## Info channel

spoken

## Mentioned (unverified hints)

- LiteParse: (no url)
- Docling: (no url)
- Qwen: (no url)
- Tesseract: (no url)
- Reducto (blog post on OCR routing): (no url)
- IsaacFlath.com: IsaacFlath.com/subscribe
