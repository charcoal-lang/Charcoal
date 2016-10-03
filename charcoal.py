# encoding: utf-8

# TODO: fix canvas expansion

from charactertransformers import *
from enum import Enum
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
    String = 4
    Number = 5
    Name = 6

    Arrows = 11
    Sides = 13

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
    Move = 57
    Pivot = 58
    Jump = 59
    Rotate = 60
    Reflect = 61
    Copy = 62
    For = 63
    While = 64
    If = 65
    Assign = 66
    InputString = 67
    InputNumber = 68

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

class Canvas:
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


    def __str__(self):
        left = min(self.indices)
        right = max(self.right_indices)
        string = ""
        for i in range(len(self.lines) - 1):
            line = self.lines[i]
            string += " " * (self.indices[i] - left) + line + " " * (right - self.right_indices[i]) + "\n"
        return string + " " * (self.indices[-1] - left) + self.lines[-1] + " " * (right - self.right_indices[-1]) + "\n"

    def Lines(self):
        left = min(self.indices)
        right = max(self.right_indices)
        return [ " " * (self.indices[i] - left) + self.lines[i] + " " * (right - self.right_indices[i]) for i in range(len(self.lines))]


    def Clear(self):
        self.x = self.y = self.top = 0
        self.lines = [ "" ]
        self.indices = [ 0 ]
        self.lengths = [ 0 ]
        self.right_indices = [ 0 ]


    def Put(self, string):
        y_index = self.y - self.top
        x_index = self.indices[y_index]
        line = self.lines[y_index]
        start = self.x - x_index
        end = start + len(string)
        self.lines[y_index] = line[:start] + " " * (start - len(line)) + string + " " * -end + line[max(0, end):]
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


    def PrintLine(self, directions, length, string="", multiprint=False): # overload
        self.most_recent = string
        self.most_recent_x = self.x
        self.most_recent_y = self.y
        self.most_recent_directions = directions[:]
        old_x = self.x
        old_y = self.y
        string_is_empty = not string

        for direction in directions:
            if string_is_empty:
                string = DirectionCharacters[direction]

            self.x = old_x
            self.y = old_y

            if direction == Direction.right or direction == Direction.left:
                self.FillLines()
                self.Put((string * int(length / len(string)))[:length])

            else:
                string_length = len(string)

                for i in range(length):
                    self.FillLines()
                    self.Put(string[i % string_length])
                    self.Move(direction)

        if multiprint:
            self.x = old_x
            self.y = old_y


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


    def Polygon(self, sides, character):
        if len(character) > 1:
            character = character[0]
        initial_x = self.x
        initial_y = self.y
        # TODO: draw polygon
        delta_x = initial_x - self.x
        sign_x = Sign(delta_x)
        delta_y = initial_y - self.y
        sign_y = Sign(delta_y)
        direction = DirectionFromXYSigns[sign_x][sign_y]
        length = (delta_x or delta_y) * (sign_x or sign_y)
        # TODO
        pass


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
        for character in "ικλμνξοπρςστυφχψωαβγδεζηθ":
            if not character in self.scope:
                loop_variable = character
        variable = expression(self)
        if isinstance(variable, int):
            variable = range(variable)
        for item in variable:
            self.scope[loop_variable] = item
            body(self)

    def While(self, condition, body):
        while expression(self):
            body(self)

    def If(self, condition, if_true, if_false):
        if condition(self):
            if_true(self)
        else:
            if_false(self)


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

    CharcoalToken.Arrows: [
        [ CharcoalToken.Arrow, CharcoalToken.Arrows ],
        [ ]
    ],
    CharcoalToken.Sides: [
        [ CharcoalToken.Side, CharcoalToken.Sides ],
        [ ]
    ],

    CharcoalToken.Expression: [
        [ CharcoalToken.Number ],
        [ CharcoalToken.String ],
        [ CharcoalToken.Name ],
        [ CharcoalToken.Niladic ],
        [ CharcoalToken.Monadic, CharcoalToken.Expression ],
        [ CharcoalToken.Dyadic, CharcoalToken.Expression, CharcoalToken.Expression ],
    ],
    CharcoalToken.Niladic: [
        [ "𝓢" ],
        [ "𝓝" ]
        # TODO
    ],
    CharcoalToken.Monadic: [
        [ "𝓛" ]
        # TODO
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
        [ "∨" ],
        [ "¬" ]
        # TODO
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
        [ CharcoalToken.Move ],
        [ CharcoalToken.Pivot ],
        [ CharcoalToken.Jump ],
        [ CharcoalToken.Rotate ],
        [ CharcoalToken.Reflect ],
        [ CharcoalToken.Copy ],
        [ CharcoalToken.For ],
        [ CharcoalToken.While ],
        [ CharcoalToken.If ],
        [ CharcoalToken.Assign ]
        # TODO
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
        #TODO: commandcharacter*
        [ CharcoalToken.Multidirectional, CharcoalToken.Expression ]
    ],
    CharcoalToken.Polygon: [
        [ "𝓖", CharcoalToken.Side, CharcoalToken.Sides, CharcoalToken.Expression ]
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
        [ "𝓡", CharcoalToken.Expression ]
    ],
    CharcoalToken.Reflect: [
        #TODO: command character*
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
        PassThrough
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

    CharcoalToken.Arrows: [
        lambda result: [ result[0] ] + result[1],
        PassThrough
    ],
    CharcoalToken.Sides: [
        lambda result: [ result[0] ] + result[1],
        PassThrough
    ],
    CharcoalToken.Expression: [ lambda result: result[0] if len(result) == 1 else result ] * len(UnicodeGrammars[CharcoalToken.Expression]),
    CharcoalToken.Niladic: [
        lambda result: "Input String",
        lambda result: "Input Number"
    ],
    CharcoalToken.Monadic: [
        lambda result: "Length",
        lambda result: "Not"
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
        lambda result: [    ]
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
        lambda result: [ "Print" ] + result,
    ],
    CharcoalToken.Polygon: [
        lambda result: [ "Polygon" ] + result[1:],
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
        lambda result: result[1].add(Direction.up) or result[1].add(Direction.left) or result[1].add(Direction.down) or result[1].add(Direction.right) or result[1],
        lambda result: result[1].add(Direction.up_left) or result[1].add(Direction.up_right) or result[1].add(Direction.down_right) or result[1].add(Direction.down_left) or result[1],
        lambda result: result[1].add(Direction.up) or result[1].add(Direction.left) or result[1].add(Direction.down) or result[1].add(Direction.right) or result[1].add(Direction.up_left) or result[1].add(Direction.up_right) or result[1].add(Direction.down_right) or result[1].add(Direction.down_left) or result[1],
        lambda result: result[1].add(result[0]) or result[1]
    ],
    CharcoalToken.Side: [
        lambda result: lambda canvas: (result[0], result[1](canvas))
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

    CharcoalToken.Arrows: [
        lambda result: result[1].add(result[0]) or result[1],
        lambda result: set()
    ],
    CharcoalToken.Sides: [
        lambda result: [ result[0] ] + result[1],
        lambda result: []
    ],

    CharcoalToken.Expression: [
        lambda result: lambda canvas: result[0],
        lambda result: lambda canvas: result[0],
        lambda result: lambda canvas: canvas.scope[result[0]],
        lambda result: lambda canvas: result[0](),
        lambda result: lambda canvas: result[0](result[1](canvas)),
        lambda result: lambda canvas: result[0](result[1](canvas), result[2](canvas))
    ],
    CharcoalToken.Niladic: [
        lambda result: lambda: canvas.InputString(),
        lambda result: lambda: canvas.InputNumber()
        # TODO
    ],
    CharcoalToken.Monadic: [
        lambda result: lambda item: len(item),
        lambda result: lambda item: not item
        # TODO
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
        lambda result: lambda left, right: left and right,
        lambda result: lambda left, right: left or right
        # TODO
    ],

    CharcoalToken.Program: [
        lambda result: lambda canvas: [result[0](canvas), result[1](canvas)] and None,
        lambda result: lambda canvas: None
    ],
    CharcoalToken.Command: [ lambda result: lambda canvas: result[0](canvas) ] * len(UnicodeGrammars[CharcoalToken.Command]),
    CharcoalToken.Body: [
        lambda result: lambda canvas: result[1](canvas),
        lambda result: lambda canvas: result[0](canvas)
    ],
    CharcoalToken.Print: [
        lambda result: lambda canvas: canvas.Print(result[1](canvas), directions={result[0]}),
        lambda result: lambda canvas: canvas.Print(result[0](canvas))
    ],
    CharcoalToken.Multiprint: [
        #TODO: commandcharacter*
        lambda result: lambda canvas: canvas.Print(result[1](canvas), directions=result[0])
    ],
    CharcoalToken.Polygon: [
        lambda result: lambda canvas: canvas.Polygon([ result[1] ] + result[2], result[3](scope))
    ],
    CharcoalToken.Move: [
        lambda result: lambda canvas: canvas.Move(result[0]),
        lambda result: lambda canvas: canvas.Move(result[1]),
        lambda result: lambda canvas: canvas.Move(result[2], result[1](scope))
    ],
    CharcoalToken.Pivot: [
        lambda result: lambda canvas: canvas.Pivot(Pivot.left, result[1](canvas)),
        lambda result: lambda canvas: canvas.Pivot(Pivot.left),
        lambda result: lambda canvas: canvas.Pivot(Pivot.right, result[1](canvas)),
        lambda result: lambda canvas: canvas.Pivot(Pivot.right)
    ],
    CharcoalToken.Jump: [
        lambda result: lambda canvas: canvas.Jump(result[1](canvas), result[2](canvas))
    ],
    CharcoalToken.Rotate: [
        lambda result: lambda canvas: canvas.Rotate(result[1](canvas))
    ],
    CharcoalToken.Reflect: [
        #TODO: command character*
        lambda result: lambda canvas: canvas.Reflect(result[1])
    ],
    CharcoalToken.Copy: [
        lambda result: lambda canvas: canvas.Copy(result[1](canvas), result[2](canvas))
    ],
    CharcoalToken.For: [
        lambda result: lambda canvas: canvas.For(result[1], result[2])
    ],
    CharcoalToken.While: [
        lambda result: lambda canvas: canvas.While(result[1], result[2])
    ],
    CharcoalToken.If: [
        lambda result: lambda canvas: canvas.If(result[1], result[2], result[3])
    ],
    CharcoalToken.Assign: [
        lambda result: lambda canvas: canvas.Assign(result[1], result[2](canvas))
    ],
    CharcoalToken.InputString: [
        lambda result: lambda canvas: canvas.InputString(result[1])
    ],
    CharcoalToken.InputNumber: [
        lambda result: lambda canvas: canvas.InputNumber(result[1])
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
    ): # TODO: interpreter processor
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
                    # print(token, result[0])
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
    parser.add_argument("-f", "--file", type=str, nargs="*", default="", help="File path of the program.")
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
                code += file.read() + "\n"
        else:
            with open(argv.file[0] + ".cl") as file:
                code += file.read() + "\n"
    if argv.astify:
        print("Program")
        PrintTree(Parse(
            code,
            whitespace=argv.whitespace
        ))
    canvas = Canvas(info=info)
    # canvas.inputs = eval(argv.input) # TODO: remove
    if argv.repl:
        while True:
            try:
                Parse(
                    input("Charcoal> "),
                    whitespace=argv.whitespace,
                    processor=InterpreterProcessor
                )(canvas)
            except (KeyboardInterrupt, EOFError):
                pass
    else:
        Parse(code, processor=InterpreterProcessor)(canvas)
        print(str(canvas))