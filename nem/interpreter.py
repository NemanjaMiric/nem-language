"""Interpret Nem code.

Holds class Interpreter and used for debugging the class Interpreter.

"""


from nem.nemtoken import Token
import re


class Interpreter:

    """Represent the interpreter.

    Used for representing the interpreter as a class.

    """

    def __init__(self, code):
        """Initialize the Interpreter class.

        Initializes the Interpreter class and adds a newline character to the end of the Nem code for handling EOF.

        """
        self.code = "{}\n".format(code.lower())

    def lex(self):
        """Lex the code.

        Lexer for Nem code.

        List of tokens:
        ',' - <list-element>
        '"..."' - <text>
        'input' - <stream>; 'output' - <stream>; 'error' - <stream>
        r'[=+-*/^]' - <symbol>
        r'[0-9]*[.]?[0-9]+' - <number>
        r'[a-z_][a-z_0-9]*' - <variable-any>

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

            elif current_token in "=+-*/^":
                tokens.append(Token("operation", current_token))

            elif current_token == "#":
                while self.code[current_index] != "\n":
                    current_index += 1
                    character += 1

            elif current_token == "\"":
                current_index += 1
                start_index = current_index
                try:
                    while self.code[current_index] != "\"":
                        current_index += 1
                        character += 1
                except IndexError:
                    print("Lexing Error (Line {}, Character: {}): Text doesn't have an end".format(line, character))
                    exit(-1)
                else:
                    tokens.append(Token("text", self.code[start_index:current_index]))

            elif re.match("[a-z_]", current_token):
                start_index = current_index
                current_index += 1
                character += 1
                while re.match("[a-z_][a-z_0-9]*\Z", self.code[start_index:current_index + 1]):
                    current_index += 1
                    character += 1
                if self.code[start_index:current_index] in ("input", "output", "error"):
                    tokens.append(Token("stream", self.code[start_index:current_index]))
                else:
                    tokens.append(Token("variable-any", self.code[start_index:current_index]))
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
                    print("Lexing Error (Line {}, Character: {}): Unrecognized token".format(line, character))
                    exit(-1)
                else:
                    tokens.append(Token("number", self.code[start_index:current_index]))
                continue

            elif current_token in " \t":
                pass

            else:
                print("Lexing Error (Line {}, Character: {}): Unrecognized token".format(line, character))
                exit(-1)

            current_index += 1
            character += 1

        return tokens


def main():
    """Debug the interpreter.

    Used as the entry-point when the file gets ran directly. It's usually used for debugging the class Interpreter.

    """
    # For Debug purposes
    while True:
        print(Interpreter(input(">> ")).lex())


if __name__ == "__main__":
    # Only gets activated when the file gets ran directly.
    main()
