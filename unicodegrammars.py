from charcoaltoken import CharcoalToken
from inspect import signature
import re

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
    CharcoalToken.PairExpressions: [
        [
            CharcoalToken.Expression,
            CharcoalToken.Expression,
            CharcoalToken.PairExpressions
        ],
        [CharcoalToken.Expression, CharcoalToken.Expression]
    ],
    CharcoalToken.Cases: [
        [CharcoalToken.Expression, CharcoalToken.Body, CharcoalToken.Cases],
        []
    ],

    CharcoalToken.List: [
        ["⟦", CharcoalToken.Expressions, "⟧"],
        ["⟦", "⟧"]
    ],
    CharcoalToken.ArrowList: [
        ["⟦", CharcoalToken.Multidirectional, "⟧"],
        ["⟦", "⟧"]
    ],
    CharcoalToken.Dictionary: [
        ["⦃", CharcoalToken.PairExpressions, "⦄"],
        ["⦃", "⦄"]
    ],

    CharcoalToken.Expression: [
        [CharcoalToken.Number, CharcoalToken.Separator],
        [CharcoalToken.String, CharcoalToken.Separator],
        [CharcoalToken.Name, CharcoalToken.Separator],
        [CharcoalToken.List, CharcoalToken.Separator],
        [CharcoalToken.Dictionary, CharcoalToken.Separator],
        [
            CharcoalToken.OtherOperator,
            CharcoalToken.Separator
        ],
        [
            CharcoalToken.LazyTernary,
            CharcoalToken.Expression,
            CharcoalToken.Expression,
            CharcoalToken.Expression
        ],
        [
            CharcoalToken.Ternary,
            CharcoalToken.Expression,
            CharcoalToken.Expression,
            CharcoalToken.Expression
        ],
        [
            CharcoalToken.LazyBinary,
            CharcoalToken.Expression,
            CharcoalToken.Expression
        ],
        [
            CharcoalToken.Binary,
            CharcoalToken.Expression,
            CharcoalToken.Expression
        ],
        [
            CharcoalToken.LazyUnary,
            CharcoalToken.Expression
        ],
        [
            CharcoalToken.Unary,
            CharcoalToken.Expression
        ],
        [CharcoalToken.Nilary, CharcoalToken.Separator]
    ],
    CharcoalToken.Nilary: [
        ["Ｓ"],
        ["Ｎ"],
        ["‽"],
        ["ＫＡ"],
        ["ＫＭ"],
        ["ＫＶ"],
        ["ＫＫ"]
    ],
    CharcoalToken.Unary: [
        ["±"],
        ["Ｌ"],
        ["¬"],
        ["Ｉ"],
        ["‽"],
        ["Ｖ"],
        ["⊟"],
        ["↧"],
        ["↥"],
        ["⌊"],
        ["⌈"],
        ["℅"],
        ["⮌"]
    ],
    CharcoalToken.Binary: [
        ["⁺"],
        ["⁻"],
        ["×"],
        ["÷"],
        ["﹪"],
        ["⁼"],
        ["‹"],
        ["›"],
        ["…·"],
        ["…"],
        ["Ｘ"],
        ["§"],
        ["⊞Ｏ"],
        ["⪫"],
        ["⪪"],
        ["⌕Ａ"],
        ["⌕"],
        ["◧"],
        ["◨"],
        ["№"]
    ],
    CharcoalToken.Ternary: [
    ],
    CharcoalToken.LazyUnary: [
    ],
    CharcoalToken.LazyBinary: [
        ["∧"],
        ["∨"]
    ],
    CharcoalToken.LazyTernary: [
        ["⎇"]
    ],
    CharcoalToken.OtherOperator: [
        ["ＫＤ", CharcoalToken.Expression, CharcoalToken.Arrow],
        ["Ｅ", CharcoalToken.Expression, CharcoalToken.Expression]
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
        ["ＵＲ", CharcoalToken.Expression, CharcoalToken.Expression],
        [
            "ＵＯ",
            CharcoalToken.Expression,
            CharcoalToken.Expression,
            CharcoalToken.Expression
        ],
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
        ["⟲Ｔ", CharcoalToken.Expression],
        ["⟲Ｔ"],
        ["‖Ｔ", CharcoalToken.Arrow],
        ["⟲Ｐ", CharcoalToken.Arrow, CharcoalToken.Number, CharcoalToken.Separator],
        ["⟲Ｐ", CharcoalToken.Arrow, CharcoalToken.List],
        ["⟲Ｐ", CharcoalToken.Arrow, CharcoalToken.Expression],
        ["⟲Ｐ", CharcoalToken.Arrow],
        ["⟲Ｐ", CharcoalToken.Number, CharcoalToken.Separator],
        ["⟲Ｐ", CharcoalToken.List],
        ["⟲Ｐ", CharcoalToken.Expression],
        ["⟲Ｐ"],
        ["‖Ｍ", CharcoalToken.ArrowList],
        ["‖Ｍ", CharcoalToken.Arrow],
        ["⟲Ｃ", CharcoalToken.Arrow, CharcoalToken.Number, CharcoalToken.Separator],
        ["⟲Ｃ", CharcoalToken.Arrow, CharcoalToken.List],
        ["⟲Ｃ", CharcoalToken.Arrow, CharcoalToken.Expression],
        ["⟲Ｃ", CharcoalToken.Arrow],
        ["⟲Ｃ", CharcoalToken.Number, CharcoalToken.Separator],
        ["⟲Ｃ", CharcoalToken.List],
        ["⟲Ｃ", CharcoalToken.Expression],
        ["⟲Ｃ"],
        ["‖Ｃ", CharcoalToken.ArrowList],
        ["‖Ｃ", CharcoalToken.Arrow],
        ["‖Ｏ", CharcoalToken.ArrowList],
        ["‖Ｏ", CharcoalToken.Arrow],
        ["⟲", CharcoalToken.Expression],
        ["⟲"],
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
        ["Ａ§", CharcoalToken.Expression, CharcoalToken.Expression, CharcoalToken.Expression],
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
        ["ＵＴ"],
        ["Ｔ", CharcoalToken.Expression, CharcoalToken.Expression],
        ["⎚"],
        ["ＵＥ", CharcoalToken.Expression, CharcoalToken.Expression],
        ["ＵＥ", CharcoalToken.Expression],
        ["⊞", CharcoalToken.Expression, CharcoalToken.Expression],
        ["≡", CharcoalToken.Expression, CharcoalToken.Cases, CharcoalToken.Body],
        ["ＵＭ", CharcoalToken.Expression, CharcoalToken.Expression]
    ]
}

