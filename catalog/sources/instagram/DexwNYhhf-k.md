reel: https://www.instagram.com/reel/DexwNYhhf-k/
captured: 2026-10-29
yt-dlp: 2026.10.26
ffmpeg: 7.0.2-static
faster-whisper: 1.2.1
ctranslate2: 4.8.4
claude: 2.1.281 (Claude Code)

## Caption

SPlisHSPlasH computes a water simulation from particles, obstacles and gravity.

We made a dam-break scene with 71,346 particles. Nearby particles contribute mass through a smooth kernel to estimate density; the DFSPH solver corrects compression as the water moves.

The workflow is SPlisHSPlasH simulation → splashsurf surface reconstruction → Mitsuba rendering. Four seconds of simulated motion took 3,052 steps and about 14 minutes on one CPU core, before rendering. The water sequences play in 2× slow motion.

Where would you use a particle-to-surface workflow: a VFX shot, a material study, or an SPH lesson? The scene and explanatory graphics are our own. Each software dependency has its own terms.

SPlisHSPlasH는 입자·장애물·중력으로 물의 움직임을 계산하는 유체 시뮬레이션 도구예요.

직접 만든 댐 붕괴 장면에 입자 71,346개를 넣었어요. 가까운 입자의 질량을 부드러운 커널로 가중해 밀도를 구하고, DFSPH 솔버가 물이 움직이는 동안 압축을 보정합니다.

SPlisHSPlasH 시뮬레이션 → splashsurf 표면 재구성 → Mitsuba 렌더 순서입니다. 시뮬레이션 속 4초에 3,052단계, CPU 코어 하나로 약 14분이 걸렸고 렌더 시간은 별도예요. 물 장면은 모두 2배 슬로모션입니다.

VFX 장면, 재질 연구, SPH 수업 중 어디에 활용하고 싶으신가요? 장면과 설명 그림은 직접 만들었습니다. 각 소프트웨어 의존성의 사용 조건은 따로 확인해야 합니다.

Source · licenses / 원본·라이선스
SPlisHSPlasH 2.18.1 · Jan Bender et al. · MIT
https://github.com/InteractiveComputerGraphics/SPlisHSPlasH/tree/2.18.1
https://github.com/InteractiveComputerGraphics/SPlisHSPlasH/blob/2.18.1/LICENSE
splashsurf · Fabian Löschner · MIT
https://github.com/InteractiveComputerGraphics/splashsurf/tree/56d3e6a
https://github.com/InteractiveComputerGraphics/splashsurf/blob/56d3e6a/LICENSE
Mitsuba 3.9.1 · renderer · BSD-3-Clause
https://github.com/mitsuba-renderer/mitsuba3/blob/v3.9.1/LICENSE
Scene, visualization & curation / 장면·시각화·큐레이션: @hyun2xyz

## Transcript

[   0.0] This is a water simulation. It's 71,000 particles computed one tiny time step at a time.
[   7.5] Today's open source project is Splish Splash, a fluid simulation library by Jan Bender.
[  13.5] It uses smoothed particle hydrodynamics, or SPH.
[  17.5] The water is split into particles and each one carries a little mass.
[  22.0] To find the density of the particle, it adds up the mass of its neighbors within a small radius,
[  27.0] weighted by a smooth kernel.
[  29.0] Here that's 41 neighbors, and the result is a thousand kilograms per cubic meter,
[  34.0] right at the density of water.
[  36.0] Real water barely compresses, so whenever particles crowd together,
[  40.0] the solver pushes them apart with pressure.
[  42.5] Its DFSPH solver repeats that correction until the average compression is under one hundredth of a percent.
[  49.5] Every step, it finds the neighbors, solves for pressure, adds gravity and viscosity,
[  54.0] and moves every particle.
[  56.0] This four-second splash took about three thousand steps.
[  59.5] On their own, the particles look like sand.
[  62.0] A companion tool, Splash Surf, wraps them in a smooth surface, and Mitsuba renders it as water.
[  68.0] Splash Splash is open source under the MIT license.
[  71.5] Thank you. Bye.

