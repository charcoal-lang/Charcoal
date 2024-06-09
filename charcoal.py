#!/usr/bin/env python3
"""
Charcoal's main module.

Contains definitions for the Charcoal canvas object, \
the CLI, and various classes used by the Charcoal class.

"""

from direction import Direction, DirectionToString, Pivot
from charcoaltoken import CharcoalToken as CT, CharcoalTokenNames as CTNames
from charactertransformers import *
from directiondictionaries import *
from unicodegrammars import UnicodeGrammars
from verbosegrammars import VerboseGrammars
from astprocessor import ASTProcessor
from interpreterprocessor import InterpreterProcessor, iter_apply
from stringifierprocessor import StringifierProcessor
from codepage import (
    UnicodeLookup, ReverseLookup, UnicodeCommands, InCodepage, sOperator,
    rCommand
)
from compression import Decompressed, Escaped
from wolfram import *
from extras import *
from enum import Enum
from ast import literal_eval
from time import sleep, perf_counter as clock, time as now
from math import ceil, log2
import random
import re
import argparse
import os
import sys
import builtins
import types
import zlib
import base64

command_abbreviations = {}

for alias, builtin in [
    ("A", abs), ("B", bin), ("C", complex), ("D", dict), ("E", enumerate),
    ("F", format), ("G", range), ("H", hex), ("I", __import__), ("M", sum),
    ("N", min), ("O", oct), ("P", repr), ("R", reversed), ("S", sorted),
    ("V", eval), ("X", max), ("Z", zip)
]:
    setattr(builtins, alias, builtin)

_H = H


def H(item):
    if isinstance(item, int):
        return hex(item)
    if isinstance(item, float):
        return item.hex()
    if isinstance(item, String):
        item = str(item)
    if isinstance(item, str):
        item = float(item) if "." in item else int(item)
        return h(item)
    if hasattr(item, "__iter__"):
        if isinstance(item[0], Expression):
            item = iter_apply(item, lambda o: o.run())
        return iter_apply(item, H)

_B = B


def B(item):
    if isinstance(item, float):
        item = int(item)
    if isinstance(item, int):
        return bin(item)
    if isinstance(item, String):
        item = str(item)
    if isinstance(item, str):
        item = float(item) if "." in item else int(item)
        return b(item)
    if hasattr(item, "__iter__"):
        if isinstance(item[0], Expression):
            item = iter_apply(item, lambda o: o.run())
        return iter_apply(item, B)


def warn(s):
    sys.stderr.write(str(s) + "\n")


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

stringify_lookup = {
    "e": "cdflmnosv"
}

def StringifyCode(code):
    result = []
    stack = []
    length = len(code)
    for i in range(length):
        add = True
        item = code[i]
        if (
            item[0] == "s" and
            item[1][0] == "´" and
            not rCommand.match(item[1][1])
        ):
            item = ("s", item[1][1:])
        if item[0] != "!":
            if item[0] != "m":
                j = i + 1
                while j < length and code[j][0] == "!":
                    j += 1
                if (
                    j < length and
                    code[j][0] == "s" and
                    code[j][1][0] == "´" and
                    not rCommand.match(code[j][1][1])
                ):
                    code[j] = ("s", code[j][1][1:])
            if item[0] == "$" and item[1] == "Ｍ":
                add = code[i + 1][0] != "a" or (
                    i > 1 and code[i - 1][0] == "m" or (
                        i + 2 < length and
                        code[i + 2][0] in stringify_lookup["e"]
                    )
                )
            while stack:
                notter = stack[0]
                if item[0] in stringify_lookup.get(notter[1], notter[1]):
                    result += [(";", "¦")]
                stack = stack[1:]
            stack = []
            if add:
                result += [item]
        else:
            stack += [item]
    while len(result) and result[-1][0] == ">":
        result.pop()
    if len(result) and result[-1][0] == "c":
        result[-1] = ("c", result[-1][1][:-1])
    return "".join(b for _, b in result)


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
    def __call__(self, *args, **kwargs):
        if kwargs == {}:
            if len(args) == 1:
                return args[0]
            if not len(args):
                return self
        return dict(enumerate(args), **kwargs)

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

    def __int__(self):
        return 0

    def __str__(self):
        return ""

    def __repr__(self):
        return ""

whatever = Whatever()


class Coordinates(object):
    __slots__ = ("top", "coordinates", "list")

    def __init__(self):
        self.top = 0
        self.coordinates = [[]]
        self.list = []

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
        self.list += [(x, y)]


class Scope(object):
    __slots__ = ("parent", "lookup")

    def __init__(self, parent=None, lookup=None):
        self.parent = parent or {}
        self.lookup = lookup or {}

    def __next__(self):
        key = next(filter(
            lambda character: character not in self,
            "ικλμνξπρςστυφχψωαβγδεζηθ"
        ))
        self.lookup[key] = None
        return key

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
        else:
            self.parent[key] = value

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


def GetPythonFunction(name):
    if isinstance(name, String):
        name = str(name)
    elif not isinstance(name, str):
        return None
    function, name, _name = None, name[:], name[:]
    if "." in name:
        try:
            module, *parts = name.split(".")
            if module not in imports:
                imports[module] = __import__(module)
            function = imports[module]
            for part in parts:
                function = getattr(function, part)
            return function
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
                return None
            return function
        else:
            variable, *parts = name.split(".")
            if variable in loc:
                function = loc[variable]
            elif variable in glob:
                function = glob[variable]
            elif hasattr(builtins, variable):
                function = getattr(builtins, variable)
            else:
                return None
            for part in parts:
                function = function[part]
            return function


class Cells(list):
    __slots__ = ("xs", "ys", "charcoal")

    def __init__(self, charcoal, value, xs=None, ys=None):
        if isinstance(value, Cells):
            result = charcoal
            indices = xs
            super().__init__(result)
            if indices is None:
                self.xs = value.xs
                self.ys = value.ys
            else:
                self.xs = [value.xs[i] for i in indices]
                self.ys = [value.ys[i] for i in indices]
            self.charcoal = value.charcoal
            return
        super().__init__(value)
        self.xs = xs
        self.ys = ys
        self.charcoal = charcoal

    def __setitem__(self, i, value):
        super().__setitem__(i, value)
        if isinstance(i, slice):
            start = i.start or 0
            stop = len(self) if i.stop is None else i.stop
            step = 1 if i.step is None else i.step
            for i in range(start, stop, step):
                self.charcoal.Put(self[i], self.xs[i], self.ys[i])
            return
        self.charcoal.Put(self[i], self.xs[i], self.ys[i])

    def __getitem__(self, i):
        if isinstance(i, slice):
            start = i.start or 0
            stop = len(self) if i.stop is None else i.stop
            step = 1 if i.step is None else i.step
            return Cells(
                self.charcoal,
                super().__getitem__(slice(start, stop, step)),
                self.xs[start:stop:step],
                self.ys[start:stop:step]
            )
        return super().__getitem__(i)


