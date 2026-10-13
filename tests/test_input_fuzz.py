import unittest

from harness import Candidate, ScriptedTransport, Verdict, verify_candidate
from harness.models import Observation


class MarkerInputFuzzTests(unittest.TestCase):
    def test_near_matches_and_arbitrary_text_cannot_confirm(self) -> None:
        marker = "classification: confidential"
        candidate = Candidate("candidate-fuzz", "mock://viewer", "mock://owner", marker)
        near_matches = (
            "classification: public",
            "classification confidential",
            "CLASSIFICATION: CONFIDENTIAL",
            "classification: confidential-ish",
            "xclassification: confidential",
            "classification: confidentialx",
            "",
            "x" * 4096,
        )
        for body in near_matches:
            with self.subTest(body=body[:40]):
                transport = ScriptedTransport(
                    {
                        candidate.least_privileged_url: Observation(True, 200, body),
                        candidate.control_url: Observation(True, 200, marker),
                    }
                )
                result = verify_candidate(candidate, transport)
                self.assertEqual(result.verdict, Verdict.REJECTED)
