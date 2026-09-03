# Using Documents — Isaac Flath

Extraction, question answering, workflows, and agents.

---

# Document Answers You Can Check

**URL:** https://isaacflath.com/writing/document-answers-you-can-check

I ask a question over a stack of documents ("What is the underwriting fee on this loan estimate?") and the model answers "$1,097."
Is that right? The only way to know for sure is to check the document, but if I have to read the whole document to find it then it didn't save me any time.
Often, a research report is built from many documents from a corpus of hundreds of other documents. Nobody can check them all, so nobody trusts any of them.
This is what citations are for, but general citations aren't enough. I need a citation to the specific table row, so checking takes seconds instead of a re-read.
Developers need to do the same thing to verify the system works properly. These citations make checking if answers are correct much faster and cheaper, and once checking is cheap, experiments are cheap (esp. with coding agents). We can swap one part of the system, rerun all the same questions, and watch what changes.
This post introduces the lab built for me to do these experiments quickly and the first three experiments I ran in it.

The setup: small on purpose
The lab is 77 document pages, 22 questions, an agent that answers them, and a review app to annotate answers and citations.
It's small enough that I can read every agent trace, look at every cited box, understand each failure, and learn from the patterns.
I created six kinds of questions:

Look up one value (e.g. fee in a table, elevation value on a map)
Combine several values on a page
Scan all documents to answer a question
Traps where a field is blank or there's no answer in the documents
Paraphrases that share no words with the page ("What does the lender charge to assess whether the borrower qualifies?" for the Underwriting Fee)
Near-misses, where a different document has an almost identical table (the Closing Disclosure repeats the Loan Estimate's fees at different amounts)

Many of the answers to these questions are in text that's hard to read like a column number on a dense census grid, the elevation of a peak on a map, the value of a bar on a bar chart, government forms, and dense financial tables.
How a checkable citation works
A citation is a set of coordinates for the corners of a box and the text that was OCR'd from that box. While different models and approaches define bounding boxes differently, I created a standard format for the agent to use. Then, the annotation can put an orange rectangle around the citation on the original page.

The citation shows me if an answer is wrong and why. For example, one question asked what the semilatus rectum of the transfer orbit was. The citation immediately showed me that this was described in a scanned handwritten equation in a NASA document. It was a bit hard to read, but the subscripts in the answer did not match the page. The trace then showed that the OCR'd output matched the agent's answer, so I knew the OCR model was struggling to read the small handwriting properly.
The baseline
I set up a baseline with all three parts of the pipeline:

Reading: Surya, an open model for OCR on documents
Finding: grep and rg over Surya's output files
Answering: pi coding agent with gpt-5.6-luna.

This setup got 14 out of 22 questions correct at a median of 24 seconds per question, and cost $0.29 for all 22. All the major errors came from the OCR model (Surya). For example, Surya returned figures without the text labels inside and misread subscripts in a scanned equation.
On the equation question, the agent searched the blocks for the semilatus rectum and found it. The agent noticed the equation's text didn't match the description, so it tried to find the original scan. Because the sandbox only contained the Surya model outputs (to prevent this kind of cheating), it found nothing and quoted the equation just as Surya extracted it.

Experiment 1: remove the reading model
I started with changing the reading/OCR model for two reasons. First, the reading model was the constraint in the baseline. And second, I wanted a baseline of just giving an agent OCR tools and letting it figure it out. I gave the agent the page images directly, and told it to return citations as pixel rectangles on the page.
The agent was told it had Tesseract, ImageMagick, and Poppler installed and it could use them if they would be helpful. It ran OCR with Tesseract on all the images, read the outputs to find relevant documents, then cropped and upscaled regions it failed on with ImageMagick. It adapted based on the situations, like using numpy to measure a bar's height on a chart to estimate a percentage.
This setup answered the most questions correctly out of all the experiments. It read the census column number, the map elevation, the URL, and the legal citation straight off the pages that Surya failed at.
It did this with its own self-built self-serve OCR process.

While it was the most accurate, it was MUCH slower and MUCH more expensive than every other test: a median of 4 minutes per question against the baseline's 24 seconds, and $0.66 against $0.29. Lookups on clean forms took about a minute, scanned maps and charts took five, and the two questions that hit the 900-second timeout were the cross-document ones that forced it to OCR every page in the corpus. Maybe it would have gotten those right eventually. A third did find the right answer, but it returned malformed JSON (I counted that as a failure.)
Experiment 2: swap how the agent finds evidence
After changing how it processes and reads documents, it's time to change how it searches for the right documents.
I wanted to test changing the retrieval strategy from grep to semantic search to see the impact. I gave the agent a semantic search tool over the OCR outputs of the Surya model. I instructed the agent to use the semantic search once or twice, then read relevant files directly.
Accuracy was the same as the baseline (the bottleneck in the baseline was the OCR model, not search), and per-question times were about the same too (median 30 seconds vs 24). But it cost $0.18 instead of $0.29, making it the cheapest approach.
I did have to tune the prompt a bit. In my first attempt, the agent kept rephrasing queries over and over instead of accepting that the answers to some questions weren't findable.
Experiment 3: swap the agent itself
Last phase! Since the Prime Agent harness came out this week, I decided to try swapping the vanilla pi harness for the Prime Agent. Instead of calling Bash tools, it would make Python calls to a persistent Python session (think Jupyter notebook). This run used gpt-5.4 instead of Luna as well.
It scored 13 of 22: the baseline's eight reading failures, plus a transfer taxes trap. The baseline correctly said the field is blank, but the Prime Agent said it was $0. Null values are not the same as $0, so I called that a failed answer. Questions took about twice as long as the baseline (median 48 seconds vs 24) and cost six times as much ($1.81 all-in).

The comparison
Same 22 questions, four configurations:

ConfigurationCorrectAll-in costMedian time/questionPage images (vision + self-serve OCR)17/22$0.664m 03s (two 900s timeouts)Surya blocks + grep (baseline)14/22$0.2924sSurya blocks + semantic search14/22$0.1830sSurya blocks + Prime Agent13/22$1.8148s
The three text runs fail the same questions because it was the OCR model (Surya) that failed on those tasks. The image run gets more right, slowly and expensively.
What's next
This framework will let me keep experimenting across every dimension of question answering and report generation over documents: the reading/OCR model, the retrieval pipeline, and the model or agent harness that orchestrates it all.
From here I will keep adding more documents, more and harder questions that help me understand capability differences. And I will test more OCR approaches, more retrieval methods, and more harness designs.
If you're interested in the experiments I've got running, subscribe and I'll send them to you as I finish them.

---

# How My RLM Tool Works

**URL:** https://isaacflath.com/writing/rlm

An LLM writes Python code to do research.
Python reads, sorts, filters, and fans out over search hits.
I give it extra functions to run cheap LLM calls and ask more questions.
An LLM writes code.
A REPL runs it.
The output comes back.
The LLM writes more code.
That loop is a Recursive Language Model (RLM).
The rest of this post unpacks that loop.
What a REPL actually is.
What functions are in scope and why.
How my harness keeps the REPL alive across turns.
How an LLM "calls a tool" through a Pi extension.
How to inspect your RLM logs to improve it.
Pi is an agent harness like Claude Code.
My implementation is a Pi extension written in TypeScript.
The REPL host is a Python subprocess.

What a REPL is
REPL stands for read-eval-print loop.
Most programmers have used one.

Three things happen on every line:

Read. Python reads what you typed.
Eval. It runs the code, updating the namespace that holds your variables.
Print. It shows you the result.
Loop. It gives a place to write more code.

The important word is namespace.
Once you assigned x = 3, x is still 3 on the next line.
That's because it's stored in the namespace.
That's what separates a REPL from a script that runs once and exits.
The read-eval core fits in four lines:

That's the heart of the REPL host.
The namespace stores variables like x from above.
It also store functions that can be used.
A real REPL also auto-prints whatever expression is on the last line.
This one doesn't.
It only prints what is explicitly print()ed.
The LLM uses print() to send output back.
The RLM Trick
The LLM is the one writing code into the REPL.
The LLM answers a question by writing Python.
For a minimal example I could ask my RLM "What is 5x5 + 10x10?"
An (kinda stupid) RLM might solve it like this

"Hmm, let's break this down in my REPL. I need to know what 5*5 is first"

"I also need to know what 10*10 is":

"Great, I have all I need to answer the question. Let's add them up":

"Isaac, the answer is 125".

The namespace has a few extra things in it before the LLM starts, like:

context: Variable pre-loaded with lots of search hits from my knowledge base.
kb_read(path): Function to read the full text of a wiki page (from my personal knowledge base).
llm_query(prompt): Function to run a cheap LLM call and return the answer.
llm_query_batched(prompts): Same, but runs many calls in parallel.
rlm_query(prompt): Function to run another RLM query
FINAL(answer): Function to end and provide the final answer.

Here's what a typical LLM turn looks like in real text:

The LLM emits prose plus a fenced code block.
The Pi extension (my RLM tool) extracts the code, runs it in the REPL, captures the output, and sends the output back as the next user message in the LLM's chat history.
On the next turn the LLM might do more, or call FINAL() with its answer.
High-Level Architecture
A quick vocabulary note first.
The whole thing, from user question to REPL to answer, is an investigation.
The LLM driving the REPL is the investigator. It writes the search strategy.
The cheaper LLM that llm_query calls is the analyst.
Three pieces talk to each other:

The user question is a string from your agent.
The Pi extension is the tool Pi can call.
When Pi decides to call rlm_query this code runs.
It creates the namespace, spawns Python, runs the loop, and returns a final answer.
The Python REPL subprocess is one Python process per rlm_query call.
It has a namespace dict that lives for the whole run.
The extension keeps writing code every turn.
That code stores results in the namespace.
One Turn of the Loop
The extension calls the LLM with the running chat history.
The chat history is the system prompt, the original question, and every prior turn's code and output.

The LLM responds with prose and a fenced Python code block.
The extension pulls the code out.
The code block goes to the Python REPL process (stdin).
(Remember it has the persistent namespace.)
Python writes output (stdout), error (stderr), and any FINAL back as JSON.
The extension appends that to the next message.
If FINAL was set the loop ends and returns the answer.
Otherwise the next turn starts.
The loop can also end if the LLM stops writing code, runs out of turns, or exhausts its budget.
What's in the Namespace
The extension does two things to set up the REPL.
1. Loads the context.
The extension sets a context variable in the REPL.
This has a list of search hits from my knowledge base for the user's question.
Each hit is a dict with the path, a relevance score, and a short snippet.
The LLM sees a description of the variable in the system prompt.
This is its starting point.
2. Installs the builtins.
Functions the LLM can call:

functionwhat it doeskb_search(query, k=5, scope='wiki')re-query agentkb for more contentkb_read(path)get full text of one wiki pagellm_query(prompt)one cheap LLM call (string in, string out)llm_query_batched(prompts)concurrent batch of calls (cap 16)rlm_query(prompt, context=None)recursive RLM callrlm_query_batched(prompts, contexts=None)concurrent batch (cap 4)FINAL(answer)terminate with this answerFINAL_VAR(name)terminate with the value of namespace variable nameSHOW_VARS()inspect what's in the namespace
Plus the entire Python standard library like itertools, collections, list comprehensions, f-strings, everything.
The RLM is given another pattern called chunking.
It's used when a page is too long to deal with.

How the Pi Extension Talks to Python
When the LLM writes kb_search("oauth") in the REPL it runs as a normal Python function.
But kb_search doesn't do the search itself.
It sends the arguments to the Pi extension, which runs the real search and hands the answer back.
From the LLM's view nothing weird happened.
A function returned a value.
Here's what kb_search looks like on the Python side:
It sends the call to the extension via RPC (remote procedure call).

It just gives arguments to the extension and returns what comes back.
kb_search uses agentkb, a Python library I wrote, to search my knowledge base.
My knowledge base is a very large collection of markdown files.
But if agentkb is a Python library I wrote, why not call agentkb directly from Python? Why the RPC stuff?
Three reasons.
One implementation.
I want to use kb_search by itself sometimes.
Putting it in Pi means the REPL and Pi can use the same implementation.
Change behavior once for both places.
llm_query can't really go any other way.
LLM calls need provider auth, budget tracking, and concurrency limits.
That lives in Pi's model registry.
Once llm_query and rlm_query have to round-trip, doing the same for kb_search is consistent.
Budget, logging, and limits live in one place.
The extension logs all LLM calls, searches, retries.
Running kb_search in the extension means logging is easy.
I don't have to add new logging for Python.
But timing is tricky.
The extension sends a block of code for Python, and Python sends back the result when the whole block is done.
That's slow.
Inside that block the code might also call kb_search or llm_query several times, and each one needs its own round trip while the block is still running.
So there are two channels.
One carries the big "run this code, here's the result" exchanges.
The other carries the small "I need X" requests the Python functions make mid-run.

Recursion: What rlm_query Actually Does
rlm_query is just another builtin in the namespace.
It's the recursive part of recursive language model.
When the investigator calls rlm_query(prompt, context=subset_of_context) a new smaller investigation starts.
New query. New namespace. New REPL. New context.
If the call tree is at the recursive limit rlm_query downgrades to a plain llm_query.

Budget is shared across the tree.
A max_budget variable tracks total LM spend across all depths and parallel siblings.
If the budget is reached the investigation ends.
Children get whatever the parent has left.
Models can differ by depth.
The investigator (depth 0) runs on the smarter model.
By default that's GPT 5.4.
Children at depth ≥ 1 and all llm_query calls run on the analyst model.
By default that's GPT 5.4 mini.
Fan-out work doesn't need the big model.
Putting It All Together
Here's the full picture of one rlm_query call.

In parallel a logger appends one NDJSON line per event to a log file.
Exploring a Run in Jupyter
Every RLM call writes NDJSON to a log file while it runs.
One line per event:
Turn starts, assistant prose, code blocks, stdouts, RPC calls, final answers.
When the loop finishes a converter turns that log into a Jupyter notebook.
Every run leaves behind a .ndjson and a .ipynb.
The front-matter cell records the question, the models, the budget, and the log path.

Below that the notebook reads as a timeline.
Each investigator turn becomes a markdown cell with the prose followed by a code cell with the Python block and its result attached.
Child investigations are inlined in order.

The first cell is a bootstrap that launches a local rlm-server subprocess and installs the same kb_search, kb_read, llm_query, rlm_query, and FINAL shims the live run used.
It preloads the same context variable from the original leads.
The namespace in the notebook is what the investigator had.
That makes the notebook live, not a replay.
If you change things and run the code you get the result of the "what if".
What does this let you do?
Prototype. Define new helpers like kb_grep or a kb_summarize and use it the way the investigator would.
Eval. Code by hand what the investigator should have done, then compare it to what it did.
Improve. Take what you learn from the comparison and change the system prompt, builtins, or initial context.
This means the traces are live experiments, not logs.
Why This Shape Works
Most tool calls are flat.
The model emits a tool call, you run it, you give it the result, repeat.
Each step is independent.
RLM's shape works for three reasons.
Richer shell.
Coding agents already do search.
They run grep, find, ripgrep.
The model reads stdout and decides what to run next.
RLM is the same idea with a more powerful shell.
Python instead of bash.
Functions instead of static binaries.
The namespace persists across turns so a search result becomes a variable you can sort, slice, fan out over, and feed back to the next search.
Less noise in the main context.
A normal agent searches by emitting tool calls into its own context.
Every hit, every page, every false lead fills the window.
The model writing your code is the same model wading through search noise.
RLM moves all of that into a separate process with a separate LLM.
The investigator can pull 50 hits, read 30 pages, throw 28 of them out, and the main agent never sees the 28.
Three good ideas stacked.
An agentic loop.
A dynamic programming language with persistent state.
Semantic search (late interaction retrieval models keep crushing benchmarks).
Each is powerful alone.
Stacking lets them handle filter, fan-out, and synthesis better.
The full original paper is at arxiv:2512.24601 (Zhang, Kraska, Khattab, MIT OASYS).
My implementation is different in places. Pipes for IPC instead of TCP. No sandboxed Python process.
But all the core ideas are theirs.
Context as a Python variable, LLM as the programmer, REPL as the runtime.
