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
    CharcoalToken.ArrowList: [
        ["[", CharcoalToken.Multidirectional, "]"]
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
    CharcoalToken.Body: [
        ["{", CharcoalToken.Program, "}"],
        [CharcoalToken.Command]
    ],
    CharcoalToken.Command: [
        ["InputString", "(", CharcoalToken.Name, ")"],
        ["InputNumber", "(", CharcoalToken.Name, ")"],
        ["Evaluate", "(", CharcoalToken.Expression, ")"],
        ["Print", "(", CharcoalToken.Arrow, CharcoalToken.Separator, CharcoalToken.Expression, ")"],
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
        ["Rectangle", "(", CharcoalToken.Expression, CharcoalToken.Expression, ")"],
        [
            "Box",
            "(",
            CharcoalToken.Expression,
            CharcoalToken.Expression,
            CharcoalToken.Expression,
            ")"
        ],
        ["Move", "(", CharcoalToken.Arrow, ")"],
        ["Move", "(", CharcoalToken.Expression, CharcoalToken.Arrow, ")"],
        ["PivotLeft", "(", CharcoalToken.Expression, ")"],
        ["PivotLeft", "(", ")"],
        ["PivotRight", "(", CharcoalToken.Expression, ")"],
        ["PivotRight", "(", ")"],
        ["Jump", "(", CharcoalToken.Expression, CharcoalToken.Expression, ")"],
        ["RotateCopy", "(", CharcoalToken.List, ")"],
        ["RotateCopy", "(", CharcoalToken.Expression, ")"],
        ["ReflectCopy", "(", CharcoalToken.ArrowList, ")"],
        ["ReflectCopy", "(", CharcoalToken.Arrow, ")"],
        ["RotateOverlap", "(", CharcoalToken.List, ")"],
        ["RotateOverlap", "(", CharcoalToken.Expression, ")"],
        ["ReflectOverlap", "(", CharcoalToken.Arrow, ")"],
        ["ReflectOverlap", "(", CharcoalToken.Arrow, ")"],
        ["Rotate", "(", CharcoalToken.Expression, ")"],
        ["Reflect", "(", CharcoalToken.Arrow, ")"],
        ["Copy", "(", CharcoalToken.Expression, CharcoalToken.Expression, ")"],
        ["For", "(", CharcoalToken.Expression, ")", CharcoalToken.Body],
        ["While", "(", CharcoalToken.Expression, ")", CharcoalToken.Body],
        [
            "If",
            "(",
            CharcoalToken.Expression,
            ")",
            CharcoalToken.Body,
            CharcoalToken.Body
        ],
        ["If", "(", CharcoalToken.Expression, ")", CharcoalToken.Body],
        ["Assign", "(", CharcoalToken.Expression, CharcoalToken.Name, ")"],
        ["Fill", "(", CharcoalToken.Expression, ")"],
        ["SetBackground", "(", CharcoalToken.Expression, ")"],
        ["Dump", "(", ")"],
        [
            "RefreshFor",
            "(",
            CharcoalToken.Expression,
            ")",
            CharcoalToken.Expression,
            CharcoalToken.Body,
            ")"
        ],
        [
            "RefreshWhile",
            "(",
            CharcoalToken.Expression,
            ")",
            CharcoalToken.Expression,
            CharcoalToken.Body
        ],
        ["Refresh", "(", CharcoalToken.Expression, ")"],
        ["Refresh", "(", ")"]
    ]
}
