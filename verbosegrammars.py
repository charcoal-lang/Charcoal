from charcoaltoken import CharcoalToken

VerboseGrammars = {
    CharcoalToken.Arrow: [
        [":UpLeft"],
        [":UpRight"],
        [":DownRight"],
        [":DownLeft"],
        [":Left"],
        [":Up"],
        [":Right"],
        [":Down"]
    ],
    CharcoalToken.Multidirectional: [
        [CharcoalToken.Arrows],
        [":+", CharcoalToken.Separator, CharcoalToken.Multidirectional],
        [":X", CharcoalToken.Separator, CharcoalToken.Multidirectional],
        [":All", CharcoalToken.Separator, CharcoalToken.Multidirectional],
        [":Vertical", CharcoalToken.Separator, CharcoalToken.Multidirectional],
        [":Horizontal", CharcoalToken.Separator, CharcoalToken.Multidirectional],
        [":\\", CharcoalToken.Separator, CharcoalToken.Multidirectional],
        [":/", CharcoalToken.Separator, CharcoalToken.Multidirectional],
        [":<", CharcoalToken.Separator, CharcoalToken.Multidirectional],
        [":>", CharcoalToken.Separator, CharcoalToken.Multidirectional],
        [":^", CharcoalToken.Separator, CharcoalToken.Multidirectional],
        [":K", CharcoalToken.Separator, CharcoalToken.Multidirectional],
        [":L", CharcoalToken.Separator, CharcoalToken.Multidirectional],
        [":T", CharcoalToken.Separator, CharcoalToken.Multidirectional],
        [":V", CharcoalToken.Separator, CharcoalToken.Multidirectional],
        [":Y", CharcoalToken.Separator, CharcoalToken.Multidirectional],
        [":7", CharcoalToken.Separator, CharcoalToken.Multidirectional],
        [":¬", CharcoalToken.Separator, CharcoalToken.Multidirectional],
        []
    ],
    CharcoalToken.Side: [
        [CharcoalToken.Arrow, CharcoalToken.Separator, CharcoalToken.Expression]
    ],
    CharcoalToken.Separator: [
        [";"],
        [","],
        []
    ],
    CharcoalToken.Span: [
        [
            CharcoalToken.Expression,
            ";;",
            CharcoalToken.Expression,
            ";;",
            CharcoalToken.Expression
        ],
        [CharcoalToken.Expression, ";;", ";;", CharcoalToken.Expression],
        [CharcoalToken.Expression, ";;", CharcoalToken.Expression],
        [CharcoalToken.Expression, ";;"],
        [";;", CharcoalToken.Expression, ";;", CharcoalToken.Expression],
        [";;", CharcoalToken.Expression],
        [";;", ";;", CharcoalToken.Expression],
        [";;", ";;"]
    ],

    CharcoalToken.Arrows: [
        [CharcoalToken.Arrow, CharcoalToken.Separator, CharcoalToken.Arrows],
        [CharcoalToken.Arrow]
    ],
    CharcoalToken.Sides: [
        [CharcoalToken.Side, CharcoalToken.Separator, CharcoalToken.Sides],
        [CharcoalToken.Side]
    ],
    CharcoalToken.Expressions: [
        [
            CharcoalToken.Expression,
            CharcoalToken.Expressions
        ],
        [CharcoalToken.Expression]
    ],
    CharcoalToken.WolframExpressions: [
        [
            CharcoalToken.WolframExpression,
            CharcoalToken.WolframExpressions
        ],
        [CharcoalToken.WolframExpression]
    ],
    CharcoalToken.PairExpressions: [
        [
            CharcoalToken.Expression,
            CharcoalToken.Expression,
            CharcoalToken.PairExpressions
        ],
        [CharcoalToken.Expression, CharcoalToken.Expression]
    ],
    CharcoalToken.Cases: [
        [
            "case",
            CharcoalToken.Expression,
            ":",
            CharcoalToken.Body,
            CharcoalToken.Separator,
            CharcoalToken.Cases
        ],
        []
    ],

    CharcoalToken.List: [
        ["[", CharcoalToken.Expressions, "]"],
        ["[", "]"]
    ],
    CharcoalToken.WolframList: [
        ["[", CharcoalToken.WolframExpressions, "]"],
        ["[", "]"]
    ],
    CharcoalToken.ArrowList: [
        ["[", CharcoalToken.Multidirectional, "]"],
        ["[", "]"]
    ],
    CharcoalToken.Dictionary: [
        ["{", CharcoalToken.PairExpressions, "}"],
        ["{", "}"]
    ],

    CharcoalToken.WolframExpression: [
        [CharcoalToken.Span, CharcoalToken.Separator],
        [CharcoalToken.Expression]
    ],
    CharcoalToken.Expression: [
        [CharcoalToken.Number, CharcoalToken.Separator],
        [CharcoalToken.String, CharcoalToken.Separator],
        [CharcoalToken.Name, CharcoalToken.Separator],
        [CharcoalToken.List, CharcoalToken.Separator],
        [CharcoalToken.Dictionary, CharcoalToken.Separator],
        ["{", CharcoalToken.Program, "}", CharcoalToken.Separator],
        [
            CharcoalToken.OtherOperator,
            CharcoalToken.Separator
        ],
        [
            CharcoalToken.LazyTernary,
            "(",
            CharcoalToken.Expression,
            CharcoalToken.Expression,
            CharcoalToken.Expression,
            ")",
            CharcoalToken.Separator
        ],
        [
            CharcoalToken.Ternary,
            "(",
            CharcoalToken.Expression,
            CharcoalToken.Expression,
            CharcoalToken.Expression,
            ")",
            CharcoalToken.Separator
        ],
        [
            CharcoalToken.LazyBinary,
            "(",
            CharcoalToken.Expression,
            CharcoalToken.Expression,
            ")",
            CharcoalToken.Separator
        ],
        [
            CharcoalToken.Binary,
            "(",
            CharcoalToken.Expression,
            CharcoalToken.Expression,
            ")",
            CharcoalToken.Separator
        ],
        [
            CharcoalToken.LazyUnary,
            "(",
            CharcoalToken.Expression,
            ")",
            CharcoalToken.Separator
        ],
        [
            CharcoalToken.Unary,
            "(",
            CharcoalToken.Expression,
            ")",
            CharcoalToken.Separator
        ],
        [CharcoalToken.Nilary, "(", ")", CharcoalToken.Separator]
    ],
    CharcoalToken.Nilary: [
        ["InputString"],
        ["InputNumber"],
        ["Random"],
        ["PeekAll"],
        ["PeekMoore"],
        ["PeekVonNeumann"],
        ["Peek"]
    ],
    CharcoalToken.Unary: [
        ["Negate"],
        ["Length"],
        ["Not"],
        ["Cast"],
        ["Random"],
        ["Evaluate"],
        ["eval"],
        ["Pop"],
        ["Lowercase"],
        ["Uppercase"],
        ["Minimum"],
        ["Maximum"],
        ["Character"],
        ["Ordinal"],
        ["chr"],
        ["ord"],
        ["Reverse"],
        ["GetVariable"],
        ["Repeated"],
        ["RepeatedNull"]
    ],
    CharcoalToken.Binary: [
        ["**"],
        ["+"],
        ["Add"],
        ["Plus"],
        ["-"],
        ["Subtract"],
        ["Minus"],
        ["*"],
        ["Multiply"],
        ["Times"],
        ["//"],
        ["/"],
        ["Divide"],
        ["IntDivide"],
        ["IntegerDivide"],
        ["%"],
        ["Modulo"],
        ["=="],
        ["Equals"],
        ["<"],
        ["Less"],
        [">"],
        ["Greater"],
        ["InclusiveRange"],
        ["Range"],
        ["Mold"],
        ["CycleChop"],
        ["Exponentiate"],
        ["Exponent"],
        ["Power"],
        ["AtIndex"],
        ["PushOperator"],
        ["Join"],
        ["Split"],
        ["FindAll"],
        ["Find"],
        ["PadLeft"],
        ["PadRight"],
        ["Count"],
        ["Rule"],
        ["DelayedRule"],
        ["PatternTest"]
    ],
    CharcoalToken.Ternary: [
    ],
    CharcoalToken.LazyUnary: [
    ],
    CharcoalToken.LazyBinary: [
        ["And"],
        ["Or"],
        ["and"],
        ["or"]
    ],
    CharcoalToken.LazyTernary: [
        ["Ternary"]
    ],
    CharcoalToken.OtherOperator: [
        [
            "PeekDirection",
            "(",
            CharcoalToken.Expression,
            CharcoalToken.Arrow,
            ")"
        ],
        [
            "Each",
            "(",
            CharcoalToken.Expression,
            CharcoalToken.Expression,
            ")"
        ],
        [
            "Map",
            "(",
            CharcoalToken.Expression,
            CharcoalToken.Expression,
            ")"
        ],
        [
            "PythonFunction",
            "(",
            CharcoalToken.Expression,
            CharcoalToken.List,
            ")"
        ],
        [
            "PythonFunction",
            "(",
            CharcoalToken.Expression,
            ")"
        ],
        [
            "EvaluateVariable",
            "(",
            CharcoalToken.Expression,
            CharcoalToken.WolframList,
            ")"
        ],
        [
            "evalvar",
            "(",
            CharcoalToken.Expression,
            CharcoalToken.WolframList,
            ")"
        ]
    ],

    CharcoalToken.Program: [
        [
            CharcoalToken.Command,
            CharcoalToken.Separator,
            CharcoalToken.Program
        ],
        []
    ],
    CharcoalToken.Body: [
        ["{", CharcoalToken.Program, "}"],
        [CharcoalToken.Command]
    ],
    CharcoalToken.Command: [
        [
            "PythonFunction",
            "(",
            CharcoalToken.Expression,
            CharcoalToken.List,
            ")"
        ],
        [
            "PythonFunction",
            "(",
            CharcoalToken.Expression,
            ")"
        ],
        ["InputString", "(", CharcoalToken.Name, ")"],
        ["InputNumber", "(", CharcoalToken.Name, ")"],
        ["Evaluate", "(", CharcoalToken.Expression, ")"],
        ["eval", "(", CharcoalToken.Expression, ")"],
        [
            "Print",
            "(",
            CharcoalToken.Arrow,
            CharcoalToken.Separator,
            CharcoalToken.Expression,
            ")"
        ],
        ["Print", "(", CharcoalToken.Expression, ")"],
        [
            "Multiprint",
            "(",
            CharcoalToken.Multidirectional,
            CharcoalToken.Separator,
            CharcoalToken.Expression,
            ")"
        ],
        ["Multiprint", "(", CharcoalToken.Expression, ")"],
        ["Polygon", "(", CharcoalToken.Sides, CharcoalToken.Separator, CharcoalToken.Expression, ")"],
        [
            "Polygon",
            "(",
            CharcoalToken.Multidirectional,
            CharcoalToken.Separator,
            CharcoalToken.Expression,
            CharcoalToken.Expression,
            ")"
        ],
        ["PolygonHollow", "(", CharcoalToken.Sides, CharcoalToken.Separator, CharcoalToken.Expression, ")"],
        [
            "PolygonHollow",
            "(",
            CharcoalToken.Multidirectional,
            CharcoalToken.Separator,
            CharcoalToken.Expression,
            CharcoalToken.Expression,
            ")"
        ],
        ["Rectangle", "(", CharcoalToken.Expression, CharcoalToken.Expression, ")"],
        ["Rectangle", "(", CharcoalToken.Expression, ")"],
        [
            "Oblong",
            "(",
            CharcoalToken.Expression,
            CharcoalToken.Expression,
            CharcoalToken.Expression,
            ")"
        ],
        ["Oblong", "(", CharcoalToken.Expression, CharcoalToken.Expression, ")"],
        [
            "Box",
            "(",
            CharcoalToken.Expression,
            CharcoalToken.Expression,
            CharcoalToken.Expression,
            ")"
        ],
        ["Box", "(", CharcoalToken.Expression, CharcoalToken.Expression, ")"],
        ["Move", "(", CharcoalToken.Arrow, ")"],
        ["Move", "(", CharcoalToken.Expression, CharcoalToken.Arrow, ")"],
        ["Move", "(", CharcoalToken.Expression, CharcoalToken.Expression, ")"],
        ["Jump", "(", CharcoalToken.Expression, CharcoalToken.Expression, ")"],
        ["PivotLeft", "(", CharcoalToken.Expression, ")"],
        ["PivotLeft", "(", ")"],
        ["PivotRight", "(", CharcoalToken.Expression, ")"],
        ["PivotRight", "(", ")"],
        ["JumpTo", "(", CharcoalToken.Expression, CharcoalToken.Expression, ")"],
        ["RotateTransform", "(", CharcoalToken.Expression, ")"],
        ["RotateTransform", "(", ")"],
        ["ReflectTransform", "(", CharcoalToken.ArrowList, ")"],
        ["ReflectTransform", "(", CharcoalToken.Arrow, ")"],
        ["ReflectTransform", "(", ")"],
        [
            "RotatePrism",
            "(",
            CharcoalToken.Arrow,
            CharcoalToken.Separator,
            CharcoalToken.Expression,
            ")"
        ],
        [
            "RotatePrism",
            "(",
            CharcoalToken.Arrow,
            ")"
        ],
        ["RotatePrism", "(", CharcoalToken.Expression, ")"],
        ["RotatePrism", "(", ")"],
        ["ReflectMirror", "(", CharcoalToken.ArrowList, ")"],
        ["ReflectMirror", "(", CharcoalToken.Arrow, ")"],
        ["ReflectMirror", "(", ")"],
        [
            "RotateCopy",
            "(",
            CharcoalToken.Arrow,
            CharcoalToken.Separator,
            CharcoalToken.List,
            ")"
        ],
        [
            "RotateCopy",
            "(",
            CharcoalToken.Arrow,
            CharcoalToken.Separator,
            CharcoalToken.Expression,
            ")"
        ],
        ["RotateCopy", "(", CharcoalToken.List, ")"],
        ["RotateCopy", "(", CharcoalToken.Arrow, ")"],
        ["RotateCopy", "(", CharcoalToken.Expression, ")"],
        ["RotateCopy", "(", ")"],
        ["ReflectCopy", "(", CharcoalToken.ArrowList, ")"],
        ["ReflectCopy", "(", CharcoalToken.Arrow, ")"],
        ["ReflectCopy", "(", ")"],
        [
            "RotateOverlapOverlap",
            "(",
            CharcoalToken.Arrow,
            CharcoalToken.Separator,
            CharcoalToken.List,
            CharcoalToken.Expression,
            ")"
        ],
        [
            "RotateOverlapOverlap",
            "(",
            CharcoalToken.Arrow,
            CharcoalToken.Separator,
            CharcoalToken.Expression,
            ")"
        ],
        [
            "RotateOverlapOverlap",
            "(",
            CharcoalToken.Arrow,
            CharcoalToken.Expression,
            ")"
        ],
        [
            "RotateOverlapOverlap",
            "(",
            CharcoalToken.List,
            CharcoalToken.Expression,
            ")"
        ],
        [
            "RotateOverlapOverlap",
            "(",
            CharcoalToken.Expression,
            CharcoalToken.Expression,
            ")"
        ],
        ["RotateOverlapOverlap", "(", CharcoalToken.Expression, ")"],
        [
            "RotateOverlap",
            "(",
            CharcoalToken.Arrow,
            CharcoalToken.Separator,
            CharcoalToken.List,
            ")"
        ],
        [
            "RotateOverlap",
            "(",
            CharcoalToken.Arrow,
            CharcoalToken.Separator,
            CharcoalToken.Expression,
            ")"
        ],
        ["RotateOverlap", "(", CharcoalToken.Arrow, ")"],
        ["RotateOverlap", "(", CharcoalToken.List, ")"],
        ["RotateOverlap", "(", CharcoalToken.Expression, ")"],
        ["RotateOverlap", "(", ")"],
        [
            "RotateShutterOverlap",
            "(",
            CharcoalToken.Arrow,
            CharcoalToken.Separator,
            CharcoalToken.List,
            CharcoalToken.Expression,
            ")"
        ],
        [
            "RotateShutterOverlap",
            "(",
            CharcoalToken.Arrow,
            CharcoalToken.Separator,
            CharcoalToken.Expression,
            ")"
        ],
        [
            "RotateShutterOverlap",
            "(",
            CharcoalToken.Arrow,
            CharcoalToken.Expression,
            ")"
        ],
        [
            "RotateShutterOverlap",
            "(",
            CharcoalToken.List,
            CharcoalToken.Expression,
            ")"
        ],
        [
            "RotateShutterOverlap",
            "(",
            CharcoalToken.Expression,
            CharcoalToken.Expression,
            ")"
        ],
        ["RotateShutterOverlap", "(", CharcoalToken.Expression, ")"],
        [
            "RotateShutter",
            "(",
            CharcoalToken.Arrow,
            CharcoalToken.Separator,
            CharcoalToken.List,
            ")"
        ],
        [
            "RotateShutter",
            "(",
            CharcoalToken.Arrow,
            CharcoalToken.Separator,
            CharcoalToken.Expression,
            ")"
        ],
        ["RotateShutter", "(", CharcoalToken.Arrow, ")"],
        ["RotateShutter", "(", CharcoalToken.List, ")"],
        ["RotateShutter", "(", CharcoalToken.Expression, ")"],
        ["RotateShutter", "(", ")"],
        [
            "ReflectOverlapOverlap",
            "(",
            CharcoalToken.ArrowList,
            CharcoalToken.Expression,
            ")"
        ],
        [
            "ReflectOverlapOverlap",
            "(",
            CharcoalToken.Arrow,
            CharcoalToken.Expression,
            ")"
        ],
        ["ReflectOverlapOverlap", "(", CharcoalToken.Expression, ")"],
        ["ReflectOverlap", "(", CharcoalToken.ArrowList, ")"],
        ["ReflectOverlap", "(", CharcoalToken.Arrow, ")"],
        ["ReflectOverlap", "(", ")"],
        [
            "ReflectButterflyOverlap",
            "(",
            CharcoalToken.ArrowList,
            CharcoalToken.Expression,
            ")"
        ],
        [
            "ReflectButterflyOverlap",
            "(",
            CharcoalToken.Arrow,
            CharcoalToken.Expression,
            ")"
        ],
        ["ReflectButterflyOverlap", "(", CharcoalToken.Expression, ")"],
        ["ReflectButterfly", "(", CharcoalToken.ArrowList, ")"],
        ["ReflectButterfly", "(", CharcoalToken.Arrow, ")"],
        ["ReflectButterfly", "(", ")"],
        ["Rotate", "(", CharcoalToken.Expression, ")"],
        ["Rotate", "(", ")"],
        ["Reflect", "(", CharcoalToken.Arrow, ")"],
        ["Reflect", "(", ")"],
        ["Copy", "(", CharcoalToken.Expression, CharcoalToken.Expression, ")"],
        ["for", "(", CharcoalToken.Expression, ")", CharcoalToken.Body],
        ["while", "(", CharcoalToken.Expression, ")", CharcoalToken.Body],
        [
            "if",
            "(",
            CharcoalToken.Expression,
            ")",
            CharcoalToken.Body,
            "else",
            CharcoalToken.Body
        ],
        ["if", "(", CharcoalToken.Expression, ")", CharcoalToken.Body],
        [
            "AssignAtIndex",
            "(",
            CharcoalToken.Expression,
            CharcoalToken.Expression,
            CharcoalToken.Expression,
            ")"
        ],
        ["Assign", "(", CharcoalToken.Expression, CharcoalToken.Name, ")"],
        ["Assign", "(", CharcoalToken.Expression, CharcoalToken.Expression, ")"],
        ["Fill", "(", CharcoalToken.Expression, ")"],
        ["SetBackground", "(", CharcoalToken.Expression, ")"],
        ["Dump", "(", ")"],
        [
            "RefreshFor",
            "(",
            CharcoalToken.Expression,
            CharcoalToken.Expression,
            ")",
            CharcoalToken.Body
        ],
        [
            "RefreshWhile",
            "(",
            CharcoalToken.Expression,
            CharcoalToken.Expression,
            ")",
            CharcoalToken.Body
        ],
        ["Refresh", "(", CharcoalToken.Expression, ")"],
        ["Refresh", "(", ")"],
        ["ToggleTrim", "(", ")"],
        ["Trim", "(", CharcoalToken.Expression, CharcoalToken.Expression, ")"],
        ["Trim", "(", CharcoalToken.Expression, ")"],
        ["Clear", "(", ")"],
        [
            "Extend",
            "(",
            CharcoalToken.Expression,
            CharcoalToken.Expression,
            ")"
        ],
        ["Extend", "(", CharcoalToken.Expression, ")"],
        [
            "Push",
            "(",
            CharcoalToken.Expression,
            CharcoalToken.Expression,
            ")"
        ],
        [
            "switch",
            "(",
            CharcoalToken.Expression,
            ")",
            "{",
            CharcoalToken.Cases,
            "default",
            ":",
            CharcoalToken.Body,
            "}"
        ],
        [
            "switch",
            "(",
            CharcoalToken.Expression,
            ")",
            "{",
            CharcoalToken.Cases,
            "}"
        ],
        [
            "MapCommand",
            "(",
            CharcoalToken.Expression,
            CharcoalToken.Expression,
            ")"
        ],
        [
            "ExecuteVariable",
            "(",
            CharcoalToken.Expression,
            CharcoalToken.WolframList,
            ")"
        ],
        [
            "execvar",
            "(",
            CharcoalToken.Expression,
            CharcoalToken.WolframList,
            ")"
        ],
        [
            "SetVariable",
            "(",
            CharcoalToken.Expression,
            CharcoalToken.Expression,
            ")"
        ]
    ]
}

