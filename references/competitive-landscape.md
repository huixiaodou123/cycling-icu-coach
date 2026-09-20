# Competitor and coaching-practice landscape

Use this reference when improving the skill, explaining how it differs from other coaching products, or designing its adaptive behavior. Product capabilities below are public vendor or project claims, not independent proof of training outcomes. Re-check volatile claims before quoting them. Last reviewed: 2026-09-20.

## Commercial products

| Product | Publicly documented approach | Useful design lesson | Boundary or opportunity for this skill |
|---|---|---|---|
| TrainerRoad AI | Uses a four-week simulation window, predicted workout difficulty, fatigue prediction, FTP detection/prediction, workout alternates, dynamic endurance duration, and a user-selected training approach. It re-simulates after calendar changes. | Show the likely consequence of a change before asking the athlete to accept it. Preserve the purpose of a workout when offering shorter, easier, or harder alternatives. | Do not imitate numeric predictions without a validated model and sufficient athlete history. Provide directional scenarios and confidence instead. |
| JOIN Cycling | Builds around cycling level, goal, and weekly availability; uses workout data, RPE, readiness, and changed or missed availability to adjust the plan. Non-race skill goals are supported. | Availability is a first-class planning input. Ask for a brief subjective response after training and let unexpected rides enter the plan. | Go beyond heart rate/power dependence with a true no-sensor mode and make evidence/case transfer visible. |
| Garmin Cycling Coach | Adapts daily from performance, recovery, health metrics, course demands, missed or extra workouts, and training load focus; supports heart-rate or power targets and optional strength. | Account for all recorded training, including unplanned and cross-training work, before choosing the next hard session. | Current adaptive cycling mode depends heavily on compatible devices and, for full use, heart rate plus power. Maintain a device-neutral fallback. |
| Wahoo SYSTM | Uses a multi-dimensional 4DP profile rather than FTP alone; daily recommendations can use available time, motivation, fatigue, and stress, with alternative workouts and integrated strength/yoga. | Match short and long efforts to the athlete's actual phenotype. Ask about motivation and stress rather than reading load alone. | A test-derived profile is useful only when test coverage and execution are credible. Keep assessment-first and no-power routes. |
| HumanGO | Markets continuously adaptive plans based on availability, physiological progress, health metrics, sport, and feedback, plus a conversational AI coach. | Conversation should modify the plan directly and explain the reason for the change. | Preserve transparent evidence, confidence, and user approval rather than presenting an opaque AI decision as fact. |
| AiFitCoach | Chinese-first conversational coach using Intervals.icu; publicly claims two-week plans, morning HRV/sleep adjustment, nutrition, strength, heart-rate fallback, and automatic calendar writes. | Chinese users value a single conversational surface covering training, food, strength, recovery, and device sync. | Differentiate through no-sensor fallback, matched-case comparison, source grading, explicit deployment preview, and multi-factor readiness rather than one morning score. |
| Onelap | Strong domestic execution layer: indoor riding, ERG targets, courses, group rides, competition, training content, calendars, and some coach services. | Adherence improves when the plan can be executed in familiar tools and when training stays engaging. | Treat it as an execution/content platform unless current documentation demonstrates athlete-specific adaptive planning. |

