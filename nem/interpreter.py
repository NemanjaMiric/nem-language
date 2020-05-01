"""Interpret Nem code.

Holds class Interpreter.

"""


import nem.lexer
import nem.parser
import nem.evaluator
import nem.types_ as value


class Interpreter:

    """Represent the interpreter.

    Used for representing the interpreter as a class.

    """

    def __init__(self, code, filename, symbol_table):
        """Initialize the Interpreter class.

        Initializes the Interpreter class

        """
        self.code = code
        self.filename = filename
        self.symbol_table = symbol_table

        self.lexer = nem.lexer.Lexer(self.code, filename)
        self.tokens = self.lex()

        self.parser = nem.parser.Parser(self.tokens)
        self.ast = self.parse()

        self.evaluator = nem.evaluator.Evaluator(self.ast, self.symbol_table)
        self.return_values = tuple(self.evaluator.evaluate())

    def lex(self):
        """Lex the code.

        Lexer for Nem code. Turns raw source code into tokens.

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
        return self.lexer.lex()

    def parse(self):
        """Parse the tokens into an AST.

        Parses the tokens that get returned from the lexer and builds an Abstract Syntax Tree out of them.

        Nem definitions (Extended Backus-Naur form):
            list_index = LEFT_SQUARE, expression, RIGHT_SQUARE ;
            list       = LEFT_SQUARE, [ expression, { COMMA, expression } ], RIGHT_SQUARE ;
            function   = FUNCTION, [ SYMBOL ], LEFT_BRACKET, [ SYMBOL, { COMMA, SYMBOL } ], RIGHT_BRACKET, expression ;
            arguments  = LEFT_BRACKET, [ expression, { COMMA, expression } ], RIGHT_BRACKET
            while      = WHILE, expression, expression ;
            if         = IF, expression, expression, [ OTHERWISE, expression ] ;
            atom       = NUMBER
                       | LEFT_BRACKET, expression, { expression }, RIGHT_BRACKET
                       | SYMBOL, { arguments }, { list_index }
                       | if
                       | while
                       | function
                       | TEXT, { list_index }
                       | list, { list_index }
                       | RETURN, expression
                       | CONTINUE
                       | BREAK
                       | NULL
                       | IMPORT, TEXT ;
            power      = atom, { CARET, factor } ;
            factor     = [ PLUS | MINUS ], power ;
            term       = factor, { ( ASTERISK | SLASH ), factor } ;
            arithmetic = term, { ( PLUS | MINUS | MODULO ), term } ;
            not        = [ NOT ], arithmetic ;
            comparison = not, { ( IS | LESS | LESS_EQUAL | GREATER | GREATER_EQUAL ), not } ;
            expression = comparison, { ( AND | OR ), comparison }
                       | SYMBOL, EQUAL, expression ;

        """
        return self.parser.parse()

    def evaluate(self):
        """Evaluate the AST.

        Evaluator for Nem code. Evaluates the Abstract Syntax Tree created by the parser.

        """
        return self.evaluator.evaluate()


def main():
    """Debug the interpreter.

    Used as the entry-point when the file gets ran directly. It's usually used for debugging the class Interpreter.

    """
    # Built-in variables and functions
    symbol_table = SymbolTable()
    symbol_table.set("true", value.Number(1))
    symbol_table.set("false", value.Number(0))
    symbol_table.set("print", value.BuiltInFunction(["element"], 0))
    symbol_table.set("input", value.BuiltInFunction([], 1))
    symbol_table.set("convert", value.BuiltInFunction(["value", "type"], 2))

    while True:
        interpreter = Interpreter(input(">> "), "<stdin>", symbol_table)
        print(list(interpreter.return_values))


if __name__ == "__main__":
    # Only activates when the file gets ran directly.
    from nem.symbol_table import SymbolTable

    main()
