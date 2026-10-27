reel: https://www.instagram.com/reel/DeMiEoaP-8i/
captured: 2026-10-27
yt-dlp: 2026.10.26
ffmpeg: 7.0.2-static
faster-whisper: 1.2.1
ctranslate2: 4.8.4
claude: 2.1.281 (Claude Code)

## Caption

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

## Transcript

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

## On-screen text

the original VoxelSpace.html | map: osrs (the repository's maps are game data and are not used) | the original VoxelSpace.html | map: osrs (the repository's maps are game data and are not used) | VoxelSpace | Ever wondered how a game in 1992 flew over detailed mountains, 1992년의 게임은 어떻게 섬세한 산 위를 날았을까요? | Today's open-source project rebuilds the trick behind Comanche in under twenty lines: 오늘의 오픈소스는 Comanche의 그 기법을 스무 줄도 안 되게 다시 만들었어요. | the whole world: two 1024 x 1024 images | maps: osrs (the repository's maps are game data, excluded from its license) | The whole world is just two images: 세상 전체가 그림 두 장뿐이에요. | from above: the camera looks out, one line at a time | maps: osrs | every 10th line drawn · fov: distance 800, as on the page · maps: osrs | camera | It looks out from the camera one line at a time, 카메라에서 앞을 내다보며 한 번에 한 줄씩, | one screen column: each point's height, projected and drawn bottom-up | one screen column | camera | distance from the camera | column 400 of 800 · points from the page's 400 lines · maps: osrs | Each point's height is projected onto the screen, and drawn as a vertical line in its color. 점마다 높이를 화면에 투영해 그 점의 색으로 세로선을 그어요. | the page's frame, pulled apart column by column | frame: the original VoxelSpace (800 x 514) · map: oasis, snow and gaps · maps: osrs | No polygons at all. Just vertical lines. 다각형은 하나도 없어요. 세로선뿐이에요. | the same page, another view · map: osrs | the original VoxelSpace.html | colour map without light (osrs) | the original VoxelSpace.html | drawn line by line, near to far (the page's own top) · map: osrs | the original page · map: osrs | github.com/s-macke/VoxelSpace | MIT License | Permissions: Commercial use, Modification, Distribution | Limitations: Liability, Warranty | Conditions: License and copyright notice | The code is MIT licensed: 코드는 MIT 라이선스예요. | Thank you. 감사합니다. | @index.opensource | @hyun2xyz | License | The software part of the repository is under the MIT license. Please read the license file for more information. Please keep in mind, that the Voxel Space technology might be still patented in some countries. The color and height maps are reverse engineered from the game Comanche and are therefore excluded from the license.

## Key claims

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

## Info channel

spoken

## Mentioned (unverified hints)

- VoxelSpace: https://github.com/s-macke/VoxelSpace
