# Agent-neutral handoff contract

Use this contract so another capable agent can continue without repeating the interview. It does not depend on Codex, a particular browser, or a particular connector.

## Portable state

Maintain a small state object in working memory or a private local artifact when the environment supports files:

```json
{
  "schema_version": 1,
  "stage": "DISCOVER",
  "user_language": "zh-CN",
  "goal_contract": {
    "primary_metric": null,
    "baseline": null,
    "target": null,
    "horizon": null,
    "test_protocol": null,
    "event_optional": true
  },
  "plan_scope": null,
  "equipment": {
    "power_meter": "unknown",
    "heart_rate_sensor": "unknown",
    "smart_trainer": "unknown"
  },
  "data_sources": [],
  "data_quality": [],
  "intake": {
    "training": "missing",
    "nutrition": "missing",
    "sleep": "missing",
    "supplements": "missing",
    "health": "missing"
  },
  "readiness_status": "DRAFT_ONLY",
  "case_comparison_status": "NOT_RUN",
  "assumptions": [],
  "unresolved": [],
  "next_action": null
}
```

Allowed stages are `DISCOVER`, `ACQUIRE_DATA`, `SCREEN`, `ASSESS`, `DRAFT`, `COMPARE`, `PREVIEW`, `READY`, and `DEPLOYED`.

Do not store API keys, access tokens, full medical history, precise home locations, or unrelated private data in this state. Store only the minimum conclusion needed for planning, such as “health screen answered; no reported issue” or “heart-rate threshold unverified”.

## Handoff behavior

On receipt of prior state:

1. Trust completed answers unless newer user input contradicts them.
2. Recheck time-sensitive data such as recent activities, health status, calendar availability, and platform connection.
3. Continue from `next_action`; do not restart the full intake.
4. Explain any conflict in plain language and update the state.
5. Keep technical artifacts linked to the state but outside the user-facing summary.

If no portable state exists, reconstruct it from the conversation before asking questions.

## Tool independence

- With an API or connector, use structured reads and local validation.
- With a logged-in browser, use visible pages and read-only requests first.
- With files, parse exports locally.
- With none of these, use conversation estimates and mark confidence.

The coaching logic, intake gates, case comparison, and user-facing preview remain the same across tool environments.
