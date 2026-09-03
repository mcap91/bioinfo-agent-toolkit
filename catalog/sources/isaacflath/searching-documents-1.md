# Searching Documents (Part 1) — Isaac Flath

Indexing, chunking, retrieval, filtering, and ranking.

---

# What Actually Improves PDF Retrieval?

**URL:** https://isaacflath.com/writing/what-actually-improves-pdf-retrieval

Note from Isaac: Searching quickly over documents and PDFs is one of the most asked questions I get. Many agent harnesses and tooling rely heavily on grep/rg, which doesn't work well with PDFs. You can OCR documents into text files, then use text based approaches. But that starts to fall apart in tables, and continues to get worse as you have diagrams, figures, maps, charts, and other things that are hard to express in text. This post compares options for searching over PDF documents, from text based keywords, to visual single & multivector approaches, to visual reranking, to managed vendors.
That's why I am so excited about the work that Antaripa did when she wrote this blog post. It shows tangible options for a super common problem people face.

Most PDF retrieval pipelines extract the text, split it into chunks, embed those chunks, and retrieve the closest ones for a query. That works well when the document is mostly clean text and the answer appears in one paragraph.
Visually rich PDFs are harder. Charts, complex tables, section hierarchies, text inside images, and values spread across rows and columns can lose their meaning during extraction.
In an earlier experiment, I compared several ways to search these documents. This follow-up tests how retrieval changes across lexical and dense text search, text and page-image embeddings, and single-vector and multivector representations.
Google Colab experiment: Google Colab

Retrieval approaches
I tested six retrieval setups:

BM25 over OCR text: Keyword search over text extracted from each page. OCR, or optical character recognition, turns page images into text.
Dense embeddings over OCR text: Semantic search over the same extracted text, using one vector for each page.
Visual single-vector retrieval: The model receives the page image and represents the entire page with one vector.
Visual multivector retrieval: The model keeps many vectors for different parts of the page instead of compressing everything into one.
Managed multivector retrieval: Mixedbread handles the embedding, storage, indexing, and search.
Visual reranking: A second model examines the query and retrieved page images, then reorders the results.

These comparisons answer two separate questions:

Does using the page image help?
Does keeping several vectors preserve useful details that one page vector loses?

Dataset and evaluation
I used the English finance corpus from ViDoRe V3, a benchmark for testing whether RAG systems can retrieve evidence from visually rich financial documents.

While the full dataset has ~ 3000 report pages, I used a subset with 80 queries and 1,200 pages from six financial reports.
Each query has good human-verified results, so I could measure whether a retriever found the correct data for the query.
The original page images were all 1,700 by 2,200 pixels. I resized them to fit within 768 pixels on the longest side before sending them to Jina, Voyage, and Mixedbread. I used the same 80 queries, relevance judgments, and evaluation code for every method.
I measured four properties. All four scores range from 0 to 1, and higher is better:

nDCG@10: Are the most relevant pages near the top?
Recall@10: How many relevant pages appear in the first ten results?
Recall@50: How many relevant pages appear in the first fifty results?
MRR@10: How quickly does the first relevant page appear?

Recall@50 matters when the system retrieves a larger candidate set before reranking. It does not mean all fifty pages have to go into the model's context.
BM25 baseline
I started with BM25 over Markdown text extracted from each page.

MethodnDCG@10Recall@10Recall@50MRR@10OCR BM250.54380.58080.81090.7044
BM25 did better than I expected. Financial reports (and other technical documents) use specfic terminology like "net income," "share repurchase," "total revenue," and "cash flow." Queries also use company names and years that are often directly on the relevent page. Keyword matching like BM25 are great for exact matches.
One query asked:

Compute the summation of the net income and share repurchase program of Citigroup in 2024.

