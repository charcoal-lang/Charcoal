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
    "Fixes",
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
    "Infix",
    "Prefix",
    "Fix",
    "FixOrEOF",
    "OtherOperator",

    "WolframList",
    "List",
    "Dictionary",

    "Program",
    "NonEmptyProgram",
    "Body",
    "Command",

    "LP",
    "RP",

    "EOF",

    "MAX",
]


class CharcoalToken:
    pass

for i in range(len(CharcoalTokenNames)):
    setattr(CharcoalToken, CharcoalTokenNames[i], i)