reel: https://www.instagram.com/reel/DeRdV4OjhM-/
captured: 2026-10-27
yt-dlp: 2026.10.26
ffmpeg: 7.0.2-static
faster-whisper: 1.2.1
ctranslate2: 4.8.4
claude: 2.1.281 (Claude Code)

## Caption

A grid of numbers becomes flickering pixel fire.

doom-fire-algorithm starts with a row of 36s. It reads the value below, subtracts a random 0, 1 or 2 (never below zero), and writes the result toward the left. A 37-entry palette turns those values into animated color. Turn the bottom row off and the fire fades.

A small JavaScript experiment for learning palette animation and building stylized pixel effects. The fire values come from the project's original fire.js; the enlarged grids, palette layout, annotations and timing presentation were made for this video.

숫자 격자가 일렁이는 픽셀 불꽃이 됩니다.

doom-fire-algorithm은 맨 아랫줄을 36으로 채우고 시작해요. 아래 칸의 값에서 무작위로 0·1·2를 빼고, 0보다 작아지지 않게 한 뒤 왼쪽으로 옮겨 적습니다. 37칸 팔레트로 숫자를 색에 연결하면 불꽃이 움직여요. 맨 아랫줄을 0으로 바꾸면 서서히 꺼지고요.

팔레트 애니메이션을 배우거나 픽셀 이펙트를 만들어 볼 수 있는 JavaScript 실험입니다. 불꽃 값은 원본 fire.js가 계산했고, 확대 격자·팔레트 배치·설명 표시·재생 연출은 영상용으로 만들었습니다.

Source: doom-fire-algorithm by Filipe Deschamps · MIT
https://github.com/filipedeschamps/doom-fire-algorithm
Implementation: playground/1st-implementation-with-tables
Inspired by “How DOOM fire was done” by Fabien Sanglard
https://fabiensanglard.net/doom_fire_psx/

#indexopensource #opensource #creativecoding #javascript #pixelart

## Transcript

[   0.0] Ever wondered how Doom drew fire that looks this alive?
[   4.3] Today's open-source project rebuilds that effect,
[   7.4] Doom Fire Algorithm by Philippe Deschamps.
[  11.1] The whole fire is a grid of numbers from 0 to 36.
[  15.0] Each number picks one of 37 colors, from black to white.
[  19.3] The bottom row is always 36, the hottest white.
[  23.3] Every step, each cell takes the number just below it
[  26.1] and subtracts a random 0, 1 or 2.
[  29.7] So the heat cools as it rises, from white to yellow to red to black.
[  35.2] That same random number also shifts the copy up to two cells to the left,
[  39.4] so the flames lean and flicker.
[  42.2] Turn the bottom row off and the fire burns out by itself.
[  45.9] It's MIT licensed, use it, change it, even sell it.
[  49.5] Just keep the copyright and license notice.
[  52.4] Thank you.
[  53.8] Bye.

## On-screen text

the original fire.js, step by step | grid 75 x 96 cells (the page: 50 x 46) - 24 steps per second | the same fire as numbers: 0 = black ... 36 = white | 25 x 17 cells, the page's debug size - closest to 6 steps per second | fireColorsPalette: 37 colours, number = index | fire.js line 5 | Ever wondered how DOOM drew fire that looks this alive? DOOM은 어떻게 이렇게 살아 있는 불꽃을 그렸을까요? | The whole fire is a grid of numbers, from zero to thirty-six. 불꽃 전체는 0부터 36까지의 숫자 격자예요. | Each number picks one of thirty-seven colors, from black to white. 숫자마다 검정부터 흰색까지 37가지 색 중 하나를 골라요. | @index.opensource | @hyun2xyz | Doom Fire Effect | https://github.com/filipedeschamps/doom-fire-algorithm | Min Fire | Max Fire | Toggle Debug Mode | Doom Fire Effect

## Key claims

- The Doom Fire Algorithm project recreates the fire effect from the original DOOM video game
- The fire is represented as a grid of numbers ranging from 0 to 36
- Each number maps to one of 37 colors in a palette, ranging from black to white
- The bottom row of the grid is always set to 36, the hottest/whitest value
- Each step, a cell's value is computed by taking the value of the cell below it and subtracting a random amount of 0, 1, or 2 (never going below zero)
- This causes the fire to cool as it rises, transitioning from white to yellow to red to black
- The same random subtracted value also shifts the result up to two cells to the left, causing the flames to lean and flicker
- If the bottom row is turned off (set to 0), the fire burns out/fades on its own
- The project is MIT licensed, allowing use, modification, and sale, provided the copyright and license notice is kept
- The project was created by Filipe Deschamps
- The enlarged grids, palette layout, annotations, and timing presentation in the video were made specifically for this video, while the fire values themselves come from the original fire.js

## Info channel

spoken

## Mentioned (unverified hints)

- doom-fire-algorithm: https://github.com/filipedeschamps/doom-fire-algorithm
