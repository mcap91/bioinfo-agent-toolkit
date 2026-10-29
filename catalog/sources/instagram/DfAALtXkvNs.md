reel: https://www.instagram.com/reel/DfAALtXkvNs/
captured: 2026-10-29
yt-dlp: 2026.10.26
ffmpeg: 7.0.2-static
faster-whisper: 1.2.1
ctranslate2: 4.8.4
claude: 2.1.281 (Claude Code)

## Caption

How did Rogue build a brand new dungeon every time you played? It plays tic-tac-toe.

Roguelikes are named after one game: Rogue, from 1980, by Michael Toy and Glenn Wichman, later with Ken Arnold. Most adventure games then were "canned", Wichman wrote, the same every time, so they decided the program itself should build the dungeon.

Drop rooms anywhere and they crash into each other, and some have no way in. In Rogue's code (version 5.4), the 80 x 24 screen is cut into a three by three board. Each square gets one room, random in size and spot but never outside its square, and up to three squares stay empty, just a spot the tunnels pass through. Then the tunnels: from a random room, dig to a neighbor that isn't joined yet, again and again until all nine are in, so every room can be reached. Then up to four extra tunnels, "so that there isn't always just one unique passage through it", as a comment in the code says.

The dungeons in this film are our own run of Rogue 5.4's rules, built in code; the crashing rooms are our own naive version. Not affiliated with or endorsed by the makers of Rogue.

Which game's level generator should we open up next?

Sources: Rogue 5.4.4 source code, rooms.c and passages.c (Michael Toy, Ken Arnold and Glenn Wichman, BSD licence). Glenn R. Wichman, "A Brief History of Rogue", 1997.
Sounds: our own, made in code.

#rogue #roguelike #gamedev #proceduralgeneration

## Transcript

[   0.0] Roguelikes are named after one game, Rogue, from 1980.
[   5.6] How did it build a new dungeon every time you played?
[   9.3] Most adventure games back then were, as its co-creator Glenn Witchman put it, canned,
[  14.2] the same every time.
[  16.4] Rogue's program would build the dungeon itself, but drop nine random rooms on a screen
[  21.9] and they crash into each other.
[  23.9] Some get no way in at all.
[  25.9] So how do you make a dungeon that's random, but always works?
[  32.0] Play Tic Tac Toe!
[  33.6] Rogue's code cuts the screen into a 3x3 board and every square gets one room.
[  39.5] Its size and spot are random, but it never leaves its square so rooms can't collide.
[  45.0] Up to three squares stay empty, just a spot where tunnels meet.
[  49.2] Then the tunnels.
[  50.8] From a random room, dig to a neighbor that isn't joined yet, again and again, until all
[  55.9] nine are in.
[  57.6] Every room can be reached.
[  59.5] Then up to four extra tunnels, so that, in the code's own words, there isn't always
[  64.3] just one unique passage through it.
[  67.0] Random, but inside a board.
[  69.6] One room per square and a tunnel to every room.
[  72.7] Witchman's goal?
[  73.9] A game that could surprise even the people who made it.

## On-screen text

ROGUE, 1980 How did Rogue build a new dungeon every time? @ ######## ###### ############# ########## ...........+########## ##

## Key claims

- Roguelikes are named after the 1980 game Rogue, created by Michael Toy and Glenn Wichman, later joined by Ken Arnold.
- Most adventure games of that era were 'canned' (the same layout every time), so Rogue's creators had the program generate the dungeon itself.
- Dropping rooms randomly anywhere causes them to crash into each other, and some rooms end up with no way in.
- Rogue's code (version 5.4) divides the 80x24 screen into a 3x3 (tic-tac-toe style) grid/board.
- Each of the nine squares gets one room, random in size and position but confined to its square, preventing collisions.
- Up to three squares can remain empty, serving only as a point where tunnels pass through/meet.
- Tunnels are dug from a random room to a neighboring unjoined room, repeated until all nine squares are connected, ensuring every room is reachable.
- Up to four extra tunnels are added so there isn't always just one unique passage through the dungeon, per a comment in the source code.
- The dungeons shown in the video are the creators' own implementation of Rogue 5.4's generation rules, built in code; the 'crashing rooms' demonstration is their own naive version, not the original game.
- The video/sounds are not affiliated with or endorsed by the makers of Rogue; all sounds were made in code by the creators.
- Glenn Wichman's goal was to create a game that could surprise even its own creators.

## Info channel

spoken

## Mentioned (unverified hints)

- Rogue (1980): (no url)
- Rogue 5.4.4 source code: (no url)
