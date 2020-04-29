"""Hold a symbol table.

Holds class SymbolTable. Used for storing variable names and their values.

"""


class SymbolTable:

    """Store variable names and their values.

    Used for storing variable names and their values.

    """

    def __init__(self):
        """Initialize SymbolTable class."""
        self.parent = None
        self.symbols = {}

    def get(self, name):
        """Return the value of the symbol with the specified name."""
        temporary_value = self.symbols.get(name, None)

        if temporary_value is None and self.parent is not None:
            temporary_value = self.parent.get(name)

        return temporary_value

    def set(self, name, value):
        """Set the value of the symbol with the specified name."""
        self.symbols[name] = value
