reel: https://www.instagram.com/reel/De8mEDavJu2/
captured: 2026-10-29
yt-dlp: 2026.10.26
ffmpeg: 7.0.2-static
faster-whisper: 1.2.1
ctranslate2: 4.8.4
claude: 2.1.281 (Claude Code)

## Caption

Twine — turn linked passages into a playable story.

In our lighthouse story, bringing tea raises trust. Later, that choice decides whether the keeper shares a secret.

① Publish to File → one HTML file you can play in a browser or host on itch.io.
② Export as Twee → plain text that a game engine can read with a suitable parser.

We ran our story in Twine 2.12.1 and Godot 4.3. The Godot parser was written for this episode: it supports only the passages, links and Harlowe macros used here. It is not an official integration or a general Harlowe runtime.

What earlier choice would you let a character remember?

Twine — 연결한 단락을 플레이할 수 있는 이야기로 만듭니다.

직접 만든 등대지기 이야기에서 차를 건네면 신뢰가 올라가요. 나중에 등대지기가 비밀을 알려 줄지는 그 선택에 달려 있습니다.

① Publish to File → 브라우저에서 열거나 itch.io에 올릴 수 있는 HTML 파일 한 장.
② Export as Twee → 알맞은 파서를 통해 게임 엔진에서 읽을 수 있는 텍스트.

같은 이야기를 Twine 2.12.1과 Godot 4.3에서 실행했습니다. Godot 파서는 이 편을 위해 작성했으며 여기 쓰인 단락·링크·Harlowe 매크로만 처리해요. 공식 연동이나 범용 Harlowe 실행기는 아닙니다.

캐릭터가 어떤 이전 선택을 기억하게 만들고 싶으신가요?

Twine: Chris Klimas & contributors · GPL-3.0
Harlowe 3.3.9: Leon Arnott · Zlib / Godot 4.3: contributors · MIT
Story & Godot example / 이야기·Godot 예제: our own / 직접 제작
Curated by @hyun2xyz

## Transcript

[   0.0] Ever wondered how a game lets you choose what to say and remembers it later?
[   4.5] Today's open-source project has been doing that since 2009.
[   8.5] Twine by Chris Clemas.
[  10.5] Even Netflix's Bandersnatch was written in it.
[  13.5] You write a story as linked passages and it turns them into a game you can play in a browser.
[  18.5] Each passage is a box on a map.
[  21.0] Double square brackets make a link and every link becomes both a choice for the player and an arrow on the map.
[  27.0] Variables remember things.
[  29.0] Bringing T adds one to trust and later an if shows the secret only to players who were kind.
[  35.5] To ship it, choose Publish to file.
[  38.0] You get a single HTML page that runs in any browser, so you can upload it to itch.io and that is your game.
[  45.0] To use it inside a game engine, choose Export as Twee to get plain text.
[  50.0] Here, a short script in Godot reads the passages, turns links into choices and lights the lamp when a passage is tagged lamp.
[  57.5] Twine is open-source under the GPL license.
[  61.0] Thank you. Bye.

## On-screen text

Keeper: Storm's coming. What brings you up here? / I brought you some tea. / Just looking around. — Wikipedia-style Bandersnatch info box: approached by Netflix about making an interactive film in May 2017... Netflix's creation of a bespoke program called Branch Manager... Bandersnatch was originally to be part of Black Mirror's 5th series... Cinematography: Will Poulter, Aaron Mordor; Music by: Tony Kearns; Production companies: Brian Reitzell / House of Tomorrow; Distributed by: Netflix; Release date: 28 December 2018; Running time: Default 90 minutes, Total 312 minutes; Country: United Kingdom; Language: English; Critics praised the technical design of the film but criticised the story's characterisation... — TWINE (title card) — itch.io: Browse Games, Game Jams, Login, Register; Top / Games / Jams; Sort by Popular, New & Popular, Top sellers, Most Recent; made with Twine (23,756 results); Select a tab...; Filter; Romance, Fantasy, Meaningful Choices, Mystery, Role Playing, Narrative (View all tags); itch.io on YouTube — Subscribe for game recommendations, clips, and more; View Channel — Archiving and Exporting Stories: Archiving Your Library — Archiving your library saves all stories in it to a single file. You can use an archive as a way to back up your work, or to move your library between computers or different web browsers. To create an archive, choose the Archive button under the Library top toolbar tab... Exporting a Story — To export a single story, select it and choose Publish to File from the Build top toolbar tab... — Subtitle overlays: Ever wondered how a game lets you choose what to say, / 게임은 어떻게 내가 할 말을 고르게 하고 — Even Netflix's Bandersnatch was written in it. / 넷플릭스 「밴더스내치」도 이걸로 썼습니다. — You write a story as linked passages, / 이야기를 서로 이어진 단락으로 쓰면 — so you can upload it to itch.io, and that is your game. / itch.io에 올리면 그게 바로 게임입니다. — To use it inside a game engine, choose Export as Twee to get plain text. / 게임 엔진 안에서 쓰려면 Export as Twee로 평범한 글을 받습니다. — Keeper / Then look quickly. (lighthouse illustration); passage: Look   $trust = 0 — Twine editor: Back / Passage / Story / Build / Twine; Start passage box: (set: $trust to 0) Keeper: Storm's coming. What brings you up here? [[Brought you tea->Tea]] [[Just looking around->Look]] — Twine story map view: linked passage nodes including Start, Tea, Look, Lamp with connecting arrows — Keeper: That's kind. Sit by the fire. / Watch the lamp — Twee export code: :: StoryTitle / The Lighthouse / :: StoryData { "ifid": "...", "format": "Harlowe", "format-version": "3.3.9", "start": "Start" } :: Start Keeper: Storm's coming. What brings you up here? [[Brought you tea->Tea]] [[Just looking around->Look]] :: Lamp [lamp] Keeper: Time to light the lamp. (if: $trust >= 1)[Keeper: Here's a secret: the old map is under the third step.](else:)[Keeper: Goodnight, stranger.] :: Look Keeper: Then look quickly. [[Watch the lamp->Lamp]] :: Start

## Key claims

- Twine has let creators write choice-based, state-remembering games since 2009
- Netflix's Bandersnatch was written using Twine
- A Twine story is written as linked passages, with each passage shown as a box on a map
- Double square brackets create links, which become both player choices and arrows on the story map
- Variables can store and remember player choices (e.g., bringing tea adds 1 to a trust variable)
- An if-check can gate content (e.g., a secret) based on a variable like trust
- Publish to File exports a single HTML file playable in any browser, which can be uploaded to itch.io
- Export as Twee produces plain text that can be read by a game engine with a suitable parser
- The reel's story was run in Twine 2.12.1 and Godot 4.3
- A custom Godot parser was written specifically for this episode and only supports the passages, links, and Harlowe macros used in this story — it is not an official integration or a general-purpose Harlowe runtime
- In the Godot example, a script reads passages, turns links into choices, and lights a lamp when a passage is tagged 'lamp'
- Twine is open-source under the GPL-3.0 license
- Harlowe 3.3.9 (by Leon Arnott) is licensed Zlib; the Godot integration code is MIT licensed

## Info channel

caption

## Mentioned (unverified hints)

- Twine: (no url)
- Harlowe: (no url)
- Godot: (no url)
- itch.io: (no url)
