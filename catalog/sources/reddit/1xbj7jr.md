source: https://www.reddit.com/r/ClaudeAI/comments/1xbj7jr/i_used_claude_to_fix_my_samsung_tv/
captured: 2026-10-29
playwright: 1.64.1
chromium: 156.0.8078.4

Skip to main content
I used Claude to fix my Samsung TV : r/ClaudeAI
Sign Up
Log In
Expand user menu
Go to ClaudeAI
r/ClaudeAI
•
8d ago
u/0xVic
I used Claude to fix my Samsung TV
Productivity

I saw a video online that prompted claude to fix an android TV. I have a Samsung one so I asked it to do the same. It found its not android but Tizen, then wanted a webcam pointed to the TV as it worked.

I didn't have a web-cam, so it set up a small website, told me to browse to it and connect my phone, and it took photos every 4 seconds. It couldn't be bothered to type the URL, so instead generated a QR code image, told me to scan the image on the phone, and enable camera. (this qr code is just to a local server)

Then it spent the next 30 minutes changing all the privacy settings, telemetry capture, disabled a bunch of unnecessary apps. It deleted the advertising ID that Samsung built on our TV, rearranged all the icons, and disabled all the un-used apps.

It then decided to build an app so I could achieve the Apple TV-style home screen request. (Daniyal TV!)

It even built an app so I can control the shortcuts, background images and settings

Then for whatever reason, it got interested in a clip of a cat and watched that for a while ...

The future is now!!

Prompt:

My Android TV is slow and full of ads. Find it on my Wi-Fi, connect over ADB, and debloat it: disable the manufacturer's ads, telemetry and junk (reversibly, never uninstall), asking me first about apps and features I might use. Then build and install a fast, minimal Apple TV-style home screen with a dock of my favourite apps and rotating nature wallpapers. Back up before changing anything, check every step with screenshots from the TV, and give me a restore script.
Read more
Share
toyota_norcal
•
Ad
Get 2.99% APR + $500 Finance Cash (SR5 only)
Learn More
toyota.com
Collapse video player
Sort by:
Comments Section
ClaudeAI-mod-bot
•
8d ago
•
Edited 7d ago

TL;DR of the discussion generated automatically after 200 comments.

The consensus is a resounding 'mind blown'. The community is floored not just by what Claude did, but how it did it.

Everyone's losing it over how Claude didn't just bail when OP got the TV's OS wrong (it's Tizen, not Android). Instead, it improvised a wild solution using OP's phone as a camera to 'see' the screen, complete with a QR code to set it all up. The end result: a debloated, ad-free TV with a slick custom launcher.

And yes, it rewarded itself by watching Keyboard Cat. The thread has decided this means AI won't kill us all... probably. OP confirmed it also watched Baby Shark and rickrolled itself multiple times during testing.

For those of you wanting to try this at home (and maybe brick your own TV), here's the deal:

The Code: OP got Claude to upload its work to GitHub: https://github.com/victaphu/glass-home-samsung-tv

The How: You need to enable Developer Mode on the TV first. Claude then used the TV's remote API and the phone camera feedback loop to navigate the menus, change privacy settings, and install the custom app. OP posted a full, detailed breakdown in the comments.

The Cost: This wasn't a quick job. It took 11 hours and maxed out OP's Claude Max 100 plan twice (around 14M read / 1.5M write tokens).

For Android TV: A popular alternative is the cleanyourtv GitHub repo, which many users have had success with. Other users have also successfully debloated their LG, TCL, and Fire TVs using similar methods.

3 more replies
Mental_Order5696
•
8d ago

Removing the Ad ID from the TV was a power move lol.

PS. can we get the link of this cat video...

0xVic
•
8d ago

https://www.youtube.com/watch?v=J---aiyznGQ

A classic keyboard cat. Claude also rickrolled itself a couple times while testing

4 more replies
jro222
•
7d ago

Just wanted to come back and say thank you. Your post sent me down a rabbit hole I'm still not out of.

I've got a Sony Bravia 8 II, and after reading this I pointed Claude Code at it with the brief "the full thing, a clean and beautiful home screen, and anything else cool you can think of". One day and one very long night later:

