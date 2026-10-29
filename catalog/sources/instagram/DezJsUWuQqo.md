reel: https://www.instagram.com/reel/DezJsUWuQqo/
captured: 2026-10-29
yt-dlp: 2026.10.26
ffmpeg: 7.0.2-static
faster-whisper: 1.2.1
ctranslate2: 4.8.4
claude: 2.1.281 (Claude Code)

## Caption

3 unconventional tricks we use to optimise our game! We’re both big steamdeck players, and we want our game to run on as many devices as possible so optimisation has been a big point as we work on our upcoming roguelike - Barrow and Blade. Besides your typical techniques like occlusion culling, baked lighting, and object pooling, we’re using a few techniques that are a bit more novel so we thought we’d make a video giving a brief overview of them! All 3 of these techniques have the added benefit of helping us achieve the art style we’ve envisioned for the game, despite only being a team of two. 

If you want to hear more about Barrow and Blade, our upcoming game that combines hack and slash roguelike dungeon crawling with a tactical shopkeeping deckbuilder, we’d love if you’d drop us a follow and join the discord in our bio! 

#roguelike #indiedev #gamedev #gamedevtips

## Transcript

[   0.0] Three tricks we use to optimize our game in under 60 seconds.
[   4.2] 2D art in a 3D world.
[   6.2] Instead of creating complex 3D models, our artist illustrates the assets for our environment,
[  11.3] which we then project onto simple boxes and cylinders.
[  14.6] This drastically reduces the poly count of our scenes
[  17.5] and lets us create really varied stylized environments super quickly.
[  21.9] Building our own shadows.
[  24.1] Instead of using the built-in shadow system in Unreal,
[  27.0] we use the second simplified mesh of the character
[  30.0] and use a material to flatten this onto the floor.
[  32.9] This not only saves us a bit of performance on lighting calculations,
[  36.5] but also allows us to create punchy stylized shadows that match our environment's art style.
[  41.9] Storing time inside a texture.
[  44.6] Instead of spawning lots of decals or actors to represent a ground effect in our game,
[  49.3] we store time and location information inside a texture
[  52.8] and use that in a material to control how the effect appears and disappears.
[  57.0] We then use a separate data-driven grid system
[  59.5] to detect when a character enters or leaves each area.
[  62.5] This saves us having to track the lifetime and overlaps of different ground effects independently,
[  67.1] which can get expensive quite quickly.
[  69.6] If you want to see more of our game's development,
[  71.8] drop us a follow and join our Discord.
[  74.1] Bye!

## On-screen text

3 TRICKS WE USE TO OPTIMISE OUR GAME IN UNDER 60 SECONDS AND LETS US CREATE REALLY STYLIZED ENVIRONMENTS SUPER QUICKLY OUR ARTIST ILLUSTRATES THE ASSETS WHICH WE THEN PROJECT ONTO THIS DRASTICALLY REDUCES THE POLY IN SHADOW SYSTEM IN UNREAL AND USE A MATERIAL TO THIS NOT ONLY SAVES US ENVIRONMENT'S ART STYLE WE STORE TIME AND LOCATION INFORMATION INSIDE A TEXTURE EACH AREA

## Key claims

- They use 2D illustrated art projected onto simple 3D boxes and cylinders instead of complex 3D models to reduce poly count and quickly create varied stylized environments.
- Instead of Unreal Engine's built-in shadow system, they use a simplified second character mesh flattened onto the floor via a material to create stylized shadows and save performance on lighting calculations.
- Instead of spawning decals/actors for ground effects, they store time and location info inside a texture, controlled via a material, paired with a data-driven grid system to detect when characters enter/leave areas, saving the cost of tracking lifetimes/overlaps separately.
- All three techniques also help achieve their intended art style despite being only a two-person team.
- They are optimizing for a wide range of devices, including the Steam Deck.
- The game, Barrow and Blade, combines hack-and-slash roguelike dungeon crawling with a tactical shopkeeping deckbuilder.

## Info channel

spoken

## Mentioned (unverified hints)

- Barrow and Blade: (no url)
- Unreal Engine: (no url)
