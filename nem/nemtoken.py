"""Represent a token.

Holds class Token which is used when the code is being lexed.

"""


class Token:

    """Represent a token.

    Used for representing a token when the code is being lexed.

    """

    def __init__(self, type_, value):
        """Initialize class Token.

        Used for initializing the Token class.

        """
        self.type = type_
        self.value = value

    def __repr__(self):
        """Represent Token class."""
        return "Token({}, {})".format(repr(self.type), repr(self.value))

    def __str__(self):
        """Convert Token class to string."""
        return "Token:{}={}".format(self.type, self.value)

    def __eq__(self, other):
        return self.type == other.type and self.value == other.value
