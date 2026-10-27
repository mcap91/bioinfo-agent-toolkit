reel: https://www.instagram.com/reel/DebFucxs5Xp/
captured: 2026-10-27
yt-dlp: 2026.10.26
ffmpeg: 7.0.2-static
faster-whisper: 1.2.1
ctranslate2: 4.8.4
claude: 2.1.281 (Claude Code)

## Caption

Can one line of code draw an entire maze?

This is MarkovJunior, by Maxim Gumin, the creator of Wave Function Collapse. The program is a list of rewrite rules: find a matching pattern, replace it, and repeat.

WBB → WAW

At the step shown, that rule fits in 38 places. The interpreter picks one at random. After 284 replacements, no matches remain: the maze is finished.

Two ordered rules can dig forward and backtrack when the tip gets stuck. The same maze program runs in 3D without changing a letter. And a larger set of rules builds the house shown in 764 steps.

The name comes from Andrei Markov Jr., son of the mathematician behind Markov chains. His 1951 string-rewriting algorithms can compute any function a Turing machine can compute. The modern grid examples shown here use random match selection.

Every maze, match count and construction step shown comes from the author's interpreter, not an invented animation.

Code: github.com/mxgmn/MarkovJunior (MIT; recorded run at commit 42aaf24).
Examples: MazeGrowth, MazeBacktracker and ModernHouse.

#math #computerscience #algorithms #proceduralgeneration #coding

## Transcript

[   0.0] This one line of code draws an entire maze.
[   3.4] It is Markov Jr. by Maxine Goumin,
[   6.2] the creator of Wave Function Collapse,
[   9.0] a language where the entire program
[  10.9] is a list of replacements.
[  12.9] It is named after Andrei Markov Jr.,
[  15.5] son of the Markov of Markov Chains.
[  18.5] In 1951, he defined an algorithm like this.
[  22.3] Find the first piece that matches a rule,
[  24.7] replace it and repeat.
[  26.9] With three rules, six written in binary
[  29.4] becomes six marks, and a student of his
[  32.3] proved that this can compute anything
[  34.4] a computer can compute.
[  36.8] Goumin brought this to a grid,
[  39.0] but here a rule fits in several places
[  41.6] at the same time, so he picks one at random.
[  44.7] At this step, the rule fits in 38 places.
[  48.1] Pick one, replace it, search again.
[  51.0] After 284 replacements, it fits nowhere, done.
[  56.0] With two rules, their order becomes logic.
[  59.2] The first digs forward.
[  61.0] When the tip gets stuck, that rule does not fit,
[  63.8] and the second goes back along the path
[  66.0] until it finds a way out.
[  68.1] And the same program, without changing a single letter,
[  71.2] runs in three dimensions.
[  73.7] Put together 500 lines of rules and a house emerges.
[  77.6] Nobody drew this house.
[  79.2] It took 764 steps, and it all starts with one line.

## On-screen text

<one value="BWA" in="WBB" out="WAW" origin="True"/> W B B → W A W This one line of code

## Key claims

- MarkovJunior is by Maxim Gumin, the creator of Wave Function Collapse
- The entire program is a list of rewrite rules (replacements): find a matching pattern, replace it, repeat
- The name comes from Andrei Markov Jr., son of the mathematician behind Markov chains
- In 1951, Markov Jr. defined a string-rewriting algorithm; with three rules, six in binary becomes six marks
- A student of Markov Jr. proved this rewriting system can compute anything a Turing machine/computer can compute
- The rule WBB → WAW fits in 38 places at the step shown; the interpreter picks one at random
- After 284 replacements, no matches remain and the maze is finished
- Two ordered rules can dig forward and backtrack when the tip gets stuck
- The same maze program runs in 3D without changing a letter
- A larger set of rules (500 lines) builds a house shown in 764 steps
- Every maze, match count, and construction step shown comes from the author's interpreter, not an invented animation
- Recorded run at commit 42aaf24; examples used: MazeGrowth, MazeBacktracker, ModernHouse

## Info channel

spoken

## Mentioned (unverified hints)

- MarkovJunior: github.com/mxgmn/MarkovJunior
- Wave Function Collapse: (no url)
