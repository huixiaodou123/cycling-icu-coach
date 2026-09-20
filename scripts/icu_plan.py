#!/usr/bin/env python3
"""Validate, preview, and deploy cycling workouts to Intervals.icu."""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path
from typing import Any


BASE_URL = "https://intervals.icu/api/v1"
UID_NAMESPACE = uuid.UUID("b9f0946a-7c1d-4b76-a43e-c116eb989e93")
PASSTHROUGH_FIELDS = {
    "moving_time",
    "carbs_per_hour",
    "indoor",
    "color",
    "tags",
    "target",
    "sub_type",
    "calendar_id",
}
PLAN_SCOPES = {"CYCLING_ONLY", "INTEGRATED_PERFORMANCE", "ASSESSMENT_ONLY"}
READINESS_STATUSES = {"FORMAL_READY", "DRAFT_ONLY", "ASSESS_FIRST"}
CASE_COMPARISON_STATUSES = {"NOT_RUN", "MATCHED", "CONTEXT_ONLY", "NO_VALID_MATCH"}
CASE_DELTA_DECISIONS = {"ADOPT", "SCALE", "REJECT", "UNKNOWN"}
PLAN_STYLES = {"CONSERVATIVE", "BALANCED", "AMBITIOUS"}
WORKOUT_DIFFICULTIES = {"EASY", "MANAGEABLE", "CHALLENGING", "VERY_HARD", "UNKNOWN"}
CONFIDENCE_LEVELS = {"HIGH", "MEDIUM", "LOW"}
REQUIRED_INTAKE = {"training", "nutrition", "sleep", "supplements", "health"}
REQUIRED_GOAL_FIELDS = {"primary_metric", "baseline", "target", "horizon", "test_protocol"}


class PlanError(ValueError):
    pass


class ApiError(RuntimeError):
    pass


