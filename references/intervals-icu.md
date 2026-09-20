# Intervals.icu integration

This integration was checked against the live Intervals.icu OpenAPI document on 2026-09-20.

Official sources: [API documentation](https://intervals.icu/api-docs.html), [API access guide](https://forum.intervals.icu/t/api-access-to-intervals-icu/609), [Workout Builder](https://forum.intervals.icu/t/workout-builder/1163).

## Credentials

Create a personal API key under Intervals.icu Settings → Developer Settings. Personal access uses HTTP Basic authentication with username `API_KEY` and the API key as password. Athlete ID `0` means the athlete associated with the credential.

Set credentials only in the process environment:

```bash
export INTERVALS_ICU_API_KEY='...'
export INTERVALS_ICU_ATHLETE_ID='0'
```

Never write the key into a plan, command transcript, note, receipt, or skill file. Multi-user applications must use OAuth; this helper is for personal/coached-athlete workflows.

## Helper commands

```bash
python scripts/icu_plan.py template --output /tmp/cycling-plan.json
python scripts/icu_plan.py validate /tmp/cycling-plan.json
python scripts/icu_plan.py render /tmp/cycling-plan.json
python scripts/icu_plan.py snapshot --days 56 --output /tmp/icu-snapshot.json
python scripts/icu_plan.py preview /tmp/cycling-plan.json
python scripts/icu_plan.py deploy /tmp/cycling-plan.json --confirm PLAN_ID --receipt /tmp/icu-receipt.json
```

All commands accept `--athlete-id`; otherwise the script uses `INTERVALS_ICU_ATHLETE_ID` or `0`. `validate` and `render` are offline. `snapshot`, `preview`, and `deploy` require the API key.

## Plan JSON

```json
{
  "plan_id": "autumn-gran-fondo-2026",
  "athlete_id": "0",
  "timezone": "Asia/Shanghai",
  "plan_scope": "CYCLING_ONLY",
  "readiness_status": "FORMAL_READY",
  "goal_contract": {
    "primary_metric": "20 分钟绝对功率",
    "baseline": "280 W，2026-09-01，同一台骑行台",
    "target": "295–300 W",
    "horizon": "8 周",
    "test_protocol": "同一骑行台、同一热身、20 分钟最大稳定输出"
  },
  "intake_confirmed": ["training", "nutrition", "sleep", "supplements", "health"],
  "case_comparison": {
    "status": "MATCHED",
    "athlete_only_thesis": "从近期可耐受训练量起步，每周安排两次关键骑行。",
    "cases": [
      {
        "source": "用户本人上一成功训练块",
        "match_reason": "目标、测试设备、周时长和生活条件一致"
      }
    ],
    "deltas": [
      {
        "dimension": "阈值总时长",
        "baseline": "每周 30 分钟",
        "case": "每周 40 分钟时完成率良好",
        "decision": "SCALE",
        "reason": "先从 32 分钟开始，根据完成质量增加"
      }
    ],
    "final_decision": "保留两次关键骑行，将阈值总时长渐进到历史有效剂量。",
    "assumption_check_date": "2026-10-06"
  },
  "events": [
    {
      "date": "2026-09-22",
      "name": "耐力 + 低量冲刺",
      "type": "Ride",
      "description": "目标：轻松耐力并保持神经募集。\n退出条件：热身后仍异常疲劳则只骑 Z1–Z2。\n补给：按已验证耐受量。\n\nWarmup\n- 15m 50-65%\n\nMain set 4x\n- 10s 150% 100-120rpm\n- 5m 55-65%\n\nEndurance\n- 45m 60-70%\n\nCooldown\n- 10m 50-60%",
      "moving_time": 5400,
      "carbs_per_hour": 40,
      "indoor": false,
      "tags": ["cycling-icu-coach", "endurance"]
    }
  ]
}
```

Required fields are `plan_id`, a non-empty `events` array, and for every event `date`, `name`, and `description`. The helper creates a deterministic `uid` from `plan_id`, date, and event identity. An explicit `uid` may be provided but must be unique within the plan.

`plan_scope` is `CYCLING_ONLY`, `INTEGRATED_PERFORMANCE`, or `ASSESSMENT_ONLY`. `readiness_status` is `DRAFT_ONLY` until the intake is complete. Live deployment requires `FORMAL_READY`, a complete `goal_contract`, confirmation flags for training, nutrition, sleep, supplements, and health, and a completed `case_comparison`. Its status is `MATCHED`, `CONTEXT_ONLY`, or `NO_VALID_MATCH`; `NOT_RUN` is valid only before the formal plan. Delta decisions are `ADOPT`, `SCALE`, `REJECT`, or `UNKNOWN`. Store only completion flags and concise comparison conclusions in this file, not sensitive intake answers.

Optional event fields passed through are `type`, `moving_time`, `carbs_per_hour`, `indoor`, `color`, `tags`, `target`, `sub_type`, and `calendar_id`. Default `type` is `Ride`; category is always `WORKOUT`.

## Native workout text

Intervals.icu parses the `description` field. Use headings or coaching notes as plain lines and steps as dash-prefixed lines. A repeat header ends in `Nx` and is followed by its steps.

```text
Warmup
- 15m 50-70% 85-95rpm

Main set 4x
- 5m 108-115%
- 5m 50-60%

Cooldown
- 10m 50-60%
```

Useful forms include fixed or ranged `%FTP`, cadence ranges such as `85-95rpm`, ramps, and HR targets such as `Z2 HR`. Use one primary target system per workout unless a secondary metric is clearly a cross-check in prose.

For athletes without a power meter, use `Z2 HR`, `% LTHR`, duration, cadence, and coaching notes only after the heart-rate anchor is validated. Intervals.icu's developer states that its LTHR suggestion uses 98% of the best 20-minute average heart rate or 100% of the best one-hour average. A stored LTHR with no supporting heart-rate activity is only a setting, not a measurement. Source: [Intervals.icu LTHR calculation](https://forum.intervals.icu/t/threshold-hr-value/39988/2).

## Safe deployment flow

1. Validate dates, duplicate identities, duration, and structured steps offline.
2. Render exact payloads and review coaching notes and targets.
3. Preview against live events across the plan date range. The preview reports create, update, or unchanged by UID.
4. Deploy only the reviewed `FORMAL_READY` plan. The helper requires `--confirm` to equal `plan_id`; incomplete case comparisons, `DRAFT_ONLY`, `ASSESS_FIRST`, and `ASSESSMENT_ONLY` plans are refused.
5. Keep the receipt. If a request fails, the helper stops and reports which earlier events were written.

Deployment uses `POST /api/v1/athlete/{id}/events?upsertOnUid=true`. It never bulk-deletes calendar entries. Stable UIDs allow the same plan to be revised without duplicates, while unrelated events are untouched.

## Snapshot content

`snapshot` reads athlete settings, the Ride power model, 42-day and one-year power curves, recent activities, wellness, and calendar events for the selected range. Sport settings expose FTP, P-max, W′, zones, and body mass when configured. Use curve coverage to judge whether model values are trustworthy; a missing maximal duration is not a zero. Treat blank wellness fields as missing, not as zero. Minimize copied data and do not place a private snapshot in permanent notes unless the user explicitly asks.

Some connected sources restrict activity detail returned through the Intervals.icu API. For example, an activity row may contain an ID, date, source, and `_note` such as `STRAVA activities are not available via the API`, while omitting duration, distance, power, heart rate, and load. The helper reports these under `data_quality.restricted_activity_stubs`. Do not count these as usable training sessions. Use the logged-in browser under the workspace browser rules or ask for an athlete export, then record which fields are still missing.
