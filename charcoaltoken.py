CharcoalTokenNames = [
    "Arrow",
    "Multidirectional",
    "Side",
    "Separator",
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
]


class CharcoalToken(object):
    pass

for i in range(len(CharcoalTokenNames)):
    setattr(CharcoalToken, CharcoalTokenNames[i], i)