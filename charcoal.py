#!/usr/bin/env python3
"""
Charcoal's main module.

Contains definitions for the Charcoal canvas object, \
the CLI, and various classes used by the Charcoal class.

"""

# TODO List:
# !WIKI!
# bresenham
# image to ascii
# turn grammars into dictionaries (bison-style)
# escape to produce unicode char
# tests for reflect overlap overlap, floats, int divide and wolfram
# command to get result from new Charcoal instance
#   - will be default behavior when a command is passed a body
# fill overload to fill as background instead of greedy fill
# test list printing
# only throw errors in debug mode
# multiply/divide supporting float * string and list
# remove redundant newlines in all other files apart from wolfram
# - from compression on
# finish string ops in wolfram

from direction import Direction, DirectionToString, Pivot
from charcoaltoken import CharcoalToken, CharcoalTokenNames
from charactertransformers import *
from directiondictionaries import *
from unicodegrammars import UnicodeGrammars
from verbosegrammars import VerboseGrammars
from astprocessor import ASTProcessor
from interpreterprocessor import InterpreterProcessor
from stringifierprocessor import StringifierProcessor
from codepage import (
    UnicodeLookup, ReverseLookup, UnicodeCommands, InCodepage, sOperator
)
from compression import Decompressed, Compressed
from wolfram import *
from extras import *
from enum import Enum
from ast import literal_eval
from time import sleep, clock
import random
import re
import argparse
import os
import sys
import builtins
import types

for alias, builtin in [
    ("a", abs), ("b", bin), ("c", complex), ("e", enumerate), ("f", format),
    ("g", range), ("h", hex), ("i", __import__), ("m", sum), ("n", min),
    ("o", oct), ("p", repr), ("r", reversed), ("s", sorted), ("v", eval),
    ("x", max), ("z", zip)
]:
    setattr(builtins, alias, builtin)

imports = {}
python_function_is_command = {}

if os.name == "nt":
    import ansiterm  # for colors/screen clear
else:
    import readline  # for arrow/Ctrl+A/Ctrl+E support

try:
    # if python > 3.6 or back-compat module exists
    import typing

    def has_return_hint(function):
        """
        has_return_hint(function)

        Returns whether function has a return type hint.

        """
        return "return" in typing.get_type_hints(function)
except:

    def has_return_hint(function):
        """
        has_return_hint(function)

        Returns false since this Python installation has no typing module.

        """
        return false


def CleanExecute(function, *args, **kwargs):
    """
    CleanExecute(function, *args, **kwargs) -> Any

    Executes the given function with the given arguments, \
exiting if an error occurs.

    """
    try:
        return function(*args, **kwargs)
    except (KeyboardInterrupt, EOFError):
        sys.exit()


def Cleanify(function):
    """
    Cleanify(function) -> Function

    Returns the function changed to that it exits without a stack trace \
if an error occurs.

    """
    return lambda *args, **kwargs: CleanExecute(function, *args, **kwargs)

_open = open


def open(*args, **kwargs):
    """
    Open(*args, **kwargs)

    Returns a file object opened with UTF-8 encoding.

    """
    kwargs["encoding"] = "utf-8"
    return _open(*args, **kwargs)


def openl1(*args, **kwargs):
    """
    Open(*args, **kwargs)

    Returns a file object opened with UTF-8 encoding.

    """
    kwargs["encoding"] = "latin1"
    return _open(*args, **kwargs)

old_input = input
input = Cleanify(old_input)
sleep = Cleanify(sleep)


def Sign(number):
    """
    Sign(number)

    Return the mathematical sign of the given number.

    """
    return number and (-1, 1)[number > 0]


def large_range(number):
    """
    large_range(number)

    Yields numbers from 0 to the given number.

    Works for numbers that do not fit in a long integer.

    """
    n = 0

    while n < number:
        yield n
        n += 1


class Modifier(Enum):
    maybe = 1
    maybe_some = 2
    some = 3


class Info(Enum):
    prompt = 1
    is_repl = 2
    warn_ambiguities = 3
    step_canvas = 4
    dump_canvas = 5


class Whatever(object):
    def __add__(self, other):
        return other

    def __radd__(self, other):
        return other

    def __sub__(self, other):
        return -other

    def __rsub__(self, other):
        return other

    def __mul__(self, other):
        return other

    def __rmul__(self, other):
        return other

    def __truediv__(self, other):
        return 1 / other

    def __rtruediv__(self, other):
        return other

    def __floordiv__(self, other):
        return 1 // other

    def __rfloordiv__(self, other):
        return other // 1

    def __or__(self, other):
        return other

    def __ror__(self, other):
        return other

    def __and__(self, other):
        return other

    def __rand__(self, other):
        return other

    def __xor__(self, other):
        return other

    def __rxor__(self, other):
        return other

    def __mod__(self, other):
        return other

    def __rmod__(self, other):
        return other

whatever = Whatever()


class Coordinates(object):
    __slots__ = ("top", "coordinates")

    def __init__(self):
        self.top = 0
        self.coordinates = [[]]

    def FillLines(self, y):
        if y > self.top + len(self.coordinates) - 1:
            self.coordinates += [[] for _ in range(
                y - self.top - len(self.coordinates) + 1
            )]
        elif y < self.top:
            self.coordinates = [
                [] for _ in range(self.top - y)
            ] + self.coordinates
            self.top = y

    def Add(self, x, y):
        self.FillLines(y)
        self.coordinates[y - self.top] += [x]


class Scope(object):
    __slots__ = ("parent", "lookup")

    def __init__(self, parent={}):
        self.parent = parent
        self.lookup = {}

    def __contains__(self, key):
        return key in self.parent or key in self.lookup

    def __getitem__(self, key):
        if key in self.lookup:
            return self.lookup[key]
        else:
            return self.parent[key]

    def __setitem__(self, key, value):
        if key in self.lookup:
            self.lookup[key] = value
        elif key in self.parent:
            self.parent[key] = value
        else:
            self.lookup[key] = value

    def __delitem__(self, key):
        if key in self.lookup:
            del self.lookup[key]
        else:
            del self.parent[key]

    def __repr__(self):
        string = "{"
        for key in self.lookup:
            value = self.lookup[key]
            string += "%s: %s, " % (key, repr(value))
        string = string[:-2] + "}"
        if string == "}":
            string = "{}"
        return (
            string +
            "\n" +
            re.sub("^", "    ", repr(self.parent))
        )

    def get(self, key, fallback):
        return self[key] if key in self else fallback

    def set(self, key, value):
        self[key] = value

    def delete(self, key):
        del self[key]


class Cells(list):
    __slots__ = ("xs", "ys", "charcoal")

    def __init__(self, charcoal, value, xs, ys):
        super().__init__(value)
        self.xs = xs
        self.ys = ys
        self.charcoal = charcoal

    def __setitem__(self, i, value):
        super().__setitem__(i, value)
        if isinstance(i, slice):
            start = i.start or 0
            stop = len(self) if i.stop is None else i.stop
            for i in range(start, stop):
                self.charcoal.PutAt(self[i], self.xs[i], self.ys[i])
            return
        self.charcoal.PutAt(self[i], self.xs[i], self.ys[i])

    def __getitem__(self, i):
        super().__getitem__(i)
        if isinstance(i, slice):
            start = i.start or 0
            stop = len(self) if i.stop is None else i.stop
            return Cells(
                self.charcoal,
                self[start:stop],
                self.xs[start:stop],
                self.ys[start:stop]
            )
        return self[i]


