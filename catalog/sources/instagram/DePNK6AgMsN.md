reel: https://www.instagram.com/reel/DePNK6AgMsN/
captured: 2026-10-27
yt-dlp: 2026.10.26
ffmpeg: 7.0.2-static
faster-whisper: 1.2.1
ctranslate2: 4.8.4
claude: 2.1.281 (Claude Code)

## Caption

PP-DocLayoutV3 segments curved and angled text into regions and predicts reading order. Then another model reads what's inside. A paragraph box shouldn't need to include part of the title.

Comment “PDF” and I’ll send you the course syllabus.

Bottle photo: Eliazar Parra Cardenas / Wikimedia Commons, CC BY 2.0 (resized). https://commons.wikimedia.org/wiki/File:Herbalessencebottles.jpg
https://creativecommons.org/licenses/by/2.0/

## Transcript

[   0.0] New OCR model that handles warped, curved and angled text and layouts. This is really great for OCR
[   6.2] when you have scans that are crooked product photos from different angles,
[  10.7] security footage or robotics where your angle is wherever the camera happened to be and more.
[  16.2] pp.layout v3 classifies and segments regions and predicts reading order. Then there's a model
[  22.9] after that to read what's in the boxes. As you can see the bounding boxes are not just
[  27.7] a square it can handle a lot of these warped images nicely and it can put them at an angle.
[  32.0] If we compare this to another approach we can get bounding boxes and it's like yeah it kind of works
[  37.6] but it's also kind of weird an incorrect text fits inside of them. The bounding box is clearly way
[  43.6] bigger than it needs to be so for the bounding box in the paragraph to work it has to be so big
[  49.8] that part of the title is actually in that bounding box. This kind of thing happens all
[  54.1] the time when you have user intake forms and you're maybe doing identity verification
[  58.5] it's in driver's licenses and things like that. I cover the full workflow from evaluating OCR to
[  64.2] deploying your pipeline in the upcoming PDF to production course. If that sounds helpful to
[  69.3] you check out the syllabus and I hope to see you inside.

## On-screen text

OCR for curved text / OCR when you have / paragraph_title / Place / ...nothing more dangerous than a familiar face... As funeral mourners stand in silence at Immaculate Cemetery, a deafening cry cuts through the air. Lying crumpled at the bottom of an open grave is the bloodied body of a young woman, and Detective Lottie Parker is called in to investigate... Read More... / paragraph_title / PDF TO PRODUCTION Comment PDF / you inside.

## Key claims

- PP-DocLayoutV3 is a new OCR layout model that handles warped, curved, and angled text and layouts.
- It is useful for crooked scans, product photos taken from different angles, security footage, and robotics where camera angle varies.
- PP-DocLayoutV3 classifies and segments regions and predicts reading order, with a separate model reading the text inside the detected boxes.
- Its bounding boxes are not just squares/rectangles — they can be angled and fitted to warped images.
- A comparison approach produces bounding boxes that are much bigger than needed, causing incorrect/extra text (e.g., part of a title) to fall inside a paragraph box.
- This bounding-box imprecision issue commonly occurs with user intake forms and identity verification documents like driver's licenses.
- The creator has an upcoming 'PDF to Production' course covering the full workflow from evaluating OCR to deploying a pipeline.
- Viewers can comment 'PDF' to receive the course syllabus.

## Info channel

spoken

## Mentioned (unverified hints)

- PP-DocLayoutV3: (no url)
