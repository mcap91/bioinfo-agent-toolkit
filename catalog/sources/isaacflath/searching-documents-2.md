# Searching Documents (Part 2) — Isaac Flath

Indexing, chunking, retrieval, filtering, and ranking (continued).

---

# mgrep with Founding Engineer Rui Huang

**URL:** https://isaacflath.com/writing/mgrep-with-founding-engineer-rui-huang

The Problem with grep for AI Agents
I hosted a talk with Rui Huang, a founding engineer at Mixedbread, about mgrep, a tool now essential to my workflow.
I sync every repo locally, automatically, all the time. I've seen companies replace production semantic search with Mixedbread's cloud service because it finds more relevant results and ranks them well.
Rui's talk focused on using their semantic search technology to build more effective coding agents.

This post covers key points from our conversation: the limits of tools
like grep, how mgrep provides a semantic alternative, and the
multi-vector and multimodal technology that powers it.

For an even deeper dive on what makes mgrep work and the research that
went into it, see Most RAG Systems Have a Context Problem

The Problem with grep for AI Agents
The "RAG is dead" headlines are bombastic but common. The argument: modern AI agents are so powerful they don't need semantic search. They can use basic tools like grep to find context with better results.
This argument targets older semantic search methods.

Agentic search using grep is powerful but has significant drawbacks.
Rui explained issues his team observed in long-running tasks.
1. It's Slow and Expensive.
grep is a pattern-matching tool. For a high-level task like "refactor
the authentication flow," an agent must guess keywords
(authentication, middleware, credentials) and run multiple tool
calls. That increases latency and token consumption, stuffing
the context window with noise.
2. It Degrades Quality.
More tool calls fill the context window with partial information.
The original intent gets diluted. Rui pointed out this is when you
see agents hallucinate or get stuck, responding with phrases like
"You're absolutely right" without making progress.
Faster feedback loops matter. When an agent uses fewer tokens and gets to the point faster, I can iterate and stay focused.
Introducing mgrep: Semantic Search for Code
Mixedbread's solution is mgrep, a command-line tool designed to be a
semantic version of grep. Instead of matching patterns, it understands
the intent behind a natural language query.
The Semantic Query
mgrep "how streaming is implemented"
The tool returns a list of relevant files with specific line numbers and
a similarity score, which helps the agent gauge the confidence of each
result.

This approach lets the agent progressively discover context instead of
stuffing multiple files into its prompt.
In Mixedbread's internal tests with Claude on complex coding tasks, mgrep delivered a large performance advantage:

53% fewer tokens used

48% faster response times

3.2x better quality responses

Note: I've seen similar gains in my own
experiments,
which is what inspired me to host this talk.

Live Demo: mgrep vs. grep
Rui demoed a playground that runs Claude side-by-side: standard grep
vs. mgrep. The task was to query the React codebase (over 6 million
tokens) with the question: "Explain how the useEffect hook works in
common patterns."

mgrep is complementary to grep, not a replacement. Agents get both
tools and can choose the right one: mgrep for semantic exploration and
grep for exact-match symbol searching.
Try the playground yourself to see
the difference without any setup.
Getting Started: Setup & Terminal Demo
mgrep syncs a local directory to a cloud-backed search index. Rui
walked through the setup.
First, install the tool via npm:
npm install -g @mixedbread/mgrep # or pnpm / bun
Then, log in to connect to your Mixedbread account:
mgrep login
Once set up, you can sync any directory. Rui used Andrej Karpathy's
nanogpt repository as an example. The watch command indexes the current
folder, respects .gitignore, and syncs to a remote Mixedbread store.
mgrep watch

Ingestion is fast and cheap: the 60-million-token React codebase takes
about five minutes and costs $20 to index.
Once synced, you can query your code with natural language. mgrep also
includes a -a (--answer) flag that uses an LLM to return a direct
answer with citations.

This gives the agent a concise summary, reducing the need to process
large file snippets.
Integrating mgrep with Coding Agents
While you can use mgrep manually, its core usage is in agent
integration. Mixedbread provides plugins for popular coding agents like
Claude Code.
A simple install command configures the agent to be aware of mgrep and
how to use it.
mgrep install-claude-code
This command sets up the necessary skills and prompts. The mgrep watch
process runs in the background during an agent session, keeping the
index up to date.
These plugins are wrappers around the mgrep CLI with a pre-written prompt. You can customize behavior by creating your own prompts in your agent's configuration files.
Under the Hood: Multi-Vector & Multimodal Search
mgrep is powered by the Mixedbread Search API. When you sync files,
they're sent to a Mixedbread store where the pipeline takes over.

The service analyzes file types, applies chunking strategies (e.g., different logic for Markdown vs. code), and generates embeddings using state-of-the-art models.
The key innovation is multi-vector search. Traditional semantic
search creates one vector per chunk. Mixedbread represents every word
as its own vector, creating a richer, more granular representation.
Advanced
quantization
techniques make this approach scalable and affordable.
This system is also multimodal. It can natively index and search
images, videos, audio, and PDFs without transcribing them to text. Rui
demoed searches like "sad cat" and "angry cat."

This helps codebases with diagrams, visual assets, or complex PDFs. Agents can find visual information that text-only tools like grep miss.
In legal domains, PDFs are often the source of truth for contracts. In e-commerce, product images are often the source of truth.
Conclusion: Give AI the Best Tools
Capable agents don't mean semantic search is dead. Agents need better search tools. Combining mgrep with grep gives agents a more powerful, efficient way to understand a codebase.

The key takeaways are:

Agentic search needs semantic search. Relying on grep alone is
slow, expensive, and leads to lower-quality results for complex tasks.

Better tools lead to better agents. mgrep improves agent
performance by reducing token usage, increasing speed, and providing
more relevant context.

The future is multimodal. As agents handle more data types, their
tools must keep up. Native search across code, PDFs, and images is a
significant advantage.

No matter how advanced agents become, their performance is constrained by tool quality. Search shouldn't be the bottleneck.
Q&A Highlights
We ended with audience questions:

Multilingual Support: Mixedbread's models are multilingual by
default, supporting languages like Arabic, Chinese, and Korean. Try
the search demo in different
languages.

Cost: Indexing is priced per token. The full React codebase (6M+
tokens) costs roughly $20. The team is open to discounts at scale.

Engineering Optimizations: Low latency comes from quantization
research and an optimized end-to-end pipeline. The team plans more
blog posts detailing the work.

---

# Understanding Keyword Search

**URL:** https://isaacflath.com/writing/keyword-search-fundamentals

Search isn't magic, it's engineering. Understanding how it works will change how you build your search system.
In this article we'll build a simple keyword search implementation from scratch. You'll learn:

What keyword search is
How raw text becomes searchable data
Why indexing is the secret to fast retrieval
How BM25 ranking puts the most relevant results first (and why it beats simple word matching)

📝 This is a brief overview of several chapters in my RAG course for backend developers on boot.dev. In that course, I teach keyword search, hybrid search, re-ranking, agentic search, and more. If that sounds interesting, check out the course landing page: Learn Retrieval-Augmented Generation.

What is Keyword Search?
Keyword search finds documents by matching the exact words a user types. When you search for "machine learning," it looks for documents containing those terms.

