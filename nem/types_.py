"""Represent type values.

Used for representing type values during evaluation.

"""


class Type:

    """Hold methods used by all types.

    Holds methods used by all types.

    """

    value = None

    def __bool__(self):
        """Convert self to bool."""
        return bool(self.value)

    def __or__(self, other):
        """Return value of OR operator when used with self and other class."""
        try:
            return Number(1 if self.value or other.value else 0)
        except TypeError:
            return Null()

    def __and__(self, other):
        """Return value of AND operator when used with self and other class."""
        try:
            return Number(1 if self.value and other.value else 0)
        except TypeError:
            return Null()

    def __eq__(self, other):
        """Return value of == operator when used with self and other class."""
        try:
            return Number(1 if self.value == other.value else 0)
        except TypeError:
            return Null()

    def __lt__(self, other):
        """Return value of < operator when used with self and other class."""
        try:
            return Number(1 if self.value < other.value else 0)
        except TypeError:
            return Null()

    def __le__(self, other):
        """Return value of <= operator when used with self and other class."""
        try:
            return Number(1 if self.value <= other.value else 0)
        except TypeError:
            return Null()

    def __gt__(self, other):
        """Return value of > operator when used with self and other class."""
        try:
            return Number(1 if self.value > other.value else 0)
        except TypeError:
            return Null()

    def __ge__(self, other):
        """Return value of >= operator when used with self and other class."""
        try:
            return Number(1 if self.value >= other.value else 0)
        except TypeError:
            return Null()


class Number(Type):

    """Hold type number.

    Holds type number.

    """

    def __init__(self, value):
        """Initialize Number class."""
        self.value = float(value)
        if self.value.is_integer():
            self.value = int(self.value)

    def __repr__(self):
        """Represent Number class."""
        return "Number({})".format(repr(self.value))

    def __str__(self):
        """Convert Number class to string."""
        return str(self.value)

    def __add__(self, other):
        """Add Number and other class."""
        if isinstance(other, Number):
            temporary = self.value + other.value
            return Number(temporary)
        raise NotImplementedError

    def __sub__(self, other):
        """Subtract Number and other class."""
        if isinstance(other, Number):
            temporary = self.value - other.value
            return Number(temporary)
        raise NotImplementedError

    def __mod__(self, other):
        """Get remainder of Number divided by other class."""
        if isinstance(other, Number):
            temporary = self.value % other.value
            return Number(temporary)
        raise NotImplementedError

    def __mul__(self, other):
        """Multiply Number and other class."""
        if isinstance(other, Number):
            temporary = self.value * other.value
            return Number(temporary)
        raise NotImplementedError

    def __truediv__(self, other):
        """Divide Number and other class."""
        if isinstance(other, Number):
            try:
                temporary = self.value / other.value
            except ZeroDivisionError:
                return Null()
            return Number(int(temporary) if temporary.is_integer() else temporary)
        raise NotImplementedError

    def __pow__(self, other):
        """Raise Number to the power of other class."""
        if isinstance(other, Number):
            temporary = self.value ** other.value
            return Number(temporary)
        raise NotImplementedError


class Text(Type):

    """Hold type text.

    Holds type text.

    """

    def __init__(self, value):
        """Initialize Text class."""
        self.value = value

    def __repr__(self):
        """Represent Text class."""
        return "Text({})".format(repr(self.value))

    def __str__(self):
        """Convert Text class to string."""
        return str(self.value)

    def __add__(self, other):
        """Concatenate Text with other class."""
        if isinstance(other, Text):
            return Text(self.value + other.value)
        raise NotImplementedError

    def __mul__(self, other):
        """Concatenate Text to itself a number of times."""
        if isinstance(other, Number):
            return Text(self.value * other.value)
        raise NotImplementedError


class List(Type):

    """Hold type list.

    Holds type list.

    """

    def __init__(self, value):
        """Initialize List class."""
        self.value = value

    def __repr__(self):
        """Represent List class."""
        return "List({})".format(repr(self.value))

    def __str__(self):
        """Convert Number class to string."""
        return "[{}]".format(", ".join(map(str, self.value)))

    def __add__(self, other):
        """Concatenate List with other class."""
        if isinstance(other, List):
            return List(self.value + other.value)
        raise NotImplementedError

    def __mul__(self, other):
        """Concatenate List to itself a number of times."""
        if isinstance(other, Number):
            return List(self.value * other.value)
        raise NotImplementedError


class Null(Type):

    """Hold type null.

    Holds type null.

    """

    def __repr__(self):
        """Represent Null class."""
        return "Null()"

    def __str__(self):
        """Convert Null class to string."""
        return "null"


class Function(Type):

    """Hold type function.

    Holds type function.

    """

    def __init__(self, parameters, body):
        """Initialize Function class."""
        self.parameters = parameters
        self.body = body

    def __repr__(self):
        """Represent Function class."""
        return "Function({}, {})".format(self.parameters, self.body)


class BuiltInFunction(Type):

    """Hold type built-in function.

    Holds type built-in function.

    """

    def __init__(self, parameters, index):
        """Initialize BuiltInFunction class."""
        self.parameters = parameters
        self.index = index

    def __repr__(self):
        """Represent Function class."""
        return "BuiltInFunction({}, {})".format(self.parameters, self.index)
