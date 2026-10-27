reel: https://www.instagram.com/reel/DeJyswKCtCY/
captured: 2026-10-27
yt-dlp: 2026.10.26
ffmpeg: 7.0.2-static
faster-whisper: 1.2.1
ctranslate2: 4.8.4
claude: 2.1.281 (Claude Code)

## Caption

Shift Left Security, Explained!🐛

Shift left is the practice of moving security checks earlier in the software delivery line so issues get caught before code reaches production. SAST (static application security testing) scans code without running it, like CodeQL in a CI pipeline. DAST (dynamic application security testing) attacks the running app from outside, like OWASP ZAP in staging. Pre-commit hooks run a quick scanner like Semgrep on changed files before code enters Git, and editor plugins like SonarQube flag problems as code is written.

The example used is SQL injection, where input like ' OR 1=1 -- ends up inside the query and returns every order in the table. The fix is a parameterized query, so user input is always treated as plain data.

Which of these checks does your pipeline actually run? Comment below.

#ShiftLeft #DevSecOps #SAST #DAST #SQLInjection #DevOps #AppSec #CodeQL #OWASPZAP #Semgrep #SonarQube #PreCommit #CICD #KodeKloud #Shorts

## Transcript

[   0.0] Shift left is a term you hear in almost every DevOps team.
[   3.6] What does it actually mean?
[   5.3] If we see how your code flows in the organization on a line
[   7.6] from left to right, it looks like this.
[  10.2] On the far left, you write the code, then you commit it,
[  13.1] then the CI pipeline builds it, then staging for testing,
[  16.2] then you deploy on production,
[  17.4] where real users access the application.
[  20.0] So shift left simply means we catch important things
[  22.7] earlier on this line.
[  24.2] Now let's take one bug in the code
[  25.6] and follow it along this line from right to left.
[  28.2] Imagine you run an online store
[  29.6] where customers can search their order
[  30.9] by entering an order ID.
[  32.8] The problem is that the application takes
[  34.3] whatever the user types
[  35.5] and puts it directly into the database SQL query.
[  38.3] Normally, a customer types 1042
[  40.8] and the application puts 1042 in the database query
[  43.8] and returns the information to the customer.
[  45.8] But an attacker can type something like quote,
[  48.0] or one equals one dash dash in the search box.
[  52.0] Because the application blindly inserts
[  53.7] this user input into the query,
[  55.4] this input will run inside the query.
[  57.9] The condition one equals one is always true.
[  60.5] So instead of returning one order,
[  62.0] the database may return every order in the table,
[  64.3] which includes other customer's information as well.
[  66.8] This type of attack is called SQL injection
[  69.6] and the core problem is simple.
[  71.3] The user input is treated as part of the SQL command
[  73.9] instead of just data.
[  75.6] Now the team finds this issue in production
[  77.4] as an incident.
[  78.5] The security team checks whose data was exposed,
[  80.7] then a developer writes a hot fix
[  82.0] that is deployed in a hurry.
[  83.3] And depending on what leaked,
[  84.5] you have to inform your customers.
[  86.2] Now let's see how we could have prevented this issue.
[  88.6] We found the bug in production,
[  89.8] but one step to the left is staging.
[  91.9] Ideally in staging, we should have run our application
[  94.4] and attacked our application with OWASP's app,
[  96.6] a free tool that sends attack inputs to our application.
[  99.6] This type of testing where you attack from outside
[ 101.7] is called DAST or Dynamic Application Security Testing.
[ 105.0] If we go left, we have the CI pipeline,
[ 107.2] which builds and tests every change in our app automatically.
[ 110.3] The DevOps team could use a tool like CodeQL
[ 112.2] in the pipeline and CodeQL checks
[ 114.0] if your code is prone to SQL injection attacks.
[ 116.8] And if it is prone, then we fail the build pipeline
[ 118.9] with an error saying a critical vulnerability was found.
[ 121.5] This is called SAST or Static Application Security Testing
[ 124.5] because the application does not run
[ 126.0] and we just check the code.
[ 127.3] One more step left is when the developer
[ 128.8] commits the code to Git.
[ 130.5] So we could run a script on the developer's laptop
[ 132.4] every time the developer runs Git commit.
[ 134.6] And this is called a pre-commit hook.
[ 136.7] The hook runs a quick scanner
[ 137.8] like SEMGREP on the changed files.
[ 139.5] And if the scanner finds the same problem,
[ 141.2] the commit is blocked.
[ 142.5] The leftmost point is the editor like VS Code.
[ 145.2] We could install a plugin like SonarCube for VS Code
[ 147.6] and SonarCube checks your code as you type
[ 149.3] and underlines the line where the issue is.
[ 151.3] The fix to our problem is to send the SQL query
[ 153.6] and the user input to the database separately.
[ 155.8] So the attacker's input is treated as plain data
[ 158.2] and this is called a parameterized query.
[ 160.4] So the idea of shift left is that we scan
[ 162.4] for vulnerabilities and issues at each stage
[ 164.4] starting from the leftmost point
[ 165.9] so that issues can't reach production.
[ 167.8] If this video helped, hit subscribe and follow.

## On-screen text

SHIFT LEFT #DevOps

## Key claims

- Shift left means catching security issues earlier in the code-to-production pipeline (editor -> commit -> CI -> staging -> production).
- SQL injection occurs when user input (e.g. ' OR 1=1 --) is inserted directly into a SQL query instead of being treated as data.
- A successful SQL injection on an order-lookup query can return every row in the table, exposing other customers' data.
- DAST (e.g. OWASP ZAP) tests the running application from outside, typically in staging.
- SAST (e.g. CodeQL) analyzes code without running it, typically in the CI pipeline, and can fail the build if a vulnerability is found.
- Pre-commit hooks (e.g. using Semgrep) scan changed files on the developer's machine and can block a commit if issues are found.
- Editor plugins (e.g. SonarQube for VS Code) flag issues as code is typed, the earliest point in the pipeline.
- The fix for SQL injection is a parameterized query, which sends the query and user input separately so input is always treated as plain data.

## Info channel

spoken

## Mentioned (unverified hints)

- CodeQL: (no url)
- OWASP ZAP: (no url)
- Semgrep: (no url)
- SonarQube: (no url)
