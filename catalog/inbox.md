# Catalog inbox

Drop URLs (one per line, optional ` — note`) or fenced ```text blocks here, then run the drain (`/catalog-intake`). Blocked items are marked `⚠ needs-link` and stay until resolved.

```text
10 vector databases worth knowing. Swipe for all 10.

1. Pinecone: Fully managed; storage and compute scale apart
2. Qdrant: Filtering built into the vector search
3. Weaviate: Keywords and vectors in one query
4. Milvus: Graduated LF AI & Data project
5. pgvector: Vectors inside the Postgres you run
6. Chroma: One pip install and you're running
7. LanceDB: Runs in-process, like SQLite
8. Vespa: Yahoo's search engine, open since 2017
9. turbopuffer: Data on S3, hot parts cached
10. S3 Vectors: Vector buckets inside S3

Mixpeek turns video, images, audio and docs into features you can search.

Which one are you running?

mxp.co/i/vector-databases

```
https://mixpeek.com/guides/vector-database-cost-comparison?utm_source=instagram&utm_medium=social&utm_campaign=ig-top10-vector-dbs

https://github.com/karpathy/llm-council
https://github.com/storytold

## Gmail pull 2026-10-19 (43 items)

https://github.com/hkuds/rag-anything
https://github.com/cursor/plugins/tree/main/pstack
https://github.com/cursor/plugins/tree/main/cursor-team-kit/skills/thermo-nuclear-code-quality-review
https://github.com/morluto/rea
https://github.com/neo4j
https://github.com/lancedb/lancedb
https://github.com/qdrant/qdrant
https://github.com/weaviate/weaviate
```text
source: https://www.instagram.com/reel/DeKlghCOQiC/
Caption:
TileShire is a low-stakes, high-depth strategy game. Combine tiles on a living landscape to grow a home rich with life.
It is developed in the Unity engine by two people.

Wishlist TileShire on Steam!

#gamedev
#indiedev
#unity3d
#godot
#gamedevlog
#proceduralanimation
#cozygame
#citybuilder

Transcript:
[   0.0] Here's a game dev trick to bring some life into an environment.
[   3.2] I'm making a game where you merge things together to create a town full of life,
[   7.0] and while the town itself looks pretty good,
[   9.0] there's something about that feels a little...
[  11.3] lifeless.
[  12.7] And I didn't want to solve it by adding a bunch of complicated animations to everything,
[  16.2] because every flower, leaf, and little patch of grass needs its own animation,
[  19.6] and that's gonna get out of hand pretty quick.
[  21.7] So I started looking for a way to make all of this feel alive,
[  24.6] without actually having to animate all of it,
[  26.3] and this is where things get a little weird.
[  28.4] We can use something called Perlin Noise,
[  30.8] and you might be wondering,
[  31.8] what is an image of a bunch of random looking noise
[  34.3] that have to do with animating flowers and leaves?
[  36.6] Well, we're not actually using the image to show anything on the screen.
[  40.2] Instead, we can take the brightness of each pixel in that noise
[  43.2] and use it to move the 3D models in our world.
[  45.7] A darker value means less movement,
[  47.8] and a brighter value means more movement.
[  49.9] Then, we continuously pan it across the environment.
[  53.2] Suddenly, all the foliage starts moving,
[  55.5] not in perfect loops,
[  56.9] but with subtle variations that make it feel much more natural.
[  59.9] You can layer multiple noise patterns together
[  62.0] and give them different variations in speed,
[  64.1] so instead of manually animating hundreds of little pieces of foliage,
[  67.4] we can turn one static piece of art
[  69.2] into something that actually feels like a living world.
[  72.2] This was all made for a game I'm making called Dial Shire.
[  74.9] Check it out on Steam.

On-screen text:
So | PEPE SILVIA | How I will spend every waking hour | Animation Todo: Flower | Well Then...

Key claims:
- The reel demonstrates a game dev trick to bring life into an environment using Perlin Noise.
- The game being developed merges things together to create a town full of life.
- The town looked good but felt lifeless without extra animation work.
- Animating every flower, leaf, and patch of grass individually was considered too time-consuming.
- Perlin Noise (an image of random noise) can be used to drive movement instead of being displayed visually.
- Pixel brightness in the noise maps to movement amount: darker = less movement, brighter = more movement.
- Panning the noise pattern continuously across the environment animates the foliage.
- This creates non-looping, naturally varied movement instead of perfect repeating loops.
- Multiple noise layers can be combined with different speeds for more variation.
- This technique turns one static art asset into something that feels like a living world without manually animating hundreds of foliage pieces.
- The game is called TileShire (referred to as 'Dial Shire' in the spoken audio, likely a transcription error).
- TileShire is developed in Unity by two people.
- TileShire is a low-stakes, high-depth strategy/city-builder game about combining tiles to grow a living home.
- TileShire can be wishlisted on Steam.

Mentioned (unverified hints):
- TileShire: (no url)
- Unity: (no url)
- Blender: (no url)
```
```text
source: https://www.instagram.com/reel/DebFucxs5Xp/
Caption:
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

Transcript:
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

On-screen text:
<one value="BWA" in="WBB" out="WAW" origin="True"/> W B B → W A W This one line of code

Key claims:
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

Mentioned (unverified hints):
- MarkovJunior: github.com/mxgmn/MarkovJunior
- Wave Function Collapse: (no url)
```
```text
source: https://www.instagram.com/reel/DeMiEoaP-8i/
Caption:
Two maps become a mountain flyover.

VoxelSpace samples a height map and a color map, projects heights into screen columns, and paints the terrain with vertical lines. Nearer terrain hides lower, more distant parts; the renderer takes wider steps farther away.

The result is a camera view of the terrain, useful for exploring retro flight visuals and height-map rendering. Each map position has one height, and lighting is already painted into the color map.

The original renderer drew these views with our own maps and camera path. We made the explanatory diagrams, separated-column view, and triangle comparison.

지도 두 장으로 산 위를 날아갑니다.

VoxelSpace는 높이 지도와 색 지도를 읽고, 높이를 화면의 세로줄에 투영해 지형을 그려요. 앞쪽 지형에 가려지는 부분은 건너뛰고, 멀리 갈수록 지도에서 읽는 줄의 간격을 넓힙니다.

결과는 카메라 시점에서 본 지형 화면입니다. 레트로 비행 장면이나 높이 지도 렌더링을 살펴보기 좋아요. 지도 한 위치에는 높이가 하나씩 있고 빛과 그림자는 색 지도에 미리 들어 있습니다.

원본 렌더러에 직접 만든 지도와 카메라 경로를 넣었습니다. 설명 그림, 벌린 세로줄 화면, 삼각형 비교 그림은 별도로 만들었어요.

VoxelSpace by Sebastian Macke · MIT (code)
https://github.com/s-macke/VoxelSpace
Terrain maps & explanatory visuals: index.opensource
직접 만든 지도를 사용했습니다. 저장소의 게임 지도는 MIT 대상이 아니며 이 영상에 쓰지 않았습니다.
#opensource #VoxelSpace #creativecoding #computergraphics

Transcript:
[   0.0] Ever wondered how a game in 1992 flew over detailed mountains when most 3D games were flat single coloured polygons?
[  10.0] Today's open source project rebuilds the trick behind Comanche in under 20 lines.
[  16.0] Voxel Space by Sebastian Macker.
[  19.0] The whole world is just two images.
[  22.0] A height map and a colour map with the light and shadows already painted in.
[  27.0] It looks out from the camera one line at a time, and on each line it picks one map point for every column of the screen.
[  35.0] Each point's height is projected onto the screen and drawn as a vertical line in its colour.
[  41.0] Working from front to back, it only draws the part that rises above what's already drawn.
[  47.0] And the farther it looks, the bigger it steps, so distant hills cost less.
[  52.0] No polygons at all, just vertical lines.
[  55.0] The code is MIT licensed.
[  58.0] Use it, change it, even sell it.
[  61.0] Just keep the copyright and license notice.
[  63.0] Thank you. Bye.

