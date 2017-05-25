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
    WolframExpressions = 14
    PairExpressions = 15
    Cases = 16

    Expression = 21
    WolframExpression = 22
    Nilary = 23
    Unary = 24
    Binary = 25
    Ternary = 26
    LazyUnary = 27
    LazyBinary = 28
    LazyTernary = 29
    OtherOperator = 30

    List = 31
    WolframList = 32
    ArrowList = 33
    Dictionary = 34

    Program = 41
    Command = 42
    Body = 43
