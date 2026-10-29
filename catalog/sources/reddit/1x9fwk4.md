source: https://www.reddit.com/r/ClaudeCode/comments/1x9fwk4/comment/phmsw9i/
captured: 2026-10-29
playwright: 1.64.1
chromium: 156.0.8078.4

Skip to main content
The world has changed : r/ClaudeCode
Sign Up
Log In
Expand user menu
Go to ClaudeCode
r/ClaudeCode
•
10d ago
u/Imaginary_Data_708
The world has changed
Built with Claude

Opus 5.5 suggested I get a web cam pointed at this ESP32 based screen so it could catch what was happening on the screen as it tried to find out what the maximum frame rate could be. The Waveshare drivers are not good in portrait mode and only got 4fps.

It got to 60fps in a couple of minutes.

It had already installed the tool chain, designed the clock layout etc.

It's not the code per se. It's the get a webcam suggestion...

What a time to be alive!

Share
Sort by:
Comments Section
Bloated_Plaid
•
10d ago
•
Edited 10d ago
 Top 1% Poster

Fuck yea man. I just debloated my old LG TV and removed all the telemetry and made it like 10x faster using Opus, also made a fully web based remote so that I don’t have to use their stupid app either. Just fucking magic and most of the world has no fucking idea. It’s a fucking superpower. I can basically just prompt to Claude to keep optimizing till it’s happy and it will go off and do it.

Edit - For those unaware, extensive report from GamerNexus on LGs surveillance system using their TVs, https://youtu.be/6IFVTcM28KA. It’s wild.

Edit 2 - This is my prompt sanitized after the TV was rooted

I have a rooted LG webOS TV (Homebrew Channel installed, root shell over SSH or telnet at [TV IP]).

Make it as lean and fast as possible: remove the bloat entirely, rather than hiding it, and give it a

much lighter, extremely responsive launcher. Use the ideas in

https://gist.github.com/lucataco/7c303b443934008a9031a55cfca552ec as a starting point, but go further:

where that script hides apps, actually remove as much as the firmware safely allows.

What I use (keep these, everything else can go):

- Apps: [e.g. Plex client, YouTube]

- Inputs: [e.g. HDMI 1 = Apple TV, HDMI 3 = Xbox]. Rename the inputs to match.

- Keep these TV features working exactly as they are: HDMI inputs, ARC/eARC and CEC, [AirPlay, screen casting].

