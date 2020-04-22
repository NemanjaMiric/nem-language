"""Test the Token class.

Unit testing for the Token class.

"""


import unittest
from nem.token_ import Token


class TokenTestCase(unittest.TestCase):

    """Unit test Token class.

    Used for unit testing the Token class.

    """

    def test_init(self):
        """Test the Token class initialization."""
        self.assertEqual(Token(Token.MODULO, "_0", 1).type, Token.MODULO)
        self.assertEqual(Token(Token.NUMBER, ".2", 2).value, ".2")
        self.assertEqual(Token(Token.TEXT, ".2", 3).line, 3)


if __name__ == '__main__':
    # Only activates when the file gets ran directly.
    unittest.main()
