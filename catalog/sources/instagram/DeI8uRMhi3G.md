reel: https://www.instagram.com/reel/DeI8uRMhi3G/
captured: 2026-10-27
yt-dlp: 2026.10.26
ffmpeg: 7.0.2-static
faster-whisper: 1.2.1
ctranslate2: 4.8.4
claude: 2.1.281 (Claude Code)

## Caption

Ultralytics YOLO — 5,040 guesses. 12 bird detections.

Ultralytics YOLO puts boxes, labels and scores on a frame. This example reports 5,040 prediction cells → 92 boxes above 0.25 confidence → 12 bird detections after NMS (IoU 0.7).

With Ultralytics 8.4.173 and yolo26l.pt, the default uses NMS. nms=False selects the NMS-free head; this frame returned 9 detections. These are one frame's results, not a benchmark or a guaranteed count.

5,040개의 추측에서 새 검출 12개까지.

Ultralytics YOLO는 프레임에 상자와 이름, 점수를 붙여요. 이번 예시에서는 5,040칸 중 신뢰도 0.25를 넘은 상자 92개를 NMS(IoU 0.7)로 정리해 새 검출 12개를 남겼어요.

사용한 8.4.173·yolo26l.pt의 기본 경로는 NMS를 써요. nms=False로 고른 출력부는 NMS 없이 9개를 냈어요. 한 프레임의 제작 기록이며, 성능 평가나 실제 개체 수를 보장하는 수치가 아닙니다. 화면의 클래스는 bird·zebra예요.

Code/models: Ultralytics · AGPL-3.0; Enterprise option. Check the terms for your use / 용도에 맞는 조건을 확인하세요.
https://github.com/ultralytics/ultralytics
https://www.ultralytics.com/license
YOLO paper: Redmon et al., 2015
https://arxiv.org/abs/1506.02640
Explainer graphics: @hyun2xyz

Footage / 원본 영상: Wikimedia Commons
JnpoJuwan · CC0
https://commons.wikimedia.org/wiki/File:Pigeon_feeding,_Jardim_da_Estrela,_2025_01.webm
Bamyers99 · Public domain
https://commons.wikimedia.org/wiki/File:Equus_quagga_(zebra)_suckling_video.ogv
Uusijani · CC0
https://commons.wikimedia.org/wiki/File:Giraffes_at_Artis.ogv
Ranch9613 · CC0
https://commons.wikimedia.org/wiki/File:2026_A_Bus_Dart_at_Parker_Rd_Plano_TX.webm
Seb35 · CC0
https://commons.wikimedia.org/wiki/File:A_grazing_horse_at_the_%C3%89comus%C3%A9e_de_la_Bintinais.webm
Drummyfish · CC0
https://commons.wikimedia.org/wiki/File:Seagull_Feeding_Young_Croatia.webm

Curated by @hyun2xyz

## Transcript

[   0.0] Today's open-source project is Ultralytics YOLO.
[   3.9] Show it any video and it boxes and names every object it knows, frame after frame.
[  10.1] YOLO stands for You Only Look Once. Joseph Redman introduced it in 2015
[  15.8] and we ran the newest version, YOLO 2.6. Each frame is shrunk to 640 pixels wide
[  23.3] and the network looks at it once. It answers on three grids from fine to coarse.
[  29.0] Every cell guesses one box, as distances from its center to the four edges,
[  34.2] plus a score for each of 80 kinds of things. That's over 5,000 guesses.
[  39.6] 92 of them say bird, with more than 25%. Many point at the same pigeon,
[  45.0] so YOLO keeps the best box and deletes boxes that overlap it too much.
[  49.6] 12 birds remain. YOLO 2.6 also has a second head that
[  54.2] learned to name each bird just once, so it can skip that cleanup at a small cost in accuracy.
[  60.2] Do this for every frame and the boxes follow along. The code and models are AGPL 3.0.
[  66.6] If you build them into a product or online service, you share your source too,
[  70.6] unless you get Ultralytics Enterprise License. Thank you. Bye.