💡 When we say "exact match," we mean "exact match of a cleaned-up version of the word." "Run", "run", "ran", "runs" all match as "run". We'll get into those details later.

Unlike semantic search, keyword search focuses on literal text matching. It's precise for exact terminology but less flexible for synonyms or conceptual queries.
For example, searching for "car" won't automatically return documents about "automobile" or "vehicle" unless those exact words appear in the text.
Why Keyword Search Matters
Why does keyword search matter in the age of large language models, vector databases, and semantic search?
Consider these scenarios:

Medical Search: A doctor searches for "COVID-19" and needs specific information about that exact condition, not a general collection of content about respiratory viruses or pandemic diseases.
Financial Services: A compliance officer searches for "KYC requirements" (Know Your Customer) and needs regulatory documentation with this exact acronym, not general customer verification content.
Legal Research: A lawyer searches for "habeas corpus" and needs cases specifically invoking this writ, not general discussions about detention or constitutional rights.

In each case, exact keyword matching matters. The more technical the terminology, the more powerful keyword search becomes.

💡 In practice, search systems perform best with both keyword and semantic search components.

Implementing Keyword Search
Let's dive in. Implementing keyword search covers five topics:

Text Pre-Processing: Run, run, ran, runs all turn into run for keyword matching
Tokenization: Break text into individual words or terms
Indexing: For each word create a list of the documents that contain it
Matching: Find documents that contain the search terms
Ranking: Score and order results by relevance (typically using algorithms like BM25)

Text Processing
We need to clean text so matching works reliably. Raw text doesn't.
Cleaning Text
Loading...
A search for "kubernetes" in the example text should match Kubernetes (capitalized), kubernetes (lowercase), and kubernetes.(punctuated).
Let's make that happen by making everything lowercase and removing punctuation.
Loading...
Loading...
Now Kubernetes, kubernetes, and kubernetes. all become kubernetes.
Stemming and Lemmatization
Stemming reduces words to their root form. This helps "running", "runs", and "ran" match "run".
Here's a simple stemmer:
Loading...
Loading...
Now implemented and implementing both become implement.

💡 Stemming vs Lemmatization: Stemming is fast but aggressive. It can destroy words or create non-words. Lemmatization is more sophisticated, using linguistic analysis to map words to their base forms (lemmas). For example, "better" → "good" or "running" → "run." Stemming is fast; lemmatization is more accurate but slower. For production, you'd typically use libraries like nltk instead of rolling your own.

Loading...
N-grams
So far we've treated each word as a token ("unigram"). But sometimes the most important information comes from phrases, not individual words.

⚠️ N-grams are not used on stemmed words. You wouldn't want "running shoes" to turn into "run shoe". Stemming is for individual words; n-grams are for phrases.

Consider searching for "COVID 19." As separate words, "COVID" and "19" don't carry the same meaning as the phrase "COVID 19" together.
N-grams solve this by creating tokens from sequences of consecutive words:

Unigrams: Individual words
Bigrams: Two-word phrases
Trigrams: Three-word phrases

Let's see this in action:
Loading...
Loading...
Loading...
This shows how n-grams capture phrases like "stock exchange" and "trading suspended" that unigrams would miss.
When to Use N-grams
Use higher-order n-grams when:

Your domain has important multi-word terms ("machine learning", "New York", "COVID 19")
You need precise phrase matching
Users search with specific terminology

Stick with unigrams when:

You have rare, specialized terms that rarely appear in phrases
You want maximum recall (finding all relevant documents)
Your documents are short

💡 Most systems combine unigram and bigram search to balance phrase precision with word recall.

⚠️ There's also something called trigram search for substring matching (finding "tion" in "information"), but that's completely different from the n-gram tokenization we're discussing here. We'll cover trigram search in a future post.

Let's update our preprocessing to include n-grams:
Loading...
Loading...
Loading...
Tokenization
Next, we split text into individual words (tokens) and remove common words that don't help with search.
Stop words like "the", "and", "in" appear everywhere but carry little meaning. Removing them improves search quality.
Loading...
Loading...
Loading...
This gives us clean, meaningful tokens ready for indexing and search.

💡 Usually you don't need your own list of stop words. Libraries like nltk and others have their own comprehensive lists you can use.

Lets make a function that pre processes the text and tokenizes it.
Loading...
The Inverted Index: Making Search Fast
Raw search is slow. To find the word "data" in 10,000 documents, you'd read every single one. That's too slow for real apps.
Without an inverted index our production system would search in this way every time a user included kubernetes in their query:

"Is data in document 1?"
"Is data in document 2?"
"Is data in document 3?"
"Is data in document 4?"

This is a lot of work and not necessary because we know the documents to search against ahead of time. We can do that work once and store it in an inverted index.
The index maps each word to a list of the documents containing it:
In an inverted index data would be associated with a list of the documents that contain the word data. It looks like this:
'data' : {1, 3} -> the word data is in documents 1 and 3.
Loading...
Loading...
Loading...
Loading...
No more scanning documents. Search becomes a simple lookup.
Boolean Search: Combining Terms
Single words are limiting. Users want to combine terms: "python AND machine learning" or "apple NOT fruit".
Boolean operators let us combine word searches to give users precise control.
Lets create a dataset and see some of these operations in action.
AND: Documents must contain all terms
Loading...
{4}
OR: Documents can contain any term
Loading...
{1, 3}
NOT: Exclude documents with certain terms
Loading...
{3}
Boolean search is powerful, but it treats all matches equally. A document with 10 mentions of "kubernetes" ranks the same as one with 1 mention. That's where ranking comes in.
TF-IDF: When Frequency Meets Rarity
Boolean search tells us which documents match, but not which ones matter most. A document mentioning "kubernetes" once ranks the same as one mentioning it 20 times. That's not helpful.
TF-IDF (Term Frequency-Inverse Document Frequency) fixes this by scoring documents based on relevance. It combines two simple ideas:

Term Frequency (TF): More mentions = more relevant
Inverse Document Frequency (IDF): Rare words = more valuable

Term Frequency: Counting Mentions
If one document mentions "kubernetes" 10 times and another mentions it once, the first is probably more about kubernetes:
Loading...
Loading...
Loading...
Inverse Document Frequency: Valuing Rare Words
But frequency alone misleads. In a tech blog, "programming" might appear everywhere, making it useless for ranking. Meanwhile, "kubernetes" might appear in only 10% of posts, making it highly valuable. We need words that tell us something about our document that is unique to it, or that make it more or less relevant when compared to a different document.
IDF is a score captures this. Rare terms get higher scores.
Loading...
Process all our documents
Loading...
Loading...
Common words get low IDF scores. Rare words get high scores.
The Magic: TF × IDF
Now we multiply them. High frequency and high rarity indicates high relevance.
Loading...
Now we can score a document based on a keyword.
Loading...
Loading...
Loading...
Loading...
Loading...
Loading...
This document is more relevant to the term data than it is to the term model based on this TF-IDF score.
Let's see this in action. Imagine searching for "machine learning" in our documents.
We need a single score for each document so we can pick the document with the largest score. To do this, we calculate the score for each query term and then add them up to get the document score.
For our query of machine learning we add the scores for machine and learning.
Loading...
Loading...
Loading...
Loading...
Loading...
Documents with both terms score higher than those with one. Documents mentioning terms more often score higher than those mentioning them less. And rare, specific terms boost scores more than common words.
Document 4 is completely irrelevant and it has a score of 0. Document 1 is the most relevant because it has the highest score. Documents 2 and 3 also rank well.
This is the foundation of relevance ranking, but we can do even better.
BM25: The Algorithm That Powers Modern Search
While TF-IDF works well, it has some limitations that become apparent in real-world use. BM25 (Best Matching 25) addresses these issues and is the algorithm that powers most modern search engines.
BM25 improves on TF-IDF in three key ways.
1. Better IDF Calculation
Basic TF-IDF can be unstable with rare or common terms. BM25 uses a more robust formula:
Loading...
The + 0.5 terms prevent division by zero and provide smoothing, while the final + 1 ensures the score is always positive.
2. Term Frequency Saturation
In basic TF-IDF, a document with 100 mentions of a term gets 10x the score of one with 10 mentions. This can lead to keyword stuffing and poor results. BM25 uses diminishing returns: additional occurrences matter less and less.
Loading...
With k1=1.5, the progression looks like:

