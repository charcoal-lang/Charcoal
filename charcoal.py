#!/usr/bin/python3
# vim: set fileencoding=<encoding name> :

from charactertransformers import *
from enum import Enum
import random
import re
import argparse
import os

if not hasattr(__builtins__, "raw_input"):
    raw_input = input
    input = lambda prompt: eval(input(prompt))
if not hasattr(__builtins__, "basestring"):
    basestring = str


def Sign(number):
    return 1 if number > 0 else -1 if number < 0 else 0


class Modifier(Enum):
    maybe = 1
    maybe_some = 2
    some = 3


class Direction(Enum):
    left = 1
    up = 2
    right = 4
    down = 8
    up_left = 16
    up_right = 32
    down_left = 64
    down_right = 128


class Pivot(Enum):
    left = 1
    right = 2

class CharcoalToken(Enum):
    Arrow = 1
    Multidirectional = 2
    Side = 3
    Separator = 4
    String = 5
    Number = 6
    Name = 7

    Arrows = 11
    Sides = 12
    Expressions = 13

    List = 31

    Expression = 21
    Niladic = 22
    Monadic = 23
    Dyadic = 24

    Program = 51
    Command = 52
    Print = 53
    Body = 54
    Multiprint = 55
    Polygon = 56
    Rectangle = 57
    Move = 58
    Pivot = 59
    Jump = 60
    Rotate = 61
    Reflect = 62
    Copy = 63
    For = 64
    While = 65
    If = 66
    Assign = 67
    InputString = 68
    InputNumber = 69
    Fill = 70
    SetBackground = 71

class Info(Enum):
    prompt = 1
    is_repl = 2

XMovement = {
    Direction.left: -1,
    Direction.up: 0,
    Direction.right: 1,
    Direction.down: 0,
    Direction.up_left: -1,
    Direction.up_right: 1,
    Direction.down_left: -1,
    Direction.down_right: 1
}

YMovement = {
    Direction.left: 0,
    Direction.up: -1,
    Direction.right: 0,
    Direction.down: 1,
    Direction.up_left: -1,
    Direction.up_right: -1,
    Direction.down_left: 1,
    Direction.down_right: 1
}

NewlineDirection = {
    Direction.left: Direction.up,
    Direction.up: Direction.right,
    Direction.right: Direction.down,
    Direction.down: Direction.left,
    Direction.up_left: Direction.up_right,
    Direction.up_right: Direction.down_right,
    Direction.down_left: Direction.up_left,
    Direction.down_right: Direction.down_left
}

DirectionCharacters = {
    Direction.left: "-",
    Direction.up: "|",
    Direction.right: "-",
    Direction.down: "|",
    Direction.up_left: "\\",
    Direction.up_right: "/",
    Direction.down_left: "/",
    Direction.down_right: "\\"
}

PivotLookup = {
    Pivot.left: {
        Direction.left: Direction.down_left,
        Direction.up: Direction.up_left,
        Direction.right: Direction.up_right,
        Direction.down: Direction.down_right,
        Direction.up_left: Direction.left,
        Direction.up_right: Direction.up,
        Direction.down_left: Direction.down,
        Direction.down_right: Direction.right
    },
    Pivot.right: {
        Direction.left: Direction.up_left,
        Direction.up: Direction.up_right,
        Direction.right: Direction.down_right,
        Direction.down: Direction.down_left,
        Direction.up_left: Direction.up,
        Direction.up_right: Direction.right,
        Direction.down_left: Direction.left,
        Direction.down_right: Direction.down
    }
}

DirectionFromXYSigns = {
    -1: {
        -1: Direction.down_left,
        0: Direction.down,
        1: Direction.down_right
    },
    0: {
        -1: Direction.left,
        0: Direction.right, # actually any
        1: Direction.right
    },
    1: {
        -1: Direction.up_left,
        0: Direction.up,
        1: Direction.up_right
    }
}

DirectionFromXYSigns = {
    -1: {
        -1: Direction.up_left,
        0: Direction.left,
        1: Direction.down_left
    },
    0: {
        -1: Direction.up,
        0: Direction.right, # actually any
        1: Direction.down
    },
    1: {
        -1: Direction.up_right,
        0: Direction.right,
        1: Direction.down_right
    }
}


class Coordinates:
    def __init__(self):
        self.top = 0
        self.coordinates = [ [ ] ]


    def FillLines(self, y):
        if y > self.top + len(self.coordinates) - 1:
            self.coordinates += [ [ ] ] * (y - self.top - len(self.coordinates) + 1)

        elif y < self.top:
            self.coordinates = [ [ ] ] * (self.top - y) + self.coordinates


    def Add(self, x, y):
        self.FillLines(y)
        if y < self.top:
            self.top = y
        self.coordinates[y - self.top] += [ x ]


