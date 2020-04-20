"""Test the Token class.

Unit testing for the Token class.

"""


import unittest
from nem.nemtoken import Token


class TokenTestCase(unittest.TestCase):

    """Unit test Token class.

    Used for unit testing the Token class.

    """

    def test_init(self):
        """Test the Token class initialization."""
        self.assertEqual(Token("variable-any", "_0").type, "variable-any")
        self.assertEqual(Token("number", ".2").value, ".2")


if __name__ == '__main__':
    # Only gets activated when the file gets ran directly.
    unittest.main()