## On-screen text

SPlisHSPlasH | Today's open-source project is SPlisHSPlasH, 오늘의 오픈소스는 SPlisHSPlasH입니다. | 71,346 particles · colour = speed   t = 0.00 s | It uses smoothed particle hydrodynamics, or SPH. 평활 입자 유체역학, 줄여서 SPH를 씁니다. | slice through the middle of the tank   t = 0.54 s | To find the density at a particle, 한 입자의 밀도를 구하려면 | closer neighbours count more (kernel weight)   t = 0.54 s | 41 neighbours (in 3D) + itself | Here that's 41 neighbors, 여기서는 이웃이 41개이고 | density in the same slice   t = 0.21 s | below 1,000 kg/m³   1,000  +0.5% | Real water barely compresses. 실제 물은 거의 압축되지 않습니다. | README | License | build-linux build-windows-wheels build-macos build-mac-wheels docs | SPlisHSPlasH is an Open-source library for the physically-based simulation of fluids. The simulation in this library is based on the Smoothed Particle Hydrodynamics | README | License | SPlisHSPlasH is an open-source library for the physically-based simulation of fluids. The simulation in this library is based on the Smoothed Particle Hydrodynamics (SPH) method which is a popular meshless Lagrangian approach to simulate complex fluid effects. The SPH formalism allows an efficient computation of a certain quantity of a fluid particle by considering only a finite set of neighboring particles. One of the most important research topics in the field of SPH methods is the simulation of... | how far each neighbour is (up to 4 r)   0 ... distance to the neighbour ... 4 r = 6.4 cm | density in the same slice   t = 1.58 s | below 1,000 kg/m³   1,000  +0.5% | average compression, all 71,346 particles: 0.010 % | @index.opensource | @hyun2xyz | Its DFSPH solver repeats that correction, DFSPH 솔버는 이 보정을 반복합니다. | Thank you. 고맙습니다. | README | License | Features | SPlisHSPlasH implements: an open-source SPH fluid simulation (2D & 3D); neighborhood search on CPU or GPU; supports vectorization using AVX; Python binding (thanks to Stefan Jeske); supports embedded Python scripts; several implicit pressure solvers (WCSPH, PCISPH, PBF, IISPH, DFSPH, PF); explicit and implicit viscosity methods; current surface tension approaches; different vorticity methods; computation of drag forces; support for multi-phase simulations

## Key claims

- The scene is a dam-break water simulation with 71,346 particles
- SPlisHSPlasH uses smoothed particle hydrodynamics (SPH) to simulate the fluid
- Density at a particle is estimated by summing neighbor mass within a radius, weighted by a smooth kernel; here each particle has 41 neighbors
- The resulting density is about 1,000 kg/m³, matching real water
- Real water barely compresses, so the DFSPH solver repeatedly corrects pressure to keep compression low (average compression 0.010% across all 71,346 particles)
- Each simulation step finds neighbors, solves for pressure, adds gravity and viscosity, and moves every particle
- 4 seconds of simulated motion took 3,052 steps and about 14 minutes on one CPU core, not counting rendering
- The workflow is SPlisHSPlasH simulation → splashsurf surface reconstruction → Mitsuba rendering
- splashsurf wraps the raw particles into a smooth surface, and Mitsuba renders it to look like water
- The water sequences in the reel are shown in 2x slow motion
- SPlisHSPlasH is open source under the MIT license; splashsurf is also MIT; Mitsuba is BSD-3-Clause

## Info channel

caption

## Mentioned (unverified hints)

- SPlisHSPlasH: https://github.com/InteractiveComputerGraphics/SPlisHSPlasH/tree/2.18.1
- splashsurf: https://github.com/InteractiveComputerGraphics/splashsurf/tree/56d3e6a
- Mitsuba: https://github.com/mitsuba-renderer/mitsuba3/blob/v3.9.1/LICENSE
