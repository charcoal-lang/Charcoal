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
    Box = 57
    Rectangle = 58
    Move = 59
    Pivot = 60
    Jump = 61
    Rotate = 62
    Reflect = 63
    Copy = 64
    For = 65
    While = 66
    If = 67
    Assign = 68
    InputString = 69
    InputNumber = 70
    Fill = 71
    SetBackground = 72
    Dump = 73
    Refresh = 74
    RefreshFor = 75
    RefreshWhile = 76