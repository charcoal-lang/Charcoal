from enum import Enum

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

    Expression = 21
    Niladic = 22
    Monadic = 23
    Dyadic = 24

    List = 31
    ArrowList = 32

    Program = 51
    Command = 52
    Body = 53
