"""Raise exceptions.

Holds multiple exceptions.

Exceptions:
LexerException - During lexing
ParserException - During parsing

"""


class LexerException(Exception):

    """Raise exception.

    Gets raised when an error appears during lexing.

    """

    pass


class ParserException(Exception):

    """Raise exception.

    Gets raised when an error appears during parsing.

    """

    pass
