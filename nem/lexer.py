"""Hold Lexer class.

Holds the Lexer class which is used for converting raw source code into tokens.

Tokens (Extended Backus-Naur form):
    LETTER_           = "A" | "B" | "C" | "D" | "E" | "F" | "G"
                      | "H" | "I" | "J" | "K" | "L" | "M" | "N"
                      | "O" | "P" | "Q" | "R" | "S" | "T" | "U"
                      | "V" | "W" | "X" | "Y" | "Z" | "a" | "b"
                      | "c" | "d" | "e" | "f" | "g" | "h" | "i"
                      | "j" | "k" | "l" | "m" | "n" | "o" | "p"
                      | "q" | "r" | "s" | "t" | "u" | "v" | "w"
                      | "x" | "y" | "z" ;
    DIGIT_            = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;
    ESCAPED_          = "\n" | "\t" | "\\" | '\"' ;
    NUMBER            = { DIGIT_ }, [ "." ], DIGIT_, { DIGIT_ } ;
    TEXT              = '"', { ? any character other than double quotation mark ? | ESCAPED_ }, '"' ;
    SYMBOL            = LETTER_ | "_", { LETTER_ | "_" | DIGIT_ } ;
    NULL              = "null" ;
    COMMA             = "," ;
    CARET             = "^" ;
    ASTERISK          = "*" ;
    SLASH             = "/" ;
    PLUS              = "+" ;
    MINUS             = "-" ;
    EQUAL             = "=" ;
    WHILE             = "while" ;
    LEFT_BRACKET      = "(" ;
    RIGHT_BRACKET     = ")" ;
    IF                = "if" ;
    OTHERWISE         = "otherwise" ;
    FUNCTION          = "function" ;
    IMPORT            = "import" ;
    LEFT_SQUARE       = "[" ;
    RIGHT_SQUARE      = "]" ;
    BREAK             = "break" ;
    CONTINUE          = "continue" ;
    RETURN            = "return" ;
    NOT               = "not" ;
    OR                = "or" ;
    AND               = "and" ;
    LESS              = "<" ;
    LESS_EQUAL        = "<=" ;
    GREATER           = ">" ;
    GREATER_EQUAL     = ">=" ;
    IS                = "is" ;
    MODULO            = "%" ;
    EOF               = ? end of file ? ;
    COMMENT_          = "#", { ? any character other than newline ? }, "\n" ;

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
        "while": Token.WHILE,
        "if": Token.IF,
        "otherwise": Token.OTHERWISE,
        "function": Token.FUNCTION,
        "import": Token.IMPORT,
        "break": Token.BREAK,
        "continue": Token.CONTINUE,
        "return": Token.RETURN,
        "not": Token.NOT,
        "or": Token.OR,
        "and": Token.AND,
        "is": Token.IS
    }

    def __init__(self, code, filename):
        """Initialize Lexer class."""
        self.code = code
        self.filename = filename

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
            raise LexerException("Lexing Error (File {}) (Line {}): No number found.".format(self.filename, self.line))

        length = 0

        # "[0-9]*\.?[0-9]*\Z" checks for a valid number (10, 10.2, .4, etc.)
        while self.current_character is not None                                                                       \
                and re.match("[0-9]*\.?[0-9]+\Z", self.code[self.current_index - length:self.current_index + 1])       \
                or self.current_character == ".":
            length += 1
            self._advance_index()

        if self.previous_character == ".":
            raise LexerException("Lexing Error (File {}) (Line {}): Unrecognized token"
                                 .format(self.filename, self.line))

        return self.code[self.current_index - length:self.current_index]

    def _next_symbol(self):
        """Return next symbol."""
        # Tries to find the next symbol
        while self.current_character is not None and not re.match("[a-zA-Z_]", self.current_character):
            self._advance_index()

        if self.current_character is None:
            raise LexerException("Lexing Error (File {}) (Line {}): No symbol found.".format(self.filename, self.line))

        length = 0

        # "[a-zA-Z_][a-zA-Z_0-9]*\Z" checks for a valid symbol, but many other tokens (purposefully) pass as well
        while self.current_character is not None                                                                       \
                and re.match("[a-zA-Z_][a-zA-Z_0-9]*\Z", self.code[self.current_index - length:self.current_index + 1]):
            length += 1
            self._advance_index()

        return self.code[self.current_index - length:self.current_index]

    def _next_text(self):
        """Return next text.

        Everything between the current or found quotation mark and the next unescaped one gets lexed.

        """
        # Tries to find the next text
        while self.current_character is not None and self.current_character != "\"":
            self._advance_index()

        if self.current_character is None:
            raise LexerException("Lexing Error (File {}) (Line {}): No text found.".format(self.filename, self.line))

        length = 0
        self._advance_index()

        escaped_characters = (
            "n",
            "t",
            "\"",
            "\\"
        )

        # Up until it reaches the closing quotation mark, it continues adding all the characters to text
        while self.current_character is not None and self.current_character != "\"":
            length += 1
            self._advance_index()

            if self.previous_character == "\\" and self.current_character in escaped_characters:
                length += 1
                self._advance_index()

        if self.current_character is None:
            raise LexerException("Lexing Error (File {}) (Line {}): Text doesn't have an end"
                                 .format(self.filename, self.line))

        self._advance_index()

        # -1s are added because of self._advance_index() at the end, which increases self.current_index by 1
        return self.code[self.current_index - length - 1:self.current_index - 1]\
            .replace("\\n", "\n").replace("\\t", "\t").replace('\\"', "\"")

    def _next_token(self):
        """Return next token."""
        if self.current_character is None:
            token = None

        # Ignores whitespaces and tabs
        elif self.current_character in " \t":
            self._advance_index()
            token = False

        # Lexes COMMA token
        elif self.current_character == ",":
            token = Token(Token.COMMA, self.current_character, self.filename, self.line)
            self._advance_index()

        # Lexes CARET token
        elif self.current_character == "^":
            token = Token(Token.CARET, self.current_character, self.filename, self.line)
            self._advance_index()

        # Lexes ASTERISK token
        elif self.current_character == "*":
            token = Token(Token.ASTERISK, self.current_character, self.filename, self.line)
            self._advance_index()

        # Lexes SLASH token
        elif self.current_character == "/":
            token = Token(Token.SLASH, self.current_character, self.filename, self.line)
            self._advance_index()

        # Lexes PLUS token
        elif self.current_character == "+":
            token = Token(Token.PLUS, self.current_character, self.filename, self.line)
            self._advance_index()

        # Lexes MINUS token
        elif self.current_character == "-":
            token = Token(Token.MINUS, self.current_character, self.filename, self.line)
            self._advance_index()

        # Lexes MODULO token
        elif self.current_character == "%":
            token = Token(Token.MODULO, self.current_character, self.filename, self.line)
            self._advance_index()

        # Lexes EQUAL token
        elif self.current_character == "=":
            token = Token(Token.EQUAL, self.current_character, self.filename, self.line)
            self._advance_index()

        # Lexes LEFT_BRACKET token
        elif self.current_character == "(":
            token = Token(Token.LEFT_BRACKET, self.current_character, self.filename, self.line)
            self._advance_index()

        # Lexes RIGHT_BRACKET token
        elif self.current_character == ")":
            token = Token(Token.RIGHT_BRACKET, self.current_character, self.filename, self.line)
            self._advance_index()

        # Lexes LEFT_SQUARE token
        elif self.current_character == "[":
            token = Token(Token.LEFT_SQUARE, self.current_character, self.filename, self.line)
            self._advance_index()

        # Lexes RIGHT_SQUARE token
        elif self.current_character == "]":
            token = Token(Token.RIGHT_SQUARE, self.current_character, self.filename, self.line)
            self._advance_index()

        # Lexes LESS or LESS_EQUAL token
        elif self.current_character == "<":
            self._advance_index()
            if self.current_character == "=":
                token = Token(Token.LESS_EQUAL, "{}{}".format(self.previous_character, self.current_character),
                              self.filename, self.line)
                self._advance_index()
            else:
                token = Token(Token.LESS, self.previous_character, self.filename, self.line)

        # Lexes GREATER or GREATER_EQUAL token
        elif self.current_character == ">":
            self._advance_index()
            if self.current_character == "=":
                token = Token(Token.GREATER_EQUAL, "{}{}".format(self.previous_character, self.current_character),
                              self.filename, self.line)
                self._advance_index()
            else:
                token = Token(Token.GREATER, self.previous_character, self.filename, self.line)

        # Lexes TEXT token - everything between the current quotation mark and the next one gets lexed
        elif self.current_character == "\"":
            token = Token(Token.TEXT, self._next_text(), self.filename, self.line)

        # Lexes NUMBER token
        elif re.match("[0-9.]", self.current_character):
            token = Token(Token.NUMBER, self._next_number(), self.filename, self.line)

        # Lexes both SYMBOL tokens and tokens comprised of letters
        elif re.match("[a-zA-Z_]", self.current_character):
            temporary = self._next_symbol()

            try:
                token = Token(self.SYMBOLS[temporary], temporary, self.filename, self.line)
            except KeyError:
                # If it's not a token comprised of letters, it's a SYMBOL token
                token = Token(Token.SYMBOL, temporary, self.filename, self.line)

        elif self.current_character == "\n":
            self._advance_index()
            token = False

        # Comments - everything in-between '#' character and the next newline character gets ignored
        elif self.current_character == "#":
            while self.current_character is not None and self.current_character != "\n":
                self._advance_index()
            self._advance_index()

            token = False

        else:
            raise LexerException("Lexing Error (File {}) (Line {}): Unrecognized token"
                                 .format(self.filename, self.line))

        return token

    def _tokens(self):
        """Return all tokens."""
        current_token = self._next_token()

        while current_token is not None:
            # If the current token is a comment, skips the yield
            if current_token:
                yield current_token
            current_token = self._next_token()

        # Appends the EOF token
        yield Token(Token.EOF, None, self.filename, self.line)

    def lex(self):
        """Lex the code.

        Lexer for Nem code.

        Tokens (Extended Backus-Naur form):
            LETTER_           = "A" | "B" | "C" | "D" | "E" | "F" | "G"
                              | "H" | "I" | "J" | "K" | "L" | "M" | "N"
                              | "O" | "P" | "Q" | "R" | "S" | "T" | "U"
                              | "V" | "W" | "X" | "Y" | "Z" | "a" | "b"
                              | "c" | "d" | "e" | "f" | "g" | "h" | "i"
                              | "j" | "k" | "l" | "m" | "n" | "o" | "p"
                              | "q" | "r" | "s" | "t" | "u" | "v" | "w"
                              | "x" | "y" | "z" ;
            DIGIT_            = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;
            ESCAPED_          = "\n" | "\t" | "\\" | '\"' ;
            NUMBER            = { DIGIT_ }, [ "." ], DIGIT_, { DIGIT_ } ;
            TEXT              = '"', { ? any character other than double quotation mark ? | ESCAPED_ }, '"' ;
            SYMBOL            = LETTER_ | "_", { LETTER_ | "_" | DIGIT_ } ;
            NULL              = "null" ;
            COMMA             = "," ;
            CARET             = "^" ;
            ASTERISK          = "*" ;
            SLASH             = "/" ;
            PLUS              = "+" ;
            MINUS             = "-" ;
            EQUAL             = "=" ;
            WHILE             = "while" ;
            LEFT_BRACKET      = "(" ;
            RIGHT_BRACKET     = ")" ;
            IF                = "if" ;
            OTHERWISE         = "otherwise" ;
            FUNCTION          = "function" ;
            IMPORT            = "import" ;
            LEFT_SQUARE       = "[" ;
            RIGHT_SQUARE      = "]" ;
            BREAK             = "break" ;
            CONTINUE          = "continue" ;
            RETURN            = "return" ;
            NOT               = "not" ;
            OR                = "or" ;
            AND               = "and" ;
            LESS              = "<" ;
            LESS_EQUAL        = "<=" ;
            GREATER           = ">" ;
            GREATER_EQUAL     = ">=" ;
            IS                = "is" ;
            MODULO            = "%" ;
            EOF               = ? end of file ? ;
            COMMENT_          = "#", { ? any character other than newline ? }, "\n" ;

        """
        return self._tokens()


def main():
    """Debug the lexer.

    Used as the entry-point when the file gets ran directly. Used for debugging the class Lexer.

    """
    while True:
        print(list(Lexer(input(">> ") + "\n", "<stdin>").lex()))


if __name__ == "__main__":
    # Only activates when the file gets ran directly.
    main()
