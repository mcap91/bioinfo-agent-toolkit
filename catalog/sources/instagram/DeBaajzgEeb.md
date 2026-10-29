reel: https://www.instagram.com/reel/DeBaajzgEeb/
captured: 2026-10-29
yt-dlp: 2026.10.26
ffmpeg: 7.0.2-static
faster-whisper: 1.2.1
ctranslate2: 4.8.4
claude: 2.1.281 (Claude Code)

## Caption

Training an AI to Drive with Natural Selection

A self-driving car does what you do, many times a second: look, decide, act. Looking turns the road into numbers (how far is that wall? how fast am I going?). Deciding is a function that turns those numbers into gas, brake and steering.

This car sees seven numbers: how far the walls are along five yellow lines, its speed, and its direction. Its function is a small neural network with 434 weights, and nobody set them. I made twenty random ones and let them race; most crashed at once. The ones that got furthest became parents, and their children are copies with small random changes. Generation 33 finished the first lap. By generation 4,000 they race through every corner, on lines they found themselves.

In the literature this is called neuroevolution: a neural network trained by selection and mutation alone, with no gradients.

#AI #neuralnetwork #evolution #selfdriving #machinelearning

## Transcript

[   0.0] I made a little car racing game.
[   2.6] Arrow keys, gas, brake, left, right.
[   6.6] But I want an AI to drive it.
[   8.8] So what is an AI that can drive this car?
[  12.2] First, what the car senses.
[  14.6] How far the walls are along these yellow lines.
[  20.2] And its speed and its direction.
[  24.6] I pass these seven numbers into a function
[  27.0] and it gives me back one number, the gas.
[  31.2] Plus one is full gas.
[  34.8] Minus one, full brake.
[  37.6] A second function, steers.
[  39.6] Plus one, full right.
[  44.9] Minus one, full left.
[  48.5] That's all it is.
[  50.0] Whether it drives well is another story.
[  53.4] Both functions are one neural network.
[  56.1] Every number is multiplied by a weight,
[  58.3] added up and squeezed between minus one and plus one.
[  62.1] Every circle does that.
[  63.7] Layer after layer, 434 weights.
[  68.4] Different weights, a different driver.
[  70.7] Somewhere there's a set that drives like Max Verstappen.
[  76.0] I don't know those weights.
[  77.5] So let's make 20 random ones and let them race.
[  83.2] Most of them crash right away.
[  86.4] But this one got the furthest.
[  88.4] Its weights must be onto something.
[  92.4] So I copy them, nudge each copy a little at random
[  96.2] and get 20 children.
[ 102.0] Some are worse, some are better.
[ 106.4] The best ones become the new parents,
[ 108.6] again and again, just like natural selection.
[ 112.5] Generation 33 and finally a full lap.
[ 117.9] Now more and more of them finish.
[ 120.2] The five fastest become the new parents.
[ 123.7] Let's fast forward.
[ 130.5] 4,000 generations later,
[ 132.9] the best driver 20 times on one grid.
[ 143.5] Nobody taught them to drive.
[ 145.5] Every corner, every line, they found it themselves.
[ 156.5] From 20 random functions to this.

## On-screen text

I don't know those weights. GEN 1 20 CARS · 11 DRIVING GEN 2 20 CARS · 4 DRIVING GEN 2 GEN 145 20 CARS · 8 DRIVING 19 FINISHED Let's fast-forward.

## Key claims

- A self-driving car in a custom racing game senses seven numbers: distances along five yellow lines to walls, its speed, and its direction.
- A neural network with 434 weights takes these seven inputs and outputs two values: gas/brake and steering.
- Each neuron multiplies inputs by weights, sums them, and squeezes the result between -1 and 1.
- Weights were not hand-set; they were evolved via neuroevolution (random initialization, selection, and mutation, with no gradients).
- 20 random-weight cars were raced initially; most crashed immediately.
- The car that got furthest was selected as a parent; its weights were copied and mutated slightly to create 20 children (offspring).
- This selection-and-mutation process repeated generation after generation, akin to natural selection.
- Generation 33 was the first to complete a full lap.
- The five fastest cars became parents in later generations as more cars began finishing.
- By generation 4,000, the best drivers (20 copies on one grid) could race through every corner on lines they discovered themselves.
- Nobody taught the cars to drive directly — the driving behavior emerged purely from evolutionary selection.

## Info channel

spoken

## Mentioned (unverified hints)

(none mentioned)
