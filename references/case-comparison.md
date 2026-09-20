# Comparing athlete data with successful training cases

Use this process for every formal plan. The purpose is to expose how much of the plan comes from the athlete's data and how much comes from an external precedent. A successful case is a benchmark, not proof that the same prescription will work for another athlete.

## Create the athlete-only baseline first

Before inspecting a case prescription, write a compact baseline using only:

- the goal contract and repeatable test;
- the athlete's recent 6–8 week volume, frequency, hard-day density, interruptions, and completion quality;
- the current power-duration profile, fatigue response, equipment, and available time;
- nutrition, sleep, supplement, health, and life-stress constraints;
- the selected plan scope.

Record the proposed weekly hours, hard days, main session families, progression, recovery pattern, testing, fueling support, and bailout rules. This prevents a striking elite case from anchoring the plan before the athlete's own constraints are considered.

## Select comparators in this order

1. The athlete's own previous block that produced a comparable, repeatably measured improvement without injury, illness, or unsustainable fatigue.
2. Controlled research or a detailed cohort with a similar goal, training status, baseline, intervention duration, and test.
3. A detailed individual case with day-level training data and a clear outcome.
4. Coach or platform cases with enough raw detail to reconstruct dose and adherence.

Use community anecdotes only to identify implementation ideas or questions. Do not use them as an efficacy benchmark.

For each candidate capture the source, population, baseline, goal, test, weekly hours, training age, intervention length, intensity structure, key sessions, strength work, fueling/recovery support, adherence, outcome, adverse events, and limitations. Record missing fields as unknown.

## Judge transferability

A case can be `MATCHED` only when all of these are defensible:

- the outcome metric and test are comparable to the athlete's goal;
- training status and baseline capacity are close enough that the dose has meaning;
- weekly time, frequency, equipment, and recovery resources can support the translated dose;
- the intervention and outcome are described well enough to separate training from measurement noise;
- no health, nutrition, or environmental difference makes the transfer inappropriate.

Use `CONTEXT_ONLY` when the case illustrates a principle but its dose is not transferable. Use `NO_VALID_MATCH` when no case clears the checks. Never weaken the standard merely to fill the table.

## Produce the delta table

Compare at least these rows:

| Dimension | Athlete-only baseline | Successful case | Normalized difference | Final decision and reason |
|---|---|---|---|---|
| Goal and test | | | | |
| Weekly hours/frequency | | | | |
| Hard days and spacing | | | | |
| Intensity distribution | | | | |
| Key interval dose | | | | |
| Long-ride/durability work | | | | |
| Strength or sprint work | | | | |
| Fueling and recovery support | | | | |
| Progression and recovery | | | | |
| Adherence and outcome | | | | |

Normalize absolute dose before comparing. Examples include hard minutes per weekly hour, sprint repetitions per session, interval work relative to the athlete's recently tolerated dose, and watts plus W/kg measured with the same protocol. Do not compare headline FTP gains when test method, training state, or duration differs.

Label each plan change `ADOPT`, `SCALE`, `REJECT`, or `UNKNOWN`. Give one athlete-specific reason. The final plan is the athlete-only baseline plus accepted deltas, not a second full case-copy plan.

## Define success without survivorship bias

Treat a case as successful only when the target measure improved beyond likely test noise or a meaningful practical threshold, adherence was reported, and the block did not create a clearly unsustainable cost. Look for unsuccessful comparators, group variability, dropouts, concurrent racing, body-mass change, equipment changes, and selective reporting.

One responder cannot establish causality. Group averages cannot predict an individual's response. Schedule an early process check and a repeatable outcome test so the athlete's own response replaces the borrowed assumption.

## Starter case cards

These are examples for comparison, not templates. Refresh them when newer or more comparable evidence is available.

### Long-term progression to professional level — context only for most amateurs

A 2025 case study analyzed 2,040 sessions across four years before a male Zwift Academy winner earned a professional contract. Moderate- and high-intensity work progressed gradually and later appeared within higher-volume days. His reported VO2max and 20-minute power were already world-class, so the volume and combined long-plus-intense days are usually not transferable. The useful principle is gradual dose progression and increasing specificity after a large endurance base.

Source: [From Amateur to Professional Cycling: A Case Study on the Training Characteristics of a Zwift Academy Winner](https://pmc.ncbi.nlm.nih.gov/articles/PMC12298706/).

### Trained cyclists improving 5- and 40-minute power — cohort benchmark

In a 12-week study of trained cyclists, both block and traditional periodization improved 5-minute and 40-minute time-trial power, while the two structures did not differ meaningfully in those performance outcomes. Use this as evidence that either structure may succeed when load and execution fit; it does not justify choosing block periodization from the success label alone.

Source: [No Differences Between 12 Weeks of Block- vs. Traditional-Periodized Training in Performance Adaptations in Trained Cyclists](https://pubmed.ncbi.nlm.nih.gov/35299664/).

### Sprint and strength over multiple seasons — goal-specific context

A case report followed four elite male cross-country mountain-bike cyclists, including riders who added heavy strength training across seasons. It provides useful longitudinal examples for strength and 6-second sprint development, but the sample is very small and the athletes were already elite. Transfer the principle of consistent, low-frequency strength exposure when appropriate; do not copy loads or infer a universal sprint response.

Source: [Effects of Multiple Seasons of Heavy Strength Training on Muscle Strength and Cycling Sprint Power in Elite Cyclists](https://pmc.ncbi.nlm.nih.gov/articles/PMC9082540/).

### Individual response and completion quality — prescription boundary

Cyclists completing interval work prescribed from an individually sustainable interval benchmark achieved better completion than those prescribed from a fixed percentage of incremental-test maximum. This supports checking whether the proposed dose is executable for the athlete rather than matching only a headline percentage.

Source: [Modelling inter-individual variability in acute and adaptive responses to interval training](https://pubmed.ncbi.nlm.nih.gov/37966510/).

## Required output

Return:

- comparison status: `MATCHED`, `CONTEXT_ONLY`, or `NO_VALID_MATCH`;
- the athlete-only thesis;
- selected case cards and why each qualified;
- the delta table with `ADOPT`, `SCALE`, `REJECT`, or `UNKNOWN` decisions;
- the final plan thesis and the first date on which the borrowed assumptions will be checked.
