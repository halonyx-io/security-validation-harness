import unittest

from harness import PolicyViolation, RequestPolicy


class RequestPolicyContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.policy = RequestPolicy()

    def test_allows_observation_methods(self) -> None:
        self.assertEqual(self.policy.authorize_rest("get"), "GET")
        self.assertEqual(self.policy.authorize_rest(" HEAD "), "HEAD")

    def test_rejects_mutating_rest_methods(self) -> None:
        for method in ("POST", "PUT", "PATCH", "DELETE", "", "OPTIONS"):
            with self.subTest(method=method):
                with self.assertRaises(PolicyViolation):
                    self.policy.authorize_rest(method)

    def test_allows_explicit_graphql_query_only(self) -> None:
        self.policy.authorize_graphql("query Viewer { viewer { id } }")

    def test_rejects_graphql_mutation_and_shorthand(self) -> None:
        for document in ("mutation Change { change { id } }", "{ viewer { id } }"):
            with self.subTest(document=document):
                with self.assertRaises(PolicyViolation):
                    self.policy.authorize_graphql(document)
