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
    Print = 53
    Body = 54
    Multiprint = 55
    Polygon = 56
    Box = 57
    Rectangle = 58
    Move = 59
    Pivot = 60
    Jump = 61
    RotateCopyMultiple = 82
    ReflectCopyMultiple = 83
    RotateOverlapMultiple = 84
    ReflectOverlapMultiple = 85
    RotateCopy = 62
    ReflectCopy = 63
    RotateOverlap = 64
    ReflectOverlap = 65
    Rotate = 66
    Reflect = 67
    Copy = 68
    For = 69
    While = 70
    If = 71
    Assign = 72
    InputString = 73
    InputNumber = 74
    Fill = 75
    SetBackground = 76
    Dump = 77
    Refresh = 78
    RefreshFor = 79
    RefreshWhile = 80
    Evaluate = 81