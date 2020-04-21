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
        code = """
            # Code made for testing purposes #
            my_very_cool_variable123 = 77
            _0=.0
            a   =  "a string123;'-p="
            
            # Do some stream stuff
            output a
            error my_very_cool_variable123
            input a
            output a
            output "some text1 2   3"
            
            # Math stuff
            2 + 2 * 2
            555 + .2 * 1^3
            66^77
            gg = 1-2+3-4+5-6
            d = 5x^2 + x^1 %3x^0#Cool stuff
            output d
            
            (2+2)*2^2
            
            list = 1, 2,3 ,4 ,6 ,7 #neat"""

        self.assertEqual(Interpreter(code).lex(),
                         [Token('symbol', 'my_very_cool_variable123'), Token('operator', '='),
                          Token('number', '77'), Token('symbol', '_0'),
                          Token('operator', '='), Token('number', '.0'),
                          Token('symbol', 'a'), Token('operator', '='),
                          Token('text', "a string123;'-p="), Token('stream', 'output'),
                          Token('symbol', 'a'), Token('stream', 'error'),
                          Token('symbol', 'my_very_cool_variable123'),
                          Token('stream', 'input'), Token('symbol', 'a'),
                          Token('stream', 'output'), Token('symbol', 'a'),
                          Token('stream', 'output'), Token('text', 'some text1 2   3'),
                          Token('number', '2'), Token('operator', '+'),
                          Token('number', '2'), Token('operator', '*'),
                          Token('number', '2'), Token('number', '555'),
                          Token('operator', '+'), Token('number', '.2'),
                          Token('operator', '*'), Token('number', '1'),
                          Token('operator', '^'), Token('number', '3'),
                          Token('number', '66'), Token('operator', '^'),
                          Token('number', '77'), Token('symbol', 'gg'),
                          Token('operator', '='), Token('number', '1'),
                          Token('operator', '-'), Token('number', '2'),
                          Token('operator', '+'), Token('number', '3'),
                          Token('operator', '-'), Token('number', '4'),
                          Token('operator', '+'), Token('number', '5'),
                          Token('operator', '-'), Token('number', '6'),
                          Token('symbol', 'd'), Token('operator', '='),
                          Token('number', '5'), Token('symbol', 'x'),
                          Token('operator', '^'), Token('number', '2'),
                          Token('operator', '+'), Token('symbol', 'x'),
                          Token('operator', '^'), Token('number', '1'),
                          Token('operator', '%'), Token('number', '3'),
                          Token('symbol', 'x'), Token('operator', '^'),
                          Token('number', '0'), Token('stream', 'output'),
                          Token('symbol', 'd'), Token('left-bracket', '('),
                          Token('number', '2'), Token('operator', '+'),
                          Token('number', '2'), Token('right-bracket', ')'),
                          Token('operator', '*'), Token('number', '2'),
                          Token('operator', '^'), Token('number', '2'),
                          Token('symbol', 'list'), Token('operator', '='),
                          Token('number', '1'), Token('list-element', ','),
                          Token('number', '2'), Token('list-element', ','),
                          Token('number', '3'), Token('list-element', ','),
                          Token('number', '4'), Token('list-element', ','),
                          Token('number', '6'), Token('list-element', ','),
                          Token('number', '7')])

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
