from enum import Enum

i = -1

def _id():
    global i
    i += 1
    return i

class CharcoalToken(object):
    Arrow = _id()
    Multidirectional = _id()
    Side = _id()
    Separator = _id()
    String = _id()
    Number = _id()
    Name = _id()
    Span = _id()

    Arrows = _id()
    Sides = _id()
    WolframExpressions = _id()
    Expressions = _id()
    PairExpressions = _id()
    Cases = _id()

    WolframExpression = _id()
    Expression = _id()
    Nilary = _id()
    Unary = _id()
    Binary = _id()
    Ternary = _id()
    LazyUnary = _id()
    LazyBinary = _id()
    LazyTernary = _id()
    OtherOperator = _id()

    WolframList = _id()
    List = _id()
    ArrowList = _id()
    Dictionary = _id()

    Program = _id()
    Body = _id()
    Command = _id()
