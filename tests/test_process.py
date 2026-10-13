import unittest

from harness import Candidate, ScriptedTransport, Verdict, verify_candidate
from harness.models import Observation


class VerificationProcessTests(unittest.TestCase):
    def setUp(self) -> None:
        self.candidate = Candidate(
            "candidate-1",
            "mock://lab/record/1?actor=viewer",
            "mock://lab/record/1?actor=owner",
            "classification: confidential",
        )

    def test_matching_subject_and_control_confirm_candidate(self) -> None:
        responses = {
            self.candidate.least_privileged_url: Observation(True, 200, self.candidate.sensitive_marker),
            self.candidate.control_url: Observation(True, 200, self.candidate.sensitive_marker),
        }
        result = verify_candidate(self.candidate, ScriptedTransport(responses))
        self.assertEqual(result.verdict, Verdict.CONFIRMED)

    def test_missing_subject_marker_rejects_candidate(self) -> None:
        responses = {
            self.candidate.least_privileged_url: Observation(True, 200, "public summary"),
            self.candidate.control_url: Observation(True, 200, self.candidate.sensitive_marker),
        }
        result = verify_candidate(self.candidate, ScriptedTransport(responses))
        self.assertEqual(result.verdict, Verdict.REJECTED)

    def test_transport_failure_is_retryable_not_a_quiet_miss(self) -> None:
        responses = {
            self.candidate.least_privileged_url: Observation(False, error="mock timeout"),
            self.candidate.control_url: Observation(True, 200, self.candidate.sensitive_marker),
        }
        result = verify_candidate(self.candidate, ScriptedTransport(responses))
        self.assertEqual(result.verdict, Verdict.RETRYABLE)
        self.assertIn("mock timeout", result.reason)
