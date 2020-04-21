"""Test for Interpreter class.

Unit testing for the Interpreter class.

"""


import unittest
from nem.interpreter import Interpreter
from nem.nemtoken import Token
from nem.exceptions import LexerException


class InterpreterTestCase(unittest.TestCase):

    """Unit test Interpreter class.

    Used for unit testing the Interpreter class.

    """

    def test_lex(self):
        """Test the lex method from the Interpreter class.

        Tests the interpreter's lexer.

        """
        self.maxDiff = None

        with open("test_interpreter_lex.in") as _input:
            _input = _input.read()

        with open("test_interpreter_lex.out") as output:
            output = eval(output.read())

        self.assertEqual(Interpreter(_input).lex(), output)

        with self.assertRaises(LexerException):
            Interpreter("\n\"\"\"").lex()

        with self.assertRaises(LexerException):
            Interpreter("\n..\n").lex()

        with self.assertRaises(LexerException):
            Interpreter("\n.\n").lex()

        with self.assertRaises(LexerException):
            Interpreter("\n'\n").lex()


if __name__ == '__main__':
    # Only activates when the file gets ran directly.
    unittest.main()
