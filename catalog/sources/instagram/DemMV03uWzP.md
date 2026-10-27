reel: https://www.instagram.com/reel/DemMV03uWzP/
captured: 2026-10-27
yt-dlp: 2026.10.26
ffmpeg: 7.0.2-static
faster-whisper: 1.2.1
ctranslate2: 4.8.4
claude: 2.1.281 (Claude Code)

## Caption

What happens when you mix a growing coral with terrain erosion?

dlaf lets wandering particles stick together into branches. We turn its 2D branches into a ridge height map and feed it to Terrain Erosion. After 716 rounds of simulated rain, valleys cut through the landscape.

Then we take a 3D coral of 6,000 particles, turn its parent links into rounded shapes, and use sdf to create an STL mesh. ln slices that mesh at 131 heights and removes hidden lines to draw it on screen.

These are digital outputs: a simulated landscape, an STL file and a line drawing.

자라나는 산호에 지형 침식을 섞으면 어떻게 될까요?

dlaf는 무작위로 움직이는 입자들을 붙여 가지를 키워요. 2D 가지를 산등성이 높이 지도로 바꿔 Terrain Erosion에 넣었어요. 비를 716번 시뮬레이션하자 지형에 골짜기가 파여요.

이어서 입자 6천 개로 자란 3D 산호의 부모 연결을 둥근 형태로 바꾸고, sdf로 STL 메시를 만들어요. ln은 그 메시를 높이 131곳에서 자른 뒤 가려진 선을 없애 화면에 그려요.

시뮬레이션 지형, STL 파일, 선 그림까지 모두 디지털 결과물이에요.

Credits / 출처
Terrain Erosion: Daniel Andrino · MIT
https://github.com/dandrino/terrain-erosion-3-ways
dlaf · sdf · ln: Michael Fogleman · MIT
https://github.com/fogleman/dlaf
https://github.com/fogleman/sdf
https://github.com/fogleman/ln
Rendering: three.js · MIT
Input conversion, connecting code and visuals: our production
입력 변환·연결 코드·화면 구성: 자체 제작
Curated by @hyun2xyz

#OpenSource #CreativeCoding #GenerativeArt

## Transcript

[   0.0] Remember D-Laf, the open source project where random walkers stick together into coral?
[   6.0] Each walker wanders until it touches the cluster and sticks there, so branches grow on branches.
[  13.0] So what happens if we mix in terrain erosion?
[  16.0] It simulates rain. Water gathers, runs downhill and carries soil away.
[  21.0] Seen from above, D-Laf's branches in 2D look like a mountain range.
[  25.0] So we raise every branch into a ridge higher where the branch runs longer
[  30.0] and hand it to the simulation in place of its usual noise.
[  34.0] 700 rounds of rain later, the coral is a mountain range, carved with valleys.
[  39.0] And can that coral leave the screen?
[  42.0] D-Laf grows 6,000 particles in 3D.
[  45.0] Each one remembers the particle it's stuck to, its parent.
[  48.0] That's our bridge to SDF, which builds shapes from distance.
[  53.0] Every particle in its parent become a capsule, thicker where more branches grow from it.
[  58.0] We blend the capsules with SDF's smooth union formula.
[  62.0] An SDF cuts a flat bottom, adds a base and writes a closed mesh, about 8 cm wide, as an STL.
[  69.0] The file 3D printers read.
[  71.0] Can a pen plotter draw it too?
[  73.0] LN draws 3D scenes as lines.
[  76.0] It slices the mesh at 131 heights.
[  79.0] Then from each point it sends a ray toward the camera.
[  82.0] If something is in the way, that bit is hidden.
[  85.0] Three quarters of the lines disappear.
[  87.0] And what's left reads as solid coral.
[  90.0] Change the seed for a new coral?
[  92.0] Or use fewer slices for a lighter drawing?
[  95.0] Four tools, three bridges.
[  97.0] A height map, parent links and a mesh.
[  99.0] Ask what the next tool reads and build that bridge.
[ 102.0] D-Laf, SDF and LN are all by Michael Fogelman and Terrain Erosion is by Daniel Andrino.
[ 109.0] All four are MIT licensed.
[ 111.0] Keep their licenses when you remix.
[ 113.0] Thank you. Bye.

## On-screen text