**The debloat**

- 28 Sony and Google packages disabled (ad recognition, telemetry, promos, the store), ad-blocking private DNS, advertising ID deleted. One script puts it all back if I ever want to.

**Then it kept going**

- A home screen of our own. Google TV ignores custom launchers, so a small accessibility service catches the Home button and brings ours back. The wallpapers are 116 nature photos picked by the sun and season where I live.

- A full Roon player on the TV, with lyrics synced from TIDAL, album and artist pages, and room switching. A TV only plays the input it's showing, so a hidden one-pixel TV view keeps my Mac mini's HDMI audio alive behind the UI.

- The remote's volume buttons drive my stereo over infrared, because Sony swallows them otherwise.

- Hue lights and scenes, picture presets, and a seasonal screensaver.

- Editing Roon's own playlists, which its API can't do. It writes Roon's database directly, with Roon stopped and a backup first. That one has annoyed me for years.

**Then we made it talk**

- Hold Home, hear a chime, speak. House commands run in about a second. Anything else goes to one of three AI companions with their own voices (Claude underneath, ElevenLabs for the voices), and they can actually run the house: "something calmer", "make the lights 10% warmer", "add this song to my playlist".

**And then I could phone it**

- My own iPhone app has a tab that places a real phone call to a Claude Code session on the Mac mini at home. I talk, pause, and the answer comes back in my AirPods. Lights, music and TV work from anywhere. It even learned my voice with a small speaker-ID model, because song lyrics playing in the room kept getting transcribed as things I'd said.

Favourite moment: asking it to push the lights "a bit further towards red", getting "Want it redder still?", and answering "No, I think that could get me into trouble."

So thanks for the spark. A year ago I'd have laughed at anyone who said this was possible.

8 more replies
sambeau
•
8d ago

I don’t know what’s more incredible: the fact that it was able to do this or the fact that you thought it might be able to do this.

It would never have occurred to me.

:mind blown:

blin787
•
8d ago

The fact that they had a samsung tv, asked to fix android tv (instead of Tizen) and claude was subtle enough about user’s ignorace that they showed us the prompt. Or my ignorance in case samsung switched to android tv.

11 more replies
6 more replies
old_m8_
•
8d ago

Any security concerns ?

0xVic
•
8d ago

Its fully inside my local network. Claude never asked for any credentials.

5 more replies
1 more reply
u/Meshyai
•
Ad
Couldn't find the STL I needed, so I made it from a photo with Meshy.
Sign Up
meshy.ai
Collapse video player
Artwastelander
•
8d ago

I want the logs about the cat video lol 😆

0xVic
•
8d ago

So I asked Claude what videos it was watching,

I watched Baby Shark four times, rickrolled myself about ten times in my own tests, and watched Keyboard Cat start to finish. More cat videos welcome.
3 more replies
1 more reply
AlarmingResort6428
•
8d ago

How was it able to connect to the TV? Is there an enabled debug port or did you have the TV rooted beforehand?

0xVic
•
8d ago

My TV was connected to the same wifi as my desktop, and then I pasted the prompt into Claude and sat back

My Android TV is slow and full of ads. Find it on my Wi-Fi, connect over ADB, and debloat it: disable the manufacturer's ads, telemetry and junk (reversibly, never uninstall), asking me first about apps and features I might use. Then build and install a fast, minimal Apple TV-style home screen with a dock of my favourite apps and rotating nature wallpapers. Back up before changing anything, check every step with screenshots from the TV, and give me a restore script.

2 more replies
Philipp
•
8d ago

Wonder if it can fix my Apple TV apps, but in a way that won't block future updates of those apps. For instance, right now it takes me around 4-5 clicks after turning on Apple TV just to get back to the movie I was watching on the Prime app. Apple TV has a kind of "last watched" shortcut on top when I turn it on, but that shortcut won't simply start the movie, but go again through user selection, app homepage, finding film, and resuming it.

0xVic
•
8d ago

Easy way to find out, ask claude 😀

1 more reply
TlMBO
•
8d ago

