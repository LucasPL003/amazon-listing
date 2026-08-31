#!/usr/bin/env python3
"""Ingest manual browser, MCP-like, or official-registry evidence deterministically."""

from __future__ import annotations

import argparse
from pathlib import Path
from urllib.parse import urlparse

from common import SOURCE_STATUSES, ensure_object, image_info, jp_candidate_verification_complete, load_json, path_within, sha256_file
from provider_utils import record_result


JP_RECALL_OPERATIONS = {"patent_recall", "design_recall", "trademark_recall"}
JP_OFFICIAL_OPERATIONS = {*JP_RECALL_OPERATIONS, "candidate_verification"}


def validate_jp_payload(operation: str, status: str, normalized: object, source_url: str) -> dict:
    if status not in {"success", "no_result", "needs_user_action", "access_limited", "failed"}:
        raise SystemExit("Japan J-PlatPat recalls do not allow not_applicable")
    if status not in {"success", "no_result"}:
        if normalized not in (None, {}):
            raise SystemExit(f"Japan J-PlatPat {status} evidence cannot include normalized candidates")
        return {}
    if not isinstance(normalized, dict) or normalized.get("operator_confirmed") is not True:
        raise SystemExit("Japan J-PlatPat terminal results require operator-confirmed normalized evidence")
    candidates = normalized.get("candidates")
    if not isinstance(candidates, list):
        raise SystemExit("Japan J-PlatPat normalized evidence requires a candidates array")
    if status == "no_result":
        if candidates or not str(normalized.get("result_message") or "").strip():
            raise SystemExit("Japan J-PlatPat no_result requires an operator-confirmed rendered result message and zero candidates")
        return normalized
    if not candidates:
        raise SystemExit("Japan J-PlatPat success requires at least one candidate")
    allowed_right_types = {
        "patent_recall": {"patent", "utility_model"},
        "design_recall": {"design"},
        "trademark_recall": {"trademark"},
    }
    for candidate in candidates:
        if not isinstance(candidate, dict):
            raise SystemExit("Japan J-PlatPat candidates must be objects")
        right_type = str(candidate.get("right_type") or "").casefold()
        if operation in JP_RECALL_OPERATIONS and right_type not in allowed_right_types[operation]:
            raise SystemExit(f"Japan J-PlatPat {operation} candidate has an invalid right_type")
        identifier = (
            candidate.get("publication_number") or candidate.get("application_number")
            or candidate.get("registration_number") or candidate.get("record_number")
        )
        if not identifier or not str(candidate.get("title") or candidate.get("mark_text") or "").strip():
            raise SystemExit("Japan J-PlatPat candidates require an identifier and title or mark_text")
        candidate.setdefault("jurisdiction", "JP")
        candidate["material"] = True
        candidate.setdefault("official_verification", {
            "status": "not_checked", "source": "J-PlatPat", "url": source_url, "checked_at": "",
        })
        if operation == "candidate_verification" and not jp_candidate_verification_complete(
            "trademark" if right_type == "trademark" else "patent", candidate,
        ):
            raise SystemExit("Japan J-PlatPat candidate_verification is missing required owner, status, and claims/views/goods fields")
    return normalized


