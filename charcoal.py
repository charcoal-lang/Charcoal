#!/usr/bin/python3

# TODO List:
# bresenham
# image to ascii
# RotateCopy, RotateOverlap and cursor movement for them
# separate string and int inputs
# possibly make deverbosify better

from direction import Direction, Pivot
from charcoaltoken import CharcoalToken
from charactertransformers import *
from directiondictionaries import *
from unicodegrammars import UnicodeGrammars
from verbosegrammars import VerboseGrammars
from astprocessor import ASTProcessor
from interpreterprocessor import InterpreterProcessor
from stringifierprocessor import StringifierProcessor
from codepage import UnicodeLookup, UnicodeCommands, InCodepage
from compression import Decompressed
from enum import Enum
import random
import re
import argparse
import os
import sys
import time
import ast

if os.name == "nt":

    try:
        from colorama import init
        init()

    except:
        print("""\
Please install the 'colorama' module ('pip install colorama'\n
 or 'pip3 install colorama') \
for the 'Refresh' command to work properly.""")


def CleanExecute(function, *args):
    try:
        return function(*args)

    except (KeyboardInterrupt, EOFError):
        sys.exit()


def Cleanify(function):
    return lambda *args: CleanExecute(function, *args)

old_input = input
input = Cleanify(old_input)
sleep = Cleanify(time.sleep)


def Sign(number):
    return 1 if number > 0 else -1 if number < 0 else 0


class Modifier(Enum):
    maybe = 1
    maybe_some = 2
    some = 3


class Info(Enum):
    prompt = 1
    is_repl = 2
    warn_ambiguities = 3
    step_canvas = 4


class Coordinates:
    def __init__(self):
        self.top = 0
        self.coordinates = [[]]

    def FillLines(self, y):
        if y > self.top + len(self.coordinates) - 1:
            self.coordinates += [[]] * (
                y - self.top - len(self.coordinates) + 1
            )

        elif y < self.top:
            self.coordinates = [[]] * (self.top - y) + self.coordinates
            self.top = y

    def Add(self, x, y):
        self.FillLines(y)
        self.coordinates[y - self.top] += [x]


class Scope:
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
            string += "%s: %s, " % (
                key,
                repr(value)
            )

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

