reel: https://www.instagram.com/reel/DeecMf9nBBn/
captured: 2026-10-27
yt-dlp: 2026.10.26
ffmpeg: 7.0.2-static
faster-whisper: 1.2.1
ctranslate2: 4.8.4
claude: 2.1.281 (Claude Code)

## Caption

Demucs separates a song into drums, bass, vocals, and the rest.

We ran its htdemucs model on Josh Woodward’s “Knock.” The video plays each separated track, then compares the estimated accompaniment with the instrumental version the musician released.

Inside, Demucs reads the same sound as a waveform and a spectrogram. Both branches compress the input, exchange information through a transformer, and expand it back into four tracks. Their estimates are added together.

The sounds are actual Demucs outputs. We made the visualizations from the audio and the model’s internal values. Some sound still leaks between tracks.

Which part would you listen to first: the bass line, the drum pattern, or the vocal?

Demucs는 노래 한 곡을 드럼, 베이스, 보컬, 나머지 소리로 나눠 줍니다.

Josh Woodward의 “Knock”을 htdemucs 모델로 분리했어요. 영상에서 각 트랙을 하나씩 듣고, Demucs가 추정한 반주를 작가가 공개한 반주판과 비교합니다.

Demucs는 같은 소리를 파형과 스펙트로그램, 두 방식으로 읽어요. 두 갈래가 입력을 압축하고, 트랜스포머로 정보를 주고받은 뒤 다시 네 트랙으로 펼칩니다. 마지막에는 두 갈래의 추정값을 더해요.

들리는 소리는 실제 Demucs 출력입니다. 소리와 모델 내부 값을 읽어 시각화했어요. 트랙 사이에 다른 소리가 일부 남기도 합니다.

베이스 라인, 드럼 패턴, 보컬 중 어떤 소리부터 따로 들어 보고 싶으신가요?

## Transcript

[   0.0] Ever wondered how an app can pull the voice out of any song?
[   4.0] Today's open source project does exactly that.
[   7.5] Demukes by Alexandra Defosse.
[  10.5] Give it any song, and it hands back four tracks.
[  13.5] Drums, bass, vocals, and everything else.
[  18.0] Listen.
[  19.5] Drums, bass, vocals, and the rest.
[  27.5] A song arrives as one single wave.
[  30.0] Every instrument added together.
[  32.0] Demukes reads it two ways at once.
[  34.0] The raw wave and a spectrogram.
[  36.5] A picture of which pitches sound when.
[  39.5] Each branch squeezes the sound down layer by layer.
[  43.0] In the middle, a transformer lets the two branches compare notes.
[  47.0] Then both grow back out into four tracks, and their two answers are added together.
[  52.0] It learned all this from hundreds of songs whose instruments were recorded separately.
[  56.5] Josh Woodward, who made this song, also released it without vocals.
[  60.5] Here's his version.
[  62.5] And here's Demukes' guess.
[  65.5] Demukes is MIT licensed.
[  67.5] Use it, change it, share it, and keep the notice.
[  71.5] Thank you.
[  72.5] Bye.

## On-screen text

a song | 2883f3d demucs README.md Preview Raw uvx demucs PATH_OF_AUDIO_FILE_1 [PATH_OF_AUDIO_FILE_2 ...] # for Demucs | uvx demucs --mp3 --mp3-bitrate BITRATE PATH_OF_AUDIO_FILE_1 # output fi | # use --mp3-preset to change encoder preset, 2 for best quality, | # If your filename contain spaces don't forget to quote it !!! | uvx demucs "my music/my favorite track.mp3" | # You can select different models with '-n', mdx_q is the quantized mode | # Note that the quantized models require the quantized extra. | uvx "demucs[quantized]" -n mdx_q myfile.mp3 | # If you only want to separate vocals out of an audio, use --two-stems= | uvx demucs --two-stems=vocals myfile.mp3 | If you have a GPU, but you run out of memory, please use --segment to reduce the length of each split. SEGMENT should be changed to a integer describing the length of each segment in seconds. A segment length of at least 10 is recommended (the bigger the number is, the more memory is required, but quality may increase). Note that the Hybrid Transformer models only support a maximum segment length of 7.8 seconds | his instrumental | Josh Woodward released it himself | Wikimedia Commons File:Josh Woodward - 04 - Knock Instrumental Version.ogg Discussion TimedText Download Use this file Edit View history Email a link Information File information Structured data Original file (Ogg Vorbis sound file, length 2 min 54 s, 201 kbps, file size: 4.16 MB) | Ever wondered how an app can pull the voice out of any song? 앱은 어떻게 아무 노래에서나 목소리만 쏙 뽑아낼까요? | Give it any song, and it hands back four tracks: 노래 한 곡을 넣으면 트랙 네 개를 돌려줘요. | Josh Woodward, who made this song, 이 노래를 만든 Josh Woodward는 | Here's his version. 이건 그의 버전이고 | song | one song in Knock.ogg | the song (with voice) | his instrumental | Demucs's guess | song: "Knock" by Josh Woodward - CC BY 4.0

## Key claims

- Demucs separates a song into four tracks: drums, bass, vocals, and everything else
- The reel uses Demucs's htdemucs model on Josh Woodward's song 'Knock'
- Demucs is made/authored by Alexandre Défossez
- Demucs reads the audio two ways at once: as a raw waveform and as a spectrogram
- Each branch compresses the input, the two branches exchange information through a transformer, then both expand back into four tracks, and their estimates are added together
- Demucs was trained on hundreds of songs whose instruments were recorded separately
- Josh Woodward released his own instrumental (vocal-free) version of 'Knock', which is used for comparison against Demucs's estimated instrumental
- Demucs is MIT licensed
- The audio outputs played are actual Demucs outputs; the visualizations were created from the audio and the model's internal values
- Some sound still leaks between the separated tracks

## Info channel

spoken

## Mentioned (unverified hints)

- Demucs: (no url)
