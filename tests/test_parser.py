"""Test for Parser class.

Unit testing for the Parser class.

"""


import unittest
from nem.lexer import Lexer
from nem.parser import Parser
from nem.exceptions import ParserException
from nem.nodes import *


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
            output = output.read()

        self.assertEqual("".join(list(map(repr, Parser(Lexer(_input, "<stdin>").lex()).parse()))), output)

        with self.assertRaises(ParserException):
            list(Parser(Lexer("\n2+", "<stdin>").lex()).parse())

        with self.assertRaises(ParserException):
            list(Parser(Lexer("import\n", "<stdin>").lex()).parse())

        with self.assertRaises(ParserException):
            list(Parser(Lexer("nem(1, 2\n", "<stdin>").lex()).parse())

        with self.assertRaises(ParserException):
            list(Parser(Lexer("function nem\n", "<stdin>").lex()).parse())

        with self.assertRaises(ParserException):
            list(Parser(Lexer("function nem(a,b\n", "<stdin>").lex()).parse())

        with self.assertRaises(ParserException):
            list(Parser(Lexer("function nem(a,\n", "<stdin>").lex()).parse())

        with self.assertRaises(ParserException):
            list(Parser(Lexer("function nem(1\n", "<stdin>").lex()).parse())

        with self.assertRaises(ParserException):
            list(Parser(Lexer("[1,2,3\n", "<stdin>").lex()).parse())

        with self.assertRaises(ParserException):
            list(Parser(Lexer("a[1\n", "<stdin>").lex()).parse())

        with self.assertRaises(ParserException):
            list(Parser(Lexer("import\n", "<stdin>").lex()).parse())


if __name__ == '__main__':
    # Only activates when the file gets ran directly.
    unittest.main()
