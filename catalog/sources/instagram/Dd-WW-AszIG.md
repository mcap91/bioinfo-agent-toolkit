reel: https://www.instagram.com/reel/Dd-WW-AszIG/
captured: 2026-10-27
yt-dlp: 2026.10.26
ffmpeg: 7.0.2-static
faster-whisper: 1.2.1
ctranslate2: 4.8.4
claude: 2.1.281 (Claude Code)

## Caption

Terrain Erosion — how does a landscape get its rivers?

Start with a height map built from layers of noise. Daniel Andrino compares three ways to shape more natural terrain: simulate rain and sediment, learn from real elevation maps, or grow rivers upstream from the coast and build heights around their drainage.

We ran the simulation and river-network code for this video. Blue water and graph lines help show the process. The machine-learning section uses the author's published examples.

For a game island or a small 3D landscape, where would you begin?

Terrain Erosion — 노이즈로 만든 지형에 물길이 생기는 방법.

노이즈를 겹쳐 땅의 높낮이를 만들면, 산처럼 보이는 형태를 얻을 수 있어요. 여기에 물이 흐른 흔적은 어떻게 만들까요?

Daniel Andrino는 세 가지 방법을 비교합니다. 비와 퇴적물의 움직임을 시뮬레이션하기, 실제 고도 지도에서 지형의 형태를 학습하기, 해안에서 강을 거슬러 연결하고 그 물길에 맞춰 높낮이를 만들기예요.

이번 영상에서는 시뮬레이션과 강 네트워크 코드를 직접 실행했습니다. 파란 물과 그래프 선은 과정을 보여주기 위해 덧붙인 표시예요. 머신러닝 부분은 저자가 공개한 결과를 소개합니다.

게임 속 섬이나 작은 입체 지형을 만든다면, 어떤 방법부터 시작하고 싶으신가요?

📎 Source / 원본: terrain-erosion-3-ways
https://github.com/dandrino/terrain-erosion-3-ways/tree/58cdebf74bf9b0b08de61187fbd0ecebd4bb2386
Original creator / 원작: Daniel Andrino
✳︎ Code license / 코드 라이선스: MIT
https://github.com/dandrino/terrain-erosion-3-ways/blob/58cdebf74bf9b0b08de61187fbd0ecebd4bb2386/LICENSE.txt
ML examples / 머신러닝 예시: Daniel Andrino
Elevation maps / 고도 지도: USGS, credited in the original project
Curated by @hyun2xyz

## Transcript

[   0.0] Today's open source project is three ways of generating terrain with erosion.
[   5.0] It starts where most terrain generators stop at noise. It's by Daniel Andrino,
[   9.8] and it's both a write-up and the code behind it. Stack noise at many scales and you get FBM.
[  15.9] Mountains and valleys. Warp it or fold it into ridges and it looks a bit more natural.
[  21.4] But compared with real elevation maps, it looks nothing like real terrain. Real terrain is
[  26.6] shaped by water. Way one. Simulated. Rain falls, water picks up soil where it runs fast, drops it
[  33.3] where it slows down and slowly evaporates. Run that 700 times and the smooth noise gets carved into
[  39.8] gullies and flat valleys. The catch, in his words, parameter hell. Way two. Machine learning.
[  47.2] A neural network trained on real US elevation data. The results look real, but training
[  53.0] took about eight days. Way three works backwards. Start with an island, scatter points,
[  58.6] and connect them into triangles. Then grow rivers upstream from the coast, one edge at a time.
[  63.9] Rivers can merge on the way down, but never split. Add up the water flowing through each branch
[  68.6] and let bigger rivers cut deeper. The terrain is built to fit the rivers.
[  73.7] For visual work, use these height maps for landscapes, 3D terrain,
[  77.8] relief prints, or animated erosion. The code is MIT licensed. Thank you. Bye.

## On-screen text

TERRAIN EROSION / Today's open-source project is Three Ways of Generating Terrain with Erosion. / 오늘 소개할 오픈소스는 '침식 지형을 만든 세 가지 방법'입니다. / dandrino / terrain-erosion-3-ways / Code Issues Pull requests Actions Projects / dandrino Merge pull request #22 from dandrino/dependabot/pip/pil... / images Simulation tweaking 8 years ago / .gitignore Simulation tweaking 8 years ago / LICENSE.txt Initial commit 8 years ago / README.md v/CPU@compute 8 years ago / It's by Daniel Andrino, / Daniel Andrino가 만든 / plain_old_fbm.py / Stack noise at many scales, and you get fBm: / 여러 크기의 노이즈를 쌓으면 fBm이 되고 / land mask / river network with volume / iteration 345 / 716 / compute_river_network 37,713 / 61,249 edges / offset x 0.0 / iteration 199 / 716 / iteration 461 / 716 / Way three works backwards. / 셋째는 거꾸로 가요. / Files Sdcdebf terrain-erosion-3-ways README.md / Preview Code Blame Raw / ...starting from the mouth i.e. where they terminate in the ocean and growing each river upstream one edge at a time... until no more valid edges are left. A valid edge is one that: / Moves uphill. Since we are growing the river graphs upstream, the end effect is only downhill-flowing rivers. / Does not reconnect with an existing river graph. This results in rivers that only merge as they flow downhill, but never split. / Furthermore, we also prioritize which edge to add by how much it aligns with the previous edge in the graph. Without this, rivers will twist and turn in ways that don't appear natural. Furthermore, amount of "directional inertia" can be configured to get more twisty or straight rivers. / For visual work, / 비주얼 작업에서는 / dandrino/terrain-erosion-3-ways LICENSE.txt / MIT License / Permissions: Commercial use, Modification, Distribution, Private use / Limitations: Liability, Warranty / Conditions: License and copyright notice / The code is MIT licensed. / 코드는 MIT 라이선스예요. / @index.opensource / @hyun2xyz

## Key claims

- The project generates terrain with erosion, going beyond simple noise-based terrain.
- It is created by Daniel Andrino and includes both a write-up and code.
- Stacking noise at many scales produces fBm (fractal Brownian motion), resembling mountains and valleys.
- Warping or folding noise into ridges makes it look more natural, but it still looks nothing like real terrain compared to real elevation maps.
- Real terrain is shaped by water.
- Way one (simulation): rain falls, water picks up soil where it runs fast, drops it where it slows, and evaporates; running this 700 times carves smooth noise into gullies and flat valleys.
- The simulation approach suffers from 'parameter hell' in the author's words.
- Way two (machine learning): a neural network trained on real US elevation data produces realistic-looking results, but training took about eight days.
- Way three (river network growth) works backwards: start with an island, scatter points into triangles, then grow rivers upstream from the coast one edge at a time.
- Rivers can merge going downhill but never split.
- Water volume accumulates through branches, and bigger rivers cut deeper; terrain height is built to fit the river network.
- The resulting height maps can be used for landscapes, 3D terrain, relief prints, or animated erosion visuals.
- The code is MIT licensed.
- The video creators ran the simulation and river-network code themselves; the ML section uses the author's published examples.
- Elevation maps are sourced from USGS, credited in the original project.

## Info channel

spoken

## Mentioned (unverified hints)

- terrain-erosion-3-ways: https://github.com/dandrino/terrain-erosion-3-ways/tree/58cdebf74bf9b0b08de61187fbd0ecebd4bb2386