BM25 ranked some pages from JPMorgan highly because it has very high keyword overlap with terms like "share repurchase" and "capital actions." It did find the relevant Citigroup page, but it wasn't always the most relevant page.
BM25 weighs each word equally regardless of the surrounding words, so it does not account for things being the right company, year, and financial concepts as higher priority. BM25 does weight words differently but that is only based on how commonly they appear in the dataset and not using context of surrounding words.
Dense OCR retrieval helped, but it was still bounded by the text representation
The next step was Jina OCR single-vector retrieval. The page input was the same OCR-derived Markdown, but each query and page became a dense vector.
This improved every metric over BM25:

MethodnDCG@10Recall@10Recall@50MRR@10OCR BM250.54380.58080.81090.7044Jina OCR single vector0.57970.61440.86500.7216
The biggest gain was Recall@50. That shows the dense text model found relevant pages that lexical search missed. The smaller gain in MRR@10 shows BM25 was already placing a relevant page near the top for many finance queries.
Dense OCR retrieval adds semantics, but it is still searching over whatever the parser extracted. If the parser flattens a table so values no longer match their row and column labels, the embedding model never gets the right information.
Jina's first visual result was a surprise
I expected Jina multimodal embedding retrieval (seeing the page as an image) to be an improvement over Jina OCR retrieval (only seeing the text on a page). It did not.

MethodnDCG@10Recall@10Recall@50MRR@10Jina OCR single vector0.57970.61440.86500.7216Jina visual single vector0.57740.63380.83720.6861
I embedded the PDF pages as images using Jina's multimodal model, which supports both text and images. The image input improved Recall@10, but nDCG@10 stayed almost the same and both Recall@50 and MRR@10 dropped.
The visual model could see layout, tables, headings, and nearby labels, but it still compressed the entire page into one vector. Changing the input from OCR text to a page image let it represent everything on the page, but a single page vector may be compressing details too much for complex and precise documents
Voyage showed that single-vector visual retrieval can still be strong
Voyage Multimodal 3.5 single-vector retrieval was much better:

MethodnDCG@10Recall@10Recall@50MRR@10Jina visual single vector0.57740.63380.83720.6861Voyage visual single vector0.63830.67500.88160.7691
Voyage was the strongest single vector model in the experiment. Its nDCG@10 was close to the Jina multivector run, and its scores were much higher than Jina visual single vector retrieval.
Voyage's a model trained to represent document screenshots can produce a strong page embedding, even when it returns only one vector. It would be interesting to explore if Voyage is stronger across the board compared to the Jina model, or if there's something about this domain that makes Voyage excel.

