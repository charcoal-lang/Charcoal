from charcoaltoken import CharcoalToken as CT

VerboseGrammars = {
    CT.Arrow: [
        [":UpLeft"],
        [":UpRight"],
        [":DownRight"],
        [":DownLeft"],
        [":Left"],
        [":Up"],
        [":Right"],
        [":Down"]
    ],
    CT.Multidirectional: [
        [CT.Arrows, CT.Separator, CT.Multidirectional],
        [":+", CT.Separator, CT.Multidirectional],
        [":X", CT.Separator, CT.Multidirectional],
        [":All", CT.Separator, CT.Multidirectional],
        [":Vertical", CT.Separator, CT.Multidirectional],
        [":Horizontal", CT.Separator, CT.Multidirectional],
        [":\\", CT.Separator, CT.Multidirectional],
        [":/", CT.Separator, CT.Multidirectional],
        [":<", CT.Separator, CT.Multidirectional],
        [":>", CT.Separator, CT.Multidirectional],
        [":^", CT.Separator, CT.Multidirectional],
        [":K", CT.Separator, CT.Multidirectional],
        [":L", CT.Separator, CT.Multidirectional],
        [":T", CT.Separator, CT.Multidirectional],
        [":V", CT.Separator, CT.Multidirectional],
        [":Y", CT.Separator, CT.Multidirectional],
        [":7", CT.Separator, CT.Multidirectional],
        [":¬", CT.Separator, CT.Multidirectional],
        ["[", CT.Multidirectional, "]"],
        [CT.Separator]
    ],
    CT.Side: [
        [CT.Arrow, CT.Separator, CT.Expression]
    ],
    CT.Separator: [[";"], [","], []],
    CT.Span: [
        [CT.Expression, ";;", CT.Expression, ";;", CT.Expression],
        [CT.Expression, ";;", ";;", CT.Expression],
        [CT.Expression, ";;", CT.Expression],
        [CT.Expression, ";;"],
        [";;", CT.Expression, ";;", CT.Expression],
        [";;", CT.Expression],
        [";;", ";;", CT.Expression],
        [";;", ";;"]
    ],
    CT.Arrows: [[CT.Arrow, CT.Separator, CT.Arrows], [CT.Arrow]],
    CT.Sides: [[CT.Side, CT.Separator, CT.Sides], [CT.Side]],
    CT.Expressions: [[CT.Expression, CT.Expressions], [CT.Expression]],
    CT.WolframExpressions: [
        [CT.WolframExpression, CT.WolframExpressions],
        [CT.WolframExpression]
    ],
    CT.PairExpressions: [
        [CT.Expression, CT.Expression, CT.PairExpressions],
        [CT.Expression, CT.Expression]
    ],
    CT.Cases: [
        ["case", CT.Expression, ":", CT.Body, CT.Separator, CT.Cases],
        []
    ],
    CT.List: [["[", CT.Expressions, "]"], ["[", "]"]],
    CT.WolframList: [["[", CT.WolframExpressions, "]"], ["[", "]"]],
    CT.Dictionary: [["{", CT.PairExpressions, "}"], ["{", "}"]],
    CT.WolframExpression: [[CT.Span, CT.Separator], [CT.Expression]],
    CT.Expression: [
        [CT.Number, CT.Separator],
        [CT.String, CT.Separator],
        [CT.Name, CT.Separator],
        [CT.List, CT.Separator],
        [CT.Dictionary, CT.Separator],
        ["{", CT.Program, "}", CT.Separator],
        [CT.OtherOperator, CT.Separator],
        [
            CT.LazyQuarternary, "(", CT.Expression, CT.Expression,
            CT.Expression, CT.Expression, ")", CT.Separator
        ],
        [
            CT.Quarternary, "(", CT.Expression, CT.Expression, CT.Expression,
            CT.Expression, ")", CT.Separator
        ],
        [
            CT.LazyTernary, "(", CT.Expression, CT.Expression, CT.Expression,
            ")", CT.Separator
        ],
        [
            CT.Ternary, "(", CT.Expression, CT.Expression, CT.Expression, ")",
            CT.Separator
        ],
        [CT.LazyBinary, "(", CT.Expression, CT.Expression, ")", CT.Separator],
        [CT.Binary, "(", CT.Expression, CT.Expression, ")", CT.Separator],
        [CT.LazyUnary, "(", CT.Expression, ")", CT.Separator],
        [CT.Unary, "(", CT.Expression, ")", CT.Separator],
        [CT.Nilary, "(", ")", CT.Separator]
    ],
    CT.Nilary: [
        ["InputString"], ["InputNumber"], ["Random"], ["PeekAll"],
        ["PeekMoore"], ["PeekVonNeumann"], ["Peek"]
    ],
    CT.Unary: [
        ["Negate"], ["Length"], ["Not"], ["Cast"], ["Random"], ["Evaluate"],
        ["eval"], ["Pop"], ["Lowercase"], ["Uppercase"], ["Minimum"],
        ["Maximum"], ["Character"], ["Ordinal"], ["chr"], ["ord"], ["Reverse"],
        ["GetVariable"], ["Repeated"], ["RepeatedNull"], ["Slice"],
        ["InclusiveRange"], ["Range"], ["~"], ["BitwiseNot"]
    ],
    CT.Binary: [
        ["**"], ["+"], ["Add"], ["Plus"], ["-"], ["Subtract"], ["Minus"], ["*"],
        ["Multiply"], ["Times"], ["\\"], ["/"], ["Divide"], ["IntDivide"],
        ["IntegerDivide"], ["%"], ["Modulo"], ["=="], ["Equals"], ["<"],
        ["Less"], [">"], ["Greater"], ["&"], ["BitwiseAnd"], ["|"],
        ["BitwiseOr"], ["InclusiveRange"], ["Range"], ["Mold"], ["CycleChop"],
        ["Exponentiate"], ["Exponent"], ["Power"], ["AtIndex"],
        ["PushOperator"], ["Join"], ["Split"], ["FindAll"], ["Find"],
        ["PadLeft"], ["PadRight"], ["Count"], ["Rule"], ["DelayedRule"],
        ["PatternTest"], ["Slice"]
    ],
    CT.Ternary: [["Slice"]],
    CT.Quarternary: [["Slice"]],
    CT.LazyUnary: [],
    CT.LazyBinary: [["And"], ["Or"], ["and"], ["or"]],
    CT.LazyTernary: [["Ternary"]],
    CT.LazyQuarternary: [],
    CT.OtherOperator: [
        ["PeekDirection", "(", CT.Expression, CT.Arrow, ")"],
        ["Each", "(", CT.Expression, CT.Expression, ")"],
        ["Map", "(", CT.Expression, CT.Expression, ")"],
        ["PythonFunction", "(", CT.Expression, CT.List, ")"],
        ["PythonFunction", "(", CT.Expression, ")"],
        ["EvaluateVariable", "(", CT.Expression, CT.WolframList, ")"],
        ["evalvar", "(", CT.Expression, CT.WolframList, ")"]
    ],
    CT.Program: [[CT.Command, CT.Separator, CT.Separator, CT.Program], []],
    CT.Body: [["{", CT.Program, "}"], [CT.Command]],
    CT.Command: [
        ["PythonFunction", "(", CT.Expression, CT.Expression, ")"],
        ["PythonFunction", "(", CT.Expression, ")"],
        ["InputString", "(", CT.Name, ")"],
        ["InputNumber", "(", CT.Name, ")"],
        ["Evaluate", "(", CT.Expression, ")"],
        ["eval", "(", CT.Expression, ")"],
        ["Print", "(", CT.Arrow, CT.Separator, CT.Expression, ")"],
        ["Print", "(", CT.Expression, ")"],
        [
            "Multiprint", "(", CT.Multidirectional, CT.Separator, CT.Expression,
            ")"
        ],
        ["Multiprint", "(", CT.Expression, ")"],
        ["Polygon", "(", CT.Sides, CT.Separator, CT.Expression, ")"],
        [
            "Polygon", "(", CT.Multidirectional, CT.Separator, CT.Expression,
            CT.Expression, ")"
        ],
        ["PolygonHollow", "(", CT.Sides, CT.Separator, CT.Expression, ")"],
        [
            "PolygonHollow", "(", CT.Multidirectional, CT.Separator,
            CT.Expression, CT.Expression, ")"
        ],
        ["Rectangle", "(", CT.Expression, CT.Expression, ")"],
        ["Rectangle", "(", CT.Expression, ")"],
        ["Oblong", "(", CT.Expression, CT.Expression, CT.Expression, ")"],
        ["Oblong", "(", CT.Expression, CT.Expression, ")"],
        ["Box", "(", CT.Expression, CT.Expression, CT.Expression, ")"],
        ["Box", "(", CT.Expression, CT.Expression, ")"],
        ["Move", "(", CT.Arrow, ")"],
        ["Move", "(", CT.Expression, CT.Arrow, ")"],
        ["Move", "(", CT.Expression, CT.Expression, ")"],
        ["Jump", "(", CT.Expression, CT.Expression, ")"],
        ["PivotLeft", "(", CT.Expression, ")"],
        ["PivotLeft", "(", ")"],
        ["PivotRight", "(", CT.Expression, ")"],
        ["PivotRight", "(", ")"],
        ["JumpTo", "(", CT.Expression, CT.Expression, ")"],
        ["RotateTransform", "(", CT.Expression, ")"],
        ["RotateTransform", "(", ")"],
        ["ReflectTransform", "(", CT.Multidirectional, ")"],
        ["ReflectTransform", "(", CT.Arrow, ")"],
        ["ReflectTransform", "(", ")"],
        ["RotatePrism", "(", CT.Arrow, CT.Separator, CT.Expression, ")"],
        ["RotatePrism", "(", CT.Arrow, ")"],
        ["RotatePrism", "(", CT.Expression, ")"],
        ["RotatePrism", "(", ")"],
        ["ReflectMirror", "(", CT.Multidirectional, ")"],
        ["ReflectMirror", "(", CT.Arrow, ")"],
        ["ReflectMirror", "(", ")"],
        ["RotateCopy", "(", CT.Arrow, CT.Separator, CT.Expression, ")"],
        ["RotateCopy", "(", CT.Arrow, ")"],
        ["RotateCopy", "(", CT.Expression, ")"],
        ["RotateCopy", "(", ")"],
        ["ReflectCopy", "(", CT.Multidirectional, ")"],
        ["ReflectCopy", "(", CT.Arrow, ")"],
        ["ReflectCopy", "(", ")"],
        [
            "RotateOverlapOverlap", "(", CT.Arrow, CT.Separator, CT.Number,
            CT.Separator, CT.Expression, CT.Separator, CT.Expression, ")"
        ],
        [
            "RotateOverlapOverlap", "(", CT.Arrow, CT.Separator, CT.Expression,
            CT.Separator, CT.Expression, ")"
        ],
        [
            "RotateOverlapOverlap", "(", CT.Arrow, CT.Separator, CT.Expression,
            ")"
        ],
        ["RotateOverlapOverlap", "(", CT.Expression, CT.Expression, ")"],
        ["RotateOverlapOverlap", "(", CT.Expression, ")"],
        ["RotateOverlap", "(", CT.Arrow, CT.Separator, CT.Expression, ")"],
        ["RotateOverlap", "(", CT.Arrow, ")"],
        ["RotateOverlap", "(", CT.Expression, ")"],
        ["RotateOverlap", "(", ")"],
        [
            "RotateShutterOverlap", "(", CT.Arrow, CT.Separator, CT.Number,
            CT.Separator, CT.Expression, CT.Separator, CT.Expression, ")"
        ],
        [
            "RotateShutterOverlap", "(", CT.Arrow, CT.Separator, CT.Expression,
            CT.Separator, CT.Expression, ")"
        ],
        [
            "RotateShutterOverlap", "(", CT.Arrow, CT.Separator, CT.Expression,
            ")"
        ],
        ["RotateShutterOverlap", "(", CT.Expression, CT.Expression, ")"],
        ["RotateShutterOverlap", "(", CT.Expression, ")"],
        ["RotateShutter", "(", CT.Arrow, CT.Separator, CT.Expression, ")"],
        ["RotateShutter", "(", CT.Arrow, ")"],
        ["RotateShutter", "(", CT.Expression, ")"],
        ["RotateShutter", "(", ")"],
        [
            "ReflectOverlapOverlap", "(", CT.Multidirectional, CT.Separator,
            CT.Expression, ")"
        ],
        [
            "ReflectOverlapOverlap", "(", CT.Arrow, CT.Separator, CT.Expression,
            ")"
        ],
        ["ReflectOverlapOverlap", "(", CT.Expression, ")"],
        ["ReflectOverlap", "(", CT.Multidirectional, ")"],
        ["ReflectOverlap", "(", CT.Arrow, ")"],
        ["ReflectOverlap", "(", ")"],
        [
            "ReflectButterflyOverlap", "(", CT.Multidirectional, CT.Separator,
            CT.Expression, ")"
        ],
        [
            "ReflectButterflyOverlap", "(", CT.Arrow, CT.Separator,
            CT.Expression, ")"
        ],
        ["ReflectButterflyOverlap", "(", CT.Expression, ")"],
        ["ReflectButterfly", "(", CT.Multidirectional, ")"],
        ["ReflectButterfly", "(", CT.Arrow, ")"],
        ["ReflectButterfly", "(", ")"],
        ["Rotate", "(", CT.Expression, ")"],
        ["Rotate", "(", ")"],
        ["Reflect", "(", CT.Arrow, ")"],
        ["Reflect", "(", ")"],
        ["Copy", "(", CT.Expression, CT.Expression, ")"],
        ["for", "(", CT.Expression, ")", CT.Body],
        ["while", "(", CT.Expression, ")", CT.Body],
        ["if", "(", CT.Expression, ")", CT.Body, "else", CT.Body],
        ["if", "(", CT.Expression, ")", CT.Body],
        [
            "AssignAtIndex", "(", CT.Expression, CT.Expression, CT.Expression,
            ")"
        ],
        ["Assign", "(", CT.Expression, CT.Name, ")"],
        ["Assign", "(", CT.Expression, CT.Expression, ")"],
        ["Fill", "(", CT.Expression, ")"],
        ["SetBackground", "(", CT.Expression, ")"],
        ["Dump", "(", ")"],
        ["RefreshFor", "(", CT.Expression, CT.Expression, ")", CT.Body],
        ["RefreshWhile", "(", CT.Expression, CT.Expression, ")", CT.Body],
        ["Refresh", "(", CT.Expression, ")"],
        ["Refresh", "(", ")"],
        ["ToggleTrim", "(", ")"],
        ["Trim", "(", CT.Expression, CT.Expression, ")"],
        ["Trim", "(", CT.Expression, ")"],
        ["Clear", "(", ")"],
        ["Extend", "(", CT.Expression, CT.Expression, ")"],
        ["Extend", "(", CT.Expression, ")"],
        ["Push", "(", CT.Expression, CT.Expression, ")"],
        [
            "switch", "(", CT.Expression, ")", "{", CT.Cases, "default", ":",
            CT.Body, "}"
        ],
        ["switch", "(", CT.Expression, ")", "{", CT.Cases, "}"],
        ["MapCommand", "(", CT.Expression, CT.Expression, ")"],
        ["ExecuteVariable", "(", CT.Expression, CT.WolframList, ")"],
        ["execvar", "(", CT.Expression, CT.WolframList, ")"],
        ["SetVariable", "(", CT.Expression, CT.Expression, ")"]
    ]
}
