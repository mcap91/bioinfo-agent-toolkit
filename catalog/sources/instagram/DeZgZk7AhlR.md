reel: https://www.instagram.com/reel/DeZgZk7AhlR/
captured: 2026-10-27
yt-dlp: 2026.10.26
ffmpeg: 7.0.2-static
faster-whisper: 1.2.1
ctranslate2: 4.8.4
claude: 2.1.281 (Claude Code)

## Caption

Reading complex layouts or columns straight across can split two different paragraphs into one sentence. PP-DocLayoutV3 takes a page image, finds blocks such as paragraphs and tables, and puts them in reading order. The Paddle team trained V3 to find the blocks and put them in order in one model.

Comment PDF and I’ll send you the course details.

## Transcript

[   0.0] Reading complex layouts or columns straight across
[   2.7] can split two different paragraphs into one sentence.
[   5.4] PP doc layout v3 takes a page image,
[   8.6] finds blocks such as paragraphs and tables,
[  11.1] and puts them in reading order in a unique way.
[  13.5] Another model will later read the text inside each block.
[  16.8] On a two column page,
[  18.2] we definitely want to finish the left column
[  20.4] before starting on the right.
[  21.7] The bottom left paragraph booms
[  23.6] before the top right paragraph.
[  25.8] Sorting blocks just by height is going to get that wrong.
[  28.3] You could use one model to find the blocks
[  30.5] and then another to order them,
[  31.8] but the paddle team trained v3 to find the blocks
[  35.2] and put them in order in one model.
[  37.0] This third version compares each of the blocks
[  39.5] and estimates which should come first.
[  41.0] So it takes every pair of blocks and does that in parallel.
[  44.4] This turns out to work really well
[  46.0] as opposed to having to pick the first block
[  48.4] and then the second and then the third one at a time.
[  51.7] You can do these computations in parallel.
[  54.1] It adds up the pairwise estimates
[  56.8] to figure out how many blocks likely come before each one
[  60.4] and then it's going to sort by that count.
[  62.2] They also tested a version
[  63.6] that learned the reading order separately.
[  65.6] They kept the model that reads the text the same
[  67.9] so they can compare the two ways of learning the order,
[  70.7] whether it's in a single model pairwise
[  73.1] or this second model that does it separate.
[  76.1] The model that was trained on both tests
[  78.4] made fewer ordering mistakes
[  80.0] on the OmniDoc bench benchmark.
[  82.0] With a separate training,
[  83.3] the error score was 0.189
[  86.0] and 0.041 when it was trained jointly.
[  90.2] And so it's quite a lot better.
[  91.6] Then when you put the extracted text back together,
[  94.1] you use this predicted block order.
[  96.0] I cover the full workflow
[  97.4] from evaluating OCR to deploying your pipeline
[ 100.2] in the upcoming PDF to production course.
[ 103.0] If that sounds helpful to you,
[ 104.3] check out the syllabus and I hope to see you inside.

## On-screen text

New model for reading order
Comment PDF

## Key claims

- Reading complex layouts or columns straight across can split two different paragraphs into one sentence
- PP-DocLayoutV3 takes a page image, finds blocks such as paragraphs and tables, and puts them in reading order
- A separate model will later read the text inside each block
- On a two-column page, the left column should finish before the right column starts
- Sorting blocks just by height gets the reading order wrong in such cases
- The Paddle team trained V3 to find the blocks and put them in order in one model, rather than using separate models for detection and ordering
- V3 compares each pair of blocks in parallel and estimates which should come first
- It adds up the pairwise estimates to count how many blocks likely come before each one, then sorts by that count
- They also tested a version that learned the reading order separately while keeping the text-reading model the same
- The jointly trained model made fewer ordering mistakes on the OmniDocBench benchmark
- Error score was 0.189 with separate training versus 0.041 when trained jointly
- The predicted block order is used to reassemble extracted text

## Info channel

spoken

## Mentioned (unverified hints)

- PP-DocLayoutV3: (no url)
