"""Test for Lexer class.

Unit testing for the Lexer class.

"""


import unittest
from nem.lexer import Lexer
from nem.token_ import Token
from nem.exceptions import LexerException


class LexerTestCase(unittest.TestCase):

    """Unit test Lexer class.

    Used for unit testing the Lexer class.

    """

    def test_lex(self):
        """Test the lex method.

        Tests the lexer.

        """
        with open("test_cases/test_lexer.in") as _input:
            _input = _input.read()

        with open("test_cases/test_lexer.out") as output:
            output = eval(output.read())

        self.assertEqual(list(Lexer(_input).lex()), output)

        with self.assertRaises(LexerException):
            list(Lexer("\n\"\"\"").lex())

        with self.assertRaises(LexerException):
            list(Lexer("\n..\n").lex())

        with self.assertRaises(LexerException):
            list(Lexer(".\n").lex())

        with self.assertRaises(LexerException):
            list(Lexer("\n'\n").lex())


if __name__ == '__main__':
    # Only activates when the file gets ran directly.
    unittest.main()
