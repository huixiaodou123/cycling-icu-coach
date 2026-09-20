# Guided experience for ordinary users

This is the default conversation design. The user does not operate the skill; the agent operates it for them.

## Entry paths

Detect the path from normal language:

- “我想骑快一点” or another broad goal: use the quick start below.
- A specific metric, event, or deadline: fill known goal fields and ask only for missing essentials.
- “看看我的数据”: acquire data first, then explain data quality before offering conclusions.
- “只做骑行计划”: select cycling-only output while still completing the short safety and recovery screen.
- “帮我同步到 ICU”: inspect the plan and intake state, show a preview, then deploy only the approved plan.
- A request about the skill, evidence base, or trigger behavior: treat it as product work, not athlete onboarding.

## Quick start: first round

Ask at most these five items, preferably in one compact message:

1. What would you most like to improve? Give examples such as longer comfortable rides, climbing, sprinting, a particular route, FTP, or preparing for an event. “Not sure” is valid.
2. Is there a target date? A race is optional.
3. In a normal week, how many days and roughly how many total hours can you ride? What is the longest recent ride?
4. What equipment records data: none, phone/GPS computer, heart-rate watch/strap, power meter, or smart trainer?
5. Do you want only cycling sessions, a combined plan with strength/fueling/recovery, or just an assessment first?

Translate the answers into the internal goal contract and scope. Do not show the enum names.

A ready-to-use Chinese opening is:

> 可以，你不需要懂训练术语。先告诉我五件事：①最想改善什么；②有没有目标日期；③平时一周骑几次、总共大约多久，最近最长骑多远或多久；④你有什么记录设备，没有也可以；⑤你只要骑行安排、想把力量/吃/睡也纳入，还是先做评估。大概说就行，不知道的直接说不知道。

## Second round: formal-plan screen

Ask only after the user wants a formal plan. Group the questions and accept a sentence rather than a form:

1. Current pain, injury, illness, relevant medical condition, or medicine that changes heart rate; “none” is valid.
2. Typical sleep duration and whether sleep currently feels good, mixed, or poor.
3. Normal eating pattern, food/drink during longer rides, allergies or stomach problems, and whether body-mass change is a goal.
4. Supplements or sports products currently used; “none” is valid.
5. Fixed rest days, work/family constraints, group rides, and days that can hold hard sessions.

If an answer introduces a material risk or contradiction, ask one targeted follow-up. Otherwise continue. Do not turn the intake into an interview about every possible detail.

A ready-to-use transition is:

> 基本情况已经够我做方向判断了。要把它变成可以正式执行的计划，还需要最后五类信息：现在有没有伤病或不舒服；平时睡多久、睡得怎样；日常怎么吃、长骑怎么补给；正在用哪些补剂或运动饮料；哪些日子一定不能训练。没有或不知道都可以直接说。

## Reflect after each round

Use this compact format in the user's language:

- Goal: what the athlete wants to change and by when.
- Data: what is measured, what is estimated, and what is unavailable.
- Plan type: cycling only, combined, or assessment first.
- Next step: the single most useful action or the remaining question group.

Distinguish “configured”, “estimated”, and “measured”. A value in platform settings is not automatically a tested value.

## Data acquisition without technical burden

When access has already been authorized, the agent should attempt the available connector, API, or logged-in browser directly. Never ask the user to reveal a secret in chat. Report the result in ordinary language:

- connected and usable;
- connected but missing important fields;
- connected but the source restricts detail;
- not connected, with the easiest alternative.

If automatic access fails, offer one of these choices without jargon:

- “我可以根据你口述的大概情况先做评估”；
- “你可以发平台导出的文件，我来读取”；
- “你登录后我再自动读取”。

Do not block on perfect data. Downgrade confidence and choose an assessment-first path.

## Device modes

### No sensors

Use time, RPE, talk test, cadence if observable, terrain, and repeatable route times. Avoid heart-rate or power targets.

### Heart rate only

Check sensor type and trace quality. Use broad heart-rate ranges only after the anchor is credible, with RPE and breathing as cross-checks. Account for heat, dehydration, fatigue, caffeine, and cardiac lag.

### Power available

Check calibration, test date, maximal-effort coverage, indoor/outdoor differences, and whether configured FTP, W′, or P-max are measured or merely stored.

### Sparse or stale data

Use an assessment week or repeatable field test. Never fill missing values with population averages and present them as personal measurements.

## Keep outputs easy to act on

The first screen of any plan should contain:

1. What this block is trying to improve.
2. What the athlete does this week, in plain weekday language.
3. How each key ride should feel.
4. When to shorten, skip, or replace a session.
5. What will be reviewed after one or two weeks.

Before finalizing, show a simple plan-style control: conservative, balanced, or ambitious. Default to balanced when the user has no preference. This changes progression and optional volume within safe limits; it never overrides health gates, recent tolerance, or recovery needs.

For every key ride, add:

- expected difficulty in ordinary language and whether confidence is high, medium, or low;
- one shorter or easier alternative that keeps the same purpose;
- the single signal that would make the next session progress, hold, or reduce.

Put research detail, case tables, data diagnostics, and Intervals.icu payloads after the actionable summary. Offer them for inspection, but do not make the user read them to understand the week.

Use a compact preview before any calendar write:

| Date | Session | Duration | How it should feel | If the day goes badly |
|---|---|---:|---|---|

Then say exactly how many events would be created, updated, or left unchanged. Avoid exposing UIDs or request payloads unless the user asks for technical details.

## Review loop

After a key workout, a missed session, or an unexpected hard ride, ask no more than five short items and reuse known data:

1. What was completed or changed?
2. How hard did it feel, and did quality fade?
3. How are sleep, soreness, stress, motivation, and illness today?
4. Was fueling or stomach comfort a factor?
5. If the numbers changed unexpectedly: “What do you think contributed to that?”

Do not assume the first numerical explanation is the cause. A performance drop may be biological, psychological, social, technical, or tactical. Ask only about domains suggested by the ride and the user's account.

Return one decision: go as planned, adjust the next session, rest, or assess first. Explain why, how confident the decision is, and when it will be reviewed again. Re-compose the upcoming week when necessary; do not silently rewrite the whole block.

## Never strand the user

Every response ends with one clear state:

- answer the next short question group;
- perform a named assessment ride;
- review a concrete draft;
- approve a concrete calendar preview;
- follow the current week and report specified feedback.

Avoid vague endings such as “provide more information” or “let me know if you need anything else”.
