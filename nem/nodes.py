"""Represent node elements.

Used for representing each node element for the AST.

"""


class Node:

    """Hold template.

    Template for node elements.

    """

    def __eq__(self, other):
        """Compare equality of classes."""
        if not isinstance(other, Node):
            raise NotImplementedError
        return type(self) == type(other) and self.__dict__ == other.__dict__


class Number(Node):

    """Hold number.

    Holds a number.

    """

    def __init__(self, value):
        """Initialize Number class."""
        self.value = value

    def __repr__(self):
        """Represent Number class."""
        return "Number({})".format(repr(self.value))


class UnaryOperation(Node):

    """Hold a unary operation.

    Holds a unary operation.

    """

    def __init__(self, node, operator):
        """Initialize UnaryOperation class."""
        self.node = node
        self.operator = operator

    def __repr__(self):
        """Represent UnaryOperation class."""
        return "UnaryOperation({}, {})".format(repr(self.node), repr(self.operator))


class BinaryOperation(Node):

    """Hold a binary operation.

    Holds a binary operation.

    """

    def __init__(self, left_node, operator, right_node):
        """Initialize BinaryOperation class."""
        self.left_node = left_node
        self.operator = operator
        self.right_node = right_node

    def __repr__(self):
        """Represent BinaryOperation class."""
        return "BinaryOperation({}, {}, {})".format(repr(self.left_node), repr(self.operator), repr(self.right_node))
