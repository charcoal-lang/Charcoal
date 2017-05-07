from charcoaltoken import CharcoalToken
from unicodegrammars import UnicodeGrammars


def PassThrough(result):
    return result

ASTProcessor = {
    CharcoalToken.Arrow: [
        lambda result: "Left",
        lambda result: "Up",
        lambda result: "Right",
        lambda result: "Down",
        lambda result: "Up Left",
        lambda result: "Up Right",
        lambda result: "Down Right",
        lambda result: "Down Left"
    ],
    CharcoalToken.Multidirectional: [
        lambda result: ["Multidirectional"] + result
    ] + [
        lambda result: [result[1][0], result[0]] + result[1][1:]
    ] * (len(UnicodeGrammars[CharcoalToken.Multidirectional]) - 2) + [
        lambda result: ["Multidirectional"]
    ],
    CharcoalToken.Side: [
        lambda result: ["Side"] + result
    ],
    CharcoalToken.String: [
        lambda result: ["String \"%s\"" % result[0]]
    ],
    CharcoalToken.Number: [
        lambda result: ["Number %s" % str(result[0])]
    ],
    CharcoalToken.Name: [
        lambda result: ["Identifier %s" % str(result[0])]
    ],
    CharcoalToken.Separator: [
        lambda result: None,
        lambda result: None
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
    CharcoalToken.PairExpressions: [
        lambda result: [result[2][0], [result[0], result[1]]] + result[2][1:],
        lambda result: ["PairExpressions", [result[0], result[1]]]
    ],
    CharcoalToken.Cases: [
        lambda result: ["Cases", ["Case", result[0], result[1]]] + result[2][1:],
        lambda result: ["Cases"]
    ],

    CharcoalToken.List: [
        lambda result: ["List"] + result[1][1:],
        lambda result: ["List"]
    ],
    CharcoalToken.ArrowList: [
        lambda result: ["Arrow list"] + result[1][1:],
        lambda result: ["Arrow list"]
    ],
    CharcoalToken.Dictionary: [
        lambda result: ["Dictionary"] + result[1][1:],
        lambda result: ["Dictionary"]
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
        lambda result: result[0]
    ],
    CharcoalToken.Nilary: [
        lambda result: "Input string",
        lambda result: "Input number",
        lambda result: "Random",
        lambda result: "Peek all",
        lambda result: "Peek Moore",
        lambda result: "Peek Von Neumann",
        lambda result: "Peek",
    ],
    CharcoalToken.Unary: [
        lambda result: "Negative",
        lambda result: "Length",
        lambda result: "Not",
        lambda result: "Cast",
        lambda result: "Random",
        lambda result: "Evaluate",
        lambda reuslt: "Pop",
        lambda result: "To lowercase",
        lambda result: "To uppercase",
        lambda result: "Minimum",
        lambda result: "Maximum",
        lambda result: "Character/Ordinal",
        lambda result: "Reverse",
        lambda result: "Get variable"
    ],
    CharcoalToken.Binary: [
        lambda result: "Sum",
        lambda result: "Difference",
        lambda result: "Product",
        lambda result: "Quotient",
        lambda result: "Modulo",
        lambda result: "Equals",
        lambda result: "Less than",
        lambda result: "Greater than",
        lambda result: "Inclusive range",
        lambda result: "Mold",
        lambda result: "Exponentiate",
        lambda result: "At index",
        lambda result: "Push",
        lambda result: "Join",
        lambda result: "Split",
        lambda result: "Find all",
        lambda result: "Find",
        lambda result: "Pad left",
        lambda result: "Pad right",
        lambda result: "Count"
    ],
    CharcoalToken.Ternary: [
    ],
    CharcoalToken.LazyUnary: [
    ],
    CharcoalToken.LazyBinary: [
        lambda result: "And",
        lambda result: "Or"
    ],
    CharcoalToken.LazyTernary: [
        lambda result: "Ternary"
    ],
    CharcoalToken.OtherOperator: [
        lambda result: ["Peek direction"] + result[1:],
        lambda result: ["Map"] + result[1:],
        lambda result: ["Evaluate variable"] + result[1:]
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
        lambda result: ["Input String", result[1]],
        lambda result: ["Input Number", result[1]],
        lambda result: ["Evaluate", result[1]],
        lambda result: ["Print"] + result,
        lambda result: ["Print"] + result,
        lambda result: ["Multiprint"] + result[1:],
        lambda result: ["Multiprint"] + result[1:],
        lambda result: ["Polygon"] + result[1:],
        lambda result: ["Polygon"] + result[1:],
        lambda result: ["Hollow Polygon"] + result[1:],
        lambda result: ["Hollow Polygon"] + result[1:],
        lambda result: ["Rectangle"] + result[1:],
        lambda result: ["Rectangle"] + result[1:],
        lambda result: ["Oblong"] + result[1:],
        lambda result: ["Oblong"] + result[1:],
        lambda result: ["Box"] + result[1:],
        lambda result: ["Box"] + result[1:],
        lambda result: ["Move"] + result,
        lambda result: ["Move"] + result[1:],
        lambda result: ["Move"] + result[1:],
        lambda result: ["Jump"] + result[1:],
        lambda result: ["Pivot Left", result[1]],
        lambda result: ["Pivot Left"],
        lambda result: ["Pivot Right", result[1]],
        lambda result: ["Pivot Right"],
        lambda result: ["Jump to"] + result[1:],
        lambda result: ["Rotate transform"] + result[1:],
        lambda result: ["Rotate transform"]
    ] +
    [lambda result: ["Reflect transform"] + result[1:]] * 3 +
    [lambda result: ["Rotate prism"] + result[1:]] * 8 +
    [lambda result: ["Reflect mirror"] + result[1:]] * 3 +
    [lambda result: ["Rotate copy"] + result[1:]] * 8 +
    [lambda result: ["Reflect copy"] + result[1:]] * 3 +
    [lambda result: ["Rotate overlap overlap"] + result[1:]] * 8 +
    [lambda result: ["Rotate overlap"] + result[1:]] * 8 +
    [lambda result: ["Rotate shutter overlap"] + result[1:]] * 8 +
    [lambda result: ["Rotate shutter"] + result[1:]] * 8 +
    [lambda result: ["Reflect overlap overlap"] + result[1:]] * 3 +
    [lambda result: ["Reflect overlap"] + result[1:]] * 3 +
    [lambda result: ["Reflect butterfly overlap"] + result[1:]] * 3 +
    [lambda result: ["Reflect butterfly"] + result[1:]] * 3 +
    [
        lambda result: ["Rotate"] + result[1:],
        lambda result: ["Rotate"],
        lambda result: ["Reflect"] + result[1:],
        lambda result: ["Reflect"],
        lambda result: ["Copy"] + result[1:],
        lambda result: ["For"] + result[1:],
        lambda result: ["While"] + result[1:],
        lambda result: ["If"] + result[1:],
        lambda result: ["If"] + result[1:],
        lambda result: ["Assign at index"] + result[1:],
        lambda result: ["Assign"] + result[1:],
        lambda result: ["Assign"] + result[1:],
        lambda result: ["Fill"] + result[1:],
        lambda result: ["SetBackground", result[1]],
        lambda result: ["Dump"],
        lambda result: ["Refresh for"] + result[1:],
        lambda result: ["Refresh while"] + result[1:],
        lambda result: ["Refresh", result[1]],
        lambda result: ["Refresh"],
        lambda result: ["Toggle trim"],
        lambda result: ["Crop", result[1], result[2]],
        lambda result: ["Crop", result[1]],
        lambda result: ["Clear"],
        lambda result: ["Extend", result[1], result[2]],
        lambda result: ["Extend", result[1]],
        lambda result: ["Push"] + result[1:],
        lambda result: ["Switch"] + result[1:],
        lambda result: ["Map"] + result[1:],
        lambda result: ["Execute variable"] + result[1:],
        lambda result: ["Set variable"] + result[1:]
    ]
}