1 occurrence → score of 1.0
2 occurrences → score of 1.4 (not 2.0)
10 occurrences → score of 2.2 (not 10.0)

This prevents any single term from dominating the results. We can visualize this diminishing return by plotting the term frequency with saturation at different frequencies.

3. Document Length Normalization
Long documents mention more words, boosting their scores unfairly. A 1000-word article about "kubernetes" will naturally contain more search terms than a focused 100-word guide, but that doesn't make it more relevant.
BM25 fixes this with length normalization. Documents longer than average get penalized. Shorter ones get boosted:
Loading...
Document lengths: [13, 8, 9, 9]
Mean document length: 9.8 tokens
Loading...
Loading...
Loading...
Loading...
Loading...
The plot shows this in action. At average length, there's no penalty. Longer documents get increasingly penalized, while shorter ones get boosted.

At 0 tokens: 0.250
At avg length (9.8): 1.000
At 20 tokens: 1.788
Full BM25
Now we can put it all together
Loading...
To score a document, we calculate the bm25_score for every term in the user query and sum them up
Loading...
Loading...
Loading...
This gives us the complete BM25 algorithm: term frequency with saturation, stable IDF calculation, and length normalization all working together to produce relevance scores that match human intuition about what makes a good search result.
Putting It All Together
We've built a complete keyword search system from the ground up, progressing from basic text processing to sophisticated ranking algorithms. Here's how all the pieces fit together:

Text Processing: Clean and normalize text for consistent matching
Tokenization: Break text into searchable terms while removing noise
Inverted Index: Enable fast lookups instead of slow document scans
Boolean Operations: Give users precise control over term combinations
TF-IDF Scoring: Rank results by relevance using frequency and rarity
BM25 Improvements: Provide more robust scoring when dealing with real-world problems

The result is a search system that's both fast and intelligent, capable of finding relevant results in milliseconds.
Learning More

📝 I've been working with the team at Boot.dev on a comprehensive RAG for backend developers course. This blog post skims information from the first 3 chapters of the course. This course will cover keyword search, semantic search, hybrid search, agentic search, and more. Sign up at the link for a discount to get started on the backend developer learning path to learn all the pre-requisite information now!

---

# Late Chunking: The Better Way to Embed Document Chunks

**URL:** https://isaacflath.com/writing/LateChunking

The Lost Context ProblemA user asks "What was Berlin's population in 2023?" and your system has a chunk containing "The city had 3.85 million inhabitants" — but with no mention of Berlin. The system fails because it doesn't know "the city" refers to Berlin, which was mentioned in a previous chunk.
This is the lost context problem, and it's a fundamental flaw in how most retrieval systems handle documents. The standard approach involves:

Break documents into smaller chunks
Turn each chunk into numbers that represents the meaning using a pre-trained embedding model
Store these embeddings
Retrieve chunks based on similarity to the query embedding

The problem? When we chunk first and embed later, we destroy contextual connections between chunks. Pronouns lose their referents, terminology becomes ambiguous, and discussions that span multiple chunks become fragmented and less retrievable.
Consider this excerpt:
Loading...
When chunked by sentence, the "Berlin" is separated from details about its population and status. A query about "Berlin's population" would be difficult.  "Berlin" would match to the first sentence, where "population" would match to the second sentence.  If the model knew that "Its" from chunk 2 represented "Berlin" from chunk 1, the query would match to the second sentence correctly.  However, we created the embeddings independently breaking this context link.
This tutorial will introduce you to late chunking to address this issue by changing the traditional "chunk-then-embed" strategy to an "embed-then-chunk" approach to keep the full document context in each chunk embedding.
By the end of this post, you'll:

Understand how late chunking works and why it outperforms traditional approaches
Implement a complete late chunking system using Python and popular embedding models
See quantitative improvements in retrieval quality
Learn how to integrate late chunking with your existing vector database

📚 If you have not implemented a retrieval system before your best bet is to start with a full, but simple retrieval implementation first.  Check out this post to get started on that!

🙏 I used a lot of great resources to put this blog post together and it is so amazing these were all available!  Please check them out!

Jina AI's Late Chunking in Long Context Embedding Models blog post
Jina AI's What Late Chunking Really Is and What it's Not Part II blog post
Jina AI's Late Chunking Github Repo with their implementation
Jina AI's Late Chunking: Contextual Chunk Embeddings Using Long-Context Embedding Models paper: Günther, M., Mohr, I., Williams, D. J., Wang, B., & Xiao, H. (2024)

Traditional ChunkingLet's start with a baseline chunking approach.  This will serve as pre-requisite knowledge but also give us a baseline to compare to to see what kinds of queries late chunking improves in practice.The standard workflow used in most retrieval and RAG applications today is:

Split a document into chunks
Embed each chunk independently
Store these embeddings for retrieval

We will start with a simple implementation using the Sentence Transformers library:We will need an example text to work with.  It is critical that you always have examples to look at constantly as you are working on this stuff.  The most common mistake I see, from early exploration and prototyping all the way to production commercial deployments, is not looking at data enough.First, let's do a simple chunking approach.  In this example, we will do a word based chunking but with an overlap to account for some conextual information.

Chunk 1:
Berlin is the capital and largest city of Germany. The city has a rich history dating back centuries. It was founded in the 13th century and has been a significant cultural and political center throughout European history. The metropolis experienced dramatic changes during the 20th century, including two world wars

Chunk 2:
dramatic changes during the 20th century, including two world wars and a period of division. After reunification, it underwent extensive reconstruction and modernization efforts. Its population reached 3.85 million inhabitants in 2023, making it the most populous urban area in the country. This represents a significant increase from previous decades,

Chunk 3:
the country. This represents a significant increase from previous decades, driven largely by immigration and economic opportunities. The city is known for its vibrant cultural scene and historical significance. Many tourists visit its famous landmarks each year, contributing significantly to the local economy. The Brandenburg Gate stands as its most

Chunk 4:
the local economy. The Brandenburg Gate stands as its most iconic symbol.
With the traditional approach we would then embed each of those chunks separately
💡 Other Common Chunking Patterns
While our example uses simple word-based chunking with overlap, several other chunking strategies are popular in practice:

Sentence-based chunking: Split at sentence boundaries to preserve complete thoughts
Paragraph-based chunking: Use natural document structure for more coherent chunks
Fixed token chunking: Count tokens instead of words for more consistent embedding sizes
Semantic chunking: Group semantically related content using embeddings or topic modeling
Recursive chunking: Apply hierarchical chunking strategies for nested document structures
Sliding windows: Create overlapping chunks with a fixed window size and stride

Each approach has trade-offs between implementation complexity, semantic coherence, and retrieval effectiveness. Regardless of the chunking strategy, traditional approaches all share the same fundamental limitation: each chunk is embedded independently without access to the full document context.
We can then do retrieval with those chunks and embeddings.Let's look at an example query

Query: What is Berlin's population?
Best matching chunk (similarity: 0.6540):
Berlin is the capital and largest city of Germany. The city has a rich history dating back centuries. It was founded in the 13th century and has been a significant cultural and political center throughout European history. The metropolis experienced dramatic changes during the 20th century, including two world wars
In this example, the approach failed to find the chunk that contains the answer to the query.Where Traditional Chunking Falls ShortThe example failed because there is information in 2 chunks that must be put together to answer the question.  The search prioritized matching on "Berlin" instead of matching on "population".  What we want is a system that is smart enough to understand that the population information from chunk 2 is about Berlin.
This traditional chunking process treats each chunk as an independent document, which means:

References to entities mentioned in other chunks become ambiguous
Contextual information spanning chunk boundaries gets lost
The embedding model has no way to resolve these references

Let's look more closely at this problematic behavior.The Reference Resolution ProblemTo demonstrate this problem more clearly, let's run a few more queries against our chunked document:

Query: What happened before reunification?
Best matching chunk (similarity: 0.3369):
dramatic changes during the 20th century, including two world wars and a period of division. After reunification, it underwent extensive reconstruction and modernization efforts. Its population reached 3.85 million inhabitants in 2023, making it the most populous urban area in the country. This represents a significant increase from previous decades,

Query: What is Berlin's population?
Best matching chunk (similarity: 0.6540):
Berlin is the capital and largest city of Germany. The city has a rich history dating back centuries. It was founded in the 13th century and has been a significant cultural and political center throughout European history. The metropolis experienced dramatic changes during the 20th century, including two world wars

Query: When did Berlin reach 3.85 million people?
Best matching chunk (similarity: 0.5929):
Berlin is the capital and largest city of Germany. The city has a rich history dating back centuries. It was founded in the 13th century and has been a significant cultural and political center throughout European history. The metropolis experienced dramatic changes during the 20th century, including two world wars

Query: What famous landmark is in Berlin?
Best matching chunk (similarity: 0.6784):
Berlin is the capital and largest city of Germany. The city has a rich history dating back centuries. It was founded in the 13th century and has been a significant cultural and political center throughout European history. The metropolis experienced dramatic changes during the 20th century, including two world wars

Query: How many people live in the German capital?
Best matching chunk (similarity: 0.5487):
Berlin is the capital and largest city of Germany. The city has a rich history dating back centuries. It was founded in the 13th century and has been a significant cultural and political center throughout European history. The metropolis experienced dramatic changes during the 20th century, including two world wars
Notice how the system struggles with queries that require connecting information across chunks. For example, when asking about Berlin's population, the system might return a chunk that mentions Berlin but not its population, or vice versa.
This happens because each chunk is embedded in isolation. When chunk 2 mentions "Its population reached 3.85 million inhabitants," the embedding model has no way to know that "Its" refers to Berlin, which was mentioned in chunk 1.Visualizing the Lost ContextWe can visualize this lost context by examining how references get disconnected across chunk boundaries:Chunk 1Berlin is the capital and largest city of Germany. The city has a rich history dating back centuries. It was founded in the 13th century and has been a significant cultural and political center throughout European history. The metropolis experienced dramatic changes during the 20th century, including two world warsChunk 2dramatic changes during the 20th century, including two world wars and a period of division. After reunification, it underwent extensive reconstruction and modernization efforts. Its population reached 3.85 million inhabitants in 2023, making it the most populous urban area in the country. This represents a significant increase from previous decades,Chunk 3the country. This represents a significant increase from previous decades, driven largely by immigration and economic opportunities. The city is known for its vibrant cultural scene and historical significance. Many tourists visit its famous landmarks each year, contributing significantly to the local economy. The Brandenburg Gate stands as its mostChunk 4the local economy. The Brandenburg Gate stands as its most iconic symbol.EvaluatingLet's make a tiny eval dataset so we can score this method (and later we will add late chunking) against queries that have all the necessary information within a single chunk as well as queries where the necessary information is spread across multiple chunks.We can create a small function that lets us evaluate against the dataset.  We already retrieved chunks so we can re-use that and see if the answer is in the chunk it returned.We can print and take a look at the accuracy.Accuracy for queries with answers in a single chunk: 1.00
Accuracy for queries with answers spanning chunks: 0.00
We've got a problem!  0% accuracy on our queries with answers spanning chunks!  Let's explore what the problem is and what to do about it.Why Overlapping Chunks Isn't EnoughA common approach to mitigate this problem is to use overlapping chunks, which we've already incorporated in our example. While overlap helps, it has significant limitations:

Limited context window: Overlap only helps with nearby context, not long-range references
Redundant storage: Overlapping chunks increase storage requirements and indexing time
Inconsistent embeddings: The same content appears in different contexts in different chunks
Arbitrary boundaries: There's no guarantee that semantic units won't still be split
While increasing overlap helps, it doesn't solve the fundamental problem: each chunk is still embedded independently without access to the full document context.
These limitations highlight why we need a better approach to chunking and embedding documents for retrieval. The ideal solution would:

Preserve contextual information across chunk boundaries
Maintain references to entities mentioned earlier in the document
Create embeddings that reflect the document's global context
Still allow for retrieving specific, focused chunks rather than entire documents

This is exactly what late chunking provides. In the next section, we'll explore how late chunking solves these problems by reversing the traditional workflow.Late ChunkingLate chunking flips the traditional approach on its head. Instead of chunking first and then embedding each chunk independently, late chunking follows this workflow:

Embed the entire document at the token level using a long-context embedding model
Apply chunking boundaries to these token-level embeddings
Create chunk embeddings by pooling the appropriate token embeddings for each chunk

