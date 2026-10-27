source: https://www.reddit.com/r/learnmachinelearning/comments/1x5mrkq/i_built_event2vector_word2vecstyle_embeddings_for/
captured: 2026-10-27
playwright: 1.64.1
chromium: 156.0.8078.4

Skip to main content
I built event2vector: word2vec-style embeddings for event sequences where order actually matters : r/learnmachinelearning
Sign Up
Log In
Expand user menu
Go to learnmachinelearning
r/learnmachinelearning
•
13d ago
[deleted]
I built event2vector: word2vec-style embeddings for event sequences where order actually matters
Sorry, this post was deleted by the person who originally posted it.
Share
Sort by:
Comments Section
CriticalTemperature1
•
13d ago

I like the idea of interpretable sequence embeddings, have you considered conditioning each event's embedding on the accumulated history vector? Something like

h_t = h_{t-1} + f(e_t, h_{t-1})

So the same event could contribute differently depending on what preceded it

Reply
Share
sulcantonin
•
13d ago

Hi CriticalTemperature1, genius, noted!!!! So far, I tried to stick to the original additive model because I have proofs that I wanted to have fulfilled for the paper.

I noted it on the list together with u/Urajimiru-kendoka's idea that I would like to explore!

Thank you very much for feedback!

Reply
Share
Urajimiru-kendoka
•
13d ago

I am on the way of trying your tool, sulcantonin, to implement in my custom agent for orchestrating tasks. The idea here - is to get P(failure) in mid-time of execution for re-planning. It also should highlight risks etc

So, if you interested - I can share my results later on.

3 more replies
Zenist289
•
12d ago

Wait that sounds like an RNN with extra steps

CriticalTemperature1
•
11d ago

I think its similar but RNNs trade interpretability for more expressiveness which I think we want to bring back the interpretability side here

orndoda
•
13d ago

This was also my first thought after a quick reading of the docs.

sulcantonin
•
11d ago

u/CriticalTemperature1 I was thinking about it and if we embed the f(e_t, h_{t-1}), we break the linear compositionality, but if we add an affine transformation in 0.4.1 version. Thanks man!

affine	x ↦ exp(M_e) x + v_e on the left	events that act on the history (shrink, stretch, rotate it), not only add to it affine x ↦ exp(M_e) x + v_e on the left events that act on the history (shrink, stretch, rotate it), not only add to it

CriticalTemperature1
•
11d ago

Brilliant, I really like this approach. So I believe now each embedding is associated with a transformation matrix. You might also be able to bootstrap these from existing embedding models like gemini embeddings etc

Urajimiru-kendoka
•
13d ago

hi. I guess, would be interesting use case - to try sequence of decisions from Jev-like models to put into your event2vector tool. this should help trace and predict decision chains outcomes

sulcantonin
•
13d ago

On it! Great idea.

OffbeatFunction
•
13d ago
dutchpsychologist
•
13d ago

Very interesting! The website helped a lot in explaining

JohnWangDoe
•
11d ago

Man so much to learn

Anonononomomom
•
13d ago

Love to apply this to next best action modeling having events sequence weighted has great application benefits

demonic_mnemonic
•
11d ago

Isnt this just graph embeddings essentially?

sulcantonin
•
11d ago

It was one of the hardest points to justify during reviews. It is learned to compose sequences with the linear compositions. That’s the feature most graph embedding approaches don’t directly enforce

For instance, I gave it randomly shuffled pairs of numbers to learn and the 1D embedding learned that optimal representation would be if each number is represented as its number in embedding space.

Frogman5678
•
12d ago

Hi, Visited your website and rwad the docs. This is brilliant work! One recommendation and application I wanted to add that you may want to explore is adding the capability to define classes and topic modelling. My thinking is that this package would be very useful in the analysis feedback and churn like some has stated in another comment

ZiddyBlud
•
10d ago

What's the point of this

