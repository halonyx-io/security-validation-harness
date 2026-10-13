"""Run a complete mock-only candidate verification."""

from harness import Candidate, ScriptedTransport, verify_candidate
from harness.models import Observation


def main() -> None:
    marker = "classification: confidential"
    candidate = Candidate(
        identifier="mock-access-boundary-001",
        least_privileged_url="mock://lab/records/42?actor=viewer",
        control_url="mock://lab/records/42?actor=owner",
        sensitive_marker=marker,
    )
    transport = ScriptedTransport(
        {
            candidate.least_privileged_url: Observation(True, 200, f"record 42; {marker}"),
            candidate.control_url: Observation(True, 200, f"record 42; {marker}"),
        }
    )
    result = verify_candidate(candidate, transport)
    print(f"{result.candidate_id}: {result.verdict.value}")
    print(result.reason)


if __name__ == "__main__":
    main()
