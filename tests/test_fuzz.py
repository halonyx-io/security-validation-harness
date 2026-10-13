import unittest

from harness import PolicyViolation, RequestPolicy


class PolicyFuzzTests(unittest.TestCase):
    def test_method_variations_do_not_expand_the_allowlist(self) -> None:
        policy = RequestPolicy()
        variants = ("post", "PoSt", "POST ", "\tdelete", "GETX", "GET\nPOST")
        for method in variants:
            with self.subTest(method=repr(method)):
                with self.assertRaises(PolicyViolation):
                    policy.authorize_rest(method)

    def test_query_word_inside_another_operation_is_not_enough(self) -> None:
        policy = RequestPolicy()
        for document in (
            "mutation queryLike { updateThing { id } }",
            "subscription queryEvents { events { id } }",
            "# query\nmutation Change { change { id } }",
        ):
            with self.subTest(document=document):
                with self.assertRaises(PolicyViolation):
                    policy.authorize_graphql(document)