More posts you may like
Related posts
Mechanical Neural Network v2
r/learnmachinelearning
•
12h ago
Mechanical Neural Network v2
199 upvotes · 16 comments
Sephora
•
Ad
TLDR: get beauty from people who get beauty, only at Sephora.
sephora.com
Shop Now
I did ML research at MIT. If you have 10+ YOE and want to go deeper in Python, ML or LLMs, or switch into ML, I mentor 1:1.
r/learnmachinelearning
•
5d ago
I did ML research at MIT. If you have 10+ YOE and want to go deeper in Python, ML or LLMs, or switch into ML, I mentor 1:1.
112 upvotes · 40 comments
every ml course stops at model.fit(). here's what happens after
r/learnmachinelearning
•
5d ago
every ml course stops at model.fit(). here's what happens after
103 upvotes · 24 comments
A free deep learning textbook + 68 Python notebooks, from neural network basics to transformers and diffusion models
r/learnmachinelearning
•
5d ago
A free deep learning textbook + 68 Python notebooks, from neural network basics to transformers and diffusion models
73 upvotes
Understanding Attention in Transformers Is Much Easier Knowing Which Problem They Solve
r/learnmachinelearning
•
7d ago
Understanding Attention in Transformers Is Much Easier Knowing Which Problem They Solve
72 upvotes · 9 comments
How do you actually learn a Python library like scikit-learn, PyTorch, or sentence-transformers? Looking for a method, not just resources.
r/learnmachinelearning
•
6d ago
How do you actually learn a Python library like scikit-learn, PyTorch, or sentence-transformers? Looking for a method, not just resources.
71 upvotes · 31 comments
I made a website to learn Machine Learning interactively.
r/learnmachinelearning
•
6d ago
I made a website to learn Machine Learning interactively.
62 upvotes · 6 comments
I made a free VS Code extension that shows tensor shapes while you step through your model
r/learnmachinelearning
•
4d ago
I made a free VS Code extension that shows tensor shapes while you step through your model
51 upvotes · 2 comments
Not able to clear Machine Learning Interviews, please help
r/learnmachinelearning
•
3d ago
Not able to clear Machine Learning Interviews, please help
47 upvotes · 24 comments
How well do you really know Pandas? 🐼
r/learnmachinelearning
•
5d ago
How well do you really know Pandas? 🐼
44 upvotes · 2 comments
A free, interactive book that goes from linear algebra to frontier AI. Looking for honest feedback.
r/learnmachinelearning
•
2d ago
A free, interactive book that goes from linear algebra to frontier AI. Looking for honest feedback.
43 upvotes · 5 comments
Let's do legendary CS336 Language Modelling From Scratch together!
r/learnmachinelearning
•
3d ago
Let's do legendary CS336 Language Modelling From Scratch together!
41 upvotes · 15 comments
"AI puzzles": a new format between a benchmark and an open-problem list
r/learnmachinelearning
•
2d ago
"AI puzzles": a new format between a benchmark and an open-problem list
40 upvotes · 6 comments
Learn Neural Networks from Scratch — Free GitHub Repo + Video
r/learnmachinelearning
•
7d ago
Learn Neural Networks from Scratch — Free GitHub Repo + Video
37 upvotes · 2 comments
How did you push through the math/theory side of ML when you couldn’t focus at first?
r/learnmachinelearning
•
2d ago
How did you push through the math/theory side of ML when you couldn’t focus at first?
32 upvotes · 26 comments
I created a page about Andrej Karpathy and his tutorials
r/learnmachinelearning
•
15h ago
I created a page about Andrej Karpathy and his tutorials
30 upvotes · 1 comment
Waymo ML Technical Screening
r/learnmachinelearning
•
3d ago
Waymo ML Technical Screening
29 upvotes · 17 comments
I feel like I'm years behind machine learning.
r/learnmachinelearning
•
4d ago
I feel like I'm years behind machine learning.
26 upvotes · 14 comments
SWE struggling to become productive in ML inference infrastructure. How would you systematically close the knowledge gaps?
r/learnmachinelearning
•
1d ago
SWE struggling to become productive in ML inference infrastructure. How would you systematically close the knowledge gaps?
24 upvotes · 7 comments
I made a free site of interactive ML explainers where the sliders run the actual math
r/learnmachinelearning
•
2d ago
I made a free site of interactive ML explainers where the sliders run the actual math
23 upvotes · 1 comment
how much programming knowledge is needed for machine learning?
r/learnmachinelearning
•
3d ago
how much programming knowledge is needed for machine learning?
23 upvotes · 31 comments
Built a 30M-parameter GPT-style language model from scratch
r/learnmachinelearning
•
5d ago
Built a 30M-parameter GPT-style language model from scratch
23 upvotes · 10 comments
Should You know Autograd
r/learnmachinelearning
•
13h ago
Should You know Autograd
22 upvotes · 10 comments
How to find mentor to learn AI/ML?
r/learnmachinelearning
•
4d ago
How to find mentor to learn AI/ML?
21 upvotes · 11 comments
is it always possible to find the minimum of a convex function using gradient descent with a reasonable learning rate?
r/learnmachinelearning
•
5d ago
is it always possible to find the minimum of a convex function using gradient descent with a reasonable learning rate?
18 upvotes · 12 comments
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
