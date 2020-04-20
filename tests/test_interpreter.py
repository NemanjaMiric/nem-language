"""Test for Interpreter class.

Unit testing for the Interpreter class.

"""


import unittest
from nem.interpreter import Interpreter
from nem.nemtoken import Token


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
            d = 5x^2 + x^1 -3x^0#Cool stuff
            output d
            
            list = 1, 2,3 ,4 ,6 ,7 #neat"""

        self.assertEqual(Interpreter(code).lex(),
                         [Token('variable-any', 'my_very_cool_variable123'), Token('operation', '='),
                          Token('number', '77'), Token('variable-any', '_0'),
                          Token('operation', '='), Token('number', '.0'),
                          Token('variable-any', 'a'), Token('operation', '='),
                          Token('text', "a string123;'-p="), Token('stream', 'output'),
                          Token('variable-any', 'a'), Token('stream', 'error'),
                          Token('variable-any', 'my_very_cool_variable123'),
                          Token('stream', 'input'), Token('variable-any', 'a'),
                          Token('stream', 'output'), Token('variable-any', 'a'),
                          Token('stream', 'output'), Token('text', 'some text1 2   3'),
                          Token('number', '2'), Token('operation', '+'),
                          Token('number', '2'), Token('operation', '*'),
                          Token('number', '2'), Token('number', '555'),
                          Token('operation', '+'), Token('number', '.2'),
                          Token('operation', '*'), Token('number', '1'),
                          Token('operation', '^'), Token('number', '3'),
                          Token('number', '66'), Token('operation', '^'),
                          Token('number', '77'), Token('variable-any', 'gg'),
                          Token('operation', '='), Token('number', '1'),
                          Token('operation', '-'), Token('number', '2'),
                          Token('operation', '+'), Token('number', '3'),
                          Token('operation', '-'), Token('number', '4'),
                          Token('operation', '+'), Token('number', '5'),
                          Token('operation', '-'), Token('number', '6'),
                          Token('variable-any', 'd'), Token('operation', '='),
                          Token('number', '5'), Token('variable-any', 'x'),
                          Token('operation', '^'), Token('number', '2'),
                          Token('operation', '+'), Token('variable-any', 'x'),
                          Token('operation', '^'), Token('number', '1'),
                          Token('operation', '-'), Token('number', '3'),
                          Token('variable-any', 'x'), Token('operation', '^'),
                          Token('number', '0'), Token('stream', 'output'),
                          Token('variable-any', 'd'), Token('variable-any', 'list'),
                          Token('operation', '='), Token('number', '1'),
                          Token('list-element', ','), Token('number', '2'),
                          Token('list-element', ','), Token('number', '3'),
                          Token('list-element', ','), Token('number', '4'),
                          Token('list-element', ','), Token('number', '6'),
                          Token('list-element', ','), Token('number', '7')])

        with self.assertRaises(SystemExit) as cm:
            Interpreter("\n\"\"\"").lex()
        self.assertEqual(cm.exception.code, -1)

        with self.assertRaises(SystemExit) as cm:
            Interpreter("\n'\n").lex()
        self.assertEqual(cm.exception.code, -1)


if __name__ == '__main__':
    # Only gets activated when the file gets ran directly.
    unittest.main()
