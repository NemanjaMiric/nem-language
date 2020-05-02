#!/usr/bin/env python
"""Implement nemrun command."""

import nem
import sys

HELP = """Usage: nemrun [[-h, --help] | [-v, --version] | [-l, --license] | [file]]
\t-h, --help\tShow help.
\t-v, --version\tShow version.
\t-l, --license\tShow license."""

VERSION = """Nem 1.0.0 [<insert commit>] 5/1/2020"""

LICENSE = """MIT License

Copyright (c) 2020 Nemanja Mirić

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""


def script():
    """Evaluate the argument variables."""
    del sys.argv[0]

    if len(sys.argv) == 0 or sys.argv[0] in ("-h", "--help"):
        print(HELP)
    elif len(sys.argv) > 0 and sys.argv[0] in ("-v", "--version"):
        print("Nem 1.0.0 5/1/2020")
    elif len(sys.argv) > 0 and sys.argv[0] in ("-l", "--license"):
        print(LICENSE)
    else:
        with open(sys.argv[0]) as code:
            # Built-in variables and functions
            symbol_table = nem.symbol_table.SymbolTable()
            symbol_table.set("true", nem.types_.Number(1))
            symbol_table.set("false", nem.types_.Number(0))
            symbol_table.set("print", nem.types_.BuiltInFunction(["element"], 0))
            symbol_table.set("input", nem.types_.BuiltInFunction([], 1))
            symbol_table.set("convert", nem.types_.BuiltInFunction(["value", "type"], 2))

            nem.interpreter.Interpreter(code.read(), sys.argv[0], symbol_table)
