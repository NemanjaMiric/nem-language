"""Hold Parser class.

Holds the Parser class which is used for converting tokens from the lexer into an Abstract Syntax Tree.

Nem definitions (Extended Backus-Naur form):
    list_index = LEFT_SQUARE, expression, RIGHT_SQUARE ;
    list       = LEFT_SQUARE, [ expression, { COMMA, expression } ], RIGHT_SQUARE ;
    function   = FUNCTION, [ SYMBOL ], LEFT_BRACKET, [ SYMBOL, { COMMA, SYMBOL } ], RIGHT_BRACKET, expression ;
    arguments  = LEFT_BRACKET, [ expression, { COMMA, expression } ], RIGHT_BRACKET
    while      = WHILE, expression, expression ;
    if         = IF, expression, expression, [ OTHERWISE, expression ] ;
    atom       = NUMBER
               | LEFT_BRACKET, expression, { expression }, RIGHT_BRACKET
               | SYMBOL, { arguments }, { list_index }
               | if
               | while
               | function
               | TEXT, { list_index }
               | list, { list_index }
               | RETURN, expression
               | CONTINUE
               | BREAK
               | NULL
               | IMPORT, TEXT ;
    power      = atom, { CARET, factor } ;
    factor     = [ PLUS | MINUS ], power ;
    term       = factor, { ( ASTERISK | SLASH ), factor } ;
    arithmetic = term, { ( PLUS | MINUS | MODULO ), term } ;
    not        = [ NOT ], arithmetic ;
    comparison = not, { ( IS | LESS | LESS_EQUAL | GREATER | GREATER_EQUAL ), not } ;
    expression = comparison, { ( AND | OR ), comparison }
               | SYMBOL, EQUAL, expression ;

"""

from nem.exceptions import ParserException
import nem.nodes as ast
from nem.token_ import Token


