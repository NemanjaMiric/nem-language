# Nem Language Guide (v1.0.0)
Official Nem Language guide for version 1.0.0.

## Table of contents
- Nem Language Guide (v1.0.0)
  - [Encoding](#encoding)
  - [Comments](#comments)
  - [Variables](#variables)
  - [Literals](#literals)
  - [Numbers](#numbers)
  - [Text](#text)
  - [Null](#null)
  - [Lists](#lists)
  - [Functions](#functions)
  - [Built-in Functions](#built-in-functions)
    - [->`function print(element)`](#-function-printelement)
    - [->`function input()`](#-function-input)
    - [->`function convert(value, type)`](#-function-convertvalue-type)
  - [Assignments](#assignments)
  - [Control flow](#control-flow)
    - [Truthy and falsey values](#truthy-and-falsey-values)
    - [If-otherwise statement](#if-otherwise-statement)
    - [While statement](#while-statement)
      - [Break](#break)
      - [Continue](#continue)
  - [Operators](#operators)
    - [Unary Operators](#unary-operators)
    - [Binary Operators](#binary-operators)
  - [Indexing](#indexing)
  - [Importing](#importing)

## Encoding
Code needs to be encoded with UTF-8.

## Comments
Comments start with `#` and end at the next newline or end-of-file
```
# This is a comment

### Another comment ###
```

## Variables
Nem is a dynamic, weakly-typed programming language.
Variables can start with a letter or an underscore, but they can also contain numbers.
If you try to access an uninitialized variable, `EvaluatorException` is thrown.
```
tango = 100
charlie = variable_1

delta = tango + charlie # => 200

delta = bravo # => evaluation error
```

## Literals
Nem has 6 different types, of which 1 cannot be constructed (`BuiltInFunction`).

| Literal                                            | Type              |
|:--------------------------------------------------:|:-----------------:|
| `22`, `-16.7`, `true`, `false`                     | `Number`          |
| `"Tango"`, `"12345"`                               | `Text`            |
| `[1, 2, 3]`, `[1, [2, [3]]]`                       | `List`            |
| `null`                                             | `Null`            |
| `function foo() (return 0)`, `function() return 0` | `Function`        |
| `print`, `input`, `convert`                        | `BuiltInFunction` |

## Numbers
`Number` type holds both integers and decimal numbers of any size.
`Number` literals can be prefixed with either `+` (stays the same) or `-` (negates itself).
```
t_rex = 22
pterodactyl = -t_rex # => -22
triceratops = +32.17 # => 32.17
```
There are 2 built-in variables of type `Number`: `true` (equal to `1`) and `false` (equal to `0`).
```
crocodile = true # => 1
chicken = false # => 0
```

## Text
`Text` literals are lists of UTF-8 characters.
`Text` literals start with a `"` and end with an unescaped `"`.
```
message = "Hello, world!"
description = "It's a really nice message,
it really is"
```
There exist special, escaped, characters as well:
```
newline   = "\n" # => newline character
tab       = "\t" # => tab character
quote     = "\"" # => double quotation mark character
backslash = "\\" # => backslash character
```

## Null
`Null` type is similar to `None` in Python.
```
n0thing = null
```

## Lists
`List` literals are lists of items of any type.
`List` literals start with a `[` and end with a `]`.
```
nem = [null, 1, "2", [3]]
organized_list = [
    1, 2, 3, 4, 5
]
```

## Functions
Functions are defined as follows:
```
function main(argv) (
    return 0
)
```
Functions return `null` by default.
```
function test() (
    2 + 2
)

test() # => null

function foobar() (
    return 2 + 2
)

foobar() # => 4
```
Functions can also be anonymous.
```
x = function(a, b) (return a + b)

x(5, 17) # => 22
```
When calling a function, it's necessary to use the same amount of arguments as the amount of parameters.
```
function some_function(a, b, c)
    return a + b * c

some_function(1, 2, 3) # => 7
some_function(1, 2) # => evaluation error
some_function(1, 2, 3, 4) 3 => evaluation error
```

## Built-in Functions
There are 3 built-in functions: `print`, `input` and `convert`.

### ->`function print(element)`
Prints the element to stdout.
```
print("Hello, world!") # => prints "Hello, world!" to stdout
```

### ->`function input()`
Returns `Text` literal gotten from stdin.
```
number = input() # => grabs input from user

if number is "22" (
    print("Correct!")
)
```

### ->`function convert(value, type)`
Converts `value` to type `type` and returns it (`null` if not possible).
`type` can be either `"number"`, `"text"` or `"list"`.
```
number = convert(input(), "number")

if number is 22 (
    print("Correct!")
) otherwise (
    print("Not correct!")
)
```

## Assignments
Assignments are done via the `=` character.
```
a = 2 # => a is assigned to 2
a = b = c = d = 10 # => a, b, c and d are all set to 10
```

## Control flow
Nem includes `if-otherwise` and `while` statements.
It also includes keywords `continue` and `break`.

### Truthy and falsey values
Falsey values are: `null`, `0` (or `false`), `""` or `[]`.
Everything else is considered a truthy value.
```
if (null or 0 or "" or []) (
    print("This code is unreachable")
)
```

### If-otherwise statement
If-otherwise statements are constructed as follows:
```
if (2 < 2) (
    print("2 is less than 2!\n")
) otherwise (
    print("2 is greater than or equal to 2!\n")
)

if 3 >= 1 # => 'otherwise' is optional, brackets are also optional for single expressions
    print("3 is greater than or equal to 1!\n")
```
> Be careful while using a variable as a condition without surrounding it with brackets, `if true (print(1))` -> `true (print(1))` is considered a function.

### While statement
While statements are constructed as follows:
```
i = 0
while (i < 10) (
    print(i)
    print("\n")
    
    i = i + 1
)
```

#### Break
`break` can be used to break out of while statements.
```
i = 0
while (true) ( # => prints all values from 0 to 9 inclusive
    if (i < 10) (
        print(i)
        print("\n")
        
        i = i + 1
    ) otherwise (
        break
    )
)
```

#### Continue
`continue` can be used to repeat the while loop.
```
i = 0
while (true) ( # => prints all values from 0 to 9 inclusive
    if (i < 10) (
        print(i)
        print("\n")
        
        i = i + 1
        
        continue
    )
    
    break
)
```

## Operators
Operators can be either unary or binary.

### Unary Operators
```
+   # positive (leave as is)  :  +2 => 2
-   # negative (negate)       :  -2 => -2
not # not                     :  not 1 => 0

```

### Binary Operators
```
+   # addition
-   # subtraction
*   # multiplication
/   # division
%   # modulo
^   # exponentiation
is  # equality
or  # logical or
and # logical and
<   # less than
<=  # less than or equal to
>   # greater than
>=  # greater than or equal to
```

## Indexing
`Text` and `List` types can be indexed (also `Function` types and variables, but only if they return text or a list).
```
"Hello, world!"[5] # => ","
[1, 2, 3][0] # => 1

[1, [2, 3]][1][1] # => 3

function numbers()
    return [1, 2, 3]

numbers()[1] # => 2
```

## Importing
Importing is done via the `import` keyword. When called, the file specified gets ran through the interpreter.
The string after `import` holds the path to the file, so `import "../file.nem"` is possible.

**math.nem**
```
PI = 3.14

function circle(r) (
    return r * 2 * PI
)
```

**main.nem**
```
import "math"

PI # => 3.14
circle(5) # => 31.4
```