dlaf · 3D | 1,449 particles | MIX OPEN SOURCE | Remember dlaf, the open-source project where random walkers stick together into coral? | 무작위로 걷는 입자들이 달라붙어 산호가 되는 오픈소스, dlaf 기억나세요? | terrain-erosion · the coral after 716 rounds of rain | So what happens if we mix in Terrain Erosion? | 그럼 여기에 Terrain Erosion을 섞으면 어떻게 될까요? | terrain-erosion · rain, round by round | Seven hundred rounds of rain later, | 비가 700번 내리고 나면 | off the screen: three open-source tools | And can that coral leave the screen? | 그럼 그 산호가 화면 밖으로 나올 수 있을까요? | dlaf · 3D | 0 particles | dlaf grows six thousand particles in 3D. | dlaf가 3D로 입자 6천 개를 키워요. | dlaf · parent links | That's our bridge to sdf, which builds shapes from distance. | 이게 sdf로 가는 다리예요. sdf는 거리로 모양을 만들어요. | later: this coral as a mountain range | dandrino / terrain-erosion-3-ways | Code Issues Pull requests Actions Projects | Go to file Code | Silkodef Merge pull request #22 from dandrino/dependency/pip/... 6 years ago | images Simulation tweaking 6 years ago | .gitignore Simulation tweaking 6 years ago | LICENSE.txt Initial commit 6 years ago | README.md 6 years ago | valleys the rain carved | the drawing · ln, pen-plotter lines | README License | And here is a 3D example with 10 million particles. This image was ray traced in about 10 hours at 4096x4096px with 2048 samples per pixel. Full resolution here. | README License | sdftext.py: Generate 2D SDFs for text (which can then be extruded) | sdfutil.py: Arithmetic constants and functions. | SDF Implementation | It is reasonable to write your own SDFs beyond those provided by the built-in library. Browse the SDF implementations to understand how they are implemented. Here are some basic examples: | def sphere(radius=1, center=ORIGIN): def f(p): return np.linalg.norm(p - center, axis=1) - radius | An SDF is simply a function that takes a numpy array of points with shape (N, 3) for 3D SDFs or shape (N, 2) for 2D SDFs and returns the signed distance for each | sdf · flat cut + base | 966,012 triangles · 80 × 82 × 55 mm | as an STL, the file 3D printers read. | 3D 프린터가 읽는 STL 파일로요. | the sdf mesh | Can a pen plotter draw it too? | 펜 플로터로도 그릴 수 있을까요? | ln · a ray from each point to the camera | Then, from each point, it sends a ray toward the camera: | 그리고 점마다 카메라 쪽으로 광선을 쏴서 | ln · every slice line | 554,006 px of line | Three quarters of the lines disappear, | 선의 4분의 3이 사라지고 | dlaf seed 21 → sdf | Change the seed for a new coral, | 시드를 바꾸면 새 산호가, | 139,619 px of line | 50,288 px of line | 131 slices | 51 slices | or use fewer slices for a lighter drawing. | 슬라이스를 줄이면 더 가벼운 그림이 나와요. | n6000.stl · 966,012 triangles | Files 12e0c6e README.md | Preview Code Blame | I created this so I could plot 3D drawings with my Makeblock XY Plotter. Here's one of my drawings from the plotter... | Files 12e0c6e README.md | Preview Code Blame | All of the Paths are chopped up to some granularity and each point is tested by shooting a ray toward the camera. If there is no intersection, that point is visible. If there is an intersection, it is hidden and will not be rendered. | The visible points are then transformed into 2D space using transformation matrices. The result can then be rendered as PNG or SVG. | The Contains method is only needed for CSG (Constructive Solid Geometry) operations. | Hello World: A Single Cube | The Code | package main | the mesh, from ln's camera | → ln · seed 21 | → ln · seed 21 | dlaf · 3D | 6,000 particles | Four tools, three bridges: | 도구 넷, 다리 셋. | Thank you. | 감사합니다. | @index.opensource | @hyun2xyz

## Key claims

- dlaf grows coral-like branching structures by letting randomly walking particles stick together when they touch the existing cluster
- The 2D dlaf branch structure is converted into a ridge height map and fed into Terrain Erosion in place of its usual noise input
- Terrain Erosion simulates rain: water gathers, runs downhill, and carries soil away, cutting valleys
- The simulation ran for 716 rounds of rain (caption/on-screen) / about seven hundred rounds (transcript)
- A separate dlaf run grows 6,000 particles in 3D
- Each particle's parent link is used as a bridge to sdf, turning the structure into capsule shapes blended with a smooth union
- sdf cuts a flat bottom, adds a base, and writes a closed STL mesh about 8 cm wide
- The resulting STL mesh has 966,012 triangles and dimensions 80 × 82 × 55 mm
- The STL is a file format that 3D printers can read
- ln slices the 3D mesh at 131 heights and removes hidden lines via ray-casting toward the camera to produce a line drawing
- About three quarters of the lines are removed as hidden, leaving a drawing that still reads as solid coral
- Using fewer slices (e.g. 51 instead of 131) produces a lighter drawing with fewer pixels of line (e.g. 50,288 px vs 139,619 px)
- Changing the dlaf random seed produces a different coral shape
- The project combines four open-source tools (dlaf, Terrain Erosion, sdf, ln) via three data bridges (height map, parent links, mesh)
- dlaf, sdf, and ln are by Michael Fogleman; Terrain Erosion is by Daniel Andrino; all are MIT licensed
- Rendering uses three.js (also MIT licensed)
- The outputs produced are a simulated terrain, an STL file, and a line drawing — all digital outputs

## Info channel

on-screen

## Mentioned (unverified hints)

- dlaf: https://github.com/fogleman/dlaf
- Terrain Erosion (terrain-erosion-3-ways): https://github.com/dandrino/terrain-erosion-3-ways
- sdf: https://github.com/fogleman/sdf
- ln: https://github.com/fogleman/ln
- three.js: (no url)
