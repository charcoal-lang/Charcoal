from charcoaltoken import CharcoalToken as CT
from unicodegrammars import UnicodeGrammars


def PassThrough(r):
    return r

def GetFreeVariable(s, n=1):
    r = ""
    for _ in range(n):
        r += next(filter(lambda c: c not in s + r, "ικλμνξπρςστδεζηθ"))
    return r

def VerbosifyVariable(c):
    return "iklmnxprvstufcywabgdezhq"["ικλμνξπρςστυφχψωαβγδεζηθ".find(c)]

def EvaluateFunctionOrList(f, s):
    if isinstance(f, list):
        return f[0](s)
    return f(s)

ASTProcessor = {
    CT.Arrow: [
        lambda r: [lambda s="": [r[0] + ": Left"]],
        lambda r: [lambda s="": [r[0] + ": Up"]],
        lambda r: [lambda s="": [r[0] + ": Right"]],
        lambda r: [lambda s="": [r[0] + ": Down"]],
        lambda r: [lambda s="": [r[0] + ": Up Left"]],
        lambda r: [lambda s="": [r[0] + ": Up Right"]],
        lambda r: [lambda s="": [r[0] + ": Down Right"]],
        lambda r: [lambda s="": [r[0] + ": Down Left"]],
        lambda r: [lambda s="": [r[0] + ": Direction", r[1][0](s)]]
    ],
    CT.Multidirectional: [
        lambda r: [lambda s="": ["Multidirectional"] + r[0][0](s)[1:] + r[1][0](s)[1:]],
        lambda r: [lambda s="": ["Multidirectional", r[0] + ": Right, down, left, up"] + r[1][0](s)[1:]],
        lambda r: [lambda s="": ["Multidirectional", r[0] + ": Down right, down left, up left, up right"] + r[1][0](s)[1:]],
        lambda r: [lambda s="": ["Multidirectional", r[0] + ": Right, down right, down, down left, left, up left, up, up right"] + r[1][0](s)[1:]],
        lambda r: [lambda s="": ["Multidirectional", r[0] + ": Down, up"] + r[1][0](s)[1:]],
        lambda r: [lambda s="": ["Multidirectional", r[0] + ": Right, left"] + r[1][0](s)[1:]],
        lambda r: [lambda s="": ["Multidirectional", r[0] + ": Down right, up left"] + r[1][0](s)[1:]],
        lambda r: [lambda s="": ["Multidirectional", r[0] + ": Down left, up right"] + r[1][0](s)[1:]],
        lambda r: [lambda s="": ["Multidirectional", r[0] + ": Down right, up right"] + r[1][0](s)[1:]],
        lambda r: [lambda s="": ["Multidirectional", r[0] + ": Down left, up left"] + r[1][0](s)[1:]],
        lambda r: [lambda s="": ["Multidirectional", r[0] + ": Down right, down left"] + r[1][0](s)[1:]],
        lambda r: [lambda s="": ["Multidirectional", r[0] + ": Down right, down, up, up right"] + r[1][0](s)[1:]],
        lambda r: [lambda s="": ["Multidirectional", r[0] + ": Right, up"] + r[1][0](s)[1:]],
        lambda r: [lambda s="": ["Multidirectional", r[0] + ": Right, down, left"] + r[1][0](s)[1:]],
        lambda r: [lambda s="": ["Multidirectional", r[0] + ": Up left, up right"] + r[1][0](s)[1:]],
        lambda r: [lambda s="": ["Multidirectional", r[0] + ": Down, up left, up right"] + r[1][0](s)[1:]],
        lambda r: [lambda s="": ["Multidirectional", r[0] + ": Down left, left"] + r[1][0](s)[1:]],
        lambda r: [lambda s="": ["Multidirectional", r[0] + ": Down, left"] + r[1][0](s)[1:]],
        lambda r: [lambda s="": ["Multidirectional", r[0] + ": Right, up"] + r[1][0](s)[1:]],
        lambda r: [lambda s="": ["Multidirectional", r[0] + ": Right, down"] + r[1][0](s)[1:]],
        lambda r: [lambda s="": r[1][0](s)],
        lambda r: [lambda s="": r[1][0](s)],
        lambda r: [lambda s="": r[1][0](s)],
        lambda r: [lambda s="": ["Multidirectional"]]
    ],
    CT.Side: [lambda r: [lambda s="": ["Side"] + [el[0](s) for el in r]]],
    CT.String: [
        lambda r: [lambda s="": [repr(r[0]) + ": String %s" % repr(r[0])]]
    ],
    CT.Number: [
        lambda r: [lambda s="": [str(r[0]) + ": Number %s" % str(r[0])]]
    ],
    CT.Name: [lambda r: [lambda s="": [r[0] + ": Identifier %s (%s)" % (str(r[0]), VerbosifyVariable(str(r[0])))]]],
    CT.S: [lambda r: [lambda s="": []]] * 2,
    CT.Span: [
        lambda r: [lambda s="": [
            "Span", ["Start", r[0][0](s)], ["Stop", r[2][0](s)], ["Step", r[4][0](s)]
        ]],
        lambda r: [lambda s="": ["Span", ["Start", r[0][0](s)], ["Step", r[3][0](s)]]],
        lambda r: [lambda s="": ["Span", ["Start", r[0][0](s)], ["Stop", r[2][0](s)]]],
        lambda r: [lambda s="": ["Span", ["Start", r[0][0](s)]]],
        lambda r: [lambda s="": ["Span", ["Stop", r[1][0](s)], ["Step", r[3][0](s)]]],
        lambda r: [lambda s="": ["Span", ["Stop", r[1][0](s)]]],
        lambda r: [lambda s="": ["Span", ["Step", r[2][0](s)]]],
        lambda r: [lambda s="": ["Span"]]
    ],

    CT.Arrows: [
        lambda r: [lambda s="": ["Arrows", r[0][0](s)] + r[1][0](s)[1:]],
        lambda r: [lambda s="": ["Arrows", r[0][0](s)]]
    ],
    CT.Sides: [
        lambda r: [lambda s="": ["Sides", r[0][0](s)] + r[1][0](s)[1:]],
        lambda r: [lambda s="": ["Sides", r[0][0](s)]]
    ],
    CT.Expressions: [
        lambda r: [lambda s="": ["Expressions", r[0][0](s)] + r[1][0](s)[1:]],
        lambda r: [lambda s="": ["Expressions", r[0][0](s)]]
    ],
    CT.WolframExpressions: [
        lambda r: [lambda s="": ["Wolfram Expressions", r[0][0](s)[0](s)] + [el[0](s) for el in r[1][0](s)[1:]]],
        lambda r: [lambda s="": ["Wolfram Expressions", r[0][0](s)]]
    ],
    CT.PairExpressions: [
        lambda r: [lambda s="": ["Pair Expressions", ["Pair", r[0][0](s), r[1][0](s)]] + r[2][0](s)[1:]],
        lambda r: [lambda s="": ["Pair Expressions", ["Pair", r[0][0](s), r[1][0](s)]]]
    ],
    CT.Cases: [
        lambda r: [lambda s="": ["Cases", ["Case", r[0][0](s), r[1][0](s)[0](s)]] + r[2][0](s)[1:]],
        lambda r: [lambda s="": ["Cases"]]
    ],

    CT.List: [
        lambda r: [lambda s="": ["List"] + r[1][0](s)[1:]],
        lambda r: [lambda s="": ["List"]]
    ] * 2,
    CT.WolframList: [
        lambda r: [lambda s="": ["Wolfram List"] + r[1][0](s)[1:]],
        lambda r: [lambda s="": ["Wolfram List"]]
    ] * 2,
    CT.Dictionary: [
        lambda r: [lambda s="": ["Dictionary"] + r[1][0](s)[1:]],
        lambda r: [lambda s="": ["Dictionary"]]
    ] * 2,

    CT.WolframExpression: [
        lambda r: [lambda s="": r[0][0](s)],
        lambda r: [lambda s="": r[0][0](s)],
    ],
    CT.Expression: [
        lambda r: [lambda s="": r[0](s)],
        lambda r: [lambda s="": r[0](s)],
        lambda r: [lambda s="": r[0](s)],
        lambda r: [lambda s="": r[0][0](s)],
        lambda r: [lambda s="": r[1][0](s)],
        lambda r: [lambda s="": r[1][0](s)],
        lambda r: [lambda s="": r[0][0](s)],
        lambda r: [lambda s="": r[1][0]()],
        lambda r: [lambda s="": r[1][0]()],
        lambda r: [lambda s="": r[0][0](s)]
    ] + [
        lambda r: [lambda s="": [el[0](s) for el in r[:-1]]]
    ] * 17,
    CT.ExpressionOrEOF: [
        lambda r: [lambda s="": r[0]],
        lambda r: [lambda s="": [": Input"]]
    ],
    CT.Nilary: [
        lambda r: [lambda s="": r[0] + ": Input string"],
        lambda r: [lambda s="": r[0] + ": Input number"],
        lambda r: [lambda s="": r[0] + ": Input"],
        lambda r: [lambda s="": r[0] + ": Random"],
        lambda r: [lambda s="": r[0] + ": Peek all"],
        lambda r: [lambda s="": r[0] + ": Peek Moore"],
        lambda r: [lambda s="": r[0] + ": Peek Von Neumann"],
        lambda r: [lambda s="": r[0] + ": Peek"],
        lambda r: [lambda s="": r[0] + ": x position"],
        lambda r: [lambda s="": r[0] + ": y position"]
    ],
    CT.Unary: [
        lambda r: [lambda s="": r[0] + ": Negative"],
        lambda r: [lambda s="": r[0] + ": Length"],
        lambda r: [lambda s="": r[0] + ": Not"],
        lambda r: [lambda s="": r[0] + ": Cast"],
        lambda r: [lambda s="": r[0] + ": Random"],
        lambda r: [lambda s="": r[0] + ": Evaluate"],
        lambda r: [lambda s="": r[0] + ": Pop"],
        lambda r: [lambda s="": r[0] + ": To lowercase"],
        lambda r: [lambda s="": r[0] + ": To uppercase"],
        lambda r: [lambda s="": r[0] + ": Minimum"],
        lambda r: [lambda s="": r[0] + ": Maximum"],
        lambda r: [lambda s="": r[0] + ": Character/Ordinal"],
        lambda r: [lambda s="": r[0] + ": Reverse"],
        lambda r: [lambda s="": r[0] + ": Get variable"],
        lambda r: [lambda s="": r[0] + ": Repeated"],
        lambda r: [lambda s="": r[0] + ": Repeated null"],
        lambda r: [lambda s="": r[0] + ": Slice"],
        lambda r: [lambda s="": r[0] + ": Inclusive range"],
        lambda r: [lambda s="": r[0] + ": Range"],
        lambda r: [lambda s="": r[0] + ": Not"],
        lambda r: [lambda s="": r[0] + ": Absolute value"],
        lambda r: [lambda s="": r[0] + ": Sum"],
        lambda r: [lambda s="": r[0] + ": Product"],
        lambda r: [lambda s="": r[0] + ": Incremented"],
        lambda r: [lambda s="": r[0] + ": Decremented"],
        lambda r: [lambda s="": r[0] + ": Doubled"],
        lambda r: [lambda s="": r[0] + ": Halved"],
        lambda r: [lambda s="": r[0] + ": eval"],
        lambda r: [lambda s="": r[0] + ": Square root"]
    ],
    CT.Binary: [
        lambda r: [lambda s="": r[0] + ": Sum"],
        lambda r: [lambda s="": r[0] + ": Difference"],
        lambda r: [lambda s="": r[0] + ": Product"],
        lambda r: [lambda s="": r[0] + ": Integer quotient"],
        lambda r: [lambda s="": r[0] + ": Quotient"],
        lambda r: [lambda s="": r[0] + ": Modulo"],
        lambda r: [lambda s="": r[0] + ": Equals"],
        lambda r: [lambda s="": r[0] + ": Less than"],
        lambda r: [lambda s="": r[0] + ": Greater than"],
        lambda r: [lambda s="": r[0] + ": Bitwise and"],
        lambda r: [lambda s="": r[0] + ": Bitwise or"],
        lambda r: [lambda s="": r[0] + ": Inclusive range"],
        lambda r: [lambda s="": r[0] + ": Mold"],
        lambda r: [lambda s="": r[0] + ": Exponentiate"],
        lambda r: [lambda s="": r[0] + ": At index"],
        lambda r: [lambda s="": r[0] + ": Push"],
        lambda r: [lambda s="": r[0] + ": Join"],
        lambda r: [lambda s="": r[0] + ": Split"],
        lambda r: [lambda s="": r[0] + ": Find all"],
        lambda r: [lambda s="": r[0] + ": Find"],
        lambda r: [lambda s="": r[0] + ": Pad left"],
        lambda r: [lambda s="": r[0] + ": Pad right"],
        lambda r: [lambda s="": r[0] + ": Count"],
        lambda r: [lambda s="": r[0] + ": Rule"],
        lambda r: [lambda s="": r[0] + ": Delayed rule"],
        lambda r: [lambda s="": r[0] + ": Pattern test"],
        lambda r: [lambda s="": r[0] + ": Slice"],
        lambda r: [lambda s="": r[0] + ": Base"],
        lambda r: [lambda s="": r[0] + ": String base"]
    ],
    CT.Ternary: [lambda r: [lambda s="": r[0] + ": Slice"]],
    CT.Quarternary: [lambda r: [lambda s="": r[0] + ": Slice"]],
    CT.LazyUnary: [],
    CT.LazyBinary: [
        lambda r: [lambda s="": r[0] + ": And"],
        lambda r: [lambda s="": r[0] + ": Or"]
    ],
    CT.LazyTernary: [lambda r: [lambda s="": r[0] + ": Ternary"]],
    CT.LazyQuarternary: [],
    CT.OtherOperator: [
        lambda r: [lambda s="": [r[0] + ": Peek direction"] + [el[0](s) for el in r[1:]]],
        lambda r: [lambda s="": (lambda t: [r[0] + ": Map (loop variable %s (%s), index variable %s (%s))" % (t[-2], VerbosifyVariable(t[-2]), t[-1], VerbosifyVariable(t[-1])), r[1][0](s), r[2][0](t)])(s + GetFreeVariable(s, 2))],
        lambda r: [lambda s="": (lambda t: [r[0] + ": String map (loop variable %s (%s), index variable %s (%s))" % (t[-2], VerbosifyVariable(t[-2]), t[-1], VerbosifyVariable(t[-1])), r[1][0](s), r[2][0](t)])(s + GetFreeVariable(s, 2))],
        lambda r: [lambda s="": (lambda t: [r[0] + ": Any (loop variable %s (%s), index variable %s (%s))" % (t[-2], VerbosifyVariable(t[-2]), t[-1], VerbosifyVariable(t[-1])), r[1][0](s), r[2][0](t)])(s + GetFreeVariable(s, 2))],
        lambda r: [lambda s="": (lambda t: [r[0] + ": All (loop variable %s (%s), index variable %s (%s))" % (t[-2], VerbosifyVariable(t[-2]), t[-1], VerbosifyVariable(t[-1])), r[1][0](s), r[2][0](t)])(s + GetFreeVariable(s, 2))],
        lambda r: [lambda s="": (lambda t: [r[0] + ": Filter (loop variable %s (%s), index variable %s (%s))" % (t[-2], VerbosifyVariable(t[-2]), t[-1], VerbosifyVariable(t[-1])), r[1][0](s), r[2][0](t)])(s + GetFreeVariable(s, 2))],
        lambda r: [lambda s="": [r[0] + ": Evaluate variable"] + [el[0](s) for el in r[1:]]],
        lambda r: [lambda s="": [r[0] + ": Evaluate variable"] + [el[0](s) for el in r[1:]]],
        lambda r: [lambda s="": [r[0] + ": Evaluate variable"] + [el[0](s) for el in r[1:]]]
    ],

    CT.Program: [
        lambda r: [lambda s="": ["Program", r[0][0](s)] + r[2][0](s)[1:]],
        lambda r: [lambda s="": ["Program"]]
    ],
    CT.Body: [
        lambda r: [lambda s="": r[1]],
        lambda r: [lambda s="": r[1]],
        lambda r: [lambda s="": r[0]]
    ],
    CT.Command: [
        lambda r: [lambda s="": [r[0] + ": Input String", EvaluateFunctionOrList(r[1], s)]],
        lambda r: [lambda s="": [r[0] + ": Input Number", EvaluateFunctionOrList(r[1], s)]],
        lambda r: [lambda s="": [r[0] + ": Input", EvaluateFunctionOrList(r[1], s)]],
        lambda r: [lambda s="": [r[0] + ": Evaluate", r[1][0](s)]],
        lambda r: [lambda s="": ["Print"] + [el[0](s) for el in r]],
        lambda r: [lambda s="": ["Print"] + [el[0](s) for el in r]],
        lambda r: [lambda s="": [r[0] + ": Multiprint"] + [el[0](s) for el in r[1:]]],
        lambda r: [lambda s="": [r[0] + ": Multiprint"] + [el[0](s) for el in r[1:]]],
        lambda r: [lambda s="": [r[0] + ": Polygon"] + [el[0](s) for el in r[1:]]],
        lambda r: [lambda s="": [r[0] + ": Polygon"] + [el[0](s) for el in r[1:]]],
        lambda r: [lambda s="": [r[0] + ": Hollow Polygon"] + [el[0](s) for el in r[1:]]],
        lambda r: [lambda s="": [r[0] + ": Hollow Polygon"] + [el[0](s) for el in r[1:]]],
        lambda r: [lambda s="": [r[0] + ": Rectangle"] + [el[0](s) for el in r[1:]]],
        lambda r: [lambda s="": [r[0] + ": Rectangle"] + [el[0](s) for el in r[1:]]],
        lambda r: [lambda s="": [r[0] + ": Oblong"] + [el[0](s) for el in r[1:]]],
        lambda r: [lambda s="": [r[0] + ": Oblong"] + [el[0](s) for el in r[1:]]],
        lambda r: [lambda s="": [r[0] + ": Box"] + [el[0](s) for el in r[1:]]],
        lambda r: [lambda s="": [r[0] + ": Box"] + [el[0](s) for el in r[1:]]],
        lambda r: [lambda s="": ["Move"] + [el[0](s) for el in r]],
        lambda r: [lambda s="": [r[0] + ": Move"] + [el[0](s) for el in r[1:]]],
        lambda r: [lambda s="": [r[0] + ": Move"] + [el[0](s) for el in r[1:]]],
        lambda r: [lambda s="": [r[0] + ": Jump"] + [el[0](s) for el in r[1:]]],
        lambda r: [lambda s="": [r[0] + ": Pivot Left", r[1][0](s)]],
        lambda r: [lambda s="": [r[0] + ": Pivot Left"]],
        lambda r: [lambda s="": [r[0] + ": Pivot Right", r[1][0](s)]],
        lambda r: [lambda s="": [r[0] + ": Pivot Right"]],
        lambda r: [lambda s="": [r[0] + ": Jump to"] + [el[0](s) for el in r[1:]]],
        lambda r: [lambda s="": [r[0] + ": Rotate transform"] + [el[0](s) for el in r[1:]]],
        lambda r: [lambda s="": [r[0] + ": Rotate transform"]]
    ] +
    [lambda r: [lambda s="": [r[0] + ": Reflect transform"] + [el[0](s) for el in r[1:]]]] * 3 +
    [lambda r: [lambda s="": [r[0] + ": Rotate prism"] + [EvaluateFunctionOrList(el, s) for el in r[1:]]]] * 6 +
    [lambda r: [lambda s="": [r[0] + ": Reflect mirror"] + [el[0](s) for el in r[1:]]]] * 3 +
    [lambda r: [lambda s="": [r[0] + ": Rotate copy"] + [EvaluateFunctionOrList(el, s) for el in r[1:]]]] * 6 +
    [lambda r: [lambda s="": [r[0] + ": Reflect copy"] + [el[0](s) for el in r[1:]]]] * 3 +
    [lambda r: [lambda s="": [
        r[0] + ": Rotate overlap overlap"
    ] + [EvaluateFunctionOrList(el, s) for el in r[1:]]]] * 6 +
    [lambda r: [lambda s="": [r[0] + ": Rotate overlap"] + [EvaluateFunctionOrList(el, s) for el in r[1:]]]] * 6 +
    [lambda r: [lambda s="": [
        r[0] + ": Rotate shutter overlap"
    ] + [EvaluateFunctionOrList(el, s) for el in r[1:]]]] * 6 +
    [lambda r: [lambda s="": [r[0] + ": Rotate shutter"] + [EvaluateFunctionOrList(el, s) for el in r[1:]]]] * 6 +
    [lambda r: [lambda s="": [
        r[0] + ": Reflect overlap overlap"
    ] + [el[0](s) for el in r[1:]]]] * 3 +
    [lambda r: [lambda s="": [r[0] + ": Reflect overlap"] + [el[0](s) for el in r[1:]]]] * 3 +
    [lambda r: [lambda s="": [
        r[0] + ": Reflect butterfly overlap"
    ] + [el[0](s) for el in r[1:]]]] * 3 +
    [lambda r: [lambda s="": [r[0] + ": Reflect butterfly"] + [el[0](s) for el in r[1:]]]] * 3 +
    [
        lambda r: [lambda s="": [r[0] + ": Rotate"] + [el[0](s) for el in r[1:]]],
        lambda r: [lambda s="": [r[0] + ": Rotate"]],
        lambda r: [lambda s="": [r[0] + ": Reflect"] + [el[0](s) for el in r[1:]]],
        lambda r: [lambda s="": [r[0] + ": Reflect"]],
        lambda r: [lambda s="": [r[0] + ": Copy"] + [el[0](s) for el in r[1:]]],
        lambda r: [lambda s="": (lambda t: [r[0] + ": For (loop variable %s (%s))" % (t[-1], VerbosifyVariable(t[-1])), r[1][0](s), r[2][0](t)[0](t)])(s + GetFreeVariable(s))],
        lambda r: [lambda s="": (lambda t: [r[0] + ": While (loop variable %s (%s))" % (t[-1], VerbosifyVariable(t[-1])), r[1][0](t), r[2][0](t)[0](t)])(s + GetFreeVariable(s))],
        lambda r: [lambda s="": [r[0] + ": If", r[1][0](s)] + [el[0](s)[0](s) for el in r[2:]]],
        lambda r: [lambda s="": [r[0] + ": If", r[1][0](s)] + [el[0](s)[0](s) for el in r[2:]]],
        lambda r: [lambda s="": [r[0] + ": Assign at index"] + [el[0](s) for el in r[1:]]],
        lambda r: [lambda s="": (lambda t: [r[0] + ": Assign", r[1][0](s)] + [el(t) for el in r[2:]])(s + GetFreeVariable(s))],
        lambda r: [lambda s="": (lambda t: [r[0] + ": Assign"] + [el[0](t) for el in r[1:]])(s + GetFreeVariable(s))],
        lambda r: [lambda s="": [r[0] + ": Fill"] + [el[0](s) for el in r[1:]]],
        lambda r: [lambda s="": [r[0] + ": SetBackground", r[1][0](s)]],
        lambda r: [lambda s="": [r[0] + ": Dump"]],
        lambda r: [lambda s="": (lambda t: [r[0] + ": Refresh for (loop variable %s (%s))" % (t[-1], VerbosifyVariable(t[-1])), r[1][0](s), r[2][0](s), r[3][0](t)[0](t)])(s + GetFreeVariable(s))],
        lambda r: [lambda s="": (lambda t: [r[0] + ": Refresh while (loop variable %s (%s))" % (t[-1], VerbosifyVariable(t[-1])), r[1][0](s), r[2][0](t), r[3][0](t)[0](t)])(s + GetFreeVariable(s))],
        lambda r: [lambda s="": [r[0] + ": Refresh", r[1][0](s)]],
        lambda r: [lambda s="": [r[0] + ": Refresh"]],
        lambda r: [lambda s="": [r[0] + ": Toggle trim"]],
        lambda r: [lambda s="": [r[0] + ": Crop", r[1][0](s), r[2][0](s)]],
        lambda r: [lambda s="": [r[0] + ": Crop", r[1][0](s)]],
        lambda r: [lambda s="": [r[0] + ": Clear"]],
        lambda r: [lambda s="": [r[0] + ": Extend", r[1][0](s), r[2][0](s)]],
        lambda r: [lambda s="": [r[0] + ": Extend", r[1][0](s)]],
        lambda r: [lambda s="": [r[0] + ": Push"] + [el[0](s) for el in r[1:]]],
        lambda r: [lambda s="": [r[0] + ": Switch", r[2][0](s), r[3][0](s), r[4][0](s)[0](s)]],
        lambda r: [lambda s="": [r[0] + ": Switch", r[2][0](s), r[3][0](s)]],
        lambda r: [lambda s="": [r[0] + ": Switch", r[2][0](s), r[3][0](s), r[4][0](s)[0](s)]],
        lambda r: [lambda s="": [r[0] + ": Switch", r[2][0](s), r[3][0](s)]],
        lambda r: [lambda s="": [r[0] + ": Switch", r[1][0](s), r[2][0](s), r[3][0](s)[0](s)]],
        lambda r: [lambda s="": [r[0] + ": Switch", r[1][0](s), r[2][0](s)]],
        lambda r: [lambda s="": (lambda t: [r[0] + ": Map (loop variable %s (%s), index variable %s (%s))" % (t[-2], VerbosifyVariable(t[-2]), t[-1], VerbosifyVariable(t[-1])), r[1][0](s), r[2][0](t)])(s + GetFreeVariable(s, 2))],
        lambda r: [lambda s="": [r[0] + ": Execute variable"] + [el[0](s) for el in r[1:]]],
        lambda r: [lambda s="": [r[0] + ": Execute variable"] + [el[0](s) for el in r[1:]]],
        lambda r: [lambda s="": [r[0] + ": Map assign left", r[1][0](s)] + [EvaluateFunctionOrList(el, s) for el in r[2:]]],
        lambda r: [lambda s="": [r[0] + ": Map assign", r[1][0](s)] + [EvaluateFunctionOrList(el, s) for el in r[2:]]],
        lambda r: [lambda s="": [r[0] + ": Map assign right", r[1][0](s)] + [EvaluateFunctionOrList(el, s) for el in r[2:]]],
        lambda r: [lambda s="": [r[0] + ": Map assign", r[1][0](s)] + [EvaluateFunctionOrList(el, s) for el in r[2:]]],
        lambda r: [lambda s="": [r[0] + ": exec"] + [el[0](s) for el in r[1:]]]
    ]
}
