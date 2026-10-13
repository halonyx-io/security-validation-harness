"""Small, explicit data types used at the verification boundary."""

from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class Candidate:
    """A hypothesis requiring a controlled, deterministic comparison."""

    identifier: str
    least_privileged_url: str
    control_url: str
    sensitive_marker: str


@dataclass(frozen=True)
class Observation:
    """One completed response or a transport failure."""

    completed: bool
    status: int | None = None
    body: str = ""
    error: str | None = None


class Verdict(str, Enum):
    CONFIRMED = "CONFIRMED"
    REJECTED = "REJECTED"
    RETRYABLE = "RETRYABLE"


@dataclass(frozen=True)
class VerificationResult:
    candidate_id: str
    verdict: Verdict
    reason: str
