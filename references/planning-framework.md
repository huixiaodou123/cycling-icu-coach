# Cycling planning framework

Use this reference to create or adapt a plan. It is a decision framework, not a fixed template.

## Athlete model

Capture the following in a short profile:

| Area | Useful inputs | Decision affected |
|---|---|---|
| Goal | primary metric, baseline, target, horizon, test; optional event demands | specificity, progression, and testing |
| Capacity | absolute/relative power curve, FTP/CP, P-max, W′, LT1/LT2, late-ride fade | zone and limiter selection |
| History | 6–8 week hours/load, longest ride, hard days, interruptions | safe starting dose |
| Availability | exact weekday windows, travel, indoor/outdoor options | weekly architecture |
| Response | RPE, sleep, soreness, motivation, HRV trend, illness | adaptation and recovery |
| Fueling | carbohydrate tolerance, sweat/sodium history, GI symptoms | session quality and gut training |
| Health | current pain, illness, medication that alters HR, RED-S risk | whether normal planning is appropriate |

Do not infer precision from stale FTP or auto-estimated zones. When power and internal response disagree, inspect heat, fatigue, hydration, fueling, sensor quality, and zone validity.

## Plan without a power meter

When the athlete has no power meter, do not prescribe watts or `%FTP`, and do not present configured FTP, W′, P-max, or platform power zones as measured ability. Build cycling sessions from duration, heart-rate ranges when validated, RPE, breathing/talk test, cadence, terrain, and repeatable route or climb times.

Treat a platform LTHR as unverified unless it can be traced to valid heart-rate data or a repeatable test. Intervals.icu may suggest LTHR from 98% of the highest 20-minute average heart rate or 100% of the highest one-hour average, but the source effort must be close to maximal and the sensor trace must be credible. Until then, use broad RPE and talk-test guidance rather than narrow heart-rate ceilings.

For absolute power, W′/FRC, P-max, and power-duration goals, explain that progress cannot be measured directly without a power meter, smart trainer, or laboratory test. A fixed climb, sprint segment, speed at a repeatable heart-rate/RPE, cadence, and completion quality can be secondary proxies, but they must not be relabelled as watts or anaerobic reserve.

## Choose plan scope

Offer the athlete a clear choice:

- `CYCLING_ONLY`: cycling workouts, testing, load, and recovery days. Nutrition, sleep, supplements, and health are still screened because they affect interpretation, but the output only notes relevant constraints.
- `INTEGRATED_PERFORMANCE`: cycling plus strength, fueling practice, sleep/recovery actions, and evidence-based supplement trials where appropriate.
- `ASSESSMENT_ONLY`: collect data, validate zones/models, and choose a target before scheduling a training block.

Do not assume that a request for FTP or sprint improvement authorizes a weight-loss, diet, sleep, or supplement intervention.

## Convert the goal into training demands

For a non-race goal, define the target duration and repeatable test first. For an event, describe duration, total work, climbing or accelerations, time near/above threshold, technical demands, environmental heat, and the need to produce power late. Pick at most two primary limiters for each block.

Capability targets require different diagnoses:

| Target | Primary measures | Common supporting qualities | Important distinction |
|---|---|---|---|
| FTP/CP | standardized threshold/CP test, 12–40 min power | aerobic volume, VO2 power, durability | do not chase weekly auto-estimates |
| Absolute power | watts at the exact target duration | muscle mass/strength, aerobic or anaerobic support | relevant even when W/kg is unchanged |
| Power-to-weight | watts and body mass measured under consistent conditions | power development, healthy body composition | improve the numerator and protect energy availability |
| W′/FRC | valid power-duration model with maximal short and long efforts | severe-domain work, recovery between efforts | reserve size differs from recharge/repeatability |
| Sprint/P-max | P-max, 1–5 s, 10–15 s, cadence and execution | maximal strength, technique, freshness | peak sprint differs from sprint after fatigue |
| Durability | change in target power after standardized prior work | aerobic base, fueling, pacing, heat tolerance | standardize prior intensity and work |

Use absolute watts and W/kg together when body mass affects the goal. Do not assume lower mass always improves real performance.

Examples:

- Non-race FTP goal: raise a standardized CP/FTP measure while preserving endurance and monitoring late-ride response.
- Absolute 5-minute power: aerobic power and tolerance of sustained severe work, with a consistent 5-minute test.
- Sprint goal: fresh P-max/5-second quality first, then sprint after fatigue only if it is a separate target.
- Power-to-weight goal: power-first block unless nutrition and health screening supports a modest body-composition phase.
- Long gran fondo: aerobic volume, fueling tolerance, climbing tempo/threshold, durability.
- Short road race or criterium: aerobic support, repeated severe efforts, sprint under fatigue, positioning practice.
- Time trial: sustainable race power, position durability, pacing, heat management.
- Hill climb: relative threshold/VO2 power and event-specific cadence.

## Choose the distribution

Use the three-domain model for reasoning when possible: below LT1, LT1–LT2, and above LT2. Power-zone labels may be used for execution, but they are not interchangeable with physiological domains.

