"""A scripted, in-memory transport; deliberately no network client exists here."""

from __future__ import annotations

from collections.abc import Mapping

from .models import Observation
from .policy import RequestPolicy


class ScriptedTransport:
    """Return fixed observations keyed by URL after enforcing request policy."""

    def __init__(self, responses: Mapping[str, Observation], policy: RequestPolicy | None = None):
        self._responses = dict(responses)
        self._policy = policy or RequestPolicy()

    def observe(self, method: str, url: str) -> Observation:
        self._policy.authorize_rest(method)
        return self._responses.get(
            url,
            Observation(completed=False, error="scripted route unavailable"),
        )
