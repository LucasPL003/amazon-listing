from __future__ import annotations

import base64
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = SKILL_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from common import now_iso, required_providers  # noqa: E402
from finalize_assessment import material_unverified, source_gaps  # noqa: E402


PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
)


class JapanProviderRoutingTests(unittest.TestCase):
    def test_japan_uses_official_registry_without_requiring_signa(self) -> None:
        providers = required_providers(["JP"])

        self.assertIn("epo_ops", providers)
        self.assertIn("official_registry_browser", providers)
        self.assertNotIn("signa", providers)

    def test_eu_still_requires_signa_and_euipo(self) -> None:
        providers = required_providers(["EU"])

        self.assertIn("signa", providers)
        self.assertIn("euipo_trademark", providers)
        self.assertIn("euipo_design", providers)

    def test_us_routing_is_unchanged(self) -> None:
        providers = required_providers(["US"])

        self.assertIn("uspto_tmsearch_browser", providers)
        self.assertIn("uspto_tsdr", providers)
        self.assertNotIn("signa", providers)


class JapanOfficialRegistryCoverageTests(unittest.TestCase):
    def source_run(
        self,
        operation: str,
        status: str = "success",
        screenshot_hash: str | None = None,
        evidence_type: str = "official_verification",
    ) -> dict[str, object]:
        return {
            "provider": "official_registry_browser",
            "operation": operation,
            "status": status,
            "jurisdiction": "JP",
            "evidence_type": evidence_type,
            "request_params": {
                "operator_confirmed": True,
                "rendered_result_message": "Rendered result checked",
                "screenshot_sha256": screenshot_hash or f"hash-{operation}",
            },
        }

    def test_japan_requires_patent_design_and_trademark_registry_recall(self) -> None:
        task = {
            "target_jurisdictions": ["JP"],
            "required_sources": ["official_registry_browser"],
        }
        evidence = {
            "source_runs": [
                self.source_run("patent_recall"),
                self.source_run("trademark_recall", "no_result"),
            ]
        }

        gaps = source_gaps(task, evidence, {"patents": [], "trademarks": []}, {})

        self.assertEqual(gaps, ["official_registry_browser"])

    def test_japan_registry_coverage_is_complete_after_all_three_recalls(self) -> None:
        task = {
            "target_jurisdictions": ["JP"],
            "required_sources": ["official_registry_browser"],
        }
        evidence = {
            "source_runs": [
                self.source_run("patent_recall"),
                self.source_run("design_recall", "no_result"),
                self.source_run("trademark_recall"),
            ]
        }

        gaps = source_gaps(task, evidence, {"patents": [], "trademarks": []}, {})

        self.assertEqual(gaps, [])

    def test_japan_not_applicable_does_not_complete_a_recall(self) -> None:
        task = {"target_jurisdictions": ["JP"], "required_sources": ["official_registry_browser"]}
        evidence = {
            "source_runs": [
                self.source_run("patent_recall"),
                self.source_run("design_recall", "not_applicable"),
                self.source_run("trademark_recall"),
            ]
        }

        self.assertEqual(
            source_gaps(task, evidence, {"patents": [], "trademarks": []}, {}),
            ["official_registry_browser"],
        )

    def test_japan_wrong_evidence_type_does_not_complete_a_recall(self) -> None:
        task = {"target_jurisdictions": ["JP"], "required_sources": ["official_registry_browser"]}
        evidence = {
            "source_runs": [
                self.source_run("patent_recall", evidence_type="patent"),
                self.source_run("design_recall"),
                self.source_run("trademark_recall"),
            ]
        }

        self.assertEqual(
            source_gaps(task, evidence, {"patents": [], "trademarks": []}, {}),
            ["official_registry_browser"],
        )

    def test_japan_reused_screenshot_does_not_complete_three_recalls(self) -> None:
        task = {"target_jurisdictions": ["JP"], "required_sources": ["official_registry_browser"]}
        evidence = {
            "source_runs": [
                self.source_run("patent_recall", screenshot_hash="same-hash"),
                self.source_run("design_recall", screenshot_hash="same-hash"),
                self.source_run("trademark_recall", screenshot_hash="third-hash"),
            ]
        }

        self.assertEqual(
            source_gaps(task, evidence, {"patents": [], "trademarks": []}, {}),
            ["official_registry_browser"],
        )

