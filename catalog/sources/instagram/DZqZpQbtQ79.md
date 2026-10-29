reel: https://www.instagram.com/reel/DZqZpQbtQ79/
captured: 2026-10-29
yt-dlp: 2026.10.26
ffmpeg: 7.0.2-static
faster-whisper: 1.2.1
ctranslate2: 4.8.4
claude: 2.1.281 (Claude Code)

## Caption

Game Dev Secrets: MENUS MENUS MENUS
#gamedev #godot #pixelart #indiegames #indiedev

## Transcript

[   0.0] A game dev secret about menus.
[   2.3] Let's say I made this really cool menu box
[   4.7] to use for the UI in Isadora's Edge.
[   6.5] So I pull it into the scene
[   7.8] and I try to get it all lined up,
[   9.2] but it's not quite long enough to fit everything.
[  11.4] I'm gonna need to stretch it out a little bit.
[  13.2] But if I just try to scale it up along the Y axis,
[  15.7] you can see how that distorts the corners
[  17.7] and it looks really bad.
[  18.9] And the more I need to scale it,
[  20.3] the worse the distortion gets.
[  21.8] So now I could go and remake the art asset directly
[  24.8] for every different version of this panel
[  26.5] that I'm gonna need,
[  27.3] but that'll take a lot of time.
[  28.9] And if I ever wanna make minor changes to the UI,
[  31.2] I would need to redo a bunch of art.
[  33.1] Instead, we're gonna use an incredibly convenient trick
[  35.9] called nine slicing.
[  37.6] And nine slicing is actually a very accurate name
[  40.2] because what we're gonna do
[  41.1] is slice the panel into nine different sections.
[  43.4] We'll separate the panel into the four corners,
[  45.1] the four edges, and then the center.
[  46.9] Now, when we scale up the panel,
[  48.5] we don't have to scale the corners at all.
[  50.6] We just put the corners in the right place
[  52.2] and then scale each edge along its own axis
[  55.5] to connect the corners together.
[  57.4] And then the center scales in both axes
[  58.8] so it still just like fits in the middle.
[  60.2] This prevents distortion on the corners entirely
[  62.5] because we're not touching them at all.
[  63.8] And as long as the edges and center are drawn
[  65.8] so that they scale cleanly,
[  67.4] it makes resizing panels super easy.
[  70.0] But now you might be thinking
[  71.1] that this nine slicing technique
[  72.4] sounds really complicated
[  74.0] to actually get set up in the first place.
[  75.7] But it's such a useful technique
[  77.4] that it's just supported by default
[  78.8] in a lot of game engine.
[  79.7] So there's almost no extra work required
[  81.3] on your end at all.

## On-screen text

LET'S SAY THAT I'M GOING TO NEED ONLY HORIZONTAL SCALING ONLY VERTICAL SCALING ALL SCALING ONLY VERTICAL SCALING ONLY HORIZONTAL SCALING LOVE THIS!

## Key claims

- Scaling a UI panel along the Y axis without nine-slicing distorts the corners, and distortion worsens with more scaling.
- Remaking art assets for every panel size is time-consuming and makes minor UI changes costly.
- Nine slicing divides a panel into nine sections: four corners, four edges, and a center.
- With nine slicing, corners are never scaled (only repositioned), preventing distortion.
- Edges are scaled along only one axis (horizontal or vertical) to connect the corners.
- The center is scaled along both axes to fill the middle.
- As long as edges/center are drawn to scale cleanly, nine slicing makes resizing panels easy without extra distortion.
- Nine slicing sounds complex to set up but is supported by default in many game engines, requiring little extra work.

## Info channel

spoken

## Mentioned (unverified hints)

- Isadora's Edge: (no url)
- Godot: (no url)
- 9-slice (nine slicing): (no url)