On-screen text:
the original VoxelSpace.html | map: osrs (the repository's maps are game data and are not used) | the original VoxelSpace.html | map: osrs (the repository's maps are game data and are not used) | VoxelSpace | Ever wondered how a game in 1992 flew over detailed mountains, 1992년의 게임은 어떻게 섬세한 산 위를 날았을까요? | Today's open-source project rebuilds the trick behind Comanche in under twenty lines: 오늘의 오픈소스는 Comanche의 그 기법을 스무 줄도 안 되게 다시 만들었어요. | the whole world: two 1024 x 1024 images | maps: osrs (the repository's maps are game data, excluded from its license) | The whole world is just two images: 세상 전체가 그림 두 장뿐이에요. | from above: the camera looks out, one line at a time | maps: osrs | every 10th line drawn · fov: distance 800, as on the page · maps: osrs | camera | It looks out from the camera one line at a time, 카메라에서 앞을 내다보며 한 번에 한 줄씩, | one screen column: each point's height, projected and drawn bottom-up | one screen column | camera | distance from the camera | column 400 of 800 · points from the page's 400 lines · maps: osrs | Each point's height is projected onto the screen, and drawn as a vertical line in its color. 점마다 높이를 화면에 투영해 그 점의 색으로 세로선을 그어요. | the page's frame, pulled apart column by column | frame: the original VoxelSpace (800 x 514) · map: oasis, snow and gaps · maps: osrs | No polygons at all. Just vertical lines. 다각형은 하나도 없어요. 세로선뿐이에요. | the same page, another view · map: osrs | the original VoxelSpace.html | colour map without light (osrs) | the original VoxelSpace.html | drawn line by line, near to far (the page's own top) · map: osrs | the original page · map: osrs | github.com/s-macke/VoxelSpace | MIT License | Permissions: Commercial use, Modification, Distribution | Limitations: Liability, Warranty | Conditions: License and copyright notice | The code is MIT licensed: 코드는 MIT 라이선스예요. | Thank you. 감사합니다. | @index.opensource | @hyun2xyz | License | The software part of the repository is under the MIT license. Please read the license file for more information. Please keep in mind, that the Voxel Space technology might be still patented in some countries. The color and height maps are reverse engineered from the game Comanche and are therefore excluded from the license.

Key claims:
- VoxelSpace recreates the terrain-rendering trick used in the 1992 game Comanche in under 20 lines of code.
- The terrain is represented by two 1024x1024 images: a height map and a color map, with lighting already painted into the color map.
- The renderer looks out from the camera one screen line at a time, picking one map point per screen column.
- Each map point's height is projected onto the screen and drawn as a vertical line in its color.
- Rendering works front-to-back, only drawing parts that rise above what's already drawn, so nearer terrain occludes farther terrain.
- The renderer takes larger sampling steps at greater distances, so distant terrain costs less to render.
- No polygons are used at all — the entire scene is composed of vertical lines.
- VoxelSpace's code is MIT licensed, permitting use, modification, and sale, provided the copyright and license notice is kept.
- The game maps included in the original repository are excluded from the MIT license and were not used in this video; custom-made maps and camera path were used instead.
- The creators made the explanatory diagrams, separated-column view, and triangle comparison themselves; the original renderer code is Sebastian Macke's.

Mentioned (unverified hints):
- VoxelSpace: https://github.com/s-macke/VoxelSpace
```
```text
source: https://www.instagram.com/reel/DemMV03uWzP/
Caption:
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

Transcript:
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

On-screen text:
dlaf · 3D | 1,449 particles | MIX OPEN SOURCE | Remember dlaf, the open-source project where random walkers stick together into coral? | 무작위로 걷는 입자들이 달라붙어 산호가 되는 오픈소스, dlaf 기억나세요? | terrain-erosion · the coral after 716 rounds of rain | So what happens if we mix in Terrain Erosion? | 그럼 여기에 Terrain Erosion을 섞으면 어떻게 될까요? | terrain-erosion · rain, round by round | Seven hundred rounds of rain later, | 비가 700번 내리고 나면 | off the screen: three open-source tools | And can that coral leave the screen? | 그럼 그 산호가 화면 밖으로 나올 수 있을까요? | dlaf · 3D | 0 particles | dlaf grows six thousand particles in 3D. | dlaf가 3D로 입자 6천 개를 키워요. | dlaf · parent links | That's our bridge to sdf, which builds shapes from distance. | 이게 sdf로 가는 다리예요. sdf는 거리로 모양을 만들어요. | later: this coral as a mountain range | dandrino / terrain-erosion-3-ways | Code Issues Pull requests Actions Projects | Go to file Code | Silkodef Merge pull request #22 from dandrino/dependency/pip/... 6 years ago | images Simulation tweaking 6 years ago | .gitignore Simulation tweaking 6 years ago | LICENSE.txt Initial commit 6 years ago | README.md 6 years ago | valleys the rain carved | the drawing · ln, pen-plotter lines | README License | And here is a 3D example with 10 million particles. This image was ray traced in about 10 hours at 4096x4096px with 2048 samples per pixel. Full resolution here. | README License | sdftext.py: Generate 2D SDFs for text (which can then be extruded) | sdfutil.py: Arithmetic constants and functions. | SDF Implementation | It is reasonable to write your own SDFs beyond those provided by the built-in library. Browse the SDF implementations to understand how they are implemented. Here are some basic examples: | def sphere(radius=1, center=ORIGIN): def f(p): return np.linalg.norm(p - center, axis=1) - radius | An SDF is simply a function that takes a numpy array of points with shape (N, 3) for 3D SDFs or shape (N, 2) for 2D SDFs and returns the signed distance for each | sdf · flat cut + base | 966,012 triangles · 80 × 82 × 55 mm | as an STL, the file 3D printers read. | 3D 프린터가 읽는 STL 파일로요. | the sdf mesh | Can a pen plotter draw it too? | 펜 플로터로도 그릴 수 있을까요? | ln · a ray from each point to the camera | Then, from each point, it sends a ray toward the camera: | 그리고 점마다 카메라 쪽으로 광선을 쏴서 | ln · every slice line | 554,006 px of line | Three quarters of the lines disappear, | 선의 4분의 3이 사라지고 | dlaf seed 21 → sdf | Change the seed for a new coral, | 시드를 바꾸면 새 산호가, | 139,619 px of line | 50,288 px of line | 131 slices | 51 slices | or use fewer slices for a lighter drawing. | 슬라이스를 줄이면 더 가벼운 그림이 나와요. | n6000.stl · 966,012 triangles | Files 12e0c6e README.md | Preview Code Blame | I created this so I could plot 3D drawings with my Makeblock XY Plotter. Here's one of my drawings from the plotter... | Files 12e0c6e README.md | Preview Code Blame | All of the Paths are chopped up to some granularity and each point is tested by shooting a ray toward the camera. If there is no intersection, that point is visible. If there is an intersection, it is hidden and will not be rendered. | The visible points are then transformed into 2D space using transformation matrices. The result can then be rendered as PNG or SVG. | The Contains method is only needed for CSG (Constructive Solid Geometry) operations. | Hello World: A Single Cube | The Code | package main | the mesh, from ln's camera | → ln · seed 21 | → ln · seed 21 | dlaf · 3D | 6,000 particles | Four tools, three bridges: | 도구 넷, 다리 셋. | Thank you. | 감사합니다. | @index.opensource | @hyun2xyz

Key claims:
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

Mentioned (unverified hints):
- dlaf: https://github.com/fogleman/dlaf
- Terrain Erosion (terrain-erosion-3-ways): https://github.com/dandrino/terrain-erosion-3-ways
- sdf: https://github.com/fogleman/sdf
- ln: https://github.com/fogleman/ln
- three.js: (no url)
```
```text
source: https://www.instagram.com/reel/DejwS6fjDvg/
Caption:
Claude pxl: Pixel Art as Code

An AI agent can now watch it paint a pixel-art sprite, step by step, in your browser. The project is called Claude pxl. It turns a simple text file into actual game assets, like PNGs and animated GIFs, using a tiny coding language. You do not need to install heavy software or learn a complex tool. You just write a few lines of code, and the program builds the image for you. The coolest part is the live viewer. It shows you exactly how the art is being drawn, like a timelapse of a painter at work. You can watch the AI add colors, shapes, and lights in real time.

Open source: crsolver/claude-pxl

Follow for more open source project drops.

#PixelArt #GameAssets #SpriteArt #IndieGameDev

Transcript:
[   0.0] An AI agent can now watch it paint a pixel art sprite step by step in your browser.
[   5.6] The project is called Claude PXL.
[   8.6] It turns a simple text file into actual game assets like PNGs and animated GIFs,
[  14.1] using a tiny coding language.
[  16.2] You do not need to install heavy software or learn a complex tool.
[  20.6] You just write a few lines of code and the program builds the image for you.
[  24.8] The coolest part is the live viewer.
[  27.4] It shows you exactly how the art is being drawn,
[  30.5] like a time lapse of a painter at work.
[  32.8] You can watch the AI add colors, shapes, and lights in real time.

On-screen text:
GitHub - crsolver/claude-pxl - GitHub | github.com/crsolver/claude-pxl | @GithubSignals | View all files | README | MIT license | pxl | Pixel art as code. Write a compact .px.js file, get PNGs, sprite sheets with JSON, animated GIFs, and a live browser viewer that replays the painting step by step as you save. | Built for AI agents (it ships as a ready-made agent skill) and pleasant for people too. No runtime dependencies, no build step: just Node ≥ 22.18. | github.com/crsolver/claude-pxl/blob/main/docs/gallery/rts_magic_night.gif | COMET | BR1T

Key claims:
- Claude pxl lets an AI agent paint a pixel-art sprite step by step, viewable in your browser
- It turns a simple text file (.px.js) into game assets like PNGs, sprite sheets, and animated GIFs
- It uses a tiny coding language to define the art
- No need to install heavy software or learn a complex tool
- A live viewer shows the art being drawn in real time, like a timelapse of a painter
- The project is open source at github.com/crsolver/claude-pxl
- It has no runtime dependencies and no build step, requiring only Node ≥ 22.18
- It is built for AI agents and ships as a ready-made agent skill, while also being usable by people

Mentioned (unverified hints):
- pxl (Claude pxl): github.com/crsolver/claude-pxl
```
```text
source: https://www.instagram.com/reel/Dd-WW-AszIG/
Caption:
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

Transcript:
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

On-screen text:
TERRAIN EROSION / Today's open-source project is Three Ways of Generating Terrain with Erosion. / 오늘 소개할 오픈소스는 '침식 지형을 만든 세 가지 방법'입니다. / dandrino / terrain-erosion-3-ways / Code Issues Pull requests Actions Projects / dandrino Merge pull request #22 from dandrino/dependabot/pip/pil... / images Simulation tweaking 8 years ago / .gitignore Simulation tweaking 8 years ago / LICENSE.txt Initial commit 8 years ago / README.md v/CPU@compute 8 years ago / It's by Daniel Andrino, / Daniel Andrino가 만든 / plain_old_fbm.py / Stack noise at many scales, and you get fBm: / 여러 크기의 노이즈를 쌓으면 fBm이 되고 / land mask / river network with volume / iteration 345 / 716 / compute_river_network 37,713 / 61,249 edges / offset x 0.0 / iteration 199 / 716 / iteration 461 / 716 / Way three works backwards. / 셋째는 거꾸로 가요. / Files Sdcdebf terrain-erosion-3-ways README.md / Preview Code Blame Raw / ...starting from the mouth i.e. where they terminate in the ocean and growing each river upstream one edge at a time... until no more valid edges are left. A valid edge is one that: / Moves uphill. Since we are growing the river graphs upstream, the end effect is only downhill-flowing rivers. / Does not reconnect with an existing river graph. This results in rivers that only merge as they flow downhill, but never split. / Furthermore, we also prioritize which edge to add by how much it aligns with the previous edge in the graph. Without this, rivers will twist and turn in ways that don't appear natural. Furthermore, amount of "directional inertia" can be configured to get more twisty or straight rivers. / For visual work, / 비주얼 작업에서는 / dandrino/terrain-erosion-3-ways LICENSE.txt / MIT License / Permissions: Commercial use, Modification, Distribution, Private use / Limitations: Liability, Warranty / Conditions: License and copyright notice / The code is MIT licensed. / 코드는 MIT 라이선스예요. / @index.opensource / @hyun2xyz

Key claims:
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

Mentioned (unverified hints):
- terrain-erosion-3-ways: https://github.com/dandrino/terrain-erosion-3-ways/tree/58cdebf74bf9b0b08de61187fbd0ecebd4bb2386
```
```text
source: https://www.instagram.com/reel/DegQ9xiIESl/
Caption:
One seed number, a whole dungeon floor.

Brogue CE starts with rock, places a room, then tries new rooms until their doors meet existing walls without overlap. In this example, 35 room-candidate attempts follow the first room; the recorded floor ends with 20 rooms. Extra doors make loops; five rounds of neighbor rules shape the lakes.

A lake is accepted only if the floor stays connected. This floor has lava; the liquid varies with depth. The same seed reproduces the same dungeon within the same dungeon version.

We redrew game-generated map data, revealing the whole map and removing players, monsters and items. Process colors and labels were added for the explanation.

Which part would you explore: rooms, loops, or lakes?

시드 번호 하나로 던전 한 층을 만듭니다.

Brogue CE는 바위에서 방 하나를 파낸 뒤, 겹치지 않으면서 문이 기존 벽에 닿는 자리를 찾아 새 방을 붙여요. 이 예에서는 첫 방 뒤로 방 후보 배치를 35번 시도했고, 기록된 층에는 방 20개가 남습니다. 문을 더 뚫어 돌아가는 길을 만들고, 이웃 규칙을 다섯 번 돌려 호수 모양을 다듬어요.

호수는 바닥이 계속 연결되는 자리에만 놓습니다. 이 층은 용암이지만 액체는 깊이에 따라 달라져요. 같은 던전 버전 안에서는 같은 시드가 같은 던전을 만듭니다.

게임이 만든 지도 데이터를 다시 그렸고, 전체 지도를 드러낸 뒤 플레이어·몬스터·아이템을 뺐어요. 과정의 색과 라벨은 설명을 위해 더했습니다.

방, 고리, 호수 중 어떤 과정을 더 보고 싶으신가요?

Brogue: Community Edition · AGPL-3.0-or-later
Brogue was created by Brian Walker; Community Edition continues its development.
https://github.com/tmewett/BrogueCE
Curated by @hyun2xyz

Transcript:
[   0.0] Ever wonder how a game can build a brand new dungeon every single time you play?
[   5.3] Today's open-source project is Brogue Community Edition, which carries on the roguelike created by
[  11.0] Brian Walker. Give it a seed number and it digs a whole level out of solid rock.
[  16.7] Rooms, doors, caves and lakes of lava. Watch. It starts with a single room. Then it designs
[  23.7] a new room off to the side and slides it across the map until one of its doors meets a wall.
[  29.1] Without overlapping anything, it designs 35 rooms this way. The ones that fit are kept.
[  35.6] Next, wherever two floors are side by side, but more than 20 steps apart on foot, it opens a door.
[  42.0] Now there are loops, not just dead ends. Lakes start as random noise. Five rounds of a simple
[  47.9] rule smooth it out. A cell is filled if enough of its eight neighbors are. A lake is only placed
[  53.8] where every floor can still be reached. Fill it with lava and the level is done. Same seed,
[  59.4] same dungeon every time. Brogue CE is licensed under the AGPL, so you can study it,
[  65.3] change it and share it. As long as your changes stay open too. Thank you. Bye.

On-screen text:
seed 1 - depth 3 | seed 5 - depth 6 | seed 2 - depth 9 | seed 2 - depth 9 | seed 2 | seed 2 | Brogue: Community Edition | Ever wonder how a game can build a brand-new dungeon, every single time you play? | 게임은 어떻게 할 때마다 처음 보는 던전을 새로 지을까요? | Today's open-source project is Brogue: Community Edition, | 오늘의 오픈소스는 Brogue: Community Edition이에요. | Give it a seed number, and it digs a whole level out of solid rock: | 시드 번호 하나를 주면 단단한 바위에서 한 층 전체를 파내요: | Brogue CE is licensed under the AGPL, | Brogue CE는 AGPL 라이선스예요. | up close: every cell is one character | trueweth / BrogueCE | BrogueCE Public | Brogue: Community Edition - a community-led fork of the much-loved minimalist roguelike game | brogue dungeon game roguelike | Readme | BrogueCE / src / brogue / Architect.c | createDungeon(grid) | roomAttempts(grid, 20) | GNU Affero General Public License v3.0 | BrogueCE / LICENSE.txt | Permissions: Commercial use, Modification, Distribution | Limitations: Liability, Warranty | Conditions: License and copyright notice, State changes, Disclose source | @index.opensource | @hyun2xyz

Key claims:
- Brogue Community Edition continues the roguelike created by Brian Walker.
- A seed number is used to generate a whole dungeon level out of solid rock.
- Generation starts with a single room, then new rooms are designed and slid across the map until a door meets a wall without overlapping anything.
- 35 room-candidate attempts are made after the first room; 20 rooms remain in the recorded floor.
- Doors are opened between adjacent floor areas that are more than 20 steps apart on foot, creating loops instead of just dead ends.
- Lakes start as random noise and are smoothed by five rounds of a cellular automaton rule (a cell fills if enough of its eight neighbors are filled).
- A lake is only placed where the floor remains fully connected/reachable.
- This floor is filled with lava; the liquid type varies with depth.
- The same seed produces the same dungeon within the same dungeon version.
- The map was redrawn from game-generated data, revealing the whole map and removing players, monsters, and items; colors/labels were added for explanation.
- Brogue CE is licensed under AGPL-3.0-or-later, allowing study, modification, and sharing as long as changes remain open.

Mentioned (unverified hints):
- Brogue: Community Edition (BrogueCE): https://github.com/tmewett/BrogueCE
```
```text
source: https://www.instagram.com/reel/DeRdV4OjhM-/
Caption:
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

Transcript:
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

On-screen text:
the original fire.js, step by step | grid 75 x 96 cells (the page: 50 x 46) - 24 steps per second | the same fire as numbers: 0 = black ... 36 = white | 25 x 17 cells, the page's debug size - closest to 6 steps per second | fireColorsPalette: 37 colours, number = index | fire.js line 5 | Ever wondered how DOOM drew fire that looks this alive? DOOM은 어떻게 이렇게 살아 있는 불꽃을 그렸을까요? | The whole fire is a grid of numbers, from zero to thirty-six. 불꽃 전체는 0부터 36까지의 숫자 격자예요. | Each number picks one of thirty-seven colors, from black to white. 숫자마다 검정부터 흰색까지 37가지 색 중 하나를 골라요. | @index.opensource | @hyun2xyz | Doom Fire Effect | https://github.com/filipedeschamps/doom-fire-algorithm | Min Fire | Max Fire | Toggle Debug Mode | Doom Fire Effect

Key claims:
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

Mentioned (unverified hints):
- doom-fire-algorithm: https://github.com/filipedeschamps/doom-fire-algorithm
```
```text
source: https://www.instagram.com/reel/DeecMf9nBBn/
Caption:
Demucs separates a song into drums, bass, vocals, and the rest.

We ran its htdemucs model on Josh Woodward’s “Knock.” The video plays each separated track, then compares the estimated accompaniment with the instrumental version the musician released.

Inside, Demucs reads the same sound as a waveform and a spectrogram. Both branches compress the input, exchange information through a transformer, and expand it back into four tracks. Their estimates are added together.

The sounds are actual Demucs outputs. We made the visualizations from the audio and the model’s internal values. Some sound still leaks between tracks.

Which part would you listen to first: the bass line, the drum pattern, or the vocal?

Demucs는 노래 한 곡을 드럼, 베이스, 보컬, 나머지 소리로 나눠 줍니다.

Josh Woodward의 “Knock”을 htdemucs 모델로 분리했어요. 영상에서 각 트랙을 하나씩 듣고, Demucs가 추정한 반주를 작가가 공개한 반주판과 비교합니다.

Demucs는 같은 소리를 파형과 스펙트로그램, 두 방식으로 읽어요. 두 갈래가 입력을 압축하고, 트랜스포머로 정보를 주고받은 뒤 다시 네 트랙으로 펼칩니다. 마지막에는 두 갈래의 추정값을 더해요.

들리는 소리는 실제 Demucs 출력입니다. 소리와 모델 내부 값을 읽어 시각화했어요. 트랙 사이에 다른 소리가 일부 남기도 합니다.

베이스 라인, 드럼 패턴, 보컬 중 어떤 소리부터 따로 들어 보고 싶으신가요?

Transcript:
[   0.0] Ever wondered how an app can pull the voice out of any song?
[   4.0] Today's open source project does exactly that.
[   7.5] Demukes by Alexandra Defosse.
[  10.5] Give it any song, and it hands back four tracks.
[  13.5] Drums, bass, vocals, and everything else.
[  18.0] Listen.
[  19.5] Drums, bass, vocals, and the rest.
[  27.5] A song arrives as one single wave.
[  30.0] Every instrument added together.
[  32.0] Demukes reads it two ways at once.
[  34.0] The raw wave and a spectrogram.
[  36.5] A picture of which pitches sound when.
[  39.5] Each branch squeezes the sound down layer by layer.
[  43.0] In the middle, a transformer lets the two branches compare notes.
[  47.0] Then both grow back out into four tracks, and their two answers are added together.
[  52.0] It learned all this from hundreds of songs whose instruments were recorded separately.
[  56.5] Josh Woodward, who made this song, also released it without vocals.
[  60.5] Here's his version.
[  62.5] And here's Demukes' guess.
[  65.5] Demukes is MIT licensed.
[  67.5] Use it, change it, share it, and keep the notice.
[  71.5] Thank you.
[  72.5] Bye.

On-screen text:
a song | 2883f3d demucs README.md Preview Raw uvx demucs PATH_OF_AUDIO_FILE_1 [PATH_OF_AUDIO_FILE_2 ...] # for Demucs | uvx demucs --mp3 --mp3-bitrate BITRATE PATH_OF_AUDIO_FILE_1 # output fi | # use --mp3-preset to change encoder preset, 2 for best quality, | # If your filename contain spaces don't forget to quote it !!! | uvx demucs "my music/my favorite track.mp3" | # You can select different models with '-n', mdx_q is the quantized mode | # Note that the quantized models require the quantized extra. | uvx "demucs[quantized]" -n mdx_q myfile.mp3 | # If you only want to separate vocals out of an audio, use --two-stems= | uvx demucs --two-stems=vocals myfile.mp3 | If you have a GPU, but you run out of memory, please use --segment to reduce the length of each split. SEGMENT should be changed to a integer describing the length of each segment in seconds. A segment length of at least 10 is recommended (the bigger the number is, the more memory is required, but quality may increase). Note that the Hybrid Transformer models only support a maximum segment length of 7.8 seconds | his instrumental | Josh Woodward released it himself | Wikimedia Commons File:Josh Woodward - 04 - Knock Instrumental Version.ogg Discussion TimedText Download Use this file Edit View history Email a link Information File information Structured data Original file (Ogg Vorbis sound file, length 2 min 54 s, 201 kbps, file size: 4.16 MB) | Ever wondered how an app can pull the voice out of any song? 앱은 어떻게 아무 노래에서나 목소리만 쏙 뽑아낼까요? | Give it any song, and it hands back four tracks: 노래 한 곡을 넣으면 트랙 네 개를 돌려줘요. | Josh Woodward, who made this song, 이 노래를 만든 Josh Woodward는 | Here's his version. 이건 그의 버전이고 | song | one song in Knock.ogg | the song (with voice) | his instrumental | Demucs's guess | song: "Knock" by Josh Woodward - CC BY 4.0

Key claims:
- Demucs separates a song into four tracks: drums, bass, vocals, and everything else
- The reel uses Demucs's htdemucs model on Josh Woodward's song 'Knock'
- Demucs is made/authored by Alexandre Défossez
- Demucs reads the audio two ways at once: as a raw waveform and as a spectrogram
- Each branch compresses the input, the two branches exchange information through a transformer, then both expand back into four tracks, and their estimates are added together
- Demucs was trained on hundreds of songs whose instruments were recorded separately
- Josh Woodward released his own instrumental (vocal-free) version of 'Knock', which is used for comparison against Demucs's estimated instrumental
- Demucs is MIT licensed
- The audio outputs played are actual Demucs outputs; the visualizations were created from the audio and the model's internal values
- Some sound still leaks between the separated tracks

Mentioned (unverified hints):
- Demucs: (no url)
```
```text
source: https://www.instagram.com/reel/DeaAbkiyU-A/
Caption:
Literally all just python scripts and I get bored 🐍🐍🐍. If you want more information DM or comment

Transcript:
[   0.0] Okay, I just made a video about how I use AI a lot and this is one of the reasons I use it for and I should gate keep this
[   6.7] But go ahead and copy me
[   8.1] You can even message me if you want to know how I did it
[  12.1] Obviously, I use AI to help build scripts, but you'll see what I mean. Let's get into it
[  16.1] Okay, this final result is me using obsidian
[  19.8] But let me break this down every single one of these nodes is a reel that I scraped off of my saved
[  26.2] Library and then deleted so that Instagram doesn't have everything that I'm interested. They have it
[  30.6] But I deleted them once I was used once I used it
[  33.1] I used a YT DLP to scrape every single one of my saved reels which ended up only being about 500
[  39.0] Each one of and then I built a separate script that analyzed and transcribed all of the reels
[  44.6] and it singled out important information like
[  47.9] Names and proper nouns what I think is pretty cool about this is
[  52.3] It will organize everything for you
[  54.3] so if you have memes or tutorials or conspiracies or
[  58.5] Useful information like health. I mean like I might my interests might be as complicated as yours
[  63.5] You know, it's we all have a lot of interest and this is a really great way of organizing and these connections are actually
[  70.0] these lines are connections between
[  72.8] Other they're called links between the two pages that you would see and it's not perfect
[  77.7] I actually do have to do a lot of pruning here
[  79.5] But I mean this got me like 80% of the way there and just a small preview of what each one of these nodes looks like
[  85.1] It gives me an executive summary all the tags the original hash of the
[  90.0] Instagram video the vlog key takeaways and
[  93.2] Screenshots so this is my database all from Instagram took control of my data
[  98.1] And now every time I have an accumulation to save videos. I'm just gonna do this and add it to my
[ 104.0] my database
[ 105.8] Which is very vast and only growing. This is the encyclopedia of bravidus till next time y'all peace

On-screen text:
Graph view

Key claims:
- The creator uses AI to help build scripts for this process.
- They used yt-dlp to scrape every one of their saved Instagram reels, which ended up being about 500 videos.
- They deleted the reels from their saved Instagram library after scraping them so Instagram wouldn't retain everything they're interested in (though they acknowledge Instagram still has it).
- They built a separate script that analyzes and transcribes all the reels and singles out important information like names and proper nouns.
- The system organizes reels into categories like memes, tutorials, conspiracies, or health information.
- The final result is visualized in Obsidian, where each node represents a scraped reel and lines represent links/connections between related pages.
- The process isn't perfect and requires a lot of manual pruning, but gets them about 80% of the way there.
- Each node preview includes an executive summary, tags, the original hash of the Instagram video, key takeaways, and screenshots.
- The creator frames this as taking control of their own data from Instagram.
- They plan to keep adding new saved videos to this growing database, which they call 'the encyclopedia of bravidus.'

Mentioned (unverified hints):
- Obsidian: (no url)
- yt-dlp: (no url)
```
```text
source: https://www.instagram.com/reel/DecS5IkjwSA/
Caption:
PaddleOCR reads the dollar amounts in this IRS example, but it mixes up what years they go with. It read all 3 amounts, so just checking the numbers wouldn’t catch the error. This doesn’t mean PaddleOCR is bad, Docling is good. You need to run your specific data on the models and see if the outputs match your use case.

Comment PDF and I’ll send you the course details.

Transcript:
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

On-screen text:
Year Basis Percentage Deduction 1st . . . . . . . . . . . $100,000 2.033% $2,033 2nd . . . . . . . . . . 100,000 2.564 2,564 3rd . . . . . . . . . . 100,000 2.564 2,564 Year ... 2nd ... OCR loses the year labels Comment PDF

Key claims:
- The IRS example table lists $2,033 for the first year and $2,564 for each of the next two years
- PaddleOCR's first run (default table settings, regular resolution) left the first two years blank and combined the second and third years in the last row
- PaddleOCR read all 3 dollar amounts correctly, so just checking the numbers wouldn't catch the year-mismatch error
- A second PaddleOCR run using a higher-resolution PDF export and PaddlePaddle's hosted Hugging Face demo (which uses a separate table-cell detection model) correctly connected amounts to years, but left the percentage and deduction headings blank
- Docling produced a complete table with all columns, headers, and numbers present
- Docling's output still needs cleanup: stripping inconsistent dollar signs/percent signs for consistent numeric formatting, and removing unnecessary leading/trailing dots in columns one and two
- PaddleOCR is described as a great tool with many good use cases, not a bad tool
- The comparison is not meant to declare PaddleOCR bad and Docling good; results depend on testing your specific data against each model for your use case
- The creator offers a 'PDF to production' course covering OCR evaluation through pipeline deployment, available by commenting 'PDF'

Mentioned (unverified hints):
- PaddleOCR: (no url)
- Docling: (no url)
```
```text
source: https://www.instagram.com/reel/Deb3bVkHBLV/
Caption:
Fit a wide picture into a narrower frame by removing low-energy pixel paths.

caire measures edges, finds a seam with one pixel in each row, removes it, then measures again. In this example, 568 seams reduce a program-generated landscape from 1960×896 to 1392×896. This can help adapt an image to a different layout or teach content-aware resizing.

The checked pagoda, house and pavilion regions lost no pixels in this run. That is specific to this image: parts of the trees did lose pixels. The process uses edge energy; it does not understand which objects matter.

caire calculated the seams, energy values and resized pixels. We added the color maps, enlarged pixel diagrams, labels, camera layout and ordinary-resize comparison.

넓은 그림에서 에너지가 낮은 픽셀 경로를 골라 지우면, 더 좁은 틀에 맞출 수 있어요.

caire는 가장자리를 바탕으로 에너지를 재고, 각 줄에서 픽셀 하나씩 지나는 이음선을 찾아 지운 뒤 다시 계산해요. 이번 예제에서는 프로그램이 그린 산수화에서 이음선 568개를 지워 1960×896을 1392×896으로 바꿨어요. 이미지의 가로세로 비율을 바꾸거나 내용 인식 리사이즈 원리를 배울 때 쓸 수 있어요.

이번 실행에서 확인한 탑·집·정자 영역은 지워진 픽셀이 없었어요. 모든 대상이 보존되는 것은 아니고, 나무 일부는 지워졌어요. 물체의 의미를 알아보는 대신 가장자리의 에너지를 계산해요.

이음선·에너지 값·리사이즈된 픽셀은 caire가 계산했어요. 색 지도, 확대 픽셀 도식, 이름표, 화면 배치와 일반 축소 비교는 저희가 덧붙였어요.

caire by Endre Simo · MIT
https://github.com/esimov/caire
Input painting: Shan Shui Infinite by Lingdong Huang · MIT
https://github.com/LingDong-/shan-shui-inf
Layout, color maps and explanatory graphics: @hyun2xyz
Curated by @hyun2xyz

#opensource #caire #seamcarving #creativecoding

Transcript:
[   0.0] Ever had to fit a wide picture into a narrow frame?
[   3.2] Squeezing it makes everything thin.
[   5.6] Today's open-source project cuts out the least noticeable pixels instead.
[  10.0] Care by Andrei Shimo.
[  12.2] First, it finds the edges.
[  14.4] Where the picture changes sharply, the energy is high.
[  17.6] Then it goes down the image row by row.
[  20.2] Each pixel adds the smallest total of the pixels just above it.
[  24.6] The lowest total in the bottom row is where the cheapest path ends.
[  28.8] Walking back up from there traces a seam.
[  31.8] One pixel in every row through the emptiest parts.
[  35.6] Remove it and the picture is one pixel narrower.
[  39.2] Then it measures the energy again and repeats hundreds of times.
[  43.4] The empty lake gets narrower while the pagoda and the houses don't lose a single pixel.
[  49.0] It's MIT-licensed. Use it, change it, even sell it.
[  52.8] Just keep the copyright and license notice.
[  55.2] Thank you. Bye.

On-screen text:
the picture: 1,960 x 896 | seams removed: 447 · width 1,513 px | caire | remove the seam: every row loses one pixel | width 1,960 px | energy measured again on the narrower picture | red: the 568 seams caire removed | esimov/caire | Code Issues Pull requests Actions Projects | caire / LICENSE | MIT License | Permissions: Commercial use, Modification, Distribution, Private use | Limitations: Liability, Warranty | Conditions: License and copyright notice | caire: carved to 1,392 x 896 | README License | Caire is a content aware image resize library based on Seam Carving for Content-Aware Image Resizing paper | How does it work | 504 func (p *Processor) shrink(img *image.NRGBA) (*image.NRGBA, error) { | 505 width, height := img.Bounds().Max.X, img.Bounds().Max.Y | 507 c := NewCarver(width, height) | 508 if _, err := c.ComputeSeams(p, img); err != nil { | 509 return nil, err | 511 seams := c.FindLowestEnergySeams(p) | 512 img = c.RemoveSeam(img, seams, p.Debug) | processor.go - esimov/caire@072a088 | caire's result: pagoda and houses, 0 pixels removed | caire - 1,960 x 896 | Thank you. 감사합니다. | @index.opensource | @hyun2xyz

Key claims:
- caire is a content-aware image resizing library that removes low-energy pixel seams to narrow an image without uniformly squeezing it
- It works by measuring edge energy, finding a seam of one pixel per row with the lowest cumulative energy, removing it, then recomputing energy and repeating
- In this example, 568 seams were removed to resize a 1,960×896 generated landscape down to 1,392×896
- The pagoda, house, and pavilion regions lost no pixels in this run, while parts of the trees did lose pixels
- The process is based purely on edge energy and does not understand which objects are semantically important
- The input image was a program-generated landscape (Shan Shui Infinite by Lingdong Huang)
- caire itself calculated the seams, energy values, and resized pixels; the color maps, enlarged pixel diagrams, labels, layout, and ordinary-resize comparison were added separately by the creators
- caire is MIT licensed, allowing commercial use, modification, distribution, and private use, provided the copyright and license notice are kept

Mentioned (unverified hints):
- caire: https://github.com/esimov/caire
- Shan Shui Infinite: https://github.com/LingDong-/shan-shui-inf
```
```text
source: https://www.instagram.com/reel/DePGBFXtswr/
Caption:
These are my essential AI coding skills I use to keep code quality high and not bloated when AI writes and merges my code for me.

This is video 5 of 7 in my “how to become a 10x ai-native developer” series, and in the first 4 videos I talked about how I use cloud agents be a 24/7 on call engineer for me that fixes bugs for me while I sleep by using verification skills to verify all the code changes actually work as intended and how they merge the code for me without me reviewing the code, and as a result I have a lot of code being merged without my supervision.

I know a lot of you are wondering, how do you keep the code quality high when letting AI write so much code?
I do so by deferring to skills to do that.
I use the cursor team’s thermo nuclear code quality review (excessive, I know) in conjunction with framework specific tools like a react best practices skill and with , one of my personal favorites, the ponytail skill. Highly recommend you check out the ponytail.dev website which is the home for the skill it is so funny and I’ll show a little screenshot right here, but essentially I have these sets of skills to point out common pitfalls of overly verbose and complicated code and I tell all my coding agents to run these skills before making the PR and sometimes I tell them to run these simplification skills multiple times in a row. Due to the non deterministic nature of LLMs, forcing them to run these simplification skills multiple times allow these models to uncover new simplification methods that it didn’t catch the previous try.

#coding #ai #developer

Transcript:
[   0.0] These are the AI coding skills I use to ship 30 PRs a day while keeping the code quality
[   4.3] high and not bloated.
[   5.6] This is video five of seven in my how to become a 10x AI native developer series.
[   9.7] And in the first four videos, we talked a lot about the creating verification skills
[  13.5] that you can create cloud agents that autonomously write, test and verify and merge code
[  18.1] for you.
[  19.1] And the number one question that I've been getting asked is how do you keep the
[  21.4] code quality high when so much code is getting merged.
[  24.1] And the way that I do that is with skills.
[  26.2] So here are some of the AI coding skills that I use to make sure my code is not
[  29.8] bloated, simple and clean and easy to read.
[  32.6] So my first and favorite skill that I want to talk about is called ponytail.
[  35.6] And you can check it out at ponytail.dev.
[  37.4] And the landing page is actually hilarious because it's all about this little
[  40.4] avatar right here.
[  41.6] It's that one senior staff engineer that gets paged when things are really bad
[  44.8] and broken comes in, fixes it with like two lines of code and goes back to sleep.
[  48.4] And the skill is essentially a gigantic D bloating tool that will call out design
[  52.6] paradigms that are bad, simplify things down as much as possible,
[  55.9] refactor into reusable code modules.
[  58.2] It's pretty great and really keeps the code quality pretty high.
[  61.0] So that's the first one that I want to talk about.
[  62.5] But we have two more that I want to call out.
[  64.2] So next up is within P stack.
[  66.1] I've talked a lot about P stack in the first four videos of the series,
[  68.8] but essentially P stack is a plugin, not just an individual skill that a
[  72.6] SpaceX engineer created who goes by potato on X.
[  76.4] And it's a giant engineering system on creating a software factory and
[  79.9] shipping code at a really high quality and shipping a lot of it.
[  82.8] And it's what powers probably a 90% of the PRs that I write on a daily basis.
[  86.9] And P stack itself actually has a lot of great D bloating simplification
[  91.0] skills built into it, such as this no comments skill right here,
[  94.4] the type script best practices and unslop.
[  97.2] And basically every single time I use P stack, it automatically calls these
[ 100.5] tools and then I also externally call this ponytail skill.
[ 103.7] And then last but not least, the third skill that it also calls is
[ 106.7] this thermal nuclear code quality review skill, which is another skill created
[ 110.8] by the team at cursor slash SpaceX AI.
[ 113.7] And it pretty much does the same thing as the first two skills that we mentioned
[ 116.8] with ponytail and some of the other sub skills that the P stack offers.
[ 120.3] So essentially with every single PR I write, I condense all of this into
[ 123.6] one single simplified command that will call all the simplification
[ 127.0] commands within ponytail within P stack and within the thermonuclear
[ 131.8] code quality review skill to keep my code changes as minimal as possible
[ 136.2] and keep the quality high in the next video in this series.
[ 139.0] I'm going to be talking about how to write really effective prompts so
[ 142.1] that you can have full confidence to significantly improve the quality
[ 145.2] of work that your agents do so that you no longer have to supervise
[ 148.0] and manage them and instead you can trust that they're actually
[ 150.2] getting the work done by themselves without you involved.

On-screen text:
How To Become a 10x AI-Native Developer Ep. 5 of 7 | These are the AI | Last Turn +285 | apps/yorby-web/lib/billing/parse-sufficient-credit-even ... have some that already ... that we use ... edit deduction ... the Account ... tent Coach, Chat Spy ... Carousel ... ch tracks credit ... is in, like, p ... able for audit logging, as well ... sure that ... ters that are ... app don't get ... educated when the app on a ... taskId: string, ... 5 unmodified lines ... message: GPMessage ... 5 unmodified lines ... p_task_id: input.taskId, ... p_user_message_id: double_IhB_listing_body ... magic ... async plan(){} ... const chart_active_forecast ... reuses the existing ... calculation, ... ledger. Admin use ... rem cost without ... 30 PRs a day | How To Become a 10x AI-Native Developer Ep. 5 of 7 | while keeping the code | this is video 5 of 7 in my | who goes by a poteto on X | in the next video

Key claims:
- The creator uses AI coding skills to ship 30 PRs a day while keeping code quality high and not bloated
- This is video 5 of 7 in a 'how to become a 10x AI-native developer' series
- Previous videos covered using cloud agents to autonomously write, test, verify, and merge code without human review
- Code quality is maintained despite high-volume autonomous merging by relying on 'skills'
- The 'ponytail' skill (ponytail.dev) is a favorite tool described as a 'gigantic de-bloating tool' that calls out bad design paradigms, simplifies code, and refactors into reusable modules
- P-stack is a plugin/engineering system created by an engineer who goes by 'poteto' on X, said to be a SpaceX engineer, and powers ~90% of the creator's PRs
- P-stack includes built-in de-bloating/simplification skills: a 'no comments' skill, TypeScript best practices, and 'unslop'
- The 'thermonuclear code quality review' skill, created by the Cursor/SpaceX AI team, performs similar de-bloating/simplification functions
- The creator combines ponytail, P-stack's built-in skills, and the thermonuclear code quality review into one condensed command run before every PR
- Simplification skills are sometimes run multiple times in a row because LLM non-determinism lets repeated runs catch additional simplifications missed on prior passes
- The next video (6 of 7) will cover writing effective prompts to improve agent work quality without needing supervision

Mentioned (unverified hints):
- ponytail: ponytail.dev
- P-stack: (no url)
- thermonuclear code quality review: (no url)
- no comments skill: (no url)
- TypeScript best practices: (no url)
- unslop: (no url)
- react best practices skill: (no url)
```
```text
source: https://www.instagram.com/reel/DeZgZk7AhlR/
Caption:
Reading complex layouts or columns straight across can split two different paragraphs into one sentence. PP-DocLayoutV3 takes a page image, finds blocks such as paragraphs and tables, and puts them in reading order. The Paddle team trained V3 to find the blocks and put them in order in one model.

Comment PDF and I’ll send you the course details.

Transcript:
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

On-screen text:
New model for reading order
Comment PDF

Key claims:
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

Mentioned (unverified hints):
- PP-DocLayoutV3: (no url)
```
```text
source: https://www.instagram.com/reel/DeNJmVuDpx_/
Caption:
Your AI coding agent greps your repo every session to rediscover it. Atomic Claude indexes it once into a local code graph, so Claude Code asks the graph instead.

- callers, callees, impact as file:line from the parse
- 31 languages, one binary, nothing uploaded
- SQL lineage across stored procedures, dbt and Snowflake
- an implement and review loop that checks blast radius before every edit

Free and local: github.com/damusix/atomic-claude

#claudecode #claude #ai #llm #aitools #aicoding #aiagents #artificialintelligence #codegraph #developertools #devtools #softwareengineering #softwaredeveloper #programming #coding #developer #tech #opensource #sql #dbt

Transcript:
[   0.0] Open a new Claude code session and ask it to change one function.
[   4.6] Before it writes a line, it goes looking.
[   7.4] It greps for the name.
[   9.0] It opens five files to find who calls it.
[  11.8] It guesses at your build command.
[  14.7] Then you correct the guess you corrected yesterday.
[  17.6] That search is a tax.
[  19.8] Every session pays it, in tokens and in wrong turns, because the session starts
[  24.2] with no memory of how your code fits together.
[  27.1] The next session pays it again.
[  29.0] Atomic Claude pays it once.
[  31.8] Run atomic code index in your repo.
[  34.6] It parses every file with tree sitter, compiled to WebAssembly, so
[  38.6] it ships as one static binary with no system dependencies.
[  42.6] The result is a symbol graph in a SQLite file inside your repo.
[  46.7] Every function, type, and import, and every call between them, 31 languages.
[  52.6] Nothing is uploaded.
[  53.8] There is no server and no account.
[  56.1] Running it again only reparses what changed.
[  59.5] Now Claude can ask the graph instead of searching.
[  62.6] Who calls this function?
[  64.2] What does it call?
[  65.6] If I change it, what breaks?
[  68.0] Those are three commands, callers, callees, and impact.
[  72.3] Each one answers with a file and a line from the parse,
[  75.6] not a list of text matches that happen to share a name.
[  79.2] Most code tools stop at the application.
[  82.2] A lot of systems live in the database.
[  84.9] Atomic Claude indexes SQL files as code.
[  88.5] It follows stored procedure lineage down to the column,
[  91.6] temp tables included.
[  93.1] It follows DBT models and snowflake tasks.
[  96.4] And it finds SQL written inside strings in your application
[ 100.2] code across 20 languages and puts it in the same graph.
[ 104.4] All of it is static.
[ 105.9] It never connects to your database.
[ 108.4] On top of the graph sits a workflow.
[ 111.2] Plan, implement, review, ship.
[ 114.6] An implementer writes the test first, then the change.
[ 118.5] A reviewer reads the work in a fresh context
[ 121.3] so it cannot inherit the implementer's reasoning.
[ 124.2] Before it edits a function, the loop
[ 126.2] asks the graph what that edit will break.
[ 129.0] The same graph keeps a project wiki current,
[ 131.6] so each new session starts with the build command,
[ 134.4] the layout, and the domains already loaded.
[ 137.4] The tax gets paid at index time.
[ 140.0] The loop spends its tokens on the change.
[ 143.1] The graph is one part of Atomic Claude.
[ 145.7] Behind it sits a whole layer of context engineering.
[ 149.2] How a session learns your repo, what it remembers,
[ 152.6] how agents check each other's work.
[ 154.8] Most of it you only notice once it is gone.
[ 157.7] Install it, index a repo, then go see what else is in there.
[ 161.8] The link is in the description.

On-screen text:
[curious] Open a new Claude Code

Key claims:
- AI coding agents like Claude Code grep the repo every new session to rediscover its structure, paying a 'search tax' in tokens and wrong turns
- Atomic Claude indexes the repo once into a local code graph via 'atomic code index', so Claude Code queries the graph instead of searching
- Indexing parses every file with tree-sitter compiled to WebAssembly, shipping as one static binary with no system dependencies
- The result is a symbol graph (every function, type, import, and call between them) stored in a SQLite file inside the repo
- Supports 31 languages
- Nothing is uploaded; no server and no account; runs fully local
- Re-running the index only reparses changed files
- Provides callers, callees, and impact commands that answer with file:line from the parse, not text-match search results
- Indexes SQL as code, following stored procedure lineage down to the column (including temp tables), dbt models, and Snowflake tasks
- Finds SQL embedded as strings inside application code across 20 languages and includes it in the same graph
- The SQL/database indexing is entirely static and never connects to the actual database
- Includes a plan/implement/review/ship workflow loop
- An implementer agent writes a test first, then the code change
- A reviewer agent reviews in a fresh context so it can't inherit the implementer's reasoning/bias
- Before editing a function, the loop queries the graph to check what the edit will break (blast radius)
- The graph also powers a project wiki kept current with build command, repo layout, and domains, loaded at the start of each session
- Atomic Claude is free and local

Mentioned (unverified hints):
- Atomic Claude: github.com/damusix/atomic-claude
```
```text
source: https://www.instagram.com/reel/DeXCWyfgHgz/
Caption:
5 vector search methods you should know 👇

Flat, IVF, HNSW, IVF-PQ and ScaNN.

They all help find similar vectors, but they do the search differently: checking every vector, searching selected groups, following connections, or using compression.

The trade-off? Speed, memory, and how many of the closest matches you find.
Save this for your next RAG project.

#study #coding #interview #ai

Transcript:
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

On-screen text:
(none)

Key claims:
- Flat checks every stored vector and looks for exact closest matches, but more documents means more work
- IVF groups similar vectors and searches a few nearby groups, resulting in fewer comparisons but it can miss matches elsewhere
- HNSW follows connections through layers of vectors that shortcut like a map, making search fast but requiring extra memory for connections
- IVF compares full vectors inside groups, while IVF-PQ splits vectors into parts and stores small codes for them, saving memory and making comparison cheaper but less precise
- ScaNN is Google's system that combines grouping and compressed comparisons to make a shortlist, then checks that shortlist more accurately so detailed comparisons happen on fewer candidates
- The trade-offs among these methods are speed, memory usage, and recall (how many of the closest matches you find)

Mentioned (unverified hints):
- Flat: (no url)
- IVF: (no url)
- HNSW: (no url)
- IVF-PQ: (no url)
- ScaNN: (no url)
```
```text
source: https://www.instagram.com/reel/DeRx_ZXFT42/
Caption:
Reducto predicts two things: how much a bigger OCR model improves accuracy and how much time it adds. You can then adjust the routing decision without retraining. Tesseract and Chandra are my example pair, not the models Reducto said it used.

Comment “OCR” and I’ll send you both OCR guides.

Transcript:
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

On-screen text:
When is a bigger model actually better? A practical framework for model routing | When is bigger worth it? | FREE OCR GUIDES Comment OCR | for hard documents.

Key claims:
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

Mentioned (unverified hints):
- Reducto: (no url)
- Tesseract: (no url)
- Chandra: (no url)
- LightParse: (no url)
- Docling: (no url)
- Qwen: (no url)
```
```text
source: https://www.instagram.com/reel/DeUWz-7FAgX/
Caption:
PaddleOCR reads this tax row as over $197,300, but not over $50,525. That doesn't work for a $200K income. Docling gets the upper limit right on this document. Test the documents your application actually uses.

Comment “EVALS” and I’ll send you the free evals guide.

Transcript:
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

On-screen text:
Section A—Use if your filing status is Single. Complete... Taxable income. If line 15 is— (a) Enter the amount from line 15. Multi... At least $100,000 but not over $103,350 $ Over $103,350 but not over $197,300 $ OCR breaks the income range FREE EVALS GUIDE Comment EVALS

Key claims:
- PaddleOCR misreads the upper limit of a tax bracket row in a tax worksheet table
- PaddleOCR transcribes the row as 'over $197,300 but not over $50,525', which is logically inconsistent
- A $200,000 income does not fit into any row due to this OCR error
- An agent using this bad data might tell the user there's no matching range and guess the intended row, risking user trust
- Docling correctly reads the upper limit as $250,000 on the same document
- Different OCR/extraction models (Docling, PaddleOCR, MinerU, etc.) perform differently depending on the document, so you must test on your own documents
- The author offers a free guide on how to evaluate OCR models and turn evaluation into repeatable tests

Mentioned (unverified hints):
- PaddleOCR: (no url)
- Docling: (no url)
- MinerU: (no url)
```
```text
source: https://www.instagram.com/reel/DeON0MOB5oi/
Caption:
This is how I made my agents native browser use so fast and efficient

Transcript:
[   0.0] This repo can turn any website into an API for your agents by reverse engineering the website's
[   4.3] network traffic. You're no longer going to have paid to use the API for apps like LinkedIn,
[   8.3] Reddit, or any other website you can think of. Just give this prompt to your agent and tell
[  12.0] it what API you want to reverse engineer. But before you reverse engineer anything,
[  15.7] make sure that your agent has browser access enabled. This is best used when you have automated
[  20.1] workflows where your agent uses the browser. By turning browser actions into API calls,
[  24.2] you can reduce the time your agent spent on a task by 50% and cut its cost by 50%.
[  29.2] I personally use this to automate my LinkedIn outreach and help me do marketing on Reddit.
[  33.2] You can find the repo in the link in my bio.

On-screen text:
goodnight000 / api-anything | Code Issues Pull requests Actions Projects Security and quality | api-anything Public | Turn any website into your agent can from the site's heals itself when changes. | Go to file <> Code | main | goodnight000 Install by pasting one line into an... (unverified) (last week) | claude-plugin Launch README, recorded sh... last week | bench Goodreads explored jobs on A... last week | docs Install by pasting one line the t... last week | README | MIT license | 9:43 marketing on Reddit | charles.zhengg | Charles Zheng (verified) | 9 posts 1,071 followers 795 following | CMU ECE+Robotics

Key claims:
- The repo (api-anything) can turn any website into an API for agents by reverse engineering the website's network traffic
- Users no longer need to pay for official APIs for sites like LinkedIn, Reddit, or others
- You just give a prompt to your agent telling it what API to reverse engineer
- The agent needs browser access enabled before reverse engineering
- Best used for automated workflows where the agent uses a browser
- Turning browser actions into API calls can reduce task time by 50% and cut cost by 50%
- The creator personally uses it to automate LinkedIn outreach and Reddit marketing
- The repo link is in the creator's bio

Mentioned (unverified hints):
- api-anything: (no url)
```
```text
source: https://www.instagram.com/reel/DePNK6AgMsN/
Caption:
PP-DocLayoutV3 segments curved and angled text into regions and predicts reading order. Then another model reads what's inside. A paragraph box shouldn't need to include part of the title.

Comment “PDF” and I’ll send you the course syllabus.

Bottle photo: Eliazar Parra Cardenas / Wikimedia Commons, CC BY 2.0 (resized). https://commons.wikimedia.org/wiki/File:Herbalessencebottles.jpg
https://creativecommons.org/licenses/by/2.0/

Transcript:
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

On-screen text:
OCR for curved text / OCR when you have / paragraph_title / Place / ...nothing more dangerous than a familiar face... As funeral mourners stand in silence at Immaculate Cemetery, a deafening cry cuts through the air. Lying crumpled at the bottom of an open grave is the bloodied body of a young woman, and Detective Lottie Parker is called in to investigate... Read More... / paragraph_title / PDF TO PRODUCTION Comment PDF / you inside.

Key claims:
- PP-DocLayoutV3 is a new OCR layout model that handles warped, curved, and angled text and layouts.
- It is useful for crooked scans, product photos taken from different angles, security footage, and robotics where camera angle varies.
- PP-DocLayoutV3 classifies and segments regions and predicts reading order, with a separate model reading the text inside the detected boxes.
- Its bounding boxes are not just squares/rectangles — they can be angled and fitted to warped images.
- A comparison approach produces bounding boxes that are much bigger than needed, causing incorrect/extra text (e.g., part of a title) to fall inside a paragraph box.
- This bounding-box imprecision issue commonly occurs with user intake forms and identity verification documents like driver's licenses.
- The creator has an upcoming 'PDF to Production' course covering the full workflow from evaluating OCR to deploying a pipeline.
- Viewers can comment 'PDF' to receive the course syllabus.

Mentioned (unverified hints):
- PP-DocLayoutV3: (no url)
```
```text
source: https://www.instagram.com/reel/DeFTnCdMfC2/
Caption:
Manim — math animation written as Python.

A scene is a Python class: create objects, then call play. Equations transform into each other, a grid bends under z², odd sine waves add up to a square wave, and a torus turns into a sphere. Manim began as Grant Sanderson's own tool for the 3Blue1Brown videos; this is ManimGL from the 3b1b/manim repository, and the Community Edition is a separate fork.

We wrote and rendered these scenes ourselves with the library, apart from the repository's own TexTransformExample. No footage or characters from 3Blue1Brown videos are used.

Which idea would you rather explain with motion than with words?

Manim — Python으로 쓰는 수학 애니메이션.

장면 하나가 Python 클래스 하나예요. 객체를 만들고 play를 부르면 수식이 다른 수식으로 바뀌고, 격자가 z²으로 휘고, 홀수 사인파가 더해져 사각파가 되고, 토러스가 구로 바뀌어요. Manim은 Grant Sanderson이 3Blue1Brown 영상을 만들려고 시작한 도구예요. 영상은 3b1b/manim 저장소의 ManimGL이고, Community Edition은 별도 포크입니다.

저장소 예제 TexTransformExample을 빼고는 모두 저희가 직접 장면을 쓰고 렌더링했어요. 3Blue1Brown 영상의 장면이나 캐릭터는 쓰지 않았습니다.

말보다 움직임으로 설명하고 싶은 개념이 있나요?

📎 Source / 원본: Manim
https://github.com/3b1b/manim/tree/fafa083a4fb274bba9cabde0b6e2f50ba6da0622
Original creator / 원작: Grant Sanderson / 3Blue1Brown LLC
✳︎ Code license / 코드 라이선스: MIT
https://github.com/3b1b/manim/blob/fafa083a4fb274bba9cabde0b6e2f50ba6da0622/LICENSE.md
Community Edition (separate fork / 별도 포크): https://github.com/ManimCommunity/manim
Curated by @hyun2xyz

Transcript:
[   0.0] Today's open-source project is Manim.
[   3.0] Every frame here comes from a few lines of Python.
[   6.0] Equations, graphs and surfaces moving with mathematical precision.
[  10.0] It began as Grant Sanderson's personal project to animate his three blue one brown math videos.
[  16.0] In 2020, a community edition forked off from it.
[  19.0] A scene is a Python class. You create objects and call play.
[  24.0] This is the whole scene.
[  25.0] Write one equation, then transform it into another.
[  28.0] Matching pieces glide into place.
[  30.0] The examples even rearrange letters.
[  32.0] The Morse code becomes here come dots.
[  35.0] Equations and pictures can share the same pieces.
[  37.0] A square, cut into four, spells out a plus b squared.
[  41.0] Link a number to shapes with an updater and everything that depends on it follows.
[  45.0] Apply a function to the whole plane and the grid bends.
[  48.0] This is z squared.
[  50.0] Add odd sine waves one by one and a square wave appears.
[  54.0] It works in 3D too.
[  56.0] The code for his videos is public as well in a separate repository.
[  59.0] For visual work, use it wherever timing has to be exact.
[  62.0] Kinetic equations, data graphics or title sequences rendered straight to video.
[  67.0] Manim is MIT licensed.
[  69.0] Thank you. Bye.

On-screen text:
f(x) = 4/π (sin x + sin3x/3 + ...) MANIM Today's open-source project is Manim. 오늘 소개할 오픈소스는 Manim입니다.

Key claims:
- Manim is a Python library for creating math animations
- A scene is a Python class where you create objects and call play
- Equations can transform into each other with matching pieces gliding into place
- Applying z² to a grid bends it
- Adding odd sine waves one by one produces a square wave
- A torus can be turned into a sphere
- Manim works in 3D as well as 2D
- Manim began as Grant Sanderson's personal tool for 3Blue1Brown videos
- The Community Edition forked from the original repository in 2020
- The code for Grant Sanderson's videos is public in a separate repository
- All scenes were written and rendered by the creators themselves, except the repository's own TexTransformExample
- No footage or characters from 3Blue1Brown videos are used
- Manim is MIT licensed

Mentioned (unverified hints):
- Manim (ManimGL, 3b1b/manim): https://github.com/3b1b/manim/tree/fafa083a4fb274bba9cabde0b6e2f50ba6da0622
- Manim Community Edition: https://github.com/ManimCommunity/manim
```
```text
source: https://www.instagram.com/reel/DeI8uRMhi3G/
Caption:
Ultralytics YOLO — 5,040 guesses. 12 bird detections.

Ultralytics YOLO puts boxes, labels and scores on a frame. This example reports 5,040 prediction cells → 92 boxes above 0.25 confidence → 12 bird detections after NMS (IoU 0.7).

With Ultralytics 8.4.173 and yolo26l.pt, the default uses NMS. nms=False selects the NMS-free head; this frame returned 9 detections. These are one frame's results, not a benchmark or a guaranteed count.

5,040개의 추측에서 새 검출 12개까지.

Ultralytics YOLO는 프레임에 상자와 이름, 점수를 붙여요. 이번 예시에서는 5,040칸 중 신뢰도 0.25를 넘은 상자 92개를 NMS(IoU 0.7)로 정리해 새 검출 12개를 남겼어요.

사용한 8.4.173·yolo26l.pt의 기본 경로는 NMS를 써요. nms=False로 고른 출력부는 NMS 없이 9개를 냈어요. 한 프레임의 제작 기록이며, 성능 평가나 실제 개체 수를 보장하는 수치가 아닙니다. 화면의 클래스는 bird·zebra예요.

Code/models: Ultralytics · AGPL-3.0; Enterprise option. Check the terms for your use / 용도에 맞는 조건을 확인하세요.
https://github.com/ultralytics/ultralytics
https://www.ultralytics.com/license
YOLO paper: Redmon et al., 2015
https://arxiv.org/abs/1506.02640
Explainer graphics: @hyun2xyz

Footage / 원본 영상: Wikimedia Commons
JnpoJuwan · CC0
https://commons.wikimedia.org/wiki/File:Pigeon_feeding,_Jardim_da_Estrela,_2025_01.webm
Bamyers99 · Public domain
https://commons.wikimedia.org/wiki/File:Equus_quagga_(zebra)_suckling_video.ogv
Uusijani · CC0
https://commons.wikimedia.org/wiki/File:Giraffes_at_Artis.ogv
Ranch9613 · CC0
https://commons.wikimedia.org/wiki/File:2026_A_Bus_Dart_at_Parker_Rd_Plano_TX.webm
Seb35 · CC0
https://commons.wikimedia.org/wiki/File:A_grazing_horse_at_the_%C3%89comus%C3%A9e_de_la_Bintinais.webm
Drummyfish · CC0
https://commons.wikimedia.org/wiki/File:Seagull_Feeding_Young_Croatia.webm

Curated by @hyun2xyz

Transcript:
[   0.0] Today's open-source project is Ultralytics YOLO.
[   3.9] Show it any video and it boxes and names every object it knows, frame after frame.
[  10.1] YOLO stands for You Only Look Once. Joseph Redman introduced it in 2015
[  15.8] and we ran the newest version, YOLO 2.6. Each frame is shrunk to 640 pixels wide
[  23.3] and the network looks at it once. It answers on three grids from fine to coarse.
[  29.0] Every cell guesses one box, as distances from its center to the four edges,
[  34.2] plus a score for each of 80 kinds of things. That's over 5,000 guesses.
[  39.6] 92 of them say bird, with more than 25%. Many point at the same pigeon,
[  45.0] so YOLO keeps the best box and deletes boxes that overlap it too much.
[  49.6] 12 birds remain. YOLO 2.6 also has a second head that
[  54.2] learned to name each bird just once, so it can skip that cleanup at a small cost in accuracy.
[  60.2] Do this for every frame and the boxes follow along. The code and models are AGPL 3.0.
[  66.6] If you build them into a product or online service, you share your source too,
[  70.6] unless you get Ultralytics Enterprise License. Thank you. Bye.

On-screen text:
YOLO | Today's open-source project is Ultralytics YOLO: 오늘의 오픈소스는 Ultralytics YOLO에요. | arXiv Computer Science > Computer Vision and Pattern Recognition arXiv:1506.02640 (cs) You Only Look Once: Unified, Real-Time Object Detection Joseph Redmon, Santosh Divvala, Ross Girshick, Ali Farhadi View PDF HTML (experimental) We present YOLO, a new approach to object detection... | YOLO stands for You Only Look Once. YOLO는 You Only Look Once, '한 번만 본다'는 뜻이에요. | README Code of conduct Contributing License Security pip install ultralytics For alternative installation methods, including Conda, Docker, and building from source via Git, please consult the Quickstart Guide. CLI You can use Ultralytics YOLO directly from the Command Line Interface (CLI) with the yolo command: # Predict using a pretrained YOLO model (e.g., YOLO26n) on an image yolo predict model=yolo26n.pt source='https://ultralytics.com/images...' | and we ran the newest version, YOLO26. 저희는 최신 버전, YOLO26을 돌렸어요. | 1920 x 1080 | Each frame is shrunk to 640 pixels wide, 프레임을 가로 640픽셀로 줄이고, | bird 0.84 bird 0.72 bird 0.41 bird 0.81 bird 0.87 bird 0.84 bird 0.27 | ultralytics/ultralytics Code Issues Pull requests Discussions Actions GNU Affero General Public License v3.0 Permissions: Commercial use, Modification, Distribution Limitations: Liability, Warranty Conditions: License and copyright notice, State changes, Disclose source | Do this for every frame, 이걸 프레임마다 하면 | The code and models are AGPL-3.0. 코드와 모델은 AGPL-3.0이에요. | bird 0.86 bird 0.65 bird 0.88 bird 0.91 bird 0.70 | #2334455 | bus 0.94 | ultralytics source # cfg/default.yaml imgsz: 640 # [int | list] train/val use int (square); predict/export may use [h,w] # cfg/models/26/yolo26.yaml - [[16, 19, 22], 1, Detect, [nc]] # Detect(P3, P4, P5) # nn/modules/head.py self.nl = len(ch) # number of detection layers | horse 0.95 | bird 0.86 bird 0.85 | bird 0.86 bird 0.68 bird 0.88 bird 0.91 bird 0.70 | Thank you. 감사합니다. | @index.opensource @hyun2xyz

Key claims:
- Ultralytics YOLO boxes and names every object it recognizes in a video, frame by frame
- YOLO stands for 'You Only Look Once', introduced by Joseph Redmon in 2015
- The demo runs the newest version, YOLO26 (caption specifies Ultralytics 8.4.173 and yolo26l.pt)
- Each frame is resized to 640 pixels wide and processed in a single pass
- The model predicts on three grids (fine to coarse) and each cell predicts one box plus class scores for 80 classes, totaling over 5,000 guesses (5,040 prediction cells)
- 92 of the predicted boxes are labeled 'bird' with confidence above 25%
- Non-Maximum Suppression (NMS, IoU 0.7) removes overlapping duplicate boxes, leaving 12 bird detections
- YOLO26 has an NMS-free head option (nms=False) that names each object once, skipping NMS cleanup at a small accuracy cost; this returned 9 detections on the same frame
- These results are from a single frame, not a benchmark or guaranteed detection count
- The code and models are licensed under AGPL-3.0; using them in a product/online service requires sharing source code unless an Ultralytics Enterprise License is obtained

Mentioned (unverified hints):
- Ultralytics YOLO: https://github.com/ultralytics/ultralytics
- Ultralytics License: https://www.ultralytics.com/license
- YOLO paper (You Only Look Once: Unified, Real-Time Object Detection): https://arxiv.org/abs/1506.02640
```
```text
source: https://www.instagram.com/reel/DeFJd9AHPVS/
Caption:
Taiga-S1: A 5 MB AI That Builds Real Parts in FreeCAD (We Tested It)

Taiga-S1 is a free, 1.2-million-parameter model (a 4.9 MB file) that builds parts in FreeCAD one click at a time, with no chatbot and no GPU.

▶ More AI news, explained: Simply AI on YouTube (link in bio)

AI-narrated.

#AI #AINews

Transcript:
[   0.0] This AI is five megabytes, small enough to email.
[   3.6] And it just built this part by itself in FreeCAD.
[   6.6] 47 clicks in three seconds.
[   9.2] Every one right.
[  10.2] No chatbot, no cloud, no graphics card.
[  13.2] On our Mac, it took about two milliseconds
[  15.3] to pick each click.
[  16.3] It's Tyga S1, a free model from one developer,
[  19.8] Shivshank Mugam, the catch.
[  22.1] You don't type, make me a bracket.
[  24.2] You give it a recipe.
[  25.5] I play this size, a hole here,
[  27.5] repeat it four times around the corners.
[  30.0] It does all the clicking.
[  31.2] Pick a plane, sketch, set the size, extrude.
[  34.3] We wrote three parts of our own
[  35.9] and it built all three exactly.
[  38.4] A plate with 11 holes.
[  40.1] 89 clicks, still right.
[  42.4] Where it breaks?
[  43.4] Ask for 22 holes and it quits nine short.
[  46.0] And the repo's own check still passes it.
[  48.3] Ask it to round the corners first and it loops.
[  50.9] Round, undo, round, undo.
[  53.5] And it only knows plates, holes and patterns.
[  55.9] Not your engine block.
[  57.1] The real lesson.
[  58.2] The clicking doesn't need a giant AI.
[  61.2] A chatbot can write the recipe
[  63.1] and a model this small builds it on your own machine.
[  66.9] Tyga S1 is free on Huggingface.
[  69.5] Follow for every new AI model.
[  71.2] Test it in about a minute.

On-screen text:
4.9 MB the whole model | Taiga-S1 | Taiga-S1 A 1.2M-parameter model that builds CAD parts in FreeCAD. | This AI is | to pick each click | Taiga-S1 | Taiga-S1 A 1.2M-parameter model that builds CAD parts in FreeCAD. | on your own machine

Key claims:
- Taiga-S1 is a 5 MB (4.9 MB) AI model, small enough to email
- It built a part by itself in FreeCAD using 47 clicks in three seconds, every one correct
- It requires no chatbot, no cloud, and no GPU
- On a Mac, it took about two milliseconds to pick each click
- It was made by one developer, Shivshank Mugam (name as transcribed)
- Users give it a recipe/instructions rather than natural-language prompts, and it performs the clicking: pick a plane, sketch, set the size, extrude
- It successfully built three custom test parts exactly as specified
- A plate with 11 holes took 89 clicks and was still correct
- It fails when asked for 22 holes, stopping nine short, yet the repo's own check still passes it
- Asking it to round corners first causes it to loop (round, undo, round, undo)
- It only knows plates, holes, and patterns — not complex objects like an engine block
- It is a 1.2-million-parameter model, free, and available on Hugging Face
- The AI narration in the video is AI-generated

Mentioned (unverified hints):
- Taiga-S1: (no url)
- FreeCAD: (no url)
- Hugging Face: (no url)
```
```text
source: https://www.instagram.com/reel/DeIm-UyIzbz/
Caption:
7 Tools to supercharge your terminal, explained by cats. #cat #code #terminal #bash #programming

Transcript:
[   0.0] Seven tools to supercharge your terminal explained by cats kitty lives in the terminal
[   5.1] But she types CD 11 times just to find her tuna. So she gave her terminal seven upgrades
[  11.7] Zoxide it remembers every folder kitty visits now. She types Z tuna and she's there fzf
[  18.4] Kitty forgot the file name. She types three letters and fzf sniffs it out of 1,200 files rip grip
[  25.6] Where did she write to do feed cat?
[  28.5] Rg searches the whole project before she can blink
[  32.1] TLDR
[  33.4] Handpages are long TLDR gives kitty the few examples. She actually needs a tune
[  39.3] Kitty ran the perfect command last Tuesday a tune remembers it which folder if it worked
[  44.9] How long it took even on her other laptop lazy get no more memorizing get commands
[  51.1] space stages see commits shift P pushes
[  55.2] JQ the API sends back a wall of JSON
[  58.9] JQ fishes out just the tuna same terminal seven new tricks and kiddies pause finally get a break
[  65.6] Save this for your next setup and tell kitty which tool she missed

On-screen text:
7 TOOLS TO SUPERCHARGE YOUR TERMINAL
kitty@laptop: zsh
~ )
kitty@laptop: zsh
~ ) cd code
/code ) ls
cat-pics naps tuna-shop yarn
/code ) cd tuna-shop
/code/tuna-shop )
ripgrep 3/7
github.com/BurntSushi/ripgrep
import feed()
let boat = []
if (cat) return
export default
return purr;
fetchCat()
for (x of naps)
await feed()
wait feed()
TODO: feed cat
ripgrep 3/7
github.com/BurntSushi/ripgrep
kitty@laptop: zsh
~/code/tuna-shop ) rg
kitty@laptop
$ brew install zoxide fzf \
ripgrep tlrc atuin \
lazygit jq