class JapanOfficialRegistryValidationTests(unittest.TestCase):
    def make_task(self, root: Path) -> tuple[Path, Path, Path]:
        (root / "screenshots").mkdir()
        (root / "raw").mkdir()
        screenshot = root / "screenshots" / "jp-search.png"
        screenshot.write_bytes(PNG)
        (root / "task.json").write_text(
            json.dumps(
                {
                    "schema_version": "2.2-free",
                    "task_id": "IPRF-test-jp",
                    "target_jurisdictions": ["JP"],
                    "required_sources": ["official_registry_browser"],
                    "optional_sources": [],
                    "low_risk_gate_sources": [],
                    "coverage_gaps": [],
                }
            ),
            encoding="utf-8",
        )
        (root / "evidence.json").write_text(
            json.dumps(
                {
                    "schema_version": "2.2-free",
                    "task_id": "IPRF-test-jp",
                    "source_runs": [],
                    "collections": {
                        "product": [],
                        "patents": [],
                        "trademarks": [],
                        "copyright_assets": [],
                        "enforcement": [],
                        "official_verifications": [],
                        "browser": [],
                        "blacklist": [],
                    },
                }
            ),
            encoding="utf-8",
        )
        normalized = root / "jp-no-result.json"
        normalized.write_text(
            json.dumps(
                {
                    "operator_confirmed": True,
                    "result_message": "J-PlatPat rendered zero results",
                    "candidates": [],
                }
            ),
            encoding="utf-8",
        )
        return root / "task.json", screenshot, normalized

    def run_recorder(
        self,
        task_dir: Path,
        screenshot: Path,
        normalized: Path,
        source_url: str,
        *,
        operation: str = "patent_recall",
        evidence_type: str = "official_verification",
        status: str = "no_result",
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "record_provider_result.py"),
                "--task-dir",
                str(task_dir),
                "--provider",
                "official_registry_browser",
                "--operation",
                operation,
                "--query",
                "portable fan",
                "--jurisdiction",
                "JP",
                "--evidence-type",
                evidence_type,
                "--status",
                status,
                "--normalized-json",
                str(normalized),
                "--source-url",
                source_url,
                "--screenshot",
                str(screenshot),
            ],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_japan_rejects_non_jplatpat_official_source(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            task_dir = Path(temp)
            _, screenshot, normalized = self.make_task(task_dir)

            result = self.run_recorder(task_dir, screenshot, normalized, "https://example.com/japan-patent")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("J-PlatPat", result.stderr + result.stdout)

    def test_japan_accepts_jplatpat_official_source(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            task_dir = Path(temp)
            _, screenshot, normalized = self.make_task(task_dir)

            result = self.run_recorder(
                task_dir,
                screenshot,
                normalized,
                "https://www.j-platpat.inpit.go.jp/p0200",
            )

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def test_japan_rejects_unknown_registry_operation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            task_dir = Path(temp)
            _, screenshot, normalized = self.make_task(task_dir)

            result = self.run_recorder(
                task_dir,
                screenshot,
                normalized,
                "https://www.j-platpat.inpit.go.jp/p0200",
                operation="manual_registry_search",
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("operation", (result.stderr + result.stdout).casefold())

    def test_japan_rejects_wrong_evidence_type(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            task_dir = Path(temp)
            _, screenshot, normalized = self.make_task(task_dir)

            result = self.run_recorder(
                task_dir,
                screenshot,
                normalized,
                "https://www.j-platpat.inpit.go.jp/p0200",
                evidence_type="patent",
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("official_verification", result.stderr + result.stdout)

    def test_japan_rejects_non_image_screenshot(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            task_dir = Path(temp)
            _, screenshot, normalized = self.make_task(task_dir)
            screenshot.write_bytes(b"not an image")

            result = self.run_recorder(
                task_dir,
                screenshot,
                normalized,
                "https://www.j-platpat.inpit.go.jp/p0200",
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("image", (result.stderr + result.stdout).casefold())

    def test_japan_rejects_unconfirmed_zero_result(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            task_dir = Path(temp)
            _, screenshot, normalized = self.make_task(task_dir)
            normalized.write_text(json.dumps({"candidates": []}), encoding="utf-8")

            result = self.run_recorder(
                task_dir,
                screenshot,
                normalized,
                "https://www.j-platpat.inpit.go.jp/p0200",
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("operator-confirmed", result.stderr + result.stdout)

    def test_japan_recorder_rejects_reused_recall_screenshot(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            task_dir = Path(temp)
            _, screenshot, normalized = self.make_task(task_dir)
            source_url = "https://www.j-platpat.inpit.go.jp/p0200"

            first = self.run_recorder(
                task_dir,
                screenshot,
                normalized,
                source_url,
                operation="patent_recall",
            )
            second = self.run_recorder(
                task_dir,
                screenshot,
                normalized,
                source_url,
                operation="design_recall",
            )

        self.assertEqual(first.returncode, 0, first.stderr + first.stdout)
        self.assertNotEqual(second.returncode, 0)
        self.assertIn("distinct screenshots", second.stderr + second.stdout)

    def test_japan_recall_candidates_default_to_material_until_verified(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            task_dir = Path(temp)
            _, screenshot, normalized = self.make_task(task_dir)
            normalized.write_text(
                json.dumps(
                    {
                        "operator_confirmed": True,
                        "candidates": [
                            {
                                "right_type": "patent",
                                "publication_number": "JP2026000001A",
                                "title": "Portable fan",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            result = self.run_recorder(
                task_dir,
                screenshot,
                normalized,
                "https://www.j-platpat.inpit.go.jp/p0200",
                operation="patent_recall",
                status="success",
            )
            evidence = json.loads((task_dir / "evidence.json").read_text(encoding="utf-8"))
            candidate = evidence["collections"]["official_verifications"][0]["payload"]["candidates"][0]

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIs(candidate["material"], True)
        self.assertEqual(candidate["official_verification"]["status"], "not_checked")

    def test_failed_japan_candidate_verification_rejects_normalized_candidates(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            task_dir = Path(temp)
            _, screenshot, normalized = self.make_task(task_dir)
            normalized.write_text(
                json.dumps(
                    {
                        "operator_confirmed": True,
                        "candidates": [
                            {
                                "right_type": "patent",
                                "jurisdiction": "JP",
                                "publication_number": "JP2026000001A",
                                "title": "Portable fan",
                                "material": True,
                                "owner": "Example KK",
                                "legal_status": "Active",
                                "claims_summary": "Claim text",
                                "official_verification": {
                                    "status": "verified",
                                    "source": "J-PlatPat",
                                    "url": "https://www.j-platpat.inpit.go.jp/p0200",
                                    "checked_at": now_iso(),
                                },
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            result = self.run_recorder(
                task_dir,
                screenshot,
                normalized,
                "https://www.j-platpat.inpit.go.jp/p0200",
                operation="candidate_verification",
                status="failed",
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("failed", (result.stderr + result.stdout).casefold())


class JapanCandidateIntegrityTests(unittest.TestCase):
    def test_jplatpat_only_candidates_enter_both_normalized_candidate_lists(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            task_dir = Path(temp)
            (task_dir / "task.json").write_text(
                json.dumps(
                    {
                        "schema_version": "2.2-free",
                        "task_id": "IPRF-merge-jp",
                        "state": "collecting",
                        "product": {"brand": ""},
                    }
                ),
                encoding="utf-8",
            )
            candidates = [
                {
                    "right_type": "patent",
                    "jurisdiction": "JP",
                    "publication_number": "JP2026000001A",
                    "title": "Portable fan",
                    "official_verification": {"status": "not_checked"},
                },
                {
                    "right_type": "trademark",
                    "jurisdiction": "JP",
                    "application_number": "JP2026-000001",
                    "mark_text": "MOCKMARK",
                    "official_verification": {"status": "not_checked"},
                },
                {
                    "right_type": "design",
                    "jurisdiction": "JP",
                    "registration_number": "JP-D-1800001",
                    "title": "Portable fan design",
                    "official_verification": {"status": "not_checked"},
                },
            ]
            (task_dir / "evidence.json").write_text(
                json.dumps(
                    {
                        "schema_version": "2.2-free",
                        "task_id": "IPRF-merge-jp",
                        "source_runs": [
                            {
                                "run_id": "ATT-jp",
                                "status": "success",
                                "raw_paths": [],
                                "data_date": "2026-08-23",
                            }
                        ],
                        "collections": {
                            "patents": [],
                            "trademarks": [],
                            "official_verifications": [
                                {
                                    "provider": "official_registry_browser",
                                    "evidence_id": "EV-jp",
                                    "source_run_id": "ATT-jp",
                                    "query": "portable fan",
                                    "collected_at": "2026-08-23T12:00:00Z",
                                    "payload": {"candidates": candidates},
                                }
                            ],
                        },
                    }
                ),
                encoding="utf-8",
            )

            result = subprocess.run(
                [sys.executable, str(SCRIPTS / "merge_candidates.py"), "--task-dir", str(task_dir)],
                text=True,
                capture_output=True,
                check=False,
            )
            merged = json.loads((task_dir / "normalized-candidates.json").read_text(encoding="utf-8"))

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertEqual(len(merged["patents"]), 2)
        self.assertEqual(len(merged["trademarks"]), 1)

    def test_failed_jplatpat_verification_cannot_enter_candidate_merge(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            task_dir = Path(temp)
            (task_dir / "task.json").write_text(
                json.dumps(
                    {
                        "schema_version": "2.2-free",
                        "task_id": "IPRF-failed-jp",
                        "state": "collecting",
                        "product": {"brand": ""},
                    }
                ),
                encoding="utf-8",
            )
            candidate = {
                "right_type": "patent",
                "jurisdiction": "JP",
                "publication_number": "JP2026000002A",
                "title": "Failed injected patent",
                "material": True,
                "owner": "Example KK",
                "legal_status": "Active",
                "claims_summary": "Claim text",
                "official_verification": {
                    "status": "verified",
                    "source": "J-PlatPat",
                    "url": "https://www.j-platpat.inpit.go.jp/p0200",
                    "checked_at": now_iso(),
                },
            }
            (task_dir / "evidence.json").write_text(
                json.dumps(
                    {
                        "schema_version": "2.2-free",
                        "task_id": "IPRF-failed-jp",
                        "source_runs": [{"run_id": "ATT-failed", "status": "failed", "raw_paths": []}],
                        "collections": {
                            "patents": [],
                            "trademarks": [],
                            "official_verifications": [
                                {
                                    "provider": "official_registry_browser",
                                    "evidence_id": "EV-failed",
                                    "source_run_id": "ATT-failed",
                                    "query": "failed",
                                    "payload": {"candidates": [candidate]},
                                }
                            ],
                        },
                    }
                ),
                encoding="utf-8",
            )

            result = subprocess.run(
                [sys.executable, str(SCRIPTS / "merge_candidates.py"), "--task-dir", str(task_dir)],
                text=True,
                capture_output=True,
                check=False,
            )
            merged = json.loads((task_dir / "normalized-candidates.json").read_text(encoding="utf-8"))

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertEqual(merged["patents"], [])

    def test_material_japan_patent_requires_complete_verified_fields(self) -> None:
        incomplete = {
            "jurisdiction": "JP",
            "right_type": "patent",
            "publication_number": "JP2026000001A",
            "material": True,
            "official_verification": {
                "status": "verified",
                "source": "J-PlatPat",
                "url": "https://www.j-platpat.inpit.go.jp/p0200",
                "checked_at": now_iso(),
            },
        }

        self.assertEqual(
            material_unverified({"patents": [incomplete], "trademarks": []}),
            ["JP2026000001A"],
        )

        complete = {
            **incomplete,
            "title": "Portable fan",
            "owner": "Example KK",
            "legal_status": "Active",
            "claims_summary": "Claim 1 covers the fan housing and support structure.",
        }
        self.assertEqual(material_unverified({"patents": [complete], "trademarks": []}), [])

        stale = {
            **complete,
            "official_verification": {**complete["official_verification"], "checked_at": "2020-01-01T00:00:00Z"},
        }
        self.assertEqual(
            material_unverified({"patents": [stale], "trademarks": []}),
            ["JP2026000001A"],
        )


if __name__ == "__main__":
    unittest.main()