class Charcoal:
    def __init__(self, inputs=[], info=set()):
        self.x = self.y = self.top = 0
        self.lines = [ "" ]
        self.indices = [ 0 ]
        self.lengths = [ 0 ]
        self.right_indices = [ 0 ]
        self.old_top = 0
        self.old_lines = []
        self.old_indices = []
        self.most_recent = ""
        self.most_recent_x = 0
        self.most_recent_y = 0
        self.most_recent_directions = []
        self.scope = {}
        self.info = info
        self.inputs = inputs
        self.direction = Direction.right
        self.background = " "


    def __str__(self):
        left = min(self.indices)
        right = max(self.right_indices)
        string = ""
        for i in range(len(self.lines) - 1):
            line = self.lines[i]
            string += self.background * (self.indices[i] - left) + line + self.background * (right - self.right_indices[i]) + "\n"
        return string + self.background * (self.indices[-1] - left) + self.lines[-1] + self.background * (right - self.right_indices[-1]) + "\n"

    def Lines(self):
        left = min(self.indices)
        right = max(self.right_indices)
        return [ self.background * (self.indices[i] - left) + self.lines[i] + self.background * (right - self.right_indices[i]) for i in range(len(self.lines))]


    def Clear(self):
        self.x = self.y = self.top = 0
        self.lines = [ "" ]
        self.indices = [ 0 ]
        self.lengths = [ 0 ]
        self.right_indices = [ 0 ]


    def Get(self):
        y_index = self.y - self.top
        return self.lines[y_index][self.x - self.indices[y_index]]


    def Put(self, string):
        y_index = self.y - self.top
        x_index = self.indices[y_index]
        line = self.lines[y_index]
        start = self.x - x_index
        end = start + len(string)
        self.lines[y_index] = line[:start] + self.background * (start - len(line)) + string + self.background * -end + line[max(0, end):]
        self.lengths[y_index] = len(self.lines[y_index])
        self.right_indices[y_index] = x_index + len(self.lines[y_index])
        if self.x < x_index:
            self.indices[y_index] = self.x


    def FillLines(self):
        if self.y > self.top + len(self.lines) - 1:
            self.lines += [ "" ] * (self.y - self.top - len(self.lines) + 1)
            self.indices += [ 0 ] * (self.y - self.top - len(self.indices) + 1)
            self.lengths += [ 0 ] * (self.y - self.top - len(self.lengths) + 1)
            self.right_indices += [ 0 ] * (self.y - self.top - len(self.right_indices) + 1)

        elif self.y < self.top:
            self.lines = [ "" ] * (self.top - self.y) + self.lines
            self.indices = [ 0 ] * (self.top - self.y) + self.indices
            self.lengths = [ 0 ] * (self.top - self.y) + self.lengths
            self.right_indices = [ 0 ] * (self.top - self.y) + self.right_indices
            self.top = self.y


    def SetBackground(self, character):
        self.background = character[0]


    def PrintLine(self, directions, length, string="", multiprint=False, coordinates=False, move_at_end=True, record_horizontal=False): # overload
        # self.most_recent = string
        # self.most_recent_x = self.x
        # self.most_recent_y = self.y
        # self.most_recent_directions = directions
        old_x = self.x
        old_y = self.y
        string_is_empty = not string
        if coordinates == True:
            coordinates = Coordinates()

        for direction in directions:
            if string_is_empty:
                string = DirectionCharacters[direction]

            self.x = old_x
            self.y = old_y

            if direction == Direction.right or direction == Direction.left:
                self.FillLines()
                if direction == Direction.left:
                    self.x -= length - 1
                self.Put((string * (int(length / len(string)) + 1))[:length])
                if record_horizontal:
                    coordinates.Add(self.x, self.y)
                    coordinates.Add(self.x + length - 1, self.y)

            else:
                string_length = len(string)

                for i in range(length):
                    self.FillLines()
                    if coordinates:
                        coordinates.Add(self.x, self.y)
                    self.Put(string[i % string_length])
                    self.Move(direction)

                if not move_at_end:
                    self.Move(NewlineDirection[NewlineDirection[direction]])

        if multiprint:
            self.x = old_x
            self.y = old_y

        if coordinates:
            return coordinates


    def Print(self, string, directions=None, length=0, multiprint=False, flags=0):

        if not directions:
            directions = { self.direction }
        self.old_top = self.top
        self.old_lines = self.lines[:]
        self.old_indices = self.indices[:]

        old_x = self.x
        old_y = self.y

        if not flags and length and not "\n" in string:
            self.PrintLine(directions, length, string)
            return

        lines = string.split("\n")

        for direction in directions:
            self.x = old_x
            self.y = old_y

            if direction == Direction.right or direction == Direction.left:
                initial_x = self.x

                for line in lines:
                    self.FillLines()
                    self.Put(line)
                    self.x = initial_x
                    self.y += 1

                self.y -= 1
                if lines[-1]:
                    self.Move(direction)

            else:
                newline_direction = NewlineDirection[direction]

                for line in lines[:-1]:
                    line_start_x = self.x
                    line_start_y = self.y

                    for character in line:
                        self.FillLines()
                        self.Put(character)
                        self.Move(direction)

                    self.x = line_start_x
                    self.y = line_start_y
                    self.Move(newline_direction)

                for character in lines[-1]:
                    self.FillLines()
                    self.Put(character)
                    self.Move(direction)

                if lines[-1]:
                    self.Move(direction)

        if multiprint:
            self.x = old_x
            self.y = old_y


    def Multiprint(self, string, directions):
        self.Print(string, directions, multiprint=True)


    def Polygon(self, sides, character, fill=True):
        if not fill:
            self.Multiline(sides, character)
            return
        record_horizontal = len(character) > 1
        if record_horizontal:
            lines = character.split("\n")
            character = "!"
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
                record_horizontal=record_horizontal
            )
        delta_x = initial_x - self.x
        sign_x = Sign(delta_x)
        delta_y = initial_y - self.y
        sign_y = Sign(delta_y)
        direction = DirectionFromXYSigns[sign_x][sign_y]
        length = (delta_x or delta_y) * (sign_x or sign_y) + 1
        if delta_x and delta_y and delta_x * sign_x != delta_y * sign_y:
            # Can't be autofilled
            return
        final_x = self.x
        final_y = self.y
        self.PrintLine(
            {direction},
            length,
            character,
            coordinates=coordinates,
            move_at_end=False,
            record_horizontal=record_horizontal
        )
        self.y = coordinates.top
        if record_horizontal:
            number_of_lines = len(lines)
            line_length = max([len(line) for line in lines])
            lines = [line + self.background * (line_length - len(line)) for line in lines]
            for row in coordinates.coordinates:
                line = lines[self.y % number_of_lines]
                while row:
                    start, end = row[:2]
                    row = row[2:]
                    if start > end:
                        start, end = end, start
                    index = self.x % line_length
                    length = end - start + 1
                    self.x = start
                    self.PrintLine({Direction.right}, length, line[index:] + line[:index])
                self.y += 1
        else:
            for row in coordinates.coordinates:
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


    def Rectangle(self, width, height, character=None, flags=None):

        if not character:
            initial_x = self.x
            initial_y = self.y
            PrintLine({Direction.right}, width, "-", move_at_end=False)
            PrintLine({Direction.down}, height, "|", move_at_end=False)
            PrintLine({Direction.left}, width, "-", move_at_end=False)
            PrintLine({Direction.up}, height, "|", move_at_end=False)
            Put("+")
            self.x += width - 1
            Put("+")
            self.y += height - 1
            Put("+")
            self.x = initial_x
            Put("+")
            self.y = initial_y

        else:
            character = character[0]
            PrintLine({Direction.right}, width, character, move_at_end=False)
            PrintLine({Direction.down}, height, character, move_at_end=False)
            PrintLine({Direction.left}, width, character, move_at_end=False)
            PrintLine({Direction.up}, height, character, move_at_end=False)


    def Fill(self, string):
        if self.Get() != self.background:
            return
        initial_x = self.x
        initial_y = self.y
        points = set()
        queue = []
        # TODO: fill algorithm
        while self.Get() == self.background:
            self.Move(Direction.up)
        self.Move(Direction.down)

        while len(queue):
            self.y, self.x = queue[0]
            queue = queue[1:]
            points.add((self.y, self.x))

            if not (self.y, self.x - 1) in points:
                self.x -= 1

                if self.Get() == self.background:
                    queue += []

                self.x += 1

            if not (self.y, self.x + 1) in points:
                self.x += 1

                if self.Get() == self.background:
                    queue += []
                self.x -= 1

            self.y += 1
            value = self.Get()

            while value == self.background:
                points.add((self.y, self.x))
                self.y += 1
                value = self.Get()
        points = list(points)
        points.sort()
        length = len(string)

        print("pts", points)
        for i in range(len(points)):
            point = points[i]
            self.y, self.x = point
            Put(string[i % length])
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


    def Reflect(self, direction):
        # TODO
        pass


    def Rotate(self, number):
        number %= 8
        if not number:
            return
        left = min(self.indices)
        right = max(self.right_indices)
        self.top = -right
        if number == 2:
            lines = self.Lines()
            number_of_lines = len(lines[0])
            self.indices = [ self.top ] * number_of_lines
            self.lengths = [ len(lines) ] * number_of_lines
            self.right_indices = [ self.top + len(self.lines) ] * number_of_lines
            self.lines = [ "" * number_of_lines ]
            for i in range(number_of_lines):
                for line in lines:
                    self.lines += line[i]
            self.top = left
        elif number == 4:
            lines = self.Lines()
            number_of_lines = len(lines[0])
            [ self.right_indices, self.indices ] = [ [-index for index in self.indices], [-index for index in self.right_indices] ]
            self.lines = [ line[::-1] for line in self.lines]
        elif number == 6:
            lines = self.Lines()
            number_of_lines = len(lines[0])
            self.indices = [ self.top ] * number_of_lines
            self.lengths = [ len(lines) ] * number_of_lines
            self.right_indices = [ self.top + len(self.lines) ] * number_of_lines
            self.lines = [ "" ] * number_of_lines
            for i in range(number_of_lines):
                for j in range(len(lines)):
                    self.lines[i] += lines[j][number_of_lines - i - 1]
            self.top = left
        else:
            self.Move({
                1: Direction.up_right,
                3: Direction.down_right,
                5: Direction.down_left,
                7: Direction.up_left
            }[number], self.top)
            self.Move({
                1: Direction.up_left,
                3: Direction.up_right,
                5: Direction.down_right,
                7: Direction.down_left
            }[number], min(self.indices))
            string = str(self)
            self.Clear()
            self.Print(string, directions={{
                1: Direction.down_right,
                3: Direction.down_left,
                5: Direction.up_left,
                7: Direction.up_right
            }[number]})
        self.x = 0
        self.y = 0


    def Copy(self):
        # TODO
        pass


    def For(self, expression, body):
        loop_variable = ""
        for character in "ικλμνξπρςστυφχψωαβγδεζηθ":
            if not character in self.scope:
                loop_variable = character
                break
        variable = expression(self)
        if isinstance(variable, int):
            variable = range(variable)
        for item in variable:
            self.scope[loop_variable] = item
            body(self)


    def While(self, condition, body):
        loop_variable = ""
        for character in "ικλμνξπρςστυφχψωαβγδεζηθ":
            if not character in self.scope:
                loop_variable = character
                break
        self.scope[loop_variable] = condition(self)
        while self.scope[loop_variable]:
            body(self)
            self.scope[loop_variable] = condition(self)


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
        if isinstance(variable, int):
            return random.randrange(variable)
        elif isinstance(variable, list):
            return random.choice(variable)


    def Assign(self, key, value):
        self.scope[key] = value


    def InputString(self, key=""):
        result = ""
        if Info.prompt in self.info:
            result = raw_input("Enter string: ")
        elif len(self.inputs):
            result = self.inputs[0]
            self.inputs = self.inputs[1:]
        if key:
            self.scope[key] = result
        else:
            return result


    def InputNumber(self, key=""):
        result = 0
        if Info.prompt in self.info:
            result = int(raw_input("Enter number: "))
        elif len(self.inputs):
            result = int(self.inputs[0])
            self.inputs = self.inputs[1:]
        if key:
            self.scope[key] = result
        else:
            return result

