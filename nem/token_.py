"""Represent a token.

Holds class Token which is used when the code is being lexed.

"""


class Token:

    """Represent a token.

    Used for representing a token when the code is being lexed.

    """

    # Tokens
    NUMBER = "NUMBER"
    TEXT = "TEXT"
    SYMBOL = "SYMBOL"
    NULL = "NULL"
    COMMA = "COMMA"
    CARET = "CARET"
    ASTERISK = "ASTERISK"
    SLASH = "SLASH"
    PLUS = "PLUS"
    MINUS = "MINUS"
    EQUAL = "EQUAL"
    WHILE = "WHILE"
    LEFT_BRACKET = "LEFT_BRACKET"
    RIGHT_BRACKET = "RIGHT_BRACKET"
    IF = "IF"
    OTHERWISE = "OTHERWISE"
    FUNCTION = "FUNCTION"
    IMPORT = "IMPORT"
    LEFT_SQUARE = "LEFT_SQUARE"
    RIGHT_SQUARE = "RIGHT_SQUARE"
    BREAK = "BREAK"
    CONTINUE = "CONTINUE"
    RETURN = "RETURN"
    NOT = "NOT"
    OR = "OR"
    AND = "AND"
    LESS = "LESS"
    LESS_EQUAL = "LESS_EQUAL"
    GREATER = "GREATER"
    GREATER_EQUAL = "GREATER_EQUAL"
    IS = "IS"
    MODULO = "MODULO"
    EOF = "EOF"

    def __init__(self, type_, value, filename, line):
        """Initialize class Token.

        Used for initializing the Token class.

        """
        self.type = type_
        self.value = value
        self.filename = filename
        self.line = line

    def __repr__(self):
        """Represent Token class."""
        return "Token({}, {}, {}, {})".format(repr(self.type), repr(self.value), repr(self.filename), repr(self.line))

    def __eq__(self, other):
        """Check equality of Token class."""
        if isinstance(other, Token):
            return self.type == other.type and self.value == other.value and self.line == other.line
        else:
            raise NotImplementedError
