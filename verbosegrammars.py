from charcoaltoken import CharcoalToken as CT

VerboseGrammars = {
    CT.LP: [["("], []],
    CT.RP: [[")"], []],
    CT.Arrow: [
        [":UpLeft"],
        [":UpRight"],
        [":DownRight"],
        [":DownLeft"],
        [":Left"],
        [":Up"],
        [":Right"],
        [":Down"],
        [":UL"],
        [":UR"],
        [":DR"],
        [":DL"],
        [":L"],
        [":U"],
        [":R"],
        [":D"],
        ["Direction", CT.LP, CT.Expression, CT.RP]
    ],
    CT.Multidirectional: [
        [CT.Arrows, CT.Separator, CT.Multidirectional],
        [":+", CT.Separator, CT.Multidirectional],
        [":X", CT.Separator, CT.Multidirectional],
        [":*", CT.Separator, CT.Multidirectional],
        [":All", CT.Separator, CT.Multidirectional],
        [":|", CT.Separator, CT.Multidirectional],
        [":Vertical", CT.Separator, CT.Multidirectional],
        [":-", CT.Separator, CT.Multidirectional],
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
        ["Directions", CT.LP, CT.Expression, CT.RP],
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
        [CT.Expression, ":", CT.Expression, CT.PairExpressions],
        [CT.Expression, ":", CT.Expression]
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
        ["[", CT.Multidirectional, "]", CT.Separator],
        [CT.Dictionary, CT.Separator],
        ["{", CT.Program, "}", CT.Separator],
        [CT.OtherOperator, CT.Separator],
        [
            CT.LazyQuarternary, CT.LP, CT.Expression, CT.Expression,
            CT.Expression, CT.Expression, CT.RP, CT.Separator
        ],
        [
            CT.Quarternary, CT.LP, CT.Expression, CT.Expression, CT.Expression,
            CT.Expression, CT.RP, CT.Separator
        ],
        [
            CT.LazyTernary, CT.LP, CT.Expression, CT.Expression, CT.Expression,
            CT.RP, CT.Separator
        ],
        [
            CT.Ternary, CT.LP, CT.Expression, CT.Expression, CT.Expression,
            CT.RP, CT.Separator
        ],
        [
            CT.LazyBinary, CT.LP, CT.Expression, CT.Expression, CT.RP,
            CT.Separator
        ],
        [CT.Binary, CT.LP, CT.Expression, CT.Expression, CT.RP, CT.Separator],
        [CT.LazyUnary, CT.LP, CT.Expression, CT.RP, CT.Separator],
        [CT.Unary, CT.LP, CT.Expression, CT.RP, CT.Separator],
        [CT.Nilary, CT.LP, CT.RP, CT.Separator],
    ],
    CT.Nilary: [
        ["InputString"], ["input"], ["InputNumber"], ["Random"], ["rand"],
        ["PeekAll"], ["PeekMoore"], ["PeekVonNeumann"], ["Peek"], ["x"], ["y"],
        ["i"], ["j"]
    ],
    CT.Unary: [
        ["Negate"], ["Length"], ["Not"], ["Cast"], ["Random"], ["rand"],
        ["Evaluate"], ["eval"], ["Pop"], ["Lowercase"], ["Uppercase"],
        ["Minimum"], ["min"], ["Floor"], ["floor"], ["Maximum"], ["max"],
        ["Ceiling"], ["ceil"], ["Character"], ["chr"], ["Ordinal"], ["ord"],
        ["Reverse"], ["rev"], ["GetVariable"], ["getvar"], ["Repeated"],
        ["RepeatedNull"], ["Slice"], ["Range"], ["~"],
        ["BitwiseNot"], ["Absolute"], ["abs"], ["Sum"], ["Product"],
        ["Incremented"], ["++"], ["Decremented"], ["--"], ["Doubled"], ["***"],
        ["Halved"], ["\\\\"], ["InclusiveRange"], ["PythonEvaluate"],
        ["pyeval"]
    ],
    CT.Binary: [
        ["**"], ["+"], ["Add"], ["Plus"], ["-"], ["Subtract"], ["Minus"],
        ["*"], ["Multiply"], ["Times"], ["\\"], ["/"], ["Divide"], ["Reduce"],
        ["IntDivide"], ["IntegerDivide"], ["%"], ["Modulo"], ["=="],
        ["Equals"], ["<"], ["Less"], [">"], ["Greater"], ["&"], ["BitwiseAnd"],
        ["|"], ["BitwiseOr"], ["InclusiveRange"], ["Range"], ["Mold"],
        ["CycleChop"], ["Exponentiate"], ["Exponent"], ["Power"], ["AtIndex"],
        ["PushOperator"], ["Join"], ["Split"], ["FindAll"], ["Find"],
        ["PadLeft"], ["PadRight"], ["Count"], ["Rule"], ["DelayedRule"],
        ["PatternTest"], ["Slice"], ["Any"], ["Some"], ["All"], ["Every"]
    ],
    CT.Ternary: [["Slice"]],
    CT.Quarternary: [["Slice"]],
    CT.LazyUnary: [],
    CT.LazyBinary: [["And"], ["Or"], ["and"], ["or"]],
    CT.LazyTernary: [["Ternary"]],
    CT.LazyQuarternary: [],
    CT.OtherOperator: [
        ["PeekDirection", CT.LP, CT.Expression, CT.Arrow, CT.RP],
        ["Each", CT.LP, CT.Expression, CT.Expression, CT.RP],
        ["Map", CT.LP, CT.Expression, CT.Expression, CT.RP],
        ["PythonFunction", CT.LP, CT.Expression, CT.List, CT.RP],
        ["PythonFunction", CT.LP, CT.Expression, CT.RP],
        ["EvaluateVariable", CT.LP, CT.Expression, CT.WolframList, CT.RP],
        ["evalvar", CT.LP, CT.Expression, CT.WolframList, CT.RP],
        ["EvaluateVariable", CT.LP, CT.Expression, CT.Expression, CT.RP],
        ["evalvar", CT.LP, CT.Expression, CT.Expression, CT.RP]
    ],
    CT.Program: [[CT.Command, CT.Separator, CT.Separator, CT.Program], []],
    CT.Body: [["{", CT.Program, "}"], [CT.Command]],
    CT.Command: [
        ["PythonFunction", CT.LP, CT.Expression, CT.Expression, CT.RP],
        ["PythonFunction", CT.LP, CT.Expression, CT.RP],
        ["InputString", CT.LP, CT.Name, CT.RP],
        ["input", CT.LP, CT.Name, CT.RP],
        ["InputNumber", CT.LP, CT.Name, CT.RP],
        ["Evaluate", CT.LP, CT.Expression, CT.RP],
        ["eval", CT.LP, CT.Expression, CT.RP],
        ["Print", CT.LP, CT.Arrow, CT.Separator, CT.Expression, CT.RP],
        ["Print", CT.LP, CT.Expression, CT.RP],
        ["print", CT.LP, CT.Arrow, CT.Separator, CT.Expression, CT.RP],
        ["print", CT.LP, CT.Expression, CT.RP],
        [
            "Multiprint", CT.LP, CT.Multidirectional, CT.Separator,
            CT.Expression, CT.RP
        ],
        ["Multiprint", CT.LP, CT.Expression, CT.RP],
        ["Polygon", CT.LP, CT.Sides, CT.Separator, CT.Expression, CT.RP],
        [
            "Polygon", CT.LP, CT.Multidirectional, CT.Separator, CT.Expression,
            CT.Expression, CT.RP
        ],
        ["PolygonHollow", CT.LP, CT.Sides, CT.Separator, CT.Expression, CT.RP],
        [
            "PolygonHollow", CT.LP, CT.Multidirectional, CT.Separator,
            CT.Expression, CT.Expression, CT.RP
        ],
        ["Rectangle", CT.LP, CT.Expression, CT.Expression, CT.RP],
        ["Rectangle", CT.LP, CT.Expression, CT.RP],
        ["Oblong", CT.LP, CT.Expression, CT.Expression, CT.Expression, CT.RP],
        ["Oblong", CT.LP, CT.Expression, CT.Expression, CT.RP],
        ["Box", CT.LP, CT.Expression, CT.Expression, CT.Expression, CT.RP],
        ["Box", CT.LP, CT.Expression, CT.Expression, CT.RP],
        ["Move", CT.LP, CT.Arrow, CT.RP],
        ["Move", CT.LP, CT.Expression, CT.Arrow, CT.RP],
        ["Move", CT.LP, CT.Expression, CT.Expression, CT.RP],
        ["Jump", CT.LP, CT.Expression, CT.Expression, CT.RP],
        ["PivotLeft", CT.LP, CT.Expression, CT.RP],
        ["PivotLeft", CT.LP, CT.RP],
        ["PivotRight", CT.LP, CT.Expression, CT.RP],
        ["PivotRight", CT.LP, CT.RP],
        ["JumpTo", CT.LP, CT.Expression, CT.Expression, CT.RP],
        ["RotateTransform", CT.LP, CT.Expression, CT.RP],
        ["RotateTransform", CT.LP, CT.RP],
        ["ReflectTransform", CT.LP, CT.Multidirectional, CT.RP],
        ["ReflectTransform", CT.LP, CT.Arrow, CT.RP],
        ["ReflectTransform", CT.LP, CT.RP],
        ["RotatePrism", CT.LP, CT.Arrow, CT.Separator, CT.Expression, CT.RP],
        ["RotatePrism", CT.LP, CT.Arrow, CT.RP],
        ["RotatePrism", CT.LP, CT.Expression, CT.RP],
        ["RotatePrism", CT.LP, CT.RP],
        ["ReflectMirror", CT.LP, CT.Multidirectional, CT.RP],
        ["ReflectMirror", CT.LP, CT.Arrow, CT.RP],
        ["ReflectMirror", CT.LP, CT.RP],
        ["RotateCopy", CT.LP, CT.Arrow, CT.Separator, CT.Expression, CT.RP],
        ["RotateCopy", CT.LP, CT.Arrow, CT.RP],
        ["RotateCopy", CT.LP, CT.Expression, CT.RP],
        ["RotateCopy", CT.LP, CT.RP],
        ["ReflectCopy", CT.LP, CT.Multidirectional, CT.RP],
        ["ReflectCopy", CT.LP, CT.Arrow, CT.RP],
        ["ReflectCopy", CT.LP, CT.RP],
        [
            "RotateOverlapOverlap", CT.LP, CT.Arrow, CT.Separator, CT.Number,
            CT.Separator, CT.Expression, CT.Separator, CT.Expression, CT.RP
        ],
        [
            "RotateOverlapOverlap", CT.LP, CT.Arrow, CT.Separator, CT.Expression,
            CT.Separator, CT.Expression, CT.RP
        ],
        [
            "RotateOverlapOverlap", CT.LP, CT.Arrow, CT.Separator, CT.Expression,
            CT.RP
        ],
        ["RotateOverlapOverlap", CT.LP, CT.Expression, CT.Expression, CT.RP],
        ["RotateOverlapOverlap", CT.LP, CT.Expression, CT.RP],
        ["RotateOverlap", CT.LP, CT.Arrow, CT.Separator, CT.Expression, CT.RP],
        ["RotateOverlap", CT.LP, CT.Arrow, CT.RP],
        ["RotateOverlap", CT.LP, CT.Expression, CT.RP],
        ["RotateOverlap", CT.LP, CT.RP],
        [
            "RotateShutterOverlap", CT.LP, CT.Arrow, CT.Separator, CT.Number,
            CT.Separator, CT.Expression, CT.Separator, CT.Expression, CT.RP
        ],
        [
            "RotateShutterOverlap", CT.LP, CT.Arrow, CT.Separator, CT.Expression,
            CT.Separator, CT.Expression, CT.RP
        ],
        [
            "RotateShutterOverlap", CT.LP, CT.Arrow, CT.Separator, CT.Expression,
            CT.RP
        ],
        ["RotateShutterOverlap", CT.LP, CT.Expression, CT.Expression, CT.RP],
        ["RotateShutterOverlap", CT.LP, CT.Expression, CT.RP],
        ["RotateShutter", CT.LP, CT.Arrow, CT.Separator, CT.Expression, CT.RP],
        ["RotateShutter", CT.LP, CT.Arrow, CT.RP],
        ["RotateShutter", CT.LP, CT.Expression, CT.RP],
        ["RotateShutter", CT.LP, CT.RP],
        [
            "ReflectOverlapOverlap", CT.LP, CT.Multidirectional, CT.Separator,
            CT.Expression, CT.RP
        ],
        [
            "ReflectOverlapOverlap", CT.LP, CT.Arrow, CT.Separator,
            CT.Expression, CT.RP
        ],
        ["ReflectOverlapOverlap", CT.LP, CT.Expression, CT.RP],
        ["ReflectOverlap", CT.LP, CT.Multidirectional, CT.RP],
        ["ReflectOverlap", CT.LP, CT.Arrow, CT.RP],
        ["ReflectOverlap", CT.LP, CT.RP],
        [
            "ReflectButterflyOverlap", CT.LP, CT.Multidirectional, CT.Separator,
            CT.Expression, CT.RP
        ],
        [
            "ReflectButterflyOverlap", CT.LP, CT.Arrow, CT.Separator,
            CT.Expression, CT.RP
        ],
        ["ReflectButterflyOverlap", CT.LP, CT.Expression, CT.RP],
        ["ReflectButterfly", CT.LP, CT.Multidirectional, CT.RP],
        ["ReflectButterfly", CT.LP, CT.Arrow, CT.RP],
        ["ReflectButterfly", CT.LP, CT.RP],
        ["Rotate", CT.LP, CT.Expression, CT.RP],
        ["Rotate", CT.LP, CT.RP],
        ["Reflect", CT.LP, CT.Arrow, CT.RP],
        ["Reflect", CT.LP, CT.RP],
        ["Copy", CT.LP, CT.Expression, CT.Expression, CT.RP],
        ["for", CT.LP, CT.Expression, CT.RP, CT.Body],
        ["while", CT.LP, CT.Expression, CT.RP, CT.Body],
        ["if", CT.LP, CT.Expression, CT.RP, CT.Body, "else", CT.Body],
        ["if", CT.LP, CT.Expression, CT.RP, CT.Body],
        [
            "AssignAtIndex", CT.LP, CT.Expression, CT.Expression, CT.Expression,
            CT.RP
        ],
        ["Assign", CT.LP, CT.Expression, CT.Name, CT.RP],
        ["SetVariable", CT.LP, CT.Expression, CT.Expression, CT.RP],
        ["setvar", CT.LP, CT.Expression, CT.Expression, CT.RP],
        ["Fill", CT.LP, CT.Expression, CT.RP],
        ["SetBackground", CT.LP, CT.Expression, CT.RP],
        ["bg", CT.LP, CT.Expression, CT.RP],
        ["Dump", CT.LP, CT.RP],
        ["RefreshFor", CT.LP, CT.Expression, CT.Expression, CT.RP, CT.Body],
        ["RefreshWhile", CT.LP, CT.Expression, CT.Expression, CT.RP, CT.Body],
        ["Refresh", CT.LP, CT.Expression, CT.RP],
        ["Refresh", CT.LP, CT.RP],
        ["ToggleTrim", CT.LP, CT.RP],
        ["Trim", CT.LP, CT.Expression, CT.Expression, CT.RP],
        ["Trim", CT.LP, CT.Expression, CT.RP],
        ["Clear", CT.LP, CT.RP],
        ["Extend", CT.LP, CT.Expression, CT.Expression, CT.RP],
        ["Extend", CT.LP, CT.Expression, CT.RP],
        ["Push", CT.LP, CT.Expression, CT.Expression, CT.RP],
        [
            "switch", CT.LP, CT.Expression, CT.RP, "{", CT.Cases, "default", ":",
            CT.Body, "}"
        ],
        ["switch", CT.LP, CT.Expression, CT.RP, "{", CT.Cases, "}"],
        ["MapCommand", CT.LP, CT.Expression, CT.Expression, CT.RP],
        ["ExecuteVariable", CT.LP, CT.Expression, CT.WolframList, CT.RP],
        ["execvar", CT.LP, CT.Expression, CT.WolframList, CT.RP],
        ["ExecuteVariable", CT.LP, CT.Expression, CT.Expression, CT.RP],
        ["execvar", CT.LP, CT.Expression, CT.Expression, CT.RP],
        ["MapAssignLeft", CT.LP, CT.Binary, CT.Expression, CT.Name, CT.RP],
        ["MapAssignRight", CT.LP, CT.Binary, CT.Expression, CT.Name, CT.RP],
        ["MapAssign", CT.LP, CT.Unary, CT.Name, CT.RP],
        ["PythonExecute", CT.LP, CT.Expression, CT.RP],
        ["pyexec", CT.LP, CT.Expression, CT.RP],
        [CT.Arrow, CT.Separator, CT.Expression],
        [CT.Expression],
    ]
}
