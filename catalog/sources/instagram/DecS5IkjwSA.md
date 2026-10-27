reel: https://www.instagram.com/reel/DecS5IkjwSA/
captured: 2026-10-27
yt-dlp: 2026.10.26
ffmpeg: 7.0.2-static
faster-whisper: 1.2.1
ctranslate2: 4.8.4
claude: 2.1.281 (Claude Code)

## Caption

PaddleOCR reads the dollar amounts in this IRS example, but it mixes up what years they go with. It read all 3 amounts, so just checking the numbers wouldn’t catch the error. This doesn’t mean PaddleOCR is bad, Docling is good. You need to run your specific data on the models and see if the outputs match your use case.

Comment PDF and I’ll send you the course details.

## Transcript

[   0.0] Paddle OCR reads the dollar amounts in this IRS example but it mixes up what years they go with.
[   5.4] The IRS list $2033 for the first year and then $2564 for each of the next two years.
[  13.3] In this run, Paddle OCR left the first two years blank and combined second and third in the last
[  19.4] row. It read all three amounts so just checking the numbers wouldn't catch the error.
[  24.7] The first run used Paddle OCR's default table settings and a regular sized image.
[  29.9] I exported the same PDF at a higher resolution and ran it through Paddle Paddle's hosted
[  35.7] demo and hugging face. That demo uses a separate model to find table cells which the first run
[  40.7] didn't use. This new run built the table properly with the amounts connected to the years
[  45.5] but the percentage and deduction headings were blank. When I ran with Dockling the table
[  49.7] did look good. All of the columns were there, all the headers, all of the numbers. The main
[  54.1] thing I would do with this output is try to strip out all the periods and make it consistent.
[  59.0] For example, the first row has dollar signs and percentages where the other ones don't. We'd
[  64.1] want to treat them all numeric. These leading and trailing dots in columns one and two are
[  68.6] also unnecessary so I would look to strip those out as well. I think Paddle OCR is a great tool
[  73.1] and I use them for many cases and I've seen lots of good cases. This doesn't mean
[  76.8] Paddle OCR is bad, Dockling is good. It just means you need to run your specific data
[  82.3] on the models you're going to try and see if the outputs
[  86.0] match what you're expecting for your use case. I cover the full workflow from evaluating OCR
[  91.4] to deploying your pipeline in the upcoming PDF to production course. If that sounds helpful to
[  96.7] you, check out the syllabus and I hope to see you inside.

## On-screen text

Year Basis Percentage Deduction 1st . . . . . . . . . . . $100,000 2.033% $2,033 2nd . . . . . . . . . . 100,000 2.564 2,564 3rd . . . . . . . . . . 100,000 2.564 2,564 Year ... 2nd ... OCR loses the year labels Comment PDF

## Key claims

- The IRS example table lists $2,033 for the first year and $2,564 for each of the next two years
- PaddleOCR's first run (default table settings, regular resolution) left the first two years blank and combined the second and third years in the last row
- PaddleOCR read all 3 dollar amounts correctly, so just checking the numbers wouldn't catch the year-mismatch error
- A second PaddleOCR run using a higher-resolution PDF export and PaddlePaddle's hosted Hugging Face demo (which uses a separate table-cell detection model) correctly connected amounts to years, but left the percentage and deduction headings blank
- Docling produced a complete table with all columns, headers, and numbers present
- Docling's output still needs cleanup: stripping inconsistent dollar signs/percent signs for consistent numeric formatting, and removing unnecessary leading/trailing dots in columns one and two
- PaddleOCR is described as a great tool with many good use cases, not a bad tool
- The comparison is not meant to declare PaddleOCR bad and Docling good; results depend on testing your specific data against each model for your use case
- The creator offers a 'PDF to production' course covering OCR evaluation through pipeline deployment, available by commenting 'PDF'

## Info channel

spoken

## Mentioned (unverified hints)

- PaddleOCR: (no url)
- Docling: (no url)