This seemingly simple change makes a big difference in retrieval quality because each chunk's embedding now contains information from the entire document.Let's implement late chunking to see it in actionChunkingTo do chunking we need out a model and tokenizer.  We will use Jina AI's which is specifically designed for late chunking.TokenizationTokenize our document to convert the document into numeric valuesTo work in the token space we need the ids and the offsets to map back to the original text.  Let's look at how that works in a dummy example before we start working on actually chunking.tensor(4068)Token 1 (the second token) is 4068.  This is a value we can use to look up an embedding.  4068 represents some text in our original document.  Token offsets gives us the mapping to look up what it is representing in the original documenttensor([1, 7])Our token 4068 has a token offset[1,7].  We now have enough information to answer "What does 4068 mean in English?".  Let's look it up in our original English document.'Berlin'Perfect, token 4068 represents Berlin.  We know this because document[1:7] ([1:7] is the token offsets) returns the text Berlin.We can go from word to token ID using the model's tokenizer, which stores a mapping that was learned when the model was trained.4068Now that we understand how to work with token offsets to connect tokens in Jina AI's model to words in our English document.EmbedGreat!  Now we need to tokenize the entire document so we can pass that to a model.torch.Size([1, 152])We can see that after passing the entire document to the tokenizer, we get back an array with 152 tokens in it.Now that it's in numeric form, we can pass all the token to the model to get the embeddings for each token.torch.Size([1, 152, 768])As we can see, each of the 152 tokens has an embedding with 768 numbers in it.
Each of these represents a word's meaning in the context of this document, not just an isolated meaning of the word itself.  That's the genius of this model.Then ChunkTo chunk by sentences we can use period as the seperator.  We can use what we learned about the token id and offset to chunk in that token space.1012We can use that followed by a space to get start and stop of a chunk.  Let's do this, and store both the start and stop indexes in both english and token spaces.Let's print a few chunks to see that we've got them both for human readable and model readable formatsChunk 0:
  Character span (0:51): Berlin is the capital and largest city of Germany.
  Token span (0:11): tensor([ 101, 4068, 2003, 1996, 3007, 1998, 2922, 2103, 1997, 2762, 1012])

Chunk 1:
  Character span (52:102): The city has a rich history dating back centuries.
  Token span (11:21): tensor([1996, 2103, 2038, 1037, 4138, 2381, 5306, 2067, 4693, 1012])

Chunk 2:
  Character span (103:223): It was founded in the 13th century and has been a significant cultural and political center throughout European history.
  Token span (21:41): tensor([2009, 2001, 2631, 1999, 1996, 6122, 2301, 1998, 2038, 2042, 1037, 3278,
        3451, 1998, 2576, 2415, 2802, 2647, 2381, 1012])

All that's left it to use our chunks in token space to chunk the token embeddings.torch.Size([11, 768])Now PoolThere are 11 tokens each with an embedding of length 768 in this chunk.  But we need a single embedding for this chunk.  To do that we use mean pooling (just average them).torch.Size([768])
💡 You may notice that it's not late chunking OR chunk overlap.  While we aren't doing overlap with late chunking, you certainly can try.  Go ahead and experiment with all the traditional chunking performance tricks with late chunking approaches as well.

Do that in a loop to get embedding for each chunk in the document.10Perfect!  Now we have our document chunked with an embedding for each chunk.  This is late chunking, so let's put all of this in a function so we can do some evaluation and see what kind of impact it made.['Berlin is the capital and largest city of Germany.',
 'The city has a rich history dating back centuries.',
 'It was founded in the 13th century and has been a significant cultural and political center throughout European history.',
 'The metropolis experienced dramatic changes during the 20th century, including two world wars and a period of division.',
 'After reunification, it underwent extensive reconstruction and modernization efforts.',
 'Its population reached 3.85 million inhabitants in 2023, making it the most populous urban area in the country.',
 'This represents a significant increase from previous decades, driven largely by immigration and economic opportunities.',
 'The city is known for its vibrant cultural scene and historical significance.',
 'Many tourists visit its famous landmarks each year, contributing significantly to the local economy.',
 'The Brandenburg Gate stands as its most iconic symbol.']Evaluations!We can re-use what we did earlier along with the sample queries we were looking at to run an evaluation.
Remember this eval is to illustrate the kinds of questions late chunking can help solve.  A lot more work needs to go into evaluating 2 different approaches like this, so read the paper and blog posts by Jina AI if you are interested in that.  For this post, it is purely illustrative to build intuition over the kinds of queries late chunking can help with.
So let's get started.  Let's refresh our memory on the document we are querying.

Berlin is the capital and largest city of Germany. The city has a rich history dating back centuries. It was founded in the 13th century and has been a significant cultural and political center throughout European history. 

The metropolis experienced dramatic changes during the 20th century, including two world wars and a period of division. After reunification, it underwent extensive reconstruction and modernization efforts. 

Its population reached 3.85 million inhabitants in 2023, making it the most populous urban area in the country. This represents a significant increase from previous decades, driven largely by immigration and economic opportunities. 

The city is known for its vibrant cultural scene and historical significance. Many tourists visit its famous landmarks each year, contributing significantly to the local economy. The Brandenburg Gate stands as its most iconic symbol. 

For convenience let's concatenate the single chunk queries (everything needed to answer the query is contained in 1 chunk) and cross chunk queries (everything needed to answer the query is spread aross more than 1 chunk)([("What is Berlin's population?", '3.85 million inhabitants'),
  ('How many people live in the German capital?', '3.85 million inhabitants'),
  ('What famous landmark is in Berlin?', 'Brandenburg Gate'),
  ('What is the city known for?', 'vibrant cultural scene'),
  ('When was it founded?', '13th century')],
 [('When was Berlin founded?', '13th century'),
  ('What happened to Berlin during the 20th century?', 'two world wars'),
  ("What's the most iconic symbol", 'Brandenburg Gate'),
  ('What happened in the 20th century?', 'two world wars')])We can re-use the all the stuff we covered earlier in the blog post to check if the answer to the question is in the chunk that is returnedLet's do the same for the late chunking approach so we can compare the two.Let's put both these evaluations into a single dataframe so we can compare and see if our late chunking did better at the cross chunk queries.

  
    
      
      query
      answer
      traditional_correct
      late_chunking_correct
      query_type
    
  
  
    
      0
      What is Berlin's population?
      3.85 million inhabitants
      False
      True
      cross_chunk
    
    
      1
      How many people live in the German capital?
      3.85 million inhabitants
      False
      True
      cross_chunk
    
    
      2
      What famous landmark is in Berlin?
      Brandenburg Gate
      False
      False
      cross_chunk
    
    
      3
      What is the city known for?
      vibrant cultural scene
      False
      True
      cross_chunk
    
    
      4
      When was it founded?
      13th century
      False
      True
      cross_chunk
    
    
      5
      When was Berlin founded?
      13th century
      True
      True
      single_chunk
    
    
      6
      What happened to Berlin during the 20th century?
      two world wars
      True
      True
      single_chunk
    
    
      7
      What's the most iconic symbol
      Brandenburg Gate
      True
      True
      single_chunk
    
    
      8
      What happened in the 20th century?
      two world wars
      True
      True
      single_chunk
    
  

The results show that late chunking maintains high accuracy for single-chunk queries while improving performance on cross-chunk queries.  While these are example queries and not a full proper eval, you can use this to build intuition about why late chunking works.Why Late Chunking WorksLate chunking solves the lost context problem in several important ways:

Bidirectional context awareness: Each token embedding is influenced by all other tokens in the document, both before and after it. This means references like "the city" can be properly linked to "Berlin" mentioned earlier.

Consistent representation: All chunks from the same document share the same contextual foundation, ensuring that related concepts are represented similarly regardless of which chunk they appear in.

Preservation of long-range dependencies: Information from the beginning of a document can influence the representation of content at the end, maintaining semantic connections across the entire text.

Resilience to boundary selection: Since each token's embedding already contains document-wide context, the specific chunking boundaries become less critical. This means simpler chunking strategies can work just as well as complex ones.