def PassThrough(result):
    return result

UnicodeGrammars = {
    CharcoalToken.Arrow: [
        [ "←" ],
        [ "↑" ],
        [ "→" ],
        [ "↓" ],
        [ "↖" ],
        [ "↗" ],
        [ "↘" ],
        [ "↙" ]
    ],
    CharcoalToken.Multidirectional: [
        [ "+", CharcoalToken.Arrows ],
        [ "x", CharcoalToken.Arrows ],
        [ "*", CharcoalToken.Arrows ],
        [ CharcoalToken.Arrow, CharcoalToken.Arrows ]
    ],
    CharcoalToken.Side: [
        [ CharcoalToken.Arrow, CharcoalToken.Expression ]
    ],
    CharcoalToken.Separator: [
        [ "¦" ],
        [ ]
    ],

    CharcoalToken.Arrows: [
        [ CharcoalToken.Arrow, CharcoalToken.Arrows ],
        [ CharcoalToken.Arrow ]
    ],
    CharcoalToken.Sides: [
        [ CharcoalToken.Side, CharcoalToken.Sides ],
        [ CharcoalToken.Side ]
    ],
    CharcoalToken.Expressions: [
        [ CharcoalToken.Expression, CharcoalToken.Separator, CharcoalToken.Expressions ],
        [ CharcoalToken.Expression ]
    ],

    CharcoalToken.List: [
        [ "⟦", CharcoalToken.Expressions, "⟧" ]
    ],

    CharcoalToken.Expression: [
        [ CharcoalToken.Number ],
        [ CharcoalToken.String ],
        [ CharcoalToken.Name ],
        [ CharcoalToken.List ],
        [ CharcoalToken.Dyadic, CharcoalToken.Expression, CharcoalToken.Expression ],
        [ CharcoalToken.Monadic, CharcoalToken.Expression ],
        [ CharcoalToken.Niladic ]
    ],
    CharcoalToken.Niladic: [
        [ "𝓢" ],
        [ "𝓝" ],
        [ "‽" ]
    ],
    CharcoalToken.Monadic: [
        [ "⁻" ],
        [ "𝓛" ],
        [ "¬" ],
        [ "‽" ],
        [ "𝓘" ]
    ],
    CharcoalToken.Dyadic: [
        [ "⁺" ],
        [ "⁻" ],
        [ "×" ],
        [ "÷" ],
        [ "﹪" ],
        [ "⁼" ],
        [ "‹" ],
        [ "›" ],
        [ "∧" ],
        [ "∨" ]
    ],

    CharcoalToken.Program: [
        [ CharcoalToken.Command, CharcoalToken.Program ],
        [ ]
    ],
    CharcoalToken.Command: [
        [ CharcoalToken.InputString ],
        [ CharcoalToken.InputNumber ],
        [ CharcoalToken.Print ],
        [ CharcoalToken.Multiprint ],
        [ CharcoalToken.Polygon ],
        [ CharcoalToken.Rectangle ],
        [ CharcoalToken.Move ],
        [ CharcoalToken.Pivot ],
        [ CharcoalToken.Jump ],
        [ CharcoalToken.Rotate ],
        [ CharcoalToken.Reflect ],
        [ CharcoalToken.Copy ],
        [ CharcoalToken.For ],
        [ CharcoalToken.While ],
        [ CharcoalToken.If ],
        [ CharcoalToken.Assign ],
        [ CharcoalToken.Fill ],
        [ CharcoalToken.SetBackground ]
    ],
    CharcoalToken.Body: [
        [ "«", CharcoalToken.Program, "»" ],
        [ CharcoalToken.Command ]
    ],
    CharcoalToken.Print: [
        [ CharcoalToken.Arrow, CharcoalToken.Expression ],
        [ CharcoalToken.Expression ]
    ],
    CharcoalToken.Multiprint: [
        [ "𝓟", CharcoalToken.Multidirectional, CharcoalToken.Expression ]
    ],
    CharcoalToken.Rectangle: [
        [ "𝓡", CharcoalToken.Expression, CharcoalToken.Expression, CharcoalToken.Expression ]
    ],
    CharcoalToken.Polygon: [
        [ "𝓖", CharcoalToken.Sides, CharcoalToken.Expression ],
        [ "𝓖", CharcoalToken.Arrows, CharcoalToken.Expression, CharcoalToken.Expression ]
    ],
    CharcoalToken.Move: [
        [ CharcoalToken.Arrow ],
        [ "𝓜", CharcoalToken.Arrow ],
        [ "𝓜", CharcoalToken.Expression, CharcoalToken.Arrow ]
    ],
    CharcoalToken.Pivot: [
        [ "↶", CharcoalToken.Expression ],
        [ "↶" ],
        [ "↷", CharcoalToken.Expression ],
        [ "↷" ]
    ],
    CharcoalToken.Jump: [
        [ "𝓙", CharcoalToken.Expression, CharcoalToken.Expression ]
    ],
    CharcoalToken.Rotate: [
        [ "⟲", CharcoalToken.Expression ]
    ],
    CharcoalToken.Reflect: [
        # TODO: command character*
        [ CharcoalToken.Arrow ]
    ],
    CharcoalToken.Copy: [
        [ "𝓒", CharcoalToken.Expression, CharcoalToken.Expression ]
    ],
    CharcoalToken.For: [
        [ "𝓕", CharcoalToken.Expression, CharcoalToken.Body ]
    ],
    CharcoalToken.While: [
        [ "𝓦", CharcoalToken.Expression, CharcoalToken.Body ]
    ],
    CharcoalToken.If: [
        [ "¿", CharcoalToken.Expression, CharcoalToken.Body, CharcoalToken.Body ]
    ],
    CharcoalToken.Assign: [
        [ "𝓐", CharcoalToken.Name, CharcoalToken.Expression ]
    ],
    CharcoalToken.Fill: [
        [ "¤", CharcoalToken.Expression ]
    ],
    CharcoalToken.SetBackground: [
        [ "𝓤𝓑", CharcoalToken.Expression ]
    ],
    CharcoalToken.InputString: [
        [ "𝓢", CharcoalToken.Name ]
    ],
    CharcoalToken.InputNumber: [
        [ "𝓝", CharcoalToken.Name ]
    ]
}