class Charcoal:
    def __init__(
        self,
        inputs=[],
        info=set(),
        canvas_step=500,
        original_input=""
    ):
        self.x = self.y = self.top = 0
        self.lines = [""]
        self.indices = [0]
        self.lengths = [0]
        self.right_indices = [0]
        self.scope = Scope()
        self.hidden = Scope({
            "θ": "abcdefghijklmnopqrstuvwxyz",
            "η": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            "ζ": 10,
            "ε": ""
        })
        self.info = info
        self.original_input = original_input
        self.inputs = inputs
        self.direction = Direction.right
        self.background = " "
        self.bg_lines = []
        self.bg_line_number = self.bg_line_length = 0
        self.timeout_end = self.dump_timeout_end = 0
        self.background_inside = False
        self.canvas_step = canvas_step
        if Info.step_canvas in self.info:
            print("\033[2J")

    def __str__(self):
        left = min(self.indices)
        right = max(self.right_indices)
        string = ""
        bg_start = None

        if self.bg_lines:

            for i in range(len(self.lines)):
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
                                    self.top + i,
                                    bg_start,
                                    j
                                ) +
                                line[j:]
                            )
                            bg_start = None

                    if bg_start is not None:
                        line = (
                            line[:bg_start] +
                            self.BackgroundString(self.top + i, bg_start, j)
                        )

                string += (
                    self.BackgroundString(
                        self.top + i,
                        left,
                        self.indices[i]
                    ) +
                    line +
                    self.BackgroundString(
                        self.top + i,
                        self.right_indices[i],
                        right
                    ) +
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
                        self.background * (right - right_index) +
                        "\n"
                    )

            return string[:-1]

    def BackgroundString(self, y, start, end):
        bg_line = self.bg_lines[y % self.bg_line_number]
        index = start % self.bg_line_length
        bg_line = bg_line[index:] + bg_line[:index]
        length = end - start
        return (bg_line * (length // self.bg_line_length + 1))[:length]

    def Lines(self):
        left = min(self.indices)
        right = max(self.right_indices)

        self.background_inside = True

        return [
            "\000" * (index - left) +
            line +
            "\000" * (right - right_index)
            for line, index, right_index in zip(
                self.lines,
                self.indices,
                self.right_indices
            )
        ]

    def AddInputs(self, inputs):
        self.inputs += inputs

    def Trim(self):
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

    def Clear(self):
        self.x = self.y = self.top = 0
        self.lines = [""]
        self.indices = [0]
        self.lengths = [0]
        self.right_indices = [0]
        self.scope = Scope()
        self.hidden = Scope({
            "θ": "abcdefghijklmnopqrstuvwxyz",
            "η": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            "ζ": 10,
            "ε": ""
        })
        self.inputs = []
        self.direction = Direction.right
        self.background = " "
        self.bg_lines = []
        self.bg_line_number = self.bg_line_length = 0
        self.timeout_end = self.dump_timeout_end = 0
        self.background_inside = False

    def Get(self):
        y_index = self.y - self.top
        return self.lines[y_index][self.x - self.indices[y_index]]

    def Put(self, string):
        is_empty = True

        for character in string:
            if character != "\000":
                is_empty = False
                break

        if is_empty:
            return

        y_index = self.y - self.top
        x_index = self.indices[y_index]

        line = self.lines[y_index]

        delta_index = len(re.match("^\000*", line).group())
        line = re.sub("\000+$", "", line[delta_index:])

        if not line:
            length = len(string)
            self.lines[y_index] = string
            self.indices[y_index] = self.x
            self.lengths[y_index] = length
            self.right_indices[y_index] = self.x + length
            return

        start = self.x - delta_index - x_index
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
        self.right_indices[y_index] = (self.indices[y_index] + length)

    def FillLines(self):
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

    def PrintLine(
        self,
        directions,
        length,
        string="",
        multiprint=False,
        coordinates=False,
        move_at_end=True,
        multichar_fill=False
    ):
        old_x = self.x
        old_y = self.y
        string_is_empty = not string

        if coordinates is True:
            coordinates = Coordinates()

        for direction in directions:

            if string_is_empty:
                string = DirectionCharacters[direction]

            self.x = old_x
            self.y = old_y

            if (
                direction == Direction.right or
                direction == Direction.left
            ):
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

                    if character == "\000":
                        self.Move(direction)
                        continue

                    if coordinates:
                        coordinates.Add(self.x, self.y)

                    self.FillLines()
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
        multiprint=False,
        flags=0
    ):

        if isinstance(string, list):
            string = "\n".join(map(str, string))

        if isinstance(string, int):
            length, string = string, ""

        if not directions:
            directions = {self.direction}

        old_x = self.x
        old_y = self.y

        if not flags and length and "\n" not in string:
            self.PrintLine(directions, length, string, multiprint=multiprint)
            return

        lines = string.split("\n")

        for direction in directions:
            self.x = old_x
            self.y = old_y

            if direction == Direction.right:
                initial_x = self.x

                for line in lines:

                    if not re.match("^\000*$", line):
                        self.PrintLine({Direction.right}, len(line), line)

                    self.x = initial_x
                    self.y += 1

                self.y -= 1

                if lines[-1]:
                    self.Move(Direction.right, len(lines[-1]))

            elif direction == Direction.left:
                initial_x = self.x

                for line in lines:

                    if not re.match("^\000*$", line):
                        self.PrintLine({Direction.left}, len(line), line)

                    self.x = initial_x
                    self.y -= 1

                self.y += 1

                if lines[-1]:
                    self.Move(Direction.left, len(lines[-1]))

            else:
                newline_direction = NewlineDirection[direction]
                delta_x = XMovement[direction]
                delta_y = YMovement[direction]

                for line in lines[:-1]:
                    line_start_x = self.x
                    line_start_y = self.y

                    for character in line:

                        if character == "\000":
                            self.x += delta_x
                            self.y += delta_y
                            continue

                        self.FillLines()
                        self.Put(character)
                        self.x += delta_x
                        self.y += delta_y

                    self.x = line_start_x
                    self.y = line_start_y
                    self.Move(newline_direction)

                for character in lines[-1]:

                    if character == "\000":
                        self.x += delta_x
                        self.y += delta_y
                        continue

                    self.FillLines()
                    self.Put(character)
                    self.x += delta_x
                    self.y += delta_y

        if multiprint:
            self.x = old_x
            self.y = old_y

        if Info.step_canvas in self.info:
            self.RefreshFastText("Print", self.canvas_step)

    def Multiprint(self, string, directions):
        self.Print(string, directions, multiprint=True)

    def Polygon(self, sides, character, fill=True):
        multichar_fill = len(character) > 1

        if multichar_fill:
            lines = character.split("\n")
            character = "*"

        initial_x = self.x
        initial_y = self.y
        coordinates = Coordinates()

        for side in sides:
            self.PrintLine(
                {side[0]},
                side[1],
                character,
                coordinates=coordinates,
                move_at_end=False,
                multichar_fill=multichar_fill
            )

            if Info.step_canvas in self.info:
                self.RefreshFastText("Polygon side", self.canvas_step)

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
            # Can't be/shouldn't be autofilled
            return

        final_x = self.x
        final_y = self.y
        self.PrintLine(
            {direction},
            length,
            character,
            coordinates=coordinates,
            move_at_end=False,
            multichar_fill=multichar_fill
        )

        if Info.step_canvas in self.info:
            self.RefreshFastText("Polygon autoclose", self.canvas_step)

        self.y = coordinates.top

        if multichar_fill:
            number_of_lines = len(lines)
            line_length = max([len(line) for line in lines])
            lines = [
                line + "\000" * (line_length - len(line))
                for line in lines
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

    def Rectangle(self, width, height, character=None, flags=None):
        if not character:
            initial_x = self.x
            initial_y = self.y
            self.PrintLine({Direction.right}, width, "-", move_at_end=False)
            self.PrintLine({Direction.down}, height, "|", move_at_end=False)
            self.PrintLine({Direction.left}, width, "-", move_at_end=False)
            self.PrintLine({Direction.up}, height, "|", move_at_end=False)
            self.Put("+")
            self.x += width - 1
            self.Put("+")
            self.y += height - 1
            self.Put("+")
            self.x = initial_x
            self.Put("+")
            self.y = initial_y

        else:
            length = len(character)
            self.PrintLine(
                {Direction.down},
                height,
                character[(width - 1) % length:] +
                character[:(width - 1) % length],
                move_at_end=False
            )
            self.PrintLine(
                {Direction.left},
                width,
                character[(width + height - 2) % length:] +
                character[:(width + height - 2) % length],
                move_at_end=False
            )
            self.PrintLine(
                {Direction.up},
                height,
                character[(width * 2 + height - 3) % length:] +
                character[:(width * 2 + height - 3) % length],
                move_at_end=False
            )
            self.PrintLine(
                {Direction.right},
                width, character,
                move_at_end=False
            )

    def Fill(self, string):

        if self.Get() != "\000":
            return

        initial_x = self.x
        initial_y = self.y
        points = set()
        queue = [(self.y, self.x)]

        try:

            while len(queue):
                self.y, self.x = queue[0]

                while self.Get() == "\000":
                    self.Move(Direction.up)

                self.Move(Direction.down)
                queue = queue[1:]
                points.add((self.y, self.x))

                if (self.y, self.x - 1) not in points:
                    self.x -= 1

                    if self.Get() == "\000":
                        queue += [(self.y, self.x)]

                    self.x += 1

                if (self.y, self.x + 1) not in points:
                    self.x += 1

                    if self.Get() == "\000":
                        queue += [(self.y, self.x)]
                    self.x -= 1

                self.y += 1
                value = self.Get()

                while value == "\000":
                    points.add((self.y, self.x))
                    self.y += 1
                    value = self.Get()

        except:
            print("RuntimeError: Attempting to fill open area")

            if Info.is_repl not in self.info:
                sys.exit(1)

        points = list(points)
        points.sort()
        length = len(string)

        for i in range(len(points)):
            point = points[i]
            self.y, self.x = point
            character = string[i % length]
            if character != "\000":
                self.Put(character)

        self.x = initial_x
        self.y = initial_y

    def Move(self, direction, length=1):
        self.x += XMovement[direction] * length
        self.y += YMovement[direction] * length

    def Pivot(self, pivot, number=2):

        for i in range(number):
            self.direction = PivotLookup[pivot][self.direction]

    def Jump(self, x, y):
        self.x += x
        self.y += y

    def ReflectTransform(self, direction):
        self.Reflect(direction, True)

    def ReflectMirror(self, direction):
        self.ReflectCopy(direction, True)

    def ReflectCopy(self, direction, transform=False):

        if isinstance(direction, list):

            for direction_ in direction:
                self.ReflectCopy(direction_)

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
            self.x += (right - self.x) * 2 + 1
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
            self.y -= (self.top - self.y) * 2 + 1
            self.top -= len(self.lines) - 1
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
            self.y += (len(self.lines) - self.y) * 2 + 1
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

                for line, length, right_index in zip(
                    self.lines[::-1], self.lengths[::-1], self.right_indices[::-1]
                ):
                    self.x += 1
                    self.y = bottom_right - right_index
                    self.PrintLine({Direction.down}, length, line[::-1])

            self.x = bottom_right - initial_y - 1
            self.y = bottom_right - initial_x - 1

        if Info.step_canvas in self.info:
            self.RefreshFastText("Reflect copy", self.canvas_step)

    def ReflectOverlap(self, direction):

        if isinstance(direction, list):

            for direction_ in direction:
                self.ReflectOverlap(direction_)

            return

        finished = True

        if direction == Direction.left:
            left = min(self.indices)
            self.x -= (self.x - left) * 2
            self.lines = [
                (line[::-1] + "\000" * (index - left))[:-1] +
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
                ("\000" * (right - right_index) + line[::-1])[1:]
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
            self.lines = self.lines[:0:-1] + self.lines
            self.indices = self.indices[:0:-1] + self.indices
            self.lengths = self.lengths[:0:-1] + self.lengths
            self.right_indices = self.right_indices[:0:-1] + self.right_indices

        elif direction == Direction.down:
            self.y += (len(self.lines) - self.y) * 2
            self.lines += self.lines[-2::-1]
            self.indices += self.indices[-2::-1]
            self.lengths += self.lengths[-2::-1]
            self.right_indices += self.right_indices[-2::-1]

        else:
            finished = False

        if finished:
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
            self.x = x + 1

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
                (y - x, i - x + 1)
                for x, y, i in zip(
                    self.right_indices,
                    range(self.top, self.top + len(self.right_indices)),
                    range(len(self.right_indices))
                )
            )
            x = -negative_x
            self.x = x - 1

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
                (y - x, x - i)
                for x, y, i in zip(
                    self.indices,
                    range(self.top, self.top + len(self.indices)),
                    range(len(self.indices))[::-1]
                )
            )
            x = x
            self.x = x + 1

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
                (x + y, -x + i + 1)
                for x, y, i in zip(
                    self.right_indices,
                    range(self.top, self.top + len(self.right_indices)),
                    range(len(self.right_indices))[::-1]
                )
            )
            x = -negative_x
            self.x = x - 1

            for line, length, right_index in zip(
                self.lines[::-1], self.lengths[::-1], self.right_indices[::-1]
            ):
                self.x += 1
                self.y = bottom_right - right_index
                self.PrintLine({Direction.down}, length, line[::-1])

            self.x = bottom_right - initial_y - 1
            self.y = bottom_right - initial_x - 1

        if Info.step_canvas in self.info:
            self.RefreshFastText("Reflect overlap", self.canvas_step)

    def Reflect(self, direction, transform=False):
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
            self.RefreshFastText("Reflect", self.canvas_step)

    def RotateTransform(self, rotations):
        self.Rotate(rotations, True)

    def RotateCopy(self, rotations, anchor=Direction.down_right):

        if isinstance(rotations, list):

            for rotation in rotations:
                self.RotateCopy(rotation, anchor)

            return

        if rotations % 2:
            print("RuntimeError: Cannot rotate an odd number of times")

            if Info.is_repl not in self.info:
                sys.exit(1)

        initial_x = self.x
        initial_y = self.y

        if rotations == 2:


            if anchor == Direction.down_right:
                right = max(self.right_indices)
                bottom = self.top + len(self.lines)
                self.x = right
                for line, length, right_index in zip(
                    self.lines[::-1],
                    self.lengths[::-1],
                    self.right_indices[::-1]
                ):
                    self.x -= 1
                    self.y = bottom + right - right_index
                    self.PrintLine({Direction.down}, length, line[::-1])

        elif rotations == 4:

            if anchor == Direction.down_right:
                right = max(self.right_indices)
                bottom = self.top + len(self.lines)
                self.y = bottom - 1
                for line, length, right_index in zip(
                    self.lines[::-1],
                    self.lengths[::-1],
                    self.right_indices[::-1]
                ):
                    self.x = right * 2 - right_index
                    self.y += 1
                    self.PrintLine({Direction.right}, length, line[::-1])

        elif rotations == 6:

            if anchor == Direction.down_right:
                right = max(self.right_indices)
                bottom = self.top + len(self.lines)
                self.x = right - 1
                for line, length, index in zip(
                    self.lines[::-1], self.lengths[::-1], self.indices[::-1]
                ):
                    self.x += 1
                    self.y = bottom - right + index
                    self.PrintLine({Direction.down}, length, line)

        if Info.step_canvas in self.info:
            self.RefreshFastText("Rotate copy", self.canvas_step)

        pass

    def RotateOverlap(self, rotations, anchor=Direction.down_right):

        if isinstance(rotations, list):

            for rotation in rotations:
                self.RotateOverlap(rotation, anchor)

            return

        # TODO

        if Info.step_canvas in self.info:
            self.RefreshFastText("Rotate overlap", self.canvas_step)

    def Rotate(self, rotations, transform=False):
        rotations %= 8

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

            self.top = left
            self.x, self.y = -self.y, self.x

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

        if Info.step_canvas in self.info:
            self.RefreshFastText("Rotate", self.canvas_step)

    def Copy(self, delta_x, delta_y):
        initial_x = self.x
        initial_y = self.y

        self.y = self.top + delta_y
        for line, index in zip(self.lines[:], self.indices[:]):
            self.FillLines()
            self.x = index + delta_x
            self.Put(line)
            self.y += 1

        self.x = initial_x
        self.y = initial_y

        if Info.step_canvas in self.info:
            self.RefreshFastText("Copy", self.canvas_step)

    def GetFreeVariable(self):

        for character in "ικλμνξπρςστυφχψωαβγδεζηθ":

            if character not in self.scope:
                return character

    def For(self, expression, body):

        if not expression:

            if len(self.inputs):
                expression = self.inputs[0]
                self.inputs = self.inputs[1:]

            else:
                pass
                # TODO

        self.scope = Scope(self.scope)
        loop_variable = self.GetFreeVariable()
        variable = expression(self)

        if isinstance(variable, int):
            variable = range(variable)

        for item in variable:
            self.scope[loop_variable] = item
            body(self)

        self.scope = self.scope.parent

    def While(self, condition, body):
        self.scope = Scope(self.scope)
        loop_variable = self.GetFreeVariable()
        self.scope[loop_variable] = condition(self)

        while self.scope[loop_variable]:
            body(self)
            self.scope[loop_variable] = condition(self)

        self.scope = self.scope.parent

    def If(self, condition, if_true, if_false):

        if condition(self):
            if_true(self)

        else:
            if_false(self)

    def Cast(self, variable):
        if isinstance(variable, list):
            return [self.Cast(item) for item in variable]

        if isinstance(variable, str):
            return int(variable)

        if isinstance(variable, int):
            return str(variable)

    def Random(self, variable=1):
        if variable == 1 and Info.warn_ambiguities in self.info:
            print("""\
Warning: Possible ambiguity, make sure you explicitly use 1 if needed""")

        if isinstance(variable, int):
            return random.randrange(variable)

        elif isinstance(variable, list) or isinstance(variable, str):
            return random.choice(variable)

    def Assign(self, key, value):
        self.scope[key] = value

    def InputString(self, key=""):
        result = ""

        if len(self.inputs):
            result = self.inputs[0]
            self.inputs = self.inputs[1:]

        elif Info.prompt in self.info:
            result = input("Enter string: ")

        if key:
            self.scope[key] = result

        else:
            return result

    def InputNumber(self, key=""):
        result = 0

        if len(self.inputs):

            try:
                result = int(self.inputs[0])

            except:
                result = 0

            self.inputs = self.inputs[1:]

        elif Info.prompt in self.info:

            try:
                result = int(input("Enter number: "))

            except:
                result = 0

        if key:
            self.scope[key] = result

        else:
            return result

    def Dump(self):
        sleep(max(0, self.dump_timeout_end - time.clock()))
        print(self)
        self.dump_timeout_end = time.clock() + .01

    def DumpNoThrottle(self):
        print(self)

    def Refresh(self, timeout=0):
        if not isinstance(timeout, int):
            print(
                "RuntimeError: Refresh expected int, found %s" %
                str(timeout)
            )

            if Info.is_repl not in self.info:
                sys.exit(1)

        elif timeout == 0 and Info.warn_ambiguities in self.info:
            print("""\
Warning: Possible ambiguity, \
make sure you explicitly use 0 for no delay if needed""")

        sleep(max(0, self.timeout_end - time.clock()))
        print("\033[0;0H" + str(self))
        self.timeout_end = time.clock() + timeout / 1000

    def RefreshFast(self, timeout=0):
        sleep(max(0, self.timeout_end - time.clock()))
        print("\033[0;0H" + str(self))
        self.timeout_end = time.clock() + timeout / 1000

    def RefreshFastText(self, text, timeout=0):
        sleep(max(0, self.timeout_end - time.clock()))
        print("\033[0;0H\033[2K" + text + "\n" + str(self))
        self.timeout_end = time.clock() + timeout / 1000

    def RefreshFor(self, timeout, variable, body):
        print("\033[2J")
        timeout /= 1000
        self.scope = Scope(self.scope)
        loop_variable = self.GetFreeVariable()
        variable = variable(self)

        if isinstance(variable, int):
            variable = range(variable)

        for item in variable:
            self.timeout_end = time.clock() + timeout
            self.scope[loop_variable] = item
            body(self)
            self.RefreshFast()

        self.scope = self.scope.parent

    def RefreshWhile(self, timeout, condition, body):
        print("\033[2J")
        timeout /= 1000
        self.scope = Scope(self.scope)
        loop_variable = self.GetFreeVariable()
        self.scope[loop_variable] = condition(self)

        while self.scope[loop_variable]:
            self.timeout_end = time.clock() + timeout
            body(self)
            self.RefreshFast()
            self.scope[loop_variable] = condition(self)

        self.scope = self.scope.parent

    def Evaluate(self, code, is_command=False):
        if is_command:
            Run(code, charcoal=self)
            return

        return Run(code, grammar=CharcoalToken.Expression)

    def CycleChop(self, iterable, length):
        if isinstance(iterable, int):
            iterable, length = length, iterable

        if isinstance(length, list) or isinstance(length, str):
            length = len(length)

        return (iterable * (length // len(iterable) + 1))[:length]

    def Crop(self, width, height):
        top_crop = max(0, self.y - self.top)
        bottom_crop = min(len(self.lines), top_crop + height)
        self.lines = self.lines[top_crop:bottom_crop]
        self.indices = self.indices[top_crop:bottom_crop]
        self.lengths = self.lengths[top_crop:bottom_crop]
        self.right_indices = self.right_indices[top_crop:bottom_crop]
        self.y = 0

        for i in range(len(self.lines)):
            left_crop = max(0, self.x - self.indices[i])
            right_crop = min(self.lengths[i], left_crop + width)
            length = self.lengths[i]
            self.lines[i] = self.lines[i][left_crop:right_crop]
            self.indices[i] += left_crop
            self.lengths[i] -= left_crop - right_crop + length
            self.right_indices[i] += right_crop - length

    def Extend(self, horizontal=0, vertical=0):
        horizontal += 1
        vertical += 1

        if horizontal:
            self.background_inside = True
            joiner = "\x00" * (horizontal - 1)
            self.lines = [joiner.join(line) for line in self.lines]
            self.lengths = [
                (length - 1) * horizontal + 1
                for length in self.lengths
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

    def RunFunction(self, function, arguments):
        self.scope = Scope(self.scope)

        for argument in arguments:
            self.scope[self.GetFreeVariable()] = argument

        function(self)

        self.scope = self.scope.parent

    def Ternary(self, condition, if_true, if_false):

        if condition(self):
            return if_true(self)

        else:
            return if_false(self)

    def GetAt(self, x, y):
        y_index = y - self.top

        if y_index < 0 or y_index >= len(self.lines):
            return ""

        line = self.lines[y_index]
        x_index = x - self.indices[y_index]

        if x_index < 0 or x_index >= self.lengths[y_index]:
            return ""

        return line[x_index]

    def Peek(self):
        return self.GetAt(self.x, self.y)

    def PeekLine(self, direction=None, length=1):

        if not direction:
            direction = self.direction

        x = self.x
        y = self.y
        delta_x += XMovement[direction]
        delta_y += YMovement[direction]
        result = []

        for i in range(length):
            result += [self.GetAt(x, y)]
            x += delta_x
            y += delta_y

        return result

def PassThrough(result):
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
    original_index = index
    lexeme_index = 0

    for lexeme in grammars[grammar]:
        success = True
        index = original_index
        tokens = []

        for token in lexeme:

            if verbose:

                while index < len(code) and code[index] in "\r\n\t ":
                    index += 1

                next_chars = code[index:index + 2]

                while next_chars == "//" or next_chars == "/*":
                    index += 2

                    if next_chars == "//":

                        while code[index] not in "\r\n":
                            index += 1

                        if code[index - 1:index + 1] == "\r\n":
                            # It's a MS newline
                            index += 1

                    else:

                        while code[index] != "*" and code[index + 1] != "/":
                            index += 1

                        index += 2

                    next_chars = code[index:index + 2]

            if isinstance(token, CharcoalToken):

                if verbose:

                    if token == CharcoalToken.String:

                        quote = code[index]

                        if (
                            index == len(code) or
                            (quote != "\"" and quote != "'")
                        ):
                            success = False
                            break

                        old_index = index
                        index += 1
                        character = code[index]

                        if quote == "\"":

                            while character != "\"":
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

                        tokens += processor[token][0]([ast.literal_eval(
                            code[old_index:index]
                        )])

                    elif token == CharcoalToken.Number:

                        if index == len(code):
                            success = False
                            break

                        old_index = index
                        character = code[index]
                        result = 0

                        while character >= "0" and character <= "9":
                            index += 1

                            if index == len(code):
                                character = ""
                            else:
                                character = code[index]

                        if old_index == index:
                            success = False
                            break

                        tokens += processor[token][0]([int(code[old_index:index])])

                    elif token == CharcoalToken.Name:

                        if index == len(code):
                            success = False
                            break

                        character = code[index]

                        if character in "abgdezhciklmnxprstufko":
                            tokens += processor[token][0]([character])
                            index += 1

                        else:
                            success = False
                            break

                    else:
                        result = ParseExpression(
                            code,
                            index,
                            token,
                            grammars,
                            processor,
                            verbose
                        )

                        if not result:
                            success = False
                            break

                        tokens += [result[0]]
                        index = result[1]

                else:

                    if token == CharcoalToken.String:

                        if index == len(code):
                            success = False
                            break

                        old_index = index
                        character = code[index]

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
                            r"´(.)",
                            r"\1",
                            re.sub(
                                r"(^|[^´])¶",
                                r"\1\n",
                                re.sub(
                                    r"(^|[^´])¶",
                                    r"\1\n",
                                    code[old_index:index]
                                )
                            )
                        )])

                    elif token == CharcoalToken.Number:

                        if index == len(code):
                            success = False
                            break

                        old_index = index
                        character = code[index]
                        result = 0

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
                            character >= "α" and
                            character <= "ω" and
                            character != "ο"
                        ):
                            tokens += processor[token][0]([character])
                            index += 1

                        else:
                            success = False
                            break

                    else:
                        result = ParseExpression(
                            code,
                            index,
                            token,
                            grammars,
                            processor,
                            verbose
                        )

                        if not result:
                            success = False
                            break

                        tokens += [result[0]]
                        index = result[1]

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

        if success:
            return (processor[grammar][lexeme_index](tokens), index)

        lexeme_index += 1

    return False


