from enum import Enum

class CharcoalToken(Enum):
    Arrow = 1
    Multidirectional = 2
    Side = 3
    Separator = 4
    String = 5
    Number = 6
    Name = 7
    Span = 8

    Arrows = 11
    Sides = 12
    Expressions = 13
    PairExpressions = 14
    Cases = 15

    Expression = 21
    Nilary = 22
    Unary = 23
    Binary = 24
    Ternary = 25
    LazyUnary = 26
    LazyBinary = 27
    LazyTernary = 28
    OtherOperator = 29

    List = 31
    ArrowList = 32
    Dictionary = 33

    Program = 41
    Command = 42
    Body = 43