def main() -> None:
    parser = argparse.ArgumentParser(description="Record a normalized provider result.")
    parser.add_argument("--task-dir", type=Path, required=True)
    parser.add_argument("--provider", required=True)
    parser.add_argument("--operation", required=True)
    parser.add_argument("--query", required=True)
    parser.add_argument("--jurisdiction", required=True)
    parser.add_argument("--evidence-type", choices=["patent", "trademark", "copyright", "enforcement", "official_verification", "blacklist", "product"], required=True)
    parser.add_argument("--status", choices=sorted(SOURCE_STATUSES), required=True)
    parser.add_argument("--normalized-json", type=Path)
    parser.add_argument("--raw", type=Path)
    parser.add_argument("--error-code", default="")
    parser.add_argument("--detail", default="")
    parser.add_argument("--data-date", default="")
    parser.add_argument("--optional", action="store_true")
    parser.add_argument("--source-url", default="")
    parser.add_argument("--screenshot", type=Path)
    args = parser.parse_args()
    task_dir = args.task_dir.resolve()
    task = ensure_object(load_json(task_dir / "task.json"), "task.json")
    allowed = set(task.get("required_sources", [])) | set(task.get("optional_sources", [])) | set(task.get("low_risk_gate_sources", [])) | {"local_high_risk_ip"}
    if args.provider not in allowed:
        raise SystemExit(f"Provider is not configured for this task: {args.provider}")
    jp_official = args.provider == "official_registry_browser" and args.jurisdiction.upper() == "JP"
    if jp_official and args.evidence_type != "official_verification":
        raise SystemExit("Japan official_registry_browser requires evidence-type official_verification")
    if jp_official and args.operation not in JP_OFFICIAL_OPERATIONS:
        raise SystemExit("Japan official_registry_browser operation must be patent_recall, design_recall, trademark_recall, or candidate_verification")
    normalized = None
    if args.normalized_json:
        normalized = ensure_object(load_json(args.normalized_json), "normalized JSON")
    raw_body = args.raw.read_bytes() if args.raw else b""
    if args.status == "no_result" and not jp_official and normalized not in (None, {}, {"candidates": []}):
        raise SystemExit("no_result requires an empty normalized result")
    if args.status in {"success", "no_result"} and args.error_code:
        raise SystemExit("Successful statuses cannot include an error code")
    request_params = {"q": args.query}
    if args.evidence_type == "official_verification":
        parsed = urlparse(args.source_url)
        if parsed.scheme != "https" or not parsed.hostname:
            raise SystemExit("Official verification requires an HTTPS --source-url")
        if jp_official:
            hostname = parsed.hostname.casefold()
            if hostname != "j-platpat.inpit.go.jp" and not hostname.endswith(".j-platpat.inpit.go.jp"):
                raise SystemExit("Japan official verification requires a J-PlatPat source URL")
        if not args.screenshot:
            raise SystemExit("Official verification requires --screenshot")
        screenshot = args.screenshot.expanduser().resolve()
        if not screenshot.is_file() or not path_within(screenshot, task_dir / "screenshots"):
            raise SystemExit("Official verification screenshot must exist inside task screenshots/")
        try:
            image_info(screenshot)
        except ValueError as exc:
            raise SystemExit("Official verification screenshot must be a readable image") from exc
        screenshot_digest = sha256_file(screenshot)
        if jp_official:
            normalized = validate_jp_payload(args.operation, args.status, normalized, args.source_url)
            if args.operation in JP_RECALL_OPERATIONS:
                evidence = ensure_object(load_json(task_dir / "evidence.json"), "evidence.json")
                reused = any(
                    run.get("provider") == "official_registry_browser"
                    and str(run.get("jurisdiction") or "").upper() == "JP"
                    and run.get("operation") in JP_RECALL_OPERATIONS
                    and run.get("operation") != args.operation
                    and (
                        run.get("request_params", {}).get("screenshot_sha256") == screenshot_digest
                        or run.get("request_params", {}).get("screenshot_path") == str(screenshot)
                    )
                    for run in evidence.get("source_runs", [])
                )
                if reused:
                    raise SystemExit("Japan J-PlatPat recall operations require distinct screenshots")
        request_params.update({
            "source_url": args.source_url,
            "screenshot_path": str(screenshot),
            "screenshot_sha256": screenshot_digest,
        })
        if jp_official:
            request_params.update({
                "operator_confirmed": bool(isinstance(normalized, dict) and normalized.get("operator_confirmed") is True),
                "rendered_result_message": str(normalized.get("result_message") or "") if isinstance(normalized, dict) else "",
            })
        if isinstance(normalized, dict):
            normalized.setdefault("browser_evidence", {}).update({"screenshot_path": str(screenshot), "screenshot_sha256": screenshot_digest})
    run = record_result(task_dir, provider=args.provider, operation=args.operation, query=args.query,
        jurisdiction=args.jurisdiction, evidence_type=args.evidence_type, status=args.status,
        normalized=normalized, raw_body=raw_body, raw_suffix=args.raw.suffix.lstrip(".") if args.raw else "json",
        error_code=args.error_code, detail=args.detail, data_date=args.data_date, mandatory=not args.optional,
        request_params=request_params)
    print(run["run_id"])


if __name__ == "__main__":
    main()