- Recreational riders with limited hours commonly need a pyramidal pattern: most time easy, useful moderate work, and a smaller high-intensity dose.
- Competitive/high-volume riders may use more polarized blocks when high-intensity quality and abundant low-intensity volume fit the phase.
- Threshold or sweet-spot blocks can be useful for time efficiency and event specificity, but accumulated fatigue must remain manageable.
- Distribution can change by phase. Evaluate it over a block, not from a single week.

For most non-professional athletes, start with no more than two hard cycling days in seven days unless recent history shows that more is tolerated. A race, hard group ride, demanding gym session, or long ride with substantial tempo can consume that budget.

## Build the block

Common phases are preparation, development, goal-specific work, verification, and—when an event exists—taper. Use only the phases the horizon needs.

- Start from recently tolerated frequency and duration.
- Add one main stressor at a time: duration, intensity minutes, interval density, or event specificity.
- Keep easy days truly easy enough to support the next key session.
- Insert recovery when performance, motivation, sleep, or completion quality trends down, or after a planned loading sequence. A 2–3 week load plus recovery rhythm is common, but not mandatory.
- Before a metric retest, reduce fatigue enough to make the result comparable; do not turn every block into a race taper.
- For an event, taper by reducing volume while preserving small doses of relevant intensity; avoid last-minute fitness tests.

Use Intervals.icu load metrics as context rather than a command. CTL, ATL, form, and ramp rate depend on model assumptions and do not replace athlete response.

## Compare before finalizing

Create an athlete-only baseline from the goal contract, recent load, availability, recovery, and current capacity before reading the selected case prescription. Then use [case-comparison.md](case-comparison.md) to produce a case-informed delta.

Prefer the athlete's own previously successful blocks over external cases. A public case may change the ordering, density, or progression of sessions only when its population, goal, test, and practical dose are sufficiently comparable. Keep the athlete-only choice when a case succeeded under materially different weekly hours, training age, recovery support, equipment, or environmental conditions.

Do not hide the comparison inside the rationale. Show what changed, what stayed, and what was rejected.

## Design workouts

Each key workout should specify:

1. Purpose.
2. Warm-up and activation.
3. Main set using a target range.
4. Internal cross-check: RPE, breathing/talk test, or HR where appropriate.
5. Cadence or terrain only if it serves the event demand.
6. Fuel and fluid target appropriate to duration and intensity.
7. Bailout rule and an easier fallback.

Useful session families:

- Endurance/LT1: stable power and breathing; monitor late-ride cardiac drift and RPE.
- Tempo/sweet spot: sustainable muscular endurance and event-specific work; avoid making every easy ride moderately hard.
- Threshold: accumulate controlled work near the current sustainable boundary; stop before repeated power collapse.
- VO2: choose long intervals, short intervals, or variable efforts for the athlete's response and event; target strong oxygen demand rather than a magical FTP percentage.
- W′/anaerobic capacity: use severe efforts that match the target duration; separate reserve development from repeated-effort recovery.
- Sprint/P-max: perform maximal quality while fresh with long recovery. Do not prescribe sprint power as a simple percentage of FTP.
- Repeated sprint or sprint-after-fatigue: add only after fresh sprint quality is established and when it is an explicit goal.
- Durability: place controlled event-specific work after meaningful prior work, without turning every long ride into a race.
- Strength: emphasize technically sound compound lower-body work; commonly two sessions in preparation and one maintenance session in season if tolerated.

Low-cadence cycling can provide event-specific torque practice, but evidence does not justify it as a universal strength substitute.

## Fueling rules

Match carbohydrate to the session. Very easy short rides may require little during-ride carbohydrate; quality and long work should be fueled. Build intake progressively and rehearse the event strategy.

Treat 120 g/h as an advanced, event-specific option supported by emerging evidence in trained athletes, not a universal goal. Start from known tolerance, use multiple transportable carbohydrates at higher rates, and track GI response. Include sodium and fluid based on conditions and individual sweat history rather than a single global number.

## Adaptation traffic light

Judge trends, not isolated wearable scores.

- Green: normal sleep/motivation, expected RPE, stable execution, no worsening pain. Continue or progress one variable.
- Amber: two or more adverse signals, unusual interval fade, rising RPE at normal load, poor sleep, or life stress. Reduce duration/density, replace intensity with easy work, or move the session.
- Red: acute illness, chest pain, fainting, unexplained breathlessness, worsening injury, or persistent performance decline. Stop hard work and seek appropriate assessment.

After a missed key session, do not automatically move it to the next day. Protect spacing and the next highest-priority stimulus.

## Plan review

Before release, confirm:

- total hours fit the calendar;
- hard days and strength sessions are spaced sensibly;
- the long ride and fueling progression match the event;
- recovery and taper are visible;
- every key workout has a bailout rule;
- assumptions and low-confidence choices are explicit;
- professional practices have been scaled to the athlete.
- the athlete-only baseline, matched cases, adopted deltas, and rejected deltas are visible;
- the selected output respects `CYCLING_ONLY`, `INTEGRATED_PERFORMANCE`, or `ASSESSMENT_ONLY` scope.