Key claims:
- Kitty used to type 'cd' 11 times just to find her tuna, so she gave her terminal seven upgrades
- zoxide remembers every folder kitty visits, so she can type 'z tuna' and jump straight there
- fzf lets kitty find a file by typing three letters, sniffing it out of 1,200 files
- ripgrep (rg) searches the whole project for text (like a TODO comment) almost instantly
- tldr gives kitty a few practical examples instead of long man pages
- atuin remembers past commands, including which folder they worked in, how long they took, and syncs across other devices/laptops
- lazygit means no more memorizing git commands — 'g' stages, 'c' commits, shift+P pushes
- jq fishes out just the needed data ('tuna') from a wall of JSON returned by an API
- All seven tools can be installed via a single Homebrew command: brew install zoxide fzf ripgrep tlrc atuin lazygit jq

Mentioned (unverified hints):
- zoxide: (no url)
- fzf: (no url)
- ripgrep: github.com/BurntSushi/ripgrep
- tldr: (no url)
- atuin: (no url)
- lazygit: (no url)
- jq: (no url)
```
```text
source: https://www.instagram.com/reel/DeJyswKCtCY/
Caption:
Shift Left Security, Explained!🐛

Shift left is the practice of moving security checks earlier in the software delivery line so issues get caught before code reaches production. SAST (static application security testing) scans code without running it, like CodeQL in a CI pipeline. DAST (dynamic application security testing) attacks the running app from outside, like OWASP ZAP in staging. Pre-commit hooks run a quick scanner like Semgrep on changed files before code enters Git, and editor plugins like SonarQube flag problems as code is written.

