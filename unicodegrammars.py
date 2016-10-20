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
        [CharcoalToken.Arrows],
        ["+", CharcoalToken.Multidirectional],
        ["X", CharcoalToken.Multidirectional],
        ["*", CharcoalToken.Multidirectional],
        ["|", CharcoalToken.Multidirectional],
        ["-", CharcoalToken.Multidirectional],
        ["\\", CharcoalToken.Multidirectional],
        ["/", CharcoalToken.Multidirectional],
        ["<", CharcoalToken.Multidirectional],
        [">", CharcoalToken.Multidirectional],
        ["^", CharcoalToken.Multidirectional],
        ["K", CharcoalToken.Multidirectional],
        ["L", CharcoalToken.Multidirectional],
        ["T", CharcoalToken.Multidirectional],
        ["V", CharcoalToken.Multidirectional],
        ["Y", CharcoalToken.Multidirectional],
        ["7", CharcoalToken.Multidirectional],
        ["¬", CharcoalToken.Multidirectional],
        []
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
        [CharcoalToken.Arrow]
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
    CharcoalToken.ArrowList: [
        ["⟦", CharcoalToken.Multidirectional, "⟧"]
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
        ["∨"],
        ["…"]
    ],

    CharcoalToken.Program: [
        [CharcoalToken.Command, CharcoalToken.Program],
        []
    ],
    CharcoalToken.Body: [
        ["«", CharcoalToken.Program, "»"],
        [CharcoalToken.Command]
    ],
    CharcoalToken.Command: [
        ["Ｓ", CharcoalToken.Name],
        ["Ｎ", CharcoalToken.Name],
        ["Ｖ", CharcoalToken.Expression],
        [CharcoalToken.Arrow, CharcoalToken.Expression],
        [CharcoalToken.Expression],
        ["Ｐ", CharcoalToken.Multidirectional, CharcoalToken.Expression],
        ["Ｐ", CharcoalToken.Expression],
        ["Ｇ", CharcoalToken.Sides, CharcoalToken.Expression],
        [
            "Ｇ",
            CharcoalToken.Multidirectional,
            CharcoalToken.Expression,
            CharcoalToken.Expression
        ],
        ["ＧＨ", CharcoalToken.Sides, CharcoalToken.Expression],
        [
            "ＧＨ",
            CharcoalToken.Multidirectional,
            CharcoalToken.Expression,
            CharcoalToken.Expression
        ],
        ["ＢＲ", CharcoalToken.Expression, CharcoalToken.Expression],
        [
            "Ｂ",
            CharcoalToken.Expression,
            CharcoalToken.Expression,
            CharcoalToken.Expression
        ],
        [CharcoalToken.Arrow],
        ["Ｍ", CharcoalToken.Arrow],
        ["Ｍ", CharcoalToken.Expression, CharcoalToken.Arrow],
        ["↶", CharcoalToken.Expression],
        ["↶"],
        ["↷", CharcoalToken.Expression],
        ["↷"],
        ["Ｊ", CharcoalToken.Expression, CharcoalToken.Expression],
        ["‖Ｔ", CharcoalToken.ArrowList],
        ["‖Ｔ", CharcoalToken.Arrow],
        ["‖Ｍ", CharcoalToken.ArrowList],
        ["‖Ｍ", CharcoalToken.Arrow],
        ["⟲Ｃ", CharcoalToken.List],
        ["⟲Ｃ", CharcoalToken.Expression],
        ["‖Ｃ", CharcoalToken.ArrowList],
        ["‖Ｃ", CharcoalToken.Arrow],
        ["⟲Ｏ", CharcoalToken.List],
        ["⟲Ｏ", CharcoalToken.Expression],
        ["‖Ｏ", CharcoalToken.ArrowList],
        ["‖Ｏ", CharcoalToken.Arrow],
        ["⟲", CharcoalToken.Expression],
        ["‖", CharcoalToken.Arrow],
        ["Ｃ", CharcoalToken.Expression, CharcoalToken.Expression],
        ["Ｆ", CharcoalToken.Expression, CharcoalToken.Body],
        ["Ｗ", CharcoalToken.Expression, CharcoalToken.Body],
        [
            "¿",
            CharcoalToken.Expression,
            CharcoalToken.Body,
            CharcoalToken.Body
        ],
        ["¿", CharcoalToken.Expression, CharcoalToken.Body],
        ["Ａ", CharcoalToken.Expression, CharcoalToken.Name],
        ["¤", CharcoalToken.Expression],
        ["ＵＢ", CharcoalToken.Expression],
        ["Ｄ"],
        [
            "ＨＦ",
            CharcoalToken.Expression,
            CharcoalToken.Expression,
            CharcoalToken.Body
        ],
        [
            "ＨＷ",
            CharcoalToken.Expression,
            CharcoalToken.Expression,
            CharcoalToken.Body
        ],
        ["Ｈ", CharcoalToken.Expression],
        ["Ｈ"],
        ["Ｔ", CharcoalToken.Expression, CharcoalToken.Expression],
        ["⎚"],
        ["Ｅ", CharcoalToken.Expression, CharcoalToken.Expression],
        ["Ｅ", CharcoalToken.Expression]
    ]
}