- [I don't use the antenna or Live TV.]

Privacy and updates:

- Block LG firmware updates for good (an update can also undo the root).

- Turn off and block LG's data collection: Live Plus/ACR, viewing data, ads, recommendations, diagnostics.

Keep the internet working for the apps I use.

The launcher:

- Pressing Home should open a launcher with only my apps and inputs, in well under a second.

- Back should return to whatever I was watching.

- Keep a way back to LG's original home screen in case something breaks.

How to work:

- Inventory and measure first (apps, background services, memory, how long Home and app launches take),

so you can show what got better.

- Make every change reversible and back up anything you modify. Never touch the firmware partitions.

- Change in small batches, and reboot and re-check after each one. Undo a batch that breaks anything

before starting the next.

- Keep the TV from going to sleep while you work, then put my power settings back afterwards.

- You can install a startup script on the TV to make the changes stick across reboots.

- Keep looping until it meets your own bar for performance and polish, and you'd expect me to approve

it. Then tell me it's ready, with before/after numbers and anything you couldn't verify.

- Write a handoff so a future session can pick up where you left off.

Reply
Share
MaxLo85
•
10d ago

These are my exact words to people right now. I feel like I have fucking superpowers and I'm in a race to do something amazing with them before the rest of the world realizes they also have literal fucking superpowers available to them

Reply
Share
doiveo
•
9d ago

As much as I agree, the above is outside the comprehension and/or interest of 95% of the world.

We (this sub) live in a bubble where everyone is comfortable with command line and hacking stuff is normal.

My family thinks I'm an alien if I show them a <body> tag.

Reply
Share
11 more replies
Sick-Little-Monky
•
10d ago

Just wait till they start charging the actual cost of those superpowers.

14 more replies
KenMantle
•
10d ago

...or the free AI lunch becomes expensive. I've been in build mode for almost a year now extracting as much value as I can. If AI cost 10x what it does now I have the base built for a lot of apps I use and it would still be affordable to do maintenance or small upgrades on them.

1 more reply
4 more replies
untracked5465
•
10d ago

Hey, great idea, can you share how you did it? I'm planning to do the same with my Samsung

Bloated_Plaid
•
10d ago
 Top 1% Poster

Depends on what OS your tv is on, I don’t think Tizen has root access available but you can still try. There might be a developer option you can enable and at least minimize the bloat. My LG TV was from 2018 and had an easy way to get root access.

1 more reply
pinescorpion
•
10d ago

Did removing telemetry itself make the TV faster or did it do some other stuff?

Delyzr
•
10d ago

It installed its own spyware and is now using OPs TV to find the smoking gun

3 more replies
spiritzzz
•
9d ago

Hell yeah, I just made this quick to improve mine some more: https://github.com/Arnedeklerk/PearWebOS/

Bloated_Plaid
•
9d ago
 Top 1% Poster

F YEA BROTHER, congrats!

_Playniac
•
10d ago

Did the same. Best decision of my life. Don't even know what it did. Don't care either. Its a Blackbox now, but its fast and doesn't sent 5 terabytes of data in one day anymore so im happy lol

1 more reply
Fuzzy_Independent241
•
10d ago

Question: do you have a repo with either the code or a how to? I was thinking about that but I'm still afraid of messing up with hardware/firmware. Tks

Bloated_Plaid
•
10d ago
 Top 1% Poster

The actual rooting stuff can be found here

https://www.webosbrew.org/rooting/

and easy to do yourself. I added my original prompt as an edit.

2 more replies
[deleted]
•
10d ago
Secret_Tap_1969
•
8d ago

I was attempting to do this exact same thing but the constant safeguards triggering a model downgrade became unbearable...how did you work around that? Dm me please

2 more replies
elsteef
•
6d ago

This is the most useful reddit posts that I have seen this year. Thanks for taking the time and energy to post it.

Ok-Dark7871
•
4d ago

I root my car ihu , and install google map without the use of android auto.

victorsaurus
•
10d ago

How do you do that? You install claude in the tv and it edits the OS or what? I want to do the same.

WeatherJazzlike8376
•
10d ago

Depends on your tv ks version, I did  it with Hermes. My version was easy, just open a GitHub link on chrome, put in the tv ip and klick “root” afterwards I installed “glassdoor” (for privacy telemetry) took me like 5 min.

https://azoffshowy.github.io/dangbro/

3 more replies
tehsilentwarrior
•
9d ago

I had mine connect to the a chrome cast using the wireless debug dev feature and configure Nuvio for me from a guide I found online.

Then asked it to create two profiles, one for us and one for the kids. Then find out what ever movies and such were all the rage for kids 6/7 year old, list them by rank and add the top 50.

Made it double check the ACTUAL playback of each to guarantee it’s not just stale metadata and to guarantee they have subtitles and the sound is dubbed to Portuguese Portugal not Portuguese Brasil. Also limit the sources to just good enough quality not ultra high not super low and auto select the first entry so that kids can just choose something quick.

Told it to keep a record of all knowledge and such in a list of steps, self correcting as it went so that I could just replicate it later.

Oh and remapped the buttons on my remote from YouTube to some custom player without ads and from Netflix to Nuvio

erikerikerik
•
9d ago

I too hand found that a handoff.MD is amazing and really useful.

Bulky-Condition-3490
•
9d ago
•
Edited 9d ago

Beautiful prompt, thanks, running it right now.

How did you get past safeguarding tho?
EDIT: Just do the root yourself and make sure claude opus knows that you are NOT asking it to root the TV. Get it to the point where dev tools are uninstalled and homebrew is open with updates blocked and SSH on, then you can prompt it.

Sonnet 4.6 is the only one that will attempt to do stuff but that model is ancient now so.. nah

Tritheone69
•
10d ago

Hi! I’ve been wanting to do this since a few people are talking about their success.

Did you connect to the TV using a USB cable or is their a way to connect to it via an endpoint?

1 more reply
58 more replies
AutoModerator
•
10d ago
People also ask about section
People also ask about
Overview of ESP32 and ClaudeCode
Tips for monitoring ESP32 usage
ESP32 performance issues in portrait mode
Innovative projects using Claude code
Best practices for coding with AI
More posts you may like
Related posts
New World: Aeternum Private Server Progress — Character Creation, Combat, Harvesting & Partial Inventory Working
r/newworldgame
•
18d ago
New World: Aeternum Private Server Progress — Character Creation, Combat, Harvesting & Partial Inventory Working
462 upvotes · 60 comments
MetaforDevelopers
•
Ad
Coding model stuck in a single file? Muse Spark works across whole repos.
dev.meta.ai
Learn More
i finally did it too!
r/webos
•
16d ago
i finally did it too!
62 upvotes · 54 comments
LG patched exploit for getting root in WebOS 26. Do Not Update!!!
r/webos
•
9d ago
LG patched exploit for getting root in WebOS 26. Do Not Update!!!
135 upvotes · 55 comments
me, this year
r/ClaudeCode
•
3d ago
me, this year
196 upvotes · 47 comments
We weren’t crazy after all…
r/ClaudeCode
•
6mo ago
We weren’t crazy after all…
731 upvotes · 126 comments
I've used Claude Code every day for a year. This is the workflow I now start every project with
r/ClaudeCode
•
18d ago
I've used Claude Code every day for a year. This is the workflow I now start every project with
231 upvotes · 71 comments
State of Nadeo and Trackmania
r/TrackMania
•
3d ago
State of Nadeo and Trackmania
231 upvotes · 103 comments
The future is bleak
r/ClaudeAI
•
15d ago
The future is bleak
1.6K upvotes · 687 comments
To be fair, it’s healthy for the community
r/ClaudeCode
•
6mo ago
To be fair, it’s healthy for the community
173 upvotes · 16 comments
it finally happened to me
r/ClaudeCode
•
10d ago
it finally happened to me
488 upvotes · 170 comments
Do you agree?
r/ClaudeCode
•
11d ago
Do you agree?
1.5K upvotes · 209 comments
My world has changed
r/LGOLED
•
2mo ago
My world has changed
19 upvotes · 26 comments
New update
r/ClaudeCode
•
2mo ago
New update
58 upvotes · 34 comments
It's happened
r/ClaudeCode
•
3mo ago
It's happened
577 upvotes · 323 comments
This is Karla, my parent's Cavapoo. Sometimes she has these weird episodes where she'll sort of hyperventilate like this for 20-30 seconds. Can anybody explain why?
r/DogAdvice
•
8d ago
This is Karla, my parent's Cavapoo. Sometimes she has these weird episodes where she'll sort of hyperventilate like this for 20-30 seconds. Can anybody explain why?
830 upvotes · 197 comments
fuck yeah or fuck ya?
r/EnglishLearning
•
6y ago
fuck yeah or fuck ya?
2 upvotes · 4 comments
Insane Micro Stutters in MP (High End PC) - Game is unplayable
r/modernwarfare4
•
6d ago
Insane Micro Stutters in MP (High End PC) - Game is unplayable
71 upvotes · 281 comments
Gifts for Adults who have EVERYTHING
r/GiftIdeas
•
1y ago
Gifts for Adults who have EVERYTHING
6 upvotes · 25 comments
The Way the World Ends
r/OCPoetry
•
3mo ago
The Way the World Ends
2 upvotes · 2 comments
South Korea OB/GYN IP Camera Hack Leaks Patient Examination Footage to Illegal Overseas Adult Sites
r/korea
•
21d ago
South Korea OB/GYN IP Camera Hack Leaks Patient Examination Footage to Illegal Overseas Adult Sites
898 upvotes · 25 comments
I’m tired of it now.
r/ClaudeCode
•
7d ago
I’m tired of it now.
25 comments
What are y’all doing
r/ClaudeCode
•
24d ago
What are y’all doing
80 upvotes · 96 comments
Seems like google have changed their icons yet again
r/googleworkspace
•
5mo ago
Seems like google have changed their icons yet again
60 upvotes · 134 comments
The Game Has Changed
r/funny
•
12y ago
The Game Has Changed
20K upvotes · 1.4K comments
Just noticed this changes.
r/ClaudeCode
•
3mo ago
Just noticed this changes.
67 upvotes · 29 comments
VIEW POST IN
Français
Português (Brasil)
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