## On-screen text

YOLO | Today's open-source project is Ultralytics YOLO: 오늘의 오픈소스는 Ultralytics YOLO에요. | arXiv Computer Science > Computer Vision and Pattern Recognition arXiv:1506.02640 (cs) You Only Look Once: Unified, Real-Time Object Detection Joseph Redmon, Santosh Divvala, Ross Girshick, Ali Farhadi View PDF HTML (experimental) We present YOLO, a new approach to object detection... | YOLO stands for You Only Look Once. YOLO는 You Only Look Once, '한 번만 본다'는 뜻이에요. | README Code of conduct Contributing License Security pip install ultralytics For alternative installation methods, including Conda, Docker, and building from source via Git, please consult the Quickstart Guide. CLI You can use Ultralytics YOLO directly from the Command Line Interface (CLI) with the yolo command: # Predict using a pretrained YOLO model (e.g., YOLO26n) on an image yolo predict model=yolo26n.pt source='https://ultralytics.com/images...' | and we ran the newest version, YOLO26. 저희는 최신 버전, YOLO26을 돌렸어요. | 1920 x 1080 | Each frame is shrunk to 640 pixels wide, 프레임을 가로 640픽셀로 줄이고, | bird 0.84 bird 0.72 bird 0.41 bird 0.81 bird 0.87 bird 0.84 bird 0.27 | ultralytics/ultralytics Code Issues Pull requests Discussions Actions GNU Affero General Public License v3.0 Permissions: Commercial use, Modification, Distribution Limitations: Liability, Warranty Conditions: License and copyright notice, State changes, Disclose source | Do this for every frame, 이걸 프레임마다 하면 | The code and models are AGPL-3.0. 코드와 모델은 AGPL-3.0이에요. | bird 0.86 bird 0.65 bird 0.88 bird 0.91 bird 0.70 | #2334455 | bus 0.94 | ultralytics source # cfg/default.yaml imgsz: 640 # [int | list] train/val use int (square); predict/export may use [h,w] # cfg/models/26/yolo26.yaml - [[16, 19, 22], 1, Detect, [nc]] # Detect(P3, P4, P5) # nn/modules/head.py self.nl = len(ch) # number of detection layers | horse 0.95 | bird 0.86 bird 0.85 | bird 0.86 bird 0.68 bird 0.88 bird 0.91 bird 0.70 | Thank you. 감사합니다. | @index.opensource @hyun2xyz

## Key claims

- Ultralytics YOLO boxes and names every object it recognizes in a video, frame by frame
- YOLO stands for 'You Only Look Once', introduced by Joseph Redmon in 2015
- The demo runs the newest version, YOLO26 (caption specifies Ultralytics 8.4.173 and yolo26l.pt)
- Each frame is resized to 640 pixels wide and processed in a single pass
- The model predicts on three grids (fine to coarse) and each cell predicts one box plus class scores for 80 classes, totaling over 5,000 guesses (5,040 prediction cells)
- 92 of the predicted boxes are labeled 'bird' with confidence above 25%
- Non-Maximum Suppression (NMS, IoU 0.7) removes overlapping duplicate boxes, leaving 12 bird detections
- YOLO26 has an NMS-free head option (nms=False) that names each object once, skipping NMS cleanup at a small accuracy cost; this returned 9 detections on the same frame
- These results are from a single frame, not a benchmark or guaranteed detection count
- The code and models are licensed under AGPL-3.0; using them in a product/online service requires sharing source code unless an Ultralytics Enterprise License is obtained

## Info channel

caption

## Mentioned (unverified hints)

- Ultralytics YOLO: https://github.com/ultralytics/ultralytics
- Ultralytics License: https://www.ultralytics.com/license
- YOLO paper (You Only Look Once: Unified, Real-Time Object Detection): https://arxiv.org/abs/1506.02640