ASTProcessor = {
    CharcoalToken.Arrow: [
        lambda result: "Left",
        lambda result: "Up",
        lambda result: "Right",
        lambda result: "Down",
        lambda result: "Up Left",
        lambda result: "Up Right",
        lambda result: "Down Right",
        lambda result: "Down Left"
    ],
    CharcoalToken.Multidirectional: [ PassThrough ] * len(UnicodeGrammars[CharcoalToken.Multidirectional]),
    CharcoalToken.Side: [
        lambda result: [ "Side" ] + result
    ],
    CharcoalToken.String: [
        lambda result: [ "String \"%s\"" % result[0] ]
    ],
    CharcoalToken.Number: [
        lambda result: [ "Number %s" % str(result[0]) ]
    ],
    CharcoalToken.Name: [
        lambda result: [ "Identifier %s" % str(result[0]) ]
    ],
    CharcoalToken.Separator: [
        lambda result: None
    ],

    CharcoalToken.Arrows: [
        lambda result: [ "Arrows", result[0] ] + result[1][1:],
        lambda result: [ "Arrows", result[0] ]
    ],
    CharcoalToken.Sides: [
        lambda result: [ "Sides", result[0] ] + result[1][1:],
        lambda result: [ "Sides", result[0] ]
    ],
    CharcoalToken.Expressions: [
        lambda result: [ "Expressions", result[0] ] + result[2][1:],
        lambda result: [ "Expressions", result[0] ]
    ],

    CharcoalToken.List: [
        lambda result: [ "List" ] + result[1][1:]
    ],

    CharcoalToken.Expression: [ lambda result: result[0] if len(result) == 1 else result ] * len(UnicodeGrammars[CharcoalToken.Expression]),
    CharcoalToken.Niladic: [
        lambda result: "Input String",
        lambda result: "Input Number",
        lambda result: "Random"
    ],
    CharcoalToken.Monadic: [
        lambda result: "Negative",
        lambda result: "Length",
        lambda result: "Not",
        lambda result: "Cast",
        lambda result: "Random"
    ],
    CharcoalToken.Dyadic: [
        lambda result: "Sum",
        lambda result: "Difference",
        lambda result: "Product",
        lambda result: "Quotient",
        lambda result: "Modulo",
        lambda result: "Equals",
        lambda result: "Less Than",
        lambda result: "Greater Than",
        lambda result: "And",
        lambda result: "Or"
    ],

    CharcoalToken.Program: [
        lambda result: [ "Program", result[0] ] + result[1][1:],
        lambda result: [ ]
    ],
    CharcoalToken.Command: [lambda result: result[0]] * len(UnicodeGrammars[CharcoalToken.Command]),
    CharcoalToken.Body: [
        lambda result: result[1],
        lambda result: result[0]
    ],
    CharcoalToken.Print: [
        lambda result: [ "Print" ] + result,
        lambda result: [ "Print" ] + result
    ],
    CharcoalToken.Multiprint: [
        lambda result: [ "Multiprint" ] + result,
    ],
    CharcoalToken.Polygon: [
        lambda result: [ "Polygon" ] + result[1:],
        lambda result: [ "Polygon" ] + result[1:] 
    ],
    CharcoalToken.Move: [
        lambda result: [ "Move" ] + result,
        lambda result: [ "Move" ] + result[1:],
        lambda result: [ "Move" ] + result[1:]
    ],
    CharcoalToken.Pivot: [
        lambda result: [ "Pivot Left", result[1] ],
        lambda result: [ "Pivot Left" ],
        lambda result: [ "Pivot Right", result[1] ],
        lambda result: [ "Pivot Right" ]
    ],
    CharcoalToken.Jump: [
        lambda result: [ "Jump" ] + result[1:]
    ],
    CharcoalToken.Rotate: [
        lambda result: [ "Reflect" ] + result[1:]
    ],
    CharcoalToken.Reflect: [
        lambda result: [ "Reflect" ] + result[1:]
    ],
    CharcoalToken.Copy: [
        lambda result: [ "Copy" ] + result[1:]
    ],
    CharcoalToken.For: [
        lambda result: [ "For" ] + result[1:]
    ],
    CharcoalToken.While: [
        lambda result: [ "While" ] + result[1:]
    ],
    CharcoalToken.If: [
        lambda result: [ "If" ] + result[1:]
    ],
    CharcoalToken.Assign: [
        lambda result: [ "Assign" ] + result[1:]
    ],
    CharcoalToken.Fill: [
        lambda result: [ "Fill" ] + result[1:]
    ],
    CharcoalToken.SetBackground: [
        lambda result: [ "SetBackground", result[1] ]
    ],
    CharcoalToken.InputString: [
        lambda result: [ "Input String", result[1] ]
    ],
    CharcoalToken.InputNumber: [
        lambda result: [ "Input Number", result[1] ]
    ]
}

