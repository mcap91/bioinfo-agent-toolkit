reel: https://www.instagram.com/reel/De5smNojeZm/
captured: 2026-10-29
yt-dlp: 2026.10.26
ffmpeg: 7.0.2-static
faster-whisper: 1.2.1
ctranslate2: 4.8.4
claude: 2.1.281 (Claude Code)

## Caption

Your slow Android TV is probably full of apps you never asked for. Here's every step to fix it. 📺

People are using Claude Code to switch off bloat, ad rows and trackers on Android TV and Google TV over ADB, with no root. Everything is disabled, not deleted, so it can be undone. The catch: one user bricked a TV, you lose whatever you switch off, and 1 GB TVs may not speed up much.

Would you let an AI tune your TV, or never risk it? 👇
Comment PROMPT and I'll send you the exact one.

Sources: TechCrunch, It's FOSS, Tom's Hardware, github.com/Gathin23/cleanyourtv, github.com/humblemuzzu/dumbtv, developer.android.com, code.claude.com
Original animation. Not affiliated with Google, Anthropic or Amazon.

#AndroidTV #GoogleTV #ClaudeCode #SmartTV #TechTips #AI #LearnTech

## Transcript

[   0.0] People are letting Claude fix their slow Android TVs, and some say it's smoother than new.
[   5.6] Real speed up or risky hack, here's every step.
[   9.3] Many budget TVs have just 1 to 2GB of RAM, and ship full of pre-installed apps, add rows
[  14.2] and trackers.
[  15.2] Some even fingerprint your screen to sell ads.
[  18.2] You need a TV, a laptop on the same Wi-Fi, and 15 minutes.
[  22.2] It works on Android TV and Google TV, not Samsung, LG or Roku.
[  27.8] Step 1.
[  28.8] On the TV, open Settings, Device Preferences about.
[  32.4] Press OK on Build 7 times.
[  34.8] Your developer.
[  36.3] Step 2.
[  37.3] In Developer Options, turn on USB debugging, plus network debugging if you see it.
[  42.8] Step 3.
[  43.8] In your Wi-Fi settings, note the TV's IP address.
[  47.8] Step 4.
[  48.8] On your laptop, install Android's free platform tools.
[  52.0] That's ADB, Google's tool for sending commands to a device.
[  56.0] Then install Claude code and sign in.
[  58.8] Step 5.
[  59.8] Tell Claude your TV model and IP, and ask it to connect over ADB.
[  64.2] Be specific.
[  65.2] Hack my TV can get refused.
[  67.8] Step 6.
[  68.8] The TV asks, allow debugging.
[  70.7] Press Allow.
[  71.7] Only computers you approve get in.
[  73.8] Step 7.
[  74.8] Have Claude back up the full app list in Settings and write a restore script.
[  78.5] That's your undo button.
[  80.3] Step 8.
[  81.3] Claude sorts every app.
[  82.6] Tracking.
[  83.6] Ads.
[  84.6] Background extras.
[  85.6] And the apps you use.
[  87.3] You pick what stays.
[  88.8] Step 9.
[  89.8] It switches the extras off with PM Disable User.
[  93.0] Disabled.
[  94.0] Not deleted.
[  95.0] So you can undo it anytime.
[  97.3] Step 10.
[  98.3] It presses remote buttons and screenshots the TV to check each change.
[ 103.2] On top of that, lower the animation scales in Developer Options.
[ 107.0] Lower means faster.
[ 108.8] Swap the heavy home screen.
[ 110.4] One user went from a 192 megabyte launcher to an 83 megabyte one and disabled 25 bloat
[ 116.5] apps.
[ 117.5] Gathen built Clean Your TV with Claude code in an afternoon for his parents TV, a light
[ 122.6] home screen made for 1 gigabyte TVs.
[ 126.2] On Fire TV, Dumb TV disables about 50 Amazon ad and tracking packages and blocks about
[ 132.4] 400 tracking addresses.
[ 134.1] One script undoes it all.
[ 136.2] You can also switch off Ad Tracking and Autoplay.
[ 139.6] To catch, one user bricked their TV.
[ 142.3] Uninstalling the wrong system app can break home or HDMI, so only disable and install
[ 147.5] the new launcher before removing the old one.
[ 150.3] Whatever you switch off is gone, like voice search or updates.
[ 153.6] On a 1 gigabyte TV, gains may be small and turn debugging off when you're done.
[ 159.2] Claude code asked before each command.
[ 161.5] Read it before you press yes.
[ 163.7] So would you let an AI tune your TV or never risk it?
[ 167.4] Comment below.
[ 168.6] What my exact prompt?
[ 170.1] Comment prompt and I'll reply.
[ 171.8] Save this and follow for one tech idea a day.

