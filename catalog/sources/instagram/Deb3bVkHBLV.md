reel: https://www.instagram.com/reel/Deb3bVkHBLV/
captured: 2026-10-27
yt-dlp: 2026.10.26
ffmpeg: 7.0.2-static
faster-whisper: 1.2.1
ctranslate2: 4.8.4
claude: 2.1.281 (Claude Code)

## Caption

Fit a wide picture into a narrower frame by removing low-energy pixel paths.

caire measures edges, finds a seam with one pixel in each row, removes it, then measures again. In this example, 568 seams reduce a program-generated landscape from 1960×896 to 1392×896. This can help adapt an image to a different layout or teach content-aware resizing.

The checked pagoda, house and pavilion regions lost no pixels in this run. That is specific to this image: parts of the trees did lose pixels. The process uses edge energy; it does not understand which objects matter.

caire calculated the seams, energy values and resized pixels. We added the color maps, enlarged pixel diagrams, labels, camera layout and ordinary-resize comparison.

넓은 그림에서 에너지가 낮은 픽셀 경로를 골라 지우면, 더 좁은 틀에 맞출 수 있어요.

caire는 가장자리를 바탕으로 에너지를 재고, 각 줄에서 픽셀 하나씩 지나는 이음선을 찾아 지운 뒤 다시 계산해요. 이번 예제에서는 프로그램이 그린 산수화에서 이음선 568개를 지워 1960×896을 1392×896으로 바꿨어요. 이미지의 가로세로 비율을 바꾸거나 내용 인식 리사이즈 원리를 배울 때 쓸 수 있어요.

이번 실행에서 확인한 탑·집·정자 영역은 지워진 픽셀이 없었어요. 모든 대상이 보존되는 것은 아니고, 나무 일부는 지워졌어요. 물체의 의미를 알아보는 대신 가장자리의 에너지를 계산해요.

이음선·에너지 값·리사이즈된 픽셀은 caire가 계산했어요. 색 지도, 확대 픽셀 도식, 이름표, 화면 배치와 일반 축소 비교는 저희가 덧붙였어요.

caire by Endre Simo · MIT
https://github.com/esimov/caire
Input painting: Shan Shui Infinite by Lingdong Huang · MIT
https://github.com/LingDong-/shan-shui-inf
Layout, color maps and explanatory graphics: @hyun2xyz
Curated by @hyun2xyz

#opensource #caire #seamcarving #creativecoding

## Transcript

[   0.0] Ever had to fit a wide picture into a narrow frame?
[   3.2] Squeezing it makes everything thin.
[   5.6] Today's open-source project cuts out the least noticeable pixels instead.
[  10.0] Care by Andrei Shimo.
[  12.2] First, it finds the edges.
[  14.4] Where the picture changes sharply, the energy is high.
[  17.6] Then it goes down the image row by row.
[  20.2] Each pixel adds the smallest total of the pixels just above it.
[  24.6] The lowest total in the bottom row is where the cheapest path ends.
[  28.8] Walking back up from there traces a seam.
[  31.8] One pixel in every row through the emptiest parts.
[  35.6] Remove it and the picture is one pixel narrower.
[  39.2] Then it measures the energy again and repeats hundreds of times.
[  43.4] The empty lake gets narrower while the pagoda and the houses don't lose a single pixel.
[  49.0] It's MIT-licensed. Use it, change it, even sell it.
[  52.8] Just keep the copyright and license notice.
[  55.2] Thank you. Bye.

## On-screen text

the picture: 1,960 x 896 | seams removed: 447 · width 1,513 px | caire | remove the seam: every row loses one pixel | width 1,960 px | energy measured again on the narrower picture | red: the 568 seams caire removed | esimov/caire | Code Issues Pull requests Actions Projects | caire / LICENSE | MIT License | Permissions: Commercial use, Modification, Distribution, Private use | Limitations: Liability, Warranty | Conditions: License and copyright notice | caire: carved to 1,392 x 896 | README License | Caire is a content aware image resize library based on Seam Carving for Content-Aware Image Resizing paper | How does it work | 504 func (p *Processor) shrink(img *image.NRGBA) (*image.NRGBA, error) { | 505 width, height := img.Bounds().Max.X, img.Bounds().Max.Y | 507 c := NewCarver(width, height) | 508 if _, err := c.ComputeSeams(p, img); err != nil { | 509 return nil, err | 511 seams := c.FindLowestEnergySeams(p) | 512 img = c.RemoveSeam(img, seams, p.Debug) | processor.go - esimov/caire@072a088 | caire's result: pagoda and houses, 0 pixels removed | caire - 1,960 x 896 | Thank you. 감사합니다. | @index.opensource | @hyun2xyz

## Key claims

- caire is a content-aware image resizing library that removes low-energy pixel seams to narrow an image without uniformly squeezing it
- It works by measuring edge energy, finding a seam of one pixel per row with the lowest cumulative energy, removing it, then recomputing energy and repeating
- In this example, 568 seams were removed to resize a 1,960×896 generated landscape down to 1,392×896
- The pagoda, house, and pavilion regions lost no pixels in this run, while parts of the trees did lose pixels
- The process is based purely on edge energy and does not understand which objects are semantically important
- The input image was a program-generated landscape (Shan Shui Infinite by Lingdong Huang)
- caire itself calculated the seams, energy values, and resized pixels; the color maps, enlarged pixel diagrams, labels, layout, and ordinary-resize comparison were added separately by the creators
- caire is MIT licensed, allowing commercial use, modification, distribution, and private use, provided the copyright and license notice are kept

## Info channel

on-screen

## Mentioned (unverified hints)

- caire: https://github.com/esimov/caire
- Shan Shui Infinite: https://github.com/LingDong-/shan-shui-inf
