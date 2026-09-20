#!/usr/bin/env python3
"""Offline contract tests for cycling-icu-coach discovery and safety gates."""

from __future__ import annotations

import argparse
import contextlib
import importlib.util
import io
import json
import re
import tempfile
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_helper():
    path = SKILL_DIR / "scripts" / "icu_plan.py"
    spec = importlib.util.spec_from_file_location("cycling_icu_plan", path)
    require(spec is not None and spec.loader is not None, "cannot load icu_plan.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def base_plan() -> dict:
    return {
        "plan_id": "self-test-plan",
        "athlete_id": "0",
        "plan_scope": "CYCLING_ONLY",
        "readiness_status": "DRAFT_ONLY",
        "goal_contract": {
            "primary_metric": "20 min power",
            "baseline": "280 W",
            "target": "295 W",
            "horizon": "8 weeks",
            "test_protocol": "same trainer and warm-up",
        },
        "intake_confirmed": [],
        "case_comparison": {
            "status": "NOT_RUN",
            "athlete_only_thesis": "",
            "cases": [],
            "deltas": [],
            "final_decision": "",
        },
        "events": [
            {
                "date": "2026-10-01",
                "event_key": "threshold-01",
                "name": "Threshold",
                "description": "Main set\n- 3x 10m 95-100%\n- 5m 55-65%",
                "moving_time": 3600,
            }
        ],
    }


def test_discovery_contract() -> None:
    skill_text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    frontmatter = skill_text.split("---", 2)[1]
    description = next(
        line.split(":", 1)[1].strip()
        for line in frontmatter.splitlines()
        if line.startswith("description:")
    ).lower()
    config = (SKILL_DIR / "agents" / "openai.yaml").read_text(encoding="utf-8")
    require("name: cycling-icu-coach" in frontmatter, "skill name does not match directory")
    require("$cycling-icu-coach" in config, "default prompt cannot explicitly invoke the skill")
    require(
        bool(re.search(r"allow_implicit_invocation:\s*true", config)),
        "implicit invocation is not enabled explicitly",
    )
    positives = [
        "ftp",
        "absolute power",
        "power-to-weight",
        "anaerobic capacity",
        "durability",
        "sprinting",
        "matched case benchmarking",
        "intervals.icu",
    ]
    negatives = [
        "bike shopping",
        "equipment repair",
        "race news",
        "running-only",
        "medical rehabilitation",
    ]
    require(all(term in description for term in positives), "positive trigger coverage is incomplete")
    require(all(term in description for term in negatives), "negative trigger boundaries are incomplete")


def test_guided_experience_contract() -> None:
    skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    guided = (SKILL_DIR / "references" / "guided-experience.md").read_text(encoding="utf-8")
    handoff = (SKILL_DIR / "references" / "agent-handoff.md").read_text(encoding="utf-8")
    scenarios = (SKILL_DIR / "references" / "acceptance-scenarios.md").read_text(
        encoding="utf-8"
    )
    required_skill_phrases = [
        "Ask no more than five short questions",
        "Do not ask the user to run commands",
        "Use the capability ladder",
        "meta request",
    ]
    require(
        all(phrase in skill for phrase in required_skill_phrases),
        "guided conversation rules are missing from SKILL.md",
    )
    required_guided_phrases = [
        "The user does not operate the skill",
        "No sensors",
        "Heart rate only",
        "Never strand the user",
    ]
    require(
        all(phrase in guided for phrase in required_guided_phrases),
        "guided experience is missing a required fallback",
    )
    require('"stage": "DISCOVER"' in handoff, "portable handoff state is missing")
    for scenario_id in (
        "BEGINNER_MINIMAL",
        "NO_RACE",
        "NO_POWER",
        "BROWSER_DATA",
        "NO_TOOLS",
        "CASE_DELTA",
        "META_WORK",
        "OUT_OF_SCOPE",
    ):
        require(scenario_id in scenarios, f"acceptance scenario is missing: {scenario_id}")


def test_plan_gates() -> None:
    helper = load_helper()
    draft = base_plan()
    helper.build_payloads(draft)

    formal = json.loads(json.dumps(draft))
    formal["readiness_status"] = "FORMAL_READY"
    formal["intake_confirmed"] = ["training", "nutrition", "sleep", "supplements", "health"]
    try:
        helper.build_payloads(formal)
    except helper.PlanError as exc:
        require("completed case comparison" in str(exc), "wrong missing-comparison error")
    else:
        raise AssertionError("formal plan without case comparison was accepted")

    formal["case_comparison"] = {
        "status": "MATCHED",
        "athlete_only_thesis": "Use two key sessions within recently tolerated load.",
        "cases": [{"source": "own prior block", "match_reason": "same goal and schedule"}],
        "deltas": [
            {
                "dimension": "threshold minutes",
                "baseline": "30",
                "case": "40",
                "decision": "SCALE",
                "reason": "start at 32",
            }
        ],
        "final_decision": "Progress toward the previously tolerated dose.",
        "assumption_check_date": "2026-10-15",
    }
    helper.build_payloads(formal)

    with tempfile.TemporaryDirectory() as temp_dir:
        temp = Path(temp_dir)
        plan_path = temp / "plan.json"
        receipt_path = temp / "receipt.json"
        plan_path.write_text(json.dumps(formal), encoding="utf-8")
        _, _, payloads = helper.build_payloads(formal)
        helper.preview_rows = lambda athlete_id, events: [
            {
                "action": "CREATE",
                "date": item["start_date_local"][:10],
                "name": item["name"],
                "uid": item["uid"],
                "existing_event_id": None,
            }
            for item in events
        ]
        helper.api_request = lambda *args, **kwargs: {"id": "mock-event"}
        args = argparse.Namespace(
            plan=str(plan_path), athlete_id=None, confirm="self-test-plan", receipt=str(receipt_path)
        )
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            helper.cmd_deploy(args)
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        require(receipt["events"][0]["result"] == "WRITTEN", "mock deployment did not write")
        require(len(payloads) == 1, "unexpected payload count")


def test_activity_quality_detection() -> None:
    helper = load_helper()
    quality = helper.activity_data_quality(
        [
            {
                "id": "stub",
                "source": "STRAVA",
                "_note": "STRAVA activities are not available via the API",
            },
            {"id": "usable", "type": "Ride", "moving_time": 3600},
        ]
    )
    require(quality["activities_returned"] == 2, "activity count is wrong")
    require(quality["usable_activity_rows"] == 1, "usable activity count is wrong")
    require(quality["restricted_activity_stubs"] == 1, "restricted stub count is wrong")


def main() -> None:
    test_discovery_contract()
    test_guided_experience_contract()
    test_plan_gates()
    test_activity_quality_detection()
    print(
        "PASS: discovery metadata, guided UX contract, case-comparison gate, "
        "activity-quality detection, payload build, and mock deployment"
    )


if __name__ == "__main__":
    main()