class Parser:

    """Convert tokens into an AST.

    Used for converting tokens from the lexer into an Abstract Syntax Tree.

    """

    def __init__(self, tokens):
        """Initialize Parser class."""
        self.tokens = tokens

        self.current_token = next(tokens)

    def _advance_index(self):
        """Advance the current token."""
        self.current_token = next(self.tokens)

    def _binary_operation(self, element_left, operations, element_right):
        """Parse a binary operation."""
        temporary = element_left()

        start_line = temporary.line

        while self.current_token.type in operations:
            temporary_operator = self.current_token.value
            self._advance_index()

            temporary_right = element_right()

            temporary = ast.BinaryOperation(temporary, temporary_operator, temporary_right)
            temporary.line = start_line
            temporary.filename = temporary_right.filename

        return temporary

    def _list_index(self, holder, start_line):
        """Parse a list index.

        Extended Backus-Naur form:
            list_index = LEFT_SQUARE, expression, RIGHT_SQUARE ;

        """
        # list_index = LEFT_SQUARE, expression, RIGHT_SQUARE ;
        if self.current_token.type == Token.LEFT_SQUARE:
            self._advance_index()

            temporary_expression = self._expression()

            if self.current_token.type == Token.RIGHT_SQUARE:
                temporary = ast.ListIndex(holder, temporary_expression)
                temporary.line = start_line
                temporary.filename = self.current_token.filename
                self._advance_index()

                return temporary
            else:
                raise ParserException("Parsing Error (File {}) (Line {}): Expected a closing square bracket"
                                      .format(self.current_token.filename, self.current_token.line))

        raise ParserException("Parsing Error (File {}) (Line {}): Expected a list index"
                              .format(self.current_token.filename, self.current_token.line))

    def _list(self):
        """Parse a list.

        Extended Backus-Naur form:
            list = LEFT_SQUARE, [ expression, { COMMA, expression } ], RIGHT_SQUARE ;

        """
        # list = LEFT_SQUARE, [ expression, { COMMA, expression } ], RIGHT_SQUARE
        if self.current_token.type == Token.LEFT_SQUARE:
            temporary_elements = []
            start_line = self.current_token.line
            self._advance_index()

            if self.current_token.type == Token.RIGHT_SQUARE:
                temporary = ast.List(temporary_elements)
                temporary.line = start_line
                temporary.filename = self.current_token.filename
                self._advance_index()

                return temporary
            else:
                temporary_expression = self._expression()

                temporary_elements.append(temporary_expression)

                while self.current_token.type == Token.COMMA:
                    self._advance_index()

                    temporary_expression = self._expression()

                    temporary_elements.append(temporary_expression)

                if self.current_token.type == Token.RIGHT_SQUARE:
                    temporary = ast.List(temporary_elements)
                    temporary.line = start_line
                    temporary.filename = self.current_token.filename
                    self._advance_index()

                    return temporary
                else:
                    raise ParserException("Parsing Error (File {}) (Line {}): Expected a closing square bracket"
                                          .format(self.current_token.filename, self.current_token.line))

        raise ParserException("Parsing Error (File {}) (Line {}): Expected a list"
                              .format(self.current_token.filename, self.current_token.line))

    def _function(self):
        """Parse a function.

        Extended Backus-Naur form:
            function = FUNCTION, [ SYMBOL ], LEFT_BRACKET, [ SYMBOL, { COMMA, SYMBOL } ], RIGHT_BRACKET, expression ;

        """
        # function = FUNCTION, [ SYMBOL ], LEFT_BRACKET, [ SYMBOL, { COMMA, SYMBOL } ], RIGHT_BRACKET, expression ;
        if self.current_token.type == Token.FUNCTION:
            start_line = self.current_token.line
            self._advance_index()

            if self.current_token.type == Token.SYMBOL:
                temporary_name = self.current_token.value
                self._advance_index()
            else:
                temporary_name = None

            if self.current_token.type == Token.LEFT_BRACKET:
                temporary_parameters = []
                self._advance_index()

                if self.current_token.type == Token.RIGHT_BRACKET:
                    self._advance_index()

                    temporary_expression = self._expression()

                    temporary = ast.FunctionDefinition(temporary_name, temporary_parameters, temporary_expression)
                    temporary.line = start_line
                    temporary.filename = self.current_token.filename

                    return temporary
                else:
                    if self.current_token.type == Token.SYMBOL:
                        temporary_parameters.append(self.current_token.value)
                        self._advance_index()
                    else:
                        raise ParserException("Parsing Error (File {}) (Line {}): Expected a symbol"
                                              .format(self.current_token.filename, self.current_token.line))

                    while self.current_token.type == Token.COMMA:
                        self._advance_index()

                        if self.current_token.type == Token.SYMBOL:
                            temporary_parameters.append(self.current_token.value)
                            self._advance_index()
                        else:
                            raise ParserException("Parsing Error (File {}) (Line {}): Expected a symbol"
                                                  .format(self.current_token.filename, self.current_token.line))

                    if self.current_token.type == Token.RIGHT_BRACKET:
                        self._advance_index()

                        temporary_expression = self._expression()

                        temporary = ast.FunctionDefinition(temporary_name, temporary_parameters, temporary_expression)
                        temporary.line = start_line
                        temporary.filename = temporary_expression.filename

                        return temporary
                    else:
                        raise ParserException("Parsing Error (File {}) (Line {}): Expected a closing bracket"
                                              .format(self.current_token.filename, self.current_token.line))
            else:
                raise ParserException("Parsing Error (File {}) (Line {}): Expected an open bracket"
                                      .format(self.current_token.filename, self.current_token.line))

        raise ParserException("Parsing Error (File {}) (Line {}): Expected a function definition"
                              .format(self.current_token.filename, self.current_token.line))

    def _arguments(self, holder):
        """Parse arguments.

        Extended Backus-Naur form:
            arguments = LEFT_BRACKET, [ expression, { COMMA, expression } ], RIGHT_BRACKET ;

        """
        # arguments = LEFT_BRACKET, [ expression, { COMMA, expression } ], RIGHT_BRACKET ;
        if self.current_token.type == Token.LEFT_BRACKET:
            temporary_arguments = []
            self._advance_index()

            if self.current_token.type == Token.RIGHT_BRACKET:
                try:
                    temporary = ast.FunctionCall(holder.value, temporary_arguments)
                    temporary.line = holder.line
                    temporary.filename = self.current_token.filename
                    self._advance_index()

                    return temporary
                except AttributeError:
                    temporary = ast.FunctionCall(holder, temporary_arguments)
                    temporary.line = holder.line
                    temporary.filename = self.current_token.filename
                    self._advance_index()

                    return temporary
            else:
                temporary_expression = self._expression()
                temporary_arguments.append(temporary_expression)

                while self.current_token.type == Token.COMMA:
                    self._advance_index()

                    temporary_expression = self._expression()
                    temporary_arguments.append(temporary_expression)

                if self.current_token.type == Token.RIGHT_BRACKET:
                    temporary = ast.FunctionCall(holder.value, temporary_arguments)
                    temporary.line = holder.line
                    temporary.filename = self.current_token.filename
                    self._advance_index()

                    return temporary
                else:
                    raise ParserException("Parsing Error (File {}) (Line {}): Expected a closing bracket"
                                          .format(self.current_token.filename, self.current_token.line))
        else:
            raise ParserException("Parsing Error (File {}) (Line {}): Expected an open bracket"
                                  .format(self.current_token.filename, self.current_token.line))

    def _while(self):
        """Parse a while.

        Extended Backus-Naur form:
            while = WHILE, expression, expression ;

        """
        # while = WHILE, expression, expression ;
        if self.current_token.type == Token.WHILE:
            start_line = self.current_token.line
            self._advance_index()

            temporary_condition = self._expression()

            temporary_expression = self._expression()

            temporary = ast.While(temporary_condition, temporary_expression)
            temporary.line = start_line
            temporary.filename = temporary_expression.filename

            return temporary

        raise ParserException("Parsing Error (File {}) (Line {}): Expected a while loop"
                              .format(self.current_token.filename, self.current_token.line))

    def _if(self):
        """Parse an if.

        Extended Backus-Naur form:
            if = IF, expression, expression, [ OTHERWISE, expression ] ;

        """
        # if = IF, expression, expression, [ OTHERWISE, expression ] ;
        if self.current_token.type == Token.IF:
            start_line = self.current_token.line
            self._advance_index()

            temporary_condition = self._expression()

            temporary_if_expression = self._expression()

            if self.current_token.type == Token.OTHERWISE:
                self._advance_index()

                temporary_else_expression = self._expression()

                temporary = ast.IfOtherwise(temporary_condition, temporary_if_expression, temporary_else_expression)
                temporary.line = start_line
                temporary.filename = temporary_else_expression.filename

                return temporary
            else:
                temporary = ast.IfOtherwise(temporary_condition, temporary_if_expression)
                temporary.line = start_line
                temporary.filename = temporary_if_expression.filename

                return temporary

        raise ParserException("Parsing Error (File {}) (Line {}): Expected an if-otherwise statement"
                              .format(self.current_token.filename, self.current_token.line))

    def _atom(self):
        """Parse an atom.

        Extended Backus-Naur form:
            atom = NUMBER
                 | LEFT_BRACKET, expression, { expression }, RIGHT_BRACKET
                 | SYMBOL, { arguments }, { list_index }
                 | if
                 | while
                 | function
                 | TEXT, { list_index }
                 | list, { list_index }
                 | RETURN, expression
                 | CONTINUE
                 | BREAK
                 | NULL
                 | IMPORT, TEXT ;

        """
        # atom = NUMBER ;
        if self.current_token.type == Token.NUMBER:
            temporary_number = self.current_token
            self._advance_index()

            temporary = ast.Number(temporary_number.value)
            temporary.line = temporary_number.line
            temporary.filename = temporary_number.filename

            return temporary

        # atom = LEFT_BRACKET, expression, { expression }, RIGHT_BRACKET ;
        elif self.current_token.type == Token.LEFT_BRACKET:
            temporary_expressions = []
            start_line = self.current_token.line
            self._advance_index()

            temporary_expression = self._expression()

            temporary_expressions.append(temporary_expression)

            while self.current_token.type != Token.RIGHT_BRACKET:
                temporary_expression = self._expression()

                temporary_expressions.append(temporary_expression)

            self._advance_index()

            temporary = ast.Expressions(temporary_expressions)
            temporary.line = start_line
            temporary.filename = temporary_expression.filename

            return temporary

        # atom = SYMBOL, { arguments }, { list_index } ;
        elif self.current_token.type == Token.SYMBOL:
            temporary_symbol = self.current_token
            temporary_call = temporary_symbol
            self._advance_index()

            while self.current_token.type == Token.LEFT_BRACKET:
                temporary_call = self._arguments(temporary_call)

            while self.current_token.type == Token.LEFT_SQUARE:
                try:
                    temporary_call = self._list_index(ast.Variable(temporary_call.value), temporary_call.line)
                except AttributeError:
                    temporary_call = self._list_index(temporary_call, temporary_call.line)

            if type(temporary_call) in (ast.ListIndex, ast.FunctionCall):
                temporary = temporary_call
                temporary.line = temporary_call.line
                temporary.filename = temporary_call.filename

                return temporary
            else:
                temporary = ast.Variable(temporary_call.value)
                temporary.line = temporary_call.line
                temporary.filename = temporary_call.filename

                return temporary

        # atom = if ;
        elif self.current_token.type == Token.IF:
            temporary = self._if()

            return temporary

        # atom = while ;
        elif self.current_token.type == Token.WHILE:
            temporary = self._while()

            return temporary

        # atom = function ;
        elif self.current_token.type == Token.FUNCTION:
            temporary = self._function()

            return temporary

        # atom = TEXT, { list_index } ;
        elif self.current_token.type == Token.TEXT:
            temporary_text = self.current_token
            self._advance_index()

            while self.current_token.type == Token.LEFT_SQUARE:
                try:
                    temporary_text = self._list_index(ast.Text(temporary_text.value), temporary_text.line)
                except AttributeError:
                    temporary_text = self._list_index(temporary_text, temporary_text.line)

            if isinstance(temporary_text, ast.ListIndex):
                temporary = temporary_text

                return temporary
            else:
                temporary = ast.Text(temporary_text.value)
                temporary.line = temporary_text.line
                temporary.filename = temporary_text.filename

                return temporary

        # atom = list, { list_index } ;
        elif self.current_token.type == Token.LEFT_SQUARE:
            temporary_list = self._list()

            while self.current_token.type == Token.LEFT_SQUARE:
                temporary_list = self._list_index(temporary_list, temporary_list.line)

            temporary = temporary_list

            return temporary

        # atom = RETURN, expression ;
        elif self.current_token.type == Token.RETURN:
            start_line = self.current_token.line
            self._advance_index()

            temporary_expression = self._expression()

            temporary = ast.Return(temporary_expression)
            temporary.line = start_line
            temporary.filename = temporary_expression.filename

            return temporary

        # atom = CONTINUE ;
        elif self.current_token.type == Token.CONTINUE:
            temporary = ast.Continue()
            temporary.line = self.current_token.line
            temporary.filename = self.current_token.filename
            self._advance_index()

            return temporary

        # atom = BREAK ;
        elif self.current_token.type == Token.BREAK:
            temporary = ast.Break()
            temporary.line = self.current_token.line
            temporary.filename = self.current_token.filename
            self._advance_index()

            return temporary

        # atom = NULL ;
        elif self.current_token.type == Token.NULL:
            temporary = ast.Null()
            temporary.line = self.current_token.line
            temporary.filename = self.current_token.filename
            self._advance_index()

            return temporary

        # atom = IMPORT, TEXT ;
        elif self.current_token.type == Token.IMPORT:
            start_line = self.current_token.line
            self._advance_index()

            if self.current_token.type == Token.TEXT:
                temporary_text = self.current_token
                self._advance_index()

                temporary = ast.Import(temporary_text.value)
                temporary.line = start_line
                temporary.filename = temporary_text.filename

                return temporary
            else:
                raise ParserException("Parsing Error (File {}) (Line {}): Expected nem file"
                                      .format(self.current_token.filename, self.current_token.line))

        raise ParserException("Parsing Error (File {}) (Line {}): Expected an atom"
                              .format(self.current_token.filename, self.current_token.line))

    def _power(self):
        """Parse a power.

        Extended Backus-Naur form:
            power = atom, { CARET, factor } ;

        """
        # power = atom, { CARET, factor } ;
        temporary = self._binary_operation(self._atom, Token.CARET, self._factor)

        return temporary

    def _factor(self):
        """Parse a factor.

        Extended Backus-Naur form:
            factor = [ PLUS | MINUS ], power ;

        """
        # factor = ( PLUS | MINUS ), power ;
        if self.current_token.type in (Token.PLUS, Token.MINUS):
            temporary_sign = self.current_token
            self._advance_index()

            temporary_power = self._power()

            temporary = ast.UnaryOperation(temporary_power, temporary_sign.value)
            temporary.line = temporary_sign.line
            temporary.filename = temporary_power.filename

            return temporary

        # factor = power ;
        temporary = self._power()

        return temporary

    def _term(self):
        """Parse a term.

        Extended Backus-Naur form:
            term = factor, { ( ASTERISK | SLASH ), factor } ;

        """
        # term = factor, { ( ASTERISK | SLASH ), factor } ;
        temporary = self._binary_operation(self._factor, (Token.ASTERISK, Token.SLASH), self._factor)

        return temporary

    def _arithmetic(self):
        """Parse an arithmetic.

        Extended Backus-Naur form:
            arithmetic = term, { ( PLUS | MINUS | MODULO ), term } ;

        """
        # arithmetic = term, { ( PLUS | MINUS | MODULO ), term } ;
        temporary = self._binary_operation(self._term, (Token.PLUS, Token.MINUS, Token.MODULO), self._term)

        return temporary

    def _not(self):
        """Parse a not.

        Extended Backus-Naur form:
            not = [ NOT ], arithmetic ;

        """
        # not = [ NOT ], arithmetic ;
        if self.current_token.type == Token.NOT:
            temporary_not = self.current_token
            self._advance_index()

            temporary_arithmetic = self._arithmetic()

            temporary = ast.UnaryOperation(temporary_arithmetic, temporary_not.value)
            temporary.line = temporary_not.line
            temporary.filename = temporary_arithmetic.filename

            return temporary

        temporary = self._arithmetic()
        return temporary

    def _comparison(self):
        """Parse a comparison.

        Extended Backus-Naur form:
            comparison = not, { ( IS | LESS | LESS_EQUAL | GREATER | GREATER_EQUAL ), not } ;

        """

        # comparison = not, { ( IS | LESS | LESS_EQUAL | GREATER | GREATER_EQUAL ), not } ;
        temporary = self._binary_operation(self._not,
                                           (Token.IS, Token.LESS, Token.LESS_EQUAL, Token.GREATER, Token.GREATER_EQUAL),
                                           self._not)

        return temporary

    def _expression(self):
        """Parse an expression.

        Extended Backus-Naur form:
            expression = comparison, { ( AND | OR ), comparison }
                       | SYMBOL, EQUAL, expression ;

        """
        # expression = comparison, { ( AND | OR ), comparison } ;
        temporary = self._binary_operation(self._comparison, (Token.AND, Token.OR), self._comparison)

        # expression = SYMBOL, EQUAL, expression ;
        if isinstance(temporary, ast.Variable) and self.current_token.type == Token.EQUAL:
            start_line = temporary.line
            self._advance_index()

            temporary_expression = self._expression()

            temporary = ast.AssignmentOperation(temporary.variable, temporary_expression)
            temporary.line = start_line
            temporary.filename = temporary_expression.filename

        return temporary

    def _parse(self):
        """Parse expressions."""
        while self.current_token.type != Token.EOF:
            temporary = self._expression()

            yield temporary

    def parse(self):
        """Parse the tokens into an AST.

        Parses the tokens that get returned from the lexer and builds an Abstract Syntax Tree out of them.

        Nem definitions (Extended Backus-Naur form):
            list_index = LEFT_SQUARE, expression, RIGHT_SQUARE ;
            list       = LEFT_SQUARE, [ expression, { COMMA, expression } ], RIGHT_SQUARE ;
            function   = FUNCTION, [ SYMBOL ], LEFT_BRACKET, [ SYMBOL, { COMMA, SYMBOL } ], RIGHT_BRACKET, expression ;
            arguments  = LEFT_BRACKET, [ expression, { COMMA, expression } ], RIGHT_BRACKET
            while      = WHILE, expression, expression ;
            if         = IF, expression, expression, [ OTHERWISE, expression ] ;
            atom       = NUMBER
                       | LEFT_BRACKET, expression, { expression }, RIGHT_BRACKET
                       | SYMBOL, { arguments }, { list_index }
                       | if
                       | while
                       | function
                       | TEXT, { list_index }
                       | list, { list_index }
                       | RETURN, expression
                       | CONTINUE
                       | BREAK
                       | NULL
                       | IMPORT, TEXT ;
            power      = atom, { CARET, factor } ;
            factor     = [ PLUS | MINUS ], power ;
            term       = factor, { ( ASTERISK | SLASH ), factor } ;
            arithmetic = term, { ( PLUS | MINUS | MODULO ), term } ;
            not        = [ NOT ], arithmetic ;
            comparison = not, { ( IS | LESS | LESS_EQUAL | GREATER | GREATER_EQUAL ), not } ;
            expression = comparison, { ( AND | OR ), comparison }
                       | SYMBOL, EQUAL, expression ;

        """
        return self._parse()


def main():
    """Debug the parser.

    Used as the entry-point when the file gets ran directly. Used for debugging the class Parser.

    """
    while True:
        print(list(Parser(Lexer(input(">> ") + "\n", "<stdin>").lex()).parse()))


if __name__ == "__main__":
    # Only activates when the file gets ran directly.
    from nem.lexer import Lexer

    main()
