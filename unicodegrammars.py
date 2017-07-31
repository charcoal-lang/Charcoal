from charcoaltoken import CharcoalToken as CT
import re

UnicodeGrammars = {
    CT.Arrow: [
        ["←"], ["↑"], ["→"], ["↓"], ["↖"], ["↗"], ["↘"], ["↙"]
    ],
    CT.Multidirectional: [
        [CT.Arrows, CT.Multidirectional],
        ["+", CT.Multidirectional],
        ["X", CT.Multidirectional],
        ["*", CT.Multidirectional],
        ["|", CT.Multidirectional],
        ["-", CT.Multidirectional],
        ["\\", CT.Multidirectional],
        ["/", CT.Multidirectional],
        ["<", CT.Multidirectional],
        [">", CT.Multidirectional],
        ["^", CT.Multidirectional],
        ["K", CT.Multidirectional],
        ["L", CT.Multidirectional],
        ["T", CT.Multidirectional],
        ["V", CT.Multidirectional],
        ["Y", CT.Multidirectional],
        ["7", CT.Multidirectional],
        ["¬", CT.Multidirectional],
        ["⟦", CT.Multidirectional, "⟧"],
        [CT.Separator]
    ],
    CT.Side: [
        [CT.Arrow, CT.Expression]
    ],
    CT.Separator: [
        ["¦"], []
    ],
    CT.Span: [
        [CT.Expression, "；", CT.Expression, "；", CT.Expression],
        [CT.Expression, "；", "；", CT.Expression],
        [CT.Expression, "；", CT.Expression],
        [CT.Expression, "；"],
        ["；", CT.Expression, "；", CT.Expression],
        ["；", CT.Expression],
        ["；", "；", CT.Expression],
        ["；", "；"]
    ],

    CT.Arrows: [
        [CT.Arrow, CT.Arrows],[CT.Arrow]
    ],
    CT.Sides: [
        [CT.Side, CT.Sides], [CT.Side]
    ],
    CT.Expressions: [
        [CT.Expression, CT.Expressions],
        [CT.Expression]
    ],
    CT.WolframExpressions: [
        [CT.WolframExpression, CT.WolframExpressions],
        [CT.WolframExpression]
    ],
    CT.PairExpressions: [
        [CT.Expression, CT.Expression, CT.PairExpressions],
        [CT.Expression, CT.Expression]
    ],
    CT.Cases: [
        [CT.Expression, CT.Body, CT.Cases], []
    ],

    CT.WolframList: [
        ["⟦", CT.WolframExpressions, "⟧"], ["⟦", "⟧"]
    ],
    CT.List: [
        ["⟦", CT.Expressions, "⟧"], ["⟦", "⟧"]
    ],
    CT.Dictionary: [
        ["⦃", CT.PairExpressions, "⦄"], ["⦃", "⦄"]
    ],

    CT.WolframExpression: [
        [CT.Span, CT.Separator],
        [CT.Expression]
    ],
    CT.Expression: [
        [CT.Number, CT.Separator],
        [CT.String, CT.Separator],
        [CT.Name, CT.Separator],
        [CT.List, CT.Separator],
        [CT.Dictionary, CT.Separator],
        ["«", CT.Program, "»", CT.Separator],
        [CT.OtherOperator, CT.Separator],
        [
            CT.LazyQuarternary, CT.Expression, CT.Expression, CT.Expression,
            CT.Expression
        ],
        [
            CT.Quarternary, CT.Expression, CT.Expression, CT.Expression,
            CT.Expression
        ],
        [CT.LazyTernary, CT.Expression, CT.Expression, CT.Expression],
        [CT.Ternary, CT.Expression, CT.Expression, CT.Expression],
        [CT.LazyBinary, CT.Expression, CT.Expression],
        [CT.Binary, CT.Expression, CT.Expression],
        [CT.LazyUnary, CT.Expression],
        [CT.Unary, CT.Expression],
        [CT.Nilary, CT.Separator]
    ],
    CT.Nilary: [
        ["Ｓ"], ["Ｎ"], ["‽"], ["ＫＡ"], ["ＫＭ"], ["ＫＶ"], ["ＫＫ"]
    ],
    CT.Unary: [
        ["±"], ["Ｌ"], ["¬"], ["Ｉ"], ["‽"], ["Ｖ"], ["⊟"], ["↧"], ["↥"], ["⌊"],
        ["⌈"], ["℅"], ["⮌"], ["≕"], ["″"], ["‴"], ["✂"], ["…·"], ["…"], ["～"]
    ],
    CT.Binary: [
        ["⁺"], ["⁻"], ["×"], ["÷"], ["∕"], ["﹪"], ["⁼"], ["‹"], ["›"], ["＆"],
        ["｜"], ["…·"], ["…"], ["Ｘ"], ["§"], ["⊞Ｏ"], ["⪫"], ["⪪"], ["⌕Ａ"],
        ["⌕"], ["◧"], ["◨"], ["№"], ["➙"], ["⧴"], ["？"], ["✂"], ["⊙"],
        ["⬤"]
    ],
    CT.Ternary: [
        ["✂"]
    ],
    CT.Quarternary: [
        ["✂"]
    ],
    CT.LazyUnary: [
    ],
    CT.LazyBinary: [
        ["∧"], ["∨"]
    ],
    CT.LazyTernary: [
        ["⎇"]
    ],
    CT.LazyQuarternary: [
    ],
    CT.OtherOperator: [
        ["ＫＤ", CT.Expression, CT.Arrow],
        ["Ｅ", CT.Expression, CT.Expression],
        ["▷", CT.Expression, CT.WolframList],
        ["▷", CT.Expression, CT.WolframExpression]
    ],

    CT.Program: [
        [CT.Command, CT.Separator, CT.Program],
        []
    ],
    CT.Body: [
        ["«", CT.Program, "»"],
        [CT.Command, CT.Separator]
    ],
    CT.Command: [
        ["Ｓ", CT.Name],
        ["Ｎ", CT.Name],
        ["Ｖ", CT.Expression],
        [CT.Arrow, CT.Expression],
        [CT.Expression],
        ["Ｐ", CT.Multidirectional, CT.Expression],
        ["Ｐ", CT.Expression],
        ["Ｇ", CT.Sides, CT.Expression],
        ["Ｇ", CT.Multidirectional, CT.Expression, CT.Expression],
        ["ＧＨ", CT.Sides, CT.Expression],
        ["ＧＨ", CT.Multidirectional, CT.Expression, CT.Expression],
        ["ＵＲ", CT.Expression, CT.Expression],
        ["ＵＲ", CT.Expression],
        ["ＵＯ", CT.Expression, CT.Expression, CT.Expression],
        ["ＵＯ", CT.Expression, CT.Expression],
        ["Ｂ", CT.Expression, CT.Expression, CT.Expression],
        ["Ｂ", CT.Expression, CT.Expression],
        [CT.Arrow],
        ["Ｍ", CT.Arrow],
        ["Ｍ", CT.Expression, CT.Arrow],
        ["Ｍ", CT.Expression, CT.Expression],
        ["↶", CT.Expression],
        ["↶"],
        ["↷", CT.Expression],
        ["↷"],
        ["Ｊ", CT.Expression, CT.Expression],
        ["⟲Ｔ", CT.Expression],
        ["⟲Ｔ"],
        ["‖Ｔ", CT.Multidirectional],
        ["‖Ｔ", CT.Arrow],
        ["‖Ｔ"],
        ["⟲Ｐ", CT.Arrow, CT.Number, CT.Separator],
        ["⟲Ｐ", CT.Arrow, CT.Expression],
        ["⟲Ｐ", CT.Arrow],
        ["⟲Ｐ", CT.Number, CT.Separator],
        ["⟲Ｐ", CT.Expression],
        ["⟲Ｐ"],
        ["‖Ｍ", CT.Multidirectional],
        ["‖Ｍ", CT.Arrow],
        ["‖Ｍ"],
        ["⟲Ｃ", CT.Arrow, CT.Number, CT.Separator],
        ["⟲Ｃ", CT.Arrow, CT.Expression],
        ["⟲Ｃ", CT.Arrow],
        ["⟲Ｃ", CT.Number, CT.Separator],
        ["⟲Ｃ", CT.Expression],
        ["⟲Ｃ"],
        ["‖Ｃ", CT.Multidirectional],
        ["‖Ｃ", CT.Arrow],
        ["‖Ｃ"],
        ["⟲ＯＯ", CT.Arrow, CT.Number, CT.Separator, CT.Expression],
        ["⟲ＯＯ", CT.Arrow, CT.Expression, CT.Expression],
        ["⟲ＯＯ", CT.Arrow, CT.Expression],
        ["⟲ＯＯ", CT.Number, CT.Separator, CT.Expression],
        ["⟲ＯＯ", CT.Expression, CT.Expression],
        ["⟲ＯＯ", CT.Expression],
        ["⟲Ｏ", CT.Arrow, CT.Number, CT.Separator ],
        ["⟲Ｏ", CT.Arrow, CT.Expression],
        ["⟲Ｏ", CT.Arrow],
        ["⟲Ｏ", CT.Number, CT.Separator],
        ["⟲Ｏ", CT.Expression],
        ["⟲Ｏ"],
        ["⟲ＳＯ", CT.Arrow, CT.Number, CT.Separator, CT.Expression],
        ["⟲ＳＯ", CT.Arrow, CT.Expression, CT.Expression],
        ["⟲ＳＯ", CT.Arrow, CT.Expression],
        ["⟲ＳＯ", CT.Number, CT.Separator, CT.Expression],
        ["⟲ＳＯ", CT.Expression, CT.Expression],
        ["⟲ＳＯ", CT.Expression],
        ["⟲Ｓ", CT.Arrow, CT.Number, CT.Separator],
        ["⟲Ｓ", CT.Arrow, CT.Expression],
        ["⟲Ｓ", CT.Arrow],
        ["⟲Ｓ", CT.Number, CT.Separator],
        ["⟲Ｓ", CT.Expression],
        ["⟲Ｓ"],
        ["‖ＯＯ", CT.Multidirectional, CT.Expression],
        ["‖ＯＯ", CT.Arrow, CT.Expression],
        ["‖ＯＯ", CT.Expression],
        ["‖Ｏ", CT.Multidirectional],
        ["‖Ｏ", CT.Arrow],
        ["‖Ｏ"],
        ["‖ＢＯ", CT.Multidirectional, CT.Expression],
        ["‖ＢＯ", CT.Arrow, CT.Expression],
        ["‖ＢＯ", CT.Expression],
        ["‖Ｂ", CT.Multidirectional],
        ["‖Ｂ", CT.Arrow],
        ["‖Ｂ"],
        ["⟲", CT.Expression],
        ["⟲"],
        ["‖", CT.Arrow],
        ["‖"],
        ["Ｃ", CT.Expression, CT.Expression],
        ["Ｆ", CT.Expression, CT.Body],
        ["Ｗ", CT.Expression, CT.Body],
        ["¿", CT.Expression, CT.Body, CT.Body],
        ["¿", CT.Expression, CT.Body],
        ["Ａ§", CT.Expression, CT.Expression, CT.Expression],
        ["Ａ", CT.Expression, CT.Name],
        ["Ａ", CT.Expression, CT.Expression],
        ["¤", CT.Expression],
        ["ＵＢ", CT.Expression],
        ["Ｄ"],
        ["ＲＦ", CT.Expression, CT.Expression, CT.Body],
        ["ＲＷ", CT.Expression, CT.Expression, CT.Body],
        ["Ｒ", CT.Expression],
        ["Ｒ"],
        ["ＵＴ"],
        ["Ｔ", CT.Expression, CT.Expression],
        ["Ｔ", CT.Expression],
        ["⎚"],
        ["ＵＥ", CT.Expression, CT.Expression],
        ["ＵＥ", CT.Expression],
        ["⊞", CT.Expression, CT.Expression],
        ["≡", CT.Expression, CT.Cases, CT.Body],
        ["≡", CT.Expression, CT.Cases],
        ["ＵＭ", CT.Expression, CT.Expression],
        ["▶", CT.Expression, CT.WolframList],
        ["▶", CT.Expression, CT.WolframExpression],
        ["≔", CT.Expression, CT.Expression]
    ]
}