class Charcoal(object):
    __slots__ = (
        "x", "y", "top", "lines", "indices", "lengths", "right_indices",
        "top_scope", "scope", "info", "original_input", "inputs",
        "original_inputs", "direction", "background", "bg_lines",
        "bg_line_number", "bg_line_length", "timeout_end", "dump_timeout_end",
        "trim", "print_at_end", "canvas_step",
        "last_printed", "charcoal"
    )

    secret = {}
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
        self.info = info
        self.original_input = original_input
        self.inputs = inputs
        self.original_inputs = inputs[:]
        self.top_scope = self.scope = Scope(lookup={
            "γ": " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ\
[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~",
            "β": "abcdefghijklmnopqrstuvwxyz",
            "α": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            "ω": "",
            "ψ": "\000",
            "χ": 10,
            "φ": 1000,
            "υ": []
        })
        self.direction = Direction.right
        self.background = " "
        self.bg_lines = [" "]
        self.bg_line_number = self.bg_line_length = 1
        self.timeout_end = self.dump_timeout_end = 0
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
        if not self.background:
            for i in range(len(self.lines)):
                top = self.top + i
                index = self.indices[i]
                line = self.lines[i]
                bg_start = None
                j = 0
                if "\000" in line:
                    for character in line:
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
                        j += 1
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
            for line, index, right_index in zip(
                self.lines, self.indices, self.right_indices
            ):
                string += (
                    self.background * (index - left) +
                    (
                        re.sub("\000", self.background, line)
                        if "\000" in line else line
                    ) +
                    (
                        "" if self.trim else
                        self.background * (right - right_index)
                    ) +
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

    def AddInputs(self, inputs):
        """
        AddInputs(inputs)

        Adds given inputs to the inputs of the canvas.

        """
        self.original_inputs += inputs
        self.inputs += inputs

    def ClearInputs(self):
        """
        ClearInputs()

        Removes all inputs from canvas.

        """
        self.inputs = []
        self.original_inputs = []

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
        if all:
            self.top_scope = self.scope = Scope(lookup={
                "γ": " !\"#$%&'()*+,-./0123456789:;<=>?@\
ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~",
                "β": "abcdefghijklmnopqrstuvwxyz",
                "α": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                "ω": "",
                "ψ": "\000",
                "χ": 10,
                "φ": 1000,
                "υ": []
            })
            self.inputs = self.original_inputs[:]
            self.direction = Direction.right
            self.background = " "
            self.bg_lines = [" "]
            self.bg_line_number = self.bg_line_length = 1
            self.timeout_end = self.dump_timeout_end = 0
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

    def CanFillAt(self, x, y):
        """
        CanFillAt() -> bool

        Returns whether there is a "\000" under the cursor

        """
        y_index = y - self.top
        result = False
        if (
            y_index < len(self.lines) and
            y_index >= 0 and
            x - self.indices[y_index] < self.lengths[y_index] and
            x - self.indices[y_index] >= 0
        ):
            result = (
                self.lines[y_index][x - self.indices[y_index]] == "\000"
            )
        return result

    def Put(self, string, x=None, y=None):
        """
        Put(string, x=None, y=None)

        Put string at position x, y. Defaults to cursor position.

        """
        x = self.x if x is None else x
        if y is not None:
            original_x, original_y, self.x, self.y = self.x, self.y, x, y
            self.FillLines()
            self.x, self.y = original_x, original_y
        y = self.y if y is None else y
        y_index = y - self.top
        x_index = self.indices[y_index]
        line = self.lines[y_index]
        if not line:
            length = len(string)
            self.lines[y_index] = string
            self.indices[y_index] = x
            self.lengths[y_index] = length
            self.right_indices[y_index] = x + length
            return
        start = x - x_index
        end = start + len(string)
        self.lines[y_index] = (
            line[:max(0, start)] +
            "\000" * (start - len(line)) +
            string +
            "\000" * -end +
            line[max(0, end):]
        )
        if x < x_index:
            self.indices[y_index] = x
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
            x_number = self.x - self.indices[0] if len(self.indices) else 0
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
        lines = string.split("\n")
        length = max(len(line) for line in lines)
        if length:
            self.bg_lines = [
                line + " " * (length - len(line))
                for line in lines
            ]
            self.bg_line_number = len(lines)
            self.bg_line_length = length
            if length > 1 or len(lines) > 1:
                self.background = ""
            else:
                self.background = string
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
                ) and not string:
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
                    if overwrite or not current or current == "\000":
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
            
            def pad(s, p, n):
                return p * (n - len(s)) + s
            matrix = [[str(item) for item in row] for row in matrix]
            maximum = max(
                max(len(item) for item in row + [""]) for row in matrix
            )
            return "\n".join(
                " ".join(pad(item, " ", maximum) for item in row)
                for row in matrix
            )

        def simplify(string):
            if isinstance(string, Expression):
                string = string.run()
                string_type = type(string)
                if (
                    string_type == String or
                    isinstance(string, Symbolic)
                ):
                    return (str(string), 0)
                if string_type == List:
                    if (
                        len(string.leaves) and
                        isinstance(string.leaves[0], List) and
                        all(
                            len(leaf.leaves) and
                            all(
                                not isinstance(leaf, List)
                                for leaf in leaf.leaves
                            ) for leaf in string.leaves
                        )
                    ):
                        length = len(string.leaves[0])
                        if all(
                            len(leaf.leaves) == length
                            for leaf in string.leaves
                        ):
                            return (grid([
                                [
                                    simplify(minileaf)[0]
                                    for minileaf in leaf.leaves
                                ]
                                for leaf in string.leaves
                            ]), 1)
                    result = [simplify(leaf) for leaf in string.leaves]
                    depth = 1 + max([item[1] for item in result] + [0])
                    return (("\n" * depth).join(
                        item[0] for item in result
                    ), depth)
                if string_type in [Rule, DelayedRule, Pattern]:
                    return ("", 0)  # TODO
                if string_type == WolframFalse:
                    return ("False", 0)
                if string_type == WolframTrue:
                    return ("True", 0)
                return (str(string), 0)
            return (string, 0)
        if (
            callable(string) and
            not isinstance(string, Whatever) and
            not isinstance(string, SymbolicVariable)
        ):
            string = string()
        if isinstance(string, Expression):
            string = simplify(string)[0]
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
        if not isinstance(string, str):
            string = str(string)
        old_x = self.x
        old_y = self.y
        if length and "\n" not in string:
            self.PrintLine(directions, length, string, multiprint=multiprint)
            self.last_printed = original
            return
        lines = re.split("\n|\r", string)
        seps = re.findall("\n|\r", string)
        for direction in directions:
            self.x = old_x
            self.y = old_y
            if direction == Direction.right:
                initial_x = self.x
                for i in range(len(lines)):
                    line = lines[i]
                    self.PrintLine({Direction.right}, len(line), line)
                    if i < len(seps) and seps[i] == "\r":
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
                    if i < len(seps) and seps[i] == "\r":
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
                    if i < len(seps) and seps[i] == "\r":
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

    def Polygon(self, sides, character, fill=True, border_only=False):
        """
        Polygon(sides, character, fill=True)

        Draws a polygon with sides in the specified direction \
and length, filling with the specified character if \
the two endpoints of the line are can be joined with \
a horizontal, vertical or diagonal line.

        """
        multichar_fill = len(character) > 1
        lines = None
        if multichar_fill and not border_only:
            lines = character.split("\n")
            character = "*"
        initial_x, initial_y, counter = self.x, self.y, 0
        coordinates = Coordinates()
        for i in range(len(sides)):
            direction, length = sides[i]
            length = int(length)
            if length < 0:
                direction = NewlineDirection[NewlineDirection[direction]]
                length *= -1
            self.PrintLine(
                {direction},
                length - (i < len(sides) - 1),
                (
                    (character[counter:] + character[:counter])
                    if border_only else
                    character
                ),
                coordinates=coordinates,
                move_at_end=(i < len(sides) - 1),
                multichar_fill=multichar_fill
            )
            if border_only:
                counter = (
                    (counter + length - (i < len(sides) - 1)) % len(character)
                )
            if Info.step_canvas in self.info:
                self.RefreshFastText("Polygon side", self.canvas_step)
            elif Info.dump_canvas in self.info:
                print("Polygon side")
                print(str(self))
        if border_only:
            if self.x == initial_x and self.y == initial_y:
                self.Put(character[0])
            return
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
            self.x = initial_x
            self.y = initial_y
            self.Polygon(
                sides, "\n".join(lines) if lines is not None else character,
                fill, border_only=True
            )
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
                while len(row) >= 2:
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
                if len(row):
                    position = row[0]
                    index = position % line_length
                    self.x = position
                    self.Put(line[index])
                self.y += 1
        else:
            for row in coordinates.coordinates:
                if len(row) % 2:
                    row = row[:-1] + row[-2:]
                while len(row) >= 2:
                    start, end = row[:2]
                    row = row[2:]
                    if start > end:
                        start, end = end, start
                    if end - start < 2:
                        continue
                    length = end - start
                    self.x = start + 1
                    self.PrintLine({Direction.right}, length, character)
                if len(row):
                    position = row[0]
                    self.x = position
                    self.Put(character)
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
        step_canvas = Info.step_canvas in self.info
        dump_canvas = Info.dump_canvas in self.info
        self.info -= {Info.step_canvas, Info.dump_canvas}
        self.Polygon([
            [Direction.right, width],
            [Direction.down, height],
            [Direction.left, width],
            [Direction.up, height]
        ], fill)
        if step_canvas:
            self.info |= {Info.step_canvas}
        if dump_canvas:
            self.info |= {Info.dump_canvas}
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
            else:
                self.Move(Direction.left if w else Direction.right, width - 1)
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
                    self.CanFillAt(x, y) and
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

        if not self.CanFillAt(x, y):
            return
        points.add((y, x))
        stack += [Segment(x, x + 1, y, 0, True, True)]
        while len(stack):
            r = stack.pop()
            start_x, end_x = r.start_x, r.end_x
            if r.scan_left:
                while (
                    start_x > left and
                    self.CanFillAt(start_x - 1, r.y) and
                    not (r.y, start_x - 1) in points
                ):
                    start_x -= 1
                    points.add((r.y, start_x))
            if r.scan_right:
                while (
                    self.CanFillAt(end_x, r.y) and
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
        self.x, self.y = x0, y0
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
        if isinstance(direction, float) or isinstance(direction, str):
            direction = int(direction)
        if isinstance(length, float) or isinstance(length, str):
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
                for line, length, right_index in zip(
                    self.lines[:], self.lengths[:], self.right_indices[:]
                ):
                    self.x += 1
                    self.y = right_index + top_right
                    self.PrintLine(
                        {Direction.up},
                        length,
                        "".join(
                            NWSEFlip.get(character, character)
                            for character in line[::-1]
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
                    self.lines[::-1], self.lengths[::-1], self.indices[::-1]
                ):
                    self.x -= 1
                    self.y = index + bottom_left
                    self.PrintLine(
                        {Direction.down},
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
                for line, length, right_index in zip(
                    self.lines[::-1], self.lengths[::-1],
                    self.right_indices[::-1]
                ):
                    self.x += 1
                    self.y = bottom_right - right_index
                    self.PrintLine(
                        {Direction.down},
                        length,
                        "".join(
                            NESWFlip.get(character, character)
                            for character in line[::-1]
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

        Overlaps the axis by the specified number of characters.

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
        finished, initial_x, initial_y = True, self.x, self.y
        if direction == Direction.left:
            self.y = self.top
            left = min(self.indices)
            for line, length, index in zip(
                self.lines[:], self.lengths[:], self.indices[:]
            ):
                self.x = left * 2 - index + overlap - 1
                string = (
                    "".join(HorizontalFlip.get(c, c) for c in line)
                    if transform else line
                )
                self.PrintLine(
                    {Direction.left}, len(string), string, overwrite=False
                )
                self.y += 1
            self.x = initial_x - (initial_x - left) * 2 + overlap - 1
            self.y = initial_y
        elif direction == Direction.right:
            self.y = self.top
            right = max(self.right_indices)
            for line, length, index in zip(
                self.lines[:], self.lengths[:], self.indices[:]
            ):
                self.x = right * 2 - index - overlap - 1
                string = (
                    "".join(HorizontalFlip.get(c, c) for c in line)
                    if transform else line
                )
                self.PrintLine(
                    {Direction.left}, len(string), string, overwrite=False
                )
                self.y += 1
            self.x = initial_x + (right - initial_x - 1) * 2 + 1 - overlap
            self.y = initial_y
        elif direction == Direction.up:
            self.y = self.top + overlap - 1
            final_y = self.y - (initial_y - self.top)
            for line, length, index in zip(
                self.lines[:], self.lengths[:], self.indices[:]
            ):
                self.x = index
                string = (
                    "".join(VerticalFlip.get(c, c) for c in line)
                    if transform else line
                )
                self.PrintLine(
                    {Direction.right}, len(string), string, overwrite=False
                )
                self.y -= 1
            self.x = initial_x
            self.y = final_y
        elif direction == Direction.down:
            line_count = len(self.lines)
            self.y = self.top + line_count * 2 - overlap - 1
            final_y = self.y - (initial_y - self.top)
            for line, length, index in zip(
                self.lines[:], self.lengths[:], self.indices[:]
            ):
                self.x = index
                string = (
                    "".join(VerticalFlip.get(c, c) for c in line)
                    if transform else line
                )
                self.PrintLine(
                    {Direction.right}, len(string), string, overwrite=False
                )
                self.y -= 1
            self.x = initial_x
            self.y = final_y
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
                    "".join(NESWFlip.get(c, c) for c in line)
                    if transform else
                    line
                )
                self.PrintLine(
                    {Direction.down}, len(string), string, overwrite=False
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
                    "".join(NWSEFlip.get(c, c) for c in line)
                    if transform else line
                )[::-1]
                self.PrintLine(
                    {Direction.down}, len(string), string, overwrite=False
                )
            self.x = bottom_right - initial_y - overlap
            self.y = bottom_right - initial_x - overlap
        if Info.step_canvas in self.info:
            self.RefreshFastText((
                "Reflect overlap transform" if transform else "Reflect overlap"
            ), self.canvas_step)
        elif Info.dump_canvas in self.info:
            print(
                "Reflect overlap transform" if transform else "Reflect overlap"
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
                "".join(HorizontalFlip.get(c, c) for c in line[::-1])
                for line in self.lines
            ] if transform else [
                line[::-1] for line in self.lines
            ]
            self.x = -self.x
        elif direction == Direction.up or direction == Direction.down:
            if transform:
                self.lines = [
                    "".join(VerticalFlip.get(c, c) for c in line)
                    for line in self.lines
                ]
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
                self.lines = [
                    "".join(NESWFlip.get(c, c) for c in line)
                    for line in self.lines
                ]
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
        old_x = self.x
        old_y = self.y
        old_top = self.top
        old_lines = self.lines
        old_indices = self.indices
        old_lengths = self.lengths
        self.top = 0
        self.lines = [""]
        self.indices = [0]
        self.lengths = [0]
        self.right_indices = [0]
        directions = {{
            1: Direction.up_right,
            2: Direction.up,
            3: Direction.up_left,
            4: Direction.left,
            5: Direction.down_left,
            6: Direction.down,
            7: Direction.down_right,
        }[rotations]}
        rotator = {
            1: lambda x, y: (y + x, y - x),
            2: lambda x, y: (y, -x),
            3: lambda x, y: (y - x, -y - x),
            4: lambda x, y: (-x, -y),
            5: lambda x, y: (-x - y, x - y),
            6: lambda x, y: (-y, x),
            7: lambda x, y: (x - y, x + y),
        }[rotations]
        for i in range(len(old_lines)):
            self.x, self.y = rotator(old_indices[i], old_top + i)
            self.PrintLine(directions, old_lengths[i], old_lines[i])
        self.x, self.y = rotator(old_x, old_y)
        if transform:
            transformer = ({
                1: RotateHalfLeft,
                2: RotateLeft,
                3: RotateThreeHalvesLeft,
                4: RotateDown,
                5: RotateThreeHalvesRight,
                6: RotateRight,
                7: RotateHalfRight
            })[rotations]
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
        y = self.top + delta_y
        for line, index in zip(self.lines[:], self.indices[:]):
            self.Put(line, index + delta_x, y)
            y += 1
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
        return next(self.scope);

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
        variable = expression(self)
        if isinstance(variable, float):
            variable = int(variable)
        if isinstance(variable, int):
            variable = large_range(variable)
        self.scope = Scope(self.scope)
        loop_variable = self.GetFreeVariable()
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
        if isinstance(variable, Expression):
            variable = variable.run()
        if isinstance(variable, String):
            variable = str(variable)
        if isinstance(variable, str):
            return literal_eval(variable or "0")
        if isinstance(variable, float):
            return "%.16g" % variable
        return str(variable)

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

    def Random(self, variable=2):
        """
        Random(variable=1)

        Returns a random number between 0 and variable \
if variable is a number, else returns a random item in variable.

        """
        if variable == 1 and Info.warn_ambiguities in self.info:
            print("""\
Warning: Possible ambiguity, make sure you explicitly use 2 if needed""")
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
        if key in "θηζεδ":
            index = "θηζεδ".index(key)
            while len(self.original_inputs) <= index:
                self.InputString()
            return self.original_inputs[index]
        if key in Charcoal.secret:
            return Charcoal.secret[key]
        python_function = GetPythonFunction(key)
        if python_function:
            return python_function
        if re.match("[a-zA-Z_]+$", key):
            return SymbolicVariable(key)
        return whatever

    def Assign(self, value, key, value2=None):
        """
        Assign(value, key, value2=None)

        If value2 is not None, set value[key] to value2, \
else set the variable with the given name to the given value.

        """
        if value2 is not None:
            try:
                value[key] = value2
            except:
                value[key % len(value)] = value2
            if Info.step_canvas in self.info and isinstance(value, Cells):
                self.RefreshFastText("Assign", self.canvas_step)
            elif Info.dump_canvas in self.info:
                print("Assign")
                print(str(self))
            return

        self.scope[key] = value

    def InputString(self, key=None):
        """
        InputString(key=None)

        Gets next input as string.

        If key is truthy, set the variable key to the input.

        """
        return self.Input(key, string=True)

    def InputNumber(self, key=None):
        """
        InputNumber(key=None)

        Gets next input as number.

        If key is truthy, set the variable key to the input.

        """
        return self.Input(key, number=True)

    def Input(self, key=None, number=False, string=False):
        """
        Input(key=None, number=False, string=False)

        Gets next input as number if possible, else as a stirng.

        If key is truthy, set the variable key to the input.

        If number is truthy, return result as number.

        If string is truthy, return result as string.

        """
        result = ""
        if self.inputs:
            result = self.inputs.pop(0)
        elif Info.prompt in self.info:
            result = input("Enter input: ")
            self.original_inputs += [result]
        if number and isinstance(result, str):
            try:
                result = literal_eval(result)
            except:
                result = 0
        if string:
            result = str(result)
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
        if type(code) == Expression:
            code = code.run()
        code = str(code)
        if is_command:
            Run(code, charcoal=self)
            return
        return Run(code, grammar=CT.Expression)

    def EvaluateVariable(self, name, arguments):
        """
        EvaluateVariable(name, arguments)

        Executes the function with the specified name with the specified
arguments.

        Returns the result.

        """
        if isinstance(name, String):
            name = str(name)
        result = None
        if isinstance(name, Expression):
            result = name.run()(*arguments)
        elif name in self.scope:
            result = self.scope[name](*arguments)
        elif name in Charcoal.secret:
            result = Charcoal.secret[name](*arguments)
        else:
            python_function = GetPythonFunction(name)
            if python_function:
                return python_function(*arguments)
            elif re.match("[a-zA-Z_]+$", name):
                return SymbolicVariable(name)(arguments)
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
        elif name in Charcoal.secret:
            Charcoal.secret[name](*arguments)
        else:
            python_function = GetPythonFunction(name)
            if python_function:
                python_function(*arguments)
        self.charcoal = None

    def Lambdafy(self, function):
        """
        Lambdafy(name, function) -> (*arguments -> Any)

        Turns the given Charcoal function into a lambda accepting arguments

        """

        def run(function, arguments, charcoal):
            lookup = {}
            for argument, key in zip(arguments, "ικλμνξπρςστυφχψωαβγδεζηθ"):
                lookup[key] = argument
            charcoal.scope = Scope(self.scope, lookup)
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
        if isinstance(iterable, int) or isinstance(iterable, float):
            iterable, length = length, iterable
        if isinstance(length, list) or isinstance(length, str):
            length = len(length)
        elif isinstance(length, float):
            length = int(length)
        return (iterable * (length and length // len(iterable) + 1))[:length]

    def Crop(self, width, height=None):
        """
        Crop(width, height)

        Crop the canvas to width columns and height rows.

        """
        if height is None:
            height = width
        width, height = int(width), int(height)
        top_crop = max(0, self.y - self.top)
        bottom_crop = max(0, self.y + height - self.top)
        self.top += top_crop
        self.lines = self.lines[top_crop:bottom_crop]
        self.indices = self.indices[top_crop:bottom_crop]
        self.lengths = self.lengths[top_crop:bottom_crop]
        self.right_indices = self.right_indices[top_crop:bottom_crop]
        for i in range(len(self.lines)):
            left_crop = max(0, self.x - self.indices[i])
            right_crop = max(0, self.x + width - self.indices[i])
            length = self.lengths[i]
            self.lines[i] = self.lines[i][left_crop:right_crop]
            self.indices[i] += left_crop
            self.lengths[i] = len(self.lines[i])
            self.right_indices[i] = self.indices[i] + self.lengths[i]
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
            joiner = "\000" * (horizontal - 1)
            self.lines = [joiner.join(line) for line in self.lines]
            self.lengths = [
                length and (length - 1) * horizontal + 1
                for length in self.lengths
            ]
            self.indices = [index * horizontal for index in self.indices]
            self.right_indices = [
                (right_index - 1) * horizontal + 1
                for right_index in self.right_indices
            ]
            self.x *= horizontal
        if vertical:
            new_number = (len(self.lines) - 1) * vertical + 1
            lines = [""] * new_number
            indices = [0] * new_number
            lengths = [0] * new_number
            right_indices = [0] * new_number
            lines[::vertical] = self.lines
            lengths[::vertical] = self.lengths
            indices[::vertical] = self.indices
            right_indices[::vertical] = self.right_indices
            self.lines = lines
            self.lengths = lengths
            self.indices = indices
            self.right_indices = right_indices
            self.top *= vertical
            self.y *= vertical
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
                if character == "\000":
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

    def Map(self, iterable, function, is_command=False, string_map=False):
        """
        Map(iterable, function, is_command=False)

        Returns an iterable with the results of applying \
a function to each element of the iterable.

        If is_command is True, it mutates the original \
iterable, else it returns the iterable.

        If string_map is True, the iterable is turned into a string.

        """
        if type(iterable) == Expression:
            iterable = iterable.run()
        if callable(iterable):
            iterable, function = function, iterable
        if type(iterable) == Expression:
            iterable = iterable.run()
        if isinstance(iterable, float):
            iterable = int(iterable)
        if isinstance(iterable, int):
            iterable = list(range(iterable))
        result = []
        self.scope = Scope(self.scope)
        loop_variable = self.GetFreeVariable()
        index_variable = self.GetFreeVariable()
        for i, v in iterable.items() if isinstance(iterable, dict) else enumerate(iterable):
            self.scope[loop_variable] = v
            self.scope[index_variable] = i
            result += [function(self)]
        if is_command:
            if isinstance(iterable, list):
                iterable[:] = result
            elif isinstance(iterable, dict):
                for i in iterable:
                    iterable[i] = result.pop(0)
        self.scope = self.scope.parent
        if isinstance(iterable, Cells):
            if Info.step_canvas in self.info:
                self.RefreshFastText("Map", self.canvas_step)
            elif Info.dump_canvas in self.info:
                print("Map")
                print(str(self))
        if not is_command:
            if string_map:
                return "".join(map(str, result))
            if isinstance(iterable, str) or isinstance(iterable, dict):
                return result
            try:
                return type(iterable)(result)
            except:
                return type(iterable)(result, iterable)

    def Filter(self, iterable, function):
        """
        Filter(iterable, function)

        Returns an iterable, keeping only elements where the result of \
a function is truthy.

        """
        if type(iterable) == Expression:
            iterable = iterable.run()
        if callable(iterable):
            iterable, function = function, iterable
        if type(iterable) == Expression:
            iterable = iterable.run()
        if isinstance(iterable, float):
            iterable = int(iterable)
        if isinstance(iterable, int):
            iterable = list(range(iterable))
        result = []
        indices = []
        self.scope = Scope(self.scope)
        loop_variable = self.GetFreeVariable()
        index_variable = self.GetFreeVariable()
        for i, v in iterable.items() if isinstance(iterable, dict) else enumerate(iterable):
            self.scope[loop_variable] = v
            self.scope[index_variable] = i
            if function(self):
                result += [iterable[i]]
                indices += [i]
        self.scope = self.scope.parent
        if isinstance(iterable, str):
            return "".join(result)
        if isinstance(iterable, dict):
            return dict(zip(indices, result))
        try:
            return type(iterable)(result)
        except:
            return type(iterable)(result, iterable, indices)

    def All(self, iterable, function):
        """
        All(iterable, function)

        Returns whether the function returns truthy for all values in the \
iterable.

        """
        if type(iterable) == Expression:
            iterable = iterable.run()
        if isinstance(iterable, float):
            iterable = int(iterable)
        if isinstance(iterable, int):
            iterable = range(iterable)
        result = 1
        self.scope = Scope(self.scope)
        loop_variable = self.GetFreeVariable()
        index_variable = self.GetFreeVariable()
        for i, v in iterable.items() if isinstance(iterable, dict) else enumerate(iterable):
            self.scope[loop_variable] = v
            self.scope[index_variable] = i
            if not function(self):
                result = 0
                break
        self.scope = self.scope.parent
        return result

    def Any(self, iterable, function):
        """
        Any(iterable, function)

        Returns whether the function returns truthy for any values in the \
iterable.

        """
        if type(iterable) == Expression:
            iterable = iterable.run()
        if isinstance(iterable, float):
            iterable = int(iterable)
        if isinstance(iterable, int):
            iterable = range(iterable)
        result = 0
        self.scope = Scope(self.scope)
        loop_variable = self.GetFreeVariable()
        index_variable = self.GetFreeVariable()
        for i, v in iterable.items() if isinstance(iterable, dict) else enumerate(iterable):
            self.scope[loop_variable] = v
            self.scope[index_variable] = i
            if function(self):
                result = 1
                break
        self.scope = self.scope.parent
        return result

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
            and not isinstance(left, set)
        )
        right_is_iterable = (
            hasattr(right, "__iter__") and not isinstance(right, str)
            and not isinstance(right, set)
        )
        if isinstance(left, dict) and isinstance(right, dict):
            left = left.copy()
            left.update(right)
            return left
        if isinstance(left, Pattern) or isinstance(right, Pattern):
            return left + right
        if left_is_iterable ^ right_is_iterable:
            if left_is_iterable:
                return [self.Add(item, right) for item in left]
            return [self.Add(left, item) for item in right]
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
            and not isinstance(left, set)
        )
        right_is_iterable = (
            hasattr(right, "__iter__") and not isinstance(right, str)
            and not isinstance(right, set)
        )
        if isinstance(left, dict) and isinstance(right, dict):
            return {key: value for key, value in left.items() if key not in right}
        if left_is_iterable or right_is_iterable:
            if left_is_iterable and right_is_iterable:
                result = [item for item in left if item not in right]
            else:
                result = (
                    [self.Subtract(item, right) for item in left]
                    if left_is_iterable else
                    [self.Subtract(left, item) for item in right]
                )
            result_type = type(left if left_is_iterable else right)
            try:
                return result_type(result)
            except:
                return result_type(result, iterable)
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

    def Multiply(self, left, right, iterable=True):
        if isinstance(left, String):
            left = str(left)
        if isinstance(right, String):
            right = str(right)
        if type(left) == Expression:
            left = left.run()
        if type(right) == Expression:
            right = right.run()
        if isinstance(left, Expression) and not isinstance(right, Expression):
            right = create_expression(right)
        if isinstance(right, Expression) and not isinstance(left, Expression):
            left = create_expression(left)
        if (
            isinstance(left, List) and
            isinstance(right, SymbolicOperation) and
            right.op == add and
            len(left.leaves) == len(right.items)
        ):
            return SymbolicOperation(add,
                *(l * r for l, r in zip(left.leaves, right.items))
            )
        if (
            isinstance(left, SymbolicOperation) and
            isinstance(right, List) and
            left.op == add and
            len(left.items) == len(right.leaves)
        ):
            return SymbolicOperation(add,
                *(l * r for l, r in zip(left.items, right.leaves))
            )
        left_type = type(left)
        right_type = type(right)
        left_is_iterable = hasattr(left, "__iter__")
        right_is_iterable = hasattr(right, "__iter__")
        if left_is_iterable ^ right_is_iterable:
            if left_is_iterable:
                if left_type == str:
                    return (left * (1 + int(right)))[:int(len(left) * right)]
                return [self.Multiply(item, right) for item in left]
            if right_type == str:
                return (right * (1 + int(left)))[:int(len(right) * left)]
            return [self.Multiply(left, item) for item in right]
        if left_is_iterable and right_is_iterable:
            if left_type == str:
                return left.join(map(str, right))
            if right_type == str:
                return right.join(map(str, left))
            return list(map(self.Multiply, left, right))
        return left * right

    def Divide(self, left, right, floor=True, iterable=True):
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
        if iterable:
            left_is_iterable = hasattr(left, "__iter__")
            right_is_iterable = hasattr(right, "__iter__")
            if left_is_iterable ^ right_is_iterable:
                if left_is_iterable:
                    if callable(right):
                        return reduce(left, right)
                    if left_type == str:
                        return (left * (1 + int(1 / right)))[
                            :int(len(left) / right)
                        ]
                    return [
                        self.Divide(item, right, floor=floor)
                        for item in left
                    ]
                if callable(left):
                    return reduce(right, left)
                if right_type == str:
                    return (right * (1 + int(1 / left)))[
                        :int(len(right) / left)
                    ]
                return [
                    self.Divide(left, item, floor=floor)
                    for item in right
                ]
        if left_type == str and right_type == str:
            return left.split(right)
        return left // right if floor else left / right

    # TODO: dry these
    def MapAssign(self, key, operator):
        iterable = self.Retrieve(key)
        if not hasattr(iterable, "__iter__"):
            self.scope[key] = operator(iterable, self)
            return
        self.scope[key] = [operator(item, self) for item in iterable]
        if isinstance(iterable, str):
            self.scope[key] = "".join(self.scope[key])
        if isinstance(iterable, String):
            self.scope[key] = String("".join(self.scope[key]))

    def MapAssignLeft(self, key, left, operator):
        iterable = self.Retrieve(key)
        if not hasattr(iterable, "__iter__"):
            self.scope[key] = operator(left, iterable, self)
            return
        self.scope[key] = [operator(left, item, self) for item in iterable]
        if isinstance(iterable, str):
            self.scope[key] = "".join(self.scope[key])
        if isinstance(iterable, String):
            self.scope[key] = String("".join(self.scope[key]))

    def MapAssignRight(self, key, right, operator):
        iterable = self.Retrieve(key)
        if not hasattr(iterable, "__iter__"):
            self.scope[key] = operator(iterable, right, self)
            return
        self.scope[key] = [operator(item, right, self) for item in iterable]
        if isinstance(iterable, str):
            self.scope[key] = "".join(self.scope[key])
        if isinstance(iterable, String):
            self.scope[key] = String("".join(self.scope[key]))

    def Base(self, item, base):
        if hasattr(base, "__iter__"):
            item, base = base, item
        if hasattr(item, "__iter__"):
            if isinstance(item, str):
                return self.BaseString(item, base)
            result = 0
            for element in item:
                if isinstance(element, str):
                    element = literal_eval(element or "0")
                result = result * base + element
            return result
        result, negative = [], False
        if item < 0:
            item, negative = -item, True
        while item:
            result = [item % base] + result
            item //= base
        return [-n for n in result] if negative else result

    def BaseString(self, item, base):
        if not base:
            return ""
        alphabet = "\
0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if hasattr(base, "__iter__"):
            alphabet, base = base, len(base)
        if hasattr(item, "__iter__"):
            result, sign, decimal = 0, 1, None
            if item[0] == "-":
                sign, item = -1, item[1:]
            if "." not in alphabet and "." in item:
                index = item.index(".")
                decimal = item[index + 1:]
                item = item[:index]
            for char in item:
                result = result * base + max(0, alphabet.index(char))
            if decimal:
                multiplier = 1
                for char in decimal:
                    multiplier /= base
                    result += multiplier * max(0, alphabet.index(char))
            return result * sign
        result, negative = "", ""
        if item < 0:
            item, negative = -item, "-"
        remainder = item % 1
        while item >= 1:
            result = (
                alphabet[item % base] +
                result
            )
            item //= base
        if not result:
            result = alphabet[0]
        if "." not in alphabet and remainder:
            result += "."
            precision = ceil(53 / log2(base))
            remainder *= base
            while remainder and precision:
                result += alphabet[int(remainder % base)]
                remainder = (remainder % 1) * base
                precision -= 1
        return negative + result


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
    grammar=CT.Program,
    grammars=UnicodeGrammars,
    processor=ASTProcessor,
    verbose=False,
    return_lexeme_index=False
):
    """
    ParseExpression(code, index=0, grammar=CT.Program, \
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
                    if token == CT.EOF:
                        if index != len(code):
                            success = False
                            break
                    elif token == CT.String:
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
                        tokens += [
                            processor[token][0]([literal_eval(
                                code[old_index:index]
                            )])
                        ]
                    elif token == CT.Number:
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
                        tokens += [
                            processor[token][0]([code[old_index:index]])
                        ]
                    elif token == CT.Name:
                        if index == len(code):
                            success = False
                            break
                        character = code[index]
                        if (
                            character in "abgdezhqiklmnxprsvtufcyw" and (
                                index == len(code) - 1 or
                                code[index + 1] not in "\
abcdefghijklmnopqrstuvwxyz"
                            )
                        ):
                            tokens += [processor[token][0]([character])]
                            index += 1
                        else:
                            success = False
                            break
                    elif token == CT.Fix:
                        infix_prec = {
                            "^": 7, "*": 6, "/": 6, "\\": 6, "%": 6,
                            "+": 5, "-": 5, "‹": 4, ">": 4, "==": 3,
                            "&": 2, "|": 1, "=": 0
                        }
                        prefix_prec = {
                            "--": 8, "++": 8, "**": 8, "//": 8,
                            "-": 8, "~": 8
                        }
                        def shunt(top=False):
                            nonlocal index
                            expect = [CT.Prefix, CT.Expression]
                            expect_lookup = {
                                CT.Prefix: [CT.Prefix, CT.Expression],
                                CT.Expression: [CT.Infix, CT.Prefix],
                                CT.Infix: [CT.Expression]
                            }
                            to_shunt, operators, types = [], [], []
                            success = True
                            while index < len(code) and success:
                                success = False
                                for expected in expect:
                                    parens = False
                                    if expected == CT.Expression:
                                        result = ParseExpression(code, index, CT.LP, grammars, processor, verbose, return_lexeme_index=True)

                                        if result and result[1] is not False and not result[2]:
                                            index = result[1]
                                            result = shunt()
    
                                            if not result or result[1] is False:
                                                break

                                            success = True
                                            to_shunt += [result]
                                            operators += [None]
                                            types += [CT.Expression]
                                            expect = expect_lookup[expected]
                                            break
                                    result = ParseExpression(code, index, expected, grammars, processor, verbose, return_lexeme_index=True)
                                    
                                    if not result or result[1] is False:
                                        continue
                                    
                                    success = True
                                    to_shunt += [result[0]]
                                    operators += [None if expected == CT.Expression else grammars[expected][result[2]][0]]
                                    types += [expected]
                                    index = result[1]
                                    expect = expect_lookup[expected]
                                    break

                            if not top:
                                close_paren = ParseExpression(code, index, CT.RP, grammars, processor, verbose, return_lexeme_index=True)
                                if not close_paren or close_paren[1] is False or close_paren[2]:
                                    return None
                                index = close_paren[1]

                            if not len(to_shunt):
                                return None
                                
                            # begin shunting
                            result, operator_stack, precedences = [], [], []
                            is_prefix, is_eq, can_prefix = [], False, True
                            for item, type, op in zip(to_shunt, types, operators):
                                if type == CT.Expression:
                                    result += [item]
                                    can_prefix = False
                                else:
                                    if (
                                        op == "=" and
                                        (not top or len(operator_stack))
                                    ):
                                        raise Exception("Assignment \
expression is a command, not an operator, so it must be at top level")
                                    if op == "=":
                                        is_eq = True
                                    prefix = can_prefix and op in prefix_prec
                                    precedence = prefix_prec[op] if prefix else infix_prec[op]
                                    if not prefix:
                                        while (
                                            len(operator_stack) and (
                                                (operator_stack[-1] != "**" and precedences[-1] >= precedence) or
                                                precedences[-1] > precedence
                                            )
                                        ):
                                            precedences.pop()
                                            if is_prefix.pop():
                                                result += [[operator_stack.pop(), result.pop()]]
                                            else:
                                                right = result.pop()
                                                left = result.pop()
                                                result += [[left, operator_stack.pop(), right]]
                                    operator_stack += [item]
                                    precedences += [precedence]
                                    is_prefix += [prefix]
                                    if not prefix:
                                        can_prefix = True
                            
                            while len(operator_stack):
                                precedences.pop()
                                if is_prefix.pop():
                                    result += [[operator_stack.pop(), result.pop()]]
                                else:
                                    right = result.pop()
                                    left = result.pop()
                                    result += [[
                                        left,
                                        operator_stack.pop(),
                                        right
                                    ]]
                            
                            def collapse(item, top=False):
                                if top and is_eq and item[0][0][0] == "s":
                                    item[0], item[2] = item[2], item[0]
                                if all(not callable(el) for el in item):
                                    return item
                                if len(item) == 2:
                                    # prefix
                                    return item[0](collapse(item[1]))
                                return item[1](
                                    collapse(item[0]),
                                    collapse(item[2])
                                )
                            
                            return collapse(result[0], True)

                        result = shunt(top=True)
                        if not result:
                            success = False
                            break
                        
                        tokens += [processor[CT.Fix][0](result)]
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
                    if token == CT.EOF:
                        if index != len(code):
                            success = False
                            break
                    elif token == CT.String:
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
                                insert_endquote = False
                                index += 1
                                character = code[index]
                                while character != "”":
                                    index += 1
                                    if index >= len(code):
                                        insert_endquote = True
                                        break
                                    character = code[index]
                                if index < len(code):
                                    index += 1
                                tokens += processor[token][0]([
                                    Decompressed(
                                        code[old_index:index] +
                                        "”" * insert_endquote
                                    )
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
                    elif token == CT.Number:
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
                    elif token == CT.Name:
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
                if code[old_index:index].lower() == token.lower():
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
            return (
                (processor[grammar][lexeme_index](tokens), index, lexeme_index)
                if return_lexeme_index else
                (processor[grammar][lexeme_index](tokens), index)
            )
        lexeme_index += 1
    return ((
        parse_trace
        if not parse_index or parse_index == original_index else
        (
            ["%s: %s" % (
                CTNames[grammar],
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
    grammar=CT.Program,
    grammars=UnicodeGrammars,
    processor=ASTProcessor,
    whitespace=False,
    normal_encoding=False,
    verbose=False,
    grave=False,
    silent=False
):
    """
    Parse(code, grammar=CT.Program, \
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
            return processor[CT.Program][-1]([])
        if parsed:
            code = StringifyCode(parsed[0])
        else:
            print("RuntimeError: Could not parse")
            sys.exit(1)
    elif grave:
        code = Degrave(code)
    result = ParseExpression(code, 0, grammar, grammars, processor)
    if not result:
        return result
    if result[1] is False and not silent:
        PrintParseTrace(result[0])
    return (
        processor[CT.Program][-1]([])
        if result[1] is False else
        result[0]
    )


def PrintParseTrace(trace):
    if not isinstance(trace, list):
        warn("Parsing failed")
    else:
        warn("""\
Parsing failed, parse trace:
%s""" % ("\n".join(trace)))


def PrintTree(tree, padding="", print=warn):
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
                if item:
                    print(new_padding + item[0])
                    PrintTree(item, new_padding, print)
            else:
                if isinstance(item, str):
                    print(new_padding + repr(item)[1:-1])
                else:
                    print(new_padding + str(item))
        new_padding = padding + "└"
        item = tree[-1]
        if isinstance(item, list):
            print(new_padding + item[0])
            PrintTree(item, new_padding, print)
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
    new_inputs = []
    if inputs:
        try:
            new_inputs = literal_eval(inputs)
            if not isinstance(new_inputs, list):
                raise Exception()
        except:
            new_inputs = (
                inputs.split("\n") if "\n" in inputs else inputs.split(" ")
            )
    return new_inputs


def Run(
    code,
    inputs="",
    charcoal=None,
    grammar=CT.Program,
    grammars=UnicodeGrammars,
    whitespace=False,
    normal_encoding=False,
    verbose=False,
    grave=False,
    silent=False
):
    """
    Run(code, inputs="", charcoal=None, grammar=CT.Program, \
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
    if grammar == CT.Program:
        return str(charcoal)
    return result


def GetProgram(
    code,
    inputs="",
    charcoal=None,
    grammar=CT.Program,
    grammars=UnicodeGrammars,
    whitespace=False,
    normal_encoding=False,
    verbose=False,
    grave=False
):
    """
    GetProgram(code, inputs="", charcoal=None, grammar=CT.Program, \
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
    return re.sub(r"``([\s\S])|`([\s\S])", lambda match: (
        {
            "`": "`", " ": "´", "4": "←", "8": "↑", "6": "→", "2": "↓",
            "7": "↖", "9": "↗", "3": "↘", "1": "↙", "#": "№", "<": "↶",
            ">": "↷", "r": "⟲", "j": "⪫", "s": "⪪", "c": "℅", "o": "℅",
            "f": "⌕", "v": "⮌", "[": "◧", "]": "◨", "=": "≡", "t": "⎇",
            "!": "‽", "&": "∧", "|": "∨", "l": "↧", "u": "↥", "_": "±",
            "+": "⊞", "-": "⊟", "\\": "“", "/": "”", "n": "⌊", "x": "⌈",
            "a": "⊙", "A": "⬤", "N": "¶", "R": "⸿", ";": "；", 
            "'": "″", "\"": "‴", "0": "➙", "5": "⧴", "?": "＆", ":": "｜"
        }[match.group(1)]
        if match.group(1) else
        UnicodeLookup[chr(ord(match.group(2)) + 128)]
        if match.group(2) != "\n" else "¶"
    ), code)


def TIOEncode(code, inp=None, args=None):
    sep = bytes((255,))
    state = bytes("charcoal", "utf-8") + sep + sep + bytes(code, "utf-8")
    if inp is not None:
        state += sep
        if isinstance(inp, list):
            if len(inp) == 0:
                inp = None
            elif len(inp) == 1:
                inp = inp[0]
            else:
                inp = repr(inp)
        if inp is not None:
            state += sep + bytes(inp, "utf-8")
    if args is not None and isinstance(args, list) and len(args):
        if inp is None:
            state += sep + bytes([])
        for arg in args:
            if arg != "--cg" and arg != "--ppcg":
                state += sep + bytes(arg, "utf-8")
    return "https://tio.run/##" + base64.b64encode(
        zlib.compress(state, 9)[2:-4]
    ).decode("ascii").replace("+", "@").replace("=", "")


def AddAmbiguityWarnings():
    """
    AddAmbiguityWarnings()

    Adds ambiguity warnings which are shown whenever the AST is printed.

    """
    ASTProcessor[CT.Monadic][4] = (
        lambda result: "Random [Warning: May be ambiguous]"
    )
    ASTProcessor[CT.Command][59] = lambda result: [
        "Refresh [Warning: May be ambiguous]", result[1]
    ]
    ASTProcessor[CT.Command][60] = lambda result: [
        "Refresh [Warning: May be ambiguous]"
    ]


def RemoveThrottle():
    """
    RemoveThrottle()

    Removes throttle for Dump.

    """
    InterpreterProcessor[CT.Command][100] = (
        lambda result: lambda charcoal: charcoal.DumpNoThrottle()
    )

# from https://gist.github.com/puentesarrin/6567480


def print_xxd(data):
    """
    print_xxd(data)

    Prints the xxd-style hexdump using Charcoal's codepage, \
given data in UTF-8.

    """
    array = []
    for original in data:
        ordinal = ord(original)
        if InCodepage(original):
            character = ReverseLookup.get(original, original)
            array.append(ord(character))
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
        "--rawinputfile", "--rif", type=str, nargs="?", default="",
        help="Path to raw input file."
    )
    parser.add_argument(
        "--inputfile", "--if", type=str, nargs="?", default="",
        help="Path to input file."
    )
    parser.add_argument(
        "--outputfile", "--of", type=str, nargs="?", default="",
        help="Path to file with expected output."
    )
    parser.add_argument(
        "--quiettesting", "--qt", action="store_true",
        help="Don't print output for each individual testcase."
    )
    parser.add_argument(
        "--canvasstep", "--cs", type=int, nargs="?", default=500,
        help="Change canvas step interval."
    )
    parser.add_argument(
        "--decode", "--de", action="store_true",
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
        "--onlyastify", "--oa", action="store_true", help="Print AST and exit."
    )
    parser.add_argument(
        "-p", "--prompt", action="store_true", help="Prompt for input."
    )
    parser.add_argument(
        "-r", "--repl", action="store_true",
        help="Open as REPL instead of interpreting."
    )
    parser.add_argument(
        "--restricted", "--rs", action="store_true",
        help="""Disable prompt input, REPL mode, \
non-raw file input and file output."""
    )
    parser.add_argument(
        "-w", "--whitespace", action="store_true",
        help="Ignore all whitespace unless prefixed by a ´."
    )
    parser.add_argument(
        "--Wambiguities", "--Wam", action="store_true",
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
        "--nothrottle", "--nt", action="store_true",
        help="Don't throttle Dump."
    )
    parser.add_argument(
        "--deverbosify", "--dv", action="store_true",
        help="Turn verbose code into normal code."
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Use verbose mode."
    )
    parser.add_argument(
        "--degrave", "--dg", action="store_true",
        help="Turn grave mode code into normal code."
    )
    parser.add_argument(
        "-g", "--grave", action="store_true", help="Use grave mode."
    )
    parser.add_argument(
        "-l", "--showlength", "--sl", action="store_true",
        help="Show the length of the code."
    )
    parser.add_argument(
        "-t", "--test", action="store_true", help="Run unit tests."
    )
    parser.add_argument(
        "--disablecompression", "--dc", action="store_true",
        help="Disable compression when deverbosifying."
    )
    parser.add_argument(
        "-x", "--hexdump", "--hd", action="store_true",
        help="Show the xxd hexdump of the code."
    )
    parser.add_argument(
        "--tioencode", "--te", action="store_true",
        help="Print a TIO link."
    )
    parser.add_argument(
        "--ppcg", "--cg", action="store_true",
        help="Output a PPCG-formatted post."
    )
    argv, info = parser.parse_args(), set()
    argv.repl = argv.repl or all(
        x in ["-g", "--grave", "-v", "--verbose"] for x in sys.argv[1:]
    )
    if argv.test:
        from test import CharcoalTests, RunTests
        RunTests()
        sys.exit()
    if argv.stepcanvas:
        info.add(Info.step_canvas)
    if argv.dumpcanvas:
        info.add(Info.dump_canvas)
    if argv.nothrottle:
        RemoveThrottle()
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
    verbose = code
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
        StringifierProcessor[CT.String][0] = lambda r: [("s", Escaped(r[0])), ("!", "s")]
    if argv.verbose or argv.deverbosify:
        code = ParseExpression(
            code, grammars=VerboseGrammars, processor=StringifierProcessor,
            verbose=True
        )[0]
        if (
            isinstance(code, list) and len(code) and
            not isinstance(code[0], tuple)
        ):
            warn(code)
            PrintParseTrace(code)
            sys.exit(1)
        code = StringifyCode(code)
        if argv.deverbosify:
            warn(code)
    if argv.grave or argv.degrave:
        code = Degrave(code)
        if argv.degrave:
            warn(code)
    elif argv.normalencoding or argv.decode:
        code = Decode(code)
        argv.normalencoding = False
        if argv.decode:
            warn(code)
    if argv.tioencode:
        print(TIOEncode("code"))
    if argv.showlength or argv.ppcg:

        def charcoal_length(character):
            ordinal = ord(character)
            if ordinal < 16512:
                return 3
            if ordinal < 2113664:
                return 4
            return 5
        length = 0
        for character in code:
            if InCodepage(character):
                length += 1
            else:
                length += charcoal_length(
                    ReverseLookup.get(character, character)
                )
        if argv.ppcg:
            def b36(n):
                r = ""
                while n:
                    r = "0123456789abcdefghijklmnopqrstuvwxyz"[n % 36] + r
                    n //= 36
                return r
            nonce = b36(int(now()*1000))
            warn("""\
# [Charcoal], %s byte%s

    %s

[Try it online!][TIO-%s]%s

[Charcoal]: https://github.com/somebody1234/Charcoal
[TIO-%s]: %s""" % (
    length, "" if len(code) == 1 else "s", code, nonce,
    " Link is to verbose version of code." if argv.verbose else "", nonce,
    TIOEncode(verbose, argv.input, sys.argv[4:])
))
        else:
            warn(
                "Charcoal, %i bytes: [`%s`](%s)" % (
                    length, re.sub("`", "\\`", code),
                    TIOEncode(verbose, argv.input, sys.argv[4:])
                )
            )
    if argv.hexdump:
        print_xxd(code)
        sys.exit()
    if argv.astify or argv.onlyastify and not argv.repl:
        warn("Program")
        result = Parse(
            code, whitespace=argv.whitespace,
            normal_encoding=argv.normalencoding
        )
        if isinstance(result, tuple) and isinstance(result[0], CT):
            warn("""\
Parsing failed, parsed:
%s

Parse trace:
%s
""" % (result[2], "".join()))
        else:
            PrintTree(result[0]())
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
                    code = StringifyCode(ParseExpression(
                        code, grammars=VerboseGrammars,
                        processor=StringifierProcessor, verbose=True
                    )[0])
                if argv.grave:
                    code = Degrave(code)
                if argv.astify:
                    print("Program")
                    PrintTree(Parse(
                        code, whitespace=argv.whitespace,
                        normal_encoding=argv.normalencoding
                    )[0](), print=print)
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
        if (
            not argv.stepcanvas and
            not argv.dumpcanvas and
            global_charcoal.print_at_end
        ):
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