def Parse(
    code,
    grammar=CharcoalToken.Program,
    grammars=UnicodeGrammars,
    processor=ASTProcessor,
    whitespace=False,
    normal_encoding=False,
    verbose=False
):
    if normal_encoding:
        code = "".join([
            UnicodeLookup[character] if
            character in UnicodeLookup else
            character
            for character in code
        ])

    if whitespace:
        code = re.sub(
            r"(´\s)?\s*",
            lambda match: match.group(1)[1] if match.group(1) else "",
            code
        )

    if verbose:
        parsed = ParseExpression(
            code,
            grammar=grammar,
            grammars=VerboseGrammars,
            processor=StringifierProcessor,
            verbose=True
        )

        if parsed:
            code = parsed[0]

        else:
            print("RuntimeError: Could not parse")
            sys.exit(1)

    code += "»" * code.count("«")
    result = ParseExpression(
        code,
        grammar=grammar,
        grammars=grammars,
        processor=processor
    )

    if not result:
        return result

    return result[0]


def PrintTree(tree, padding=""):
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
    new_inputs = inputs

    try:
        new_inputs = list(map(str, ast.literal_eval(inputs)))

        if not isinstance(new_inputs, list):
            raise Exception()

    except:

        new_inputs = (
            inputs.split("\n") if
            "\n" in inputs else
            inputs.split(" ")
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
    verbose=False
):
    inputs = ProcessInput(inputs)

    if not charcoal:
        charcoal = Charcoal(inputs)

    else:
        charcoal.AddInputs(inputs)

    result = Parse(
        code,
        whitespace=whitespace,
        grammar=grammar,
        grammars=grammars,
        processor=InterpreterProcessor,
        normal_encoding=normal_encoding,
        verbose=verbose
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
    verbose=False
):
    result = Parse(
        code,
        whitespace=whitespace,
        grammar=grammar,
        grammars=grammars,
        processor=InterpreterProcessor,
        normal_encoding=normal_encoding,
        verbose=verbose
    )

    return result


