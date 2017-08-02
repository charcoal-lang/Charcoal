#!/usr/bin/env python3
from charcoal import Run
from random import choice, randint
from ast import literal_eval
import sys
import argparse

print("""\
Welcome to Charcoal tutor!
If you don't like copy-pasting commands, use -g for grave mode or \
-v for verbose mode.
If you've done this before, \
use -l to specify the last level you've completed.""")

parser = argparse.ArgumentParser(description="Helps learn Charcoal.")
parser.add_argument(
    "-v", "--verbose", action="store_true", help="Use verbose mode."
)
parser.add_argument(
    "-g", "--grave", action="store_true", help="Use grave mode."
)
parser.add_argument(
    "-l", "--level", type=int, nargs="?", default=0, help="Start from a level."
)
argv = parser.parse_args()

i = argv.level
index = 1 if argv.grave else 2 if argv.verbose else 0


def true(code):
    return True
trues = (true, true, true)


def word():
    return "".join([
        choice("bcdfghjklmnpqrstvwxz") + choice("aeiouy")
        for _ in range(randint(2, 5))
    ])[::choice([-1, 1])].replace("q", "qu")


def ensure(text, strings, expected, limits, validate=trues, inp=""):
    global i
    i += 1
    print("\033[32;1m=== Level %i ===\033[0m" % i)
    print(text % strings[index])
    print("Print:")
    print(expected)
    if inp:
        inputs = literal_eval(inp)
        print("With the input%s:" % ("s" * (len(inputs) > 1)))
        print("\n".join(literal_eval(inp)))
    try:
        while True:
            code = ""
            while not len(code):
                code = input("\033[36;1mCharcoal> \033[0m")
            if len(code) > limits[index]:
                print("Try again. Your code was too long.")
                continue
            if not validate[index](code):
                print("Try again. Please use the syntax given.")
                continue
            result = Run(code, inp, grave=argv.grave, verbose=argv.verbose)
            if result == expected:
                print("Congratulations on passing level %i!" % i)
                return
            if len(result):
                print("Try again. Your output was:")
                print(result)
            else:
                print("""\
Your code gave no output.
Did you make a mistake? Please read the level text \
to make sure you did not miss anything important.""")
    except (KeyboardInterrupt, EOFError):
        print()
        sys.exit()

for generator in [
    lambda: (
        lambda expected: (
            lambda expected, length: (
                """\
    The most important part of Charcoal is its literals.
    A string is %s.""",
                (
                    "a run of non-commands, \
    and/or commands preceded by the escape character '´'",
                    "a run of non-commands, \
    and/or commands preceded by the escape character '```'",
                    """an ordinary Python string.
    In verbose mode, Print() is needed to print a value."""
                ),
                expected,
                (length, length, length + 11)
            )
        )(expected, len(expected))
    )(word()),
    lambda: (
        lambda expected: (
            "A number is %s.",
            (
                "a run of any character in '⁰¹²³⁴⁵⁶⁷⁸⁹·'",
                "a run of '`0'-'`9' or '`.'",
                "an ordinary number"
            ),
            expected,
            (1, 2, 10)
        )
    )("-" * randint(5, 9)),
    lambda: (
        lambda expected: (
            lambda expected, length: (
                """\
    Another important part of Charcoal is its directional printing.
    Preceding a number with one of the directions %s \
    prints a line with a character selected from '-|/\\' in that direction.""",
                (
                    "'←↑→↓↖↗↘↙'",
                    "'``0'-'``9' according to numpad directions",
                    """
    :Up, :Down, :Left, :Right:UpLeft, :UpRight, :DownLeft and :DownRight"""
                ),
                expected,
                (2, 5, 22)
            )
        )(expected, len(expected))
    )(Run(choice("←↑→↓↖↗↘↙") + choice("⁵⁶⁷⁸⁹"))),
    lambda: (lambda expected: (
        """\
A language is never complete without arithmetic.
Charcoal has the basic arithmetic operators %s,
but the cast operator %s is needed to see the result as a number,
and a separator %s is needed to delimit two of the same literal type.%s""",
        (
            ("'⁺⁻×÷'", "'Ｉ'", "'¦'", ""),
            ("'`+`-`*`/'", "'`I'", "'`:'", ""),
            (
                """
Plus (+), Minus (-), Times (*) and Divide (/)""",
                "Cast",
                "',', ';' or ' '",
                """
In verbose mode, operators are called like functions:
e.g. Plus(1, 'a') or +(1, 'a')"""
            )
        ),
        expected,
        (5, 10, 22),
        (
            lambda code: code[0] == "Ｉ" and code[1] in "⁺⁻×÷",
            lambda code: code[:2] == "`I" and code[2:4] in "`+`-`*`/",
            lambda code: "Cast" in code and any(
                operator in code
                for operator in [
                    "+", "-", "*", "/", "Plus", "Minus", "Times", "Divide"
                ]
            )
        )
    ))(Run(
        "Ｉ" + choice("⁺⁻×÷") + choice("³⁴⁵⁶⁷⁸⁹") + "¦" + choice("³⁴⁵⁶⁷⁸⁹")
    )),
    lambda: (lambda expected: (
        """\
Operators work between most types.""",
        ((), (), ()),
        expected,
        (5, 10, 25)
    ))(chr(randint(33, 126)) * randint(4, 9)),
    lambda: (lambda expected: (
        """\
Charcoal can take number and string input, \
which are %s and %s respectively.""",
        (
            ("'Ｎ'", "'Ｓ'"),
            ("'`N'", "'`S'"),
            ("'InputNumber()'", "'InputString()'")
        ),
        expected,
        (1, 2, 25),
        (
            lambda code: code == "Ｓ",
            lambda code: code == "`S",
            lambda code: "InputString" in code
        ),
        repr([expected])
    ))(word()),
    lambda: (lambda expected: (
        """\
Unlike most other golfing languages, \
Charcoal uses a conventional memory model.
This means that in Charcoal you need to specify arguments, \
and assign to variables.
To assign to a variable, which is one of %s,
use the assignment command %s with the value and the variable name.
The input operators allow you to specify a variable name \
to assign the input to the variable.""",
        (
            ("'αβγδεζηθικλμνξπρσςτυφχψω'", "'Ａ'"),
            ("'`a`b`g`d`e`z`h`q`i`k`l`m`n`x`p`r`s`v`t`u`f`c`y`w'", "'`A'"),
            ("'abgdezhqiklmnxprsvtufcyw'", "Assign")
        ),
        expected * 2,
        (3, 6, 35),
        (
            lambda code: "Ｓ" in code,
            lambda code: "`S" in code,
            lambda code: "InputString" in code
        ),
        repr([expected])
    ))(word())
    # TODO: https://github.com/somebody1234/Charcoal/wiki/Tutorial
    # Next up:
    # Assign
    # Some more commands
    # loops (modulus for For, if (a) {}
][argv.level:]:
    ensure(*generator())

print("Congratulations on finishing the Charcoal interactive tutorial!")