InterpreterProcessor = {
    CharcoalToken.Arrow: [
        lambda result: Direction.left,
        lambda result: Direction.up,
        lambda result: Direction.right,
        lambda result: Direction.down,
        lambda result: Direction.up_left,
        lambda result: Direction.up_right,
        lambda result: Direction.down_right,
        lambda result: Direction.down_left
    ],
    CharcoalToken.Multidirectional: [
        lambda result: [ Direction.right, Direction.down, Direction.left, directio.up ] + result[1],
        lambda result: [ Direction.up_right, Direction.down_right, Direction.down_left, Direction.up_left ] + result[1],
        lambda result: [ Direction.right, Direction.down_right, Direction.down, Direction.down_left, Direction.left, Direction.up_left, Direction.up, Direction.up_right ] + result[1],
        lambda result: [ result[0] ] + result[1]
    ],
    CharcoalToken.Side: [
        lambda result: lambda charcoal: (result[0], result[1](charcoal))
    ],
    CharcoalToken.String: [
        lambda result: result
    ],
    CharcoalToken.Number: [
        lambda result: result
    ],
    CharcoalToken.Name: [
        lambda result: result
    ],
    CharcoalToken.Separator: [
        lambda result: None
    ],

    CharcoalToken.Arrows: [
        lambda result: [ result[0] ] + result[1],
        lambda result: [ result[0] ]
    ],
    CharcoalToken.Sides: [
        lambda result: lambda charcoal: [ result[0](charcoal) ] + result[1](charcoal),
        lambda result: lambda charcoal: [ result[0](charcoal) ]
    ],
    CharcoalToken.Expressions: [
        lambda result: lambda charcoal: [ result[0](charcoal) ] + result[2](charcoal),
        lambda result: lambda charcoal: [ result[0](charcoal) ]
    ],

    CharcoalToken.List: [
        lambda result: lambda charcoal: result[1](charcoal)
    ],

    CharcoalToken.Expression: [
        lambda result: lambda charcoal: result[0],
        lambda result: lambda charcoal: result[0],
        lambda result: lambda charcoal: charcoal.scope[result[0]],
        lambda result: lambda charcoal: result[1](charcoal),
        lambda result: lambda charcoal: result[0](result[1](charcoal), result[2](charcoal)),
        lambda result: lambda charcoal: result[0](result[1](charcoal)),
        lambda result: lambda charcoal: result[0]()
    ],
    CharcoalToken.Niladic: [
        lambda result: lambda: charcoal.InputString(),
        lambda result: lambda: charcoal.InputNumber(),
        lambda result: lambda: charcoal.Random()
    ],
    CharcoalToken.Monadic: [
        lambda result: lambda item: -item,
        lambda result: lambda item: len(item),
        lambda result: lambda item: int(not item),
        lambda result: lambda item: charcoal.Cast(item),
        lambda result: lambda item: charcoal.Random(item)
    ],
    CharcoalToken.Dyadic: [
        lambda result: lambda left, right: left + right,
        lambda result: lambda left, right: left - right,
        lambda result: lambda left, right: left * right,
        lambda result: lambda left, right: int(left / right),
        lambda result: lambda left, right: left % right,
        lambda result: lambda left, right: left == right,
        lambda result: lambda left, right: left < right,
        lambda result: lambda left, right: left > right,
        lambda result: lambda left, right: int(left and right),
        lambda result: lambda left, right: int(left or right)
    ],

    CharcoalToken.Program: [
        lambda result: lambda charcoal: [result[0](charcoal), result[1](charcoal)] and None,
        lambda result: lambda charcoal: None
    ],
    CharcoalToken.Command: [ lambda result: lambda charcoal: result[0](charcoal) ] * len(UnicodeGrammars[CharcoalToken.Command]),
    CharcoalToken.Body: [
        lambda result: lambda charcoal: result[1](charcoal),
        lambda result: lambda charcoal: result[0](charcoal)
    ],
    CharcoalToken.Print: [
        lambda result: lambda charcoal: charcoal.Print(result[1](charcoal), directions={result[0]}),
        lambda result: lambda charcoal: charcoal.Print(result[0](charcoal))
    ],
    CharcoalToken.Multiprint: [
        lambda result: lambda charcoal: charcoal.Multiprint(result[2](charcoal), directions=set(result[1]))
    ],
    CharcoalToken.Polygon: [
        lambda result: lambda charcoal: charcoal.Polygon(result[1](charcoal), result[2](charcoal)),
        lambda result: lambda charcoal: charcoal.Polygon([[(side, length) for side in result[1]] for length in [ result[2](charcoal)]][0], result[3](charcoal))
    ],
    CharcoalToken.Move: [
        lambda result: lambda charcoal: charcoal.Move(result[0]),
        lambda result: lambda charcoal: charcoal.Move(result[1]),
        lambda result: lambda charcoal: charcoal.Move(result[2], result[1](charcoal))
    ],
    CharcoalToken.Pivot: [
        lambda result: lambda charcoal: charcoal.Pivot(Pivot.left, result[1](charcoal)),
        lambda result: lambda charcoal: charcoal.Pivot(Pivot.left),
        lambda result: lambda charcoal: charcoal.Pivot(Pivot.right, result[1](charcoal)),
        lambda result: lambda charcoal: charcoal.Pivot(Pivot.right)
    ],
    CharcoalToken.Jump: [
        lambda result: lambda charcoal: charcoal.Jump(result[1](charcoal), result[2](charcoal))
    ],
    CharcoalToken.Rotate: [
        lambda result: lambda charcoal: charcoal.Rotate(result[1](charcoal))
    ],
    CharcoalToken.Reflect: [
        lambda result: lambda charcoal: charcoal.Reflect(result[1])
    ],
    CharcoalToken.Copy: [
        lambda result: lambda charcoal: charcoal.Copy(result[1](charcoal), result[2](charcoal))
    ],
    CharcoalToken.For: [
        lambda result: lambda charcoal: charcoal.For(result[1], result[2])
    ],
    CharcoalToken.While: [
        lambda result: lambda charcoal: charcoal.While(result[1], result[2])
    ],
    CharcoalToken.If: [
        lambda result: lambda charcoal: charcoal.If(result[1], result[2], result[3])
    ],
    CharcoalToken.Assign: [
        lambda result: lambda charcoal: charcoal.Assign(result[1], result[2](charcoal))
    ],
    CharcoalToken.Fill: [
        lambda result: lambda charcoal: charcoal.Fill(result[1](charcoal))
    ],
    CharcoalToken.SetBackground: [
        lambda result: lambda charcoal: charcoal.SetBackground(result[1](charcoal))
    ],
    CharcoalToken.InputString: [
        lambda result: lambda charcoal: charcoal.InputString(result[1])
    ],
    CharcoalToken.InputNumber: [
        lambda result: lambda charcoal: charcoal.InputNumber(result[1])
    ]
}

