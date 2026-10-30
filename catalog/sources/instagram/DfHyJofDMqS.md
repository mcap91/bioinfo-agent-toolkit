reel: https://www.instagram.com/reel/DfHyJofDMqS/
captured: 2026-10-30
yt-dlp: 2026.10.26
ffmpeg: 7.0.2-static
faster-whisper: 1.2.1
ctranslate2: 4.8.4
claude: 2.1.281 (Claude Code)

## Caption

No motion clips as input—just a T-pose to start.

In this experiment, NVIDIA’s MotionBricks generates a walk by connecting the character’s current pose to a target pose placed ahead. On the zigzag course, we keep updating the blue target as the character moves.

The pretrained model was trained on motion data; we did not use NVIDIA’s evaluation-only sample motions as inputs here. We also made a free Blender add-on to import the generated walk as an animated character.

The tested workflow needs an NVIDIA RTX GPU, Windows or Linux, Blender 4.2 or newer, and about 12 GB of disk space.

입력한 동작 클립 없이, T자세 하나에서 출발했습니다.

이번 실험에서는 NVIDIA MotionBricks가 캐릭터의 현재 자세와 앞에 놓은 목표 자세를 연결해 걷는 동작을 만듭니다. 지그재그 코스에서는 캐릭터가 움직이는 동안 파란 목표를 계속 앞에 놓습니다.

모델 자체는 동작 데이터로 사전 학습됐으며, 이번 입력에는 NVIDIA의 평가 전용 샘플 동작을 사용하지 않았습니다. 생성한 걷기를 애니메이션 캐릭터로 가져올 수 있는 무료 Blender 애드온도 직접 만들었습니다.

검증한 작업 환경에는 NVIDIA RTX GPU, Windows 또는 Linux, Blender 4.2 이상, 약 12GB의 디스크 공간이 필요합니다.

Free add-on download / 무료 애드온 다운로드:
https://github.com/hyun2xyz/motionbricks-blender/releases/tag/v0.1.0
Project & demo / 프로젝트와 데모:
https://github.com/hyun2xyz/motionbricks-blender
MotionBricks code / 코드: https://github.com/NVlabs/motionbricks
Paper / 논문: https://arxiv.org/abs/2604.24833

MotionBricks code: Apache 2.0; model: NVIDIA Open Model Agreement. Add-on: GPL-3.0-or-later; walker: Apache 2.0. README images shown: © NVIDIA, CC BY 4.0 (cropped): https://creativecommons.org/licenses/by/4.0/. Unofficial; not affiliated with NVIDIA.
코드·모델·애드온의 라이선스는 각각 다릅니다. 영상의 README 이미지는 © NVIDIA, CC BY 4.0이며 일부 잘랐습니다. NVIDIA와 제휴하지 않은 비공식 작업입니다.

Curated by @hyun2xyz

## Transcript

[   0.0] Zero motion data.
[   2.0] All this character was given is a T-Pode.
[   4.5] Today's open source project is Motion Bricks,
[   7.0] Nvidia's real-time motion model from SIGGRAPH 2026.
[  11.0] Show it where the character is now and where it should be next.
[  14.0] It draws every frame in between in about three milliseconds.
[  18.0] Its code is open source.
[  20.0] The model isn't open source, but you can use it, even commercially.
[  23.5] The sample motions are for evaluation only, so we use none of them.
[  27.5] We started from the T-Podes and the code,
[  29.5] asked for the same pose a little ahead,
[  31.5] and the model invented its own first steps.
[  34.0] On the SIGG-Zag, we keep placing the next pose one step ahead, in blue.
[  38.0] Before the character gets there, we place the next one.
[  40.5] We built a free Blender add-on that brings it in as a real character.
[  45.0] Everything you need along the way, from the code and demo files
[  48.0] to our own Blender add-on, is in the GitHub link.
[  51.0] Just give that link to a coding agent like Codex or Claude Code,
[  54.0] and you can use it right away.
[  56.0] The link is in the caption.
[  57.5] Thank you. Bye!

## On-screen text

