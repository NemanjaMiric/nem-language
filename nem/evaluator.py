"""Hold Evaluator class.

Holds the Evaluator class which is used for evaluating the Abstract Syntax Tree created by the parser.

"""

from nem.exceptions import EvaluatorException
import nem.interpreter
import nem.nodes as ast
import nem.types_ as value


class Evaluator:

    """Evaluate the AST.

    Used for evaluating the Abstract Syntax Tree created by the parser.

    """

    def __init__(self, abstract_syntax_tree, symbol_table):
        """Initialize Evaluator class."""
        self.abstract_syntax_tree = abstract_syntax_tree
        self.symbol_table = symbol_table

    @staticmethod
    def _check(value_, return_error=None, continue_error=None, break_error=None):
        """Check for return, continue and break."""
        try:
            if value_[0] == "RETURN":
                if return_error is None:
                    return value_, True
                else:
                    raise EvaluatorException(return_error)
            elif value_[0] == "CONTINUE":
                if continue_error is None:
                    return value_, True
                else:
                    raise EvaluatorException(continue_error)
            elif value_[0] == "BREAK":
                if continue_error is None:
                    return value_, True
                else:
                    raise EvaluatorException(break_error)
        except TypeError:
            pass

        return value_, False

    @staticmethod
    def _evaluate_number(node, _):
        """Evaluate Number node."""
        return value.Number(node.value)

    @staticmethod
    def _evaluate_variable(node, symbol_table):
        """Evaluate Variable node."""
        temporary_variable = symbol_table.get(node.variable)

        if temporary_variable is not None:
            return temporary_variable
        else:
            raise EvaluatorException("Evaluation Error (File {}) (Line {}): Variable '{}' is not defined"
                                     .format(node.filename, node.line, node.variable))

    @staticmethod
    def _evaluate_text(node, _):
        """Evaluate Text node."""
        return value.Text(node.text)

    def _evaluate_list(self, node, symbol_table):
        """Evaluate List node."""
        temporary_elements = []

        for temporary_element in node.elements:
            temporary_value = self._check(
                self._evaluate_node(temporary_element, symbol_table),

                "Evaluation Error (File {}) (Line {}): Cannot return value inside of list"
                .format(node.filename, node.line),
                "Evaluation Error (File {}) (Line {}): Cannot continue inside of list"
                .format(node.filename, node.line),
                "Evaluation Error (File {}) (Line {}): Cannot break inside of list"
                .format(node.filename, node.line)
            )[0]

            temporary_elements.append(temporary_value)

        return value.List(temporary_elements)

    def _evaluate_listindex(self, node, symbol_table):
        """Evaluate ListIndex node."""
        temporary_holder = self._evaluate_node(node.holder, symbol_table)

        temporary_index = self._check(
            self._evaluate_node(node.index, symbol_table),

            "Evaluation Error (File {}) (Line {}): Cannot return value inside of list index"
            .format(node.filename, node.line),
            "Evaluation Error (File {}) (Line {}): Cannot continue inside of list index"
            .format(node.filename, node.line),
            "Evaluation Error (File {}) (Line {}): Cannot break inside of list index"
            .format(node.filename, node.line)
        )[0]

        if not isinstance(temporary_index, value.Number):
            raise EvaluatorException(
                "Evaluation Error (File {}) (Line {}): List index has to be a number"
                .format(node.filename, node.line)
            )

        try:
            # Text indexing
            if isinstance(temporary_holder, value.Text):
                return value.Text(temporary_holder.value[temporary_index.value])
            # List indexing
            elif isinstance(temporary_holder, value.List):
                return temporary_holder.value[temporary_index.value]
            else:
                raise EvaluatorException(
                    "Evaluation Error (Filename {}) (Line {}): '{}' does not support indexing"
                    .format(node.filename, node.line, type(temporary_holder).__name__)
                )
        except IndexError:
            raise EvaluatorException(
                "Evaluation Error (Filename {}) (Line {}): Index out of range"
                .format(node.filename, node.line)
            )

    def _evaluate_expressions(self, node, symbol_table):
        """Evaluate Expressions node."""
        temporary_value = (value.Null(), False)

        for expression in node.expressions:
            temporary_value = self._check(self._evaluate_node(expression, symbol_table))

            # If 'return', 'continue' or 'break' is detected, backpropagate
            if temporary_value[1]:
                return temporary_value[0]

        return temporary_value[0]

    def _evaluate_unaryoperation(self, node, symbol_table):
        """Evaluate UnaryOperation node."""
        temporary_value = self._check(
            self._evaluate_node(node.node, symbol_table),

            "Evaluation Error (File {}) (Line {}): Cannot perform unary operation on return"
            .format(node.filename, node.line),
            "Evaluation Error (File {}) (Line {}): Cannot perform unary operation on continue"
            .format(node.filename, node.line),
            "Evaluation Error (File {}) (Line {}): Cannot perform unary operation on break"
            .format(node.filename, node.line)
        )[0]

        if node.operator == "not":
            if isinstance(temporary_value, value.Number):
                return value.Number(0 if temporary_value.value else 1)
            elif isinstance(temporary_value, value.Text):
                return value.Number(0 if temporary_value.value else 1)
            elif isinstance(temporary_value, value.List):
                return value.Number(0 if temporary_value.value else 1)
            elif isinstance(temporary_value, value.Null):
                return value.Number(1)
            else:
                raise EvaluatorException(
                    "Evaluation Error (File {}) (Line {}): Cannot apply unary operator 'not' on '{}'"
                    .format(node.filename, node.line, type(temporary_value).__name__)
                )
        elif node.operator == "+":
            if isinstance(temporary_value, value.Number):
                return temporary_value
            else:
                raise EvaluatorException(
                    "Evaluation Error (File {}) (Line {}): Cannot apply unary operator '+' on '{}'"
                    .format(node.filename, node.line, type(temporary_value).__name__)
                )
        elif node.operator == "-":
            if isinstance(temporary_value, value.Number):
                return value.Number(-temporary_value.value)
            else:
                raise EvaluatorException(
                    "Evaluation Error (File {}) (Line {}): Cannot apply unary operator '-' on '{}'"
                    .format(node.filename, node.line, type(temporary_value).__name__)
                )
        else:
            raise EvaluatorException(
                "Evaluation Error (File {}) (Line {}): Unary operator '{}' not implemented"
                .format(node.filename, node.line, node.operator)
            )

    def _evaluate_binaryoperation(self, node, symbol_table):
        """Evaluate BinaryOperation node."""
        temporary_left_value = self._check(self._evaluate_node(node.left_node, symbol_table))

        # If 'return', 'continue' or 'break' is detected, backpropagate
        if temporary_left_value[1]:
            return temporary_left_value[0]
        temporary_left_value = temporary_left_value[0]

        temporary_right_value = self._check(self._evaluate_node(node.right_node, symbol_table))

        # If 'return', 'continue' or 'break' is detected, backpropagate
        if temporary_right_value[1]:
            return temporary_right_value[0]
        temporary_right_value = temporary_right_value[0]

        try:
            if node.operator == "+":
                return temporary_left_value + temporary_right_value
            elif node.operator == "-":
                return temporary_left_value - temporary_right_value
            elif node.operator == "%":
                return temporary_left_value % temporary_right_value
            elif node.operator == "*":
                return temporary_left_value * temporary_right_value
            elif node.operator == "/":
                return temporary_left_value / temporary_right_value
            elif node.operator == "^":
                return temporary_left_value ** temporary_right_value
            elif node.operator == "or":
                return temporary_left_value or temporary_right_value
            elif node.operator == "and":
                return temporary_left_value and temporary_right_value
            elif node.operator == "is":
                return temporary_left_value == temporary_right_value
            elif node.operator == "<":
                return temporary_left_value < temporary_right_value
            elif node.operator == "<=":
                return temporary_left_value <= temporary_right_value
            elif node.operator == ">":
                return temporary_left_value > temporary_right_value
            elif node.operator == ">=":
                return temporary_left_value >= temporary_right_value
            else:
                raise EvaluatorException(
                    "Evaluation Error (File {}) (Line {}): Binary operator '{}' not implemented"
                    .format(node.filename, node.line, node.operator)
                )
        except (NotImplementedError, TypeError):
            raise EvaluatorException(
                "Evaluation Error (File {}) (Line {}): Cannot apply binary operator '{}' to '{}' and '{}'"
                .format(
                    node.filename, node.line, node.operator,
                    type(temporary_left_value).__name__, type(temporary_right_value).__name__
                )
            )

    def _evaluate_assignmentoperation(self, node, symbol_table):
        """Evaluate AssignmentOperation node."""
        temporary_value = self._check(
            self._evaluate_node(node.value, symbol_table),

            "Evaluation Error (File {}) (Line {}): Cannot assign variable to return value"
            .format(node.filename, node.line),
            "Evaluation Error (File {}) (Line {}): Cannot assign variable to continue"
            .format(node.filename, node.line),
            "Evaluation Error (File {}) (Line {}): Cannot assign variable to break"
            .format(node.filename, node.line)
        )[0]

        symbol_table.set(node.variable, temporary_value)

        return temporary_value

    def _evaluate_ifotherwise(self, node, symbol_table):
        """Evaluate IfOtherwise node."""
        temporary_condition = self._check(
            self._evaluate_node(node.condition, symbol_table),

            "Evaluation Error (File {}) (Line {}): Cannot return value in condition"
            .format(node.filename, node.line),
            "Evaluation Error (File {}) (Line {}): Cannot continue in condition"
            .format(node.filename, node.line),
            "Evaluation Error (File {}) (Line {}): Cannot break in condition"
            .format(node.filename, node.line)
        )[0]

        # If condition is true
        if temporary_condition.value:
            temporary_expression = self._check(self._evaluate_node(node.if_expression, symbol_table))

            # If 'return', 'continue' or 'break' is detected, backpropagate
            if temporary_expression[1]:
                return temporary_expression[0]
        # Otherwise
        elif node.otherwise_expression is not None:
            temporary_expression = self._check(self._evaluate_node(node.otherwise_expression, symbol_table))

            # If 'return', 'continue' or 'break' is detected, backpropagate
            if temporary_expression[1]:
                return temporary_expression[0]

        return value.Null()

    def _evaluate_while(self, node, symbol_table):
        """Evaluate While node."""
        temporary_condition = self._check(
            self._evaluate_node(node.condition, symbol_table),

            "Evaluation Error (File {}) (Line {}): Cannot return value in condition"
            .format(node.filename, node.line),
            "Evaluation Error (File {}) (Line {}): Cannot continue in condition"
            .format(node.filename, node.line),
            "Evaluation Error (File {}) (Line {}): Cannot break in condition"
            .format(node.filename, node.line)
        )[0]

        while temporary_condition.value:
            temporary_return_value = self._check(self._evaluate_node(node.expression, symbol_table))

            # If 'break' is detected, break the loop
            if temporary_return_value[1] and temporary_return_value[0][0] == "BREAK":
                break

            temporary_condition = self._evaluate_node(node.condition, symbol_table)

        return value.Null()

    @staticmethod
    def _evaluate_functiondefinition(node, symbol_table):
        """Evaluate FunctionDefinition node."""
        temporary_function = value.Function(node.parameters, node.expression)
        symbol_table.set(node.name, temporary_function)
        return temporary_function

    def _evaluate_functioncall(self, node, symbol_table):
        """Evaluate FunctionCall node."""
        temporary_function = symbol_table.get(node.name)

        if temporary_function is None:
            if isinstance(node.name, ast.FunctionCall):
                temporary_function = self._evaluate_functioncall(node.name, symbol_table)
            else:
                raise EvaluatorException(
                    "Evaluation Error (File {}) (Line {}): Function '{}' is not defined"
                    .format(node.filename, node.line, node.name)
                )

        difference = len(temporary_function.parameters) - len(node.arguments)

        if difference > 0:
            raise EvaluatorException(
                "Evaluation Error (File {}) (Line {}): Function call for function '{}' is missing {} argument(s)"
                .format(node.filename, node.line, node.name, difference)
            )
        elif difference < 0:
            raise EvaluatorException(
                "Evaluation Error (File {}) (Line {}): Function call for function '{}' has too many argument(s) ({})"
                .format(node.filename, node.line, node.name, abs(difference))
            )

        temporary_symbol_table = symbol_table.copy()

        for parameter, argument in zip(temporary_function.parameters, node.arguments):
            argument = self._check(
                self._evaluate_node(argument, temporary_symbol_table),

                "Evaluation Error (File {}) (Line {}): Cannot return value in argument"
                .format(node.filename, node.line),
                "Evaluation Error (File {}) (Line {}): Cannot continue in argument"
                .format(node.filename, node.line),
                "Evaluation Error (File {}) (Line {}): Cannot break in argument"
                .format(node.filename, node.line)
            )[0]

            temporary_symbol_table.set(parameter, argument)

        if isinstance(temporary_function, value.Function):
            temporary_return_value = self._check(self._evaluate_node(temporary_function.body, temporary_symbol_table))

            # If 'return' is detected, return the value
            if temporary_return_value[1] and temporary_return_value[0][0] == "RETURN":
                return temporary_return_value[0][1]

            return value.Null()
        elif isinstance(temporary_function, value.BuiltInFunction):
            # 'print(element)' built-in function
            if temporary_function.index == 0:
                parameter_element = temporary_symbol_table.get("element")

                print(parameter_element, end="")

                return value.Null()
            # 'input()' built-in function
            elif temporary_function.index == 1:
                return value.Text(input())
            # 'convert(value, type)' built-in function
            elif temporary_function.index == 2:
                parameter_value = temporary_symbol_table.get("value")
                parameter_type = temporary_symbol_table.get("type")

                # Convert Number to...
                if isinstance(parameter_value, value.Number):
                    # ... Number
                    if parameter_type.value == "number":
                        return parameter_value
                    # ... Text
                    elif parameter_type.value == "text":
                        return value.Text(str(parameter_value.value))
                    # ... List
                    elif parameter_type.value == "list":
                        return value.List(list(str(parameter_value.value)))
                    else:
                        return parameter_value
                # Convert Text to...
                elif isinstance(parameter_value, value.Text):
                    # ... Number
                    if parameter_type.value == "number":
                        try:
                            return value.Number(float(parameter_value.value))
                        except ValueError:
                            return parameter_value
                    # ... Text
                    elif parameter_type.value == "text":
                        return parameter_value
                    # ... List
                    elif parameter_type.value == "list":
                        return value.List(list(str(parameter_value.value)))
                    else:
                        return parameter_value
                # Convert List to...
                elif isinstance(parameter_value, value.List):
                    # ... Number
                    if parameter_type.value == "number":
                        try:
                            return value.Number(float("".join(map(str, parameter_value.value))))
                        except ValueError:
                            return parameter_value
                    # ... Text
                    elif parameter_type.value == "text":
                        return value.Text("".join(map(str, parameter_value.value)))
                    # ... List
                    elif parameter_type.value == "list":
                        return parameter_value
                    else:
                        return parameter_value
                else:
                    return parameter_value
            else:
                raise EvaluatorException(
                    "Evaluation Error (File {}) (Line {}): Built-in function '{}' not implemented"
                    .format(node.filename, node.line, node.name)
                )
        else:
            raise EvaluatorException(
                "Evaluation Error (File {}) (Line {}): Function type '{}' not implemented"
                .format(node.filename, node.line, type(temporary_function))
            )

    @staticmethod
    def _evaluate_import(node, symbol_table):
        """Evaluate Import node."""
        try:
            with open("{}.nem".format(node.file)) as nem_file:
                temporary_code = nem_file.read()
                nem.interpreter.Interpreter(temporary_code, node.file, symbol_table)
        except FileNotFoundError:
            raise EvaluatorException(
                "Evaluation Error (File {}) (Line {}): File '{}.nem' doesn't exist"
                .format(node.filename, node.line, node.file)
            )

        return value.Null()

    def _evaluate_return(self, node, symbol_table):
        """Evaluate Return node."""
        temporary_return_value = self._check(
            self._evaluate_node(node.value, symbol_table),

            "Evaluation Error (File {}) (Line {}): Cannot return value within return value"
            .format(node.filename, node.line),
            "Evaluation Error (File {}) (Line {}): Cannot continue within return value"
            .format(node.filename, node.line),
            "Evaluation Error (File {}) (Line {}): Cannot break within return value"
            .format(node.filename, node.line)
        )[0]

        return "RETURN", temporary_return_value

    @staticmethod
    def _evaluate_continue(_, __):
        """Evaluate Continue node."""
        return "CONTINUE", None

    @staticmethod
    def _evaluate_break(_, __):
        """Evaluate Break node."""
        return "BREAK", None

    @staticmethod
    def _evaluate_null(_, __):
        """Evaluate Null node."""
        return value.Null()

    def _evaluate_node(self, node, symbol_table):
        """Evaluate a node."""
        try:
            method = getattr(self, "_evaluate_{}".format(type(node).__name__.lower()))
        except AttributeError:
            raise EvaluatorException(
                "Evaluation Error (File {}) (Line {}): Node '{}' is not defined"
                .format(node.filename, node.line, type(node).__name__)
            )

        return method(node, symbol_table)

    def _evaluate_all(self):
        """Evaluate all nodes."""
        for node in self.abstract_syntax_tree:
            current_result = self._check(
                self._evaluate_node(node, self.symbol_table),

                "Evaluation Error (File {}) (Line {}): 'return' not in function"
                .format(node.filename, node.line),
                "Evaluation Error (File {}) (Line {}): 'continue' not in loop"
                .format(node.filename, node.line),
                "Evaluation Error (File {}) (Line {}): 'break' not in loop"
                .format(node.filename, node.line)
            )[0]

            yield current_result

    def evaluate(self):
        """Evaluate the AST.

        Evaluator for Nem code. Evaluates the Abstract Syntax Tree created by the parser.

        """
        return self._evaluate_all()


def main():
    """Debug the evaluator.

    Used as the entry-point when the file gets ran directly. Used for debugging the class Evaluator.

    """
    symbol_table = SymbolTable()
    symbol_table.set("true", value.Number(1))
    symbol_table.set("false", value.Number(0))
    symbol_table.set("print", value.BuiltInFunction(["element"], 0))
    symbol_table.set("input", value.BuiltInFunction([], 1))
    symbol_table.set("convert", value.BuiltInFunction(["value", "type"], 2))

    while True:
        print(list(Evaluator(Parser(Lexer(input(">> ") + "\n", "<stdin>").lex()).parse(), symbol_table).evaluate()))


if __name__ == "__main__":
    # Only activates when the file gets ran directly.
    from nem.lexer import Lexer
    from nem.parser import Parser
    from nem.symbol_table import SymbolTable

    main()