Sources: [TrainerRoad AI update](https://www.trainerroad.com/blog/whats-new-with-trainerroad-ai/), [JOIN setup](https://help.join.cc/hc/en-150/articles/4402679265809-Setting-up-your-first-JOIN-training-plan), [JOIN adaptive method](https://join.cc/why-join), [Garmin Cycling Coach](https://www.garmin.com/en-GB/garmin-technology/garmin-coach/garmin-cycling-coach/), [Wahoo daily recommendations](https://support.wahoofitness.com/hc/en-us/articles/22483546617618-Daily-Recommended-Workouts-for-Wahoo-app-SYSTM), [Wahoo 4DP](https://support.wahoofitness.com/hc/en-us/articles/4405243309330-IF-and-TSS-with-4DP), [HumanGO](https://humango.ai/how-it-works/athletes), [AiFitCoach](https://aifitbike.com/coach), [Onelap](https://www.onelap.cn/).

## Open protocols and self-hosted projects

| Project | Strong idea to learn from | Do not copy blindly |
|---|---|---|
| Section 11 | Deterministic, auditable protocol; stable private athlete dossier separated from current metrics; derived metrics computed before the language model explains them. | Its setup and data-mirror surface can be too heavy for a novice. Keep this skill operable through ordinary conversation. |
| Montis.icu | Data integrity and governed athlete state precede AI dialogue; durability, repeatability, physiology, forecast, and adaptive decisions are separated. | Avoid presenting proprietary internal scores without a plain-language reason and confidence. |
| Enduragent | Local memory, multilingual chat, periodized plans, schedule-change edits, cost control, and direct Intervals.icu writes. | Calendar convenience cannot replace formal intake, case transfer checks, or a concrete preview. |
| DomestiqueAI | Tested calculations, LLM explanations, deterministic guardrails, a daily go/adjust/rest check, and a weekly reduce/maintain/progress loop. | Universal 80/20 or fixed ramp limits should not become safety laws; distribution and progression remain athlete- and phase-specific. |
| Intervals.icu MCP servers | Broad read/write tools make data access portable across agents. | Tool access is not coaching logic or write authorization. Verify data quality and retain the preview/approval gate. |

Sources: [Section 11](https://github.com/CrankAddict/section-11), [Montis.icu](https://github.com/revo2wheels/intervalsicugptcoach-public), [Enduragent](https://github.com/yerzhansa/enduragent), [DomestiqueAI](https://github.com/arnaudstdr/domestique-ai), [Intervals.icu MCP Server](https://github.com/mvilanova/intervals-mcp-server).

## What working coaches add

Products mostly optimize schedules and workout selection. Coaching practice adds diagnosis, context, and a relationship with the athlete.

1. **Change distribution by phase.** A survey of 117 cycling coaches found 94% changed intensity distribution across the season. Pyramidal-to-polarized toward competition was common, which argues against assigning one permanent training identity.
2. **Profile several abilities.** FTP is useful but incomplete. Coaches compare performance across durations, repeatability, fresh versus fatigued output, and the demands of the target before selecting a limiter.
3. **Investigate before prescribing.** A drop in late-ride power may reflect physiology, fueling, sleep, fear, technique, pacing, group positioning, or life context. The data identifies where performance changed; a short open question helps identify why.
4. **Combine objective and subjective evidence.** Power, heart rate, work, and completion data are interpreted with RPE, confidence, motivation, symptoms, and what the rider was trying to do.
5. **Preserve the session purpose.** When time or readiness changes, good coaches shorten, reduce, or replace the session while protecting the intended stimulus and the next important day.
6. **Use role and terrain specificity.** Climbers, sprinters, time-trial riders, beginners, and non-racers need different target durations, cadence/terrain choices, and late-ride tests even at the same FTP.
7. **Review adherence as a system.** Repeated misses can indicate a schedule or plan-design failure, not a motivation defect. Adjust density and friction before escalating load.

Sources: [2025 cycling-coach survey](https://journals.sagepub.com/doi/10.1177/17479541251362199), [Robert Ferguson on diagnosing durability](https://www.trainingpeaks.com/coach-blog/what-durability-data-can-not-measure/), [Astana performance approach](https://www.trainingpeaks.com/blog/we-speak-peak-team-astana/), [Coggan power profiling](https://www.trainingpeaks.com/blog/power-profiling/). Chinese practice signals include [Intervals.icu plans for time-crunched riders](https://www.bilibili.com/video/BV1RpbL6CEke), [testing and FTP progress case](https://www.bilibili.com/video/BV1iT411d7CG), [anaerobic and sprint training](https://www.bilibili.com/video/BV1vJSqYbEr9), and [strength planning](https://www.bilibili.com/video/BV1qWRDB3E12). Treat platform videos as practice signals until their prescriptions are checked against stronger evidence.

## Product decisions for this skill

Adopt these patterns:

- Keep stable athlete context separate from current measurements and readiness. Add timestamps and state what is measured, configured, estimated, stale, or missing.
- Default the plan style to balanced, then let the athlete choose conservative, balanced, or ambitious without weakening health gates.
- Show a plain-language difficulty prediction for each key workout: easy, manageable, challenging, very hard, or unknown. State confidence and the evidence used.
- Offer at least one purpose-preserving alternate when time, location, equipment, or readiness changes.
- Show directional what-if effects for common disruptions: a missed key session, an unplanned hard group ride, and a shorter training window. Do not invent exact FTP or fitness outcomes.
- Commit the next 7–14 days in detail and keep later weeks provisional. Re-review the upcoming week instead of silently rewriting the whole block.
- After important or failed sessions, ask one open causal question before choosing the change. Consider biological, psychological, social, technical, and tactical factors only as relevant.
- End every review with one decision (`GO`, `ADJUST`, `REST`, or `ASSESS`) plus the reason, confidence, and next review point.

Reject these shortcuts:

- automatic changes from a single HRV, sleep, or readiness value;
- a universal weekly percentage increase, fixed recovery-week ratio, or permanent 80/20 rule;
- numerical forecasts without a validated model and enough comparable data;
- assuming completion proves the intended stimulus was correct;
- deploying a changed plan without showing the concrete calendar delta.