## On-screen text

SPONSORED | YOU NEED THE TV A LAPTOP 15 MIN Internet erences WORKS ON ANDROID TV GOOGLE TV NOT SAMSUNG LG ROKU | Many budget TVs have just | 02 STEP 1 UNLOCK DEVELOPER Settings > Device Preferences > Device name Android TV OS 12 Build tap Status You are now a developer! PRESS OK x7 you're a developer. | 03 STEP 2 TURN ON DEBUGGING Developer options Stay awake Home Wi-Fi USB debugging Good Network debugging IP address 192.168.1.42 Window animation scale 1x USB + NETWORK NO WIRELESS TOGGLE? USB MAY BE ENOUGH | 04 STEP 3 FIND THE TV'S IP Wi-Fi Network Signal strength Good IP address 192.168.1.42 Proxy settings 192.168.1.42 EXAMPLE · YOURS WILL DIFFER | 05 STEP 5 CONNECT · TELL CL... CLAUDE CODE > My TV is a [model]. Connect over ADB and back... $ adb connect 192.168.1.42:5... hack my TV CAN GET REFUSED BE SPECIFIC Step six. | 06 STEP 6 APPROVE IT ON THE... Allow USB debugging backu only computers you approve. | 07 STEP 7 BACK UP FIRST restore.sh your undo button. | 10 STEP 10 CHECK EVERY CHANGE KEYEVENT → TV screen.png | ON TOP OF THAT LOWER ANIMATION SCALES · 1x LOWER = FASTER | A LIGHTER HOME SCREEN 25 BLOAT APPS OFF OR: PROJECTIVY · FLAUNCHER · ATV | WHAT OTHERS BUILT 1 AFT... Good evening 8:42 FOR 1 GB TVS A DOCK · A GRID · NO VIDEO · NO BLUR | LET AI TU... RI... Want my exact prompt?

## Key claims

- Budget Android TVs often have just 1-2GB RAM and ship full of pre-installed apps, ad rows and trackers, some fingerprinting the screen to sell ads
- You can use Claude Code over ADB (no root) to disable bloatware, ad rows and trackers on Android TV/Google TV
- This works on Android TV and Google TV, not Samsung, LG, or Roku
- The process requires a TV, a laptop on the same Wi-Fi, and about 15 minutes
- Apps are disabled via 'pm disable-user', not deleted, so changes can be undone
- Claude Code backs up the full app list and writes a restore.sh script as an undo button
- Claude Code checks each change by pressing remote buttons and taking screenshots
- Lowering animation scales in Developer Options makes the TV feel faster
- One user swapped a 192MB launcher for an 83MB one and disabled 25 bloat apps
- Gathin built 'Clean Your TV' with Claude Code in an afternoon, a light home screen for 1GB TVs
- 'Dumb TV' disables about 50 Amazon ad/tracking packages on Fire TV and blocks about 400 tracking addresses, with one script to undo everything
- One user bricked their TV during this process
- Uninstalling the wrong system app can break the home screen or HDMI; recommendation is to disable and install a new launcher before removing the old one
- Whatever is switched off is lost until restored, including features like voice search or updates
- Gains may be small on 1GB RAM TVs
- Claude Code asks for approval before each command, so users should read commands before approving
- Users should turn off USB/network debugging when finished

## Info channel

spoken

## Mentioned (unverified hints)

- Claude Code: code.claude.com
- ADB (Android Debug Bridge / Android platform tools): developer.android.com
- Clean Your TV: github.com/Gathin23/cleanyourtv
- Dumb TV: github.com/humblemuzzu/dumbtv
- restore.sh: (no url)
- Projectivy: (no url)
- Flauncher: (no url)
- ATV: (no url)
