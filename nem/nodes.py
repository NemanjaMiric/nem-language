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

    """Hold a number.

    Holds a number.

    """

    def __init__(self, value):
        """Initialize Number class."""
        self.value = value

    def __repr__(self):
        """Represent Number class."""
        return "Number({})".format(repr(self.value))


class Variable(Node):

    """Hold a variable.

    Holds a variable.

    """

    def __init__(self, variable):
        """Initialize Variable class."""
        self.variable = variable

    def __repr__(self):
        """Represent Variable class."""
        return "Variable({})".format(repr(self.variable))


class Text(Node):

    """Hold text.

    Holds text.

    """

    def __init__(self, text):
        """Initialize Text class."""
        self.text = text

    def __repr__(self):
        """Represent Text class."""
        return "Text({})".format(repr(self.text))


class List(Node):

    """Hold a list.

    Holds a list.

    """

    def __init__(self, elements):
        """Initialize List class."""
        self.elements = elements

    def __repr__(self):
        """Represent List class."""
        return "List({})".format(repr(self.elements))


class ListIndex(Node):

    """Hold a list index.

    Holds a list index.

    """

    def __init__(self, holder, index):
        """Initialize ListIndex class."""
        self.holder = holder
        self.index = index

    def __repr__(self):
        """Represent ListIndex class."""
        return "ListIndex({}, {})".format(repr(self.holder), repr(self.index))


class Expressions(Node):

    """Hold expressions.

    Holds expressions.

    """

    def __init__(self, expressions):
        """Initialize Expressions class."""
        self.expressions = expressions

    def __repr__(self):
        """Represent Expressions class."""
        return "Expressions({})".format(repr(self.expressions))


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


class AssignmentOperation(Node):

    """Hold an assignment operation.

    Holds an assignment operation.

    """

    def __init__(self, variable, value):
        """Initialize AssignmentOperation class."""
        self.variable = variable
        self.value = value

    def __repr__(self):
        """Represent AssignmentOperation class."""
        return "AssignmentOperation({}, {})".format(repr(self.variable), repr(self.value))


class IfElse(Node):

    """Hold an if-else statement.

    Holds an if-else statement.

    """

    def __init__(self, condition, if_expression, else_expression=None):
        """Initialize IfElse class."""
        self.condition = condition
        self.if_expression = if_expression
        self.else_expression = else_expression

    def __repr__(self):
        """Represent IfElse class."""
        return "IfElse({}, {}, {})".format(repr(self.condition), repr(self.if_expression), repr(self.else_expression))


class While(Node):

    """Hold a while loop.

    Holds an while loop.

    """

    def __init__(self, condition, expression):
        """Initialize While class."""
        self.condition = condition
        self.expression = expression

    def __repr__(self):
        """Represent While class."""
        return "While({}, {})".format(repr(self.condition), repr(self.expression))


class FunctionDefinition(Node):

    """Hold a function definition.

    Holds a function definition.

    """

    def __init__(self, name, parameters, expression):
        """Initialize FunctionDefinition class."""
        self.name = name
        self.parameters = parameters
        self.expression = expression

    def __repr__(self):
        """Represent FunctionDefinition class."""
        return "FunctionDefinition({}, {}, {})".format(repr(self.name), repr(self.parameters), repr(self.expression))


class FunctionCall(Node):

    """Hold a function call.

    Holds a function call.

    """

    def __init__(self, name, arguments):
        """Initialize FunctionCall class."""
        self.name = name
        self.arguments = arguments

    def __repr__(self):
        """Represent FunctionCall class."""
        return "FunctionCall({}, {})".format(repr(self.name), repr(self.arguments))


class Import(Node):

    """Hold an import.

    Holds an import.

    """

    def __init__(self, filename):
        """Initialize Import class."""
        self.filename = filename

    def __repr__(self):
        """Represent Import class."""
        return "Import({})".format(repr(self.filename))


class Return(Node):

    """Hold a return value.

    Holds a return value.

    """

    def __init__(self, value):
        """Initialize Return class."""
        self.value = value

    def __repr__(self):
        """Represent Return class."""
        return "Return({})".format(repr(self.value))


class Continue(Node):

    """Hold a continue.

    Holds a continue.

    """

    def __init__(self):
        """Initialize Continue class."""
        pass

    def __repr__(self):
        """Represent Continue class."""
        return "Continue()"


class Break(Node):

    """Hold a break.

    Holds a break.

    """

    def __init__(self):
        """Initialize Break class."""
        pass

    def __repr__(self):
        """Represent Break class."""
        return "Break()"


class Null(Node):

    """Hold null.

    Holds null.

    """

    def __init__(self):
        """Initialize Null class."""
        pass

    def __repr__(self):
        """Represent Null class."""
        return "Null()"
