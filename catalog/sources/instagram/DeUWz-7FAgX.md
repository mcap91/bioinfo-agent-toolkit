reel: https://www.instagram.com/reel/DeUWz-7FAgX/
captured: 2026-10-27
yt-dlp: 2026.10.26
ffmpeg: 7.0.2-static
faster-whisper: 1.2.1
ctranslate2: 4.8.4
claude: 2.1.281 (Claude Code)

## Caption

PaddleOCR reads this tax row as over $197,300, but not over $50,525. That doesn't work for a $200K income. Docling gets the upper limit right on this document. Test the documents your application actually uses.

Comment “EVALS” and I’ll send you the free evals guide.

## Transcript

[   0.0] OCR misread an income limit in this tax worksheet. So now software using it can't find the tax
[   5.9] calculation for someone making 200k a year. The worksheet has income ranges with a tax
[  11.0] calculation for every range. In the section for single filers 200k would go in the row
[  17.2] above 197k and up to 250k. Patel OCR's table extraction transcribes the upper limit on that
[  24.6] row as 50,000. That makes the row say over 197,300 dollars but not over 50,525 which just doesn't
[  34.5] work. On the other hand an agent answering tax questions over this might instead tell the user
[  40.2] there's no range for 200,000 dollars this is likely the intended row and give some instructions
[  45.8] assuming that's the right row. Even though it spotted that that uncertainty could make the
[  50.8] user lose trust in it to handle taxes entirely especially if they're not comfortable with the
[  55.3] taxes to begin with they want to make sure it's right. In this case Dockling will read the upper
[  59.7] limit as the 250k like it's supposed to and so you need to check it on your own documents to see
[  65.7] if Dockling or Patel OCR or Minor U or some other model performs best for your particular case.
[  71.1] I wrote a free guide on how to evaluate what OCR model to pick, how to look through the data
[  76.2] and then how to turn that into repeatable tests so you don't have to continue to evaluate
[  80.4] on every new model change. If that be useful to you comment evals and I'll send you the link.

## On-screen text

Section A—Use if your filing status is Single. Complete... Taxable income. If line 15 is— (a) Enter the amount from line 15. Multi... At least $100,000 but not over $103,350 $ Over $103,350 but not over $197,300 $ OCR breaks the income range FREE EVALS GUIDE Comment EVALS

## Key claims

- PaddleOCR misreads the upper limit of a tax bracket row in a tax worksheet table
- PaddleOCR transcribes the row as 'over $197,300 but not over $50,525', which is logically inconsistent
- A $200,000 income does not fit into any row due to this OCR error
- An agent using this bad data might tell the user there's no matching range and guess the intended row, risking user trust
- Docling correctly reads the upper limit as $250,000 on the same document
- Different OCR/extraction models (Docling, PaddleOCR, MinerU, etc.) perform differently depending on the document, so you must test on your own documents
- The author offers a free guide on how to evaluate OCR models and turn evaluation into repeatable tests

## Info channel

spoken

## Mentioned (unverified hints)

- PaddleOCR: (no url)
- Docling: (no url)
- MinerU: (no url)