The example used is SQL injection, where input like ' OR 1=1 -- ends up inside the query and returns every order in the table. The fix is a parameterized query, so user input is always treated as plain data.

Which of these checks does your pipeline actually run? Comment below.

#ShiftLeft #DevSecOps #SAST #DAST #SQLInjection #DevOps #AppSec #CodeQL #OWASPZAP #Semgrep #SonarQube #PreCommit #CICD #KodeKloud #Shorts

Transcript:
[   0.0] Shift left is a term you hear in almost every DevOps team.
[   3.6] What does it actually mean?
[   5.3] If we see how your code flows in the organization on a line
[   7.6] from left to right, it looks like this.
[  10.2] On the far left, you write the code, then you commit it,
[  13.1] then the CI pipeline builds it, then staging for testing,
[  16.2] then you deploy on production,
[  17.4] where real users access the application.
[  20.0] So shift left simply means we catch important things
[  22.7] earlier on this line.
[  24.2] Now let's take one bug in the code
[  25.6] and follow it along this line from right to left.
[  28.2] Imagine you run an online store
[  29.6] where customers can search their order
[  30.9] by entering an order ID.
[  32.8] The problem is that the application takes
[  34.3] whatever the user types
[  35.5] and puts it directly into the database SQL query.
[  38.3] Normally, a customer types 1042
[  40.8] and the application puts 1042 in the database query
[  43.8] and returns the information to the customer.
[  45.8] But an attacker can type something like quote,
[  48.0] or one equals one dash dash in the search box.
[  52.0] Because the application blindly inserts
[  53.7] this user input into the query,
[  55.4] this input will run inside the query.
[  57.9] The condition one equals one is always true.
[  60.5] So instead of returning one order,
[  62.0] the database may return every order in the table,
[  64.3] which includes other customer's information as well.
[  66.8] This type of attack is called SQL injection
[  69.6] and the core problem is simple.
[  71.3] The user input is treated as part of the SQL command
[  73.9] instead of just data.
[  75.6] Now the team finds this issue in production
[  77.4] as an incident.
[  78.5] The security team checks whose data was exposed,
[  80.7] then a developer writes a hot fix
[  82.0] that is deployed in a hurry.
[  83.3] And depending on what leaked,
[  84.5] you have to inform your customers.
[  86.2] Now let's see how we could have prevented this issue.
[  88.6] We found the bug in production,
[  89.8] but one step to the left is staging.
[  91.9] Ideally in staging, we should have run our application
[  94.4] and attacked our application with OWASP's app,
[  96.6] a free tool that sends attack inputs to our application.
[  99.6] This type of testing where you attack from outside
[ 101.7] is called DAST or Dynamic Application Security Testing.
[ 105.0] If we go left, we have the CI pipeline,
[ 107.2] which builds and tests every change in our app automatically.
[ 110.3] The DevOps team could use a tool like CodeQL
[ 112.2] in the pipeline and CodeQL checks
[ 114.0] if your code is prone to SQL injection attacks.
[ 116.8] And if it is prone, then we fail the build pipeline
[ 118.9] with an error saying a critical vulnerability was found.
[ 121.5] This is called SAST or Static Application Security Testing
[ 124.5] because the application does not run
[ 126.0] and we just check the code.
[ 127.3] One more step left is when the developer
[ 128.8] commits the code to Git.
[ 130.5] So we could run a script on the developer's laptop
[ 132.4] every time the developer runs Git commit.
[ 134.6] And this is called a pre-commit hook.
[ 136.7] The hook runs a quick scanner
[ 137.8] like SEMGREP on the changed files.
[ 139.5] And if the scanner finds the same problem,
[ 141.2] the commit is blocked.
[ 142.5] The leftmost point is the editor like VS Code.
[ 145.2] We could install a plugin like SonarCube for VS Code
[ 147.6] and SonarCube checks your code as you type
[ 149.3] and underlines the line where the issue is.
[ 151.3] The fix to our problem is to send the SQL query
[ 153.6] and the user input to the database separately.
[ 155.8] So the attacker's input is treated as plain data
[ 158.2] and this is called a parameterized query.
[ 160.4] So the idea of shift left is that we scan
[ 162.4] for vulnerabilities and issues at each stage
[ 164.4] starting from the leftmost point
[ 165.9] so that issues can't reach production.
[ 167.8] If this video helped, hit subscribe and follow.

