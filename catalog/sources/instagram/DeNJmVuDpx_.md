reel: https://www.instagram.com/reel/DeNJmVuDpx_/
captured: 2026-10-27
yt-dlp: 2026.10.26
ffmpeg: 7.0.2-static
faster-whisper: 1.2.1
ctranslate2: 4.8.4
claude: 2.1.281 (Claude Code)

## Caption

Your AI coding agent greps your repo every session to rediscover it. Atomic Claude indexes it once into a local code graph, so Claude Code asks the graph instead.

- callers, callees, impact as file:line from the parse
- 31 languages, one binary, nothing uploaded
- SQL lineage across stored procedures, dbt and Snowflake
- an implement and review loop that checks blast radius before every edit

Free and local: github.com/damusix/atomic-claude

#claudecode #claude #ai #llm #aitools #aicoding #aiagents #artificialintelligence #codegraph #developertools #devtools #softwareengineering #softwaredeveloper #programming #coding #developer #tech #opensource #sql #dbt

## Transcript

[   0.0] Open a new Claude code session and ask it to change one function.
[   4.6] Before it writes a line, it goes looking.
[   7.4] It greps for the name.
[   9.0] It opens five files to find who calls it.
[  11.8] It guesses at your build command.
[  14.7] Then you correct the guess you corrected yesterday.
[  17.6] That search is a tax.
[  19.8] Every session pays it, in tokens and in wrong turns, because the session starts
[  24.2] with no memory of how your code fits together.
[  27.1] The next session pays it again.
[  29.0] Atomic Claude pays it once.
[  31.8] Run atomic code index in your repo.
[  34.6] It parses every file with tree sitter, compiled to WebAssembly, so
[  38.6] it ships as one static binary with no system dependencies.
[  42.6] The result is a symbol graph in a SQLite file inside your repo.
[  46.7] Every function, type, and import, and every call between them, 31 languages.
[  52.6] Nothing is uploaded.
[  53.8] There is no server and no account.
[  56.1] Running it again only reparses what changed.
[  59.5] Now Claude can ask the graph instead of searching.
[  62.6] Who calls this function?
[  64.2] What does it call?
[  65.6] If I change it, what breaks?
[  68.0] Those are three commands, callers, callees, and impact.
[  72.3] Each one answers with a file and a line from the parse,
[  75.6] not a list of text matches that happen to share a name.
[  79.2] Most code tools stop at the application.
[  82.2] A lot of systems live in the database.
[  84.9] Atomic Claude indexes SQL files as code.
[  88.5] It follows stored procedure lineage down to the column,
[  91.6] temp tables included.
[  93.1] It follows DBT models and snowflake tasks.
[  96.4] And it finds SQL written inside strings in your application
[ 100.2] code across 20 languages and puts it in the same graph.
[ 104.4] All of it is static.
[ 105.9] It never connects to your database.
[ 108.4] On top of the graph sits a workflow.
[ 111.2] Plan, implement, review, ship.
[ 114.6] An implementer writes the test first, then the change.
[ 118.5] A reviewer reads the work in a fresh context
[ 121.3] so it cannot inherit the implementer's reasoning.
[ 124.2] Before it edits a function, the loop
[ 126.2] asks the graph what that edit will break.
[ 129.0] The same graph keeps a project wiki current,
[ 131.6] so each new session starts with the build command,
[ 134.4] the layout, and the domains already loaded.
[ 137.4] The tax gets paid at index time.
[ 140.0] The loop spends its tokens on the change.
[ 143.1] The graph is one part of Atomic Claude.
[ 145.7] Behind it sits a whole layer of context engineering.
[ 149.2] How a session learns your repo, what it remembers,
[ 152.6] how agents check each other's work.
[ 154.8] Most of it you only notice once it is gone.
[ 157.7] Install it, index a repo, then go see what else is in there.
[ 161.8] The link is in the description.

## On-screen text

[curious] Open a new Claude Code

## Key claims

- AI coding agents like Claude Code grep the repo every new session to rediscover its structure, paying a 'search tax' in tokens and wrong turns
- Atomic Claude indexes the repo once into a local code graph via 'atomic code index', so Claude Code queries the graph instead of searching
- Indexing parses every file with tree-sitter compiled to WebAssembly, shipping as one static binary with no system dependencies
- The result is a symbol graph (every function, type, import, and call between them) stored in a SQLite file inside the repo
- Supports 31 languages
- Nothing is uploaded; no server and no account; runs fully local
- Re-running the index only reparses changed files
- Provides callers, callees, and impact commands that answer with file:line from the parse, not text-match search results
- Indexes SQL as code, following stored procedure lineage down to the column (including temp tables), dbt models, and Snowflake tasks
- Finds SQL embedded as strings inside application code across 20 languages and includes it in the same graph
- The SQL/database indexing is entirely static and never connects to the actual database
- Includes a plan/implement/review/ship workflow loop
- An implementer agent writes a test first, then the code change
- A reviewer agent reviews in a fresh context so it can't inherit the implementer's reasoning/bias
- Before editing a function, the loop queries the graph to check what the edit will break (blast radius)
- The graph also powers a project wiki kept current with build command, repo layout, and domains, loaded at the start of each session
- Atomic Claude is free and local

## Info channel

spoken

## Mentioned (unverified hints)

- Atomic Claude: github.com/damusix/atomic-claude
