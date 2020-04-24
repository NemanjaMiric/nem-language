"""Hold Parser class.

Holds the Parser class which is used for converting tokens from the lexer into an Abstract Syntax Tree.

Nem definitions (Extended Backus-Naur form):
    atom       = NUMBER | LEFT_BRACKET, expression, RIGHT_BRACKET
    power      = atom, { CARET, factor }
    factor     = [ PLUS | MINUS ], power
    term       = factor, { ( ASTERISK | SLASH ), factor }
    expression = term, { ( PLUS | MINUS | MODULO ), term }

"""

from nem.token_ import Token
import nem.nodes as ast
from nem.exceptions import ParserException


class Parser:

    """Convert tokens into an AST.

    Used for converting tokens from the lexer into an Abstract Syntax Tree.

    """

    def __init__(self, tokens):
        """Initialize Parser class."""
        self.tokens = tokens

        self.current_token = next(tokens)
        self.end_reached = False

    def _advance_index(self):
        """Advance the current token."""
        self.current_token = next(self.tokens)

    def _binary_operation(self, element_left, operations, element_right):
        """Parse a binary operation."""
        temporary = element_left()

        while self.current_token.type in operations:
            temporary_operator = self.current_token.value
            self._advance_index()
            temporary_right = element_right()
            temporary = ast.BinaryOperation(temporary, temporary_operator, temporary_right)

        return temporary

    def _atom(self):
        """Parse an atom.

        Extended Backus-Naur form:
            atom = NUMBER | LEFT_BRACKET, expression, RIGHT_BRACKET

        """
        # atom = NUMBER
        if self.current_token.type == Token.NUMBER:
            temporary = ast.Number(self.current_token.value)
            self._advance_index()

            return temporary
        # atom = LEFT_BRACKET, expression, RIGHT_BRACKET
        elif self.current_token.type == Token.LEFT_BRACKET:
            self._advance_index()
            temporary = self._expression()

            if self.current_token.type == Token.RIGHT_BRACKET:
                self._advance_index()
                return temporary

            # If there's no closing bracket after the expression - raise ParserException
            raise ParserException("Parsing Error (Line {}): Expected a closing bracket".format(self.current_token.line))

        # If atom is expected but there's no number or an opening bracket - raise ParserException
        raise ParserException("Parsing Error (Line {}): Expected a number or an opening bracket"
                              .format(self.current_token.line))

    def _power(self):
        """Parse a power.

        Extended Backus-Naur form:
            power = atom, { CARET, factor }

        """
        temporary = self._binary_operation(self._atom, Token.CARET, self._factor)

        return temporary

    def _factor(self):
        """Parse a factor.

        Extended Backus-Naur form:
            factor = [ PLUS | MINUS ], power

        """
        if self.current_token.type in (Token.PLUS, Token.MINUS):
            temporary_sign = self.current_token.value
            self._advance_index()
            temporary = ast.UnaryOperation(temporary_sign, self._power())

            return temporary
        temporary = self._power()

        return temporary

    def _term(self):
        """Parse a term.

        Extended Backus-Naur form:
            term = factor, { ( ASTERISK | SLASH ), factor }

        """
        temporary = self._binary_operation(self._factor, (Token.ASTERISK, Token.SLASH), self._factor)

        return temporary

    def _expression(self):
        """Parse an expression.

        Extended Backus-Naur form:
            expression = term, { ( PLUS | MINUS | MODULO ), term }

        """
        temporary = self._binary_operation(self._term, (Token.PLUS, Token.MINUS, Token.MODULO), self._term)

        return temporary

    def _parse(self):
        while self.current_token.type != Token.EOF:
            temporary = self._expression()

            yield temporary

    def parse(self):
        """Parse the tokens into an AST.

        Parses the tokens that get returned from the lexer and builds an Abstract Syntax Tree out of them.

        Nem definitions (Extended Backus-Naur form):
            atom       = NUMBER | LEFT_BRACKET, expression, RIGHT_BRACKET
            power      = atom, { CARET, factor }
            factor     = [ PLUS | MINUS ], power
            term       = factor, { ( ASTERISK | SLASH ), factor }
            expression = term, { ( PLUS | MINUS | MODULO ), term }

        """
        return self._parse()


def main():
    """Debug the parser.

    Used as the entry-point when the file gets ran directly. Used for debugging the class Parser.

    """
    while True:
        print(list(Parser(Lexer(input(">> ") + "\n").lex()).parse()))


if __name__ == "__main__":
    # Only activates when the file gets ran directly.
    from nem.lexer import Lexer

    main()