SuperscriptToNormal = {
    "⁰": 0,
    "¹": 1,
    "²": 2,
    "³": 3,
    "⁴": 4,
    "⁵": 5,
    "⁶": 6,
    "⁷": 7,
    "⁸": 8,
    "⁹": 9
}


def ParseExpression(
        code,
        index=0,
        grammar=CharcoalToken.Program,
        grammars=UnicodeGrammars,
        processor=ASTProcessor
    ):
    original_index = index

    lexeme_index = 0
    for lexeme in grammars[grammar]:
        success = True
        index = original_index
        tokens = [ ]

        for token in lexeme:

            if isinstance(token, CharcoalToken):
                if token == CharcoalToken.String:
                    if index == len(code):
                        success = False
                        break
                    old_index = index
                    character = code[index]

                    while character >= " " and character <= "~" or character == "¶":
                        index += 1
                        if index == len(code):
                            character = ""
                        else:
                            character = code[index]

                    if old_index == index:
                        success = False
                        break
                    tokens += processor[token][0]([ re.sub(r"¶", r"\n", code[old_index:index]) ])

                elif token == CharcoalToken.Number:

                    if index == len(code):
                        success = False
                        break
                    old_index = index
                    character = code[index]
                    result = 0

                    while character >= "⁴" and character <= "⁹" or character in ["⁰", "¹", "²", "³"]:
                        result = result * 10 + SuperscriptToNormal[character]
                        index += 1

                        if index == len(code):
                            character = ""
                        else:
                            character = code[index]

                    # if character == "·":
                    #     multiplier = 0.1
                    #     index += 1
                    #     character = code[index]

                    #     while character >= "⁴" and character <= "⁹" or character in ["⁰", "¹", "²", "³"]:
                    #         result += multiplier * SuperscriptToNormal[character]
                    #         index += 1
                    #         if index == len(code):
                    #             character = ""
                    #         else:
                    #             character = code[index]
                    #         multiplier /= 10

                    if old_index == index:
                        success = False
                        break
                    tokens += processor[token][0]([ result ])

                elif token == CharcoalToken.Name:

                    if index == len(code):
                        success = False
                        break
                    character = code[index]

                    if character >= "α" and character <= "ω":
                        tokens += processor[token][0]([ character ])
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
                        processor
                    )

                    if not result:
                        success = False
                        break
                    tokens += [ result[0] ]
                    index = result[1]

            elif isinstance(token, str):
                old_index = index
                index += len(token)

                if code[old_index:index] == token:
                    tokens += [ token ]
                else:
                    success = False
                    break

            else:
                pass # supposed to error

        if success:

            return (processor[grammar][lexeme_index](tokens), index)

        lexeme_index += 1

    return False