NVlabs/motionbricks | Code Issues 9 Pull requests 2 Actions Projects Security Insights | motionbricks Public | Notifications Fork 42 | About | Official implementation of MotionBricks: Scalable Real-Time Motions with Modular Latent & Generative Model and Smart Primitives (SIGGRAPH 2026) | Readme License Contributing | MOTIONBRICKS | 1 token = 4 poses | README Contributing License Security | Citation | If you use this code in your research, please cite: | @article{yang2026motionbricks, title = {MotionBricks: Scalable Real-Time Motions with Modular Latent & Generative Model and Smart Primitives}, author = {...}, journal = {ACM Transactions on Graphics (TOG)}, year = {2026}, volume = {45}, number = {4}, doi = {10.1145/3011334}} | License | Code, documentation, models, and sample motions have different licenses: | README Contributing License Security | Documentation and media: NVIDIA-authored documentation text and media (images, screenshots, and videos, including the files in docs/media/) use Creative Commons Attribution (CC BY 4.0) | Models: NVIDIA Open Model Agreement. This covers the SOMA and G1 checkpoints on Hugging Face and the ONNX models. It permits commercial use and redistribution of modified models, subject to the agreement's terms. Licensed by NVIDIA Corporation under the NVIDIA Open Model Agreement. | Sample motions: NVIDIA Sample Data License. The covered human BVH and retargeted G1 CSV clips are for evaluating and testing NVIDIA technologies. The sample-data notice lists the covered files and credits Bones. These sample terms are separate from the model terms. | Licenses for dependencies and bundled robot assets are in licenses. Exporter dependency licenses are in tools/crmo/licenses. | This project downloads and installs additional components under their own license terms. Review those terms before use. | First steps | PS C:\tutorial> Expand-Archive motionbricks-blender-main.zip -DestinationPath . | PS C:\tutorial> dir .\motionbricks-blender-main\sources | Mode LastWriteTime Length Name | PS C:\tutorial> cd motionbricks-blender-main\sources | PS C:\tutorial> python .\motionbricks-blender.py | Code open source Apache 2.0 | hyun2xyz/motionbricks-blender | Code Issues Pull requests Actions Projects Security Insights | motionbricks-blender Public | Notifications Fork 0 | About | Free, unofficial Blender add-on: import NVIDIA MotionBricks motion as an animated character, plus a Scene Preview recorder | animation blender motion-editor motion-generation | Readme License | hyun2xyz/motionbricks-blender | main | motionbricks-blender / AGENTS.md | hyun2xyz and claude AGENTS.md: outline and track check on Windows | Preview Code Blame | Instructions for AI coding agents (Codex, Claude Code, and others) | @index.opensource | @hyun2xyz

## Key claims

- The character started from zero motion data, just a T-pose, with no motion clips used as input.
- MotionBricks is NVIDIA's real-time motion model, presented at SIGGRAPH 2026.
- The model connects the character's current pose to a target pose placed ahead, generating every in-between frame in about 3 milliseconds.
- MotionBricks' code is open source (Apache 2.0); the model itself is not open source but can be used, including commercially, under the NVIDIA Open Model Agreement.
- NVIDIA's sample motions are for evaluation only and were not used as inputs in this experiment.
- On a zigzag course, a new target pose (shown in blue) is continually placed just ahead of the character as it moves, driving continuous walking.
- A free, unofficial Blender add-on (GPL-3.0-or-later) was built to import the generated walk as an animated character.
- The tested workflow requires an NVIDIA RTX GPU, Windows or Linux, Blender 4.2+, and about 12 GB of disk space.
- Links to the add-on, project/demo, MotionBricks code, and paper are provided, and the link can be given directly to a coding agent like Codex or Claude Code to use the project.
- README images used are © NVIDIA under CC BY 4.0 (cropped); this project is unofficial and not affiliated with NVIDIA.

## Info channel

caption

## Mentioned (unverified hints)

- MotionBricks (NVIDIA): https://github.com/NVlabs/motionbricks
- MotionBricks paper: https://arxiv.org/abs/2604.24833
- motionbricks-blender (add-on): https://github.com/hyun2xyz/motionbricks-blender
- motionbricks-blender release v0.1.0: https://github.com/hyun2xyz/motionbricks-blender/releases/tag/v0.1.0
- Codex: (no url)
- Claude Code: (no url)
