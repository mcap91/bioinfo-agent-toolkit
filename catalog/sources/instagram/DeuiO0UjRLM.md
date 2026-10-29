reel: https://www.instagram.com/reel/DeuiO0UjRLM/
captured: 2026-10-29
yt-dlp: 2026.10.26
ffmpeg: 7.0.2-static
faster-whisper: 1.2.1
ctranslate2: 4.8.4
claude: 2.1.281 (Claude Code)

## Caption

Make Your Game Feel Responsive by Breaking the Rules. Traditional animation rules divide an animation into three sections. The first "Anticipation" is great for adding weight, but can make a game feel less responsive. It's great for non-interactive media such as movies and television, as well as games where the wind-up animation is built into the gameplay. For games that want to optimize the responsiveness these rules sometimes need to be broken.  Jump animation credit: Andrew Coyle (https://cloytoons.wordpress.com/)

#gamedesign

## Transcript

[   0.0] Break! Traditional animation rules to make your game feel snappier and more responsive.
[   5.8] Here's how we did it in Diablo 3. In traditional animation, any action,
[  10.4] like swinging a weapon, jumping or casting a spell, breaks down into three parts,
[  15.9] the anticipation, the action itself, and the follow-through, with roughly a third of
[  21.1] the total animation time spent on each. A common problem in video game design is how
[  26.6] the anticipation portion of the animation can make input feel non-responsive.
[  32.4] Looking way back at classics like Super Mario, we know that when the player hits jump,
[  38.2] it feels more responsive to have the character begin moving up immediately.
[  42.9] The principle is widely taught in game design schools. Don't animate the wind-up part of a
[  48.3] jump if you want snappy controls. But it applies to more than just jumping.
[  53.4] In Diablo 3, we do the same thing with many attack animations.
[  57.6] Let's use a barbarian two-handed weapon swing as an example.
[  61.1] During early development, we had anticipation in the animation. The player clicks the mouse,
[  66.5] and the barbarian reaches back from the neutral pose to the start of the swing.
[  71.6] That's the anticipation. But everybody in the team said,
[  75.6] oh, the attack feels sluggish. Speed it up! But speeding up the animation causes the
[  81.6] entire animation to look less believable and to lose its sense of weight. Worst of all,
[  87.4] it doesn't even fix the problem. We still got complaints that the attacks didn't feel responsive.
[  93.2] What actually helped was chopping out the anticipation frames of the animation.
[  98.2] In Diablo, the moment you click the mouse, the barbarian instantly pops to a fully
[ 103.0] retracted extension right where the action begins. It's the same as the Mario jumping
[ 108.3] principle. In game development, we often talk about a character's silhouette,
[ 113.3] that is, how the overall shape of the character looks on the screen.
[ 117.6] Popping the barbarian instantaneously to a dramatically different silhouette
[ 122.2] allows the player to make an instantaneous and satisfying visual read that something on the
[ 128.1] screen has changed. Sometimes it's still crazy to me that we're just talking about 5 or 6
[ 133.1] frames of animation, which takes maybe 180 milliseconds, but it makes all the difference.
[ 139.8] Removing those 180 milliseconds gives the player the instantaneous visual feedback
[ 145.7] that the game is acting on the player's input, which in turn makes the game feel responsive
[ 152.0] and satisfying.

## On-screen text

Cut Animation Frames to Make Your Game Feel Responsive / TRADITIONAL ANIMATION RULES / 1/3 ANTICIPATION 1/3 ACTION 1/3 FOLLOW-THROUGH / every action, three equal parts / it in Diablo 3. / In traditional animation, any action like / A common problem in video / game design is how the / Looking way back at classics like / But it applies to / ANTICIPATION ACTION FOLLOW-THROUGH / EARLY BUILD / During early development we had / 1x / 2x / But speeding up the animation / 2x WAIT / FRAME 509 / FRAME 520 / In Diablo, the moment you click / the mouse the Barbarian instantly pops / where the action begins, it's the / In game development we often / It doesn't even fix the problem, / talk about a character's silhouette. / Sometimes it's still crazy to me / 0 ms / that we're just talking about five / player's input, which in turn makes / CLICK SWING

## Key claims

- Traditional animation divides any action into three roughly equal parts: anticipation, action, and follow-through.
- The anticipation portion of an animation can make video game input feel non-responsive.
- Classic games like Super Mario make the character begin moving up immediately on jump input rather than animating a wind-up, which feels more responsive.
- It's widely taught in game design schools not to animate the wind-up part of a jump for snappy controls.
- In Diablo 3's early development, the barbarian's two-handed weapon swing included an anticipation phase (reaching back from neutral pose).
- Team members felt the attack animation was sluggish and asked for it to be sped up.
- Speeding up the animation made it look less believable and lose its sense of weight, and still didn't fix the responsiveness complaints.
- The actual fix was removing/chopping out the anticipation frames so the barbarian instantly pops to a fully retracted swing position the moment the player clicks.
- This relates to the concept of a character's 'silhouette' — an instant change in silhouette gives the player a satisfying, instantaneous visual read that something changed.
- The removed anticipation was only about 5-6 frames, roughly 180 milliseconds, but removing it made a significant difference to perceived responsiveness.
- Removing those frames gives instantaneous visual feedback that the game is responding to player input, making the game feel more responsive and satisfying.

## Info channel

spoken

## Mentioned (unverified hints)

- Diablo 3: (no url)
- Overwatch: (no url)
- Super Mario (classic Mario games): (no url)
- Cloytoons (Andrew Coyle jump animation): https://cloytoons.wordpress.com/
