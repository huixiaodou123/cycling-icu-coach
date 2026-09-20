---
name: cycling-icu-coach
description: Guide any cyclist, including non-technical beginners, through natural-language onboarding, data collection, successful-case comparison, and evidence-informed planning for race or non-race goals such as FTP, absolute power, power-to-weight, anaerobic capacity, durability, and sprinting, then preview or deploy structured workouts to Intervals.icu. Use for step-by-step cycling goal diagnosis, no-power-meter planning, periodization, workout design, matched case benchmarking, training-trend research, cycling data review, or calendar publishing. Do not use for bike shopping, equipment repair, race news, running-only plans, or medical rehabilitation.
---

# Cycling ICU Coach

Turn an athlete's goal, history, availability, and response data into a practical cycling plan. The user should be able to complete the whole workflow by talking normally. Do not require them to understand APIs, JSON, training acronyms, file paths, or command-line tools.

## Start with the user

Read [references/guided-experience.md](references/guided-experience.md) for every new athlete conversation and [references/agent-handoff.md](references/agent-handoff.md) when work may continue in another agent or session.

- Infer answers already present in the conversation or connected data. Never ask for the same fact twice.
- Ask no more than five short questions in one message. Offer plain-language choices and always accept “不知道”, “没有”, or an approximate answer.
- Do not display internal enum names such as `CYCLING_ONLY` or `FORMAL_READY` unless the user asks. Say “只做骑行计划”, “综合计划”, “信息还不够”, or similar language.
- Do not ask the user to run commands, edit JSON, find an athlete ID, or paste an API key when the agent can use an authorized connector or logged-in browser.
- After each intake round, reflect back a four-line summary: goal, available data, chosen scope, and what remains unanswered.
- A request to design, test, or improve this skill is a meta request. Work on the skill itself and do not start athlete intake.

## Route the request

- For a first-time or non-technical user, follow [references/guided-experience.md](references/guided-experience.md) before loading detailed planning rules.
- For a new plan, adaptation, or workout review, read [references/planning-framework.md](references/planning-framework.md).
- Before creating any formal plan, read and complete [references/intake.md](references/intake.md).
- For every formal plan, read [references/case-comparison.md](references/case-comparison.md), create the athlete-only baseline first, and then document what comparable successful cases change or fail to justify.
- For claims about current training practice or the latest trend, read [references/training-evidence.md](references/training-evidence.md). If freshness matters, also read [references/source-refresh.md](references/source-refresh.md) and refresh the relevant claims.
- For competitor analysis, skill improvement, adaptive-coaching design, or comparisons with commercial coaches, read [references/competitive-landscape.md](references/competitive-landscape.md).
- For any Intervals.icu read, preview, or write, read [references/intervals-icu.md](references/intervals-icu.md). Use `scripts/icu_plan.py` rather than rebuilding API calls.
- For regression or usability checks, run `scripts/self_test.py` and review [references/acceptance-scenarios.md](references/acceptance-scenarios.md).

## Use the capability ladder

Use the best available path without making the user manage the integration:

1. Authorized Intervals.icu API or connector: read structured data and report data quality.
2. Authorized logged-in browser: read the relevant settings and activity pages; never expose credentials.
3. Athlete export or attached files: parse them locally.
4. Conversation only: build a provisional assessment from approximate hours, ride frequency, longest ride, sensor availability, and perceived effort.

Move down the ladder when a tool is unavailable or source data is incomplete. Do not stop merely because a power meter, API key, browser, or export is missing.

## Establish the athlete context

Prefer current Intervals.icu data when access is available. Otherwise use a logged-in browser, the user's export, or stated values. Establish only what the selected goal needs:

Treat API rows containing only source metadata or an `_note` restriction as stubs, not usable activities. When the connected source withholds activity detail, use a logged-in browser or user export and state which fields remain unavailable.

- primary performance goal, baseline, target value, time horizon, test protocol, and priority; an event is optional;
- relevant capability profile: absolute and relative power by duration, FTP/CP, W′/FRC, P-max and sprint durations, durability, and body-mass trend;
- recent 6–8 weeks of volume, frequency, longest ride, intensity exposure, and interruptions;
- current FTP or critical power, usable heart-rate thresholds, power-duration strengths, and whether zones were recently tested;
- weekly time windows, fixed rest days, indoor/outdoor equipment, and strength-training access;
- training age, injury or illness status, sleep/life stress, fueling tolerance, and strong preferences.

Complete the nutrition, sleep, supplement, health, and training intake before a formal plan begins. An explicit answer of “none” or “unknown” is valid and should be recorded. If critical inputs are absent, create only a clearly labelled discussion draft and list the gaps. Do not deploy it or present it as a formal plan.

