"""Hold Lexer class.

Holds the Lexer class which is used for converting raw source code into tokens.

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
    MODULO = '%'

Everything in between '#' character and newline character gets ignored.

"""

from nem.token_ import Token
from nem.exceptions import LexerException
import re


class Lexer:

    """Convert source code into tokens.

    Used for converting raw source code into tokens.

    """

    SYMBOLS = {
        "null": Token.NULL,
        "input": Token.INPUT,
        "output": Token.OUTPUT,
        "error": Token.ERROR,
        "while": Token.WHILE,
        "if": Token.IF,
        "otherwise": Token.OTHERWISE,
        "function": Token.FUNCTION,
        "import": Token.IMPORT,
        "file": Token.FILE,
        "read": Token.READ,
        "write": Token.WRITE,
        "convert": Token.CONVERT,
        "number": Token.NUMBER_DEFINITION,
        "text": Token.TEXT_DEFINITION,
        "list": Token.LIST_DEFINITION,
        "break": Token.BREAK,
        "continue": Token.CONTINUE,
        "return": Token.RETURN,
        "not": Token.NOT,
        "or": Token.OR,
        "and": Token.AND,
        "is": Token.IS
    }

    def __init__(self, code):
        """Initialize Lexer class."""
        self.code = code

        self.current_index = 0
        self.previous_character = None
        self.current_character = code[0]

        self.line = 1

    def _advance_index(self):
        """Advance the current character."""
        self.current_index += 1
        self.previous_character = self.current_character
        self.current_character = self.code[self.current_index] if self.current_index < len(self.code) else None
        if self.previous_character == "\n" and self.current_character is not None:
            self.line += 1

    def _next_number(self):
        """Return next number relative to the current position."""
        # Tries to find the next number
        while self.current_character is not None and not re.match("[0-9.]", self.current_character):
            self._advance_index()

        if self.current_character is None:
            raise LexerException("No number found.")

        length = 0

        # "[0-9]*\.?[0-9]*\Z" checks for a valid number (10, 10.2, .4, etc.)
        while self.current_character is not None                                                                       \
                and re.match("[0-9]*\.?[0-9]+\Z", self.code[self.current_index - length:self.current_index + 1])       \
                or self.current_character == ".":
            length += 1
            self._advance_index()

        # If a number has a decimal place, but no decimals - LexerException is raised
        if self.previous_character == ".":
            raise LexerException("Lexing Error (Line {}): Unrecognized token".format(self.line))

        return self.code[self.current_index - length:self.current_index]

    def _next_symbol(self):
        """Return next symbol."""
        # Tries to find the next symbol
        while self.current_character is not None and not re.match("[a-zA-Z_]", self.current_character):
            self._advance_index()

        if self.current_character is None:
            raise LexerException("No symbol found.")

        length = 0

        # "[a-zA-Z_][a-zA-Z_0-9]*\Z" checks for a valid symbol, but many other tokens (purposefully) pass as well
        while self.current_character is not None                                                                       \
                and re.match("[a-zA-Z_][a-zA-Z_0-9]*\Z", self.code[self.current_index - length:self.current_index + 1]):
            length += 1
            self._advance_index()

        return self.code[self.current_index - length:self.current_index]

    def _next_text(self):
        """Return next text.

        Everything between the current or found quotation mark and the next one gets lexed.

        """
        # Tries to find the next text
        while self.current_character is not None and self.current_character != "\"":
            self._advance_index()

        if self.current_character is None:
            raise LexerException("No text found.")

        length = 0
        self._advance_index()

        # Up until it reaches the closing quotation mark, it continues adding all the characters to text
        while self.current_character is not None and self.current_character != "\"":
            length += 1
            self._advance_index()

        # If there's no closing quotation mark - LexerException is raised
        if self.current_character is None:
            raise LexerException("Lexing Error (Line {}): Text doesn't have an end".format(self.line))

        self._advance_index()

        # -1s are added because of self._advance_index() at the end, which increases self.current_index by 1
        return self.code[self.current_index - length - 1:self.current_index - 1]

    def _next_token(self):
        """Return next token."""
        if self.current_character is None:
            token = None

        # Ignores whitespaces and tabs
        elif self.current_character in " \t":
            self._advance_index()
            token = False

        # Lexes LIST_ELEMENT token
        elif self.current_character == ",":
            token = Token(Token.LIST_ELEMENT, self.current_character, self.line)
            self._advance_index()

        # Lexes CARET token
        elif self.current_character == "^":
            token = Token(Token.CARET, self.current_character, self.line)
            self._advance_index()

        # Lexes ASTERISK token
        elif self.current_character == "*":
            token = Token(Token.ASTERISK, self.current_character, self.line)
            self._advance_index()

        # Lexes SLASH token
        elif self.current_character == "/":
            token = Token(Token.SLASH, self.current_character, self.line)
            self._advance_index()

        # Lexes PLUS token
        elif self.current_character == "+":
            token = Token(Token.PLUS, self.current_character, self.line)
            self._advance_index()

        # Lexes MINUS token
        elif self.current_character == "-":
            token = Token(Token.MINUS, self.current_character, self.line)
            self._advance_index()

        # Lexes MODULO token
        elif self.current_character == "%":
            token = Token(Token.MODULO, self.current_character, self.line)
            self._advance_index()

        # Lexes EQUAL token
        elif self.current_character == "=":
            token = Token(Token.EQUAL, self.current_character, self.line)
            self._advance_index()

        # Lexes LEFT_BRACKET token
        elif self.current_character == "(":
            token = Token(Token.LEFT_BRACKET, self.current_character, self.line)
            self._advance_index()

        # Lexes RIGHT_BRACKET token
        elif self.current_character == ")":
            token = Token(Token.RIGHT_BRACKET, self.current_character, self.line)
            self._advance_index()

        # Lexes LEFT_SQUARE token
        elif self.current_character == "[":
            token = Token(Token.LEFT_SQUARE, self.current_character, self.line)
            self._advance_index()

        # Lexes RIGHT_SQUARE token
        elif self.current_character == "]":
            token = Token(Token.RIGHT_SQUARE, self.current_character, self.line)
            self._advance_index()

        # Lexes LESS or LESS_EQUAL token
        elif self.current_character == "<":
            self._advance_index()
            if self.current_character == "=":
                token = Token(Token.LESS_EQUAL, "{}{}".format(self.previous_character, self.current_character),
                              self.line)
                self._advance_index()
            else:
                token = Token(Token.LESS, self.previous_character, self.line)

        # Lexes GREATER or GREATER_EQUAL token
        elif self.current_character == ">":
            self._advance_index()
            if self.current_character == "=":
                token = Token(Token.GREATER_EQUAL, "{}{}".format(self.previous_character, self.current_character),
                              self.line)
                self._advance_index()
            else:
                token = Token(Token.GREATER, self.previous_character, self.line)

        # Lexes TEXT token - everything between the current quotation mark and the next one gets lexed
        elif self.current_character == "\"":
            token = Token(Token.TEXT, self._next_text(), self.line)

        # Lexes NUMBER token
        elif re.match("[0-9.]", self.current_character):
            token = Token(Token.NUMBER, self._next_number(), self.line)

        # Lexes both SYMBOL tokens and tokens comprised of letters
        elif re.match("[a-zA-Z_]", self.current_character):
            temporary = self._next_symbol()

            try:
                token = Token(self.SYMBOLS[temporary], temporary, self.line)
            except KeyError:
                # If it's not a token comprised of letters, it's a SYMBOL token
                token = Token(Token.SYMBOL, temporary, self.line)

        elif self.current_character == "\n":
            self._advance_index()
            token = False

        # Comments - everything in-between '#' character and the next newline character gets ignored
        elif self.current_character == "#":
            while self.current_character is not None and self.current_character != "\n":
                self._advance_index()
            self._advance_index()

            token = False

        # If there's no token to describe the current character - raises LexerException
        else:
            raise LexerException("Lexing Error (Line {}): Unrecognized token".format(self.line))

        return token

    def _tokens(self):
        """Return all tokens."""
        current_token = self._next_token()

        while current_token is not None:
            if current_token:
                yield current_token
            current_token = self._next_token()

    def lex(self):
        """Lex the code.

        Lexer for Nem code.

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
        MODULO = '%'

        Everything in between '#' character and newline character gets ignored.

        """
        return self._tokens()


def main():
    """Debug the lexer.

    Used as the entry-point when the file gets ran directly. Used for debugging the class Lexer.

    """
    while True:
        print(list(Lexer(input(">> ") + "\n").lex()))


if __name__ == "__main__":
    # Only activates when the file gets ran directly.
    main()
