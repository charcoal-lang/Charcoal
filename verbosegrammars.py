from charcoaltoken import CharcoalToken as CT
import re

VerboseGrammars = {
    CT.LP: [["("], []],
    CT.RP: [[")"], []],
    CT.Arrow: [
        ["Direction", CT.LP, CT.Fix, CT.RP],
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
    ],
    CT.Multidirectional: [
        ["Directions", CT.LP, CT.Fix, CT.RP],
        [CT.Arrows, CT.S, CT.Multidirectional],
        [":+", CT.S, CT.Multidirectional],
        [":Orthogonal", CT.S, CT.Multidirectional],
        [":X", CT.S, CT.Multidirectional],
        [":Diagonal", CT.S, CT.Multidirectional],
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
        [":⌊", CT.S, CT.Multidirectional],
        [":⌈", CT.S, CT.Multidirectional],
        [":DnL", CT.S, CT.Multidirectional],
        [":UnR", CT.S, CT.Multidirectional],
        [":RnD", CT.S, CT.Multidirectional],
        [":DownAndLeft", CT.S, CT.Multidirectional],
        [":UpAndRight", CT.S, CT.Multidirectional],
        [":RightAndDown", CT.S, CT.Multidirectional],
        ["[", CT.Multidirectional, "]"],
        [CT.S]
    ],
    CT.Side: [
        [CT.Arrow, CT.S, CT.Fix]
    ],
    CT.S: [[";"], [","], []],
    CT.Span: [
        [CT.Fix, ";;", CT.Fix, ";;", CT.Fix],
        [CT.Fix, ";;", ";;", CT.Fix],
        [CT.Fix, ";;", CT.Fix],
        [CT.Fix, ";;"],
        [";;", CT.Fix, ";;", CT.Fix],
        [";;", CT.Fix],
        [";;", ";;", CT.Fix],
        [";;", ";;"]
    ],
    CT.Arrows: [[CT.Arrow, CT.S, CT.Arrows], [CT.Arrow]],
    CT.Sides: [[CT.Side, CT.S, CT.Sides], [CT.Side]],
    CT.Fixes: [[CT.Fix, CT.Fixes], [CT.Fix]],
    CT.WolframExpressions: [
        [CT.WolframExpression, CT.WolframExpressions],
        [CT.WolframExpression]
    ],
    CT.PairExpressions: [
        [CT.Fix, ":", CT.Fix, CT.PairExpressions],
        [CT.Fix, ":", CT.Fix]
    ],
    CT.Cases: [
        [
            "case", CT.Fix, ":", CT.Body, CT.S, CT.S,
            CT.Cases
        ],
        []
    ],
    CT.List: [["[", CT.Fixes, "]"], ["[", "]"]],
    CT.WolframList: [["[", CT.WolframExpressions, "]"], ["[", "]"]],
    CT.Dictionary: [["{", CT.PairExpressions, "}"], ["{", "}"]],
    CT.WolframExpression: [[CT.Span, CT.S], [CT.Fix]],
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
            CT.LazyQuarternary, CT.LP, CT.Fix, CT.Fix,
            CT.Fix, CT.Fix, CT.RP, CT.S
        ],
        [
            CT.Quarternary, CT.LP, CT.Fix, CT.Fix,
            CT.Fix, CT.Fix, CT.RP, CT.S
        ],
        [
            CT.LazyTernary, CT.LP, CT.Fix, CT.Fix,
            CT.Fix, CT.RP, CT.S
        ],
        [
            CT.Ternary, CT.LP, CT.Fix, CT.Fix,
            CT.Fix, CT.RP, CT.S
        ],
        [
            CT.LazyBinary, CT.LP, CT.Fix, CT.Fix,
            CT.RP, CT.S
        ],
        [
            CT.Binary, CT.LP, CT.Fix, CT.Fix, CT.RP,
            CT.S
        ],
        [CT.LazyUnary, CT.LP, CT.Fix, CT.RP, CT.S],
        [CT.Unary, CT.LP, CT.FixOrEOF, CT.RP, CT.S],
        [CT.Nilary, CT.LP, CT.RP, CT.S],
        [
            CT.LazyQuarternary, CT.LP, CT.FixOrEOF, CT.FixOrEOF,
            CT.FixOrEOF, CT.FixOrEOF, CT.RP, CT.S
        ],
        [
            CT.Quarternary, CT.LP, CT.FixOrEOF, CT.FixOrEOF,
            CT.FixOrEOF, CT.FixOrEOF, CT.RP, CT.S
        ],
        [
            CT.LazyTernary, CT.LP, CT.FixOrEOF, CT.FixOrEOF,
            CT.FixOrEOF, CT.RP, CT.S
        ],
        [
            CT.Ternary, CT.LP, CT.FixOrEOF, CT.FixOrEOF,
            CT.FixOrEOF, CT.RP, CT.S
        ],
        [
            CT.LazyBinary, CT.LP, CT.FixOrEOF, CT.FixOrEOF,
            CT.RP, CT.S
        ],
        [
            CT.Binary, CT.LP, CT.FixOrEOF, CT.FixOrEOF, CT.RP,
            CT.S
        ],
        [CT.LazyUnary, CT.LP, CT.FixOrEOF, CT.RP, CT.S],
        [CT.Unary, CT.LP, CT.FixOrEOF, CT.RP, CT.S]
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
        ["RepeatedNull"], ["BitwiseNot"],
        ["Absolute"], ["abs"], ["Sum"], ["Product"],
        ["Incremented"], ["Decremented"], ["Doubled"],
        ["Halved"], ["SquareRoot"], ["sqrt"], ["Slice"],
        ["Range"], ["InclusiveRange"], ["PythonEvaluate"], ["pyeval"]
    ],
    CT.Binary: [
        ["Add"], ["Plus"], ["Subtract"], ["Minus"],
        ["Multiply"], ["Times"], ["Divide"], ["Reduce"],
        ["IntDivide"], ["IntegerDivide"], ["Modulo"], ["mod"],
        ["Equals"], ["Less"], ["Greater"], ["BitwiseAnd"],
        ["BitwiseOr"], ["InclusiveRange"], ["Range"], ["Mold"],
        ["CycleChop"], ["Exponentiate"], ["Exponent"], ["Power"], ["AtIndex"],
        ["PushOperator"], ["Join"], ["Split"], ["FindAll"], ["Find"],
        ["PadLeft"], ["PadRight"], ["Count"], ["Rule"], ["DelayedRule"],
        ["PatternTest"], ["BaseString"], ["Base"], ["Slice"]
    ],
    CT.Infix: [
        ["**"], ["+"], ["-"], ["*"], ["/"], ["\\"], ["%"], ["=="], ["<"],
        [">"], ["&"], ["|"], ["="]
    ],
    CT.Prefix: [
        ["--"], ["-"], ["~"], ["++"], ["***"], ["\\\\"]
    ],
    CT.FixOrEOF: [
        [CT.Fix],
        [CT.EOF]
    ],
    CT.Ternary: [["Slice"]],
    CT.Quarternary: [["Slice"]],
    CT.LazyUnary: [],
    CT.LazyBinary: [["And"], ["Or"], ["and"], ["or"]],
    CT.LazyTernary: [["Ternary"]],
    CT.LazyQuarternary: [],
    CT.OtherOperator: [
        ["PeekDirection", CT.LP, CT.Fix, CT.Arrow, CT.RP],
        ["Each", CT.LP, CT.Fix, CT.Fix, CT.RP],
        ["Map", CT.LP, CT.Fix, CT.Fix, CT.RP],
        ["Any", CT.LP, CT.Fix, CT.Fix, CT.RP],
        ["Some", CT.LP, CT.Fix, CT.Fix, CT.RP],
        ["Every", CT.LP, CT.Fix, CT.Fix, CT.RP],
        ["All", CT.LP, CT.Fix, CT.Fix, CT.RP],
        ["StringMap", CT.LP, CT.Fix, CT.Fix, CT.RP],
        ["SMap", CT.LP, CT.Fix, CT.Fix, CT.RP],
        ["Filter", CT.LP, CT.Fix, CT.Fix, CT.RP],
        ["EvaluateVariable", CT.LP, CT.Fix, CT.WolframList, CT.RP],
        ["evalvar", CT.LP, CT.Fix, CT.WolframList, CT.RP],
        ["EvaluateVariable", CT.LP, CT.Fix, CT.Fix, CT.RP],
        ["evalvar", CT.LP, CT.Fix, CT.Fix, CT.RP],
        ["EvaluateVariable", CT.LP, CT.Fix, CT.RP],
        ["evalvar", CT.LP, CT.Fix, CT.RP]
    ],
    CT.Program: [[CT.Command, CT.Program], []],
    CT.NonEmptyProgram: [[CT.Command, CT.Program], [CT.Command]],
    CT.Body: [["{", CT.Program, "}"], [CT.Command]],
    CT.Command: [
        ["InputString", CT.LP, CT.Name, CT.RP, CT.S],
        ["InputNumber", CT.LP, CT.Name, CT.RP, CT.S],
        ["Input", CT.LP, CT.Name, CT.RP, CT.S],
        ["Evaluate", CT.LP, CT.Fix, CT.RP, CT.S],
        ["eval", CT.LP, CT.Fix, CT.RP, CT.S],
        ["Print", CT.LP, CT.Arrow, CT.S, CT.Fix, CT.RP, CT.S],
        ["Print", CT.LP, CT.Fix, CT.RP, CT.S],
        ["print", CT.LP, CT.Arrow, CT.S, CT.Fix, CT.RP, CT.S],
        ["print", CT.LP, CT.Fix, CT.RP, CT.S],
        [
            "Multiprint", CT.LP, CT.Multidirectional, CT.S,
            CT.Fix, CT.RP, CT.S
        ],
        ["Multiprint", CT.LP, CT.Fix, CT.RP, CT.S],
        [
            "Polygon", CT.LP, CT.Multidirectional, CT.S, CT.Fix,
            CT.Fix, CT.RP, CT.S
        ],
        ["Polygon", CT.LP, CT.Sides, CT.S, CT.Fix, CT.RP, CT.S],
        [
            "PolygonHollow", CT.LP, CT.Multidirectional, CT.S,
            CT.Fix, CT.Fix, CT.RP, CT.S
        ],
        ["PolygonHollow", CT.LP, CT.Sides, CT.S, CT.Fix, CT.RP, CT.S],
        ["Rectangle", CT.LP, CT.Fix, CT.Fix, CT.RP, CT.S],
        ["Rectangle", CT.LP, CT.Fix, CT.RP, CT.S],
        [
            "Oblong", CT.LP, CT.Fix, CT.Fix, CT.Fix,
            CT.RP, CT.S
        ],
        ["Oblong", CT.LP, CT.Fix, CT.Fix, CT.RP, CT.S],
        [
            "Box", CT.LP, CT.Fix, CT.Fix, CT.Fix, CT.RP,
            CT.S
        ],
        ["Box", CT.LP, CT.Fix, CT.Fix, CT.RP, CT.S],
        ["Move", CT.LP, CT.Arrow, CT.RP, CT.S],
        ["Move", CT.LP, CT.Fix, CT.Arrow, CT.RP, CT.S],
        ["Move", CT.LP, CT.Fix, CT.Fix, CT.RP, CT.S],
        ["Jump", CT.LP, CT.Fix, CT.Fix, CT.RP, CT.S],
        ["PivotLeft", CT.LP, CT.Fix, CT.RP, CT.S],
        ["PivotLeft", CT.LP, CT.RP, CT.S],
        ["PivotRight", CT.LP, CT.Fix, CT.RP, CT.S],
        ["PivotRight", CT.LP, CT.RP, CT.S],
        ["JumpTo", CT.LP, CT.Fix, CT.Fix, CT.RP, CT.S],
        ["RotateTransform", CT.LP, CT.Fix, CT.RP, CT.S],
        ["RotateTransform", CT.LP, CT.RP, CT.S],
        ["ReflectTransform", CT.LP, CT.Multidirectional, CT.RP, CT.S],
        ["ReflectTransform", CT.LP, CT.Arrow, CT.RP, CT.S],
        ["ReflectTransform", CT.LP, CT.RP, CT.S],
        ["RotatePrism", CT.LP, CT.Arrow, CT.S, CT.Fix, CT.RP, CT.S],
        ["RotatePrism", CT.LP, CT.Arrow, CT.RP, CT.S],
        ["RotatePrism", CT.LP, CT.Fix, CT.RP, CT.S],
        ["RotatePrism", CT.LP, CT.RP, CT.S],
        ["ReflectMirror", CT.LP, CT.Multidirectional, CT.RP, CT.S],
        ["ReflectMirror", CT.LP, CT.Arrow, CT.RP, CT.S],
        ["ReflectMirror", CT.LP, CT.RP, CT.S],
        ["RotateCopy", CT.LP, CT.Arrow, CT.S, CT.Fix, CT.RP, CT.S],
        ["RotateCopy", CT.LP, CT.Arrow, CT.RP, CT.S],
        ["RotateCopy", CT.LP, CT.Fix, CT.RP, CT.S],
        ["RotateCopy", CT.LP, CT.RP, CT.S],
        ["ReflectCopy", CT.LP, CT.Multidirectional, CT.RP, CT.S],
        ["ReflectCopy", CT.LP, CT.Arrow, CT.RP, CT.S],
        ["ReflectCopy", CT.LP, CT.RP, CT.S],
        [
            "RotateOverlapOverlap", CT.LP, CT.Arrow, CT.S, CT.Number, CT.S,
            CT.Fix, CT.RP, CT.S
        ],
        [
            "RotateOverlapOverlap", CT.LP, CT.Arrow, CT.S, CT.Fix, CT.S,
            CT.Fix, CT.RP, CT.S
        ],
        [
            "RotateOverlapOverlap", CT.LP, CT.Arrow, CT.S, CT.Fix,
            CT.RP, CT.S
        ],
        [
            "RotateOverlapOverlap", CT.LP, CT.Number, CT.S, CT.Fix,
            CT.RP, CT.S
        ],
        [
            "RotateOverlapOverlap", CT.LP, CT.Fix, CT.Fix, CT.RP,
            CT.S
        ],
        ["RotateOverlapOverlap", CT.LP, CT.Fix, CT.RP, CT.S],
        ["RotateOverlap", CT.LP, CT.Arrow, CT.S, CT.Fix, CT.RP, CT.S],
        ["RotateOverlap", CT.LP, CT.Arrow, CT.RP, CT.S],
        ["RotateOverlap", CT.LP, CT.Fix, CT.RP, CT.S],
        ["RotateOverlap", CT.LP, CT.RP, CT.S],
        [
            "RotateShutterOverlap", CT.LP, CT.Arrow, CT.S, CT.Number, CT.S,
            CT.Fix, CT.RP, CT.S
        ],
        [
            "RotateShutterOverlap", CT.LP, CT.Arrow, CT.S, CT.Fix, CT.S,
            CT.Fix, CT.RP, CT.S
        ],
        [
            "RotateShutterOverlap", CT.LP, CT.Arrow, CT.S, CT.Fix,
            CT.RP, CT.S
        ],
        [
            "RotateShutterOverlap", CT.LP, CT.Number, CT.S, CT.Fix,
            CT.RP, CT.S
        ],
        [
            "RotateShutterOverlap", CT.LP, CT.Fix, CT.Fix, CT.RP,
            CT.S
        ],
        ["RotateShutterOverlap", CT.LP, CT.Fix, CT.RP, CT.S],
        ["RotateShutter", CT.LP, CT.Arrow, CT.S, CT.Fix, CT.RP, CT.S],
        ["RotateShutter", CT.LP, CT.Arrow, CT.RP, CT.S],
        ["RotateShutter", CT.LP, CT.Fix, CT.RP, CT.S],
        ["RotateShutter", CT.LP, CT.RP, CT.S],
        [
            "ReflectOverlapOverlap", CT.LP, CT.Multidirectional, CT.S,
            CT.Fix, CT.RP, CT.S
        ],
        [
            "ReflectOverlapOverlap", CT.LP, CT.Arrow, CT.S,
            CT.Fix, CT.RP, CT.S
        ],
        ["ReflectOverlapOverlap", CT.LP, CT.Fix, CT.RP, CT.S],
        ["ReflectOverlap", CT.LP, CT.Multidirectional, CT.RP, CT.S],
        ["ReflectOverlap", CT.LP, CT.Arrow, CT.RP, CT.S],
        ["ReflectOverlap", CT.LP, CT.RP, CT.S],
        [
            "ReflectButterflyOverlap", CT.LP, CT.Multidirectional, CT.S,
            CT.Fix, CT.RP, CT.S
        ],
        [
            "ReflectButterflyOverlap", CT.LP, CT.Arrow, CT.S,
            CT.Fix, CT.RP, CT.S
        ],
        ["ReflectButterflyOverlap", CT.LP, CT.Fix, CT.RP, CT.S],
        ["ReflectButterfly", CT.LP, CT.Multidirectional, CT.RP, CT.S],
        ["ReflectButterfly", CT.LP, CT.Arrow, CT.RP, CT.S],
        ["ReflectButterfly", CT.LP, CT.RP, CT.S],
        ["Rotate", CT.LP, CT.Fix, CT.RP, CT.S],
        ["Rotate", CT.LP, CT.RP, CT.S],
        ["Reflect", CT.LP, CT.Arrow, CT.RP, CT.S],
        ["Reflect", CT.LP, CT.RP, CT.S],
        ["Copy", CT.LP, CT.Fix, CT.Fix, CT.RP, CT.S],
        ["for", CT.LP, CT.Fix, CT.RP, CT.Body],
        ["while", CT.LP, CT.Fix, CT.RP, CT.Body],
        ["if", CT.LP, CT.Fix, CT.RP, CT.Body, "else", CT.Body],
        ["if", CT.LP, CT.Fix, CT.RP, CT.Body],
        [
            "AssignAtIndex", CT.LP, CT.Fix, CT.Fix,
            CT.Fix, CT.RP, CT.S
        ],
        ["Assign", CT.LP, CT.Fix, CT.Name, CT.RP, CT.S],
        ["SetVariable", CT.LP, CT.Fix, CT.Fix, CT.RP, CT.S],
        ["setvar", CT.LP, CT.Fix, CT.Fix, CT.RP, CT.S],
        ["Fill", CT.LP, CT.Fix, CT.RP, CT.S],
        ["SetBackground", CT.LP, CT.Fix, CT.RP, CT.S],
        ["bg", CT.LP, CT.Fix, CT.RP, CT.S],
        ["Dump", CT.LP, CT.RP, CT.S],
        ["RefreshFor", CT.LP, CT.Fix, CT.Fix, CT.RP, CT.Body],
        ["RefreshWhile", CT.LP, CT.Fix, CT.Fix, CT.RP, CT.Body],
        ["Refresh", CT.LP, CT.Fix, CT.RP, CT.S],
        ["Refresh", CT.LP, CT.RP, CT.S],
        ["ToggleTrim", CT.LP, CT.RP, CT.S],
        ["Trim", CT.LP, CT.Fix, CT.Fix, CT.RP, CT.S],
        ["Trim", CT.LP, CT.Fix, CT.RP, CT.S],
        ["Clear", CT.LP, CT.RP, CT.S],
        ["Extend", CT.LP, CT.Fix, CT.Fix, CT.RP, CT.S],
        ["Extend", CT.LP, CT.Fix, CT.RP, CT.S],
        ["Push", CT.LP, CT.Fix, CT.Fix, CT.RP, CT.S],
        [
            "switch_delimited", CT.LP, CT.Fix, CT.RP, "{", CT.Cases,
            "default", ":", CT.Body, "}"
        ],
        ["switch_delimited", CT.LP, CT.Fix, CT.RP, "{", CT.Cases, "}"],
        [
            "switch", CT.LP, CT.Fix, CT.RP, "{", CT.Cases, "default",
            ":", CT.Body, "}"
        ],
        ["switch", CT.LP, CT.Fix, CT.RP, "{", CT.Cases, "}"],
        ["MapCommand", CT.LP, CT.Fix, CT.Fix, CT.RP, CT.S],
        ["ExecuteVariable", CT.LP, CT.Fix, CT.WolframList, CT.RP, CT.S],
        ["execvar", CT.LP, CT.Fix, CT.WolframList, CT.RP, CT.S],
        ["ExecuteVariable", CT.LP, CT.Fix, CT.Fix, CT.RP, CT.S],
        ["execvar", CT.LP, CT.Fix, CT.Fix, CT.RP, CT.S],
        [
            "MapAssignLeft", CT.LP, CT.Binary, CT.S, CT.Fix,
            CT.Name, CT.RP, CT.S
        ],
        [
            "MapAssignRight", CT.LP, CT.Binary, CT.S, CT.Fix,
            CT.Name, CT.RP, CT.S
        ],
        ["MapAssign", CT.LP, CT.Unary, CT.S, CT.Name, CT.RP, CT.S],
        ["PythonExecute", CT.LP, CT.Fix, CT.RP, CT.S],
        ["pyexec", CT.LP, CT.Fix, CT.RP, CT.S],
        [CT.Arrow, CT.S, CT.Fix],
        [CT.Fix]
    ]
}
