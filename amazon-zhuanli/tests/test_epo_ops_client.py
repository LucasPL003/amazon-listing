from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest import mock


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = SKILL_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import epo_ops_client as epo  # noqa: E402
from provider_utils import ProviderError  # noqa: E402


class EpoNoResultTests(unittest.TestCase):
    def test_search_entity_not_found_fault_is_returned_as_zero_result_xml(self) -> None:
        fault_xml = b"""<?xml version="1.0" encoding="UTF-8"?>
<fault xmlns="http://ops.epo.org">
  <code>SERVER.EntityNotFound</code>
  <message>No results found</message>
</fault>"""
        error = ProviderError(
            "PROVIDER_HTTP_ERROR",
            "failed",
            f"Provider HTTP 404: {fault_xml.decode()}",
            404,
        )
        config = {"http": {"timeout_seconds": 5, "retries": 0}}

        with (
            mock.patch.object(epo, "settings", return_value=(config, "https://ops.test", "", "", "")),
            mock.patch.object(epo, "access_token", return_value=("token", {})),
            mock.patch.object(epo, "http_request", side_effect=error),
        ):
            try:
                body, headers = epo.ops_get("published-data/search?q=missing")
            except ProviderError as exc:
                self.fail(f"Explicit EPO zero-result fault was misclassified as provider failure: {exc}")

        self.assertIn(b"SERVER.EntityNotFound", body)
        self.assertIn(b"No results found", body)
        self.assertEqual(headers, {})

    def test_other_404_faults_remain_provider_failures(self) -> None:
        error = ProviderError(
            "PROVIDER_HTTP_ERROR",
            "failed",
            "Provider HTTP 404: <fault><code>SERVER.UnknownRecord</code></fault>",
            404,
        )
        config = {"http": {"timeout_seconds": 5, "retries": 0}}

        with (
            mock.patch.object(epo, "settings", return_value=(config, "https://ops.test", "", "", "")),
            mock.patch.object(epo, "access_token", return_value=("token", {})),
            mock.patch.object(epo, "http_request", side_effect=error),
        ):
            with self.assertRaises(ProviderError):
                epo.ops_get("published-data/search?q=missing")


if __name__ == "__main__":
    unittest.main()