The Importance of Long-Context ModelsLate chunking requires embedding models that can handle long contexts—ideally 8K tokens or more. These models aren't just standard embedding models with longer input windows; they're specifically designed to maintain coherent representations across thousands of tokens.
The key advantages of these long-context models for late chunking include:

Attention across the entire document: They can attend to relationships between distant parts of the text
Training on document-level tasks: They're often fine-tuned on tasks that require understanding document structure
Optimized pooling strategies: They use pooling methods that effectively compress long sequences

Without these capabilities, late chunking wouldn't be possible or effective.

---

# Retrieval 101

**URL:** https://isaacflath.com/writing/Retrieval101

The Challenge of Finding Relevant ContentHave you ever spent hours writing a blog post only to have it disappear into the void? You're not alone. I spend a lot of time making detailed tutorials, explanations, and code examples, yet much of this content is hard to find.
90% of users never venture past the first page of search results, and most scan only the top 3-5 entries before reformulating their query or abandoning the search altogether. For technical blogs, this problem is even more acute - the specialized vocabulary and conceptual relationships between topics make keyword matching particularly ineffective.
Search solutions that rely solely on finding exact words will often have huge misses.  For example my post about custom tags for FastHTML may be be highly relevant to someone looking to use web components but web components is a term never mentioned directly in the blog post!
This disconnect creates a frustrating experience for both content creators and consumers.  Content creators have to spend time trying to jam in keywords to make things more discoverable, and readers struggle to find the solutions they're looking for.
The question becomes: how can we make technical content discoverable by meaning rather than just keywords?What This Post Will DeliverIn this tutorial, you'll learn how to implement a semantic search system using LanceDB. Instead of relying on exact keyword matches, you'll be able to find content based on meaning and conceptual relationships.  We will go beyond the hello-world of "vector-search" and do a hybrid vector-search + keyword search approach and then re-rank final results with a cross-encoder.  By the end of this tutorial, you'll know what that means and how to implement it.
By the end of this post, you'll have a complete solution that can:

Find conceptually related blog posts even when they use different terminology
Surface relevant technical content based on the intent behind a search query
Provide more accurate and helpful search results to your readers

Here's a quick preview of what we'll build:
Loading...
This isn't just theory - you'll implement this system step-by-step using real blog posts, and I'll show you how to adapt it to your own content. Whether you have a personal tech blog, manage documentation for a larger project, or have anything else you want people to be able to search, this approach will help your valuable content reach the right audience
This is the foundation of a modern retrieval system and I am hard-pressed to thing of an example where you want good semantic search but would not want this as the foundation.

💡 Check out the companion repo for runnable code examples

Vector Embeddings: The Key to Semantic SearchAt the heart of semantic search is the concept of vector embeddings.  AI models cannot understand words directly so we have to convert everything to numbers to compare them programatically.  Let's take a simple example, maybe we give 3 words vector embeddings

Cat    = [1.5, 2.5, 2.2]
Dog    = [1.8, 2.6, 2.6]
Animal = [1.6, 2.4, 2.4]
Bog    = [0.1, 0.3, 5.9]

You can see how using just the numbers Cat and Dog are more similar to Animal than they are to Bog.  What does each specific number mean?  I don't know - they don't map to human language!  Similar concepts end up close to each other in this space, even if they use different words.  That's what semantic search is.
In a more targetted example, the phrases "how to test Python code" and "writing unit tests for Python functions" might use different words, but their vector embeddings would be very similar because they represent the same concept.
This leads to the question: "How do you pick the numbers for each word, sentence, or article?".
Modern language models like BERT, GPT, and their derivatives can generate these embeddings by processing vast amounts of text and learning the relationships between words and concepts.  We can use those pre-existing models to generate these embeddings (training a new model to do this is out of the scope of this tutorial).Initial Solution Attempt: Setting Up LanceDBShow codeWe'll prepare our blog posts. For simplicity, we'll extract titles and content from our sample posts:
Credit: This post was inspired by Ben Clavie's excellent work on semantic search implementations. His talk on RAG systems at a conference provided many of the core concepts and techniques explored in this tutorial. I highly recommend checking out his original presentation for additional context and perspectives.  You will be glad you did - it is well worth the time.

  
    
      
      title
      content
    
  
  
    
      0
      Creating Custom FastHTML Tags for Markdown Ren...
      # Creating Custom FastHTML Tags for Markdown R...
    
    
      1
      MeanShift From Scratch
      # MeanShift From Scratch\n\nA deep dive on mea...
    
    
      2
      Python Programming Tips
      # Python Programming Tips\n\nA list of handy t...
    
    
      3
      Introduction To Statistical Testing
      # Introduction To Statistical Testing\n\nAn in...
    
  