def AddAmbiguityWarnings():
    ASTProcessor[CharcoalToken.Monadic][4] = (
        lambda result: "Random [Warning: May be ambiguous]"
    )
    ASTProcessor[CharcoalToken.Command][-2] = lambda result: [
        "Refresh [Warning: May be ambiguous]",
        result[1]
    ]
    ASTProcessor[CharcoalToken.Command][-1] = lambda result: [
        "Refresh [Warning: May be ambiguous]"
    ]


def RemoveThrottle():
    InterpreterProcessor[-5] = (
        lambda result: lambda charcoal: charcoal.DumpNoThrottle()
    )

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
        "-e", "--normalencoding", action="store_true",
        help="Use custom codepage."
    )
    parser.add_argument(
        "-a", "--astify", action="store_true",
        help="Print AST."
    )
    parser.add_argument(
        "-oa", "--onlyastify", action="store_true",
        help="Print AST and exit."
    )
    parser.add_argument(
        "-p", "--prompt", action="store_true",
        help="Prompt for input."
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
        help="Run unit tests."
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
        "-v", "--verbose", action="store_true",
        help="Use verbose mode."
    )
    parser.add_argument(
        "-sl", "--showlength", action="store_true",
        help="Show the length of the code."
    )
    parser.add_argument(
        "-t", "--test", action="store_true",
        help="Run unit tests."
    )
    argv = parser.parse_args()
    info = set()

    argv.repl = argv.repl or len(sys.argv) == 1

    if argv.test:
        from test import CharcoalTests, RunTests
        RunTests()
        sys.exit()

    if argv.stepcanvas:
        info.add(Info.step_canvas)

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

        if os.path.isfile(argv.file):
            with open(argv.file) as file:
                code = file.read()

        else:
            with open(argv.file + ".cl") as file:
                    code = file.read()

    if argv.rawinputfile:
        with open(argv.rawinputfile) as file:
            argv.input = [file.read()] + argv.input

    if not argv.restricted and argv.inputfile:
        with open(argv.inputfile) as file:
            raw_file_input = file.read()

        try:
            file_input = list(map(str, ast.literal_eval(raw_file_input)))

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
            file_output = list(map(str, ast.literal_eval(raw_file_output)))

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

    if argv.verbose or argv.deverbosify:
        code = re.sub(
            r"»+$",
            "",
            ParseExpression(
                code,
                grammars=VerboseGrammars,
                processor=StringifierProcessor,
                verbose=True
            )[0]
        )

        if argv.deverbosify:
            print(code)

    if argv.showlength:
        length = 0

        for character in code:

            if InCodepage(character):
                length += 1

            else:
                length += len(bytes(character, 'utf-8'))

        print("Charcoal, %i bytes: `%s`" % (
            length,
            re.sub("`", "\`", code)
        ))

    if argv.astify or argv.onlyastify and not argv.repl:
        print("Program")
        PrintTree(Parse(
            code,
            whitespace=argv.whitespace,
            normal_encoding=argv.normalencoding
        ))

        if argv.onlyastify:
            sys.exit()

    if argv.deverbosify and not argv.verbose:
        sys.exit()

    global_charcoal = Charcoal(
        info=info,
        canvas_step=argv.canvasstep,
        original_input=argv.input
    )

    if argv.repl:

        while True:

            try:
                code = old_input("Charcoal> ")

                if argv.astify:
                    print("Program")
                    PrintTree(Parse(
                        code,
                        whitespace=argv.whitespace,
                        normal_encoding=argv.normalencoding
                    ))

                print(Run(
                    code,
                    (argv.input or [""])[0],
                    charcoal=global_charcoal,
                    whitespace=argv.whitespace,
                    normal_encoding=argv.normalencoding
                ))

            except KeyboardInterrupt:
                global_charcoal.Clear()
                print("\nCleared canvas")

            except EOFError:
                break

    elif len(argv.input) <= 1 and not len(argv.output):
        result = Run(
            code,
            argv.input[0] if len(argv.input) else "",
            charcoal=global_charcoal,
            whitespace=argv.whitespace,
            normal_encoding=argv.normalencoding
        )

        if not argv.stepcanvas:
            print(result)

    else:
        successes = failures = 0
        argv.input = [""] + [ProcessInput(inp) for inp in argv.input]
        argv.output = [""] + argv.output
        output_length = len(argv.output)
        test_charcoal = Charcoal()
        program = GetProgram(
            code,
            whitespace=argv.whitespace,
            normal_encoding=argv.normalencoding
        )

        if argv.quiettesting:

            for i in range(1, len(argv.input)):

                test_charcoal.Clear()
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

            for i in range(1, len(argv.input)):

                if i == next_padding:
                    padding += "="
                    next_padding *= 10

                test_charcoal.Clear()
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
                        success_padding[success],
                        i,
                        success_string[success],
                        success_padding[success]
                    ))

                else:
                    print("%s\nTest case %i:\n%s" % (padding, i, padding))

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
