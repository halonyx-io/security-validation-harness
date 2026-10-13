"""Central, deliberately narrow policy for mock requests."""

from __future__ import annotations

import re


class PolicyViolation(ValueError):
    """Raised before an operation leaves the policy boundary."""


class RequestPolicy:
    """Allow only observation operations used by this portfolio demo."""

    _REST_METHODS = frozenset({"GET", "HEAD"})
    _QUERY = re.compile(r"^\s*(?:#[^\n]*\n\s*)*query\b", re.IGNORECASE)

    def authorize_rest(self, method: str) -> str:
        normalized = method.upper().strip()
        if normalized not in self._REST_METHODS:
            raise PolicyViolation(f"REST method {normalized or '<empty>'} is not allowed")
        return normalized

    def authorize_graphql(self, document: str) -> None:
        """Require an explicit GraphQL query operation.

        Requiring the operation keyword avoids treating shorthand documents or
        strings containing the word 'query' as safe by accident.
        """

        if not self._QUERY.match(document):
            raise PolicyViolation("only explicit GraphQL query operations are allowed")