The next thing we need is some sort of vector embedding for each post.  As mentioned before, we can us a pretrained model for this.
💡 One place to look for embedding models to use is the MTEB Leaderboard BEIR.  Though be careful because many of the models are overfit to the leaderboard.

  
    
      
      title
      content
      vector
    
  
  
    
      0
      Creating Custom FastHTML Tags for Markdown Ren...
      # Creating Custom FastHTML Tags for Markdown R...
      [-0.0600754, 0.07570859, 0.0017243278, 0.00696...
    
    
      1
      MeanShift From Scratch
      # MeanShift From Scratch\n\nA deep dive on mea...
      [0.022285162, -0.03508064, -0.006767927, -0.04...
    
    
      2
      Python Programming Tips
      # Python Programming Tips\n\nA list of handy t...
      [-0.017614271, -0.015829531, -0.044863362, 0.0...
    
    
      3
      Introduction To Statistical Testing
      # Introduction To Statistical Testing\n\nAn in...
      [-0.0035132996, -0.026535656, -0.10052579, 0.0...
    
  

We can load all that into our vector database, lancedb.Now, we're ready to use LanceDB to search.  There are a two main steps for this1. Create an embedding of your query or question((384,), array([-0.01018321, -0.05370776, -0.08562952], dtype=float32))2. Compare SimilarityNow we can search the table to find most similar embeddings0    0.585938
1    0.810537
2    0.951037
3    0.976564
Name: _distance, dtype: float32
💡 Different models use different distance metrics.  This was trained with cosine similarity per the huggingface model card so I matched to that.
3. See ResultsNow we can see which post is the most similar to the query based on those embeddingsPost: Creating Custom FastHTML Tags for Markdown Rendering
Distance: 0.59
Post: Python Programming Tips
Distance: 0.81
Post: Introduction To Statistical Testing
Distance: 0.95
Post: MeanShift From Scratch
Distance: 0.98
This basic implementation allows us to search our blog posts semantically. When we run a query like ""How do I make web components?", it will find the revelant post even though web component is not mentioned in the tutorial directly.
However, this approach has a lot of limitations.Why the Initial Approach Isn't EnoughOur simple semantic search implementation works, but it has several limitations that make it inadequate for serious technical content:

Full document embeddings lose detail: When we embed entire blog posts, we're compressing thousands of words into a single 384-dimensional vector. This means specific technical details get lost.

Code blocks get mixed with text: Technical blogs contain a mix of explanatory text and code examples. Our current approach treats both the same way, diluting the search quality.

No re-ranking: We're using a simple bi-encoder approach with cosine similarity, but as Ben Clavié explains, this misses the nuance that cross-encoders can provide.

ChunkingTo address the limitations of our initial approach, we need to implement a more sophisticated solution. Following Ben Clavié's recommendations, we'll improve our system by:

Chunking our documents by markdown sections
Adding keyword search capabilities (BM25)
Implementing a re-ranking step

Let's start with the chunking strategy, which will help us preserve more context and detail:There are many chunking strategies you can test, but lets use the most obvious one.  Let's use the chunks defined by the author of the article, and split on markdown headers.

Note: There's lots of discussions on optimal chunk length, and overlap, and different ways to split it.  I recommend starting with what makes sense, and then try out different ones.
[{'title': 'Markdown', 'content': '# Markdown'},
 {'title': 'Chunked', 'content': '# Chunked'},
 {'title': 'Based on markdown', 'content': '## Based on markdown'},
 {'title': 'Headers for RAG', 'content': '## Headers for RAG'}]Now let's apply this chunking function to our blog posts:The most important thing to learn from this entire guide is that when you do things, you should look at your data.  Don't assume things were right.  Don't assume your idea made sense.  Print it out and look!# Intro

This post will cover how to render markdown using zero-md in FastHTML in a practical example. This includes:

  * Defining a custom HTML tag in FastHTML
  * Using external CSS and javascript libraries with FastHTML
  * Adding CSS styling
  * Organize UI into columns

In this tutorial we will convert a markdown of an early lesson in the boot.dev curriculum and a fake conversation between a student and a chatbot about the lesson to HTML. Boot.dev is an online learning platform that offers self-paced, gamified courses for back-end web development.

-----

# Markdown With Zero-md

[code]

    # Import style 1 
    from fasthtml.common import *
    from functools import partial
    
    # Import style 2
    from fasthtml.core import P, Script, Html, Link, Div, Template, Style, to_xml
    from fasthtml.components import show
[/code]

In FastHTML we can use the `P` function to put text in a paragraph `<p></p>` tag (a common way of displaying text). However, markdown is not rendered properly and is hard to read!

While text can be read without styling, markdown has headers, code, bullets and other elements. So we need something more than just a regular text rendering.

We need to convert markdown formatting into a format that HTML understands. We can use a javascript library called zero-md to do this, but this tag does not have a function in FastHTML. There are still two options for using this tag in FastHTML.

> ### 💡 What is zero-md?
>
> In web development, HTML defines the general structure of a web page. However, HTML alone is usually not sufficient. Javascript allows us to extend what we can do beyond out-of-the-box HTML. `zero-md` is a Javascript library that adds functionality for displaying markdown content that we can use with an HTML tag.

The first option is to write the HTML in a text string and use that.

[code]

    NotStr(f'''<zero-md><script type="text/markdown">{lesson_content}</script></zero-md>''')
    
[/code]

> ### 💡 Tip
>
> `NotStr` is a FastHTML function designed for passing a string that should be executed as HTML code rather than a string. In the example above, because `NotStr` is used, FastHTML will treat it as HTML code rather than a Python string. If we removed the `NotStr`, all the HTML tags would be displayed on the page just as they are written rather than being rendered nicely for your web application.

This is fine for very simple things, but the more you build, the messier and harder it gets to work with. It is better to create a FastHTML style tag that works just like everything else. It's incredibly simple to create a custom tag. By importing from `fasthtml.components` the HTML tag will be created automatically (defined in the module's `__getattr__`).

[code]

    from fasthtml.components import Zero_md
[/code]

Now that we have our custom tag defined, we can use that with the `<script>` tag (included in FastHTML) to apply the formatting per the zero-md documentation. For now, we will use the defaults and do nothing with CSS (more details on this later).

[code]

    def render_local_md(md, css = ''):
        css_template = Template(Style(css), data_append=True)
        return Zero_md(css_template, Script(md, type="text/markdown"))
    
    lesson_content_html = render_local_md(lesson_content)
    print(to_xml(lesson_content_html))
[/code]

[code]

    <zero-md><template data-append>    <style></style>
    </template><script type="text/markdown"># Startup bug
    
    A new startup has a bug in its server code. The code is supposed to print messages indicating the server has started successfully.
    
    ## Challenge
    
    Fix the 2 errors in the code and get it to run!
    
    ```python
    print(&quot;Starting up server...&#x27;)
    prnt(&quot;local server is listening on port 8080&quot;)
    ```</script></zero-md>
    
[/code]

The last thing we need to do is load zero-md from a CDN. We can do this by adding a `<script>` tag to the `<head>` of the HTML, and it all works!

[code]

    with open('static/_readme.md') as f: lesson_content = f.read()
    
    zeromd_headers = [Script(type="module", src="https://cdn.jsdelivr.net/npm/zero-md@3?register")]
[/code]

`Html(*zeromd_headers, lesson_content_html)`

-----

# Markdown Conversation Bubbles

We will start with default DaisyUI chat bubbles. For many types of conversations this is fine, but for this use case we need markdown to render properly for code snippets and structural elements.

> ### 💡 Note
>
> This part of the tutorial picks up where the step-by-step the DaisyUI example in the FastHTML documentation leaves off. For more information, start there!
[code]

    #loading messages
    import json
    with open('static/conversation.json') as f:
        messages = json.load(f)['messages']
[/code]

[code]

    # Loading tailwind and daisyui
    chat_headers = [Script(src="https://cdn.tailwindcss.com"),
               Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/[email protected]/dist/full.min.css")]
[/code]

We re-use the code from the daisyUI example with one change. We are using the `render_local_md` function we defined.

[code]

    # Functionality identical to Daisy UI example linked above
    def ChatMessage(msg, render_md_fn=lambda x: x):
        md = render_md_fn(msg['content'])
        return Div(
            Div(msg['role'], cls="chat-header"),
            Div(md, cls=f"chat-bubble chat-bubble-{'primary' if msg['role'] == 'user' else 'secondary'}"),
            cls=f"chat chat-{'end' if msg['role'] == 'user' else 'start'}")
[/code]

Using this, markdown doesn't render properly, causing readability issues.

Instead let's do exactly what we did before with Zero-md. Our markdown renders, however there are some issues with css styles clashing.

[code]

    chat_bubble =Html(*(chat_headers+zeromd_headers), ChatMessage(messages[1], render_md_fn=render_local_md))
[/code]

We can inject CSS styling to handle this issue by telling zero-md to use a template and ignore the default styles to make beautiful properly rendered conversations.

> ### 💡 Tip
>
> CSS allows us to extend what we can do with just HTML by providing a syntax for adding styling to HTML elements in a programmatic way. You may want every header to have a specific text color or every paragraph to have a specific background color. CSS allows us to do that.
[code]

    css = '.markdown-body {background-color: unset !important; color: unset !important;}'
    _render_local_md = partial(render_local_md, css=css)
    chat_bubble = Html(*(chat_headers+zeromd_headers), ChatMessage(messages[1], render_md_fn=_render_local_md))
[/code]

Now that it looks good we can apply this style to all messages

-----

Now we can create a new LanceDB table with our chunked content:We can then query to find the most relevant chunks instead of entire documents.Distance: 0.63
Post: Creating Custom FastHTML Tags for Markdown Rendering : Intro
---
Distance: 0.64
Post: Creating Custom FastHTML Tags for Markdown Rendering : Putting it Together
---
Distance: 0.66
Post: Creating Custom FastHTML Tags for Markdown Rendering : Markdown With Zero-md
---
This chunking approach gives us several advantages:

Each vector now represents a more focused piece of content
We preserve the hierarchical structure of the document
We can return specific sections rather than entire posts
We stay within the token limits of our embedding model

In the next section, we'll enhance our retrieval system by implementing a hybrid search approach that combines vector similarity with keyword matching for more accurate results.Hybrid SearchNow that we've improved our system with chunking, let's implement the next key improvements from Ben Clavié's recommendations:

Adding keyword search (BM25) alongside vector search
Implementing a re-ranking step

Let's start with implementing keyword search to complement our vector search:BM25 is a powerful keyword-based search algorithm that works by analyzing term frequency and document length. We'll use it to complement our vector search by capturing exact keyword matches that semantic search might miss.Split strings:   0%|          | 0/66 [00:00<?, ?it/s]BM25S Count Tokens:   0%|          | 0/66 [00:00<?, ?it/s]BM25S Compute Scores:   0%|          | 0/66 [00:00<?, ?it/s]Split strings:   0%|          | 0/1 [00:00<?, ?it/s]BM25S Retrieve:   0%|          | 0/1 [00:00<?, ?it/s]Post: Creating Custom FastHTML Tags for Markdown Rendering
Section: Intro
Relevance: 0.26
---
Post: Creating Custom FastHTML Tags for Markdown Rendering
Section: Putting it Together
Relevance: 0.25
---
Post: Creating Custom FastHTML Tags for Markdown Rendering
Section: Markdown With Zero-md
Relevance: 0.24
---
Re-rankingSo far with Vector Search a model takes in a piece of text and creates a representation of that output.  This is really fast in practice because all of the documents you want to search against can have these vectors pre-calculated.  Their vector representation doesn't change regardless of the user query so we calculated them up front and stored them in LanceDB.
However, cross-encoders make more powerful vector embeddings.  It accomplished this by examining each query-document pair in context, which helps it understand nuanced relationships that might be missed by the initial retrieval step. For example, it can better understand when a document answers a question even if it uses different terminology.
The process works in two stages:

We use our hybrid search (vector + BM25) to efficiently retrieve a set of candidate chunks
We then apply the more computationally expensive cross-encoder to re-rank these candidates

This approach gives us the best of both worlds - the efficiency of bi-encoders for initial retrieval and the accuracy of cross-encoders for final ranking.Loading default cross-encoder model for language en
Warning: Model type could not be auto-mapped with the defaults list. Defaulting to TransformerRanker.
If your model is NOT intended to be ran as a one-label cross-encoder, please reload it and specify the model_type! Otherwise, you may ignore this warning. You may specify `model_type='cross-encoder'` to suppress this warning in the future.

💡 A good safe bet (today) is to use Cohere Rerank for an API for reranking.  I'm not using this for this blog post because it requires an API key and it's not neccesary for this intro tutorial, but something you should look into!
Split strings:   0%|          | 0/66 [00:00<?, ?it/s]BM25S Count Tokens:   0%|          | 0/66 [00:00<?, ?it/s]BM25S Compute Scores:   0%|          | 0/66 [00:00<?, ?it/s]Split strings:   0%|          | 0/1 [00:00<?, ?it/s]BM25S Retrieve:   0%|          | 0/1 [00:00<?, ?it/s]Post: Creating Custom FastHTML Tags for Markdown Rendering
Section: Putting it Together
Relevance: 0.01
---
Post: Creating Custom FastHTML Tags for Markdown Rendering
Section: Markdown With Zero-md
Relevance: -1.34
---
Post: Creating Custom FastHTML Tags for Markdown Rendering
Section: Markdown Conversation Bubbles
Relevance: -2.31
---
While our hybrid search with re-ranking is already a significant improvement, this are still lots of improvements that can be made.Key Takeaways and Principles

Semantic search isn't magic - It's about transforming text into numbers that capture meaning. These numerical representation are flawed and cannot be relied on exclusively for every type of query.

Domain Knowledge is king - Understanding your specific domain and content type allows you to make intelligent decisions.  Be a user of your own system and actually query and see responses.  Do this A LOT.  This allows you to start with a simple approach, identifying limitations, and systematically addressing them with targeted improvements.

Hybrid approaches outperform single methods - There is no magic answer that fixes all problems.  A combination of vector search, keyword matching, and re-ranking provides significantly better results than any single approach alone. But this is just the basics and there are many more things to add based on use-case.

Chunking matters - How you divide your content has a huge impact on retrieval quality and user experience. The chunks should be meaningful units that preserve context while remaining focused enough to be useful.  After chunking, look at them to see if they make sense!

The bi-encoder/cross-encoder pattern is widely applicable - The pattern of using a fast but less accurate method for initial retrieval, followed by a slower but more accurate method for refinement is super powerful

Evaluation is essential - Though we didn't cover it in this tutorial, having a way to measure search quality is critical for ongoing improvement. What gets measured getscan be improved.

Next StepsIf you've followed along to this point, you now have a powerful semantic search system for your blog posts. But there's massive room for growth and experimentation:

💡 Check out the companion repo to start experimenting!
Extend Your Implementation

Add Metadata Filtering: Enable users to narrow results by programming language, difficulty level, or post type (e.g., "Show me only Python tutorials for beginners").

Add Multi-Modal Search: Incorporate images, diagrams, and code snippets in your search index to find visual explanations alongside text (e.g., "Find me posts with architecture diagrams for microservices").

Add Evaluation Framework: Build a systematic way to measure search quality with metrics like precision and recall to continuously improve your system.  Create implicit evaluation (link tracking) or user feedback systems.

Add Query Pre-processing: Identify and prioritize technical terms and entities in user queries to better match domain-specific content (e.g., recognizing "React hooks" as a specific technical concept).

Add Query Classification: Detect the intent behind searches to provide more tailored results (e.g., distinguishing between "how to" tutorials vs conceptual explanations).

Add Query Expansion: Automatically add related technical terms to queries to improve recall (e.g., expanding "web components" to include "custom elements" and "shadow DOM").

Experiment with different chunking strategies: Test different chunking strategies and sizes to find the optimal balance between context preservation and specificity for your content.

"More Like This" Functionality: Allow users to find similar content to a post they're already reading, creating a natural exploration path through your technical content.

Resources for Further Learning
LanceDB Documentation - Dive deeper into vector database capabilities
Sentence Transformers Library - Explore more embedding models and fine-tuning
Ben Clavié's RAG Talk - The inspiration for many techniques in this post
MTEB Leaderboard - Compare embedding model performance
Rerankers Library - Explore more re-ranking options
Join the ConversationI'd love to hear about your experiences implementing semantic search:

What chunking strategies worked best for your content?
Which embedding models performed best in your domain?
What unexpected challenges did you encounter?

Share your implementation, ask questions, or suggest improvements in the comments below or reach out on Twitter/X @isaac_flath.
Remember, the field of semantic search and retrieval is evolving rapidly. The techniques we've covered provide a solid foundation, but staying curious and experimental will keep your system current.
