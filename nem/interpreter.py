"""Interpret Nem code.

Holds class Interpreter and used for debugging the class Interpreter.

"""


from nem.nemtoken import Token
from nem.exceptions import LexerException, ParserException
import re


class Interpreter:

    """Represent the interpreter.

    Used for representing the interpreter as a class.

    """

    def __init__(self, code):
        """Initialize the Interpreter class.

        Initializes the Interpreter class and adds a newline character to the end of the Nem code for handling EOF.

        """
        self.code = "{}\n".format(code)

    def lex(self):
        """Lex the code.

        Lexer for Nem code.

        List of tokens:
        ',' - <list-element>
        ';' - <end>
        r'[=+-*/^%<>]' - <operator>
        '(' - <left-bracket>
        ')' - <right-bracket>
        '[' - <left-square>
        ']' - <right-square>
        '"..."' - <text>
        r'[0-9]*[.]?[0-9]+' - <number>
        r'[a-z_][a-z_0-9]*' - <symbol>
        'null' - <null>
        'input' - <keyword>
        'output' - <keyword>
        'error' - <keyword>
        'while' - <keyword>
        'if' - <keyword>
        'otherwise' - <keyword>
        'import' - <keyword>
        'open' - <keyword>
        'convert' - <keyword>
        'number' - <keyword>
        'text' - <keyword>
        'list' - <keyword>
        'break' - <keyword>
        'continue' - <keyword>
        'function' - <keyword>
        'not' - <operator>
        'is' - <operator>
        'and' - <operator>
        'or' - <operator>

        Gets ignored:
        '#...\n' - Comment

        """
        tokens = []
        current_index = 0

        line = 1
        character = 1

        while current_index < len(self.code):
            current_token = self.code[current_index]

            if current_token == "\n":
                line += 1
                character = 1

            elif current_token == ",":
                tokens.append(Token("list-element", current_token))

            elif current_token == ";":
                tokens.append(Token("end", current_token))

            elif current_token in "=+-*/^%<>":
                tokens.append(Token("operator", current_token))

            elif current_token == "[":
                tokens.append(Token("left-square", current_token))

            elif current_token == "]":
                tokens.append(Token("right-square", current_token))

            elif current_token == "(":
                tokens.append(Token("left-bracket", current_token))

            elif current_token == ")":
                tokens.append(Token("right-bracket", current_token))

            elif current_token == "#":
                while self.code[current_index] != "\n":
                    current_index += 1
                line += 1
                character = 0

            elif current_token == "\"":
                current_index += 1
                start_index = current_index
                try:
                    while self.code[current_index] != "\"":
                        current_index += 1
                        character += 1
                except IndexError:
                    raise LexerException("Lexing Error (Line {}, Character: {}): Text doesn't have an end"
                                         .format(line, character))
                else:
                    tokens.append(Token("text", self.code[start_index:current_index]))

            elif re.match("[a-zA-Z_]", current_token):
                start_index = current_index
                current_index += 1
                character += 1
                while re.match("[a-zA-Z_][a-zA-Z_0-9]*\Z", self.code[start_index:current_index + 1]):
                    current_index += 1
                    character += 1
                if self.code[start_index:current_index] in ("input", "output", "error", "while", "if",
                                                            "otherwise", "import", "open", "convert", "number",
                                                            "text", "list", "break", "continue", "function"
                                                            ):
                    tokens.append(Token("keyword", self.code[start_index:current_index]))
                elif self.code[start_index:current_index] == "null":
                    tokens.append(Token("null", self.code[start_index:current_index]))
                elif self.code[start_index:current_index] in ("not", "is", "and", "or"):
                    tokens.append(Token("operator", self.code[start_index:current_index]))
                else:
                    tokens.append(Token("symbol", self.code[start_index:current_index]))
                continue

            elif re.match("[0-9.]", current_token):
                start_index = current_index
                current_index += 1
                character += 1
                while re.match("[0-9]*[.]?[0-9]+\Z", self.code[start_index:current_index + 1])                         \
                        or self.code[start_index:current_index + 1] == ".":
                    current_index += 1
                    character += 1
                if self.code[start_index:current_index] == ".":
                    raise LexerException("Lexing Error (Line {}, Character: {}): Unrecognized token"
                                         .format(line, character))
                else:
                    tokens.append(Token("number", self.code[start_index:current_index]))
                continue

            elif current_token in " \t":
                pass

            else:
                raise LexerException("Lexing Error (Line {}, Character: {}): Unrecognized token"
                                     .format(line, character))

            current_index += 1
            character += 1

        return tokens

    def parse(self):
        """Parse the tokens.

        Parses the tokens that get returned from the lexer and builds an AST out of them.

        """
        pass


def main():
    """Debug the interpreter.

    Used as the entry-point when the file gets ran directly. It's usually used for debugging the class Interpreter.

    """
    # For Debug purposes
    while True:
        print(Interpreter(input(">> ")).lex())


if __name__ == "__main__":
    # Only activates when the file gets ran directly.
    main()
