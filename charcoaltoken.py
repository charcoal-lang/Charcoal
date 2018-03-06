CharcoalTokenNames = [
    "Arrow",
    "Multidirectional",
    "Side",
    "S",
    "String",
    "Number",
    "Name",
    "Span",

    "Arrows",
    "Sides",
    "WolframExpressions",
    "Expressions",
    "PairExpressions",
    "Cases",

    "WolframExpression",
    "Expression",
    "ExpressionOrEOF",
    "Nilary",
    "Unary",
    "Binary",
    "Ternary",
    "Quarternary",
    "LazyUnary",
    "LazyBinary",
    "LazyTernary",
    "LazyQuarternary",
    "OtherOperator",

    "WolframList",
    "List",
    "Dictionary",

    "Program",
    "Body",
    "Command",

    "LP",
    "RP",

    "EOF",

    "MAX",
]


class CharcoalToken(object):
    pass

for i in range(len(CharcoalTokenNames)):
    setattr(CharcoalToken, CharcoalTokenNames[i], i)