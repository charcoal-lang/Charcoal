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
            CharcoalToken.Separator,
            CharcoalToken.Expressions
        ],
        [CharcoalToken.Expression]
    ],

    CharcoalToken.List: [
        ["[", CharcoalToken.Expressions, "]"]
    ],

    CharcoalToken.Expression: [
        [CharcoalToken.Number, CharcoalToken.Separator],
        [CharcoalToken.String, CharcoalToken.Separator],
        [CharcoalToken.Name, CharcoalToken.Separator],
        [CharcoalToken.List, CharcoalToken.Separator],
        [
            CharcoalToken.Dyadic,
            "(",
            CharcoalToken.Expression,
            CharcoalToken.Expression,
            ")",
            CharcoalToken.Separator
        ],
        [
            CharcoalToken.Monadic,
            "(",
            CharcoalToken.Expression,
            ")",
            CharcoalToken.Separator
        ],
        [CharcoalToken.Niladic, "(", ")", CharcoalToken.Separator]
    ],
    CharcoalToken.Niladic: [
        ["InputString"],
        ["InputNumber"],
        ["Random"]
    ],
    CharcoalToken.Monadic: [
        ["Negate"],
        ["Length"],
        ["Not"],
        ["Cast"],
        ["Random"],
        ["Evaluate"]
    ],
    CharcoalToken.Dyadic: [
        ["Add"],
        ["Subtract"],
        ["Multiply"],
        ["Divide"],
        ["Modulo"],
        ["Equals"],
        ["LessThan"],
        ["GreaterThan"],
        ["And"],
        ["Or"],
        ["Mold"]
    ],

    CharcoalToken.Program: [
        [CharcoalToken.Command, CharcoalToken.Separator, CharcoalToken.Program],
        []
    ],
    CharcoalToken.Command: [
        [CharcoalToken.InputString],
        [CharcoalToken.InputNumber],
        [CharcoalToken.Evaluate],
        [CharcoalToken.Print],
        [CharcoalToken.Multiprint],
        [CharcoalToken.Polygon],
        [CharcoalToken.Box],
        [CharcoalToken.Rectangle],
        [CharcoalToken.Move],
        [CharcoalToken.Pivot],
        [CharcoalToken.Jump],
        [CharcoalToken.RotateCopy],
        [CharcoalToken.ReflectCopy],
        [CharcoalToken.RotateOverlap],
        [CharcoalToken.ReflectOverlap],
        [CharcoalToken.Rotate],
        [CharcoalToken.Reflect],
        [CharcoalToken.Copy],
        [CharcoalToken.For],
        [CharcoalToken.While],
        [CharcoalToken.If],
        [CharcoalToken.Assign],
        [CharcoalToken.Fill],
        [CharcoalToken.SetBackground],
        [CharcoalToken.Dump],
        [CharcoalToken.RefreshFor],
        [CharcoalToken.RefreshWhile],
        [CharcoalToken.Refresh]
    ],
    CharcoalToken.Body: [
        ["{", CharcoalToken.Program, "}"],
        [CharcoalToken.Command]
    ],
    CharcoalToken.Print: [
        ["Print", "(", CharcoalToken.Arrow, CharcoalToken.Separator, CharcoalToken.Expression, ")"],
        ["Print", "(", CharcoalToken.Expression, ")"]
    ],
    CharcoalToken.Multiprint: [
        [
            "Multiprint",
            "(",
            CharcoalToken.Multidirectional,
            CharcoalToken.Separator,
            CharcoalToken.Expression,
            ")"
        ],
        ["Multiprint", "(", CharcoalToken.Expression, ")"]
    ],
    CharcoalToken.Box: [
        [
            "Box",
            "(",
            CharcoalToken.Expression,
            CharcoalToken.Expression,
            CharcoalToken.Expression,
            ")"
        ]
    ],
    CharcoalToken.Rectangle: [
        ["Rectangle", "(", CharcoalToken.Expression, CharcoalToken.Expression, ")"]
    ],
    CharcoalToken.Polygon: [
        ["Polygon", "(", CharcoalToken.Sides, CharcoalToken.Separator, CharcoalToken.Expression, ")"],
        [
            "Polygon",
            "(",
            CharcoalToken.Multidirectional,
            CharcoalToken.Separator,
            CharcoalToken.Expression,
            CharcoalToken.Expression,
            ")"
        ]
    ],
    CharcoalToken.Move: [
        ["Move", "(", CharcoalToken.Arrow, ")"],
        ["Move", "(", CharcoalToken.Expression, CharcoalToken.Arrow, ")"]
    ],
    CharcoalToken.Pivot: [
        ["PivotLeft", "(", CharcoalToken.Expression, ")"],
        ["PivotLeft", "(", ")"],
        ["PivotRight", "(", CharcoalToken.Expression, ")"],
        ["PivotRight", "(", ")"]
    ],
    CharcoalToken.Jump: [
        ["Jump", "(", CharcoalToken.Expression, CharcoalToken.Expression, ")"]
    ],
    CharcoalToken.RotateCopy: [
        ["RotateCopy", "(", CharcoalToken.Expression, ")"]
    ],
    CharcoalToken.ReflectCopy: [
        ["ReflectCopy", "(", CharcoalToken.Arrow, ")"]
    ],
    CharcoalToken.RotateOverlap: [
        ["RotateOverlap", "(", CharcoalToken.Expression, ")"]
    ],
    CharcoalToken.ReflectOverlap: [
        ["ReflectOverlap", "(", CharcoalToken.Arrow, ")"]
    ],
    CharcoalToken.Rotate: [
        ["Rotate", "(", CharcoalToken.Expression, ")"]
    ],
    CharcoalToken.Reflect: [
        ["Reflect", "(", CharcoalToken.Arrow, ")"]
    ],
    CharcoalToken.Copy: [
        ["Copy", "(", CharcoalToken.Expression, CharcoalToken.Expression, ")"]
    ],
    CharcoalToken.For: [
        ["For", "(", CharcoalToken.Expression, ")", CharcoalToken.Body]
    ],
    CharcoalToken.While: [
        ["While", "(", CharcoalToken.Expression, ")", CharcoalToken.Body]
    ],
    CharcoalToken.If: [
        [
            "If",
            "(",
            CharcoalToken.Expression,
            ")",
            CharcoalToken.Body,
            CharcoalToken.Body
        ],
        ["If", "(", CharcoalToken.Expression, ")", CharcoalToken.Body]
    ],
    CharcoalToken.Assign: [
        ["Assign", "(", CharcoalToken.Expression, CharcoalToken.Name, ")"]
    ],
    CharcoalToken.Fill: [
        ["Fill", "(", CharcoalToken.Expression, ")"]
    ],
    CharcoalToken.SetBackground: [
        ["SetBackground", "(", CharcoalToken.Expression, ")"]
    ],
    CharcoalToken.Dump: [
        ["Dump", "(", ")"]
    ],
    CharcoalToken.RefreshFor: [
        [
            "RefreshFor",
            "(",
            CharcoalToken.Expression,
            ")",
            CharcoalToken.Expression,
            CharcoalToken.Body,
            ")"
        ]
    ],
    CharcoalToken.RefreshWhile: [
        [
            "RefreshWhile",
            "(",
            CharcoalToken.Expression,
            ")",
            CharcoalToken.Expression,
            CharcoalToken.Body
        ]
    ],
    CharcoalToken.Refresh: [
        ["Refresh", "(", CharcoalToken.Expression, ")"],
        ["Refresh", "(", ")"]
    ],
    CharcoalToken.Evaluate: [
        ["Evaluate", "(", CharcoalToken.Expression, ")"]
    ],
    CharcoalToken.InputString: [
        ["InputString", "(", CharcoalToken.Name, ")"]
    ],
    CharcoalToken.InputNumber: [
        ["InputNumber", "(", CharcoalToken.Name, ")"]
    ]
}
