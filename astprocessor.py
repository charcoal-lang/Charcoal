from charcoaltoken import CharcoalToken
from unicodegrammars import UnicodeGrammars


def PassThrough(result):
    return result

ASTProcessor = {
    CharcoalToken.Arrow: [
        lambda result: result[0] + ": Left",
        lambda result: result[0] + ": Up",
        lambda result: result[0] + ": Right",
        lambda result: result[0] + ": Down",
        lambda result: result[0] + ": Up Left",
        lambda result: result[0] + ": Up Right",
        lambda result: result[0] + ": Down Right",
        lambda result: result[0] + ": Down Left"
    ],
    CharcoalToken.Multidirectional: [
        lambda result: ["Multidirectional"] + result[0][1:] + result[1][1:]
    ] + [
        lambda result: [result[1][0], result[0]] + result[1][1:]
    ] * (len(UnicodeGrammars[CharcoalToken.Multidirectional]) - 3) + [
        lambda result: result[1],
        lambda result: ["Multidirectional"]
    ],
    CharcoalToken.Side: [
        lambda result: ["Side"] + result
    ],
    CharcoalToken.String: [
        lambda result: [repr(result[0]) + ": String %s" % repr(result[0])]
    ],
    CharcoalToken.Number: [
        lambda result: [str(result[0]) + ": Number %s" % str(result[0])]
    ],
    CharcoalToken.Name: [
        lambda result: [result[0] + ": Identifier %s" % str(result[0])]
    ],
    CharcoalToken.Separator: [
        lambda result: None,
        lambda result: None
    ],
    CharcoalToken.Span: [
        lambda result: [
            "Span",
            ["Start", result[0]],
            ["Stop", result[2]],
            ["Step", result[4]]
        ],
        lambda result: [
            result[0] + ": Span", ["Start", result[0]], ["Step", result[3]]
        ],
        lambda result: [
            result[0] + ": Span", ["Start", result[0]], ["Stop", result[2]]
        ],
        lambda result: [result[0] + ": Span", ["Start", result[0]]],
        lambda result: [
            result[0] + ": Span", ["Stop", result[1]], ["Step", result[3]]
        ],
        lambda result: [result[0] + ": Span", ["Stop", result[1]]],
        lambda result: [result[0] + ": Span", ["Step", result[2]]],
        lambda result: [result[0] + ": Span"]
    ],

    CharcoalToken.Arrows: [
        lambda result: [result[1][0], result[0]] + result[1][1:],
        lambda result: ["Arrows", result[0]]
    ],
    CharcoalToken.Sides: [
        lambda result: [result[1][0], result[0]] + result[1][1:],
        lambda result: ["Sides", result[0]]
    ],
    CharcoalToken.Expressions: [
        lambda result: [result[1][0], result[0]] + result[1][1:],
        lambda result: ["Expressions", result[0]]
    ],
    CharcoalToken.WolframExpressions: [
        lambda result: [result[1][0], result[0]] + result[1][1:],
        lambda result: ["Wolfram expressions", result[0]]
    ],
    CharcoalToken.PairExpressions: [
        lambda result: [result[2][0], [result[0], result[1]]] + result[2][1:],
        lambda result: ["PairExpressions", [result[0], result[1]]]
    ],
    CharcoalToken.Cases: [
        lambda result: [
            "Cases", ["Case", result[0], result[1]]
        ] + result[2][1:],
        lambda result: ["Cases"]
    ],

    CharcoalToken.List: [
        lambda result: ["List"] + result[1][1:],
        lambda result: ["List"]
    ],
    CharcoalToken.WolframList: [
        lambda result: ["Wolfram list"] + result[1][1:],
        lambda result: ["Wolfram list"]
    ],
    CharcoalToken.Dictionary: [
        lambda result: ["Dictionary"] + result[1][1:],
        lambda result: ["Dictionary"]
    ],

    CharcoalToken.WolframExpression: [
        lambda result: result[0],
        lambda result: result[0]
    ],
    CharcoalToken.Expression: [
        lambda result: result[0],
        lambda result: result[0],
        lambda result: result[0],
        lambda result: result[0],
        lambda result: result[0],
        lambda result: result[1],
        lambda result: result[0],
        lambda result: result,
        lambda result: result,
        lambda result: result,
        lambda result: result,
        lambda result: result,
        lambda result: result,
        lambda result: result,
        lambda result: result,
        lambda result: result[0]
    ],
    CharcoalToken.Nilary: [
        lambda result: result[0] + ": Input string",
        lambda result: result[0] + ": Input number",
        lambda result: result[0] + ": Random",
        lambda result: result[0] + ": Peek all",
        lambda result: result[0] + ": Peek Moore",
        lambda result: result[0] + ": Peek Von Neumann",
        lambda result: result[0] + ": Peek",
    ],
    CharcoalToken.Unary: [
        lambda result: result[0] + ": Negative",
        lambda result: result[0] + ": Length",
        lambda result: result[0] + ": Not",
        lambda result: result[0] + ": Cast",
        lambda result: result[0] + ": Random",
        lambda result: result[0] + ": Evaluate",
        lambda result: result[0] + ": Pop",
        lambda result: result[0] + ": To lowercase",
        lambda result: result[0] + ": To uppercase",
        lambda result: result[0] + ": Minimum",
        lambda result: result[0] + ": Maximum",
        lambda result: result[0] + ": Character/Ordinal",
        lambda result: result[0] + ": Reverse",
        lambda result: result[0] + ": Get variable",
        lambda result: result[0] + ": Repeated",
        lambda result: result[0] + ": Repeated null",
        lambda result: result[0] + ": Slice"
    ],
    CharcoalToken.Binary: [
        lambda result: result[0] + ": Sum",
        lambda result: result[0] + ": Difference",
        lambda result: result[0] + ": Product",
        lambda result: result[0] + ": Quotient",
        lambda result: result[0] + ": Integer quotient",
        lambda result: result[0] + ": Modulo",
        lambda result: result[0] + ": Equals",
        lambda result: result[0] + ": Less than",
        lambda result: result[0] + ": Greater than",
        lambda result: result[0] + ": Bitwise and",
        lambda result: result[0] + ": Bitwise or",
        lambda result: result[0] + ": Inclusive range",
        lambda result: result[0] + ": Mold",
        lambda result: result[0] + ": Exponentiate",
        lambda result: result[0] + ": At index",
        lambda result: result[0] + ": Push",
        lambda result: result[0] + ": Join",
        lambda result: result[0] + ": Split",
        lambda result: result[0] + ": Find all",
        lambda result: result[0] + ": Find",
        lambda result: result[0] + ": Pad left",
        lambda result: result[0] + ": Pad right",
        lambda result: result[0] + ": Count",
        lambda result: result[0] + ": Rule",
        lambda result: result[0] + ": Delayed rule",
        lambda result: result[0] + ": Pattern test",
        lambda result: result[0] + ": Slice"
    ],
    CharcoalToken.Ternary: [
        lambda result: result[0] + ": Slice"
    ],
    CharcoalToken.Quarternary: [
        lambda result: result[0] + ": Slice"
    ],
    CharcoalToken.LazyUnary: [
    ],
    CharcoalToken.LazyBinary: [
        lambda result: result[0] + ": And",
        lambda result: result[0] + ": Or"
    ],
    CharcoalToken.LazyTernary: [
        lambda result: result[0] + ": Ternary"
    ],
    CharcoalToken.LazyQuarternary: [
    ],
    CharcoalToken.OtherOperator: [
        lambda result: [result[0] + ": Peek direction"] + result[1:],
        lambda result: [result[0] + ": Map"] + result[1:],
        lambda result: [result[0] + ": Evaluate variable"] + result[1:],
        lambda result: [result[0] + ": Evaluate variable"] + result[1:]
    ],

    CharcoalToken.Program: [
        lambda result: [result[2][0], result[0]] + result[2][1:],
        lambda result: ["Program"]
    ],
    CharcoalToken.Body: [
        lambda result: result[1],
        lambda result: result[0]
    ],
    CharcoalToken.Command: [
        lambda result: [result[0] + ": Input String", result[1]],
        lambda result: [result[0] + ": Input Number", result[1]],
        lambda result: [result[0] + ": Evaluate", result[1]],
        lambda result: ["Print"] + result,
        lambda result: ["Print"] + result,
        lambda result: [result[0] + ": Multiprint"] + result[1:],
        lambda result: [result[0] + ": Multiprint"] + result[1:],
        lambda result: [result[0] + ": Polygon"] + result[1:],
        lambda result: [result[0] + ": Polygon"] + result[1:],
        lambda result: [result[0] + ": Hollow Polygon"] + result[1:],
        lambda result: [result[0] + ": Hollow Polygon"] + result[1:],
        lambda result: [result[0] + ": Rectangle"] + result[1:],
        lambda result: [result[0] + ": Rectangle"] + result[1:],
        lambda result: [result[0] + ": Oblong"] + result[1:],
        lambda result: [result[0] + ": Oblong"] + result[1:],
        lambda result: [result[0] + ": Box"] + result[1:],
        lambda result: [result[0] + ": Box"] + result[1:],
        lambda result: ["Move"] + result,
        lambda result: [result[0] + ": Move"] + result[1:],
        lambda result: [result[0] + ": Move"] + result[1:],
        lambda result: [result[0] + ": Jump"] + result[1:],
        lambda result: [result[0] + ": Pivot Left", result[1]],
        lambda result: [result[0] + ": Pivot Left"],
        lambda result: [result[0] + ": Pivot Right", result[1]],
        lambda result: [result[0] + ": Pivot Right"],
        lambda result: [result[0] + ": Jump to"] + result[1:],
        lambda result: [result[0] + ": Rotate transform"] + result[1:],
        lambda result: [result[0] + ": Rotate transform"]
    ] +
    [lambda result: [result[0] + ": Reflect transform"] + result[1:]] * 3 +
    [lambda result: [result[0] + ": Rotate prism"] + result[1:]] * 6 +
    [lambda result: [result[0] + ": Reflect mirror"] + result[1:]] * 3 +
    [lambda result: [result[0] + ": Rotate copy"] + result[1:]] * 6 +
    [lambda result: [result[0] + ": Reflect copy"] + result[1:]] * 3 +
    [lambda result: [
        result[0] + ": Rotate overlap overlap"
    ] + result[1:]] * 6 +
    [lambda result: [result[0] + ": Rotate overlap"] + result[1:]] * 6 +
    [lambda result: [
        result[0] + ": Rotate shutter overlap"
    ] + result[1:]] * 6 +
    [lambda result: [result[0] + ": Rotate shutter"] + result[1:]] * 6 +
    [lambda result: [
        result[0] + ": Reflect overlap overlap"
    ] + result[1:]] * 3 +
    [lambda result: [result[0] + ": Reflect overlap"] + result[1:]] * 3 +
    [lambda result: [
        result[0] + ": Reflect butterfly overlap"
    ] + result[1:]] * 3 +
    [lambda result: [result[0] + ": Reflect butterfly"] + result[1:]] * 3 +
    [
        lambda result: [result[0] + ": Rotate"] + result[1:],
        lambda result: [result[0] + ": Rotate"],
        lambda result: [result[0] + ": Reflect"] + result[1:],
        lambda result: [result[0] + ": Reflect"],
        lambda result: [result[0] + ": Copy"] + result[1:],
        lambda result: [result[0] + ": For"] + result[1:],
        lambda result: [result[0] + ": While"] + result[1:],
        lambda result: [result[0] + ": If"] + result[1:],
        lambda result: [result[0] + ": If"] + result[1:],
        lambda result: [result[0] + ": Assign at index"] + result[1:],
        lambda result: [result[0] + ": Assign"] + result[1:],
        lambda result: [result[0] + ": Assign"] + result[1:],
        lambda result: [result[0] + ": Fill"] + result[1:],
        lambda result: [result[0] + ": SetBackground", result[1]],
        lambda result: [result[0] + ": Dump"],
        lambda result: [result[0] + ": Refresh for"] + result[1:],
        lambda result: [result[0] + ": Refresh while"] + result[1:],
        lambda result: [result[0] + ": Refresh", result[1]],
        lambda result: [result[0] + ": Refresh"],
        lambda result: [result[0] + ": Toggle trim"],
        lambda result: [result[0] + ": Crop", result[1], result[2]],
        lambda result: [result[0] + ": Crop", result[1]],
        lambda result: [result[0] + ": Clear"],
        lambda result: [result[0] + ": Extend", result[1], result[2]],
        lambda result: [result[0] + ": Extend", result[1]],
        lambda result: [result[0] + ": Push"] + result[1:],
        lambda result: [result[0] + ": Switch"] + result[1:],
        lambda result: [result[0] + ": Map"] + result[1:],
        lambda result: [result[0] + ": Execute variable"] + result[1:],
        lambda result: [result[0] + ": Execute variable"] + result[1:],
        lambda result: [result[0] + ": Set variable"] + result[1:]
    ]
}
