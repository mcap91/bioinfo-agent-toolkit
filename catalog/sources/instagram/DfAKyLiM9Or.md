reel: https://www.instagram.com/reel/DfAKyLiM9Or/
captured: 2026-10-29
yt-dlp: 2026.10.26
ffmpeg: 7.0.2-static
faster-whisper: 1.2.1
ctranslate2: 4.8.4
claude: 2.1.281 (Claude Code)

## Caption

I hate tilesets. So my map doesn’t have one. 🗺️

Edges, corners, inner corners, 47 pieces for every pair of terrains, all tiling with each other. I drew zero. Every tile is one number, and one shader draws the rest: coasts, grass blades, foam, roads, fields, snow.

Valdrin is a medieval kingdom builder, wishlist on Steam (link in bio).

#gamedev #indiedev #pixelart #shaders #steamgames

## Transcript

[   0.0] I hate tile sets, so my map doesn't have one.
[   3.1] Grass meets dirt, draw the edges, draw the corners, draw the inner corners.
[   8.2] Make sure they all tile with each other.
[  10.4] Now do that 47 times, 16 if you're clever, 5 if you're really clever.
[  16.0] Then add sand and water.
[  18.0] Do it all again for every pair.
[  20.4] I drew zero.
[  22.4] So what are my people standing on?
[  24.7] Numbers.
[  25.7] Every tile is one number.
[  28.0] Water, sand, dirt, grass.
[  30.2] The ground is one shader.
[  32.1] Every pixel looks at the four tiles around it.
[  34.4] They stack, each one shows only where it holds more than half corners.
[  38.4] Round off by themselves.
[  40.0] Add a little noise and the coast starts to wander.
[  43.0] Grass hangs over the dirt, one blade at a time, foam washes in and out.
[  47.9] Roads, footpaths, plowed fields, snow, same shader, and the whole ground is one
[  52.2] draw call.
[  54.1] Zero tiles, just math.
[  56.5] The game's called Baldream.
[  58.1] It's on Steam.

## On-screen text

Grass meets dirt? Draw the edges. So what are my people standing on? Numbers. The ground is one shader one blade at a time. Foam washes in and out. Zero tiles, just math.

## Key claims

- The map uses no tileset at all; every tile is represented by a single number instead of hand-drawn tile art.
- Traditional tilesets require drawing edges, corners, and inner corners for every pair of terrains, which can mean up to 47 tile variants per terrain pair.
- A single shader reads the four surrounding tile numbers per pixel and renders coasts, grass blades, foam, roads, footpaths, plowed fields, and snow.
- Each terrain layer is shown only where it covers more than half the surrounding corners, producing automatically rounded transitions.
- Added noise makes coastlines appear to wander naturally.
- The entire ground is rendered in a single draw call.
- The game is a medieval kingdom builder named Valdrin, available to wishlist on Steam.

## Info channel

spoken

## Mentioned (unverified hints)

- Valdrin: (no url)