def Parse(
        code,
        grammars=UnicodeGrammars,
        processor=ASTProcessor,
        whitespace=False
    ):
    if whitespace:
        code = re.sub(
            r"(´)?(\s)",
            lambda match: match.group(2) if match.group(1) else "",
            code
        )
    code += "»" * (code.count("«") - code.count("»"))
    result = ParseExpression(
        code,
        grammars=grammars,
        processor=processor
    )
    if not result:
        return result
    return result[0]


def PrintTree(tree, padding=""):
    padding = re.sub(r"└$", r" ", re.sub(r"├$", r"│", padding))
    new_padding = padding + "├"

    if len(tree): # > 1:

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

# temporary, delete when integrated into main interpreter
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument("-f", "--file", type=str, nargs="*", default="", help="File path of the program.")
    parser.add_argument("-c", "--code", type=str, nargs="?", default="", help="Code of the program.")
    parser.add_argument("-i", "--input", type=str, nargs="?", default="", help="Input to the program.")
    parser.add_argument("-a", "--astify", action="store_true", help="Print AST.")
    parser.add_argument("-p", "--prompt", action="store_true", help="Prompt for input.")
    parser.add_argument("-r", "--repl", action="store_true", help="Open as REPL instead of interpreting.")
    parser.add_argument("-w", "--whitespace", action="store_true", help="Ignore all whitespace unless prefixed by a `.")
    parser.add_argument("-t", "--test", action="store_true", help="Run unit tests.")
    argv = parser.parse_args()
    info = set()
    if argv.prompt:
        info.add(Info.prompt)
    if argv.repl:
        info.add(Info.prompt)
        info.add(Info.is_repl)
    code = ""
    for path in argv.file:
        if os.path.isfile(argv.file[0]):
            with open(argv.file[0]) as file:
                code += file.read()
        else:
            with open(argv.file[0] + ".cl") as file:
                code += file.read()
    if argv.astify:
        print("Program")
        PrintTree(Parse(
            code,
            whitespace=argv.whitespace
        ))
    charcoal = Charcoal(info=info)
    # charcoal.inputs = eval(argv.input) # TODO: fix
    if argv.repl:
        while True:
            try:
                Parse(
                    input("Charcoal> "),
                    whitespace=argv.whitespace,
                    processor=InterpreterProcessor
                )(charcoal)
            except (KeyboardInterrupt, EOFError):
                pass
    else:
        Parse(code, processor=InterpreterProcessor)(charcoal)
        print(str(charcoal))