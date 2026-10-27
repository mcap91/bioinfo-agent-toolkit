reel: https://www.instagram.com/reel/DeXCWyfgHgz/
captured: 2026-10-27
yt-dlp: 2026.10.26
ffmpeg: 7.0.2-static
faster-whisper: 1.2.1
ctranslate2: 4.8.4
claude: 2.1.281 (Claude Code)

## Caption

5 vector search methods you should know 👇

Flat, IVF, HNSW, IVF-PQ and ScaNN.

They all help find similar vectors, but they do the search differently: checking every vector, searching selected groups, following connections, or using compression.

The trade-off? Speed, memory, and how many of the closest matches you find.
Save this for your next RAG project.

#study #coding #interview #ai

## Transcript

[   0.0] 5-vector search methods. What's the difference?
[   3.0] Flat versus IVF.
[   4.7] Flat checks every store vector. It looks for exact closest matches.
[   9.5] But more documents means more work.
[  12.0] IVF groups similar vectors and searches a few nearby groups.
[  16.5] Fewer comparisons, but it can miss matches elsewhere.
[  20.5] IVF versus HNSW.
[  23.0] IVF searches groups.
[  24.7] HNSW follows connections to layers of vectors that shortcut on a map.
[  30.2] That can make search fast, but the connections take extra memory.
[  33.7] IVF versus IVF PQ.
[  36.7] IVF flat compares full vectors inside those groups.
[  40.7] IVF PQ splits vectors into parts and stores small codes for them.
[  45.7] That saves memory and makes comparison cheaper, but less precise.
[  50.2] And last scan end. This is Google's third system.
[  53.7] It can combine grouping and compressed comparisons to make a shortlist.
[  58.2] Then check that shortlist more accurately so that the detailed comparisons happen on fewer candidates.

## On-screen text

(none)

## Key claims

- Flat checks every stored vector and looks for exact closest matches, but more documents means more work
- IVF groups similar vectors and searches a few nearby groups, resulting in fewer comparisons but it can miss matches elsewhere
- HNSW follows connections through layers of vectors that shortcut like a map, making search fast but requiring extra memory for connections
- IVF compares full vectors inside groups, while IVF-PQ splits vectors into parts and stores small codes for them, saving memory and making comparison cheaper but less precise
- ScaNN is Google's system that combines grouping and compressed comparisons to make a shortlist, then checks that shortlist more accurately so detailed comparisons happen on fewer candidates
- The trade-offs among these methods are speed, memory usage, and recall (how many of the closest matches you find)

## Info channel

spoken

## Mentioned (unverified hints)

- Flat: (no url)
- IVF: (no url)
- HNSW: (no url)
- IVF-PQ: (no url)
- ScaNN: (no url)