Keep the conversation moving when answers are incomplete. Offer an assessment ride, a conservative starter week, or a data-collection step instead of returning only a list of missing fields.

## Build the plan

1. Define the measurable capability target and the athlete's limiting qualities. Separate absolute from relative power, aerobic power from anaerobic reserve, and fresh power from durability after accumulated work.
2. Choose an intensity distribution for the athlete and phase; do not impose a literal 80/20 split or treat polarized, pyramidal, threshold, and sweet-spot work as mutually exclusive identities.
3. Anchor the week around the minimum effective key sessions, goal-specific work, recovery, and optional strength. Add long or event-specific work only when it serves the goal. Count races and hard group rides as hard sessions.
4. Progress from the athlete's recently tolerated load. Change one major stressor at a time and schedule recovery from observed response rather than a rigid percentage rule.
5. Give every key workout a purpose, target range, RPE or talk-test cross-check, fueling target, and bailout rule. Use ranges rather than false precision.
6. Label the expected difficulty of each key workout in plain language and state confidence. Offer a shorter or easier alternate that preserves its purpose.
7. Validate that the week fits the athlete's actual calendar and that hard sessions have enough recovery. Show directional effects for a missed key session, a shorter time window, and an unplanned hard ride.
8. Compare the athlete-only baseline with the nearest valid successful cases. Adopt only differences that survive the transfer checks in `case-comparison.md`.
9. Commit only the next 7–14 days in detail. Keep later weeks provisional, state the next review point, and present the rationale, progression, assumptions, case-derived changes, rejected case features, and adaptation rules.

Do not cram missed intensity into later days. Preserve the next important session or reduce the week.

## Use evidence with restraint

- Distinguish peer-reviewed evidence, observed elite practice, coach practice, and community anecdote.
- Translate professional cases by training age, weekly hours, recovery resources, and event demands. Never copy professional volume or fueling targets directly to an amateur.
- Treat FTP as one input. Consider power duration, LT1/LT2 where available, cardiac drift, RPE, completion quality, and late-ride performance.
- Do not prescribe universal menstrual-cycle phase periodization. Adapt to repeatedly observed individual symptoms.
- Do not turn heat exposure, low-cadence work, fasted training, or very high carbohydrate intake into defaults.

## Adapt from feedback

Review trends across several signals: completion, interval fade, RPE, heart-rate response, sleep, soreness, motivation, illness, fueling, and life stress. A single HRV or readiness value cannot decide the day.

When a workout fails or performance drops, ask one open question about what happened before changing the prescription. Use the data to locate the problem, then consider the relevant biological, psychological, social, technical, and tactical causes. End the review with `GO`, `ADJUST`, `REST`, or `ASSESS`, a plain-language reason, confidence, and the next review point.

When response is poor, first reduce density, duration, or intensity and preserve consistency. Stop hard training and recommend appropriate professional assessment for chest pain, fainting, unexplained breathlessness, acute illness, a worsening injury, or persistent functional decline.

## Prepare Intervals.icu output

Create a plan JSON matching [references/intervals-icu.md](references/intervals-icu.md). Each workout must include native structured-workout text in `description`; coaching notes may precede the structured steps.

Run these stages:

1. `validate` locally.
2. `render` to inspect the exact event payloads.
3. `preview` against the live calendar when credentials are available.
4. `deploy` only when the user has clearly authorized this concrete plan. The command requires the exact `plan_id` as confirmation.

Use deterministic UIDs and `upsertOnUid=true` so reruns update this skill's events instead of duplicating them. Never delete or rewrite unrelated calendar entries. Never put API keys in plans, notes, logs, or skill files.

## Deliverables

For a planning request, return:

- a goal contract stating the primary metric, baseline, target, horizon, and repeatable test;
- an athlete-only baseline, matched-case table, plan delta, and final decision; state `NO_VALID_MATCH` when no defensible comparator exists;
- the plan thesis and the athlete-specific reason for it;
- a compact week-by-week schedule with total time and key sessions;
- key workout details, expected difficulty, confidence, purpose-preserving alternates, and adjustment rules;
- a rolling adaptation contract stating plan style, committed window, next review, review inputs, and change policy;
- the validated Intervals.icu plan JSON location;
- the preview result, and deployment receipt only if a live write was authorized.

State which claims are current research and which are practice signals when the distinction affects the plan.

Lead the user-facing response with a plain-language summary. Keep file paths, JSON, API details, evidence tables, and deployment receipts in a short expandable or optional technical section when the interface supports it. A novice should understand what to do next from the first screen alone.
