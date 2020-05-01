"""Test for Evaluator class.

Unit testing for the Evaluator class.

"""


import unittest
from nem.lexer import Lexer
from nem.parser import Parser
from nem.evaluator import Evaluator
from nem.symbol_table import SymbolTable
from nem.types_ import *
from nem.exceptions import EvaluatorException


class ParserTestCase(unittest.TestCase):

    """Unit test Parser class.

    Used for unit testing the Parser class.

    """

    def test_parse(self):
        """Test the parse method.

        Tests the parser.

        """
        symbol_table = SymbolTable()
        symbol_table.set("true", Number(1))
        symbol_table.set("false", Number(0))
        symbol_table.set("print", BuiltInFunction(["element"], 0))
        symbol_table.set("input", BuiltInFunction([], 1))
        symbol_table.set("convert", BuiltInFunction(["value", "type"], 2))

        with open("test_cases/test_evaluator.in") as _input:
            _input = _input.read()

        with open("test_cases/test_evaluator.out") as output:
            output = output.read()

        self.assertEqual(
            "".join(list(map(repr, Evaluator(Parser(Lexer(_input, "test").lex()).parse(), symbol_table).evaluate()))),
            output
        )

        with self.assertRaises(EvaluatorException):
            list(Evaluator(Parser(Lexer("\nvariable", "<stdin>").lex()).parse(), symbol_table).evaluate())

        with self.assertRaises(EvaluatorException):
            list(Evaluator(Parser(Lexer("import \"test\"\n", "<stdin>").lex()).parse(), symbol_table).evaluate())

        with self.assertRaises(EvaluatorException):
            list(Evaluator(Parser(Lexer("nem(1, 2)\n", "<stdin>").lex()).parse(), symbol_table).evaluate())

        with self.assertRaises(EvaluatorException):
            list(Evaluator(Parser(Lexer("[1, 2][2]\n", "<stdin>").lex()).parse(), symbol_table).evaluate())

        with self.assertRaises(EvaluatorException):
            list(Evaluator(Parser(Lexer("22 * [1, 2]\n", "<stdin>").lex()).parse(), symbol_table).evaluate())

        with self.assertRaises(EvaluatorException):
            list(Evaluator(Parser(Lexer("[1, 2] ^ [1, 2]\n", "<stdin>").lex()).parse(), symbol_table).evaluate())

        with self.assertRaises(EvaluatorException):
            list(Evaluator(Parser(Lexer("a = return 1\n", "<stdin>").lex()).parse(), symbol_table).evaluate())

        with self.assertRaises(EvaluatorException):
            list(Evaluator(Parser(Lexer("while (return 1) (print(1))\n", "<stdin>").lex()).parse(),
                           symbol_table).evaluate())

        with self.assertRaises(EvaluatorException):
            list(Evaluator(Parser(Lexer("if (return 1) (print(1))\n", "test").lex()).parse(), symbol_table).evaluate())

        with self.assertRaises(EvaluatorException):
            list(Evaluator(Parser(Lexer("return 2\n", "<stdin>").lex()).parse(), symbol_table).evaluate())


if __name__ == '__main__':
    # Only activates when the file gets ran directly.
    unittest.main()
