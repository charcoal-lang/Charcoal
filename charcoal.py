#!/usr/bin/python3
# vim: set fileencoding=<encoding name> :

# TODO List: 
# bresenham
# multichar background
# input separation - do we take it as an array of python strings
# having more than one number consecutively in the code

from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals

from direction import Direction, Pivot
from charcoaltoken import CharcoalToken
from charactertransformers import *
from directiondictionaries import *
from unicodegrammars import UnicodeGrammars
from astprocessor import ASTProcessor
from interpreterprocessor import InterpreterProcessor
from unicodelookup import UnicodeLookup
from enum import Enum
import random
import re
import argparse
import os
import sys
import time

from colorama import init
init()

if not hasattr(__builtins__, "raw_input"):
    raw_input = input
    input = lambda prompt: eval(raw_input(prompt))
if not hasattr(__builtins__, "basestring"):
    basestring = str

def CleanExecute(function, args):
    try:
        return function(*args)
    except (KeyboardInterrupt, EOFError):
        sys.exit()

old_raw_input = raw_input
raw_input = lambda prompt: CleanExecute(old_raw_input, prompt)
old_input = input
input = lambda prompt: CleanExecute(old_input, prompt)

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
        self.timeout_end = 0


    def __str__(self):
        # multichar_bg = len(character) > 1
        # if multichar_bg:
        #     bg_lines = character.split("\n")

        left = min(self.indices)
        right = max(self.right_indices)
        string = ""
        for i in range(len(self.lines) - 1):
            # line = self.lines[i]
            # index = self.x % line_length
            # background = self.background[index:] + self.background[:index]
            string += self.background * (self.indices[i] - left) + line + self.background * (right - self.right_indices[i]) + "\n"
        return string + self.background * (self.indices[-1] - left) + self.lines[-1] + self.background * (right - self.right_indices[-1])

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


    def PrintLine(self, directions, length, string="", multiprint=False, coordinates=False, move_at_end=True, multichar_fill=False): # overload
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
                if multichar_fill:
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

        if isinstance(string, int):
            length, string = string, ""

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
                    self.Move(direction, len(lines[-1]))

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
        multichar_fill = len(character) > 1
        if multichar_fill:
            lines = character.split("\n")
            character = " "
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
            multichar_fill=multichar_fill
        )
        self.y = coordinates.top
        if multichar_fill:
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
        queue = [ (self.y, self.x) ]

        while len(queue):
            self.y, self.x = queue[0]

            while self.Get() == self.background:
                self.Move(Direction.up)

            self.Move(Direction.down)
            queue = queue[1:]
            points.add((self.y, self.x))

            if not (self.y, self.x - 1) in points:
                self.x -= 1

                if self.Get() == self.background:
                    queue += [ (self.y, self.x) ]

                self.x += 1

            if not (self.y, self.x + 1) in points:
                self.x += 1

                if self.Get() == self.background:
                    queue += [ (self.y, self.x) ]
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

        for i in range(len(points)):
            point = points[i]
            self.y, self.x = point
            self.Put(string[i % length])
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


    def ReflectCopy(self, direction):
        if direction == Direction.left:
            pass
        elif direction == Direction.right:
            lines = [ line[::-1] for line in self.lines ]
        elif direction == Direction.up:
            lines = [ line[::-1] for line in self.lines ]
        elif direction == Direction.down:
            pass
        elif direction == Direction.up_left:
            pass
        elif direction == Direction.up_right:
            pass
        elif direction == Direction.down_left:
            pass
        elif direction == Direction.down_right:
            pass
        # TODO


    def Reflect(self, direction, copy=False):
        if copy:
            self.ReflectCopy(direction)
            return
        if direction == Direction.left or direction == Direction.right:
            self.indices, self.right_indices = [ -index for index in self.right_indices ], [ -index for index in self.indices ]
            self.lines = [ line[::-1] for line in self.lines ]
        elif direction == Direction.up or direction == Direction.down:
            self.lines.reverse()
            self.indices.reverse()
            self.lengths.reverse()
            self.right_indices.reverse()
        elif direction == Direction.up_left or direction == Direction.down_right:
            self.Rotate(6)
            self.Reflect(Direction.right)
        elif direction == Direction.up_right or direction == Direction.down_left:
            self.Rotate(2)
            self.Reflect(Direction.right)


    def RotateCopy(self, rotations):
        # TODO
        pass


    def Rotate(self, rotations, copy=False):
        if copy:
            self.RotateCopy(direction)
            return
        rotations %= 8
        if not rotations:
            return
        left = min(self.indices)
        right = max(self.right_indices)
        self.top = -right
        if rotations == 2:
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
        elif rotations == 4:
            lines = self.Lines()
            number_of_lines = len(lines[0])
            [ self.right_indices, self.indices ] = [ [-index for index in self.indices], [-index for index in self.right_indices] ]
            self.lines = [ line[::-1] for line in self.lines]
        elif rotations == 6:
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
            }[rotations], self.top)
            self.Move({
                1: Direction.up_left,
                3: Direction.up_right,
                5: Direction.down_right,
                7: Direction.down_left
            }[rotations], min(self.indices))
            string = str(self)
            self.Clear()
            self.Print(string, directions={{
                1: Direction.down_right,
                3: Direction.down_left,
                5: Direction.up_left,
                7: Direction.up_right
            }[rotations]})
        self.x = 0
        self.y = 0


    def Copy(self):
        # TODO
        pass


    def GetLoopVariable(self):
        for character in "ικλμνξπρςστυφχψωαβγδεζηθ":
            if not character in self.scope:
                return character


    def For(self, expression, body):
        loop_variable = self.GetLoopVariable()
        variable = expression(self)
        if isinstance(variable, int):
            variable = range(variable)
        for item in variable:
            self.scope[loop_variable] = item
            body(self)


    def While(self, condition, body):
        loop_variable = self.GetLoopVariable()
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
        if variable == 1 and Info.warn_ambiguities in self.info:
            print("Warning: Possible ambiguity, make sure you explicitly use 1 if needed")
        if isinstance(variable, int):
            return random.randrange(variable)
        elif isinstance(variable, list):
            return random.choice(variable)
        elif isinstance(variable, str):
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


    def Dump(self):
        print(self)


    def Refresh(self, timeout=0, ignore_warnings=False):
        if not isinstance(timeout, int):
            print("Refresh expected int, found %s" % str(timeout))
            sys.exit()
        elif not ignore_warnings and timeout == 0 and Info.warn_ambiguities in self.info:
            print("Warning: Possible ambiguity, make sure you explicitly use 0 for no delay if needed")
        try:
            time.sleep(max(0, self.timeout_end - time.clock()))
        except (KeyboardInterrupt, EOFError):
            sys.exit()
        print("\033[0;0H" + str(self))


    def RefreshFor(self, timeout, variable, body):
        print("\033[2J")
        timeout /= 1000.
        loop_variable = self.GetLoopVariable()
        variable = variable(self)
        if isinstance(variable, int):
            variable = range(variable)
        for item in variable:
            self.timeout_end = time.clock() + timeout
            self.scope[loop_variable] = item
            body(self)
            self.Refresh(ignore_warnings=True)


    def RefreshWhile(self, timeout, condition, body):
        print("\033[2J")
        timeout /= 1000.
        loop_variable = self.GetLoopVariable()
        self.scope[loop_variable] = condition(self)
        while self.scope[loop_variable]:
            self.timeout_end = time.clock() + timeout
            body(self)
            self.Refresh(ignore_warnings=True)
            self.scope[loop_variable] = condition(self)


