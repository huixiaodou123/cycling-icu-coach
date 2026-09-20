# Mandatory intake before a formal plan

Complete this intake before calling a plan formal or deploying it to Intervals.icu. Do not show this full checklist to the user. Follow the two-round flow in [guided-experience.md](guided-experience.md), ask at most five short questions per message, and extract answers from normal prose. An explicit “none”, “unknown”, an approximation, or “I prefer not to answer” counts as an answer; record the resulting limitation. Never repeat a question already answered in the conversation or connected data.

## 0. Choose the plan scope

Let the user choose in plain language. Keep these internal labels out of the main user-facing choice:

- `CYCLING_ONLY`: only cycling workouts, tests, rest days, and cycling-load adjustments in the final plan.
- `INTEGRATED_PERFORMANCE`: also include strength, fueling practice, sleep/recovery actions, and justified supplement trials.
- `ASSESSMENT_ONLY`: analyze the current profile and collect better baseline data before planning.

All modes still complete a short nutrition, sleep, supplement, and health screen because those factors change training interpretation. In `CYCLING_ONLY`, use the answers only to set constraints, bailout rules, and recovery decisions unless the user later expands scope.

## 1. Goal contract

An event is optional. Choose one primary goal and no more than two secondary goals for the current block.

For every selected goal record:

- metric and duration;
- current baseline and date;
- target value or target range;
- target date or block length;
- repeatable test protocol and equipment;
- why the goal matters and its priority.
- preferred comparison source: the athlete's own successful history, matched research/cases, or both; default to both when available.

Examples include:

- FTP or critical power;
- absolute power for 5 s, 15 s, 1 min, 5 min, 20 min, or another target duration;
- power-to-weight for a defined duration;
- P-max, acceleration, or seated/standing sprint;
- W′/FRC, 30 s–3 min capacity, or repeated severe efforts;
- durability: power, threshold, or sprint ability after a specified amount of prior work;
- aerobic endurance, consistency, health, or enjoyment;
- a race, tour, time trial, climb, or other event.

Do not accept “get stronger” or “raise watts/kg” as the complete contract. Define the duration and test.

## 2. Training and equipment

- last 6–8 weeks: weekly hours, frequency, load if available, longest ride, hard sessions, breaks;
- cycling age and recent block history;
- current FTP/CP and test method/date;
- recent best power at 1–5 s, 15 s, 30 s, 1 min, 3–5 min, 12–20 min, and longer durations where available;
- Intervals.icu P-max, W′, power model, power curve, and fatigued curve when available;
- power meter/trainer availability and type, calibration habits, indoor/outdoor difference; if there is no power meter, record the heart-rate sensor type and whether it is worn consistently;
- exact weekly time windows, fixed rest days, gym access, terrain, and group rides;
- current pain, injury, illness, and medication that changes exercise response.

Sparse maximal efforts make P-max, W′, and model estimates unreliable. Label gaps and schedule safe familiarization or testing before prescribing from the model.

## 3. Eating and training fuel

Ask before setting workload, body-mass goals, or fueling targets:

- typical daily meal pattern and appetite;
- dietary pattern, allergies, intolerances, and foods avoided;
- current body mass trend and whether weight change is a goal;
- history of aggressive restriction, persistently low energy intake, or training while under-fueled;
- food before and after training;
- carbohydrate and fluid intake during easy, hard, and long rides;
- maximum carbohydrate rate already tolerated and any GI symptoms;
- sweat rate clues, salt loss, heat exposure, and hydration habits;
- caffeine amount/timing and alcohol frequency;
- practical constraints such as budget, cooking, travel, and work schedule.

For power-to-weight goals, model both numerator and denominator. Prefer improving power unless a health-compatible body-composition change is explicitly supported by the intake. Do not create an aggressive weight-loss target or diagnose RED-S.

## 4. Sleep and recovery

- usual bedtime/wake time on workdays and free days;
- actual sleep duration, sleep opportunity, and perceived sleep need;
- sleep quality, awakenings, difficulty falling asleep, and daytime sleepiness;
- shift work, childcare, travel, early training, and screen habits;
- naps and their timing;
- late caffeine, alcohol, or supplements that may affect sleep;
- loud snoring, witnessed breathing pauses, or persistent insomnia symptoms;
- current life stress, soreness, motivation, and recovery preferences.

Do not reduce sleep to a universal “8 hours” rule or trust one wearable score. Use the athlete's pattern and perceived need. Persistent insomnia, breathing pauses, or severe daytime sleepiness warrants professional assessment.

## 5. Supplements and sports products

Ask for every regularly or occasionally used product:

- exact product/brand and ingredient list;
- dose, timing, frequency, and duration of use;
- intended purpose and perceived effect;
- side effects or GI response;
- third-party batch testing/certification when competition rules matter;
- prescribed medicines and known medical conditions relevant to interactions;
- diagnosed deficiencies and the clinician/dietitian overseeing treatment.

Prompt specifically for caffeine/pre-workout products, creatine, beta-alanine, bicarbonate, nitrate/beetroot, protein, carbohydrate/electrolyte products, vitamins/minerals, iron, herbal products, ketones, and “fat burners”. “None” is a valid answer.

Classify a supplement decision by safety, legality, evidence, relevance to the exact goal, dose, and trial plan. Food and adequate energy availability come first. Do not recommend correcting iron, vitamin D, or another clinical deficiency without appropriate testing and qualified oversight.

Authoritative reference: [Australian Institute of Sport Supplement Framework](https://www.ais.gov.au/nutrition/supplements). Sleep reference: [Sleep and the athlete consensus](https://pubmed.ncbi.nlm.nih.gov/33144349/).

## Readiness status

Use one of these labels:

- `FORMAL_READY`: goal contract, training availability/history, nutrition, sleep, supplements, and health questions are sufficiently answered.
- `DRAFT_ONLY`: important answers are missing or measurement quality is too poor. Discuss options and collect data; do not deploy a multi-week plan.
- `ASSESS_FIRST`: symptoms or risks require appropriate health, nutrition, or sleep assessment before normal progression.

Show the status and unresolved items before presenting the plan.
