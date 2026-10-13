"""Deterministic verdicts from paired observations."""

from __future__ import annotations

import re

from .models import Candidate, Verdict, VerificationResult
from .transport import ScriptedTransport


def _contains_exact_marker(body: str, marker: str) -> bool:
    """Match a marker as a distinct value, never as part of a longer token."""

    pattern = rf"(?<![\w-]){re.escape(marker)}(?![\w-])"
    return re.search(pattern, body) is not None


def verify_candidate(candidate: Candidate, transport: ScriptedTransport) -> VerificationResult:
    """Verify a candidate without allowing a failed observation to look benign."""

    subject = transport.observe("GET", candidate.least_privileged_url)
    control = transport.observe("GET", candidate.control_url)

    if not subject.completed or not control.completed:
        failures = ", ".join(
            error
            for error in (subject.error, control.error)
            if error
        ) or "observation did not complete"
        return VerificationResult(candidate.identifier, Verdict.RETRYABLE, failures)

    if subject.status != 200 or control.status != 200:
        return VerificationResult(
            candidate.identifier,
            Verdict.REJECTED,
            f"unexpected response status (subject={subject.status}, control={control.status})",
        )

    if not _contains_exact_marker(control.body, candidate.sensitive_marker):
        return VerificationResult(
            candidate.identifier,
            Verdict.REJECTED,
            "authorised control did not contain the expected marker",
        )

    if not _contains_exact_marker(subject.body, candidate.sensitive_marker):
        return VerificationResult(
            candidate.identifier,
            Verdict.REJECTED,
            "least-privileged observation did not reproduce the marker",
        )

    return VerificationResult(
        candidate.identifier,
        Verdict.CONFIRMED,
        "least-privileged observation reproduced the authorised control marker",
    )
