reel: https://www.instagram.com/reel/DegQ9xiIESl/
captured: 2026-10-27
yt-dlp: 2026.10.26
ffmpeg: 7.0.2-static
faster-whisper: 1.2.1
ctranslate2: 4.8.4
claude: 2.1.281 (Claude Code)

## Caption

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

## Transcript

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

## On-screen text

seed 1 - depth 3 | seed 5 - depth 6 | seed 2 - depth 9 | seed 2 - depth 9 | seed 2 | seed 2 | Brogue: Community Edition | Ever wonder how a game can build a brand-new dungeon, every single time you play? | 게임은 어떻게 할 때마다 처음 보는 던전을 새로 지을까요? | Today's open-source project is Brogue: Community Edition, | 오늘의 오픈소스는 Brogue: Community Edition이에요. | Give it a seed number, and it digs a whole level out of solid rock: | 시드 번호 하나를 주면 단단한 바위에서 한 층 전체를 파내요: | Brogue CE is licensed under the AGPL, | Brogue CE는 AGPL 라이선스예요. | up close: every cell is one character | trueweth / BrogueCE | BrogueCE Public | Brogue: Community Edition - a community-led fork of the much-loved minimalist roguelike game | brogue dungeon game roguelike | Readme | BrogueCE / src / brogue / Architect.c | createDungeon(grid) | roomAttempts(grid, 20) | GNU Affero General Public License v3.0 | BrogueCE / LICENSE.txt | Permissions: Commercial use, Modification, Distribution | Limitations: Liability, Warranty | Conditions: License and copyright notice, State changes, Disclose source | @index.opensource | @hyun2xyz

## Key claims

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

## Info channel

caption

## Mentioned (unverified hints)

- Brogue: Community Edition (BrogueCE): https://github.com/tmewett/BrogueCE
