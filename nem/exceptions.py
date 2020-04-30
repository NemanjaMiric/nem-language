"""Raise exceptions.

Holds multiple exceptions.

Exceptions:
LexerException - During lexing
ParserException - During parsing
EvaluatorException - During evaluation

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


class EvaluatorException(Exception):

    """Raise exception.

    Gets raised when an error appears during evaluation.

    """

    pass