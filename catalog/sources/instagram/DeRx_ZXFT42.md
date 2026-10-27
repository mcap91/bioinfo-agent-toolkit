reel: https://www.instagram.com/reel/DeRx_ZXFT42/
captured: 2026-10-27
yt-dlp: 2026.10.26
ffmpeg: 7.0.2-static
faster-whisper: 1.2.1
ctranslate2: 4.8.4
claude: 2.1.281 (Claude Code)

## Caption

Reducto predicts two things: how much a bigger OCR model improves accuracy and how much time it adds. You can then adjust the routing decision without retraining. Tesseract and Chandra are my example pair, not the models Reducto said it used.

Comment “OCR” and I’ll send you both OCR guides.

## Transcript

[   0.0] Reducto wrote about their auto-router approach with two trained regression models. When you
[   4.6] need to extract text from a PDF, one of the first decisions is which OCR model to use.
[   8.9] Often people use a router to do that by page, because using the slowest model in every page
[  14.1] wastes a lot of time and money, but if cheaper models fail 20% more often, that's a problem too.
[  19.3] You want the best of both worlds. Reducto's approach runs the same pages through a fast
[  23.4] model as well as a bigger one. I don't know which models they used, but to build
[  27.5] something similar yourself, you could use Tesseract for a super light model and Chandra for a heavy model.
[  32.7] To create the dataset, run every page through both and score and time them. For example,
[  38.7] Tesseract may score 80 out of 100 on one page and take one second and Chandra might score
[  45.0] 90 and take three seconds. The changes between the two is what we want to predict.
[  50.2] Now, instead of putting all of Tesseract's output into the regression model,
[  54.5] they calculate its statistics. For example, word count and confidence scores from Tesseract.
[  60.5] Then we can train one regression model from statistics as the input to that accuracy delta
[  66.6] between the two models, and then another from statistics to the latency delta.
[  70.6] Once you have this estimated accuracy improvement and latency change,
[  74.4] you can create logic to say whether that trade-off is worth it for the particular page
[  78.7] is a 5% boost in accuracy worth three seconds in latency. That depends on the use case.
[  84.0] Now, we did this for Tesseract and Chandra, but you could do this for any model pair. You could run
[  88.6] something through light parse and use that to predict whether dockling should be run for OCR.
[  93.9] You could then predict, should I send it to Quinn for a VLM? And you could build up this
[  98.7] router that way. I think this is a pretty good approach to have the regression model.
[ 102.2] The other option is to have a classifier where you predict is it worth it to move up
[ 105.9] or not, but the regression model kind of pushes that logic a little bit later
[ 110.0] so that you can kind of tweak and adjust your router without retraining.
[ 113.3] For more information on hard OCR tasks like messy scans, tables, hand writing,
[ 118.1] check out my guides on choosing an OCR model and using VLMs for hard documents.

## On-screen text

When is a bigger model actually better? A practical framework for model routing | When is bigger worth it? | FREE OCR GUIDES Comment OCR | for hard documents.

## Key claims

- Reducto's auto-router approach uses two trained regression models to predict accuracy improvement and latency added by a bigger OCR model.
- Running the slowest OCR model on every page wastes time and money, but cheaper models can fail more often, so a router is used to balance the tradeoff.
- Reducto's approach runs the same pages through both a fast model and a bigger model to build a training dataset.
- To replicate this, you can use Tesseract as a light model and Chandra as a heavy model, though these are not necessarily what Reducto actually used.
- Each page is scored and timed for both models, and the delta between them (accuracy and latency) is what gets predicted.
- Instead of feeding raw model output into the regression model, summary statistics (e.g., word count, confidence scores) from the light model are used as input.
- One regression model predicts the accuracy delta between the two models; another predicts the latency delta.
- These predictions let you decide whether the tradeoff (e.g., 5% accuracy boost for 3 seconds latency) is worth it for a given page, depending on use case.
- This approach generalizes to any model pair, such as LightParse to Docling, or Docling to a VLM like Qwen.
- A regression model is preferred over a binary classifier because it pushes the routing decision logic later, allowing adjustment without retraining.
- Comment 'OCR' to receive guides on choosing an OCR model and using VLMs for hard documents.

## Info channel

spoken

## Mentioned (unverified hints)

- Reducto: (no url)
- Tesseract: (no url)
- Chandra: (no url)
- LightParse: (no url)
- Docling: (no url)
- Qwen: (no url)
