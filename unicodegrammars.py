from charcoaltoken import CharcoalToken

UnicodeGrammars = {
    CharcoalToken.Arrow: [
        ["←"],
        ["↑"],
        ["→"],
        ["↓"],
        ["↖"],
        ["↗"],
        ["↘"],
        ["↙"]
    ],
    CharcoalToken.Multidirectional: [
        ["+", CharcoalToken.Arrows],
        ["x", CharcoalToken.Arrows],
        ["*", CharcoalToken.Arrows],
        [CharcoalToken.Arrow, CharcoalToken.Arrows]
    ],
    CharcoalToken.Side: [
        [CharcoalToken.Arrow, CharcoalToken.Expression]
    ],
    CharcoalToken.Separator: [
        ["¦"],
        []
    ],

    CharcoalToken.Arrows: [
        [CharcoalToken.Arrow, CharcoalToken.Arrows],
        []
    ],
    CharcoalToken.Sides: [
        [CharcoalToken.Side, CharcoalToken.Sides],
        [CharcoalToken.Side]
    ],
    CharcoalToken.Expressions: [
        [
            CharcoalToken.Expression,
            CharcoalToken.Expressions
        ],
        [CharcoalToken.Expression]
    ],

    CharcoalToken.List: [
        ["⟦", CharcoalToken.Expressions, "⟧"]
    ],

    CharcoalToken.Expression: [
        [CharcoalToken.Number, CharcoalToken.Separator],
        [CharcoalToken.String, CharcoalToken.Separator],
        [CharcoalToken.Name, CharcoalToken.Separator],
        [CharcoalToken.List, CharcoalToken.Separator],
        [
            CharcoalToken.Dyadic,
            CharcoalToken.Expression,
            CharcoalToken.Expression
        ],
        [
            CharcoalToken.Monadic,
            CharcoalToken.Expression
        ],
        [CharcoalToken.Niladic, CharcoalToken.Separator]
    ],
    CharcoalToken.Niladic: [
        ["Ｓ"],
        ["Ｎ"],
        ["‽"]
    ],
    CharcoalToken.Monadic: [
        ["⁻"],
        ["Ｌ"],
        ["¬"],
        ["Ｉ"],
        ["‽"],
        ["Ｖ"]
    ],
    CharcoalToken.Dyadic: [
        ["⁺"],
        ["⁻"],
        ["×"],
        ["÷"],
        ["﹪"],
        ["⁼"],
        ["‹"],
        ["›"],
        ["∧"],
        ["∨"]
    ],

    CharcoalToken.Program: [
        [CharcoalToken.Command, CharcoalToken.Program],
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
        ["«", CharcoalToken.Program, "»"],
        [CharcoalToken.Command]
    ],
    CharcoalToken.Print: [
        [CharcoalToken.Arrow, CharcoalToken.Expression],
        [CharcoalToken.Expression]
    ],
    CharcoalToken.Multiprint: [
        ["Ｐ", CharcoalToken.Multidirectional, CharcoalToken.Expression],
        ["Ｐ", CharcoalToken.Expression]
    ],
    CharcoalToken.Box: [
        [
            "Ｂ",
            CharcoalToken.Expression,
            CharcoalToken.Expression,
            CharcoalToken.Expression
        ]
    ],
    CharcoalToken.Rectangle: [
        ["Ｒ", CharcoalToken.Expression, CharcoalToken.Expression]
    ],
    CharcoalToken.Polygon: [
        ["Ｇ", CharcoalToken.Sides, CharcoalToken.Expression],
        [
            "Ｇ",
            CharcoalToken.Multidirectional,
            CharcoalToken.Expression,
            CharcoalToken.Expression
        ]
    ],
    CharcoalToken.Move: [
        [CharcoalToken.Arrow],
        ["Ｍ", CharcoalToken.Arrow],
        ["Ｍ", CharcoalToken.Expression, CharcoalToken.Arrow]
    ],
    CharcoalToken.Pivot: [
        ["↶", CharcoalToken.Expression],
        ["↶"],
        ["↷", CharcoalToken.Expression],
        ["↷"]
    ],
    CharcoalToken.Jump: [
        ["Ｊ", CharcoalToken.Expression, CharcoalToken.Expression]
    ],
    CharcoalToken.RotateCopy: [
        ["⟲Ｃ", CharcoalToken.Expression]
    ],
    CharcoalToken.ReflectCopy: [
        ["‖Ｃ", CharcoalToken.Arrow]
    ],
    CharcoalToken.RotateOverlap: [
        ["⟲Ｏ", CharcoalToken.Expression]
    ],
    CharcoalToken.ReflectOverlap: [
        ["‖Ｏ", CharcoalToken.Arrow]
    ],
    CharcoalToken.Rotate: [
        ["⟲", CharcoalToken.Expression]
    ],
    CharcoalToken.Reflect: [
        ["‖", CharcoalToken.Arrow]
    ],
    CharcoalToken.Copy: [
        ["Ｃ", CharcoalToken.Expression, CharcoalToken.Expression]
    ],
    CharcoalToken.For: [
        ["Ｆ", CharcoalToken.Expression, CharcoalToken.Body]
    ],
    CharcoalToken.While: [
        ["Ｗ", CharcoalToken.Expression, CharcoalToken.Body]
    ],
    CharcoalToken.If: [
        [
            "¿",
            CharcoalToken.Expression,
            CharcoalToken.Body,
            CharcoalToken.Body
        ],
        ["¿", CharcoalToken.Expression, CharcoalToken.Body]
    ],
    CharcoalToken.Assign: [
        ["Ａ", CharcoalToken.Expression, CharcoalToken.Name]
    ],
    CharcoalToken.Fill: [
        ["¤", CharcoalToken.Expression]
    ],
    CharcoalToken.SetBackground: [
        ["ＵＢ", CharcoalToken.Expression]
    ],
    CharcoalToken.Dump: [
        ["Ｄ"]
    ],
    CharcoalToken.RefreshFor: [
        [
            "ＨＦ",
            CharcoalToken.Expression,
            CharcoalToken.Expression,
            CharcoalToken.Body
        ]
    ],
    CharcoalToken.RefreshWhile: [
        [
            "ＨＷ",
            CharcoalToken.Expression,
            CharcoalToken.Expression,
            CharcoalToken.Body
        ]
    ],
    CharcoalToken.Refresh: [
        ["Ｈ", CharcoalToken.Expression],
        ["Ｈ"]
    ],
    CharcoalToken.Evaluate: [
        ["Ｖ", CharcoalToken.Expression]
    ],
    CharcoalToken.InputString: [
        ["Ｓ", CharcoalToken.Name]
    ],
    CharcoalToken.InputNumber: [
        ["Ｎ", CharcoalToken.Name]
    ]
}
