from charcoaltoken import CharcoalToken as CT
import re

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
        [":Le"],
        [":U"],
        [":R"],
        [":D"],
        ["Direction", CT.LP, CT.Expression, CT.RP]
    ],
    CT.Multidirectional: [
        [CT.Arrows, CT.S, CT.Multidirectional],
        [":+", CT.S, CT.Multidirectional],
        [":X", CT.S, CT.Multidirectional],
        [":*", CT.S, CT.Multidirectional],
        [":All", CT.S, CT.Multidirectional],
        [":|", CT.S, CT.Multidirectional],
        [":Vertical", CT.S, CT.Multidirectional],
        [":-", CT.S, CT.Multidirectional],
        [":Horizontal", CT.S, CT.Multidirectional],
        [":\\", CT.S, CT.Multidirectional],
        [":/", CT.S, CT.Multidirectional],
        [":<", CT.S, CT.Multidirectional],
        [":>", CT.S, CT.Multidirectional],
        [":^", CT.S, CT.Multidirectional],
        [":K", CT.S, CT.Multidirectional],
        [":L", CT.S, CT.Multidirectional],
        [":T", CT.S, CT.Multidirectional],
        [":V", CT.S, CT.Multidirectional],
        [":Y", CT.S, CT.Multidirectional],
        [":7", CT.S, CT.Multidirectional],
        [":¬", CT.S, CT.Multidirectional],
        ["[", CT.Multidirectional, "]"],
        ["Directions", CT.LP, CT.Expression, CT.RP],
        [CT.S]
    ],
    CT.Side: [
        [CT.Arrow, CT.S, CT.Expression]
    ],
    CT.S: [[";"], [","], []],
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
    CT.Arrows: [[CT.Arrow, CT.S, CT.Arrows], [CT.Arrow]],
    CT.Sides: [[CT.Side, CT.S, CT.Sides], [CT.Side]],
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
        [
            "case", CT.Expression, ":", CT.Body, CT.S, CT.S,
            CT.Cases
        ],
        []
    ],
    CT.List: [["[", CT.Expressions, "]"], ["[", "]"]],
    CT.WolframList: [["[", CT.WolframExpressions, "]"], ["[", "]"]],
    CT.Dictionary: [["{", CT.PairExpressions, "}"], ["{", "}"]],
    CT.WolframExpression: [[CT.Span, CT.S], [CT.Expression]],
    CT.Expression: [
        [CT.Number, CT.S],
        [CT.String, CT.S],
        [CT.Name, CT.S],
        [CT.List, CT.S],
        ["[", CT.Multidirectional, "]", CT.S],
        [CT.Dictionary, CT.S],
        ["{", CT.Program, "}", CT.S],
        [CT.OtherOperator, CT.S],
        [
            CT.LazyQuarternary, CT.LP, CT.Expression, CT.Expression,
            CT.Expression, CT.Expression, CT.RP, CT.S
        ],
        [
            CT.Quarternary, CT.LP, CT.Expression, CT.Expression,
            CT.Expression, CT.Expression, CT.RP, CT.S
        ],
        [
            CT.LazyTernary, CT.LP, CT.Expression, CT.Expression,
            CT.Expression, CT.RP, CT.S
        ],
        [
            CT.Ternary, CT.LP, CT.Expression, CT.Expression,
            CT.Expression, CT.RP, CT.S
        ],
        [
            CT.LazyBinary, CT.LP, CT.Expression, CT.Expression,
            CT.RP, CT.S
        ],
        [
            CT.Binary, CT.LP, CT.Expression, CT.Expression, CT.RP,
            CT.S
        ],
        [CT.LazyUnary, CT.LP, CT.Expression, CT.RP, CT.S],
        [CT.Unary, CT.LP, CT.ExpressionOrEOF, CT.RP, CT.S],
        [CT.Nilary, CT.LP, CT.RP, CT.S],
        [
            CT.LazyQuarternary, CT.LP, CT.ExpressionOrEOF, CT.ExpressionOrEOF,
            CT.ExpressionOrEOF, CT.ExpressionOrEOF, CT.RP, CT.S
        ],
        [
            CT.Quarternary, CT.LP, CT.ExpressionOrEOF, CT.ExpressionOrEOF,
            CT.ExpressionOrEOF, CT.ExpressionOrEOF, CT.RP, CT.S
        ],
        [
            CT.LazyTernary, CT.LP, CT.ExpressionOrEOF, CT.ExpressionOrEOF,
            CT.ExpressionOrEOF, CT.RP, CT.S
        ],
        [
            CT.Ternary, CT.LP, CT.ExpressionOrEOF, CT.ExpressionOrEOF,
            CT.ExpressionOrEOF, CT.RP, CT.S
        ],
        [
            CT.LazyBinary, CT.LP, CT.ExpressionOrEOF, CT.ExpressionOrEOF,
            CT.RP, CT.S
        ],
        [
            CT.Binary, CT.LP, CT.ExpressionOrEOF, CT.ExpressionOrEOF, CT.RP,
            CT.S
        ],
        [CT.LazyUnary, CT.LP, CT.ExpressionOrEOF, CT.RP, CT.S],
        [CT.Unary, CT.LP, CT.ExpressionOrEOF, CT.RP, CT.S]
    ],
    CT.ExpressionOrEOF: [
        [CT.Expression],
        [CT.EOF]
    ],
    CT.Nilary: [
        ["InputString"], ["InputNumber"], ["Input"], ["Random"], ["rand"],
        ["PeekAll"], ["PeekMoore"], ["PeekVonNeumann"], ["Peek"], ["x"], ["y"],
        ["i"], ["j"]
    ],
    CT.Unary: [
        ["Negate"], ["neg"], ["Length"], ["Not"], ["Cast"], ["Random"],
        ["rand"], ["Evaluate"], ["eval"], ["Pop"], ["Lowercase"],
        ["Uppercase"], ["Minimum"], ["min"], ["Floor"], ["Maximum"], ["max"],
        ["Ceiling"], ["ceil"], ["Character"], ["chr"], ["Ordinal"], ["ord"],
        ["Reverse"], ["rev"], ["GetVariable"], ["getvar"], ["Repeated"],
        ["RepeatedNull"], ["~"], ["BitwiseNot"],
        ["Absolute"], ["abs"], ["Sum"], ["Product"],
        ["Incremented"], ["++"], ["Decremented"], ["--"], ["Doubled"], ["***"],
        ["Halved"], ["\\\\"], ["SquareRoot"], ["sqrt"], ["Slice"],
        ["Range"], ["InclusiveRange"], ["PythonEvaluate"], ["pyeval"]
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
        ["PatternTest"], ["BaseString"], ["Base"], ["Slice"]
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
        ["Any", CT.LP, CT.Expression, CT.Expression, CT.RP],
        ["Some", CT.LP, CT.Expression, CT.Expression, CT.RP],
        ["Every", CT.LP, CT.Expression, CT.Expression, CT.RP],
        ["All", CT.LP, CT.Expression, CT.Expression, CT.RP],
        ["StringMap", CT.LP, CT.Expression, CT.Expression, CT.RP],
        ["SMap", CT.LP, CT.Expression, CT.Expression, CT.RP],
        ["Filter", CT.LP, CT.Expression, CT.Expression, CT.RP],
        ["EvaluateVariable", CT.LP, CT.Expression, CT.WolframList, CT.RP],
        ["evalvar", CT.LP, CT.Expression, CT.WolframList, CT.RP],
        ["EvaluateVariable", CT.LP, CT.Expression, CT.Expression, CT.RP],
        ["evalvar", CT.LP, CT.Expression, CT.Expression, CT.RP],
        ["EvaluateVariable", CT.LP, CT.Expression, CT.RP],
        ["evalvar", CT.LP, CT.Expression, CT.RP]
    ],
    CT.Program: [[CT.Command, CT.Program], []],
    CT.Body: [["{", CT.Program, "}"], [CT.Command]],
    CT.Command: [
        ["InputString", CT.LP, CT.Name, CT.RP, CT.S],
        ["InputNumber", CT.LP, CT.Name, CT.RP, CT.S],
        ["Input", CT.LP, CT.Name, CT.RP, CT.S],
        ["Evaluate", CT.LP, CT.Expression, CT.RP, CT.S],
        ["eval", CT.LP, CT.Expression, CT.RP, CT.S],
        ["Print", CT.LP, CT.Arrow, CT.S, CT.Expression, CT.RP, CT.S],
        ["Print", CT.LP, CT.Expression, CT.RP, CT.S],
        ["print", CT.LP, CT.Arrow, CT.S, CT.Expression, CT.RP, CT.S],
        ["print", CT.LP, CT.Expression, CT.RP, CT.S],
        [
            "Multiprint", CT.LP, CT.Multidirectional, CT.S,
            CT.Expression, CT.RP, CT.S
        ],
        ["Multiprint", CT.LP, CT.Expression, CT.RP, CT.S],
        ["Polygon", CT.LP, CT.Sides, CT.S, CT.Expression, CT.RP, CT.S],
        [
            "Polygon", CT.LP, CT.Multidirectional, CT.S, CT.Expression,
            CT.Expression, CT.RP, CT.S
        ],
        ["PolygonHollow", CT.LP, CT.Sides, CT.S, CT.Expression, CT.RP, CT.S],
        [
            "PolygonHollow", CT.LP, CT.Multidirectional, CT.S,
            CT.Expression, CT.Expression, CT.RP, CT.S
        ],
        ["Rectangle", CT.LP, CT.Expression, CT.Expression, CT.RP, CT.S],
        ["Rectangle", CT.LP, CT.Expression, CT.RP, CT.S],
        [
            "Oblong", CT.LP, CT.Expression, CT.Expression, CT.Expression,
            CT.RP, CT.S
        ],
        ["Oblong", CT.LP, CT.Expression, CT.Expression, CT.RP, CT.S],
        [
            "Box", CT.LP, CT.Expression, CT.Expression, CT.Expression, CT.RP,
            CT.S
        ],
        ["Box", CT.LP, CT.Expression, CT.Expression, CT.RP, CT.S],
        ["Move", CT.LP, CT.Arrow, CT.RP, CT.S],
        ["Move", CT.LP, CT.Expression, CT.Arrow, CT.RP, CT.S],
        ["Move", CT.LP, CT.Expression, CT.Expression, CT.RP, CT.S],
        ["Jump", CT.LP, CT.Expression, CT.Expression, CT.RP, CT.S],
        ["PivotLeft", CT.LP, CT.Expression, CT.RP, CT.S],
        ["PivotLeft", CT.LP, CT.RP, CT.S],
        ["PivotRight", CT.LP, CT.Expression, CT.RP, CT.S],
        ["PivotRight", CT.LP, CT.RP, CT.S],
        ["JumpTo", CT.LP, CT.Expression, CT.Expression, CT.RP, CT.S],
        ["RotateTransform", CT.LP, CT.Expression, CT.RP, CT.S],
        ["RotateTransform", CT.LP, CT.RP, CT.S],
        ["ReflectTransform", CT.LP, CT.Multidirectional, CT.RP, CT.S],
        ["ReflectTransform", CT.LP, CT.Arrow, CT.RP, CT.S],
        ["ReflectTransform", CT.LP, CT.RP, CT.S],
        ["RotatePrism", CT.LP, CT.Arrow, CT.S, CT.Expression, CT.RP, CT.S],
        ["RotatePrism", CT.LP, CT.Arrow, CT.RP, CT.S],
        ["RotatePrism", CT.LP, CT.Expression, CT.RP, CT.S],
        ["RotatePrism", CT.LP, CT.RP, CT.S],
        ["ReflectMirror", CT.LP, CT.Multidirectional, CT.RP, CT.S],
        ["ReflectMirror", CT.LP, CT.Arrow, CT.RP, CT.S],
        ["ReflectMirror", CT.LP, CT.RP, CT.S],
        ["RotateCopy", CT.LP, CT.Arrow, CT.S, CT.Expression, CT.RP, CT.S],
        ["RotateCopy", CT.LP, CT.Arrow, CT.RP, CT.S],
        ["RotateCopy", CT.LP, CT.Expression, CT.RP, CT.S],
        ["RotateCopy", CT.LP, CT.RP, CT.S],
        ["ReflectCopy", CT.LP, CT.Multidirectional, CT.RP, CT.S],
        ["ReflectCopy", CT.LP, CT.Arrow, CT.RP, CT.S],
        ["ReflectCopy", CT.LP, CT.RP, CT.S],
        [
            "RotateOverlapOverlap", CT.LP, CT.Arrow, CT.S, CT.Number, CT.S,
            CT.Expression, CT.Expression, CT.RP, CT.S
        ],
        [
            "RotateOverlapOverlap", CT.LP, CT.Arrow, CT.S, CT.Number, CT.S,
            CT.Expression, CT.RP, CT.S
        ],
        [
            "RotateOverlapOverlap", CT.LP, CT.Arrow, CT.S, CT.Expression,
            CT.Expression, CT.RP, CT.S
        ],
        [
            "RotateOverlapOverlap", CT.LP, CT.Arrow, CT.S, CT.Expression,
            CT.RP, CT.S
        ],
        [
            "RotateOverlapOverlap", CT.LP, CT.Expression, CT.Expression, CT.RP,
            CT.S
        ],
        ["RotateOverlapOverlap", CT.LP, CT.Expression, CT.RP, CT.S],
        ["RotateOverlap", CT.LP, CT.Arrow, CT.S, CT.Expression, CT.RP, CT.S],
        ["RotateOverlap", CT.LP, CT.Arrow, CT.RP, CT.S],
        ["RotateOverlap", CT.LP, CT.Expression, CT.RP, CT.S],
        ["RotateOverlap", CT.LP, CT.RP, CT.S],
        [
            "RotateShutterOverlap", CT.LP, CT.Arrow, CT.S, CT.Number, CT.S,
            CT.Expression, CT.Expression, CT.RP, CT.S
        ],
        [
            "RotateShutterOverlap", CT.LP, CT.Arrow, CT.S, CT.Number, CT.S,
            CT.Expression, CT.RP, CT.S
        ],
        [
            "RotateShutterOverlap", CT.LP, CT.Arrow, CT.S, CT.Expression,
            CT.Expression, CT.RP, CT.S
        ],
        [
            "RotateShutterOverlap", CT.LP, CT.Arrow, CT.S, CT.Expression,
            CT.RP, CT.S
        ],
        [
            "RotateShutterOverlap", CT.LP, CT.Expression, CT.Expression, CT.RP,
            CT.S
        ],
        ["RotateShutterOverlap", CT.LP, CT.Expression, CT.RP, CT.S],
        ["RotateShutter", CT.LP, CT.Arrow, CT.S, CT.Expression, CT.RP, CT.S],
        ["RotateShutter", CT.LP, CT.Arrow, CT.RP, CT.S],
        ["RotateShutter", CT.LP, CT.Expression, CT.RP, CT.S],
        ["RotateShutter", CT.LP, CT.RP, CT.S],
        [
            "ReflectOverlapOverlap", CT.LP, CT.Multidirectional, CT.S,
            CT.Expression, CT.RP, CT.S
        ],
        [
            "ReflectOverlapOverlap", CT.LP, CT.Arrow, CT.S,
            CT.Expression, CT.RP, CT.S
        ],
        ["ReflectOverlapOverlap", CT.LP, CT.Expression, CT.RP, CT.S],
        ["ReflectOverlap", CT.LP, CT.Multidirectional, CT.RP, CT.S],
        ["ReflectOverlap", CT.LP, CT.Arrow, CT.RP, CT.S],
        ["ReflectOverlap", CT.LP, CT.RP, CT.S],
        [
            "ReflectButterflyOverlap", CT.LP, CT.Multidirectional, CT.S,
            CT.Expression, CT.RP, CT.S
        ],
        [
            "ReflectButterflyOverlap", CT.LP, CT.Arrow, CT.S,
            CT.Expression, CT.RP, CT.S
        ],
        ["ReflectButterflyOverlap", CT.LP, CT.Expression, CT.RP, CT.S],
        ["ReflectButterfly", CT.LP, CT.Multidirectional, CT.RP, CT.S],
        ["ReflectButterfly", CT.LP, CT.Arrow, CT.RP, CT.S],
        ["ReflectButterfly", CT.LP, CT.RP, CT.S],
        ["Rotate", CT.LP, CT.Expression, CT.RP, CT.S],
        ["Rotate", CT.LP, CT.RP, CT.S],
        ["Reflect", CT.LP, CT.Arrow, CT.RP, CT.S],
        ["Reflect", CT.LP, CT.RP, CT.S],
        ["Copy", CT.LP, CT.Expression, CT.Expression, CT.RP, CT.S],
        ["for", CT.LP, CT.Expression, CT.RP, CT.Body],
        ["while", CT.LP, CT.Expression, CT.RP, CT.Body],
        ["if", CT.LP, CT.Expression, CT.RP, CT.Body, "else", CT.Body],
        ["if", CT.LP, CT.Expression, CT.RP, CT.Body],
        [
            "AssignAtIndex", CT.LP, CT.Expression, CT.Expression,
            CT.Expression, CT.RP, CT.S
        ],
        ["Assign", CT.LP, CT.Expression, CT.Name, CT.RP, CT.S],
        ["SetVariable", CT.LP, CT.Expression, CT.Expression, CT.RP, CT.S],
        ["setvar", CT.LP, CT.Expression, CT.Expression, CT.RP, CT.S],
        ["Fill", CT.LP, CT.Expression, CT.RP, CT.S],
        ["SetBackground", CT.LP, CT.Expression, CT.RP, CT.S],
        ["bg", CT.LP, CT.Expression, CT.RP, CT.S],
        ["Dump", CT.LP, CT.RP, CT.S],
        ["RefreshFor", CT.LP, CT.Expression, CT.Expression, CT.RP, CT.Body],
        ["RefreshWhile", CT.LP, CT.Expression, CT.Expression, CT.RP, CT.Body],
        ["Refresh", CT.LP, CT.Expression, CT.RP, CT.S],
        ["Refresh", CT.LP, CT.RP, CT.S],
        ["ToggleTrim", CT.LP, CT.RP, CT.S],
        ["Trim", CT.LP, CT.Expression, CT.Expression, CT.RP, CT.S],
        ["Trim", CT.LP, CT.Expression, CT.RP, CT.S],
        ["Clear", CT.LP, CT.RP, CT.S],
        ["Extend", CT.LP, CT.Expression, CT.Expression, CT.RP, CT.S],
        ["Extend", CT.LP, CT.Expression, CT.RP, CT.S],
        ["Push", CT.LP, CT.Expression, CT.Expression, CT.RP, CT.S],
        [
            "switch_delimited", CT.LP, CT.Expression, CT.RP, "{", CT.Cases,
            "default", ":", CT.Body, "}"
        ],
        ["switch_delimited", CT.LP, CT.Expression, CT.RP, "{", CT.Cases, "}"],
        [
            "switch", CT.LP, CT.Expression, CT.RP, "{", CT.Cases, "default",
            ":", CT.Body, "}"
        ],
        ["switch", CT.LP, CT.Expression, CT.RP, "{", CT.Cases, "}"],
        ["MapCommand", CT.LP, CT.Expression, CT.Expression, CT.RP, CT.S],
        ["ExecuteVariable", CT.LP, CT.Expression, CT.WolframList, CT.RP, CT.S],
        ["execvar", CT.LP, CT.Expression, CT.WolframList, CT.RP, CT.S],
        ["ExecuteVariable", CT.LP, CT.Expression, CT.Expression, CT.RP, CT.S],
        ["execvar", CT.LP, CT.Expression, CT.Expression, CT.RP, CT.S],
        [
            "MapAssignLeft", CT.LP, CT.Binary, CT.S, CT.Expression,
            CT.Name, CT.RP
        ],
        [
            "MapAssignRight", CT.LP, CT.Binary, CT.S, CT.Expression,
            CT.Name, CT.RP
        ],
        ["MapAssign", CT.LP, CT.Unary, CT.S, CT.Name, CT.RP, CT.S],
        ["PythonExecute", CT.LP, CT.Expression, CT.RP, CT.S],
        ["pyexec", CT.LP, CT.Expression, CT.RP, CT.S],
        [CT.Arrow, CT.S, CT.Expression],
        [CT.Expression]
    ]
}
