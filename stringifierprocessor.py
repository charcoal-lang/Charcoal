from charcoaltoken import CharcoalToken as CT
from unicodegrammars import UnicodeGrammars
from compression import Compressed
from codepage import rCommand
import re

SuperscriptToNormal = "⁰¹²³⁴⁵⁶⁷⁸⁹"

StringifierProcessor = {
    CT.Arrow: [
        (lambda i: lambda r: "↖↗↘↙←↑→↓"[i])(i)
        for i in range(8)
    ] + [
        lambda r: "✳" + r[2],
    ],
    CT.Multidirectional: [
        lambda r: r[0] + r[1] + r[2],
        lambda r: "+" + r[1] + r[2],
        lambda r: "X" + r[1] + r[2],
        lambda r: "*" + r[1] + r[2],
        lambda r: "|" + r[1] + r[2],
        lambda r: "-" + r[1] + r[2],
        lambda r: "\\" + r[1] + r[2],
        lambda r: "/" + r[1] + r[2],
        lambda r: "<" + r[1] + r[2],
        lambda r: ">" + r[1] + r[2],
        lambda r: "^" + r[1] + r[2],
        lambda r: "K" + r[1] + r[2],
        lambda r: "L" + r[1] + r[2],
        lambda r: "T" + r[1] + r[2],
        lambda r: "V" + r[1] + r[2],
        lambda r: "Y" + r[1] + r[2],
        lambda r: "7" + r[1] + r[2],
        lambda r: "¬" + r[1] + r[2],
        lambda r: "⟦" + r[1] + "⟧",
        lambda r: "✳✳" + r[2],
        lambda r: r[0]
    ],
    CT.Side: [
        lambda r: r[0] + r[2],
        lambda r: r[0]
    ],
    CT.Separator: [
        lambda r: "¦",
        lambda r: "¦",
        lambda r: ""
    ],
    CT.String: [
        lambda r: [Compressed(
            rCommand.sub(r"´\1", r[0])
                    .replace("\n", "¶")
                    .replace("\r", "⸿"),
            True
        )]
    ],
    CT.Number: [
        lambda r: ["".join(
            ("·" if n == "." else SuperscriptToNormal[int(n)])
            for n in str(r[0])
        )]
    ],
    CT.Name: [
        lambda r: "αβγδεζηθικλμνξπρσςτυφχψω"[
            "abgdezhqiklmnxprsvtufcyw".index(r[0])
        ]
    ],
    CT.Span: [
        lambda r: r[0] + "；" + r[2] + "；" + r[4],
        lambda r: r[0] + "；；" + r[3],
        lambda r: r[0] + "；" + r[2],
        lambda r: r[0] + "；",
        lambda r: "；" + r[1] + "；" + r[3],
        lambda r: "；" + r[1],
        lambda r: "；；" + r[2],
        lambda r: "；；"
    ],

    CT.Arrows: [
        lambda r: r[0] + r[2],
        lambda r: r[0]
    ],
    CT.Sides: [
        lambda r: r[0] + r[2],
        lambda r: r[0]
    ],
    CT.Expressions: [
        lambda r: r[0] + r[1],
        lambda r: r[0]
    ],
    CT.WolframExpressions: [
        lambda r: r[0] + r[1],
        lambda r: r[0]
    ],
    CT.PairExpressions: [
        lambda r: r[0] + r[1] + r[2],
        lambda r: r[0] + r[1]
    ],
    CT.Cases: [
        lambda r: r[1] + r[3] + r[5],
        lambda r: ""
    ],

    CT.List: [
        lambda r: "⟦" + r[1] + "⟧",
        lambda r: "⟦⟧"
    ],
    CT.WolframList: [
        lambda r: "⟦" + r[1] + "⟧",
        lambda r: "⟦⟧"
    ],
    CT.Dictionary: [
        lambda r: "⦃" + r[1] + "⦄",
        lambda r: "⦃⦄"
    ],

    CT.WolframExpression: [
        lambda r: r[0] + r[1],
        lambda r: r[0],
    ],
    CT.Expression: [
        lambda r: r[0] + r[1],
        lambda r: r[0] + r[1],
        lambda r: r[0] + r[1],
        lambda r: r[0] + r[1],
        lambda r: "⟦" + r[1] + "⟧" + r[3],
        lambda r: r[0] + r[1],
        lambda r: "«" + r[1] + "»" + r[3],
        lambda r: r[0] + r[1],
        lambda r: r[0] + r[2] + r[3] + r[4] + r[5] + r[7],
        lambda r: r[0] + r[2] + r[3] + r[4] + r[5] + r[7],
        lambda r: r[0] + r[2] + r[3] + r[4] + r[6],
        lambda r: r[0] + r[2] + r[3] + r[4] + r[6],
        lambda r: r[0] + r[2] + r[3] + r[5],
        lambda r: r[0] + r[2] + r[3] + r[5],
        lambda r: r[0] + r[2] + r[4],
        lambda r: r[0] + r[2] + r[4],
        lambda r: r[0] + r[3]
    ],
    CT.Nilary: [
        lambda r: "Ｓ",
        lambda r: "Ｎ",
        lambda r: "‽",
        lambda r: "ＫＡ",
        lambda r: "ＫＭ",
        lambda r: "ＫＶ",
        lambda r: "ＫＫ",
        lambda r: "ⅈ",
        lambda r: "ⅉ",
        lambda r: "ⅈ",
        lambda r: "ⅉ"
    ],
    CT.Unary: [
        (lambda i: lambda r: "±Ｌ¬Ｉ‽ＶＶ⊟↧↥⌊⌈℅℅℅℅⮌≕″‴✂…·…～～"[i])(i)
        for i in range(25)
    ],
    CT.Binary: [
        (lambda i: lambda r: "Ｘ⁺⁺⁺⁻⁻⁻×××÷∕∕∕÷÷﹪﹪⁼⁼‹‹››＆＆｜｜"[i])(i)
        for i in range(28)
    ] + [
        lambda r: "…·",
        lambda r: "…",
        lambda r: "…",
        lambda r: "…",
        lambda r: "Ｘ",
        lambda r: "Ｘ",
        lambda r: "Ｘ",
        lambda r: "§",
        lambda r: "⊞Ｏ",
        lambda r: "⪫",
        lambda r: "⪪",
        lambda r: "⌕Ａ",
    ] + [
        (lambda i: lambda r: "⌕◧◨№➙⧴？✂⊙⊙⬤⬤"[i])(i)
        for i in range(12)
    ],
    CT.Ternary: [lambda r: "✂"],
    CT.Quarternary: [lambda r: "✂"],
    CT.LazyUnary: [],
    CT.LazyBinary: [(lambda i: lambda r: "∧∨∧∨"[i])(i) for i in range(4)],
    CT.LazyTernary: [lambda r: "⎇"],
    CT.LazyQuarternary: [],
    CT.OtherOperator: [
        lambda r: "ＫＤ" + r[2] + r[3],
        lambda r: "Ｅ" + r[2] + r[3],
        lambda r: "Ｅ" + r[2] + r[3],
        lambda r: "ＵＰ" + r[2] + r[3],
        lambda r: "ＵＰ" + r[2],
        lambda r: "▷" + r[2] + r[3],
        lambda r: "▷" + r[2] + r[3],
        lambda r: "▷" + r[2] + r[3],
        lambda r: "▷" + r[2] + r[3]
    ],

    CT.Program: [
        lambda r: r[0] + ("¦" if r[2] else "") + r[3],
        lambda r: ""
    ],
    CT.Body: [
        lambda r: "«" + r[1] + "»",
        lambda r: r[0]
    ],
    CT.Command: [
        lambda r: "ＵＰ" + r[2] + r[3],
        lambda r: "ＵＰ" + r[2],
        lambda r: "Ｓ" + r[2],
        lambda r: "Ｎ" + r[2],
        lambda r: "Ｖ" + r[2],
        lambda r: "Ｖ" + r[2],
        lambda r: r[2] + r[4],
        lambda r: r[2],
        lambda r: "Ｐ" + r[2] + r[4],
        lambda r: "Ｐ" + r[2],
        lambda r: "Ｇ" + r[2] + r[4],
        lambda r: "Ｇ" + r[2] + r[4] + r[5],
        lambda r: "ＧＨ" + r[2] + r[4],
        lambda r: "ＧＨ" + r[2] + r[4] + r[5],
        lambda r: "ＵＲ" + r[2] + r[3],
        lambda r: "ＵＲ" + r[2] + "¦¦",
        lambda r: "ＵＯ" + r[2] + r[3] + r[4],
        lambda r: "ＵＯ" + r[2] + r[3] + "¦¦",
        lambda r: "Ｂ" + r[2] + r[3] + r[4],
        lambda r: "Ｂ" + r[2] + r[3] + "¦¦",
        lambda r: "Ｍ" + r[2],
        lambda r: "Ｍ" + r[2] + r[3],
        lambda r: "Ｍ" + r[2] + r[3],
        lambda r: "Ｍ" + r[2] + r[3],
        lambda r: "↶" + r[2],
        lambda r: "↶",
        lambda r: "↷" + r[2],
        lambda r: "↷",
        lambda r: "Ｊ" + r[2] + r[3],
        lambda r: "⟲Ｔ" + r[2],
        lambda r: "⟲Ｔ",
        lambda r: "‖Ｔ" + r[2],
        lambda r: "‖Ｔ" + r[2],
        lambda r: "‖Ｔ",
        lambda r: "⟲Ｐ" + r[2] + r[4],
        lambda r: "⟲Ｐ" + r[2],
        lambda r: "⟲Ｐ" + r[2],
        lambda r: "⟲Ｐ",
        lambda r: "‖Ｍ" + r[2],
        lambda r: "‖Ｍ" + r[2],
        lambda r: "‖Ｍ",
        lambda r: "⟲Ｃ" + r[2] + r[4],
        lambda r: "⟲Ｃ" + r[2],
        lambda r: "⟲Ｃ" + r[2],
        lambda r: "⟲Ｃ",
        lambda r: "‖Ｃ" + r[2],
        lambda r: "‖Ｃ" + r[2],
        lambda r: "‖Ｃ",
        lambda r: "⟲ＯＯ" + r[2:-1],
        lambda r: "⟲ＯＯ" + r[2:-1],
        lambda r: "⟲ＯＯ" + r[2] + r[4] + r[5],
        lambda r: "⟲ＯＯ" + r[2] + r[3],
        lambda r: "⟲ＯＯ" + r[2],
        lambda r: "⟲Ｏ" + r[2] + r[4],
        lambda r: "⟲Ｏ" + r[2],
        lambda r: "⟲Ｏ" + r[2],
        lambda r: "⟲Ｏ",
        lambda r: "⟲ＳＯ" + r[2:-1],
        lambda r: "⟲ＳＯ" + r[2:-1],
        lambda r: "⟲ＳＯ" + r[2] + r[4] + r[5],
        lambda r: "⟲ＳＯ" + r[2] + r[3],
        lambda r: "⟲ＳＯ" + r[2],
        lambda r: "⟲Ｓ" + r[2] + r[4],
        lambda r: "⟲Ｓ" + r[2],
        lambda r: "⟲Ｓ" + r[2],
        lambda r: "⟲Ｓ",
        lambda r: "‖ＯＯ" + r[2] + r[3] + r[4],
        lambda r: "‖ＯＯ" + r[2] + r[4],
        lambda r: "‖ＯＯ" + r[2],
        lambda r: "‖Ｏ" + r[2],
        lambda r: "‖Ｏ" + r[2],
        lambda r: "‖Ｏ",
        lambda r: "‖ＢＯ" + r[2] + r[3] + r[4],
        lambda r: "‖ＢＯ" + r[2] + r[4],
        lambda r: "‖ＢＯ" + r[2],
        lambda r: "‖Ｂ" + r[2],
        lambda r: "‖Ｂ" + r[2],
        lambda r: "‖Ｂ",
        lambda r: "⟲" + r[2],
        lambda r: "⟲",
        lambda r: "‖" + r[2],
        lambda r: "‖",
        lambda r: "Ｃ" + r[2] + r[3],
        lambda r: "Ｆ" + r[2] + r[4],
        lambda r: "Ｗ" + r[2] + r[4],
        lambda r: "¿" + r[2] + r[4] + r[6],
        lambda r: "¿" + r[2] + r[4],
        lambda r: "Ａ§" + r[2] + r[3] + r[4],
        lambda r: "Ａ" + r[2] + r[3],
        lambda r: "Ａ" + r[2] + r[3],
        lambda r: "¤" + r[2],
        lambda r: "ＵＢ" + r[2],
        lambda r: "Ｄ",
        lambda r: "ＲＦ" + r[2] + r[3] + r[5],
        lambda r: "ＲＷ" + r[2] + r[3] + r[5],
        lambda r: "Ｒ" + r[2],
        lambda r: "Ｒ",
        lambda r: "ＵＴ",
        lambda r: "Ｔ" + r[2] + r[3],
        lambda r: "Ｔ" + r[2] + "¦¦",
        lambda r: "⎚",
        lambda r: "ＵＥ" + r[2] + r[3],
        lambda r: "ＵＥ" + r[2],
        lambda r: "⊞" + r[2] + r[3],
        lambda r: "≡" + r[2] + r[5] + r[8],
        lambda r: "≡" + r[2] + r[5],
        lambda r: "ＵＭ" + r[2] + r[3],
        lambda r: "▶" + r[2] + r[3],
        lambda r: "▶" + r[2] + r[3],
        lambda r: "▶" + r[2] + r[3],
        lambda r: "▶" + r[2] + r[3],
        lambda r: "≔" + r[2] + r[3]
    ]
}
