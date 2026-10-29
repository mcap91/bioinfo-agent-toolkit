reel: https://www.instagram.com/reel/De4iU2vMW7X/
captured: 2026-10-29
yt-dlp: 2026.10.26
ffmpeg: 7.0.2-static
faster-whisper: 1.2.1
ctranslate2: 4.8.4
claude: 2.1.281 (Claude Code)

## Caption

The 7 levels of observability, explained simply 🔦

Each level lets you see more of your system. Save this:

1️⃣ Logs (Grafana Loki): your app writes a line for every event, so you know what happened and exactly when. But one line can't show a trend
2️⃣ Metrics (Prometheus, Grafana): numbers your app reports every few seconds (requests, errors, latency). On a dashboard you see the trend: checkout is getting slower
3️⃣ Traces (OpenTelemetry, Jaeger): follow one request through every service and time each step. The database took 800 ms. Now you know where
4️⃣ Correlation (OpenTelemetry, Grafana): give every request an ID when it arrives and stamp it on every log and trace. Search that ID and the log tells you why
5️⃣ Alerts (Alertmanager, PagerDuty): don't wait for users to complain. "Errors above 5% for 5 minutes" pages you before they notice
6️⃣ SLOs (Datadog, Grafana): SLI = what you measure, SLO = your target (99.9%), SLA = your promise to customers. Page only when the target is at risk
7️⃣ Cardinality, the boss (Prometheus, Datadog): tag a metric with user IDs and a million users = a million time series. Keep metric labels few; per-user detail goes in logs and traces

Observability isn't more data. It's the right data.

Where to start: map your critical user journeys, instrument services with logs, metrics and traces sharing one ID, set SLOs, build dashboards, alert on what matters, then keep improving.

Which level is your team on? 👇

#observability #devops #sre #monitoring #logging #opentelemetry #prometheus #grafana #microservices #programming

## Transcript

[   0.0] The seven levels of observability each one lets you see more of your system level one logs
[   6.2] Users say checkout is broken. You can't see why so your app writes a line for every event
[  11.2] What happened and exactly when but one line can't show you a trend
[  15.6] level 2
[  16.8] metrics
[  17.6] Numbers your app reports every few seconds
[  19.9] Requests errors and how long each one takes put them on a dashboard and you see the trend
[  25.8] Check out is getting slower, but check out touches five services. Which one is slow?
[  31.3] level 3
[  32.6] Traces a trace follows one request through every service and times each step the database took 800 milliseconds
[  40.2] Now you know where but not why
[  42.7] level 4
[  44.2] Correlation give every request an ID the moment it arrives every service stamps that ID on its logs and traces
[  51.0] Search that ID and the log says why a database query with no index
[  57.0] level 5
[  58.6] Alerts, but you only looked because users complained and alert watches the numbers for you
[  63.8] Errors above 5% for five minutes your phone rings before users notice
[  69.8] level 6
[  71.1] SLOs alert on every blip and you'll ignore them all so decide what good means measure it
[  77.2] That's your SLI pick a target like 99.9 percent. That's your SLO promise it to customers
[  84.0] That's your SLA now. You only get paged when the target's at risk
[  88.6] level 7 the boss
[  91.3] Cardinality now you want to measure everything so you add a user ID to a metric a million users a million separate graphs to store
[  99.3] The bill explodes so keep metric labels few per user detail goes in logs and traces
[ 106.0] Seven levels one system you can finally see
[ 109.0] Observability isn't more data. It's the right data
[ 112.0] Which level is your team on?
[ 114.8] Save this share it with a friend and follow for more

## On-screen text

(none)

## Key claims

- There are seven levels of observability, each letting you see more of your system
- Logs: your app writes a line for every event so you know what happened and when, but one line can't show a trend
- Metrics: numbers reported every few seconds (requests, errors, latency) show trends on a dashboard, e.g. checkout getting slower
- Traces: follow one request through every service and time each step to find where time is spent (e.g. database took 800ms)
- Correlation: giving every request an ID stamped on logs and traces lets you search that ID to find why something happened
- Alerts: watch metrics automatically (e.g. errors above 5% for 5 minutes) so you're notified before users complain
- SLOs: SLI is what you measure, SLO is your target (e.g. 99.9%), SLA is your promise to customers; you only get paged when the target is at risk
- Cardinality is the hardest challenge: adding high-cardinality tags like user ID to metrics creates millions of time series and explodes storage/cost
- Keep metric labels few; put per-user detail in logs and traces instead
- Observability isn't about more data, it's about the right data
- Recommended starting approach: map critical user journeys, instrument with logs/metrics/traces sharing one ID, set SLOs, build dashboards, alert on what matters, then keep improving

## Info channel

spoken

## Mentioned (unverified hints)

- Grafana Loki: (no url)
- Prometheus: (no url)
- Grafana: (no url)
- OpenTelemetry: (no url)
- Jaeger: (no url)
- Alertmanager: (no url)
- PagerDuty: (no url)
- Datadog: (no url)
