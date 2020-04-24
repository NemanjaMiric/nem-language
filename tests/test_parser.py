"""Test for Parser class.

Unit testing for the Parser class.

"""


import unittest
from nem.lexer import Lexer
from nem.parser import Parser
from nem.exceptions import ParserException
from nem.nodes import Number, UnaryOperation, BinaryOperation


class ParserTestCase(unittest.TestCase):

    """Unit test Parser class.

    Used for unit testing the Parser class.

    """

    def test_parse(self):
        """Test the parse method.

        Tests the parser.

        """
        with open("test_cases/test_parser.in") as _input:
            _input = _input.read()

        with open("test_cases/test_parser.out") as output:
            output = eval(output.read())

        self.assertEqual(list(Parser(Lexer(_input).lex()).parse()), output)

        with self.assertRaises(ParserException):
            list(Parser(Lexer("\n2+").lex()).parse())

        with self.assertRaises(ParserException):
            list(Parser(Lexer("(1+1\n").lex()).parse())


if __name__ == '__main__':
    # Only activates when the file gets ran directly.
    unittest.main()