def load_json(path: str | Path) -> Any:
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise PlanError(f"Plan file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise PlanError(f"Invalid JSON in {path}: {exc}") from exc


def write_json(data: Any, path: str | None) -> None:
    rendered = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    if path:
        Path(path).write_text(rendered, encoding="utf-8")
        print(f"Wrote {path}", file=sys.stderr)
    else:
        print(rendered, end="")


def valid_date(value: Any, label: str) -> str:
    if not isinstance(value, str):
        raise PlanError(f"{label} must be YYYY-MM-DD")
    try:
        dt.date.fromisoformat(value)
    except ValueError as exc:
        raise PlanError(f"{label} must be YYYY-MM-DD: {value!r}") from exc
    return value


def normalized_plan_id(value: Any) -> str:
    if not isinstance(value, str) or not re.fullmatch(r"[a-z0-9][a-z0-9._-]{2,63}", value):
        raise PlanError("plan_id must be 3–64 lowercase letters, numbers, dots, underscores, or hyphens")
    return value


def event_uid(plan_id: str, event: dict[str, Any], index: int) -> str:
    explicit = event.get("uid")
    if explicit is not None:
        if not isinstance(explicit, str) or len(explicit) < 8:
            raise PlanError(f"events[{index}].uid must be a string of at least 8 characters")
        return explicit
    identity = event.get("event_key") or event.get("name")
    seed = f"{plan_id}|{event.get('date')}|{identity}"
    return str(uuid.uuid5(UID_NAMESPACE, seed))


def plan_metadata(plan: dict[str, Any]) -> dict[str, Any]:
    scope = plan.get("plan_scope", "CYCLING_ONLY")
    readiness = plan.get("readiness_status", "DRAFT_ONLY")
    if scope not in PLAN_SCOPES:
        raise PlanError(f"plan_scope must be one of: {', '.join(sorted(PLAN_SCOPES))}")
    if readiness not in READINESS_STATUSES:
        raise PlanError(f"readiness_status must be one of: {', '.join(sorted(READINESS_STATUSES))}")
    goal = plan.get("goal_contract")
    intake = plan.get("intake_confirmed", [])
    comparison = plan.get("case_comparison", {"status": "NOT_RUN"})
    adaptation = plan.get("adaptation_contract")
    if not isinstance(intake, list) or not all(isinstance(item, str) for item in intake):
        raise PlanError("intake_confirmed must be an array of strings")
    if not isinstance(comparison, dict):
        raise PlanError("case_comparison must be an object")
    comparison_status = comparison.get("status", "NOT_RUN")
    if comparison_status not in CASE_COMPARISON_STATUSES:
        raise PlanError(
            f"case_comparison.status must be one of: {', '.join(sorted(CASE_COMPARISON_STATUSES))}"
        )
    cases = comparison.get("cases", [])
    deltas = comparison.get("deltas", [])
    if not isinstance(cases, list) or not all(isinstance(item, dict) for item in cases):
        raise PlanError("case_comparison.cases must be an array of objects")
    if not isinstance(deltas, list) or not all(isinstance(item, dict) for item in deltas):
        raise PlanError("case_comparison.deltas must be an array of objects")
    invalid_decisions = sorted(
        {
            str(item.get("decision"))
            for item in deltas
            if item.get("decision") not in CASE_DELTA_DECISIONS
        }
    )
    if invalid_decisions:
        raise PlanError(
            "case_comparison.deltas decisions must be one of "
            f"{', '.join(sorted(CASE_DELTA_DECISIONS))}; found: {', '.join(invalid_decisions)}"
        )
    if readiness == "FORMAL_READY":
        if not isinstance(goal, dict):
            raise PlanError("FORMAL_READY plans require goal_contract")
        missing_goal = sorted(field for field in REQUIRED_GOAL_FIELDS if not goal.get(field))
        if missing_goal:
            raise PlanError(f"FORMAL_READY goal_contract missing: {', '.join(missing_goal)}")
        missing_intake = sorted(REQUIRED_INTAKE - set(intake))
        if missing_intake:
            raise PlanError(f"FORMAL_READY intake_confirmed missing: {', '.join(missing_intake)}")
        if comparison_status == "NOT_RUN":
            raise PlanError("FORMAL_READY plans require a completed case comparison")
        for field in ("athlete_only_thesis", "final_decision"):
            if not isinstance(comparison.get(field), str) or not comparison[field].strip():
                raise PlanError(f"FORMAL_READY case_comparison.{field} must be non-empty")
        if comparison_status == "MATCHED" and (not cases or not deltas):
            raise PlanError("MATCHED case comparisons require non-empty cases and deltas")
        if not isinstance(adaptation, dict):
            raise PlanError("FORMAL_READY plans require an adaptation_contract")
        style = adaptation.get("plan_style")
        if style not in PLAN_STYLES:
            raise PlanError(
                f"adaptation_contract.plan_style must be one of: {', '.join(sorted(PLAN_STYLES))}"
            )
        committed_through = valid_date(
            adaptation.get("committed_through"), "adaptation_contract.committed_through"
        )
        next_review = valid_date(
            adaptation.get("next_review_date"), "adaptation_contract.next_review_date"
        )
        if next_review > committed_through:
            raise PlanError("adaptation_contract.next_review_date must not follow committed_through")
        review_inputs = adaptation.get("review_inputs")
        if (
            not isinstance(review_inputs, list)
            or not review_inputs
            or not all(isinstance(item, str) and item.strip() for item in review_inputs)
        ):
            raise PlanError("adaptation_contract.review_inputs must be a non-empty array of strings")
        if not isinstance(adaptation.get("change_policy"), str) or not adaptation[
            "change_policy"
        ].strip():
            raise PlanError("adaptation_contract.change_policy must be non-empty")
    return {
        "plan_scope": scope,
        "readiness_status": readiness,
        "goal_contract": goal,
        "intake_confirmed": intake,
        "case_comparison": comparison,
        "adaptation_contract": adaptation,
    }


def build_payloads(plan: dict[str, Any]) -> tuple[str, str, list[dict[str, Any]]]:
    if not isinstance(plan, dict):
        raise PlanError("Plan root must be an object")
    plan_id = normalized_plan_id(plan.get("plan_id"))
    metadata = plan_metadata(plan)
    athlete_id = str(plan.get("athlete_id") or os.getenv("INTERVALS_ICU_ATHLETE_ID") or "0")
    events = plan.get("events")
    if not isinstance(events, list) or not events:
        raise PlanError("events must be a non-empty array")

    payloads: list[dict[str, Any]] = []
    seen_uids: set[str] = set()
    seen_keys: set[tuple[str, str]] = set()
    errors: list[str] = []

    for index, event in enumerate(events):
        prefix = f"events[{index}]"
        if not isinstance(event, dict):
            errors.append(f"{prefix} must be an object")
            continue
        try:
            date = valid_date(event.get("date"), f"{prefix}.date")
            name = event.get("name")
            description = event.get("description")
            if not isinstance(name, str) or not name.strip():
                raise PlanError(f"{prefix}.name must be non-empty")
            if not isinstance(description, str) or not description.strip():
                raise PlanError(f"{prefix}.description must be non-empty")
            if not any(line.lstrip().startswith("-") for line in description.splitlines()):
                raise PlanError(f"{prefix}.description needs at least one dash-prefixed workout step")
            if metadata["readiness_status"] == "FORMAL_READY":
                for field in ("purpose", "fallback"):
                    if not isinstance(event.get(field), str) or not event[field].strip():
                        raise PlanError(f"{prefix}.{field} must be non-empty for FORMAL_READY plans")
                if event.get("difficulty") not in WORKOUT_DIFFICULTIES:
                    raise PlanError(
                        f"{prefix}.difficulty must be one of: "
                        f"{', '.join(sorted(WORKOUT_DIFFICULTIES))}"
                    )
                if event.get("difficulty_confidence") not in CONFIDENCE_LEVELS:
                    raise PlanError(
                        f"{prefix}.difficulty_confidence must be one of: "
                        f"{', '.join(sorted(CONFIDENCE_LEVELS))}"
                    )
                if date > metadata["adaptation_contract"]["committed_through"]:
                    raise PlanError(
                        f"{prefix}.date is after adaptation_contract.committed_through"
                    )
            moving_time = event.get("moving_time")
            if moving_time is not None and (not isinstance(moving_time, int) or moving_time <= 0):
                raise PlanError(f"{prefix}.moving_time must be a positive integer in seconds")
            carbs = event.get("carbs_per_hour")
            if carbs is not None and (not isinstance(carbs, int) or not 0 <= carbs <= 250):
                raise PlanError(f"{prefix}.carbs_per_hour must be an integer from 0 to 250")
            uid = event_uid(plan_id, event, index)
            if uid in seen_uids:
                raise PlanError(f"{prefix}.uid duplicates another event: {uid}")
            event_key = str(event.get("event_key") or name).strip()
            identity = (date, event_key)
            if identity in seen_keys:
                raise PlanError(f"{prefix} duplicates date/event identity: {date} / {event_key}")
            seen_uids.add(uid)
            seen_keys.add(identity)

            payload: dict[str, Any] = {
                "category": "WORKOUT",
                "start_date_local": f"{date}T00:00:00",
                "name": name.strip(),
                "description": description.strip(),
                "type": event.get("type") or "Ride",
                "uid": uid,
                "external_id": f"cycling-icu-coach:{plan_id}:{hashlib.sha1(uid.encode()).hexdigest()[:12]}",
            }
            for field in PASSTHROUGH_FIELDS:
                if field in event and event[field] is not None:
                    payload[field] = event[field]
            payloads.append(payload)
        except PlanError as exc:
            errors.append(str(exc))

    if errors:
        raise PlanError("\n".join(errors))
    payloads.sort(key=lambda item: (item["start_date_local"], item["name"]))
    return plan_id, athlete_id, payloads


def api_request(
    method: str,
    athlete_id: str,
    path: str,
    *,
    query: dict[str, Any] | None = None,
    body: Any | None = None,
) -> Any:
    api_key = os.getenv("INTERVALS_ICU_API_KEY")
    if not api_key:
        raise ApiError("INTERVALS_ICU_API_KEY is not set")
    url = f"{BASE_URL}{path.format(athlete_id=urllib.parse.quote(athlete_id, safe=''))}"
    if query:
        url += "?" + urllib.parse.urlencode(query, doseq=True)
    token = base64.b64encode(f"API_KEY:{api_key}".encode()).decode()
    headers = {"Authorization": f"Basic {token}", "Accept": "application/json"}
    data = None
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            raw = response.read()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:1500]
        raise ApiError(f"Intervals.icu HTTP {exc.code} for {method} {path}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise ApiError(f"Intervals.icu request failed for {method} {path}: {exc.reason}") from exc
    if not raw:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ApiError(f"Intervals.icu returned non-JSON for {method} {path}") from exc


def list_events(athlete_id: str, oldest: str, newest: str) -> list[dict[str, Any]]:
    result = api_request(
        "GET",
        athlete_id,
        "/athlete/{athlete_id}/events",
        query={"oldest": oldest, "newest": newest, "category": "WORKOUT"},
    )
    if not isinstance(result, list):
        raise ApiError("Intervals.icu events response was not an array")
    return result


def events_equivalent(current: dict[str, Any], desired: dict[str, Any]) -> bool:
    """Compare only fields owned by the desired payload, ignoring server defaults."""
    for key, expected in desired.items():
        actual = current.get(key)
        if key == "description" and isinstance(actual, str):
            if actual.strip() != str(expected).strip():
                return False
        elif key == "start_date_local" and isinstance(actual, str):
            if actual[:19] != str(expected)[:19]:
                return False
        elif key == "tags" and isinstance(actual, list) and isinstance(expected, list):
            if sorted(actual) != sorted(expected):
                return False
        elif actual != expected:
            return False
    return True


def activity_data_quality(activities: Any) -> dict[str, Any]:
    """Summarize whether activity rows contain training data or restricted stubs."""
    if not isinstance(activities, list):
        return {
            "activities_returned": 0,
            "usable_activity_rows": 0,
            "restricted_activity_stubs": 0,
            "warning": "Activities response was not an array",
        }
    training_fields = {
        "moving_time",
        "distance",
        "icu_training_load",
        "icu_average_watts",
        "average_heartrate",
        "type",
        "name",
    }
    restricted = sum(
        isinstance(item, dict) and bool(item.get("_note"))
        for item in activities
    )
    usable = sum(
        isinstance(item, dict)
        and any(item.get(field) is not None for field in training_fields)
        for item in activities
    )
    warning = None
    if activities and usable == 0:
        warning = (
            "Activity rows contain no usable training fields. The source may restrict API detail; "
            "use a logged-in browser or athlete export before planning."
        )
    return {
        "activities_returned": len(activities),
        "usable_activity_rows": usable,
        "restricted_activity_stubs": restricted,
        "warning": warning,
    }


def preview_rows(athlete_id: str, payloads: list[dict[str, Any]]) -> list[dict[str, Any]]:
    oldest = min(item["start_date_local"][:10] for item in payloads)
    newest = max(item["start_date_local"][:10] for item in payloads)
    existing = list_events(athlete_id, oldest, newest)
    by_uid = {item.get("uid"): item for item in existing if item.get("uid")}
    rows = []
    for payload in payloads:
        current = by_uid.get(payload["uid"])
        if current is None:
            action = "CREATE"
        elif events_equivalent(current, payload):
            action = "UNCHANGED"
        else:
            action = "UPDATE"
        rows.append(
            {
                "action": action,
                "date": payload["start_date_local"][:10],
                "name": payload["name"],
                "uid": payload["uid"],
                "existing_event_id": current.get("id") if current else None,
            }
        )
    return rows


def cmd_template(args: argparse.Namespace) -> None:
    start = dt.date.today() + dt.timedelta(days=1)
    template = {
        "plan_id": "example-cycling-plan",
        "athlete_id": args.athlete_id or "0",
        "timezone": "Asia/Shanghai",
        "plan_scope": "CYCLING_ONLY",
        "readiness_status": "DRAFT_ONLY",
        "goal_contract": {
            "primary_metric": "",
            "baseline": "",
            "target": "",
            "horizon": "",
            "test_protocol": "",
        },
        "intake_confirmed": [],
        "case_comparison": {
            "status": "NOT_RUN",
            "athlete_only_thesis": "",
            "cases": [],
            "deltas": [],
            "final_decision": "",
            "assumption_check_date": "",
        },
        "adaptation_contract": {
            "plan_style": "BALANCED",
            "committed_through": (start + dt.timedelta(days=13)).isoformat(),
            "next_review_date": (start + dt.timedelta(days=6)).isoformat(),
            "review_inputs": [
                "completion",
                "RPE",
                "interval fade",
                "sleep",
                "soreness",
                "fueling",
            ],
            "change_policy": "Re-compose only the upcoming week and preserve session purpose.",
        },
        "events": [
            {
                "date": start.isoformat(),
                "event_key": "endurance-01",
                "name": "耐力骑",
                "type": "Ride",
                "purpose": "稳定耐力并观察后半程体感",
                "difficulty": "MANAGEABLE",
                "difficulty_confidence": "LOW",
                "fallback": "缩短为 40 分钟轻松骑",
                "description": "目标：稳定耐力。\n退出条件：异常疲劳则缩短。\n\nWarmup\n- 10m 50-60%\n\nEndurance\n- 50m 60-70%\n\nCooldown\n- 10m 50-60%",
                "moving_time": 4200,
                "carbs_per_hour": 30,
                "tags": ["cycling-icu-coach", "endurance"],
            }
        ],
    }
    write_json(template, args.output)


def cmd_validate(args: argparse.Namespace) -> None:
    plan = load_json(args.plan)
    plan_id, athlete_id, payloads = build_payloads(plan)
    metadata = plan_metadata(plan)
    result = {
        "valid": True,
        "plan_id": plan_id,
        "athlete_id": athlete_id,
        "events": len(payloads),
        **metadata,
    }
    write_json(result, None)


def cmd_render(args: argparse.Namespace) -> None:
    plan = load_json(args.plan)
    plan_id, athlete_id, payloads = build_payloads(plan)
    write_json({"plan_id": plan_id, "athlete_id": athlete_id, **plan_metadata(plan), "events": payloads}, args.output)


def cmd_snapshot(args: argparse.Namespace) -> None:
    athlete_id = str(args.athlete_id or os.getenv("INTERVALS_ICU_ATHLETE_ID") or "0")
    try:
        newest_date = dt.date.fromisoformat(args.newest) if args.newest else dt.date.today()
    except ValueError as exc:
        raise PlanError(f"--newest must be YYYY-MM-DD: {args.newest!r}") from exc
    oldest_date = newest_date - dt.timedelta(days=args.days - 1)
    oldest, newest = oldest_date.isoformat(), newest_date.isoformat()
    activity_fields = (
        "id,name,type,start_date_local,moving_time,distance,icu_training_load,icu_intensity,"
        "icu_average_watts,icu_weighted_avg_watts,average_heartrate,icu_ftp,icu_rpe,feel,"
        "decoupling,icu_efficiency_factor,carbs_ingested,calories,icu_ctl,icu_atl"
    )
    wellness_fields = (
        "id,ctl,atl,rampRate,weight,restingHR,hrv,sleepSecs,sleepQuality,fatigue,soreness,"
        "stress,mood,motivation,readiness,injury,comments"
    )
    snapshot = {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "range": {"oldest": oldest, "newest": newest},
        "athlete": api_request("GET", athlete_id, "/athlete/{athlete_id}"),
        "power_model": api_request(
            "GET",
            athlete_id,
            "/athlete/{athlete_id}/mmp-model",
            query={"type": "Ride"},
        ),
        "power_curves": api_request(
            "GET",
            athlete_id,
            "/athlete/{athlete_id}/power-curves.json",
            query={"type": "Ride", "curves": ["42d", "1y"]},
        ),
        "activities": api_request(
            "GET",
            athlete_id,
            "/athlete/{athlete_id}/activities",
            query={"oldest": oldest, "newest": newest, "fields": activity_fields},
        ),
        "wellness": api_request(
            "GET",
            athlete_id,
            "/athlete/{athlete_id}/wellness",
            query={"oldest": oldest, "newest": newest, "fields": wellness_fields},
        ),
        "events": list_events(athlete_id, oldest, newest),
    }
    snapshot["data_quality"] = activity_data_quality(snapshot["activities"])
    write_json(snapshot, args.output)


def cmd_preview(args: argparse.Namespace) -> None:
    plan_id, plan_athlete_id, payloads = build_payloads(load_json(args.plan))
    athlete_id = str(args.athlete_id or plan_athlete_id)
    rows = preview_rows(athlete_id, payloads)
    counts = {key: sum(row["action"] == key for row in rows) for key in ("CREATE", "UPDATE", "UNCHANGED")}
    write_json({"plan_id": plan_id, "athlete_id": athlete_id, "counts": counts, "events": rows}, None)


def cmd_deploy(args: argparse.Namespace) -> None:
    plan = load_json(args.plan)
    plan_id, plan_athlete_id, payloads = build_payloads(plan)
    metadata = plan_metadata(plan)
    if metadata["readiness_status"] != "FORMAL_READY":
        raise PlanError("Only FORMAL_READY plans can be deployed; complete the intake and goal contract first")
    if metadata["plan_scope"] == "ASSESSMENT_ONLY":
        raise PlanError("ASSESSMENT_ONLY plans cannot be deployed")
    if args.confirm != plan_id:
        raise PlanError(f"--confirm must exactly match plan_id: {plan_id}")
    athlete_id = str(args.athlete_id or plan_athlete_id)
    before = preview_rows(athlete_id, payloads)
    results = []
    failure: ApiError | None = None
    for row, payload in zip(before, payloads):
        if row["action"] == "UNCHANGED":
            results.append({**row, "result": "SKIPPED"})
            continue
        try:
            response = api_request(
                "POST",
                athlete_id,
                "/athlete/{athlete_id}/events",
                query={"upsertOnUid": "true"},
                body=payload,
            )
        except ApiError as exc:
            results.append({**row, "result": "FAILED", "error": str(exc)})
            failure = exc
            break
        results.append(
            {
                **row,
                "result": "WRITTEN",
                "event_id": response.get("id") if isinstance(response, dict) else None,
                "push_errors": response.get("push_errors") if isinstance(response, dict) else None,
            }
        )
    receipt = {
        "plan_id": plan_id,
        "athlete_id": athlete_id,
        "deployed_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "events": results,
    }
    write_json(receipt, args.receipt)
    if failure:
        completed = sum(item["result"] == "WRITTEN" for item in results)
        raise ApiError(f"Deployment stopped after {completed} successful write(s): {failure}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    template = subparsers.add_parser("template", help="Write a starter plan JSON")
    template.add_argument("--output", required=True)
    template.add_argument("--athlete-id")
    template.set_defaults(func=cmd_template)

    validate = subparsers.add_parser("validate", help="Validate a plan offline")
    validate.add_argument("plan")
    validate.set_defaults(func=cmd_validate)

    render = subparsers.add_parser("render", help="Render exact API payloads offline")
    render.add_argument("plan")
    render.add_argument("--output")
    render.set_defaults(func=cmd_render)

    snapshot = subparsers.add_parser("snapshot", help="Read recent athlete data")
    snapshot.add_argument("--days", type=int, default=56)
    snapshot.add_argument("--newest", help="Latest local date, YYYY-MM-DD")
    snapshot.add_argument("--athlete-id")
    snapshot.add_argument("--output")
    snapshot.set_defaults(func=cmd_snapshot)

    preview = subparsers.add_parser("preview", help="Compare a plan with the live calendar")
    preview.add_argument("plan")
    preview.add_argument("--athlete-id")
    preview.set_defaults(func=cmd_preview)

    deploy = subparsers.add_parser("deploy", help="Create or update the reviewed plan")
    deploy.add_argument("plan")
    deploy.add_argument("--athlete-id")
    deploy.add_argument("--confirm", required=True, help="Must exactly match plan_id")
    deploy.add_argument("--receipt")
    deploy.set_defaults(func=cmd_deploy)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if getattr(args, "days", 1) < 1:
        parser.error("--days must be at least 1")
    try:
        args.func(args)
    except (PlanError, ApiError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