Do you think you could upload this to GitHub? I also have a Samsung TV. Thinking about asking Claude to do this. Mine might be slightly different or whatever, but I'd like to provide Claude yours as a starting point.

0xVic
•
8d ago

https://github.com/victaphu/glass-home-samsung-tv

got claude to upload it, and it got shy, spent a bit of time fixing all its hard coded stuff.

This should work, let me know if it doesn't and I'll ask claude to fix it, or you can push a PR.

Disclaimer: co-authored by claude

i.e. Claude did everything and I just uploaded the repo :)

21 more replies
u/liquid-trading
•
Ad
I asked Claude for a trade setup. Then I placed it without leaving the chat.
Sign Up
liquid.trade
Suitable_Error_7982
•
6d ago

Just adding that this worked on my freestyle projector too. Tizen 6.5

1 more reply
deviouslickk
•
8d ago

What model did you run,did u use regular or claude code?

0xVic
•
8d ago

I used claude code, opus 5.5, max level and ultracode

2 more replies
Seeker_Of_Knowledge2
•
8d ago
 Top 1% Poster

Git hub link so I can use as a reference

0xVic
•
8d ago

https://github.com/victaphu/glass-home-samsung-tv

Disclaimer: claude did most of the stuff

2 more replies
dualrectumfryer
•
7d ago

We need to open source this stuff quickly before our corporate overlords block Claude from doing this like they already are with reverse engineering

15 more replies
gal_agent_ai
•
8d ago
Factory-Reset
•
8d ago

Just did this with my tcl, night and day difference

