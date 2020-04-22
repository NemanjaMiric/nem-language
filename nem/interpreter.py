"""Interpret Nem code.

Holds class Interpreter and used for debugging the class Interpreter.

"""


from nem.lexer import Lexer


class Interpreter:

    """Represent the interpreter.

    Used for representing the interpreter as a class.

    """

    def __init__(self, code):
        """Initialize the Interpreter class.

        Initializes the Interpreter class and adds a newline character to the end of the Nem code for handling EOF.

        """
        self.code = "{}\n".format(code)
        self.lexer = Lexer(self.code)

        self.tokens = self.lex()

    def lex(self):
        """Lex the code.

        Lexer for Nem code. Turns raw source code into tokens.

        Tokens:
        NUMBER = re'[0-9]*\.?[0-9]+'
        TEXT = re'".*"' ::: DOTALL flag
        SYMBOL = re'[a-zA-Z_][a-zA-Z_0-9]*'
        NULL = 'null'
        LIST_ELEMENT = ','
        CARET = '^'
        ASTERISK = '*'
        SLASH = '/'
        PLUS = '+'
        MINUS = '-'
        EQUAL = '='
        INPUT = 'input'
        OUTPUT = 'output'
        ERROR = 'error'
        WHILE = 'while'
        LEFT_BRACKET = '('
        RIGHT_BRACKET = ')'
        IF = 'if'
        OTHERWISE = 'otherwise'
        FUNCTION = 'function'
        IMPORT = 'import'
        FILE = 'file'
        READ = 'read'
        WRITE = 'write'
        CONVERT = 'convert'
        NUMBER_DEFINITION = 'number'
        TEXT_DEFINITION = 'text'
        LIST_DEFINITION = 'list'
        LEFT_SQUARE = '['
        RIGHT_SQUARE = ']'
        BREAK = 'break'
        CONTINUE = 'continue'
        RETURN = 'return'
        NOT = 'not'
        OR = 'or'
        AND = 'and'
        LESS = '<'
        LESS_EQUAL = '<='
        GREATER = '>'
        GREATER_EQUAL = '>='
        IS = 'is'

        Everything in between '#' character and newline character gets ignored.

        """
        return self.lexer.lex()

    def parse(self):
        """Parse the tokens.

        Parses the tokens that get returned from the lexer and builds an AST out of them.

        """
        pass


def main():
    """Debug the interpreter.

    Used as the entry-point when the file gets ran directly. It's usually used for debugging the class Interpreter.

    """
    while True:
        print(list(Interpreter(input(">> ")).lex()))


if __name__ == "__main__":
    # Only activates when the file gets ran directly.
    main()
