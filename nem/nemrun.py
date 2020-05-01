#!/usr/bin/env python
"""Implement nemrun command."""

import nem

import sys


def script():
    """Interpret nem file."""
    with open(sys.argv[1]) as code:
        # Built-in variables and functions
        symbol_table = nem.symbol_table.SymbolTable()
        symbol_table.set("true", nem.types_.Number(1))
        symbol_table.set("false", nem.types_.Number(0))
        symbol_table.set("print", nem.types_.BuiltInFunction(["element"], 0))
        symbol_table.set("input", nem.types_.BuiltInFunction([], 1))
        symbol_table.set("convert", nem.types_.BuiltInFunction(["value", "type"], 2))

        nem.interpreter.Interpreter(code.read(), sys.argv[1], symbol_table)