On-screen text:
SHIFT LEFT #DevOps

Key claims:
- Shift left means catching security issues earlier in the code-to-production pipeline (editor -> commit -> CI -> staging -> production).
- SQL injection occurs when user input (e.g. ' OR 1=1 --) is inserted directly into a SQL query instead of being treated as data.
- A successful SQL injection on an order-lookup query can return every row in the table, exposing other customers' data.
- DAST (e.g. OWASP ZAP) tests the running application from outside, typically in staging.
- SAST (e.g. CodeQL) analyzes code without running it, typically in the CI pipeline, and can fail the build if a vulnerability is found.
- Pre-commit hooks (e.g. using Semgrep) scan changed files on the developer's machine and can block a commit if issues are found.
- Editor plugins (e.g. SonarQube for VS Code) flag issues as code is typed, the earliest point in the pipeline.
- The fix for SQL injection is a parameterized query, which sends the query and user input separately so input is always treated as plain data.

Mentioned (unverified hints):
- CodeQL: (no url)
- OWASP ZAP: (no url)
- Semgrep: (no url)
- SonarQube: (no url)
```
```text
source: https://www.instagram.com/reel/DeIV3Tam24w/
Caption:
Cloudflare and OpenAI came for Jev with their own decision models.
What Clef adds that Jev doesn't:
1. reads images
2. 64K context window, double Jev's 32K
3. open weights, so it runs on your own machine
#cloudflare #jev #typesafe #openai #aiengineering

Transcript:
[   0.0] So Cloudflare just dropped a free AM model you can download on a running machine,
[   3.6] and they're coming straight for Jev.
[   5.1] Quick catch up, a company called Typesafe launched Jev.
[   7.6] You hand it something messy plus a question with a set of answers,
[  10.6] it hands you back a pick, a score, a yes-no, and how sure it is.
[  14.2] Hey, if you're new here, I'm Kevin.
[  15.3] I break down what's happening in AI and I actually build with it,
[  17.9] so if that's your thing, hit follow.
[  19.3] So when Jev released, it blew up on Twitter, and now the big players went in.
[  22.5] First of all, OpenAI at Dev Day, they released a Decisions API,
[  26.2] which is the same idea as Jev.
[  28.0] And they tuned a version of GPT-6 Luna as a Jev Decision Model,
[  31.6] and it takes images too.
[  33.0] It's in limited preview with no pricing yet,
[  35.2] but the one I'm really excited about is Cloudflare.
[  37.4] Last week, Cloudflare released their own Decision Model, and they call it Clef.
[  42.2] Two sizes, there's Clef, the big one, for accuracy,
[  44.7] and then Clef flashed the small one for speed,
[  47.1] and three things stand out for this.
[  48.8] One, it runs locally.
[  50.3] Cloudflare put the weights on Huggingface under the Apache license,
[  53.4] which means it's free to use even commercially.
[  55.6] Download it, run it on your own hardware,
[  57.6] and your data never leaves the building.
[  59.2] You'll want a beefy GPU for that, or skip the hardware,
[  62.1] and call it with Cloudflare's workers' AI.
[  64.1] The second thing, and this is massive, it sees images, so it's multimodal.
[  67.3] And if people have been talking in comments,
[  68.9] even when I made my videos about Jev,
[  70.6] people asked if I could see images.
[  71.9] Jev can't, you have to explain images in text Jev,
[  75.0] but Cloudflare or Clef can see images.
[  77.4] Clef takes up to four images per request,
[  79.5] and so now you can ask it,
[  80.7] is this home furniture empty?
[  82.3] Does this receipt match the expense report?
[  84.3] And you get back a straight answer.
[  85.6] And number three, it's double the context window.
[  88.2] So Jev reads about 32,000 tokens per request,
[  90.9] and Clef reads 64,000.
[  92.8] So this works for long email threads or a full contract,
[  95.4] now fit into one API call.
[  97.1] And then there's speed, and Cloudflare's own testing.
[  99.4] Clef Flash answered in around 38 milliseconds,
[ 101.8] whereas Jev came in around 520.
[ 103.8] That's about 10 times faster,
[ 105.1] but to be honest, you really won't feel that.
[ 106.9] To be fair, Jev, it's still the cheaper by tokens,
[ 109.5] it still wins on a lot of benchmarks,
[ 111.2] and I still have it ripping across most of my stack.
[ 113.5] Here's how I pick.
[ 114.4] Are you building on Jev, then keep going.
[ 116.6] Unless you need images, longer context,
[ 118.9] or a model running on your own machine,
[ 120.7] the price point here is so cheap,
[ 122.2] I would stick with Jev for all the stuff
[ 124.0] you have running now.
[ 124.9] Anything new, anything that requires images,
[ 127.3] anything that has a large context window,
[ 129.0] or if you just want to play around with something local,
[ 130.8] especially if you're worried about privacy and security,
[ 133.0] I would then move over to Cloudflare and Clef,
[ 135.0] and start messing with that
[ 135.9] either through the API or locally.

On-screen text:
CLOUDFLARE JUST CAME FOR JEV FREE - OPEN WEIGHTS - RUNS ON YOUR MACHINE 01 LOCAL 02 IMAGES 03 2x CONTEXT AI. THAT.

Key claims:
- Cloudflare released a free AI model called Clef that you can download and run on your own machine
- Jev (by Typesafe) takes messy input plus a question with answer options and returns a pick, score, yes/no, and confidence level
- OpenAI released a Decisions API at Dev Day, tuning a version of GPT-6 Luna as a Jev Decision Model, which also takes images; it's in limited preview with no pricing yet
- Cloudflare's Clef comes in two sizes: Clef (big, for accuracy) and Clef Flash (small, for speed)
- Clef weights are on Hugging Face under Apache license, free for commercial use, can run on your own hardware or via Cloudflare Workers AI
- Clef is multimodal and can see/read images (up to 4 per request), while Jev cannot read images and requires text descriptions
- Clef has a 64,000 token context window, double Jev's 32,000 tokens
- In Cloudflare's own testing, Clef Flash answered in ~38ms vs Jev's ~520ms, about 10x faster, though the difference may not be noticeable in practice
- Jev is still cheaper by tokens and wins on many benchmarks
- Recommendation: stick with Jev for existing stacks unless you need images, longer context, or local/private deployment, in which case switch to Clef

Mentioned (unverified hints):
- Jev (Typesafe): (no url)
- Clef (Cloudflare Decision Model): (no url)
- Clef Flash: (no url)
- OpenAI Decisions API: (no url)
- GPT-6 Luna: (no url)
- Cloudflare Workers AI: (no url)
- Hugging Face: (no url)
```

## kb session drop 2026-10-26

https://www.reddit.com/r/ClaudeCode/comments/1xbxoza/my_claude_code_setup_it_runs_like_a_small/ — practitioner setup post: hooks over prose, GitLab state machine, model-tier routing, Jev typed-judgment tier with measured break-even, typed/dated memory (full text in kb SRC-0028)
https://github.com/JustVugg/colibri — pure-C MoE inference streaming experts from SSD (read-only); Apache-2.0
https://huggingface.co/Contrastive-LM/CLM-v0.1-8B — Stanford + NVIDIA contrastive "System One" scorer on frozen Qwen3-8B; Apache-2.0
https://github.com/yt-dlp/yt-dlp — media/metadata downloader; anonymous Instagram reel capture proven 2026-10-26 (bioinfo WK-0079)
https://github.com/instaloader/instaloader — Instagram posts/metadata downloader
https://github.com/imageio/imageio-ffmpeg — pip-installable ffmpeg binary (used for keyframes/audio decode)
Jev (TypeSafe AI) — typed-judgment model (choice/score/probability only); find the official URL before draining
strata — annotate existing entry: PolyStrata adds four more MoE models (see the needs-link Reddit item "PolyStrata"); entry acquired 2026-09-29, likely stale
⚠ not-cataloguable-(post-body-removed-by-Reddit-filters;-the-5-projects-are-not-recoverable-from-the-thread)
```text
source: https://www.reddit.com/r/SATNA_PROJECT/comments/1x2856v/the_500mo_stack_for_0_5_new_opensource_ai/
Skip to main content
The $500/mo stack for $0: 5 new open-source AI projects that feel too good to be free 🔥 : r/SATNA_PROJECT
Sign Up
Log In
Expand user menu
Go to SATNA_PROJECT
r/SATNA_PROJECT
•
17d ago
DarkLight-874
The $500/mo stack for $0: 5 new open-source AI projects that feel too good to be free 🔥
Sorry, this post was removed by Reddit’s filters.
Share
Roblox
•
Ad
Forget mindless scrolling. Start solving instead. Crack cases, outsmart friends, and flex your brain in Roblox's best puzzle games — free to play.
Play Now
roblox.com
Sort by:
Comments Section
busters1
•
17d ago

I'd like to add this one to the list. We launched just 5 weeks ago. It's a collaboration platform that lets engineering teams keep their technical documentation, observability, RFCs, and other internal knowledge in one place. It aims to make knowledge-keeping easy and tailored for engineers, especially in new startups and teams.

https://github.com/oxynote/oxynote

Reply
Share
More posts you may like
Related posts
A free deep learning textbook + 68 Python notebooks, from neural network basics to transformers and diffusion models
r/SATNA_PROJECT
•
7d ago
A free deep learning textbook + 68 Python notebooks, from neural network basics to transformers and diffusion models
575 upvotes · 4 comments
anthropic-ai
•
Ad
Claude handles the search. Researchers handle the breakthroughs.
claude.com
Learn More
How to build a 100% Free & Local AI Coding Setup on your machine (No subscriptions, zero token caps) 🛠️🔥
r/SATNA_PROJECT
•
4d ago
How to build a 100% Free & Local AI Coding Setup on your machine (No subscriptions, zero token caps) 🛠️🔥
260 upvotes · 9 comments
20 GitHub tools for Claude Code worth bookmarking — start with 3, not all 20
r/SATNA_PROJECT
•
9h ago
20 GitHub tools for Claude Code worth bookmarking — start with 3, not all 20
194 upvotes · 19 comments
The Ultimate 2026 Open-Source AI Stack: How to build, host, and automate AI apps for $0/mo 🚀
r/SATNA_PROJECT
•
6d ago
The Ultimate 2026 Open-Source AI Stack: How to build, host, and automate AI apps for $0/mo 🚀
148 upvotes · 17 comments
A practical digital-footprint cleanup workflow—with AI prompts for organizing the work
r/SATNA_PROJECT
•
7d ago
A practical digital-footprint cleanup workflow—with AI prompts for organizing the work
132 upvotes · 2 comments
6 open-source repos for building a parallel AI coding workflow
r/SATNA_PROJECT
•
6d ago
6 open-source repos for building a parallel AI coding workflow
130 upvotes · 8 comments
Before you build another AI agent, check this GitHub repo — 300+ tools organized by what they actually do
r/SATNA_PROJECT
•
6d ago
Before you build another AI agent, check this GitHub repo — 300+ tools organized by what they actually do
110 upvotes · 1 comment
The AI reverse-engineering toolkit: free tools, agents, courses, and practice labs — organized by what you’re trying to understand
r/SATNA_PROJECT
•
9h ago
The AI reverse-engineering toolkit: free tools, agents, courses, and practice labs — organized by what you’re trying to understand
107 upvotes
Why are motion designers still starting from a blank timeline? This Claude Code setup is wild.
r/SATNA_PROJECT
•
6d ago
Why are motion designers still starting from a blank timeline? This Claude Code setup is wild.
105 upvotes · 9 comments
Jensen asked this little duck robot for a somersault. It actually delivered. 🦆
r/SATNA_PROJECT
•
3d ago
Jensen asked this little duck robot for a somersault. It actually delivered. 🦆
52 upvotes
20 humanoid robots danced alongside 120 people at the WorldSkills opening ceremony in Shanghai
r/SATNA_PROJECT
•
3d ago
20 humanoid robots danced alongside 120 people at the WorldSkills opening ceremony in Shanghai
45 upvotes · 3 comments
Learning REA? Here’s a practical roadmap—with linked resources, real investigations, and the fundamentals alongside it
r/SATNA_PROJECT
•
8h ago
Learning REA? Here’s a practical roadmap—with linked resources, real investigations, and the fundamentals alongside it
22 upvotes · 1 comment
50 crypto research websites, organized by what you actually need to check
r/SATNA_PROJECT
•
3d ago
50 crypto research websites, organized by what you actually need to check
20 upvotes
Complete Cybersecurity Course — Resources in One Google Drive Folder
r/SATNA_PROJECT
•
6d ago
Complete Cybersecurity Course — Resources in One Google Drive Folder
12 upvotes · 2 comments
68% of my Claude Code spend was a too-full context
r/SATNA_PROJECT
•
2d ago
68% of my Claude Code spend was a too-full context
7 upvotes
Make your AI editor grade its own writing—and show you exactly what it changed
r/SATNA_PROJECT
•
7d ago
Make your AI editor grade its own writing—and show you exactly what it changed
5 upvotes
I’ve tested all the major AI generators for my side hustle. Here’s my Top 5 right now (and how I'm making my posters).
r/SATNA_PROJECT
•
9h ago
I’ve tested all the major AI generators for my side hustle. Here’s my Top 5 right now (and how I'm making my posters).
3 upvotes · 1 comment
🎃 Halloween Deal: Satna Project Premium — 18% Off Lifetime Access Until October 31
r/SATNA_PROJECT
•
6d ago
🎃 Halloween Deal: Satna Project Premium — 18% Off Lifetime Access Until October 31
37 comments
VIEW POST IN
Français
Português (Brasil)
See more
Public
Home
Popular
News
Explore
Best of Reddit
Best of Reddit in Portuguese
Best of Reddit in German
Reddit Rules
Privacy Policy
User Agreement
Your Privacy Choices
Accessibility
Reddit, Inc. © 2026. All rights reserved.

Join the most real place on the internet

 Sign in with Apple
Continue with Phone Number
Continue with Email

By continuing, you agree to our User Agreement and acknowledge that you understand the Privacy Policy.
```