class Charcoal(object):
    __slots__ = (
        "x", "y", "top", "lines", "indices", "lengths", "right_indices",
        "scope", "info", "original_input", "inputs", "original_inputs",
        "all_inputs", "hidden", "direction", "background", "bg_lines",
        "bg_line_number", "bg_line_length", "timeout_end", "dump_timeout_end",
        "background_inside", "trim", "print_at_end", "canvas_step",
        "last_printed", "charcoal"
    )

    secret = {
        "γ": " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ\
[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~",
        "β": "abcdefghijklmnopqrstuvwxyz",
        "α": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "ω": "",
        "ψ": "\000",
        "χ": 10,
        "φ": 1000,
        "υ": []
    }
    for key in dir(builtins):
        if key[0] != "_":
            secret[key] = getattr(builtins, key)
    globs = globals()
    for key in globs:
        if key[0] != "_":
            secret[key] = globs[key]
    wolfram = vars(__import__("wolfram"))
    for key in wolfram:
        if len(key) == 1 or key[1] != "_":
            if key[:2] == "_p":
                secret[key[2:]] = wolfram[key]
            elif key[0] == "_":
                secret[key[1:]] = wolfram[key]
            secret[key] = wolfram[key]
    extras = vars(__import__("extras"))
    for key in extras:
        if key[0] != "_":
            secret[key] = extras[key]

    def __init__(
        self,
        inputs=[],
        info=set(),
        canvas_step=500,
        original_input="",
        trim=False
    ):
        """
        Charcoal(inputs=[], info=set(), canvas_step=500, original_input="") \
-> Charcoal

        Creates a Charcoal canvas, \
an object on which all canvas drawing methods exist.

        """
        self.x = self.y = self.top = 0
        self.lines = [""]
        self.indices = [0]
        self.lengths = [0]
        self.right_indices = [0]
        self.scope = Scope()
        self.info = info
        self.original_input = original_input
        self.inputs = inputs
        self.original_inputs = inputs[:]
        self.all_inputs = inputs + [""] * (5 - len(inputs))
        self.hidden = {
            "θ": self.all_inputs[0],
            "η": self.all_inputs[1],
            "ζ": self.all_inputs[2],
            "ε": self.all_inputs[3],
            "δ": self.all_inputs[4]
        }
        self.direction = Direction.right
        self.background = " "
        self.bg_lines = []
        self.bg_line_number = self.bg_line_length = 0
        self.timeout_end = self.dump_timeout_end = 0
        self.background_inside = False
        self.trim = trim
        self.print_at_end = True
        self.canvas_step = canvas_step
        self.last_printed = None
        self.charcoal = None
        if Info.step_canvas in self.info:
            print("\033[2J")

    def __str__(self):
        """Returns the current state of the canvas."""
        left = min(self.indices)
        right = max(self.right_indices)
        string = ""
        bg_start = None
        if self.bg_lines:
            for i in range(len(self.lines)):
                top = self.top + i
                index = self.indices[i]
                line = self.lines[i]
                j = -1
                if self.background_inside:
                    for character in line:
                        j += 1
                        if character == "\000":
                            if bg_start is None:
                                bg_start = j
                        elif bg_start is not None:
                            line = (
                                line[:bg_start] +
                                self.BackgroundString(
                                    top, index + bg_start, index + j
                                ) +
                                line[j:]
                            )
                            bg_start = None
                    if bg_start is not None:
                        line = (
                            line[:bg_start] +
                            self.BackgroundString(
                                top, index + bg_start, index + j
                            )
                        )
                string += (
                    self.BackgroundString(
                        self.top + i, left, self.indices[i]
                    ) +
                    line +
                    ("" if self.trim else self.BackgroundString(
                        self.top + i, self.right_indices[i], right
                    )) +
                    "\n"
                )
            return string[:-1]
        else:
            if self.background_inside:
                for line, index, right_index in zip(
                    self.lines, self.indices, self.right_indices
                ):
                    string += (
                        self.background * (index - left) +
                        re.sub("\000", self.background, line) +
                        self.background * (right - right_index) +
                        "\n"
                    )
            else:
                for line, index, right_index in zip(
                    self.lines, self.indices, self.right_indices
                ):
                    string += (
                        self.background * (index - left) +
                        line +
                        ("" if self.trim else (
                            self.background * (right - right_index)
                        )) +
                        "\n"
                    )
            return string[:-1]

    def __getattribute__(self, attr):
        method = object.__getattribute__(self, attr)
        if isinstance(method, types.MethodType):
            self.last_printed = None
        return method

    def BackgroundString(self, y, start, end):
        """
        BackgroundString(y, start, end) -> str

        Returns the background for row at the specified y-coordinate,
        from the x-coordinates start to end.

        """
        bg_line = self.bg_lines[y % self.bg_line_number]
        index = start % self.bg_line_length
        bg_line = bg_line[index:] + bg_line[:index]
        length = end - start
        return (bg_line * (length // self.bg_line_length + 1))[:length]

    def Lines(self):
        """
        Lines() -> list[str]

        Returns the canvas padded to the leftmost and rightmost columns.

        """
        left = min(self.indices)
        right = max(self.right_indices)
        self.background_inside = True
        return [
            "\000" * (index - left) + line + "\000" * (right - right_index)
            for line, index, right_index in zip(
                self.lines, self.indices, self.right_indices
            )
        ]

    def AddInputs(self, inputs):
        """
        AddInputs(inputs)

        Adds given inputs to the inputs of the canvas.

        """
        self.original_inputs += inputs
        self.inputs = self.original_inputs[:]
        self.all_inputs = self.inputs + [""] * (5 - len(self.inputs))
        self.hidden["θ"] = self.all_inputs[0]
        self.hidden["η"] = self.all_inputs[1]
        self.hidden["ζ"] = self.all_inputs[2]
        self.hidden["ε"] = self.all_inputs[3]
        self.hidden["δ"] = self.all_inputs[4]

    def ClearInputs(self):
        """
        ClearInputs()

        Removes all inputs from canvas.

        """
        self.inputs = []
        self.original_inputs = []
        self.all_inputs = [""] * 5
        self.hidden["θ"] = ""
        self.hidden["η"] = ""
        self.hidden["ζ"] = ""
        self.hidden["ε"] = ""
        self.hidden["δ"] = ""

    def Trim(self):
        """
        Trim()

        Deletes empty cells on all four sides of the canvas.

        """
        to_delete = 0
        while re.match("^\000*$", self.lines[to_delete]):
            to_delete += 1
        to_delete -= 1
        if to_delete > 0:
            self.lines = self.lines[to_delete:]
            self.top += to_delete
        to_delete = -1
        while re.match("^\000*$", self.lines[to_delete]):
            to_delete -= 1
        to_delete += 1
        if to_delete < 0:
            self.lines = self.lines[:to_delete]
        for i in range(len(self.lines)):
            line = self.lines[i]
            match = re.match("^\000*", line)
            match_length = len(match.group(0)) if match else 0
            self.indices[i] += match_length
            self.lengths[i] -= match_length
            match_2 = re.match("\000*$", line)
            match_2_length = len(match_2.group(0)) if match_2 else 0
            self.right_indices[i] -= match_2_length
            self.lengths[i] -= match_2_length
            line = line[match_length:]
            if match_2_length > 0:
                line = line[:-match_2_length]
            self.lines[i] = line

    def Clear(self, all=True):
        """
        Clear(all=True)

        Resets Charcoal object to initial state.

        If all is False, only reset canvas

        """
        self.x = self.y = self.top = 0
        self.lines = [""]
        self.indices = [0]
        self.lengths = [0]
        self.right_indices = [0]
        if not all:
            return
        self.scope = Scope()
        self.inputs = self.original_inputs[:]
        self.direction = Direction.right
        self.background = " "
        self.bg_lines = []
        self.bg_line_number = self.bg_line_length = 0
        self.timeout_end = self.dump_timeout_end = 0
        self.background_inside = False
        self.trim = False
        self.print_at_end = True
        self.last_printed = None
        self.charcoal = None
        if Info.step_canvas in self.info:
            self.RefreshFastText("Clear", self.canvas_step)
        elif Info.dump_canvas in self.info:
            print("Clear")
            print(str(self))

    def Get(self):
        """
        Get() -> str

        Returns value of cell under cursor.

        """
        y_index = self.y - self.top
        if (
            y_index >= len(self.lines) or
            y_index < 0 or
            self.x - self.indices[y_index] >= self.lengths[y_index] or
            self.x - self.indices[y_index] < 0
        ):
            return ""
        return self.lines[y_index][self.x - self.indices[y_index]]

    def HasCharAt(self, x, y):
        """
        Get() -> str

        Returns value of cell under cursor.

        """
        x0, y0, self.x, self.y = self.x, self.y, x, y
        y_index = self.y - self.top
        result = True
        if (
            y_index < len(self.lines) and
            y_index >= 0 and
            self.x - self.indices[y_index] < self.lengths[y_index] and
            self.x - self.indices[y_index] >= 0
        ):
            result = (
                self.lines[y_index][self.x - self.indices[y_index]] != "\000"
            )
        self.x, self.y = x0, y0
        return result

    def PutAt(self, string, x, y):
        """
        PutAt(string, x, y)

        Put string at position x, y.

        """
        initial_x = self.x
        initial_y = self.y
        self.x = x
        self.y = y
        self.Put(string)
        self.x = initial_x
        self.y = initial_y

    def Put(self, string):
        """
        Put()

        Put string at cursor position.

        """
        y_index = self.y - self.top
        line = self.lines[y_index]
        delta_index = len(re.match("^\000*", line).group())
        self.indices[y_index] += delta_index
        x_index = self.indices[y_index]
        line = re.sub("\000+$", "", line[delta_index:])
        if not line:
            length = len(string)
            self.lines[y_index] = string
            self.indices[y_index] = self.x
            self.lengths[y_index] = length
            self.right_indices[y_index] = self.x + length
            return
        start = self.x - x_index
        end = start + len(string)
        if start - len(line) > 0 or end < 0:
            self.background_inside = True
        self.lines[y_index] = (
            line[:max(0, start)] +
            "\000" * (start - len(line)) +
            string +
            "\000" * -end +
            line[max(0, end):]
        )
        if start - len(line) > 0 or -end > 0:
            self.background_inside = True
        if self.x < x_index:
            self.indices[y_index] = self.x
        length = len(self.lines[y_index])
        self.lengths[y_index] = length
        self.right_indices[y_index] = self.indices[y_index] + length

    def FillLines(self):
        """
        FillLines()

        Adds empty lines up to the y-index of the cursor.

        """
        if self.y > self.top + len(self.lines) - 1:
            number = self.y - self.top - len(self.lines) + 1
            x_number = self.x - self.indices[-1]
            x_sign = Sign(x_number)
            x_number *= x_sign
            x_number = min(number, x_number)
            difference = number - x_number
            if x_sign == 1:
                indices = (
                    [0] * difference +
                    list(range(1, x_number + 1))
                )
            elif x_sign == -1:
                indices = (
                    [0] * difference +
                    list(range(-x_number, 0)[::-1])
                )
            else:
                indices = [0] * number
            self.lines += [""] * number
            self.indices += indices
            self.lengths += [0] * number
            self.right_indices += indices
        elif self.y < self.top:
            number = self.top - self.y
            x_number = self.x - self.indices[0]
            x_sign = Sign(x_number)
            x_number *= x_sign
            x_number = min(number, x_number)
            difference = number - x_number
            if x_sign == 1:
                indices = (
                    list(range(1, x_number + 1)[::-1]) +
                    [0] * difference
                )
            elif x_sign == -1:
                indices = (
                    list(range(-x_number, 0)) +
                    [0] * difference
                )
            else:
                indices = [0] * number
            self.lines = [""] * number + self.lines
            self.indices = indices + self.indices
            self.lengths = [0] * number + self.lengths
            self.right_indices = indices + self.right_indices
            self.top = self.y

    def SetBackground(self, string):
        """
        SetBackground(string)

        Sets the background of the canvas,
        tiling with the top left at (0, 0).

        """
        if len(string) > 1:
            lines = string.split("\n")
            length = max(len(line) for line in lines)
            self.bg_lines = [
                line + " " * (length - len(line))
                for line in lines
            ]
            self.bg_line_number = len(lines)
            self.bg_line_length = length
            if self.background:
                self.background = ""
        elif len(string):
            self.background = string
            if self.bg_lines:
                self.bg_lines = []
        else:
            print("RuntimeError: Cannot change background to nothing")
            if Info.is_repl not in self.info:
                sys.exit(1)
        if Info.step_canvas in self.info:
            self.RefreshFastText("Set background", self.canvas_step)
        elif Info.dump_canvas in self.info:
            print("Set background")
            print(str(self))

    def PrintLine(
        self, directions, length, string="", multiprint=False,
        coordinates=False, move_at_end=True, multichar_fill=False,
        overwrite=True
    ):
        """
        PrintLine(directions, length, string="", multiprint=False, \
coordinates=False, move_at_end=True, multichar_fill=False, overwrite=True)

        Prints the given string, repeated to the given length, \
in the specified directions away from the cursor.

        If the string is falsy, a character will be selected from \
\\/|-.

        If multiprint is true, the cursor will return to \
its original position.

        If coordinates is true, the coordinates of each character \
will be returned. If it is truthy, it will be assumed to be a \
Coordinates object and used as such.

        If move_at_end is false, the cursor will stay on \
the last character instead of moving to the cell after it.

        If multichar_fill is true, horizontal lines will also \
be added to the list of coordinates.

        If overwrite is false, existing characters will not be overwritten.

        """
        old_x = self.x
        old_y = self.y
        string_is_empty = not string
        length = int(length)
        if coordinates is True:
            coordinates = Coordinates()
        for direction in directions:
            if string_is_empty:
                string = DirectionCharacters[direction]
            self.x = old_x
            self.y = old_y
            if (
                overwrite and (
                    direction == Direction.right or
                    direction == Direction.left
                )
            ):
                if (
                    self.y < self.top or self.y > (self.top + len(self.lines))
                ) and re.match("\000*$", string):
                    continue
                self.FillLines()
                final = (string * (length // len(string) + 1))[:length]
                if direction == Direction.left:
                    final = final[::-1]
                    self.x -= length - 1
                self.Put(final)
                if multichar_fill:
                    coordinates.Add(self.x, self.y)
                    coordinates.Add(self.x + length - 1, self.y)
                if direction == Direction.right:
                    self.x += length - 1
                if move_at_end:
                    self.Move(direction)
            else:
                string_length = len(string)
                for i in range(length):
                    character = string[i % string_length]
                    if coordinates:
                        coordinates.Add(self.x, self.y)
                    self.FillLines()
                    current = self.Get()
                    if overwrite or not current or current == "\x00":
                        self.Put(character)
                    self.Move(direction)
                if not move_at_end:
                    self.Move(NewlineDirection[NewlineDirection[direction]])
        if multiprint:
            self.x = old_x
            self.y = old_y
        if coordinates:
            return coordinates

    def Print(
        self,
        string,
        directions=None,
        length=0,
        multiprint=False
    ):
        """
        Print(string, directions=None, length=0, multiprint=False)

        Prints a string, in the specified direcions from the cursor, \
repeated to the specified length if it is given.

        If string is in fact a number, print a line of the given length \
with a character automatically selected from -|/\\.

        If multiprint is true, the cursor will not be moved.

        """
        original = string

        def grid(matrix):
            # matrix = [[str(item) for item in row] for row in matrix]
            # maximum = max(max(len(item) for item in row) for row in matrix)
            return matrix

        def simplify(string):
            if isinstance(string, Expression):
                string = string.run()
                if isinstance(string, String):
                    return str(string)
                if isinstance(string, List):
                    # if isinstance(string[0], List):
                    #     return grid(string)
                    return [simplify(leaf) for leaf in string.leaves]
                if type(string) in [Rule, DelayedRule, Pattern]:
                    return ""  # TODO
                return string.to_number()
            return string
        string = simplify(string)
        if isinstance(string, float):
            string = int(string)
        if isinstance(string, int):
            length, string = string, ""
        elif isinstance(string, Direction):
            string = DirectionToString[string]
        length = int(length)
        if not directions:
            directions = {self.direction}
        if isinstance(string, list):
            newline_direction = NewlineDirection[list(directions)[0]]
            for element in string:
                self.Print(element, directions, multiprint=True)
                self.Move(newline_direction)
            return
        old_x = self.x
        old_y = self.y
        if length and "\n" not in string:
            self.PrintLine(directions, length, string, multiprint=multiprint)
            self.last_printed = original
            return
        lines = re.split("[\n\r]", string)
        seps = re.findall("[\n\r]", string)
        r_index = seps.index("\r") if "\r" in seps else -1
        for direction in directions:
            self.x = old_x
            self.y = old_y
            if direction == Direction.right:
                initial_x = self.x
                for i in range(len(lines)):
                    line = lines[i]
                    self.PrintLine({Direction.right}, len(line), line)
                    if i == r_index:
                        initial_x = 0
                    self.x = initial_x
                    self.y += 1
                self.y -= 1
                if lines[-1]:
                    self.Move(Direction.right, len(lines[-1]))
            elif direction == Direction.left:
                initial_x = self.x
                for i in range(len(lines)):
                    line = lines[i]
                    self.PrintLine({Direction.left}, len(line), line)
                    if i == r_index:
                        initial_x = 0
                    self.x = initial_x
                    self.y -= 1
                self.y += 1
                if lines[-1]:
                    self.Move(Direction.left, len(lines[-1]))
            else:
                newline_direction = NewlineDirection[direction]
                delta_x = XMovement[direction]
                delta_y = YMovement[direction]
                for i in range(len(lines) - 1):
                    line = lines[i]
                    line_start_x = self.x
                    line_start_y = self.y
                    for character in line:
                        self.FillLines()
                        self.Put(character)
                        self.x += delta_x
                        self.y += delta_y
                    self.x = line_start_x
                    self.y = line_start_y
                    self.Move(newline_direction)
                    if i == r_index:
                        if delta_x:
                            if delta_y:
                                n = (self.x * delta_x + self.y * delta_y) // 2
                                self.x += n * delta_x
                                self.y += n * delta_y
                            else:
                                self.x = 0
                        else:
                            self.y = 0
                for character in lines[-1]:
                    self.FillLines()
                    self.Put(character)
                    self.x += delta_x
                    self.y += delta_y
        if multiprint:
            self.x = old_x
            self.y = old_y
        if Info.step_canvas in self.info:
            self.RefreshFastText("Print", self.canvas_step)
        elif Info.dump_canvas in self.info:
            print("Print")
            print(str(self))
        self.last_printed = original

    def Multiprint(self, string, directions=None):
        """
        Multiprint(string, directions)

        Prints a string in the specified directions, \
moving the cursor back to its original position \
after it is finished.

        """
        self.Print(string, directions, multiprint=True)

    def Polygon(self, sides, character, fill=True):
        """
        Polygon(sides, character, fill=True)

        Draws a polygon with sides in the specified direction \
and length, filling with the specified character if \
the two endpoints of the line are can be joined with \
a horizontal, vertical or diagonal line.

        """
        multichar_fill = len(character) > 1
        if multichar_fill:
            lines = character.split("\n")
            character = "*"
        initial_x = self.x
        initial_y = self.y
        coordinates = Coordinates()
        for side in sides:
            direction = side[0]
            length = int(side[1])
            if length < 0:
                direction = NewlineDirection[NewlineDirection[direction]]
                length *= -1
            self.PrintLine(
                {direction},
                length,
                character,
                coordinates=coordinates,
                move_at_end=False,
                multichar_fill=multichar_fill
            )
            if Info.step_canvas in self.info:
                self.RefreshFastText("Polygon side", self.canvas_step)
            elif Info.dump_canvas in self.info:
                print("Polygon side")
                print(str(self))
        delta_x = initial_x - self.x
        sign_x = Sign(delta_x)
        delta_y = initial_y - self.y
        sign_y = Sign(delta_y)
        direction = DirectionFromXYSigns[sign_x][sign_y]
        length = (delta_x or delta_y) * (sign_x or sign_y) + 1
        if (
            not fill or
            delta_x and delta_y and delta_x * sign_x != delta_y * sign_y
        ):
            return
        final_x = self.x
        final_y = self.y
        self.PrintLine(
            {direction}, length, character, coordinates=coordinates,
            move_at_end=False, multichar_fill=multichar_fill
        )
        if Info.step_canvas in self.info:
            self.RefreshFastText("Polygon autoclose", self.canvas_step)
        elif Info.dump_canvas in self.info:
            print("Polygon autoclose")
            print(str(self))
        self.y = coordinates.top
        if multichar_fill:
            number_of_lines = len(lines)
            line_length = max([len(line) for line in lines])
            lines = [
                line + "\000" * (line_length - len(line)) for line in lines
            ]
            for row in coordinates.coordinates:
                line = lines[self.y % number_of_lines]
                while row:
                    start, end = row[:2]
                    row = row[2:]
                    if start > end:
                        start, end = end, start
                    index = start % line_length
                    length = end - start + 1
                    self.x = start
                    self.PrintLine(
                        {Direction.right},
                        length,
                        line[index:] + line[:index]
                    )
                self.y += 1
        else:
            for row in coordinates.coordinates:
                if len(row) % 2:
                    row = row[:-1] + row[-2:]
                while row:
                    start, end = row[:2]
                    row = row[2:]
                    if start > end:
                        start, end = end, start
                    if end - start < 2:
                        continue
                    length = end - start
                    self.x = start + 1
                    self.PrintLine({Direction.right}, length, character)
                self.y += 1
        self.x = final_x
        self.y = final_y
        if Info.step_canvas in self.info:
            self.RefreshFastText("Polygon fill", self.canvas_step)
        elif Info.dump_canvas in self.info:
            print("Polygon fill")
            print(str(self))

    def Oblong(self, width, height=0, fill=""):
        """
        Oblong(width, height, fill)

        Draws a rectangle with the specified dimensions, \
filled with the specified string.

        The top left of the rectangle is at the cursor.

        """
        if isinstance(height, str) and not fill:
            fill, height = height, width
        height, width = int(height), int(width)
        self.Polygon([
            [Direction.right, width],
            [Direction.down, height],
            [Direction.left, width],
            [Direction.up, height]
        ], fill)
        if Info.step_canvas in self.info:
            self.RefreshFastText("Oblong", self.canvas_step)
        elif Info.dump_canvas in self.info:
            print("Oblong")
            print(str(self))

    def Rectangle(self, width, height=None, border=None):
        """
        Rectangle(width, height, character=None)

        Draws a rectangle with the specified dimensions, \
with the border composed of the string, starting at \
the top left corner, going clockwise without overlap.

        If the border character is not given, - and | will \
be used for the sides and + for the corners.

        """
        if isinstance(height, str) and not border:
            border, height = height, width
        elif height is None:
            height = width
        if not width or not height:
            return
        height, width = int(height), int(width)
        if not border:
            initial_x = self.x
            initial_y = self.y
            if width > 0:
                self.PrintLine(
                    {Direction.right}, width, "-", move_at_end=False
                )
            else:
                self.PrintLine(
                    {Direction.left}, -width, "-", move_at_end=False
                )
            if height > 0:
                self.PrintLine(
                    {Direction.down}, height, "|", move_at_end=False
                )
            else:
                self.PrintLine({Direction.up}, -height, "|", move_at_end=False)
            if width > 0:
                self.PrintLine({Direction.left}, width, "-", move_at_end=False)
            else:
                self.PrintLine(
                    {Direction.right}, -width, "-", move_at_end=False
                )
            if height > 0:
                self.PrintLine({Direction.up}, height, "|", move_at_end=False)
            else:
                self.PrintLine(
                    {Direction.down}, -height, "|", move_at_end=False
                )
            self.Put("+")
            self.x += (
                width - 1 if width > 0 else width + 1 if width < 0 else 0
            )
            self.Put("+")
            self.y += (
                height - 1 if height > 0 else height + 1 if height < 0 else 0
            )
            self.Put("+")
            self.x = initial_x
            self.Put("+")
            self.y = initial_y
        else:
            h, w, height, width = (
                height > 0, width > 0, abs(height), abs(width)
            )
            length = len(border)
            self.PrintLine({
                Direction.right if w else Direction.left
            }, width, border, move_at_end=False)
            if height != 1 and height != -1:
                self.PrintLine(
                    {Direction.down if h else Direction.up},
                    height,
                    border[(width - 1) % length:] +
                    border[:(width - 1) % length],
                    move_at_end=False
                )
                self.PrintLine(
                    {Direction.left if w else Direction.right},
                    width,
                    border[(width + height - 2) % length:] +
                    border[:(width + height - 2) % length],
                    move_at_end=False
                )
                self.PrintLine(
                    {Direction.up if h else Direction.down},
                    height - 1,
                    border[(width * 2 + height - 3) % length:] +
                    border[:(width * 2 + height - 3) % length]
                )
        if Info.step_canvas in self.info:
            self.RefreshFastText((
                "Rectangle"
                if character else
                "Box"
            ), self.canvas_step)
        elif Info.dump_canvas in self.info:
            print("Rectangle" if character else "Box")
            print(str(self))

    def Fill(self, string):
        """
        Fill(string)

        Fills the empty area under the cursor \
with the specified string, repeating it if needed.

        """
        left, top, bottom = min(self.indices), self.top, len(self.lines)
        points = set()
        stack = []
        x0, y0 = self.x, self.y
        y, x = self.y, self.x

        class Segment(object):
            __slots__ = (
                "start_x", "end_x", "y", "direction", "scan_left", "scan_right"
            )
        
            def __init__(
                self, start_x, end_x, y, direction, scan_left, scan_right
            ):
                self.start_x = start_x
                self.end_x = end_x
                self.y = y
                self.direction = direction
                self.scan_left = scan_left
                self.scan_right = scan_right

        def add_line(
            start_x, end_x, y, ignore_start, ignore_end, direction,
            is_next_in_dir
        ):
            nonlocal stack
            region_start, x = left - 1, start_x
            while x < end_x:
                if (
                    (is_next_in_dir or x < ignore_start or x >= ignore_end) and
                    not self.HasCharAt(x, y) and
                    not (y, x) in points
                ):
                    points.add((y, x))
                    if region_start < left:
                        region_start = x
                elif region_start >= left:
                    stack += [Segment(
                        region_start, x, y, direction, region_start == start_x,
                        False
                    )]
                    region_start = left - 1
                if not is_next_in_dir and x < ignore_end and x >= ignore_start:
                    x = ignore_end - 1
                x += 1
            if region_start >= left:
                stack += [Segment(
                    region_start, x, y, direction, region_start == start_x,
                    True
                )]

        if self.HasCharAt(x, y):
            return
        points.add((y, x))
        stack += [Segment(x, x + 1, y, 0, True, True)]
        while len(stack):
            r = stack.pop()
            start_x, end_x = r.start_x, r.end_x
            if r.scan_left:
                while (
                    start_x > left and
                    not self.HasCharAt(start_x - 1, r.y) and
                    not (r.y, start_x - 1) in points
                ):
                    start_x -= 1
                    points.add((r.y, start_x))
            if r.scan_right:
                while (
                    not self.HasCharAt(end_x, r.y) and
                    not (r.y, end_x) in points
                ):
                    points.add((r.y, end_x))
                    end_x += 1
            r.start_x -= 1
            r.end_x += 1
            if r.y > top:
                add_line(
                    start_x, end_x, r.y - 1, r.start_x, r.end_x, -1,
                    r.direction <= 0
                )
            if r.y < bottom:
                add_line(
                    start_x, end_x, r.y + 1, r.start_x, r.end_x, 1,
                    r.direction >= 0
                )
        points = sorted(points)
        n_points = len(points)
        if isinstance(string, int) or isinstance(string, float):
            string = str(string)
        if isinstance(string, Expression):
            string = str(string.run(n_points))
        length = len(string)
        for i in range(len(points)):
            point = points[i]
            self.y, self.x = point
            character = string[i % length]
            if character != "\000":
                self.Put(character)
        self.x, self.y = x0, x0
        if Info.step_canvas in self.info:
            self.RefreshFastText("Fill", self.canvas_step)
        elif Info.dump_canvas in self.info:
            print("Fill")
            print(str(self))

    def Move(self, direction, length=1):
        """
        Move(direction, length=1)

        Moves cursor the specified number of cells \
in the specified direction.

        """
        if isinstance(direction, float):
            direction = int(direction)
        if isinstance(length, float):
            length = int(length)
        if isinstance(direction, int):
            self.x += direction
            self.y += length
        else:
            self.x += XMovement[direction] * length
            self.y += YMovement[direction] * length

    def Pivot(self, pivot, number=2):
        """
        Pivot(pivot, number=2)

        Pivots the cursor the specified number of rotations \
clockwise or counterclockwise depending on pivot.

        """
        for i in range(int(number)):
            self.direction = PivotLookup[pivot][self.direction]

    def Jump(self, x, y):
        """
        Jump(x, y)

        Moves cursor to the specified coordinates.

        """
        self.x, self.y = int(x), int(y)

    def ReflectButterfly(self, direction=Direction.right, overlap=1):
        """
        ReflectButterfly(direction=Direction.right)

        Reflect canvas in specified direction, reflecting characters \
whenever possible. The original is kept, and characters are not overwritten.

        """
        self.ReflectOverlap(direction, True, overlap)

    def ReflectTransform(self, direction=Direction.right):
        """
        ReflectTransform(direction=Direction.right)

        Reflect canvas in specified direction, reflecting characters \
whenever possible.

        """
        self.Reflect(direction, True)

    def ReflectMirror(self, direction=Direction.right):
        """
        ReflectMirror(direction=Direction.right)

        Reflect canvas in specified direction, reflecting characters \
whenever possible, and leaving the original intact.

        """
        self.ReflectCopy(direction, True)

    def ReflectCopy(self, direction=Direction.right, transform=False):
        """
        ReflectCopy(direction=Direction.right, transform=False)

        Reflect canvas in specified direction, reflecting characters \
whenever possible, and leaving the original intact. The closest \
characters to the axis are next to the axis.

        If transform is true, reflect characters in the copy.

        """
        if isinstance(direction, list):
            if not len(direction):
                self.ReflectCopy(Direction.right, transform)
            else:
                for direction_ in direction:
                    self.ReflectCopy(direction_, transform)
            return
        finished = True
        if direction == Direction.left:
            left = min(self.indices)
            self.x -= (self.x - left) * 2 + 1
            self.background_inside = True
            self.lines = [
                "".join(
                    HorizontalFlip.get(character, character)
                    for character in line[::-1]
                ) +
                "\000\000" * (index - left) +
                line
                for line, index in zip(self.lines, self.indices)
            ] if transform else [
                line[::-1] +
                "\000\000" * (index - left) +
                line
                for line, index in zip(self.lines, self.indices)
            ]
            self.lengths = [
                (length + index - left) * 2
                for length, index in zip(self.lengths, self.indices)
            ]
            self.indices = [
                left * 2 - right_index
                for right_index in self.right_indices
            ]
        elif direction == Direction.right:
            right = max(self.right_indices)
            self.x += (right - self.x) * 2 - 1
            self.lines = [
                line +
                "\000\000" * (right - right_index) +
                "".join(
                    HorizontalFlip.get(character, character)
                    for character in line[::-1]
                )
                for line, right_index in zip(self.lines, self.right_indices)
            ] if transform else [
                line +
                "\000\000" * (right - right_index) +
                line[::-1]
                for line, right_index in zip(self.lines, self.right_indices)
            ]
            self.background_inside = True
            self.lengths = [
                (length + right - right_index) * 2
                for length, right_index in zip(
                    self.lengths,
                    self.right_indices
                )
            ]
            self.right_indices = [
                right * 2 - index
                for index in self.indices
            ]
        elif direction == Direction.up:
            self.y -= (self.y - self.top) * 2 + 1
            self.top -= len(self.lines)
            self.lines = (
                [
                    "".join(
                        VerticalFlip.get(character, character)
                        for character in line
                    ) for line in self.lines[::-1]
                ]
                if transform else
                self.lines[::-1]
            ) + self.lines
            self.indices = self.indices[::-1] + self.indices
            self.lengths = self.lengths[::-1] + self.lengths
            self.right_indices = self.right_indices[::-1] + self.right_indices
        elif direction == Direction.down:
            self.y += (self.top + len(self.lines) - self.y) * 2 - 1
            self.lines += (
                [
                    "".join(
                        VerticalFlip.get(character, character)
                        for character in line
                    ) for line in self.lines[::-1]
                ]
                if transform else
                self.lines[::-1]
            )
            self.indices += self.indices[::-1]
            self.lengths += self.lengths[::-1]
            self.right_indices += self.right_indices[::-1]
        else:
            finished = False
        if finished:
            return
        initial_x = self.x
        initial_y = self.y
        self.Trim()
        if direction == Direction.up_left:
            top_left, negative_x = min(
                (x + y - 1, -i - x)
                for x, y, i in zip(
                    self.indices,
                    range(self.top, self.top + len(self.indices)),
                    range(len(self.indices))
                )
            )
            x = -negative_x
            self.x = x
            if transform:
                for line, length, index in zip(
                    self.lines[:], self.lengths[:], self.indices[:]
                ):
                    self.x -= 1
                    self.y = top_left - index
                    self.PrintLine(
                        {Direction.up},
                        length,
                        "".join(
                            NESWFlip.get(character, character)
                            for character in line
                        )
                    )
            else:
                for line, length, index in zip(
                    self.lines[:], self.lengths[:], self.indices[:]
                ):
                    self.x -= 1
                    self.y = top_left - index
                    self.PrintLine({Direction.up}, length, line)
            self.x = top_left - initial_y
            self.y = top_left - initial_x
        elif direction == Direction.up_right:
            top_right, negative_x = min(
                (y - x - 1, i - x + 1)
                for x, y, i in zip(
                    self.right_indices,
                    range(self.top, self.top + len(self.right_indices)),
                    range(len(self.right_indices))
                )
            )
            self.x = x = -negative_x
            if transform:
                for line, length, index in zip(
                    self.lines[:], self.lengths[:], self.indices[:]
                ):
                    self.x -= 1
                    self.y = top_left - index
                    self.PrintLine(
                        {Direction.up},
                        length,
                        "".join(
                            NWSEFlip.get(character, character)
                            for character in line
                        )
                    )
            else:
                for line, length, right_index in zip(
                    self.lines[:], self.lengths[:], self.right_indices[:]
                ):
                    self.x += 1
                    self.y = right_index + top_right
                    self.PrintLine({Direction.up}, length, line[::-1])
            self.x = initial_y - top_right - 1
            self.y = top_right + initial_x + 1
        elif direction == Direction.down_left:
            bottom_left, x = max(
                (y - x + 1, x - i)
                for x, y, i in zip(
                    self.indices,
                    range(self.top, self.top + len(self.indices)),
                    range(len(self.indices))[::-1]
                )
            )
            self.x = x
            if transform:
                for line, length, index in zip(
                    self.lines[:], self.lengths[:], self.indices[:]
                ):
                    self.x -= 1
                    self.y = top_left - index
                    self.PrintLine(
                        {Direction.up},
                        length,
                        "".join(
                            NWSEFlip.get(character, character)
                            for character in line
                        )
                    )
            else:
                for line, length, index in zip(
                    self.lines[::-1], self.lengths[::-1], self.indices[::-1]
                ):
                    self.x -= 1
                    self.y = index + bottom_left
                    self.PrintLine({Direction.down}, length, line)
            self.x = initial_y - bottom_left
            self.y = bottom_left + initial_x
        elif direction == Direction.down_right:
            bottom_right, negative_x = max(
                (x + y + 1, -x + i + 1)
                for x, y, i in zip(
                    self.right_indices,
                    range(self.top, self.top + len(self.right_indices)),
                    range(len(self.right_indices))[::-1]
                )
            )
            self.x = x = -negative_x
            if transform:
                for line, length, index in zip(
                    self.lines[:], self.lengths[:], self.indices[:]
                ):
                    self.x -= 1
                    self.y = top_left - index
                    self.PrintLine(
                        {Direction.up},
                        length,
                        "".join(
                            NESWFlip.get(character, character)
                            for character in line
                        )
                    )
            else:
                for line, length, right_index in zip(
                    self.lines[::-1], self.lengths[::-1],
                    self.right_indices[::-1]
                ):
                    self.x += 1
                    self.y = bottom_right - right_index
                    self.PrintLine({Direction.down}, length, line[::-1])
            self.x = bottom_right - initial_y - 1
            self.y = bottom_right - initial_x - 1
        if Info.step_canvas in self.info:
            self.RefreshFastText((
                "Reflect mirror"
                if transform else
                "Reflect copy"
            ), self.canvas_step)
        elif Info.dump_canvas in self.info:
            print("Reflect mirror" if transform else "Reflect copy")
            print(str(self))

    def ReflectOverlap(
        self,
        direction=Direction.right,
        transform=False,
        overlap=1
    ):
        """
        ReflectOverlap(direction=Direction.right, transform=False, overlap=1)

        Reflect canvas in specified direction, reflecting characters \
whenever possible, and leaving the original intact. The closest \
characters to the axis are on the axis.

        If transform is true, reflect characters in the copy, \
but not if it overwrites the original.

        Leaves out the specified overlap of characters closest to the axis. 

        """
        if not overlap:
            self.ReflectCopy(direction, transform)
            return
        if isinstance(direction, list):
            if not len(direction):
                self.ReflectOverlap(Direction.right, transform, overlap)
            else:
                for direction_ in direction:
                    self.ReflectOverlap(direction_, transform, overlap)
            return
        finished = True
        if direction == Direction.left:
            left = min(self.indices)
            self.x -= (self.x - left) * 2
            self.lines = [
                (
                    "".join(
                        HorizontalFlip.get(character, character)
                        for character in
                        (line[::-1] + "\000" * (index - left))[:-overlap]
                    )
                    if transform else
                    (line[::-1] + "\000" * (index - left))[:-overlap]
                ) +
                "\000" * (index - left) +
                line
                for line, index in zip(self.lines, self.indices)
            ]
            self.background_inside = True
            self.lengths = [
                (length + index - left) * 2 - 1
                for length, index in zip(self.lengths, self.indices)
            ]
            self.indices = [
                left * 2 - right_index + 1
                for right_index in self.right_indices
            ]
        elif direction == Direction.right:
            right = max(self.right_indices)
            self.x += (right - self.x - 1) * 2
            self.lines = [
                line +
                "\000" * (right - right_index) +
                (
                    "".join(
                        HorizontalFlip.get(character, character)
                        for character in
                        ("\000" * (right - right_index) + line[::-1])[overlap:]
                    )
                    if transform else
                    ("\000" * (right - right_index) + line[::-1])[overlap:]
                )
                for line, right_index in zip(self.lines, self.right_indices)
            ]
            self.background_inside = True
            self.lengths = [
                (length + right - right_index) * 2 - 1
                for length, right_index in zip(
                    self.lengths,
                    self.right_indices
                )
            ]
            self.right_indices = [
                right * 2 - index - 1
                for index in self.indices
            ]
        elif direction == Direction.up:
            self.y -= (self.top - self.y) * 2
            self.top -= len(self.lines) - 1
            self.lines = (
                [
                    "".join(
                        VerticalFlip.get(character, character)
                        for character in line
                    ) for line in self.lines[:overlap - 1:-1]
                ]
                if transform else
                self.lines[:overlap - 1:-1]
            ) + self.lines
            self.indices = self.indices[:overlap - 1:-1] + self.indices
            self.lengths = self.lengths[:overlap - 1:-1] + self.lengths
            self.right_indices = (
                self.right_indices[:overlap - 1:-1] +
                self.right_indices
            )
        elif direction == Direction.down:
            self.y += (len(self.lines) - self.y) * 2
            self.lines += (
                [
                    "".join(
                        VerticalFlip.get(character, character)
                        for character in line
                    ) for line in self.lines[-1 - overlap::-1]
                ]
                if transform else
                self.lines[-1 - overlap::-1]
            )
            self.indices += self.indices[-1 - overlap::-1]
            self.lengths += self.lengths[-1 - overlap::-1]
            self.right_indices += self.right_indices[-1 - overlap::-1]
        else:
            finished = False
        if finished:
            if Info.step_canvas in self.info:
                self.RefreshFastText((
                    "Reflect overlap transform"
                    if transform else
                    "Reflect overlap"
                ), self.canvas_step)
            elif Info.dump_canvas in self.info:
                print(
                    "Reflect overlap transform"
                    if transform else
                    "Reflect overlap"
                )
                print(str(self))
            return
        initial_x = self.x
        initial_y = self.y
        self.Trim()
        if direction == Direction.up_left:
            top_left, negative_x = min(
                (x + y, -i - x)
                for x, y, i in zip(
                    self.indices,
                    range(self.top, self.top + len(self.indices)),
                    range(len(self.indices))
                )
            )
            x = -negative_x
            self.x = x + overlap

            for line, length, index in zip(
                self.lines[:], self.lengths[:], self.indices[:]
            ):
                self.x -= 1
                self.y = top_left - index + overlap - 1
                string = (
                    "".join(
                        NWSEFlip.get(character, character)
                        for character in line
                    )
                    if transform else
                    line
                )
                self.PrintLine(
                    {Direction.up},
                    len(string),
                    string,
                    overwrite=False
                )
            self.x = top_left - initial_y + overlap - 1
            self.y = top_left - initial_x + overlap - 1
        elif direction == Direction.up_right:
            top_right, negative_x = min(
                (y - x, i - x + 1)
                for x, y, i in zip(
                    self.right_indices,
                    range(self.top, self.top + len(self.right_indices)),
                    range(len(self.right_indices))
                )
            )
            x = -negative_x
            self.x = x - overlap
            for line, length, right_index in zip(
                self.lines[:], self.lengths[:], self.right_indices[:]
            ):
                self.x += 1
                self.y = top_right + right_index + overlap - 1
                string = (
                    "".join(
                        NESWFlip.get(character, character)
                        for character in line
                    )
                    if transform else
                    line
                )[::-1]
                self.PrintLine(
                    {Direction.up},
                    len(string),
                    string,
                    overwrite=False
                )
            self.x = initial_y - top_right - overlap
            self.y = top_right + initial_x + overlap
        elif direction == Direction.down_left:
            bottom_left, x = max(
                (y - x, x - i)
                for x, y, i in zip(
                    self.indices,
                    range(self.top, self.top + len(self.indices)),
                    range(len(self.indices))[::-1]
                )
            )
            self.x = x + overlap
            for line, length, index in zip(
                self.lines[::-1], self.lengths[::-1], self.indices[::-1]
            ):
                self.x -= 1
                self.y = bottom_left + index - overlap + 1
                string = (
                    "".join(
                        NESWFlip.get(character, character)
                        for character in line
                    )
                    if transform else
                    line
                )
                self.PrintLine(
                    {Direction.down},
                    len(string),
                    string,
                    overwrite=False
                )
            self.x = initial_y - bottom_left - 1 + overlap
            self.y = bottom_left + initial_x + 1 - overlap
        elif direction == Direction.down_right:
            bottom_right, negative_x = max(
                (x + y, -x + i + 1)
                for x, y, i in zip(
                    self.right_indices,
                    range(self.top, self.top + len(self.right_indices)),
                    range(len(self.right_indices))[::-1]
                )
            )
            x = -negative_x
            self.x = x - overlap
            for line, length, right_index in zip(
                self.lines[::-1], self.lengths[::-1], self.right_indices[::-1]
            ):
                self.x += 1
                self.y = bottom_right - right_index - overlap + 1
                string = (
                    "".join(
                        NWSEFlip.get(character, character)
                        for character in line
                    )
                    if transform else
                    line
                )[::-1]
                self.PrintLine(
                    {Direction.down},
                    len(string),
                    string,
                    overwrite=False
                )
            self.x = bottom_right - initial_y - overlap
            self.y = bottom_right - initial_x - overlap
        if Info.step_canvas in self.info:
            self.RefreshFastText((
                "Reflect overlap transform"
                if transform else
                "Reflect overlap"
            ), self.canvas_step)
        elif Info.dump_canvas in self.info:
            print(
                "Reflect overlap transform"
                if transform else
                "Reflect overlap"
            )
            print(str(self))

    def Reflect(self, direction=Direction.right, transform=False):
        """
        Reflect(direction=Direction.right, transform=False)

        Reflect canvas in specified direction.

        If transform is true, reflect characters if possible.

        """
        if isinstance(direction, list):
            if not len(direction):
                self.Reflect(Direction.right, transform)
            else:
                for direction_ in direction:
                    self.Reflect(direction_, transform)
            return
        if direction == Direction.left or direction == Direction.right:
            self.indices, self.right_indices = [
                1 - right_index
                for right_index in self.right_indices
            ], [
                1 - index
                for index in self.indices
            ]
            self.lines = [
                "".join(
                    HorizontalFlip.get(character, character)
                    for character in line[::-1]
                ) for line in self.lines
            ] if transform else [
                line[::-1] for line in self.lines
            ]
            self.x = -self.x
        elif direction == Direction.up or direction == Direction.down:
            if transform:
                for i in range(len(self.lines)):
                    self.lines[i] = "".join(
                        VerticalFlip.get(character, character)
                        for character in self.lines[i]
                    )
            self.lines.reverse()
            self.indices.reverse()
            self.lengths.reverse()
            self.right_indices.reverse()
            self.top = -self.top - len(self.lines) + 1
            self.y = -self.y
        elif (
            direction == Direction.up_left or
            direction == Direction.down_right
        ):
            if transform:
                for i in range(len(self.lines)):
                    self.lines[i] = "".join(
                        NESWFlip.get(character, character)
                        for character in self.lines[i]
                    )
            self.Rotate(2)
            self.Reflect(Direction.right, False)
        elif (
            direction == Direction.up_right or
            direction == Direction.down_left
        ):
            if transform:
                for i in range(len(self.lines)):
                    self.lines[i] = "".join(
                        NWSEFlip.get(character, character)
                        for character in self.lines[i]
                    )
            self.Rotate(6)
            self.Reflect(Direction.right, False)
        if Info.step_canvas in self.info:
            self.RefreshFastText((
                "Reflect transform"
                if transform else
                "Reflect"
            ), self.canvas_step)
        elif Info.dump_canvas in self.info:
            print("Reflect transform" if transform else "Reflect")
            print(str(self))

    def RotateShutter(
        self,
        rotations=2,
        anchor=Direction.down_right,
        number=False,
        overlap=1
    ):
        """
        RotateShutter(direction)

        Rotate canvas 45 degrees the specified number of times, \
rotating characters whenever possible. \
The original is kept, and characters are not overwritten.

        """
        self.RotateOverlap(rotations, anchor, True, number, overlap)

    def RotateTransform(self, rotations=2):
        """
        RotateTransform(rotations=2)

        Rotates canvas 45 degrees the specified number of times.

        If transform is true, rotate characters if possible.

        """
        self.Rotate(rotations, True)

    def RotatePrism(
        self,
        rotations=2,
        anchor=Direction.down_right,
        number=False
    ):
        """
        RotatePrism(rotations=2)

        Rotates canvas 45 degrees the specified number of times, \
with the specified anchor point as the rotation axis.

        If number is true, \
make a copy for each of the digits in rotations.

        Rotate characters if possible.

        """
        self.RotateCopy(rotations, anchor, True, number)

    def RotateCopy(
        self,
        rotations=2,
        anchor=Direction.down_right,
        transform=False,
        number=False
    ):
        """
        RotateCopy(rotations=2, anchor=Direction.down_right, transform=False, \
number=False)

        Rotates canvas 45 degrees the specified number of times, \
with the specified anchor point as the rotation axis.

        If number is true, \
make a copy for each of the digits in rotations.

        If transform is true, rotate characters if possible.

        """
        _lines, lengths, indices = (
            self.lines[::-1], self.lengths[::-1], self.indices[::-1]
        )
        if isinstance(rotations, list):
            for rotation in rotations:
                self.RotateCopy(rotation, anchor, transform, number)
            return
        if rotations % 2:
            print("RuntimeError: Cannot rotate an odd number of times")
            if Info.is_repl not in self.info:
                sys.exit(1)
        rotations = int(rotations)
        if number and rotations > 10:
            new_rotations = set()
            while rotations:
                new_rotations |= {rotations % 10}
                rotations //= 10
                if rotations % 2:
                    print("RuntimeError: Cannot rotate an odd number of times")
                    if Info.is_repl not in self.info:
                        sys.exit(1)
            rotations = new_rotations
        else:
            rotations = {rotations}
        initial_x, initial_y = self.x, self.y
        line_count = len(self.lines)
        if XMovement[anchor] == 1:
            right = max(self.right_indices)
        elif XMovement[anchor] == -1:
            left = min(self.indices)
        else:
            return
        if YMovement[anchor] == 1:
            bottom = self.top + len(self.lines)
        elif YMovement[anchor] == -1:
            top = self.top
        else:
            return
        if 2 in rotations:
            lines = [
                "".join(
                    RotateLeft.get(character, character) for character in line
                )
                for line in _lines
            ] if transform else _lines
            if anchor == Direction.down_right:
                self.x = right
                for line, length, index in zip(lines, lengths, indices):
                    self.x -= 1
                    self.y = bottom + right - index - 1
                    self.PrintLine({Direction.up}, length, line)
            elif anchor == Direction.down_left:
                self.x = left
                for line, length, index in zip(lines, lengths, indices):
                    self.x -= 1
                    self.y = bottom + left - index - 1
                    self.PrintLine({Direction.up}, length, line)
            elif anchor == Direction.up_left:
                self.x = left + line_count
                for line, length, index in zip(lines, lengths, indices):
                    self.x -= 1
                    self.y = top + left - index - 1
                    self.PrintLine({Direction.up}, length, line)
            elif anchor == Direction.up_right:
                self.x = right + line_count
                for line, length, index in zip(lines, lengths, indices):
                    self.x -= 1
                    self.y = top + right - index - 1
                    self.PrintLine({Direction.up}, length, line)
        if 4 in rotations:
            lines = [
                "".join(
                    RotateDown.get(character, character) for character in line
                )
                for line in _lines
            ] if transform else _lines
            if anchor == Direction.down_right:
                self.y = bottom - 1
                for line, length, index in zip(lines, lengths, indices):
                    self.x = right * 2 - index - 1
                    self.y += 1
                    self.PrintLine({Direction.left}, length, line)
            elif anchor == Direction.down_left:
                self.y = bottom - 1
                for line, length, index in zip(lines, lengths, indices):
                    self.x = left - index - 1
                    self.y += 1
                    self.PrintLine({Direction.left}, length, line)
            elif anchor == Direction.up_left:
                self.y = top - line_count - 1
                for line, length, index in zip(lines, lengths, indices):
                    self.x = left - index - 1
                    self.y += 1
                    self.PrintLine({Direction.left}, length, line)
            elif anchor == Direction.up_right:
                self.y = top - line_count - 1
                for line, length, index in zip(lines, lengths, indices):
                    self.x = right * 2 - index - 1
                    self.y += 1
                    self.PrintLine({Direction.left}, length, line)
        if 6 in rotations:
            lines = [
                "".join(
                    RotateRight.get(character, character)
                    for character in line
                )
                for line in _lines
            ] if transform else _lines
            if anchor == Direction.down_right:
                self.x = right - 1
                for line, length, index in zip(lines, lengths, indices):
                    self.x += 1
                    self.y = bottom - right + index
                    self.PrintLine({Direction.down}, length, line)
            elif anchor == Direction.down_left:
                self.x = left - 1
                for line, length, index in zip(lines, lengths, indices):
                    self.x += 1
                    self.y = bottom - left + index
                    self.PrintLine({Direction.down}, length, line)
            elif anchor == Direction.up_left:
                self.x = left - line_count - 1
                for line, length, index in zip(lines, lengths, indices):
                    self.x += 1
                    self.y = top - left + index
                    self.PrintLine({Direction.down}, length, line)
            elif anchor == Direction.up_right:
                self.x = right - line_count - 1
                for line, length, index in zip(lines, lengths, indices):
                    self.x += 1
                    self.y = top - right + index
                    self.PrintLine({Direction.down}, length, line)
        if Info.step_canvas in self.info:
            self.RefreshFastText((
                "Rotate prism"
                if transform else
                "Rotate copy"
            ), self.canvas_step)
        elif Info.dump_canvas in self.info:
            print("Rotate prism" if transform else "Rotate copyu")
            print(str(self))

    def RotateOverlap(
        self,
        rotations=2,
        anchor=Direction.down_right,
        transform=False,
        number=False,
        overlap=1
    ):
        """
        RotateOverlap(rotations=2, anchor=Direction.down_right, \
transform=False, number=False, overlap=1)

        Rotates canvas 45 degrees the specified number of times, \
with the specified anchor point as the rotation axis.

        Overlaps the specified number of characters with the original, \
keeping the original character if there is a conflict.

        If number is true, \
make a copy for each of the digits in rotations.

        If transform is true, rotate characters if possible.

        """
        if not overlap:
            self.RotateCopy(rotations, anchor, transform, number)
            return
        _lines, lengths, indices = (
            self.lines[::-1],
            self.lengths[::-1],
            self.indices[::-1]
        )
        if isinstance(rotations, list):
            for rotation in rotations:
                self.RotateOverlap(
                    rotation, anchor, transform, number, overlap
                )
            return
        if rotations % 2:
            print("RuntimeError: Cannot rotate an odd number of times")
            if Info.is_repl not in self.info:
                sys.exit(1)
        rotations = int(rotations)
        if number and rotations > 10:
            new_rotations = set()
            while rotations:
                new_rotations |= {rotations % 10}
                rotations //= 10
                if rotations % 2:
                    print("RuntimeError: Cannot rotate an odd number of times")
                    if Info.is_repl not in self.info:
                        sys.exit(1)
            rotations = new_rotations
        else:
            rotations = {rotations}
        initial_x, initial_y = self.x, self.y
        line_count = len(self.lines)
        if XMovement[anchor] == 1:
            right = max(self.right_indices)
        elif XMovement[anchor] == -1:
            left = min(self.indices)
        if YMovement[anchor] == 1:
            bottom = self.top + len(self.lines)
        elif YMovement[anchor] == -1:
            top = self.top
        if 2 in rotations:
            lines = [
                "".join(
                    RotateLeft.get(character, character)
                    for character in line
                )
                for line in _lines
            ] if transform else _lines
            if anchor == Direction.down_right:
                self.x = right
                for line, length, index in zip(lines, lengths, indices):
                    self.x -= 1
                    self.y = bottom + right - index - 1 - overlap
                    self.PrintLine(
                        {Direction.up}, length, line, overwrite=False
                    )
            if anchor == Direction.down_left:
                self.x = left + overlap
                for line, length, index in zip(lines, lengths, indices):
                    self.x -= 1
                    self.y = bottom + left - index - 1
                    self.PrintLine(
                        {Direction.up}, length, line, overwrite=False
                    )
            if anchor == Direction.up_left:
                self.x = left + line_count
                for line, length, index in zip(lines, lengths, indices):
                    self.x -= 1
                    self.y = top + left - index - 1 + overlap
                    self.PrintLine(
                        {Direction.up}, length, line, overwrite=False
                    )
            if anchor == Direction.up_right:
                self.x = right + line_count - overlap
                for line, length, index in zip(lines, lengths, indices):
                    self.x -= 1
                    self.y = top + right - index - 1
                    self.PrintLine(
                        {Direction.up}, length, line, overwrite=False
                    )
        if 4 in rotations:
            lines = [
                "".join(
                    RotateDown.get(character, character)
                    for character in line
                )
                for line in _lines
            ] if transform else _lines
            if anchor == Direction.down_right:
                self.y = bottom - 1 - overlap
                for line, length, index in zip(lines, lengths, indices):
                    self.x = right * 2 - index - 1 - overlap
                    self.y += 1
                    self.PrintLine(
                        {Direction.left},
                        length,
                        line,
                        overwrite=False
                    )
            if anchor == Direction.down_left:
                self.y = bottom - 1 - overlap
                for line, length, index in zip(lines, lengths, indices):
                    self.x = left - index - 1 + overlap
                    self.y += 1
                    self.PrintLine(
                        {Direction.left},
                        length,
                        line,
                        overwrite=False
                    )
            if anchor == Direction.up_left:
                self.y = top - line_count - 1 + overlap
                for line, length, index in zip(lines, lengths, indices):
                    self.x = left - index - 1 + overlap
                    self.y += 1
                    self.PrintLine(
                        {Direction.left},
                        length,
                        line,
                        overwrite=False
                    )
            if anchor == Direction.up_right:
                self.y = top - line_count - 1 + overlap
                for line, length, index in zip(lines, lengths, indices):
                    self.x = right * 2 - index - 1 - overlap
                    self.y += 1
                    self.PrintLine(
                        {Direction.left},
                        length,
                        line,
                        overwrite=False
                    )
        if 6 in rotations:
            lines = [
                "".join(
                    RotateRight.get(character, character)
                    for character in line
                )
                for line in _lines
            ] if transform else _lines
            if anchor == Direction.down_right:
                self.x = right - 1 - overlap
                for line, length, index in zip(lines, lengths, indices):
                    self.x += 1
                    self.y = bottom - right + index
                    self.PrintLine(
                        {Direction.down},
                        length,
                        line,
                        overwrite=False
                    )
            if anchor == Direction.down_left:
                self.x = left - 1
                for line, length, index in zip(lines, lengths, indices):
                    self.x += 1
                    self.y = bottom - left + index - overlap
                    self.PrintLine(
                        {Direction.down},
                        length,
                        line,
                        overwrite=False
                    )
            if anchor == Direction.up_left:
                self.x = left - line_count - 1 + overlap
                for line, length, index in zip(lines, lengths, indices):
                    self.x += 1
                    self.y = top - left + index
                    self.PrintLine(
                        {Direction.down},
                        length,
                        line,
                        overwrite=False
                    )
            if anchor == Direction.up_right:
                self.x = right - line_count - 1
                for line, length, index in zip(lines, lengths, indices):
                    self.x += 1
                    self.y = top - right + index + overlap
                    self.PrintLine(
                        {Direction.down},
                        length,
                        line,
                        overwrite=False
                    )
        if Info.step_canvas in self.info:
            self.RefreshFastText((
                "Rotate shutter"
                if transform else
                "Rotate overlap"
            ), self.canvas_step)
        elif Info.dump_canvas in self.info:
            print("Rotate shutter" if transform else "Rotate overlap")
            print(str(self))

    def Rotate(self, rotations=2, transform=False):
        """
        Rotate(rotations=2, transform=False)

        Rotates canvas 45 degrees the specified number of times.

        If transform is true, rotate characters if possible.

        """
        rotations = int(rotations) % 8
        if not rotations:
            return
        left = min(self.indices)
        right = max(self.right_indices)
        if rotations == 2:
            if transform:
                self.lines = [
                    "".join(
                        RotateLeft.get(character, character)
                        for character in line
                    )
                    for line in self.lines
                ]
            lines = self.Lines()
            number_of_lines = len(lines[0])
            self.indices = [self.top] * number_of_lines
            self.lengths = [len(lines)] * number_of_lines
            self.right_indices = (
                [self.top + len(self.lines)] * number_of_lines
            )
            self.lines = [""] * number_of_lines
            for i in range(number_of_lines):
                for j in range(len(lines)):
                    self.lines[i] += lines[j][number_of_lines - i - 1]
            self.top = -right + 1
            self.x, self.y = self.y, -self.x
        elif rotations == 4:
            if transform:
                self.lines = [
                    "".join(
                        RotateDown.get(character, character)
                        for character in line
                    )
                    for line in self.lines
                ]
            self.right_indices, self.indices = (
                [-index + 1 for index in self.indices][::-1],
                [-right_index + 1 for right_index in self.right_indices][::-1]
            )
            self.lengths.reverse()
            self.lines = [line[::-1] for line in self.lines][::-1]
            self.top = -self.top - len(self.lines) + 1
            self.x, self.y = -self.x, -self.y
        elif rotations == 6:
            if transform:
                self.lines = [
                    "".join(
                        RotateRight.get(character, character)
                        for character in line
                    )
                    for line in self.lines
                ]
            x, y = self.x, self.y
            lines = self.Lines()
            number_of_lines = len(lines[0])
            line_length = len(lines)
            self.indices = [-self.top - len(self.lines) + 1] * number_of_lines
            self.lengths = [len(lines)] * number_of_lines
            self.right_indices = [-self.top + 1] * number_of_lines
            self.lines = [""] * number_of_lines
            for i in range(number_of_lines):
                for j in range(line_length):
                    self.lines[i] += lines[line_length - j - 1][i]
            self.top, self.x, self.y = left, -self.y, self.x
        else:
            self.Move({
                1: Direction.up_left,
                5: Direction.down_right,
                3: Direction.down_left,
                7: Direction.up_right
            }[rotations], self.top)
            self.Move({
                1: Direction.down_left,
                3: Direction.down_right,
                5: Direction.up_right,
                7: Direction.up_left
            }[rotations], min(self.indices))
            string = str(self)
            self.Clear()
            self.Print(string, directions={{
                1: Direction.up_right,
                3: Direction.up_left,
                5: Direction.down_left,
                7: Direction.down_right
            }[rotations]})
            transformer = ({
                1: RotateHalfLeft,
                3: RotateThreeHalvesLeft,
                5: RotateThreeHalvesRight,
                7: RotateHalfRight
            })[rotations]
            if transform:
                self.lines = [
                    "".join(
                        transformer.get(character, character)
                        for character in line
                    ) for line in self.lines
                ]
        if Info.step_canvas in self.info:
            self.RefreshFastText((
                "Rotate transform"
                if transform else
                "Rotate"
            ), self.canvas_step)
        elif Info.dump_canvas in self.info:
            print("Rotate transform" if transform else "Rotate")
            print(str(self))

    def Copy(self, delta_x, delta_y):
        """
        Copy(delta_x, delta_y)

        Copies canvas right delta_x cells and down delta_y cells.

        """
        delta_x, delta_y = int(delta_x), int(delta_y)
        initial_x = self.x
        initial_y = self.y
        self.y = self.top + delta_y
        for line, index in zip(self.lines[:], self.indices[:]):
            self.FillLines()
            self.x = index + delta_x
            self.Put(line)
            self.y += 1
        self.x, self.y = initial_x, initial_y
        if Info.step_canvas in self.info:
            self.RefreshFastText("Copy", self.canvas_step)
        elif Info.dump_canvas in self.info:
            print("Copy")
            print(str(self))

    def GetFreeVariable(self):
        """
        GetFreeVariable()

        Gets the next free variable in ικλμνξπρςστυφχψωαβγδεζηθ.

        """
        return next(filter(
            lambda character: character not in self.scope,
            "ικλμνξπρςστυφχψωαβγδεζηθ"
        ))

    def For(self, expression, body):
        """
        For(expression, body)

        Executes body for each element in expression, or range(expression) \
if expression is a number.

        """
        if not expression:
            if len(self.inputs):
                expression = self.inputs[0]
                self.inputs = self.inputs[1:]
            else:
                pass  # TODO
        self.scope = Scope(self.scope)
        loop_variable = self.GetFreeVariable()
        variable = expression(self)
        if isinstance(variable, float):
            variable = int(variable)
        if isinstance(variable, int):
            variable = large_range(variable)
        for item in variable:
            self.scope[loop_variable] = item
            body(self)
        self.scope = self.scope.parent

    def While(self, condition, body):
        """
        While(condition, body)

        Executes body while condition evaluates to truthy.

        """
        self.scope = Scope(self.scope)
        loop_variable = self.GetFreeVariable()
        self.scope[loop_variable] = condition(self)
        while self.scope[loop_variable]:
            body(self)
            self.scope[loop_variable] = condition(self)
        self.scope = self.scope.parent

    def If(self, condition, if_true, if_false):
        """
        If(condition, if_true, if_false)

        Executes if_true if condition evaluates to truthy, \
otherwise executes if false.

        """
        if condition(self):
            if_true(self)
        else:
            if_false(self)

    def Cast(self, variable):
        """
        Cast(variable) -> any

        Returns a variable cast into a string if it was a number, \
or into a number if it was a string.

        Vectorizes.

        """
        if isinstance(variable, list):
            return [self.Cast(item) for item in variable]
        if isinstance(variable, str):
            return float(variable) if "." in variable else int(variable or "0")
        if isinstance(variable, int) or isinstance(variable, float):
            return str(variable)
        if isinstance(variable, String):
            return int(str(variable) or "0")
        if isinstance(variable, Expression):
            variable = variable.run()
            if isinstance(variable, String):
                variable = str(variable)
                return (
                    float(variable)
                    if "." in variable else
                    int(variable or "0")
                )
            if isinstance(variable, List):
                return List(self.Cast(item) for item in variable)
            return str(variable.to_number())

    def ChrOrd(self, variable):
        """
        ChrOrd(variable) -> any

        Returns a variable cast into a string if it was a number, \
or into a number if it was a string.

        Vectorizes.

        """
        if isinstance(variable, list):
            return [self.ChrOrd(item) for item in variable]
        if isinstance(variable, str):
            return ord(variable or "\000")
        if isinstance(variable, int) or isinstance(variable, float):
            return chr(int(variable))
        if isinstance(variable, String):
            return ord(str(variable) or "\000")
        if isinstance(variable, Expression):
            return chr(int(variable.run()))

    def Random(self, variable=1):
        """
        Random(variable=1)

        Returns a random number between 0 and variable \
if variable is a number, else returns a random item in variable.

        """
        if variable == 1 and Info.warn_ambiguities in self.info:
            print("""\
Warning: Possible ambiguity, make sure you explicitly use 1 if needed""")
        if isinstance(variable, float):
            variable = int(variable)
        if isinstance(variable, int):
            return random.randrange(variable)
        elif isinstance(variable, list) or isinstance(variable, str):
            return random.choice(variable)

    def Retrieve(self, key):
        """
        Retrieve(key)
        Get the variable with the given name.

        """
        if key in self.scope:
            return self.scope[key]
        if key in self.hidden:
            return self.hidden[key]
        if key in Charcoal.secret:
            return Charcoal.secret[key]
        return whatever

    def Assign(self, value, key, value2=None):
        """
        Assign(value, key, value2=None)

        If value2 is not None, set value[key] to value2, \
else set the variable with the given name to the given value.

        """
        if value2 is not None:
            value[key] = value2
            if Info.step_canvas in self.info and isinstance(value, Cells):
                self.RefreshFastText("Assign", self.canvas_step)
            elif Info.dump_canvas in self.info:
                print("Assign")
                print(str(self))
            return

        self.scope[key] = value

    def InputString(self, key=None):
        """
        InputString(key="")

        Gets next input as string.

        If key is truthy, set the variable key to the input.

        """
        result = ""
        if len(self.inputs):
            result = self.inputs[0]
            self.inputs = self.inputs[1:]
        elif Info.prompt in self.info:
            result = input("Enter string: ")
        self.original_inputs += [result]
        if len(self.all_inputs) < 5:
            self.all_inputs = self.original_inputs + [""] * (
                5 - len(self.original_inputs)
            )
            self.hidden["θ"] = self.all_inputs[0]
            self.hidden["η"] = self.all_inputs[1]
            self.hidden["ζ"] = self.all_inputs[2]
            self.hidden["ε"] = self.all_inputs[3]
            self.hidden["δ"] = self.all_inputs[4]
        if key:
            self.scope[key] = result
        else:
            return result

    def InputNumber(self, key=""):
        """
        InputNumber(key="")

        Gets next input as number.

        If key is truthy, set the variable key to the input.

        """
        result = 0
        if len(self.inputs):
            try:
                result = (float if "." in self.inputs[0] else int)(
                    self.inputs[0]
                )
            except:
                result = 0
            self.inputs = self.inputs[1:]
        elif Info.prompt in self.info:
            try:
                inp = input("Enter number: ")
                result = (float if "." in inp else int)(inp)
            except:
                result = 0
        self.original_inputs += [result]
        if not all(self.all_inputs):
            self.all_inputs = self.original_inputs + [""] * (
                5 - len(self.original_inputs)
            )
            self.hidden["θ"] = self.all_inputs[0]
            self.hidden["η"] = self.all_inputs[1]
            self.hidden["ζ"] = self.all_inputs[2]
            self.hidden["ε"] = self.all_inputs[3]
            self.hidden["δ"] = self.all_inputs[4]
        if key:
            self.scope[key] = result
        else:
            return result

    def Dump(self):
        """
        Dump()

        Dump contents of canvas with a minimum interval of 10ms.

        """
        sleep(max(0, self.dump_timeout_end - clock()))
        print(self)
        self.dump_timeout_end = clock() + .01

    def DumpNoThrottle(self):
        """
        DumpNoThrottle()

        Dump contents of canvas with no interval.

        """
        print(self)

    def Refresh(self, timeout=0):
        """
        Refresh(timeout=0)

        Refresh the screen with contents of canvas. If timeout is not 0, \
add a timeout of timeout ms before which the screen cannot be refreshed again.

        """
        self.print_at_end = False
        if not isinstance(timeout, int):
            print(
                "RuntimeError: Refresh expected int, found %s" % str(timeout)
            )
            if Info.is_repl not in self.info:
                sys.exit(1)
        elif timeout == 0 and Info.warn_ambiguities in self.info:
            print("""\
Warning: Possible ambiguity, \
make sure you explicitly use 0 for no delay if needed""")
        sleep(max(0, self.timeout_end - clock()))
        print("\033[2J\033[0;0H" + str(self))
        self.timeout_end = clock() + timeout / 1000

    def RefreshFast(self, timeout=0):
        """
        RefreshFast(timeout=0)

        Refresh the screen with contents of canvas. If timeout is not 0, \
add a timeout of timeout ms before which the screen cannot be refreshed again.

        Used in RefreshFor and RefreshWhile.

        """
        sleep(max(0, self.timeout_end - clock()))
        print("\033[2J\033[0;0H" + str(self))
        self.timeout_end = clock() + timeout / 1000

    def RefreshFastText(self, text, timeout=0):
        """
        RefreshFastText(text, timeout=0)

        Refresh the screen with text, a newline, \
and the contents of the canvas. If timeout is not 0, \
add a timeout of timeout ms before which the screen cannot be refreshed again.

        Used for debugging purposes.

        """
        sleep(max(0, self.timeout_end - clock()))
        print("\033[0;0H\033[2J" + text + "\n" + str(self))
        self.timeout_end = clock() + timeout / 1000

    def RefreshFor(self, timeout, variable, body):
        """
        RefreshFor(timeout, variable, body)

        Execute body and refresh the screen with contents of canvas \
for each element in variable, or range(variable) if it is a number. \
Add a timeout of timeout ms before which the screen cannot be refreshed again.

        """
        self.print_at_end = False
        print("\033[2J")
        timeout /= 1000
        self.scope = Scope(self.scope)
        loop_variable = self.GetFreeVariable()
        variable = variable(self)
        if isinstance(variable, int):
            variable = range(variable)
        for item in variable:
            self.timeout_end = clock() + timeout
            self.scope[loop_variable] = item
            body(self)
            self.RefreshFast()
        self.scope = self.scope.parent

    def RefreshWhile(self, timeout, condition, body):
        """
        RefreshFor(timeout, variable, body)

        Execute body and refresh the screen with contents of canvas \
while condition evaluates to truthy. \
Add a timeout of timeout ms before which the screen cannot be refreshed again.

        """
        self.print_at_end = False
        print("\033[2J")
        timeout /= 1000
        self.scope = Scope(self.scope)
        loop_variable = self.GetFreeVariable()
        self.scope[loop_variable] = condition(self)
        while self.scope[loop_variable]:
            self.timeout_end = clock() + timeout
            body(self)
            self.RefreshFast()
            self.scope[loop_variable] = condition(self)
        self.scope = self.scope.parent

    def ToggleTrim(self):
        """
        Trim()

        Turns trim on or off, which will determine \
whether the output wil be right-padded.

        """
        self.trim = not self.trim

    def Evaluate(self, code, is_command=False):
        """
        Evaluate(code, is_command=False)

        Evaluate code as Charcoal code.

        If is_command is false, return the result.

        """
        if is_command:
            Run(code, charcoal=self)
            return
        return Run(code, grammar=CharcoalToken.Expression)

    def EvaluateVariable(self, name, arguments):
        """
        EvaluateVariable(name, arguments)

        Executes the function with the specified name with the specified
arguments.

        Returns the result.

        """
        self.charcoal = self
        if isinstance(name, String):
            name = str(name)
        result = None
        if isinstance(name, Expression):
            result = name.run()(*arguments)
        if name in self.scope:
            result = self.scope[name](*arguments)
        if name in self.hidden:
            result = self.hidden[name](*arguments)
        if name in Charcoal.secret:
            result = Charcoal.secret[name](*arguments)
        self.charcoal = None
        return result

    def ExecuteVariable(self, name, arguments):
        """
        ExecuteVariable(name, arguments)

        Executes the function with the specified name with the specified
arguments.

        """
        self.charcoal = self
        if isinstance(name, String):
            name = str(name)
        if isinstance(name, Expression):
            name.run()(*arguments)
        elif name in self.scope:
            self.scope[name](*arguments)
        elif name in self.hidden:
            self.hidden[name](*arguments)
        elif name in Charcoal.secret:
            Charcoal.secret[name](*arguments)
        self.charcoal = None

    def Lambdafy(self, function):
        """
        Lambdafy(name, function) -> (*arguments -> Any)

        Turns the given Charcoal function into a lambda accepting arguments

        """

        def run(function, arguments, charcoal):
            charcoal.scope = Scope(self.scope)
            for argument, key in zip(arguments, "ικλμνξπρςστυφχψωαβγδεζηθ"):
                charcoal.scope[key] = argument
            function(charcoal)
            return (
                charcoal.last_printed
                if charcoal.last_printed is not None else
                str(charcoal)
            )

        return lambda *arguments: run(
            function, arguments, self.charcoal or Charcoal()
        )

    def CycleChop(self, iterable, length):
        """
        CycleChop(iterable, length)

        Repeat iterable until it is longer than length, \
then take the first length values.

        If iterable is a number, iterable and length will be switched.

        If length is a list or string, length will be set to the length of \
the list or string.

        """
        if isinstance(iterable, int):
            iterable, length = length, iterable
        if isinstance(length, list) or isinstance(length, str):
            length = len(length)
        elif isinstance(length, float):
            length = int(length)
        return (iterable * (length // len(iterable) + 1))[:length]

    def Crop(self, width, height=None):
        """
        Crop(width, height)

        Crop the canvas to width columns and height rows.

        """
        if height is None:
            height = width
        width, height = int(width), int(height)
        top_crop = max(0, self.y - self.top)
        bottom_crop = min(len(self.lines), top_crop + height)
        self.lines = self.lines[top_crop:bottom_crop]
        self.indices = self.indices[top_crop:bottom_crop]
        self.lengths = self.lengths[top_crop:bottom_crop]
        self.right_indices = self.right_indices[top_crop:bottom_crop]
        self.y = 0
        for i in range(len(self.lines)):
            left_crop = max(0, self.x - self.indices[i])
            right_crop = max(
                0,
                min(self.lengths[i], self.x + width - self.indices[i])
            )
            length = self.lengths[i]
            self.lines[i] = self.lines[i][left_crop:right_crop]
            self.indices[i] += left_crop
            self.lengths[i] -= left_crop - right_crop + length
            self.right_indices[i] += right_crop - length
        if Info.step_canvas in self.info:
            self.RefreshFastText("Crop", self.canvas_step)
        elif Info.dump_canvas in self.info:
            print("Crop")
            print(str(self))

    def Extend(self, horizontal=0, vertical=0):
        """
        Extend(horizontal=0, vertical=0)

        Insert horizontal columns between columns, \
and vertical rows between rows.

        """
        horizontal, vertical = int(horizontal) + 1, int(vertical) + 1
        if horizontal:
            self.background_inside = True
            joiner = "\x00" * (horizontal - 1)
            self.lines = [joiner.join(line) for line in self.lines]
            self.lengths = [
                (length - 1) * horizontal + 1 for length in self.lengths
            ]
            self.indices = [index * horizontal for index in self.indices]
            self.right_indices = [
                (right_index - 1) * horizontal + 1
                for right_index in self.right_indices
            ]
        if vertical:
            new_number = (len(self.lines) - 1) * vertical + 1
            lines = [""] * new_number
            indices = [0] * new_number
            right_indices = [0] * new_number
            lines[::vertical] = self.lines
            indices[::vertical] = self.indices
            right_indices[::vertical] = self.right_indices
            self.lines = lines
            self.indices = indices
            self.right_indices = right_indices
        if Info.step_canvas in self.info:
            self.RefreshFastText("Extend", self.canvas_step)
        elif Info.dump_canvas in self.info:
            print("Extend")
            print(str(self))

    def Ternary(self, condition, if_true, if_false):
        """
        Ternary(condition, if_true, if_false)

        Returns if_true if condition evaluates to truthy else if_false.

        """
        return if_true(self) if condition(self) else if_false(self)

    def GetAt(self, x, y):
        """
        GetAt(x, y)

        Returns the character at the specified coordinates on the canvas.

        """
        x, y = int(x), int(y)
        y_index = y - self.top
        if y_index < 0 or y_index >= len(self.lines):
            return ""
        line = self.lines[y_index]
        x_index = x - self.indices[y_index]
        if x_index < 0 or x_index >= self.lengths[y_index]:
            return ""
        return line[x_index]

    def Peek(self):
        """
        Peek()

        Returns the character under the cursor on the canvas.

        """
        return self.GetAt(self.x, self.y)

    def PeekDirection(self, length=1, direction=None):
        """
        PeekDirection(length=1, direction=None)

        Returns the characters in a line \
in the specified direction from the cursor.

        """
        if not direction:
            direction = self.direction
        length = int(length)
        x, y, result, xs, ys = self.x, self.y, [], [], []
        delta_x, delta_y = XMovement[direction], YMovement[direction]
        for i in range(length):
            result += [self.GetAt(x, y)]
            xs += [x]
            ys += [y]
            x += delta_x
            y += delta_y
        return Cells(self, result, xs, ys)

    def PeekAll(self):
        """
        PeekDirection(length=1, direction=None)

        Returns all the characters on the canvas.

        """
        y, result, xs, ys = self.top, [], [], []
        for i in range(len(self.lines)):
            line, x = self.lines[i], self.indices[i]
            for character in line:
                if character == "\x00":
                    x += 1
                    continue
                result += [character]
                xs += [x]
                ys += [y]
                x += 1
            y += 1
        return Cells(self, result, xs, ys)

    def PeekMoore(self, direction=None):
        """
        PeekDirection(length=1, direction=None)

        Returns all the characters in a Moore neighborhood around the canvas.

        """
        if not direction:
            direction = Direction.up_left
        result, xs, ys = [], [], []
        for i in range(8):
            x = self.x + XMovement[direction]
            y = self.y + YMovement[direction]
            result += [self.GetAt(x, y)]
            xs += [x]
            ys += [y]
            direction = NextDirection[direction]
        return Cells(self, result, xs, ys)

    def PeekVonNeumann(self, direction=None):
        """
        PeekDirection(length=1, direction=None)

        Returns all the characters in a Moore neighborhood around the canvas.

        """
        if not direction:
            direction = Direction.up
        result, xs, ys = [], [], []
        for i in range(4):
            x = self.x + XMovement[direction]
            y = self.y + YMovement[direction]
            result += [self.GetAt(x, y)]
            xs += [x]
            ys += [y]
            direction = NewlineDirection[direction]
        return Cells(self, result, xs, ys)

    def Map(self, iterable, function, is_command=False):
        """
        Map(iterable, function, is_command=False)

        Returns an iterable with the results of applying \
function to each element of the iterable.

        If is_command is false, it mutates the original \
iterable, else it returns the iterable.

        """
        self.scope = Scope(self.scope)
        loop_variable = self.GetFreeVariable()
        self.scope[loop_variable] = 1
        index_variable = self.GetFreeVariable()
        result = []
        if callable(iterable):
            iterable, function = function, iterable
        if type(iterable) == Expression:
            iterable = iterable.run()
        if isinstance(iterable, float):
            iterable = int(iterable)
        if isinstance(iterable, int):
            iterable = list(range(iterable))
        for i in range(len(iterable)):
            self.scope[loop_variable] = iterable[i]
            self.scope[index_variable] = i
            result += [function(self)]
        if isinstance(iterable, Cells):
            clone = iterable[:]
            clone[:] = result
        self.scope = self.scope.parent
        if Info.step_canvas in self.info and isinstance(iterable, Cells):
            self.RefreshFastText("Map", self.canvas_step)
        elif Info.dump_canvas in self.info:
            print("Map")
            print(str(self))
        return result

    def All(self, iterable, function):
        """
        All(iterable, function)

        Returns whether the function returns truthy for all values in the \
iterable.

        """
        if callable(iterable):
            iterable, function = function, iterable
        if type(iterable) == Expression:
            iterable = iterable.run()
        return all(function(item) for item in iterable)

    def Any(self, iterable, function):
        """
        Any(iterable, function)

        Returns whether the function returns truthy for any values in the \
iterable.

        """
        if callable(iterable):
            iterable, function = function, iterable
        if type(iterable) == Expression:
            iterable = iterable.run()
        return any(function(item) for item in iterable)

    def Add(self, left, right):
        if isinstance(left, String):
            left = str(left)
        if isinstance(right, String):
            right = str(right)
        if type(left) == Expression:
            left = left.run()
        if type(right) == Expression:
            right = right.run()
        left_type = type(left)
        right_type = type(right)
        left_is_iterable = (
            hasattr(left, "__iter__") and not isinstance(left, str)
        )
        right_is_iterable = (
            hasattr(right, "__iter__") and not isinstance(right, str)
        )
        if isinstance(left, Pattern) or isinstance(right, Pattern):
            return left + right
        if left_is_iterable ^ right_is_iterable:
            if left_is_iterable:
                return left + [right]
            return [left] + right
        if (left_type == str) ^ (right_type == str):
            if left_type == str:
                return left + str(right)
            return str(left) + right
        return left + right

    def Subtract(self, left, right):
        if isinstance(left, String):
            left = str(left)
        if isinstance(right, String):
            right = str(right)
        if type(left) == Expression:
            left = left.run()
        if type(right) == Expression:
            right = right.run()
        left_type = type(left)
        right_type = type(right)
        left_is_iterable = (
            hasattr(left, "__iter__") and not isinstance(left, str)
        )
        right_is_iterable = (
            hasattr(right, "__iter__") and not isinstance(right, str)
        )
        if left_is_iterable ^ right_is_iterable:
            if left_is_iterable:
                return [item for item in left if item != right]
            # return [left] - right
        if (left_type == str) ^ (right_type == str):
            if left_type == str:
                if right_type == int or right_type == float:
                    return (float if "." in left else int)(left) - right
                return left - str(right)
            if left_type == int or left_type == float:
                return left - (float if "." in right else int)(right)
            return str(left) - right
        if left_type == str and right_type == str:
            return left.replace(right, "")
        return left - right

    def Multiply(self, left, right):
        if isinstance(left, String):
            left = str(left)
        if isinstance(right, String):
            right = str(right)
        if type(left) == Expression:
            left = left.run()
        if type(right) == Expression:
            right = right.run()
        left_type = type(left)
        right_type = type(right)
        left_is_iterable = hasattr(left, "__iter__")
        right_is_iterable = hasattr(right, "__iter__")
        if left_is_iterable ^ right_is_iterable:
            if left_is_iterable:
                return (left * (1 + int(right)))[:int(len(left) * right)]
            return (right * (1 + int(left)))[:int(len(right) * left)]
        if left_is_iterable and right_is_iterable:
            if left_type == str:
                return left.join(right)
            if right_type == str:
                return right.join(left)
        return left * right

    def Divide(self, left, right, floor=True):
        def reduce(lst, function):
            result = lst[0]
            for item in lst[1:]:
                result = function(result, item)
            return result
        if isinstance(left, String):
            left = str(left)
        if isinstance(right, String):
            right = str(right)
        if type(left) == Expression:
            left = left.run()
        if type(right) == Expression:
            right = right.run()
        left_type = type(left)
        right_type = type(right)
        left_is_iterable = hasattr(left, "__iter__")
        right_is_iterable = hasattr(right, "__iter__")
        if left_is_iterable ^ right_is_iterable:
            if left_is_iterable:
                if callable(right):
                    return reduce(left, right)
                return (left * (1 + int(1 / right)))[:int(len(left) / right)]
            if callable(left):
                return reduce(right, left)
            return (right * (1 + int(1 / left)))[:int(len(right) / left)]
        if left_type == str and right_type == str:
            return left.split(right)
        return left // right if floor else left / right


def PassThrough(result):
    """
    PassThrough(result) -> Any

    Returns its argument.

    """
    return result

SuperscriptToNormal = {
    "⁰": 0, "¹": 1, "²": 2, "³": 3, "⁴": 4,
    "⁵": 5, "⁶": 6, "⁷": 7, "⁸": 8, "⁹": 9
}


def ParseExpression(
    code,
    index=0,
    grammar=CharcoalToken.Program,
    grammars=UnicodeGrammars,
    processor=ASTProcessor,
    verbose=False
):
    """
    ParseExpression(code, index=0, grammar=CharcoalToken.Program, \
grammars=UnicodeGrammars, processor=ASTProcessor, verbose=False) -> Any

    Parse the given code starting from the given index, \
starting from the token given as grammar.

    The grammars are taken from grammars.

    The processor turns the tokens into the return value.

    If verbose is true, parses using VerboseGrammars and verbose literals.

    Returns the processed expression.

    """
    original_index, lexeme_index, parse_index, parse_trace = index, 0, 0, []
    for lexeme in grammars[grammar]:
        success, index, tokens = True, original_index, []
        for token in lexeme:
            if verbose:
                while index < len(code) and code[index] in "\r\n\t ":
                    index += 1
                next_chars = code[index:index + 2]
                while next_chars == "//" or next_chars == "/*":
                    index += 2
                    if next_chars == "//":
                        while index < len(code) and code[index] not in "\r\n":
                            index += 1
                        if code[index - 1:index + 1] == "\r\n":
                            # It's a MS newline
                            index += 1
                    else:
                        depth = 1
                        while depth:
                            next_chars = code[index:index + 2]
                            while next_chars != "*/":
                                if next_chars == "/*":
                                    depth += 1
                                index += 1
                                next_chars = code[index:index + 2]
                            depth -= 1
                        index += 2
                    while index < len(code) and code[index] in "\r\n\t ":
                        index += 1
                    next_chars = code[index:index + 2]
            if isinstance(token, int):
                if verbose:
                    if token == CharcoalToken.String:
                        if index == len(code):
                            success = False
                            break
                        quote = code[index]
                        if quote != '"' and quote != "'":
                            success = False
                            break
                        old_index = index
                        index += 1
                        character = code[index]
                        if quote == '"':
                            while character != '"':
                                index += 1
                                if character == "\\":
                                    index += 1
                                if index >= len(code):
                                    break
                                character = code[index]
                        else:
                            while character != "'":
                                index += 1
                                if character == "\\":
                                    index += 1
                                if index >= len(code):
                                    break
                                character = code[index]
                        index += 1
                        if index - old_index < 2:
                            success = False
                            break
                        tokens += processor[token][0]([literal_eval(
                            code[old_index:index]
                        )])
                    elif token == CharcoalToken.Number:
                        if index == len(code):
                            success = False
                            break
                        old_index, character, result = index, code[index], 0
                        integer = True
                        while (
                            (character >= "0" and character <= "9") or
                            character == "."
                        ):
                            if character == ".":
                                if not integer:
                                    break
                                integer = False
                            index += 1
                            if index == len(code):
                                character = ""
                            else:
                                character = code[index]
                        if old_index == index:
                            success = False
                            break
                        tokens += processor[token][0]([
                            (int if integer else float)(code[old_index:index])
                        ])
                    elif token == CharcoalToken.Name:
                        if index == len(code):
                            success = False
                            break
                        character = code[index]
                        if (
                            character in "abgdezhqiklmnxprsvtufcyw" and not
                            code[index + 1] in "abcdefghijklmnopqrstuvwxyz"
                        ):
                            tokens += processor[token][0]([character])
                            index += 1
                        else:
                            success = False
                            break
                    else:
                        result = ParseExpression(
                            code, index, token, grammars, processor, verbose
                        )
                        if not result:
                            success = False
                            break
                        tokens += [result[0]]
                        index = result[1]
                        if index is False:
                            parse_trace = result[0]
                            parse_index = result[2]
                            success = False
                            break
                else:
                    if token == CharcoalToken.String:
                        if index == len(code):
                            success = False
                            break
                        old_index, character = index, code[index]
                        while character not in UnicodeCommands:
                            index += 1
                            if character == "´":
                                index += 1
                            if index >= len(code):
                                break
                            character = code[index]
                        if old_index == index:
                            if character == "“" or character == "”":
                                index += 1
                                character = code[index]
                                while character != "”":
                                    index += 1
                                    if index >= len(code):
                                        break
                                    character = code[index]
                                if index < len(code):
                                    index += 1
                                tokens += processor[token][0]([
                                    Decompressed(code[old_index:index])
                                ])
                            else:
                                success = False
                                break
                        tokens += processor[token][0]([re.sub(
                            r"´(.)", r"\1",
                            re.sub(
                                r"(^|[^´])¶", r"\1\n",
                                re.sub(
                                    r"(^|[^´])¶", r"\1\n",
                                    re.sub(
                                        r"(^|[^´])⸿", r"\1\r",
                                        re.sub(
                                            r"(^|[^´])⸿", r"\1\r",
                                            code[old_index:index]
                                        )
                                    )
                                )
                            )
                        )])
                    elif token == CharcoalToken.Number:
                        if index == len(code):
                            success = False
                            break
                        old_index, character, result = index, code[index], 0
                        while (
                            character >= "⁴" and character <= "⁹" or
                            character in ["⁰", "¹", "²", "³"]
                        ):
                            result = result * 10 + SuperscriptToNormal[
                                character
                            ]
                            index += 1
                            if index == len(code):
                                character = ""
                            else:
                                character = code[index]
                        if character == "·":
                            multiplier = .1
                            index += 1
                            if index == len(code):
                                character = ""
                            else:
                                character = code[index]
                            while (
                                character >= "⁴" and character <= "⁹" or
                                character in ["⁰", "¹", "²", "³"]
                            ):
                                result = result + SuperscriptToNormal[
                                    character
                                ] * multiplier
                                index += 1
                                multiplier *= .1
                                if index == len(code):
                                    character = ""
                                else:
                                    character = code[index]
                        if old_index == index:
                            success = False
                            break
                        tokens += processor[token][0]([result])
                    elif token == CharcoalToken.Name:
                        if index == len(code):
                            success = False
                            break
                        character = code[index]
                        if (
                            character >= "α" and character <= "ω" and
                            character != "ο"
                        ):
                            tokens += processor[token][0]([character])
                            index += 1
                        else:
                            success = False
                            break
                    else:
                        result = ParseExpression(
                            code, index, token, grammars, processor, verbose
                        )
                        if not result:
                            success = False
                            break
                        tokens += [result[0]]
                        index = result[1]
                        if index is False:
                            parse_trace, parse_index = result[0], result[2]
                            success = False
                            break
            elif isinstance(token, str):
                old_index = index
                index += len(token)
                if code[old_index:index] == token:
                    tokens += [token]
                else:
                    success = False
                    break
            else:
                print(
                    "ParseError: Unexpected token %s found in grammar." %
                    repr(token)
                )
        if parse_trace and not parse_index and not original_index:
            break
        if success:
            return (processor[grammar][lexeme_index](tokens), index)
        lexeme_index += 1
    return ((
        parse_trace
        if not parse_index or parse_index == original_index else
        (
            ["%s: %s" % (
                CharcoalTokenNames[grammar],
                repr(code[original_index:parse_index])
            )] +
            parse_trace
        )
    ), False, original_index)


def Decode(code):
    """
    Decode(code)

    Returns code converted from Charcoal's codepage to Unicode.

    """
    result = ""
    i = 0
    while i < len(code):
        character = code[i]
        ordinal = ord(character)
        if ordinal == 0xFF:
            i += 1
            ordinal = ord(code[i])
            if ordinal & 0b11000000 == 0b10000000:  # 2 bytes
                result += chr(
                    ((ordinal & 63) << 8) + ord(code[i + 1]) + 128
                )
                i += 2
            elif ordinal & 0b11100000 == 0b11000000:  # 3 bytes
                result += chr(
                    ((ordinal & 31) << 16) +
                    (ord(code[i + 1]) << 8) +
                    ord(code[i + 2]) +
                    16512
                )
                i += 3
            elif ordinal & 0b11110000 == 0b11100000:  # 4 bytes
                result += chr(
                    ((ordinal & 15) << 24) +
                    (ord(code[i + 1]) << 16) +
                    (ord(code[i + 2]) << 8) +
                    ord(code[i + 3]) +
                    2113664
                )
                i += 4
        else:
            result += UnicodeLookup.get(character, character)
            i += 1
    return result


def Parse(
    code,
    grammar=CharcoalToken.Program,
    grammars=UnicodeGrammars,
    processor=ASTProcessor,
    whitespace=False,
    normal_encoding=False,
    verbose=False,
    grave=False,
    silent=False
):
    """
    Parse(code, grammar=CharcoalToken.Program, \
grammars=UnicodeGrammars, processor=ASTProcessor, whitespace=False, \
normal_encoding=False, verbose=False, grave=False) -> Any

    Parse the given Charcoal code, starting from the token given as grammar.

    The grammars are taken from grammars.

    The processor turns the tokens into the return value.

    If whitespace is true, removes all whitespace that is not preceded by ´.

    If normal_encoding is true, runs using Charcoal's codepage.

    If verbose is true, parses using VerboseGrammars and verbose literals.

    If grave is true, converts all characters preceded by ´ or ´´ with the \
symbols they represent.

    Returns the processed program.

    """
    if normal_encoding:
        code = Decode(code)
    if whitespace:
        code = re.sub(
            r"(´\s)?\s*",
            lambda match: match.group(1)[1] if match.group(1) else "",
            code
        )
    if verbose:
        parsed = ParseExpression(
            code, 0, grammar, VerboseGrammars, StringifierProcessor, True
        )
        if parsed[1] is False and not silent:
            PrintParseTrace(parsed[0])
            return processor[CharcoalToken.Program][-1]([])
        if parsed:
            code = parsed[0]
        else:
            print("RuntimeError: Could not parse")
            sys.exit(1)
    elif grave:
        code = Degrave(code)
    for python_function in re.findall("ＵＰ[ -~]+", code):
        AddPythonFunction(python_function)
    code += "»" * code.count("«")
    result = ParseExpression(code, 0, grammar, grammars, processor)
    if not result:
        return result
    if result[1] is False and not silent:
        PrintParseTrace(result[0])
    return (
        processor[CharcoalToken.Program][-1]([])
        if result[1] is False else
        result[0]
    )


def PrintParseTrace(trace):
    if not isinstance(trace, list):
        print("Parsing failed")
    else:
        print("""\
Parsing failed, parse trace:
%s""" % ("\n".join(trace)))


def PrintTree(tree, padding=""):
    """
    PrintTree(tree, padding="")

    Print tree with the given padding on the left.

    Trees are of the form [name, children] where children is a list and \
name is not.

    """
    padding = re.sub(r"└$", r" ", re.sub(r"├$", r"│", padding))
    new_padding = padding + "├"
    if len(tree) > 1:
        for item in tree[1:-1]:
            if isinstance(item, list):
                print(new_padding + item[0])
                PrintTree(item, new_padding)
            else:
                if isinstance(item, str):
                    print(new_padding + repr(item)[1:-1])
                else:
                    print(new_padding + str(item))
        new_padding = padding + "└"
        item = tree[-1]
        if isinstance(item, list):
            print(new_padding + item[0])
            PrintTree(item, new_padding)
        else:
            if isinstance(item, str):
                print(new_padding + repr(item)[1:-1])
            else:
                print(new_padding + str(item))


def ProcessInput(inputs):
    """
    ProcessInput(inputs) -> list

    Tries to split given input.

    Returns processed input.

    """
    new_inputs = inputs
    try:
        new_inputs = list(map(str, literal_eval(inputs)))
        if not isinstance(new_inputs, list):
            raise Exception()
    except:
        new_inputs = (
            inputs.split("\n") if "\n" in inputs else inputs.split(" ")
        )
    return new_inputs if len(new_inputs) > 1 or new_inputs[0] else []


def Run(
    code,
    inputs="",
    charcoal=None,
    grammar=CharcoalToken.Program,
    grammars=UnicodeGrammars,
    whitespace=False,
    normal_encoding=False,
    verbose=False,
    grave=False,
    silent=False
):
    """
    Run(code, inputs="", charcoal=None, grammar=CharcoalToken.Program, \
grammars=UnicodeGrammars, whitespace=False, normal_encoding=False, \
verbose=False, grave=False) -> Any

    Runs given Charcoal code with given inputs as a string.

    If charcoal is falsy, a new Charcoal object is used instead of charcoal.

    Starts parsing from the given grammar, using the given list of grammars.

    If whitespace is true, removes all whitespace that is not preceded by ´.

    If normal_encoding is true, runs using Charcoal's codepage.

    If verbose is true, parses using VerboseGrammars and verbose literals.

    If grave is true, converts all characters preceded by ´ or ´´ with the \
symbols they represent.

    Returns the state of the canvas as a string if grammar is Program, \
else the result of parsing.

    """
    inputs = ProcessInput(inputs)
    if not charcoal:
        charcoal = Charcoal(inputs)
    else:
        charcoal.AddInputs(inputs)
    result = Parse(
        code, grammar, grammars, InterpreterProcessor, whitespace,
        normal_encoding, verbose, grave, silent
    )(charcoal)
    if grammar == CharcoalToken.Program:
        return str(charcoal)
    return result


def GetProgram(
    code,
    inputs="",
    charcoal=None,
    grammar=CharcoalToken.Program,
    grammars=UnicodeGrammars,
    whitespace=False,
    normal_encoding=False,
    verbose=False,
    grave=False
):
    """
    GetProgram(code, inputs="", charcoal=None, grammar=CharcoalToken.Program, \
grammars=UnicodeGrammars, whitespace=False, normal_encoding=False, \
verbose=False, grave=False) -> Any

    Runs given Charcoal code with given inputs as a string.

    If charcoal is falsy, a new Charcoal object is used instead if charcoal.

    Starts parsing from the given grammar, using the given list of grammars.

    If whitespace is true, removes all whitespace that is not preceded by ´.

    If normal_encoding is true, runs using Charcoal's codepage.

    If verbose is true, parses using VerboseGrammars and verbose literals.

    If grave is true, converts all characters preceded by ´ or ´´ with the \
symbols they represent.

    Returns the Charcoal program as a function.

    """
    return Parse(
        code, grammar, grammars, InterpreterProcessor, whitespace,
        normal_encoding, verbose, grave
    )


def Degrave(code):
    return re.sub("``([\s\S])|`([\s\S])", lambda match: (
        {
            "`": "`", " ": "´", "4": "←", "8": "↑", "6": "→", "2": "↓",
            "7": "↖", "9": "↗", "3": "↘", "1": "↙", "#": "№", "<": "↶",
            ">": "↷", "r": "⟲", "j": "⪫", "s": "⪪", "c": "℅", "o": "℅",
            "f": "⌕", "v": "⮌", "[": "◧", "]": "◨", "=": "≡", "t": "⎇",
            "?": "‽", "&": "∧", "|": "∨", "d": "↧", "u": "↥", "_": "±",
            "+": "⊞", "-": "⊟", "\\": "“", "/": "”", "n": "⌊", "x": "⌈"
        }[match.group(1)]
        if match.group(1) else
        UnicodeLookup[chr(ord(match.group(2)) + 128)]
        if match.group(2) != "\n" else "¶"
    ), code)


def Golf(code):
    codes = re.split("([“”])([^”]*?)(”)", code)
    success = True
    while success:
        success = False
        for i in range(0, len(codes), 4):
            for regex, replacement in (
                ("([^·⁰¹²³⁴-⁹]|^)¹⁰⁰⁰([^·⁰¹²³⁴-⁹]|$)", "\\1φ\\2"),
                ("([^·⁰¹²³⁴-⁹]|^)¹⁰([^·⁰¹²³⁴-⁹]|$)", "\\1χ\\2"),
                ("(^|[^´].|[^ -~´⸿¶�]) !\"#\$%&'\(\)\*\+,-\./0123456789:;<=>\?@\
        ABCDEFGHIJKLMNOPQRSTUVWXYZ\[\\\]\^_`\
        abcdefghijklmnopqrstuvwxyz{\|}~([^´]|$)", "\\1γ\\2"),
                (
                    "([^´].|[^ -~´⸿¶�]|^)abcdefghijklmnopqrstuvwxyz([^´]|$)",
                    "\\1β\\2"
                ),
                (
                    "([^´].|[^ -~´⸿¶�]|^)ABCDEFGHIJKLMNOPQRSTUVWXYZ([^´]|$)",
                    "\\1α\\2"
                ),
                ("([^·⁰¹²³⁴-⁹ -~´⸿¶�])¦([^·⁰¹²³⁴-⁹ -~´⸿¶�])", "\\1\\2"),
                ("([^·⁰¹²³⁴-⁹])¦([·⁰¹²³⁴-⁹])", "\\1\\2"),
                ("([·⁰¹²³⁴-⁹])¦([^·⁰¹²³⁴-⁹])", "\\1\\2"),
                ("([^´].|[^ -~´⸿¶�])¦([ -~´⸿¶�])", "\\1\\2"),
                ("([ -~´⸿¶�])¦([^ -~´⸿¶�])", "\\1\\2"),
                ("(^|[^ -~])´([ -~])", "\\1\\2"),
                ("((?:^|[^´])[α-ξπ-ω])¦", "\\1"),
                ("¦((?:^|[^´])[α-ξπ-ω])", "\\1"),
                (
                    "(^|[^‖])Ｍ([←-↓↖-↙])(?!%s|[·⁰¹²³⁴-⁹ -~´⸿¶�])" % sOperator,
                    "\\1\\2"
                ),
                ("(%s)¦(%s)" % (sOperator, sOperator), "\\1\\2"),
                ("»+$", "")
            ):
                old = codes[i]
                codes[i] = re.sub(regex, replacement, codes[i])
                if codes[i] != old:
                    success = True
    code = "".join(codes)
    for match, replacement in (
        (Compressed(" !\"#$%&'()*+,-./0123456789:;<=>?@\
ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"), "γ"),
        (Compressed("abcdefghijklmnopqrstuvwxyz"), "β"),
        (Compressed("ABCDEFGHIJKLMNOPQRSTUVWXYZ"), "α")
    ):
        code = code.replace(match, replacement)
    return code


def AddAmbiguityWarnings():
    """
    AddAmbiguityWarnings()

    Adds ambiguity warnings which are shown whenever the AST is printed.

    """
    ASTProcessor[CharcoalToken.Monadic][4] = (
        lambda result: "Random [Warning: May be ambiguous]"
    )
    ASTProcessor[CharcoalToken.Command][59] = lambda result: [
        "Refresh [Warning: May be ambiguous]", result[1]
    ]
    ASTProcessor[CharcoalToken.Command][60] = lambda result: [
        "Refresh [Warning: May be ambiguous]"
    ]


def RemoveThrottle():
    """
    RemoveThrottle()

    Removes throttle for Dump.

    """
    InterpreterProcessor[-5] = (
        lambda result: lambda charcoal: charcoal.DumpNoThrottle()
    )


def AddPythonFunction(name):
    """
    AddPythonFunction(name)

    Adds the Python function with the given name to all grammars \
and processors.

    """
    if name in python_function_is_command:
        return
    function, name, _name = None, name[2:], name[2:]
    if "." in name:
        try:
            module, *parts = name.split(".")
            if module not in imports:
                imports[module] = __import__(module)
            function = imports[module]
            for part in parts:
                function = getattr(function, part)
        except:
            pass
    if not function:
        loc, glob = locals(), globals()
        if "." not in name:
            if name in loc:
                function = loc[name]
            elif name in glob:
                function = glob[name]
            elif hasattr(builtins, name):
                function = getattr(builtins, name)
        else:
            variable, *parts = name.split(".")
            if variable in loc:
                function = loc[variable]
            elif variable in glob:
                function = glob[variable]
            elif hasattr(builtins, variable):
                function = getattr(builtins, variable)
            for part in parts:
                function = function[part]
    is_operator = re.search(
        "\
(?i)return|disassemble|find|compute|build|make|convert|create|read|\*\*|->",
        function.__doc__
    )
    python_function_is_command[name] = not is_operator
    if is_operator:
        UnicodeGrammars[CharcoalToken.OtherOperator] += [
            ["ＵＰ" + _name, CharcoalToken.Separator, CharcoalToken.List],
            [
                "ＵＰ" + _name, CharcoalToken.Separator,
                CharcoalToken.Expression
            ],
            ["ＵＰ" + _name, CharcoalToken.Separator]
        ]
        VerboseGrammars[CharcoalToken.OtherOperator] += [
            [
                "PythonFunction", "(", _name, CharcoalToken.Separator,
                CharcoalToken.WolframList, ")"
            ],
            [
                "PythonFunction", "(", _name, CharcoalToken.Separator,
                CharcoalToken.WolframExpression, ")"
            ],
            ["PythonFunction", "(", _name, CharcoalToken.Separator, ")"]
        ]
        ASTProcessor[CharcoalToken.OtherOperator] += [
            lambda result: ["Python function: \"%s\"" % name, result[2]],
            lambda result: ["Python function: \"%s\"" % name, result[2]],
            lambda result: ["Python function: \"%s\"" % name]
        ]
        StringifierProcessor[CharcoalToken.OtherOperator] += [
            lambda result: "ＵＰ" + "".join(result[2:-1]),
            lambda result: "ＵＰ" + "".join(result[2:-1]),
            lambda result: "ＵＰ" + "".join(result[2:-1])
        ]
        InterpreterProcessor[CharcoalToken.OtherOperator] += [
            lambda result: lambda charcoal: function(*result[2](charcoal)),
            lambda result: lambda charcoal: function(result[2](charcoal)),
            lambda result: lambda charcoal: function()
        ]
    else:
        UnicodeGrammars[CharcoalToken.Command] += [
            ["ＵＰ" + _name, CharcoalToken.Separator, CharcoalToken.List],
            [
                "ＵＰ" + _name, CharcoalToken.Separator,
                CharcoalToken.Expression
            ],
            ["ＵＰ" + _name, CharcoalToken.Separator]
        ]
        VerboseGrammars[CharcoalToken.Command] += [
            [
                "PythonFunction", "(", _name, CharcoalToken.Separator,
                CharcoalToken.WolframList, ")"
            ],
            [
                "PythonFunction", "(", _name, CharcoalToken.Separator,
                CharcoalToken.WolframExpression, ")"
            ],
            ["PythonFunction", "(", _name, CharcoalToken.Separator, ")"]
        ]
        ASTProcessor[CharcoalToken.Command] += [
            lambda result: ["Python function: \"%s\"" % name, result[2]],
            lambda result: ["Python function: \"%s\"" % name, result[2]],
            lambda result: ["Python function: \"%s\"" % name]
        ]
        StringifierProcessor[CharcoalToken.Command] += [
            lambda result: "ＵＰ" + "".join(result[2:-1]),
            lambda result: "ＵＰ" + "".join(result[2:-1]),
            lambda result: "ＵＰ" + "".join(result[2:-1])
        ]
        InterpreterProcessor[CharcoalToken.Command] += [
            lambda result: lambda charcoal: function(*result[2](charcoal)),
            lambda result: lambda charcoal: function(result[2](charcoal)),
            lambda result: lambda charcoal: function()
        ]

# from https://gist.github.com/puentesarrin/6567480


def print_xxd(data):
    """
    print_xxd(data)

    Prints the xxd-style hexdump using Charcoal's codepage, \
given data in UTF-8.

    """
    array = []
    for original in data:
        character = ReverseLookup.get(original, original)
        ordinal = ord(character)
        if InCodepage(original) or ordinal < 256:
            array.append(ordinal)
        elif ordinal < 16512:
            code = ordinal - 128
            array.append(0xFF)
            array.append(0b10000000 | (code >> 8))
            array.append(code & 0xFF)
        elif ordinal < 2113664:
            code = ordinal - 16512
            array.append(0xFF)
            array.append(0b11000000 | (code >> 16))
            array.append((code >> 8) & 0xFF)
            array.append(code & 0xFF)
        else:
            code = ordinal - 2113664
            array.append(0xFF)
            array.append(0b11100000 | (code >> 24))
            array.append((code >> 16) & 0xFF)
            array.append((code >> 8) & 0xFF)
            array.append(code & 0xFF)
    data, counter = array, 0
    buf = [1]
    while buf:
        buf = data[counter << 4:(counter + 1) << 4]
        if not buf:
            break
        buf2 = ["%02x" % i for i in buf]
        print("{0}: {1:<39}  {2}".format(
            ("%07x" % (counter << 4)),
            " ".join(["".join(buf2[i:i + 2]) for i in range(0, len(buf2), 2)]),
            "".join([chr(c) if c >= 32 and c <= 126 else "." for c in buf])
        ))
        counter += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Interpret the Charcoal language."
    )
    parser.add_argument(
        "file", metavar="FILE", type=str, nargs="?", default="",
        help="File path of the program."
    )
    parser.add_argument(
        "-c", "--code", type=str, nargs="?", default="",
        help="Code."
    )
    parser.add_argument(
        "-i", "--input", type=str, nargs="*", default=[],
        help="Input."
    )
    parser.add_argument(
        "-o", "--output", type=str, nargs="*", default=[],
        help="Expected output."
    )
    parser.add_argument(
        "-rif", "--rawinputfile", type=str, nargs="?", default="",
        help="Path to raw input file."
    )
    parser.add_argument(
        "-if", "--inputfile", type=str, nargs="?", default="",
        help="Path to input file."
    )
    parser.add_argument(
        "-of", "--outputfile", type=str, nargs="?", default="",
        help="Path to file with expected output."
    )
    parser.add_argument(
        "-qt", "--quiettesting", action="store_true",
        help="Don't print output for each individual testcase."
    )
    parser.add_argument(
        "-cs", "--canvasstep", type=int, nargs="?", default=500,
        help="Change canvas step interval."
    )
    parser.add_argument(
        "-de", "--decode", action="store_true",
        help="Turn encoded code into unicode code."
    )
    parser.add_argument(
        "-e", "--normalencoding", action="store_true",
        help="Use custom codepage."
    )
    parser.add_argument(
        "-a", "--astify", action="store_true", help="Print AST."
    )
    parser.add_argument(
        "-oa", "--onlyastify", action="store_true", help="Print AST and exit."
    )
    parser.add_argument(
        "-p", "--prompt", action="store_true", help="Prompt for input."
    )
    parser.add_argument(
        "-r", "--repl", action="store_true",
        help="Open as REPL instead of interpreting."
    )
    parser.add_argument(
        "-rs", "--restricted", action="store_true",
        help="""Disable prompt input, REPL mode, \
non-raw file input and file output."""
    )
    parser.add_argument(
        "-w", "--whitespace", action="store_true",
        help="Ignore all whitespace unless prefixed by a ´."
    )
    parser.add_argument(
        "-Wam", "--Wambiguities", action="store_true",
        help="Warn the user of any ambiguities."
    )
    parser.add_argument(
        "-s", "--stepcanvas", action="store_true",
        help="Pause canvas every time it is changed."
    )
    parser.add_argument(
        "-d", "--dumpcanvas", action="store_true",
        help="Dump canvas every time it is changed."
    )
    parser.add_argument(
        "-nt", "--nothrottle", action="store_true",
        help="Don't throttle Dump."
    )
    parser.add_argument(
        "-dv", "--deverbosify", action="store_true",
        help="Turn verbose code into normal code."
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Use verbose mode."
    )
    parser.add_argument(
        "-dg", "--degrave", action="store_true",
        help="Turn grave mode code into normal code."
    )
    parser.add_argument(
        "-g", "--grave", action="store_true", help="Use grave mode."
    )
    parser.add_argument(
        "-sl", "--showlength", action="store_true",
        help="Show the length of the code."
    )
    parser.add_argument(
        "-t", "--test", action="store_true", help="Run unit tests."
    )
    parser.add_argument(
        "-dc", "--disablecompression", action="store_true",
        help="Disable compression when deverbosifying."
    )
    parser.add_argument(
        "-hd", "--hexdump", action="store_true",
        help="Show the xxd hexdump of the code."
    )
    argv, info = parser.parse_args(), set()
    argv.repl = argv.repl or all(list(map(
        lambda x: x in ["-g", "-grave", "--v", "--verbose"], sys.argv[1:]
    )))
    if argv.test:
        from test import CharcoalTests, RunTests
        RunTests()
        sys.exit()
    if argv.stepcanvas:
        info.add(Info.step_canvas)
    if argv.dumpcanvas:
        info.add(Info.dump_canvas)
    if argv.Wambiguities:
        info.add(Info.warn_ambiguities)
        AddAmbiguityWarnings()
    if not argv.restricted and (argv.prompt or not argv.input):
        info.add(Info.prompt)
    if not argv.restricted and argv.repl:
        info.add(Info.prompt)
        info.add(Info.is_repl)
    code = argv.code
    if argv.file:
        openfile = openl1 if argv.normalencoding or argv.decode else open
        if os.path.isfile(argv.file):
            with openfile(argv.file) as file:
                code = file.read()
                if argv.file.endswith(".clv"):
                    argv.verbose = True
                if argv.file.endswith(".clg"):
                    argv.grave = True
        elif os.path.isfile(argv.file + ".cl"):
            with openfile(argv.file + ".cl") as file:
                code = file.read()
        elif os.path.isfile(argv.file + ".clv"):
            with openfile(argv.file + ".clv") as file:
                code = file.read()
                argv.verbose = True
        elif os.path.isfile(argv.file + "clg"):
            with openfile(argv.file + ".clg") as file:
                code = file.read()
                argv.grave = True
        else:
            print(
                "FileNotFoundError: The specified Charcoal file was not found."
            )
            sys.exit(1)
    if argv.rawinputfile:
        with open(argv.rawinputfile) as file:
            argv.input = [file.read()] + argv.input
    if not argv.restricted and argv.inputfile:
        with open(argv.inputfile) as file:
            raw_file_input = file.read()
        try:
            file_input = list(map(str, literal_eval(raw_file_input)))
            if not isinstance(file_input, list):
                raise Exception()
        except:
            file_input = (
                raw_file_input.split("\n") if
                "\n" in raw_file_input else
                raw_file_input.split(" ")
            )
        argv.input += file_input
        del raw_file_input
        del file_input
    if not argv.restricted and argv.outputfile:
        with open(argv.outputfile) as file:
            raw_file_output = file.read()
        try:
            file_output = list(map(str, literal_eval(raw_file_output)))
            if not isinstance(file_ouptut, list):
                raise Exception()
        except:
            file_output = (
                raw_file_output.split("\n") if
                "\n" in raw_file_output else
                raw_file_output.split(" ")
            )
        argv.output += raw_file_output
        del raw_file_output
        del file_output
    if argv.disablecompression:
        StringifierProcessor[CharcoalToken.String][0] = lambda result: [re.sub(
            "\n", "¶", rCommand.sub(r"´\1", result[0])
        )]
    if argv.verbose or argv.deverbosify:
        code = ParseExpression(
            code, grammars=VerboseGrammars, processor=StringifierProcessor,
            verbose=True
        )[0]
        if isinstance(code, list):
            PrintParseTrace(code)
            sys.exit(1)
        code = Golf(code)
        if argv.deverbosify:
            print(code)
    if argv.grave or argv.degrave:
        code = Degrave(code)
        if argv.degrave:
            print(code)
    elif argv.normalencoding or argv.decode:
        code = Decode(code)
        argv.normalencoding = False
        if argv.decode:
            print(code)
    if argv.showlength:

        def charcoal_length(character):
            ordinal = ord(character)
            if ordinal < 16512:
                return 3
            if ordinal < 2113664:
                return 4
            return 5
        length = 0
        for character in code:
            if InCodepage(character) or ord(character) < 256:
                length += 1
            else:
                length += charcoal_length(
                    ReverseLookup.get(character, character)
                )
        print("Charcoal, %i bytes: `%s`" % (length, re.sub("`", "\`", code)))
    if argv.hexdump:
        print_xxd(code)
    if argv.astify or argv.onlyastify and not argv.repl:
        print("Program")
        result = Parse(
            code, whitespace=argv.whitespace,
            normal_encoding=argv.normalencoding
        )
        if isinstance(result[0], CharcoalToken):
            print("""\
Parsing failed, parsed:
%s

Parse trace:
%s
""" % (result[2], "".join()))
        else:
            PrintTree(result)
        if argv.onlyastify:
            sys.exit()
    if argv.deverbosify and not argv.verbose:
        sys.exit()
    if argv.degrave and not argv.grave:
        sys.exit()
    global_charcoal = Charcoal(
        info=info, canvas_step=argv.canvasstep, original_input=argv.input
    )
    if argv.repl:
        is_clear = True
        prompt = "\033[36;1mCharcoal> \033[0m"
        while True:
            try:
                code = old_input(prompt)
                if argv.verbose:
                    code = ParseExpression(
                        code, grammars=VerboseGrammars,
                        processor=StringifierProcessor, verbose=True
                    )[0]
                    code = Golf(code)
                if argv.grave:
                    code = Degrave(code)
                if argv.astify:
                    print("Program")
                    PrintTree(Parse(
                        code, whitespace=argv.whitespace,
                        normal_encoding=argv.normalencoding
                    ))
                print(Run(
                    code, (argv.input or [""])[0], charcoal=global_charcoal,
                    whitespace=argv.whitespace,
                    normal_encoding=argv.normalencoding
                ))
                is_clear = False
            except KeyboardInterrupt:
                if is_clear:
                    break
                global_charcoal.Clear()
                print("\nCleared canvas")
                is_clear = True
            except EOFError:
                break
    elif len(argv.input) <= 1 and not len(argv.output):
        result = Run(
            code, argv.input[0] if len(argv.input) else "",
            charcoal=global_charcoal, whitespace=argv.whitespace,
            normal_encoding=argv.normalencoding
        )
        if not argv.stepcanvas and global_charcoal.print_at_end:
            sys.stdout.write(result)
    else:
        successes = failures = 0
        argv.input = [ProcessInput(inp) for inp in argv.input]
        argv.output = argv.output
        output_length = len(argv.output) + 1
        test_charcoal = Charcoal()
        program = GetProgram(
            code, whitespace=argv.whitespace,
            normal_encoding=argv.normalencoding
        )
        if argv.quiettesting:
            for i in range(len(argv.input)):
                test_charcoal.Clear()
                test_charcoal.ClearInputs()
                test_charcoal.AddInputs(argv.input[i])
                program(test_charcoal)
                result = str(test_charcoal)
                if i < output_length:
                    success = result == argv.output[i]
                    if success:
                        successes += 1
                    else:
                        failures += 1
        else:
            next_padding = 10
            padding = "=" * 12
            success_padding = ["=" * 19, "=" * 21]
            success_string = ["failed", "succeded"]
            for i in range(len(argv.input)):
                if i == next_padding:
                    padding += "="
                    next_padding *= 10
                test_charcoal.Clear()
                test_charcoal.ClearInputs()
                test_charcoal.AddInputs(argv.input[i])
                program(test_charcoal)
                result = str(test_charcoal)
                if i < output_length:
                    success = result == argv.output[i]
                    if success:
                        successes += 1
                    else:
                        failures += 1
                    print("%s\nTest case %i %s:\n%s" % (
                        success_padding[success], i + 1,
                        success_string[success], success_padding[success]
                    ))
                else:
                    print("%s\nTest case %i:\n%s" % (padding, i + 1, padding))
                print(result)
        if output_length > 1:
            real_output_length = output_length - 1
            print("%i/%i successes (%g%%)" % (
                successes,
                real_output_length,
                successes * 100 / real_output_length
            ))
            print("%i/%i failures (%g%%)" % (
                failures,
                real_output_length,
                failures * 100 / real_output_length
            ))