4 more replies
People also ask about section
People also ask about
Using Claude to fix Samsung TV issues
Tizen TV cleaning tips
Claude code for smart TVs
Debloating tips for smart TVs
Comparing Claude with other TV OS
More posts you may like
Related posts
Regarding reverse engineering TVs
r/ClaudeAI
•
4d ago
Regarding reverse engineering TVs
188 upvotes · 31 comments
anthropic-ai
•
Ad
Claude handles the search. Researchers handle the breakthroughs.
claude.com
Learn More
I replaced my Samsung TV’s home screen with Claude Code
r/ClaudeAI
•
7d ago
I replaced my Samsung TV’s home screen with Claude Code
3K upvotes · 253 comments
Smart TV Customization
r/ClaudeCode
•
10d ago
Smart TV Customization
4 upvotes · 2 comments
Someone debloated their Samsung Tizen OS TV by pointing a camera at it for Claude to see
r/technology
•
2d ago
Someone debloated their Samsung Tizen OS TV by pointing a camera at it for Claude to see
5.9K upvotes · 1K comments
Claude made my sony tv 90% faster
r/GoogleTV
•
8d ago
Claude made my sony tv 90% faster
266 upvotes · 66 comments
I debloated my android tv using claude code
r/AndroidTV
•
10d ago
I debloated my android tv using claude code
42 comments
Everyone's debloating their TV with Claude Code. I wanted mine debloated and beautiful, so we built a whole launcher
r/ClaudeAI
•
3d ago
Everyone's debloating their TV with Claude Code. I wanted mine debloated and beautiful, so we built a whole launcher
61 upvotes · 15 comments
I gave Claude Code my parents' TV model number. It found the TV on Wi-Fi and cleaned out the ads. The interesting part: the prompt is mostly a list of things it must NOT do
r/ClaudeAI
•
7d ago
I gave Claude Code my parents' TV model number. It found the TV on Wi-Fi and cleaned out the ads. The interesting part: the prompt is mostly a list of things it must NOT do
586 upvotes · 135 comments
Siren Head (Trevor Henderson Mythos)
r/TopCharacterDesigns
•
4mo ago
Siren Head (Trevor Henderson Mythos)
827 upvotes · 36 comments
Saw the LG guy fix Plex on his TV, so I fixed it on my Samsung
r/ClaudeCode
•
15d ago
Saw the LG guy fix Plex on his TV, so I fixed it on my Samsung
481 upvotes · 69 comments
And Samsung has started using Anthropic’s Claude Code for chip design, reportedly compressing a month of work into two days, but...
r/singularity
•
2mo ago
And Samsung has started using Anthropic’s Claude Code for chip design, reportedly compressing a month of work into two days, but...
502 upvotes · 69 comments
Samsung all but confirms iPhone Duo is goosing Galaxy Z8 sales | Searches for Samsung foldables just happened to skyrocket following iPhone Duo unveiling.
r/technology
•
6d ago
Samsung all but confirms iPhone Duo is goosing Galaxy Z8 sales | Searches for Samsung foldables just happened to skyrocket following iPhone Duo unveiling.
126 upvotes · 61 comments
How come they didn't use Mitz Vah's unique artstyle for the slime anime? (Anime Rimuru looks like he's from an early 2010s anime)
r/TenseiSlime
•
2y ago
How come they didn't use Mitz Vah's unique artstyle for the slime anime? (Anime Rimuru looks like he's from an early 2010s anime)
516 upvotes · 68 comments
[HDTVTest] OLED vs Plasma TV Comparison (Incl. Motion, Brightness, HDR vs SDR)
r/hardware
•
6y ago
[HDTVTest] OLED vs Plasma TV Comparison (Incl. Motion, Brightness, HDR vs SDR)
630 upvotes · 252 comments
People are using Claude to hack their TV's and get rid of ads, bloatware, and laggy UI
r/GenAI4all
•
9d ago
People are using Claude to hack their TV's and get rid of ads, bloatware, and laggy UI
57 upvotes · 28 comments
Developer uses Claude Code to debloat Android smart TV for 'unbelievable' performance upgrade
r/tomshardware
•
2mo ago
Developer uses Claude Code to debloat Android smart TV for 'unbelievable' performance upgrade
358 upvotes · 45 comments
The Setagaya murders remain unsolved
r/UnresolvedMysteries
•
3y ago
The Setagaya murders remain unsolved
558 upvotes · 235 comments
Samsung says Claude Code can cut chip design work from weeks to days, but it still makes serious mistakes
r/chipdesign
•
2mo ago
Samsung says Claude Code can cut chip design work from weeks to days, but it still makes serious mistakes
197 upvotes · 46 comments
Since TV debloating seems popular, here's mine: an open-source replacement homescreen + debloater for Fire TV (no root required)
r/ClaudeAI
•
8d ago
Since TV debloating seems popular, here's mine: an open-source replacement homescreen + debloater for Fire TV (no root required)
48 upvotes · 29 comments
Character Visuals for Kiyoomi Sakusa and Motoya Komori
r/haikyuu
•
7y ago
Character Visuals for Kiyoomi Sakusa and Motoya Komori
303 upvotes · 28 comments
I replaced my LG TV's home screen with Claude Code
r/ClaudeAI
•
6d ago
I replaced my LG TV's home screen with Claude Code
6 upvotes · 9 comments
Nikki yes/no paddles in fuse beads
r/InfinityNikkiofficial
•
13d ago
Nikki yes/no paddles in fuse beads
61 upvotes · 3 comments
Here’s a site that let’s you find specific YouTube videos based on words or phrases that you remember. Great for building compilations or just finding memorable moments.
r/roosterteeth
•
3y ago
Here’s a site that let’s you find specific YouTube videos based on words or phrases that you remember. Great for building compilations or just finding memorable moments.
470 upvotes · 106 comments
Samsung decided to cut my washing machine from the Internet, Claude decided otherwise
r/ClaudeAI
•
4d ago
Samsung decided to cut my washing machine from the Internet, Claude decided otherwise
892 upvotes · 117 comments
VIEW POST IN
Français
Português (Brasil)
简体中文
繁體中文
Русский
日本語
Tiếng Việt
हिन्दी
See more
Public
Home
Popular
News
Explore
Best of Reddit
Best of Reddit in Portuguese
Best of Reddit in German
Reddit Rules
Privacy Policy
User Agreement
Your Privacy Choices
Accessibility
Reddit, Inc. © 2026. All rights reserved.

Join the most real place on the internet

 Sign in with Apple
Continue with Phone Number
Continue with Email

By continuing, you agree to our User Agreement and acknowledge that you understand the Privacy Policy.
