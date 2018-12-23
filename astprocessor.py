from charcoaltoken import CharcoalToken as CT
from unicodegrammars import UnicodeGrammars


def PassThrough(r):
    return r

ASTProcessor = {
    CT.Arrow: [
        lambda r: r[0] + ": Left",
        lambda r: r[0] + ": Up",
        lambda r: r[0] + ": Right",
        lambda r: r[0] + ": Down",
        lambda r: r[0] + ": Up Left",
        lambda r: r[0] + ": Up Right",
        lambda r: r[0] + ": Down Right",
        lambda r: r[0] + ": Down Left",
        lambda r: r[1]
    ],
    CT.Multidirectional: [
        lambda r: ["Multidirectional"] + r[0][1:] + r[1][1:]
    ] + [
        lambda r: [r[1][0], r[0]] + r[1][1:]
    ] * (len(UnicodeGrammars[CT.Multidirectional]) - 5) + [
        lambda r: r[1],
        lambda r: r[1],
        lambda r: r[1],
        lambda r: ["Multidirectional"]
    ],
    CT.Side: [lambda r: ["Side"] + r],
    CT.String: [
        lambda r: [repr(r[0]) + ": String %s" % repr(r[0])]
    ],
    CT.Number: [
        lambda r: [str(r[0]) + ": Number %s" % str(r[0])]
    ],
    CT.Name: [lambda r: [r[0] + ": Identifier %s" % str(r[0])]],
    CT.S: [lambda r: None] * 2,
    CT.Span: [
        lambda r: [
            r[0] + ": Span", ["Start", r[0]], ["Stop", r[2]], ["Step", r[4]]
        ],
        lambda r: [r[0] + ": Span", ["Start", r[0]], ["Step", r[3]]],
        lambda r: [r[0] + ": Span", ["Start", r[0]], ["Stop", r[2]]],
        lambda r: [r[0] + ": Span", ["Start", r[0]]],
        lambda r: [r[0] + ": Span", ["Stop", r[1]], ["Step", r[3]]],
        lambda r: [r[0] + ": Span", ["Stop", r[1]]],
        lambda r: [r[0] + ": Span", ["Step", r[2]]],
        lambda r: [r[0] + ": Span"]
    ],

    CT.Arrows: [
        lambda r: [r[1][0], r[0]] + r[1][1:],
        lambda r: ["Arrows", r[0]]
    ],
    CT.Sides: [
        lambda r: [r[1][0], r[0]] + r[1][1:],
        lambda r: ["Sides", r[0]]
    ],
    CT.Expressions: [
        lambda r: [r[1][0], r[0]] + r[1][1:],
        lambda r: ["Expressions", r[0]]
    ],
    CT.WolframExpressions: [
        lambda r: [r[1][0], r[0]] + r[1][1:],
        lambda r: ["Wolfram expressions", r[0]]
    ],
    CT.PairExpressions: [
        lambda r: [r[2][0], [r[0], r[1]]] + r[2][1:],
        lambda r: ["PairExpressions", [r[0], r[1]]]
    ],
    CT.Cases: [
        lambda r: ["Cases", ["Case", r[0], r[1]]] + r[2][1:],
        lambda r: ["Cases"]
    ],

    CT.List: [
        lambda r: ["List"] + r[1][1:],
        lambda r: ["List"]
    ] * 2,
    CT.WolframList: [
        lambda r: ["Wolfram list"] + r[1][1:],
        lambda r: ["Wolfram list"]
    ] * 2,
    CT.Dictionary: [
        lambda r: ["Dictionary"] + r[1][1:],
        lambda r: ["Dictionary"]
    ] * 2,

    CT.WolframExpression: [
        lambda r: r[0],
        lambda r: r[0]
    ],
    CT.Expression: [
        lambda r: r[0],
        lambda r: r[0],
        lambda r: r[0],
        lambda r: r[0],
        lambda r: r[1],
        lambda r: r[1],
        lambda r: r[0],
        lambda r: r[1],
        lambda r: r[1],
        lambda r: r[0]
    ] + [
        lambda r: r[:-1]
    ] * 17,
    CT.ExpressionOrEOF: [
        lambda r: r[0],
        lambda r: [": Input"]
    ],
    CT.Nilary: [
        lambda r: r[0] + ": Input string",
        lambda r: r[0] + ": Input number",
        lambda r: r[0] + ": Input",
        lambda r: r[0] + ": Random",
        lambda r: r[0] + ": Peek all",
        lambda r: r[0] + ": Peek Moore",
        lambda r: r[0] + ": Peek Von Neumann",
        lambda r: r[0] + ": Peek",
        lambda r: r[0] + ": x position",
        lambda r: r[0] + ": y position"
    ],
    CT.Unary: [
        lambda r: r[0] + ": Negative",
        lambda r: r[0] + ": Length",
        lambda r: r[0] + ": Not",
        lambda r: r[0] + ": Cast",
        lambda r: r[0] + ": Random",
        lambda r: r[0] + ": Evaluate",
        lambda r: r[0] + ": Pop",
        lambda r: r[0] + ": To lowercase",
        lambda r: r[0] + ": To uppercase",
        lambda r: r[0] + ": Minimum",
        lambda r: r[0] + ": Maximum",
        lambda r: r[0] + ": Character/Ordinal",
        lambda r: r[0] + ": Reverse",
        lambda r: r[0] + ": Get variable",
        lambda r: r[0] + ": Repeated",
        lambda r: r[0] + ": Repeated null",
        lambda r: r[0] + ": Slice",
        lambda r: r[0] + ": Inclusive range",
        lambda r: r[0] + ": Range",
        lambda r: r[0] + ": Not",
        lambda r: r[0] + ": Absolute value",
        lambda r: r[0] + ": Sum",
        lambda r: r[0] + ": Product",
        lambda r: r[0] + ": Incremented",
        lambda r: r[0] + ": Decremented",
        lambda r: r[0] + ": Doubled",
        lambda r: r[0] + ": Halved",
        lambda r: r[0] + ": eval",
        lambda r: r[0] + ": Square root"
    ],
    CT.Binary: [
        lambda r: r[0] + ": Sum",
        lambda r: r[0] + ": Difference",
        lambda r: r[0] + ": Product",
        lambda r: r[0] + ": Integer quotient",
        lambda r: r[0] + ": Quotient",
        lambda r: r[0] + ": Modulo",
        lambda r: r[0] + ": Equals",
        lambda r: r[0] + ": Less than",
        lambda r: r[0] + ": Greater than",
        lambda r: r[0] + ": Bitwise and",
        lambda r: r[0] + ": Bitwise or",
        lambda r: r[0] + ": Inclusive range",
        lambda r: r[0] + ": Mold",
        lambda r: r[0] + ": Exponentiate",
        lambda r: r[0] + ": At index",
        lambda r: r[0] + ": Push",
        lambda r: r[0] + ": Join",
        lambda r: r[0] + ": Split",
        lambda r: r[0] + ": Find all",
        lambda r: r[0] + ": Find",
        lambda r: r[0] + ": Pad left",
        lambda r: r[0] + ": Pad right",
        lambda r: r[0] + ": Count",
        lambda r: r[0] + ": Rule",
        lambda r: r[0] + ": Delayed rule",
        lambda r: r[0] + ": Pattern test",
        lambda r: r[0] + ": Slice",
        lambda r: r[0] + ": All",
        lambda r: r[0] + ": Any"
    ],
    CT.Ternary: [lambda r: r[0] + ": Slice"],
    CT.Quarternary: [lambda r: r[0] + ": Slice"],
    CT.LazyUnary: [],
    CT.LazyBinary: [
        lambda r: r[0] + ": And",
        lambda r: r[0] + ": Or"
    ],
    CT.LazyTernary: [lambda r: r[0] + ": Ternary"],
    CT.LazyQuarternary: [],
    CT.OtherOperator: [
        lambda r: [r[0] + ": Peek direction"] + r[1:],
        lambda r: [r[0] + ": Map"] + r[1:],
        lambda r: [r[0] + ": String map"] + r[1:],
        lambda r: [r[0] + ": Any"] + r[1:],
        lambda r: [r[0] + ": All"] + r[1:],
        lambda r: [r[0] + ": Filter"] + r[1:],
        lambda r: [r[0] + ": Evaluate variable"] + r[1:],
        lambda r: [r[0] + ": Evaluate variable"] + r[1:],
        lambda r: [r[0] + ": Evaluate variable"] + r[1:]
    ],

    CT.Program: [
        lambda r: [r[2][0], r[0]] + r[2][1:],
        lambda r: ["Program"]
    ],
    CT.Body: [
        lambda r: r[1],
        lambda r: r[1],
        lambda r: r[0]
    ],
    CT.Command: [
        lambda r: [r[0] + ": Input String", r[1]],
        lambda r: [r[0] + ": Input Number", r[1]],
        lambda r: [r[0] + ": Input", r[1]],
        lambda r: [r[0] + ": Evaluate", r[1]],
        lambda r: ["Print"] + r,
        lambda r: ["Print"] + r,
        lambda r: [r[0] + ": Multiprint"] + r[1:],
        lambda r: [r[0] + ": Multiprint"] + r[1:],
        lambda r: [r[0] + ": Polygon"] + r[1:],
        lambda r: [r[0] + ": Polygon"] + r[1:],
        lambda r: [r[0] + ": Hollow Polygon"] + r[1:],
        lambda r: [r[0] + ": Hollow Polygon"] + r[1:],
        lambda r: [r[0] + ": Rectangle"] + r[1:],
        lambda r: [r[0] + ": Rectangle"] + r[1:],
        lambda r: [r[0] + ": Oblong"] + r[1:],
        lambda r: [r[0] + ": Oblong"] + r[1:],
        lambda r: [r[0] + ": Box"] + r[1:],
        lambda r: [r[0] + ": Box"] + r[1:],
        lambda r: ["Move"] + r,
        lambda r: [r[0] + ": Move"] + r[1:],
        lambda r: [r[0] + ": Move"] + r[1:],
        lambda r: [r[0] + ": Jump"] + r[1:],
        lambda r: [r[0] + ": Pivot Left", r[1]],
        lambda r: [r[0] + ": Pivot Left"],
        lambda r: [r[0] + ": Pivot Right", r[1]],
        lambda r: [r[0] + ": Pivot Right"],
        lambda r: [r[0] + ": Jump to"] + r[1:],
        lambda r: [r[0] + ": Rotate transform"] + r[1:],
        lambda r: [r[0] + ": Rotate transform"]
    ] +
    [lambda r: [r[0] + ": Reflect transform"] + r[1:]] * 3 +
    [lambda r: [r[0] + ": Rotate prism"] + r[1:]] * 6 +
    [lambda r: [r[0] + ": Reflect mirror"] + r[1:]] * 3 +
    [lambda r: [r[0] + ": Rotate copy"] + r[1:]] * 6 +
    [lambda r: [r[0] + ": Reflect copy"] + r[1:]] * 3 +
    [lambda r: [
        r[0] + ": Rotate overlap overlap"
    ] + r[1:]] * 6 +
    [lambda r: [r[0] + ": Rotate overlap"] + r[1:]] * 6 +
    [lambda r: [
        r[0] + ": Rotate shutter overlap"
    ] + r[1:]] * 6 +
    [lambda r: [r[0] + ": Rotate shutter"] + r[1:]] * 6 +
    [lambda r: [
        r[0] + ": Reflect overlap overlap"
    ] + r[1:]] * 3 +
    [lambda r: [r[0] + ": Reflect overlap"] + r[1:]] * 3 +
    [lambda r: [
        r[0] + ": Reflect butterfly overlap"
    ] + r[1:]] * 3 +
    [lambda r: [r[0] + ": Reflect butterfly"] + r[1:]] * 3 +
    [
        lambda r: [r[0] + ": Rotate"] + r[1:],
        lambda r: [r[0] + ": Rotate"],
        lambda r: [r[0] + ": Reflect"] + r[1:],
        lambda r: [r[0] + ": Reflect"],
        lambda r: [r[0] + ": Copy"] + r[1:],
        lambda r: [r[0] + ": For"] + r[1:],
        lambda r: [r[0] + ": While"] + r[1:],
        lambda r: [r[0] + ": If"] + r[1:],
        lambda r: [r[0] + ": If"] + r[1:],
        lambda r: [r[0] + ": Assign at index"] + r[1:],
        lambda r: [r[0] + ": Assign"] + r[1:],
        lambda r: [r[0] + ": Assign"] + r[1:],
        lambda r: [r[0] + ": Fill"] + r[1:],
        lambda r: [r[0] + ": SetBackground", r[1]],
        lambda r: [r[0] + ": Dump"],
        lambda r: [r[0] + ": Refresh for"] + r[1:],
        lambda r: [r[0] + ": Refresh while"] + r[1:],
        lambda r: [r[0] + ": Refresh", r[1]],
        lambda r: [r[0] + ": Refresh"],
        lambda r: [r[0] + ": Toggle trim"],
        lambda r: [r[0] + ": Crop", r[1], r[2]],
        lambda r: [r[0] + ": Crop", r[1]],
        lambda r: [r[0] + ": Clear"],
        lambda r: [r[0] + ": Extend", r[1], r[2]],
        lambda r: [r[0] + ": Extend", r[1]],
        lambda r: [r[0] + ": Push"] + r[1:],
        lambda r: [r[0] + ": Switch"] + r[1:],
        lambda r: [r[0] + ": Switch"] + r[1:],
        lambda r: [r[0] + ": Switch"] + r[1:],
        lambda r: [r[0] + ": Switch"] + r[1:],
        lambda r: [r[0] + ": Switch"] + r[1:],
        lambda r: [r[0] + ": Switch"] + r[1:],
        lambda r: [r[0] + ": Map"] + r[1:],
        lambda r: [r[0] + ": Execute variable"] + r[1:],
        lambda r: [r[0] + ": Execute variable"] + r[1:],
        lambda r: [r[0] + ": Map assign left"] + r[1:],
        lambda r: [r[0] + ": Map assign"] + r[1:],
        lambda r: [r[0] + ": Map assign right"] + r[1:],
        lambda r: [r[0] + ": Map assign"] + r[1:],
        lambda r: [r[0] + ": exec"] + r[1:],
    ]
}