What multivector models change
The Citigroup query needs lots of details to line up: the company, the year, net income, the share repurchase program, and the requested calculation.
A single-vector retriever (like we've tried so far) represents the entire query and the entire page with one vector each. It's fast, but details can get compressed away.

A multivector retriever keeps many representations for different parts of the query and page. One part of the query can match "Citigroup," another can match "2024," and others can match the two financial terms.

Clarification: The term "Multi-Vector" for retrieval was used for ColBERT style models. A few years later, LangChain popularized the use of Multi-Vector retrieval as a term for a competely different retrieval concept. We are discussing multi-vector embedding models in this post.

MaxSim finds the best page match for each part of the query and adds those matches into one score. A page ranks well when it contains evidence for several parts of the question.
The tradeoff is that the system has to store and compare more vectors.
Jina single-vector versus multivector retrieval
Both runs used page images and Jina models, but the multivector version improved every metric.

MethodnDCG@10Recall@10Recall@50MRR@10Jina visual single vector0.57740.63380.83720.6861Jina visual multivector0.64800.70520.89320.7754
This supports the idea that keeping more page detail (by using more vectors to represent them) helps. A page is relevant because lots of specific details appear together: the company, year, a metric, a table, a note, or a heading. By have each token (vector) in the query match to a specific best token (vector) in the document, it can match these concepts from the query exactly to a place in the document.
Mixedbread showed what a managed multivector system can do
Mixedbread Wholembed v3 had the strongest results.

MethodnDCG@10Recall@10Recall@50MRR@10Jina visual multivector0.64800.70520.89320.7754Mixedbread Wholembed v30.70710.73640.95270.8379
The Recall@50 was almost perfect. Mixedbread retrieved almost all relevant pages within the first 50 results.
However it's not a completely fair comparison. Mixedbread is a managed retrieval system so the results from mixedbread includes its embedding model, storage, indexing, and built-in ranking pipeline.
However, from an engineering time perspective it's easier to set up because MixedBread does all that for you. It's a great option to test if quality is a priority, and you do not want to invest in the infrastructure yourself.
I also tried LightOn as a reranker
Rerankers are more accurate because all calculations happen in the context of the query, but it's slower because you cannot cache/save the document embeddings ahead of time. I used LightOn MonoQwen2 VL as a reranked over the top 20 candidates from Jina multivector retrieval and Mixedbread.

MethodnDCG@10Recall@10Recall@50MRR@10Jina visual multivector0.64800.70520.89320.7754Jina multivector + LightOn rerank0.65830.69280.89790.8111Mixedbread Wholembed v30.70710.73640.95270.8379Mixedbread + LightOn rerank0.70000.73440.95270.8313
This made the first relevant page show up sooner (MRR improvement) and the top results were ordered better (nDGC improvement). However, Recall@10 dropped, meaning less relevant pages were in the top 10 results.
Whether this is "better" depends on the product and the use case. For a simple fact lookup, just having the first relevant page could be the #1 thing that matters. If it's a analyst assistant or research report where it should combine and compare data from many pages, lower recall could mean it misses details and gives an incomplete answer.
The LightOn reranker slightly reduced Mixedbread's scores, so the ranking that their managed system was doing was already better.

Tip: If you implement a reranker, look at the first-stage recall first. They are (re)ranking things from the first pass, so if recall is low on the first step the re-ranker never sees the data and has no chance.

Here are the final dev results:

MethodnDCG@10Recall@10Recall@50MRR@10Mixedbread Wholembed v30.70710.73640.95270.8379Jina visual multivector + LightOn rerank0.65830.69280.89790.8111Jina visual multivector0.64800.70520.89320.7754Voyage visual single vector0.63830.67500.88160.7691Jina OCR single vector0.57970.61440.86500.7216Jina visual single vector0.57740.63380.83720.6861OCR BM250.54380.58080.81090.7044
What I would take from this

For mostly clean text, start with BM25 and dense OCR retrieval. BM25 found many of the right pages, and dense OCR improved on it.
For PDFs with tables, charts, forms, screenshots, or complex layouts, test visual retrieval. Do not assume page-image embeddings will automatically beat text. Jina's visual single-vector run did not.
If a visual single-vector model meets your eval target, keep the simpler system. Voyage performed well in this experiment.
Move to multivectors when the missing results depend on several details appearing together. That includes dense tables, scientific figures, forms, invoices, slide decks, and any document where layout carries meaning.
Add a reranker after inspecting what the first stage misses. The LightOn run improved the first hit without improving recall.

Limitations
This was a dev-subset experiment, not a full benchmark. The run used 80 queries and 1,200 pages.
The notebook focused on retrieval quality. It did not produce a controlled comparison of storage, indexing time, query latency, or API cost.
The Mixedbread result covers a managed system rather than an isolated model. Jina and Voyage embeddings were also generated through APIs.
Image resizing may have affected visual retrieval, especially for small text in financial tables.
I also attempted a ColQwen2.5 run. A checkpoint loading problem in the local environment produced scores that were effectively random, so I excluded them rather than include a misleading comparison.
Next, I would split the queries into table lookup, numerical comparison, chart reading, multi-page synthesis, and plain text lookup. That would show which method helps with which kind of question instead of hiding those differences in one average score.
References

ViDoRe V3 paper and Finance English dataset
ColBERT paper, which introduced late interaction and MaxSim scoring for text retrieval
Jina Embeddings v4 paper and model card
Voyage multimodal embedding documentation
Mixedbread's account of multimodal late interaction at scale
LightOn MonoQwen2 VL model card

---

# Query Disambiguation

**URL:** https://isaacflath.com/writing/query-disambiguation

The missing context behind a simple request

"Make a workout for me."

To give that user a good response, a lot of information has to go into it. We may need to know:

How much time do they have
Do they have any injuries
What workouts do they enjoy (cardio, strength, boxing, etc.)
Are they a beginner or advanced?
What did they do recently? (if leg day was yesterday that should effect today's workout)
Goals (bodybuilding vs marathon runner workouts are very different)

There's a ton of information that we need to get out of the user in order to answer the simple question.
Some of this can be answered by your product. Couch to 5K knows users are training for their first 5K because their entire product is focused around that. So they can make a lot of assumptions immediately. In other cases, like Chat GPT, you can't make those assumptions. The product still has to get this context from somewhere in order to give a good answer.
When a trace produces a bad output, I first determine whether the model generated something poorly or followed a reasonable assumption that the user did not share. The first may require a better prompt. The second requires more context.
Products can gather that context before the request, during the agent loop, or from the user's reaction to early results.
Product patterns for disambiguation
Let the user set relevance
AnkiHub provides relevant flashcards to medical students. Students can upload a powerpoint from a lecture, type text, or upload PDF notes or book sections.
But different students want different results. Some want only the flashcards explicitely mentioned in the material. And some want related topics that aren't covered but might make sense to study at the same time anyway.
In AnkiHub's operator review, domain-expert annotators said their judgments could vary by as much as 90%, depending on how they interpreted the query. That kind of disagreement is a signal to inspect the interpretation before changing the model or prompt.
AnkiHub uses a slider that lets users set how strong the relevance should be. The problem is that the difference between 75% and 50% may not be obvious. What do those numbers mean in your product? Use sliders when you need them, but not by default.
Sliders work well for ankihub because students will find the settings they like as they upload dozens of lectures per week.

Make the relevance criteria visible
Ai2's Paper Finder shows what it considers relevant after a search. It breaks the query into criteria such as dataset introduction, unscripted dialogue, two speakers, and English language. Each result gets a green, orange, or red marker for each criterion.
This shows the user how the system interpreted the query and how each result maps to it. If a result is wrong, the user can see what the system misunderstood, sort the results, and refine the next query instead of guessing.

Give the user a map
NotebookLM can turn one or more uploaded documents into a map of categories and topics. You can expand a category and select a topic to scope the query. Instead of forcing me to write a precise question about a document I may not understand, it shows me how the document is organized and lets me point to the part I want.

Show the plan before a long run
OpenAI Deep Research creates an editable plan before it runs. It might propose querying the literature, looking for UX patterns, collecting sources, and examining evaluation methods. If it misunderstood me, I can edit or cancel the plan before starting the research.
Putting the interpretation up front makes sense for a long-running task. A quick check can keep the user and the product from spending 5+ minutes on work on the wrong thing.

Compile natural language into a query
Censys lets technical users enter plain English, such as "hosts running SSH on a nonstandard port," and compiles it into a structured query. I can see that it interpreted "nonstandard" to mean "not port 22" and confirm that interpretation before searching.

Ask for missing information in the loop
I asked Lovable to create a beautiful landing page. Before generating it, Lovable asked what product the page was for and let me type an answer. Then it gave me options for visual direction, which may help someone who doesn't know how to describe a visual style.
I like this better than putting a large form before the first request. The flow says, "Put in whatever you want. It's okay if it's underspecified." The agent finds what is missing and asks only the relevant questions.

Generate several directions
I asked Spiral to write an article about loops in different programming languages. It returned three quick drafts with different angles: design philosophy, an off-by-one problem, and a side-by-side comparison. I could click one to read it in detail and pick.
Instead of asking enough questions to produce one polished draft, Spiral lets the user react to several directions. The user can choose one, give more instructions, or ask it to blend them.

Let the user point
A common request about a rendered page is, "For this table, I don't want it to have so much color." If the page contains several tables, describing the location can be imprecise.
The Codex app lets you click an HTML element, attach a note, and send both to the agent. Pointing is easier than describing the location and ensures the model knows which part of the page I mean.

Decide where to collect the context
If the missing information will matter repeatedly, collect it during onboarding or save it as a default. If it is specific to the current request, ask in the loop with a text box, a small set of choices, or several sample outputs. Too many fields, buttons, and sliders make the product clunky, so make the correction as easy as possible.
Keep inspecting traces for reasonable interpretations that did not match what the user meant. Those are ambiguity errors, and they show you what the product still needs to learn or ask.
Questions
What about e-commerce search?

Question: The examples so far are chat applications that can ask follow-up questions. What about e-commerce or delivery search, where the query is still ambiguous but a long agent loop may not fit?

Some personal data can be saved instead of requested every time. If I am searching for pants, the site could already know my size and gender. That can come from onboarding, but a store with Amazon's scope cannot ask 150 questions about every kind of product.
Without an agent loop, you are limited to information collected before the request and controls such as text boxes, filters, and sliders. Navigation also provides context. An agentic search could go further and show three or four examples for the user to choose among.
But, the extremely broad scope still makes disambiguation difficult, so Amazon relies on a fast search loop. Result presentation helps. Paper Finder exposes its criteria, and Amazon exposes product images, so users can scan many results and see a mismatch quickly. If I search for tables and see only coffee tables, my next query becomes "dining room table." That is much less frustrating than opening a bunch of results before discovering the same mismatch.
How do you handle a topic change over email?

Question: How should an agent handle a user who changes topics in the middle of an email thread, where you cannot present the same UI controls? Could a small model detect the change and ask whether to start a new thread without feeling robotic?

Warp did something similar. It is part terminal and part agent CLI, so it detects whether an input is a shell command or an agent request. It could also notice a topic change and recommend starting a new thread.
Email makes this harder because each turn may take a minute or a day. You want to limit follow-up questions, and sending the user to a form may feel awkward. I would detect the probable topic change without creating a new thread, because two requests that look unrelated can share context.
For example, someone discussing a talk might suddenly ask for a VSL strategy because they want to promote that talk. The agent could say, "It looks like you moved from this topic to that one. I'll answer the new question." If the topics are related, the user can clarify the connection, and the user doesn't have to re-explain the context. Cheap models already name threads in tools such as Claude Code, Codex, and Amp, so the same kind of classification could support this behavior.
Can memory reduce repeated questions?

Question: I am building a product for CPAs, and research assistants keep asking the same questions without getting to know me. Have you seen anyone use memory well enough to reduce those repeated menus?

I have not seen a commercial product where I love how the memory works. You can create skills automatically, template prompts, or retrieve stored context, and retrieval has improved. But preferences change over time and between projects. My writing style for a public blog post is intentionally different from how I write inside the community.
Memory is another word for retrieval (find the right context at the right time). And when context is completely auto-generated without any human intervention it tends to get worse over time.
What should be deleted and when? What should be updated? Which pieces are more important than others in case on conflicts?

---

# Quantization for ColBERT

**URL:** https://isaacflath.com/writing/QuantizationFundamentalsForMultiVectorRetrieval

Multi-vector search approaches are now critical for coding agents and multi-modal applications. MixedBread, Cursor, Parallel AI, and others have enabled coding agents to use this semantic search because it cuts token usage in half, allows agents to finish tasks in half the time, and yields better-quality outputs. I've validated the impact on my own commercial codebases and analysis.
Multi-vector search is more powerful because it uses more contextual data from the inputs. The architecture stores a separate embedding for each word in a document, rather than storing an entire document (or chunk) in a single embedding. This gives multi-vector approaches a more detailed understanding of the content, but it also means there's a lot more embeddings.

Quantization is what makes handling this extra information practical in many cases. By representing numbers with fewer bits (like rounding to fewer decimal places), quantization trades a small amount of precision for a large reduction in storage.
This post is a guide to understanding how quantization for multi-vector and ColBERT approaches work.

Related Posts on Multi-Vector Search

Modern Multi-Vector Code Search – Technical deep-dive on the multi-vector approach by mixedbread's founder
The 1/2 Token Codebase Search – Benefits and intuition for using multi-vector search with agents to improve speed, quality, and reduce token usage.

Intro to Quantization
Before diving into the advanced approach ColBERT uses (Product Quantization), let's understand the basic concept of quantization with a simpler approach.

We'll start with creating some dummy data to quantize.

We can look at the size of the data we are starting with. Our goal is to reduce the size of original_values without losing too much information. This is called Quantization.

Let's compress this data so we're only storing 8 bits per value. All data values are between the minimum and the maximum value. We want to represent each one of them using just 8 bits. We do this by dividing up the range into 2^8 = 256 equal intervals (called levels) and storing which level each value is in.

Let's save the minimum and maximum values that defines the range we need to divide up.

Now we can quantize the data to these levels by replacing the 64 bit data value with the 8 bit level it lies in. We'll use the astype function to convert the data to the new type. This is a simple form of quantization called uniform scalar quantization.

This is our quantized representation - just 8 bits per value instead of 64. Much smaller!

We can calculate how much space we saved by comparing the original size to the quantized size.

This is a compression ratio of 8x. We've gone from 64 bits per value to 8 bits per value. Not bad!
Now what's the catch? We've lost some information.
We've rounded the values to the nearest level. This means that some values are not exactly the same as the original values. Sometimes this is a big deal, but sometimes it's not.
We can measure how much error we introduced. We'll use mean absolute error, which is just the average difference between the original and reconstructed values. Quantifying information loss is an important concept to be aware of.
To calculate the error, we'll need to convert back to the original range. This is the inverse of the scaling we did earlier.

Because our sample data is so simple, we can see the error is very small. We'll plot the original values and the quantized values. You can see that while it's almost the same line, our reconstructed values are not exactly the same as the original values. That's called information loss. We reduced the size of our data from 64 bits per value to 8 bits per value, but we lost some information in the process.

This is the most basic form of quantization - uniform scalar quantization. We're simply:

Taking continuous values in a range
Mapping them to a smaller set of discrete levels (like 256 levels for 8-bit quantization)
Using these discrete levels to reconstruct approximations of the original values

The tradeoff is clear: we reduce storage space at the cost of some precision. With 8 bits, the error is usually very small for many applications.
Quantizing Whole Vectors
We've seen how to quantize scalar data. For ColBERT, we need to quantize embeddings (high-dimensional vectors).
We could apply scalar quantization to each number independently, but quantization errors add up across all dimensions. Finding quantization parameters that work well across the entire embedding space would be challenging.
In practice it often works better to quantize vectors as a whole. This is done using a clustering algorithm like KMeans to group similar vectors. The algorithm organizes the data so that vectors with high similarity end up in the same cluster. Each cluster is represented by a single point called a centroid. Instead of storing each vector's exact values, we store two things:

The cluster ID that each vector belongs to.

The centroid value for each cluster.

When we need to reconstruct a vector, we look up its cluster ID and use the corresponding centroid as its approximation. This reduces storage space while maintaining a reasonable approximation of the original data. The trade-off: more clusters yields better approximation but requires more storage for centroids and larger cluster IDs.

This approach, called Vector Quantization (VQ), is a solid foundation. However, achieving high precision would require a massive number of centroids, making it impractical for large-scale systems. This is where Product Quantization comes in.
Product Quantization builds on the clustering idea but achieves far better compression by splitting each vector into smaller pieces and clustering those pieces separately.

[Content continues with Simplified Version, Real Implementation, Extreme Quantization, and The Real ColBERT Approach sections — full text available by re-fetching the URL]

---

# RAG Systems Have a Context Problem

**URL:** https://isaacflath.com/writing/most-rag-systems-have-a-context-problem

Multi-Vector Retrieval Details with Mixedbread's Aamir Shakir
RAG systems have a context problem. I talked with Aamir Shakir, the founder of Mixedbread, for a deep dive into the research and engineering behind modern retrieval systems. I've been using Mixedbread's tools, like mgrep. They claim to cut tokens in half, speed up retrieval, and improve quality. After running my own experiments, I found they were right.
We went beyond hybrid search and re-rankers to the architectural shift of multi-vector retrieval. This post summarizes the theory, engineering challenges, and practical applications.

If you missed the first talk on using mgrep for agentic workflows, you can watch it here: mgrep with Founding Engineer Rui.

What is Mixedbread & Multi-Vector Search?
Mixedbread began as an applied research lab built on a simple hypothesis: AI will only be as useful as its context. Without context, an AI is like a new employee on day one. This "context problem" is a search and retrieval problem.
AI models have advanced fast, but retrieval tech still relies on concepts from 20 years ago. Mixedbread's goal is to modernize retrieval.
The core of their approach is multi-vector search.
Traditional retrieval-augmented generation (RAG) typically follows this path:

Take a document.
Split it into chunks.
Create one single vector embedding for each chunk.

This process compresses complex information into a single vector.
Multi-vector search, particularly models like ColBERT, changes this. Instead of one vector per chunk, it creates one vector per token.
For a sentence like "I love bread," a traditional model produces one vector. A multi-vector model produces three, preserving far more granular information.
Why Multi-Vector Outperforms Traditional RAG
The limitations of older methods highlight why a new approach is needed.

Keyword Search (BM25) anchors on exact keywords, making it robust for niche domains with specific terminology. It fails with semantics, synonyms, abbreviations (like "RAG" vs. "retrieval augmented generation"), and context ("Apple" the fruit vs. "Apple" the company).

Single-Vector Search: compresses paragraphs into a single point. It captures the topic but blurs nuance. If a paragraph covers politics, food, and sports, you may only retain the main topic and lose the details. It's also sensitive to "out-of-distribution" data. If the model hasn't seen a term or OCR errors introduce strange characters, it guesses where to place the vector, losing meaning.

Multi-vector search combines the best of both worlds.

Granularity: By representing every token, it captures the keyword-level precision of BM25, making it robust to out-of-distribution terms.

Semantics: Since each token's representation is a dense vector, it also captures the semantic meaning and context, like a traditional embedding.

This approach provides a powerful hybrid search "out of the box." Because it retains more information, it generalizes well to new domains, complex data, and long-context retrieval.
Aamir shared benchmarks where their ColBERT-style model (trained on 300-token docs) outperformed models designed for long-context retrieval on documents with tens of thousands of tokens.

Making Multi-Vector Practical with Quantization
If multi-vector is so powerful, why wasn't it the standard all along? The primary barriers were infrastructure and cost. Storing a vector for every token generates massive data, making it expensive and slow without the right engineering.
This is where quantization becomes critical. Quantization converts high-precision numbers (like 32-bit floats) into lower-precision formats to save storage and speed up computation.
Aamir explained two common techniques:

Int8 Quantization: Store 8-bit integers per dimension instead of 32-bit floats. Map values to 256 buckets based on min/max. This cuts storage by 4x and can speed computation by 8-10x with little loss in retrieval quality.

Binary (1-bit) Quantization: Store a 1 or 0 per dimension. This reduces storage by 32x. Instead of cosine similarity, you can use Hamming distance (XOR and popcount), which is extremely fast. This can lead to performance loss if the model isn't optimized for it.

Mixedbread found a trick to mitigate binary loss: keep document vectors binary, but keep the query vector higher precision (float32 or int8). That drops performance loss from ~40% to ~5%. Query precision matters more than storing both at low precision.

Mixedbread and Hugging Face co-authored a post on this topic, showing how to achieve a 40x speedup and 62x cost reduction.

Mixedbread's Architecture & Semantic Chunking
With these techniques, Mixedbread built an end-to-end system for speed and scale. Indexing the entire React codebase (60 million tokens) takes a couple of minutes.
Here's an overview of their architecture:

Ingestion & Chunking: When a file is uploaded, it's chunked based on semantics (more on this later)

Inference: Chunks are sent to GPUs running a custom inference engine with CUDA kernels, enabling massive parallelization and low latency embedding generation.

Storage & Caching: Embeddings are quantized and stored. The system uses a two-step retrieval process (fast, lossy first pass; full precision second pass) and multi-tier caching from S3 to hard drives, NVMe SSDs, and in-memory for hot data.

A query typically takes around 60 milliseconds end-to-end (P95).
Smart Chunking for Any Data Type
A key part of Mixedbread's system is its approach to parsing and chunking different file types.

Code: They parse the Abstract Syntax Tree (AST) to create semantically meaningful chunks, grouping related functions or classes together.

PDFs: PDFs are hard to parse due to tables, columns, and charts. Mixedbread takes a screenshot of each page and embeds the image, preserving layout and content. They also use LLMs to create contextual summaries to link pages together.

Video: A transformer-based shot detection model analyzes frames to identify scene changes, creating logical chunks based on the visual narrative.

Text/Markdown: They use contextualization methods to ensure each chunk contains relevant surrounding information, a technique inspired by research from Anthropic.

This idea of processing entire documents and then chunking at the embedding level is sometimes called "late chunking."

The Role of Re-rankers & Cross-Encoders
Even with a strong retriever like ColBERT, re-ranking can boost quality. Aamir confirmed they use cross-encoders internally.
A cross-encoder looks at the query and a candidate document together, making a more accurate relevance judgment than a retriever that embeds the document in isolation.
The next frontier is list-wise re-ranking, where the model sees the query and the entire list of candidates at once. It can answer questions like "which is the fastest?" by comparing all options, but it's currently too slow and expensive for most production systems.
Aamir is also excited about learnable scoring functions. Instead of burning GPUs to create complex embeddings only to compare them with cosine similarity, the scoring function itself could be learned, improving relevance.
How to Get Started in Retrieval Research
Retrieval is more accessible than training foundational LLMs. You can start with a MacBook. Aamir's advice:

Read the Fundamentals: Start with the original Sbert (Sentence-BERT) paper to understand the basics of modern embedding models.

Learn by Doing: Use libraries like sentence-transformers to train your own models. The documentation is excellent.

Read In-Depth Guides: The Mixedbread blog offers deep dives into their training techniques.

Stay Updated: Follow resources like the Information Retrieval Substack to keep up with the latest research.

Embrace the Struggle: Build things yourself. Don't rely on AI to write all the code. The learning happens when you debug PyTorch and CUDA errors.

Conclusion
Multi-vector search is heavier and harder to engineer than standard RAG. With quantization making it affordable, the quality gains are now accessible. If you're hitting a ceiling with semantic search, this is the architecture to investigate next. Mixedbread offers an API that does it for you.
My conversation with Aamir reinforced that AI quality is tied to context quality. As models get smarter, the tools we use to feed them information must get smarter too.
If you're working on complex retrieval problems, the techniques discussed here are the new baseline. If you're an engineer passionate about building high-performance, distributed systems, Mixedbread is hiring.

Explore their work and open positions at mixedbread.com.
