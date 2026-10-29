reel: https://www.instagram.com/reel/Der26qADV2G/
captured: 2026-10-29
yt-dlp: 2026.10.26
ffmpeg: 7.0.2-static
faster-whisper: 1.2.1
ctranslate2: 4.8.4
claude: 2.1.281 (Claude Code)

## Caption

6 enemies in my game share the exact same code 🦫 Only their numbers and animations change.

The trick is reusable components: small pieces that each do one thing. A health node that stores health, subtracts damage and fires a signal when it runs out. Another that takes hits, another that deals damage on touch, another that drops experience. Each one is tiny and knows nothing about the enemy.

So making a new enemy is like building with Lego: drop in the components, hook up health, tweak the numbers, and I only work on the animations. Today 76 enemies in Capy of Gods use the same health component.

Wishlist it and play the free demo right now on Steam (link in bio).

#CapyOfGods #gamedev #godot #godotengine #indiedev #solodev #gamedevtips #pixelart #roguelike

## Transcript

[   0.0] Hi, I'm Cappy Ember, and I'm making Cappy of Gods.
[   3.7] These six enemies in my game share the exact same code, only their numbers and animations
[   8.5] change.
[   9.5] The trick?
[  10.5] Reusable components.
[  11.5] A component is a small piece that does just one thing.
[  14.1] Like health.
[  15.1] Instead of writing health inside every enemy, you make a health node.
[  18.4] It stores max health, subtracts damage, and fires a signal when it runs out.
[  22.5] Then another component to take hits.
[  24.3] An area that detects the attack and passes the damage to health.
[  27.5] Another one to deal damage on touch.
[  29.3] Another that drops experience on death.
[  31.3] Each one is tiny, and knows nothing about the enemy.
[  33.7] Now, making a new enemy is like building with LEGO.
[  36.3] I drop in the components, hook health up to the hit area, tweak the numbers, and I only
[  40.2] work on its animations.
[  41.7] If I improve a component, every enemy gets better at once.
[  44.8] Today, 76 enemies use the same health component.
[  47.9] This was super useful while making Cappy of Gods.
[  50.5] Wish listed, and play the free demo right now on Steam.

## On-screen text

6 ENEMIES 1 SINGLE SCRIPT EyeBall Bug Wasp WaterWisp Reaper BurningSkull

## Key claims

- Six enemies in the game share the exact same code; only their numbers and animations change
- Reusable components are used: a health node stores max health, subtracts damage, and fires a signal when it runs out
- A hit-detection component (area) detects attacks and passes damage to the health component
- A separate component deals damage on touch
- Another component drops experience on death
- Each component is tiny and knows nothing about the enemy
- Making a new enemy is like building with Lego: drop in components, hook up health, tweak numbers, and only animations need custom work
- Improving one component improves every enemy at once
- 76 enemies in Capy of Gods currently use the same health component
- Capy of Gods has a free demo available on Steam and can be wishlisted

## Info channel

spoken

## Mentioned (unverified hints)

- Capy of Gods: (no url)
- Godot Engine: (no url)
- Steam: (no url)