def PassThrough(result):
    return result

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
        whitespace=False,
        normal_encoding=False
    ):
    if normal_encoding:
        code = "".join([ UnicodeLookup[character] if character in UnicodeLookup else character for character in code ])
    if whitespace:
        code = re.sub(
            r"(´.)?\s+",
            lambda match: match.group(1)[1] if match.group(1) else "",
            code
        )
    code += "»" * code.count("«") # because of escaped characters, will need to change to custom universal end closing character (not to be used by the user) if we have autoclosing delimited strings, lists etc
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


def AddAmbiguityWarnings():
    ASTProcessor[CharcoalToken.Monadic][4] = lambda result: "Random [Warning: May be ambiguous]"
    ASTProcessor[CharcoalToken.Refresh][0] = lambda: [ "Refresh [Warning: May be ambiguous]" ] # TODO: implement

if __name__ == "__main__":
    interactive = len(sys.argv) == 1

    parser = argparse.ArgumentParser(description="Interpret the Charcoal language.")
    parser.add_argument("-f", "--file", type=str, nargs="*", default="", help="File path of the program.")
    parser.add_argument("-c", "--code", type=str, nargs="?", default="", help="Code of the program.")
    parser.add_argument("-i", "--input", type=str, nargs="?", default="", help="Input to the program.")
    parser.add_argument("-e", "--normalencoding", action="store_true", help="Use custom codepage.")
    parser.add_argument("-a", "--astify", action="store_true", help="Print AST.")
    parser.add_argument("-p", "--prompt", action="store_true", help="Prompt for input.")
    parser.add_argument("-r", "--repl", action="store_true", help="Open as REPL instead of interpreting.")
    parser.add_argument("-w", "--whitespace", action="store_true", help="Ignore all whitespace unless prefixed by a ´.")
    parser.add_argument("-Wam", "--Wambiguities", action="store_true", help="Warn the user of any ambiguities.")
    parser.add_argument("-t", "--test", action="store_true", help="Run unit tests.")
    argv = parser.parse_args()
    info = set()

    if argv.Wambiguities:
        info.add(Info.warn_ambiguities)
        AddAmbiguityWarnings()

    if argv.prompt:
        info.add(Info.prompt)

    if argv.repl or interactive:
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
            whitespace=argv.whitespace,
            normal_encoding=argv.normalencoding
        ))

    charcoal = Charcoal(info=info)
    # charcoal.inputs = eval(argv.input) # TODO: fix

    if argv.repl or interactive:

        while True:

            try:
                Parse(
                    raw_input("Charcoal> "),
                    whitespace=argv.whitespace,
                    processor=InterpreterProcessor,
                    normal_encoding=argv.normalencoding
                )(charcoal)
                print(charcoal)

            except (KeyboardInterrupt, EOFError):
                break

    else:
        Parse(code, whitespace=argv.whitespace, processor=InterpreterProcessor, normal_encoding=argv.normalencoding)(charcoal)
        print(charcoal)
