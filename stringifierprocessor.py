from charcoaltoken import CharcoalToken as CT
from unicodegrammars import UnicodeGrammars
from compression import Compressed
import re

def string(s):
    if s == "":
        return [("v", "ω")]
    if s == "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        return [("v", "α")]
    if s == "abcdefghijklmnopqrstuvwxyz":
        return [("v", "β")]
    if s == " !\"#$%&'()*+,-./0123456789:;<=>?@\
ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~":
        return [("v", "γ")]
    s = Compressed(s)
    if s[0] != "“" and s[0] != "”":
        return [("s", s), ("!", "s")]
    return [("c", s)]

def number(s):
    s = s.lstrip("0")
    if not "." in s:
        if s == "10":
            return [("v", "χ")]
        if s == "1000":
            return [("v", "φ")]
    s = "".join(
        ("·" if n == "." else SuperscriptToNormal[int(n)]) for n in (s or "0")
    )
    return [("n", s), ("!", "n")]

SuperscriptToNormal = "⁰¹²³⁴⁵⁶⁷⁸⁹"

StringifierProcessor = {
    CT.LP: [lambda r: []] * 2,
    CT.RP: [lambda r: []] * 2,
    CT.Arrow: [
        lambda r: [("$", "✳")] + r[2],
    ] + [
        (lambda i: lambda r: [("a", ("↖↗↘↙←↑→↓" * 2)[i])])(i)
        for i in range(16)
    ],
    CT.Multidirectional: [
        lambda r: [("$", "✳✳" )] + r[2],
        lambda r: r[0] + r[2]
    ] + [
        (lambda i: lambda r: [(
            "a",
            "++XX**||--\\/<>^KLTVY7¬⌊⌈¬⌊⌈¬⌊⌈"[i]
        )] + r[2])(i)
        for i in range(30)
    ] + [
        lambda r: [("<", "⟦")] + r[1] + [(">", "⟧")],
        lambda r: [("m", "")]
    ],
    CT.Side: [lambda r: r[0] + r[2]],
    CT.S: [lambda r: []] * 3,
    CT.String: [lambda r: string(r[0])],
    CT.Number: [lambda r: number(r[0])],
    CT.Name: [
        lambda r: [("v", "αβγδεζηθικλμνξπρσςτυφχψω"[
            "abgdezhqiklmnxprsvtufcyw".index(r[0])
        ])]
    ],
    CT.Span: [
        lambda r: r[0] + [("$", "；")] + r[2] + [("$", "；")] + r[4],
        lambda r: r[0] + [("$", "；；")] + r[3],
        lambda r: r[0] + [("$", "；")] + r[2],
        lambda r: r[0] + [("$", "；"), ("!", "e")],
        lambda r: [("$", "；")] + r[1] + [("$", "；")] + r[3],
        lambda r: [("$", "；")] + r[1],
        lambda r: [("$", "；")] + r[2],
        lambda r: [("$", "；"), ("!", "e")],
    ],

    CT.Arrows: [lambda r: r[0] + r[2], lambda r: r[0]],
    CT.Sides: [lambda r: r[0] + r[2], lambda r: r[0]],
    CT.Fixes: [lambda r: r[0] + r[1], lambda r: r[0]],
    CT.WolframExpressions: [lambda r: r[0] + r[1], lambda r: r[0]],
    CT.PairExpressions: [lambda r: r[0] + r[2] + r[3], lambda r: r[0] + r[2]],
    CT.Cases: [lambda r: r[1] + r[3] + r[5] + r[6], lambda r: []],

    CT.List: [
        lambda r: [("<", "⟦")] + r[1] + [(">", "⟧")],
        lambda r: [("<", "⟦"), (">", "⟧")],
    ],
    CT.WolframList: [
        lambda r: [("<", "⟦")] + r[1] + [(">", "⟧")],
        lambda r: [("<", "⟦"), (">", "⟧")],
    ],
    CT.Dictionary: [
        lambda r: [("<", "⦃")] + r[1] + [(">", "⦄")],
        lambda r: [("<", "⦃"), (">", "⦄")],
    ],

    CT.WolframExpression: [lambda r: r[0], lambda r: r[0]],
    CT.Expression: [
        lambda r: r[0],
        lambda r: r[0],
        lambda r: r[0],
        lambda r: [("l", "")] + r[0],
        lambda r: [("m", ""), ("<", "⟦")] + r[1] + [(">", "⟧")] + r[3],
        lambda r: [("d", "")] + r[0] + r[1],
        lambda r: [("f", ""), ("<", "«")] + r[1] +  [(">", "»")] + r[3],
        lambda r: r[0] + r[1],
        lambda r: r[0][:1] + r[2] + r[3] + r[4] + r[5] + r[0][1:],
        lambda r: r[0][:1] + r[2] + r[3] + r[4] + r[5] + r[0][1:],
        lambda r: r[0][:1] + r[2] + r[3] + r[4] + r[0][1:],
        lambda r: r[0][:1] + r[2] + r[3] + r[4] + r[0][1:],
        lambda r: r[0][:1] + r[2] + r[3] + r[0][1:],
        lambda r: r[0][:1] + r[2] + r[3] + r[0][1:],
        lambda r: r[0][:1] + r[2] + r[0][1:],
        lambda r: r[0][:1] + r[2] + r[0][1:],
        lambda r: r[0],
        lambda r: r[0][:1] + r[2] + r[3] + r[4] + r[5],
        lambda r: r[0][:1] + r[2] + r[3] + r[4] + r[5],
        lambda r: r[0][:1] + r[2] + r[3] + r[4],
        lambda r: r[0][:1] + r[2] + r[3] + r[4],
        lambda r: r[0][:1] + r[2] + r[3],
        lambda r: r[0][:1] + r[2] + r[3],
        lambda r: r[0][:1] + r[2],
        lambda r: r[0][:1] + r[2],
    ],
    CT.ExpressionOrEOF: [lambda r: r[0], lambda r: []],
    CT.Nilary: [
        (lambda i: lambda r: [("o", [
            "Ｓ", "Ｎ", "Ａ"
        ][i])])(i)
        for i in range(3)
    ] + [
        lambda r: [("o", "‽"), ("!", "e")]
    ] * 2 + [
        (lambda i: lambda r: [("o", [
            "ＫＡ", "ＫＭ", "ＫＶ", "ＫＫ", "ⅈ", "ⅉ", "ⅈ", "ⅉ"
        ][i])])(i)
        for i in range(8)
    ],
    CT.Unary: [
        (lambda i: lambda r: [("o", "±±Ｌ¬Ｉ‽‽ＶＶ⊟↧↥⌊⌊⌊⌈⌈⌈⌈℅℅℅℅⮌⮌≕≕″‴～↔↔\
ΣΠ⊕⊖⊗⊘₂₂"[i])])(i)
        for i in range(40)
    ] + [
        lambda r: [("o", "✂"), ("!", "e"), ("!", "e")],
        lambda r: [("o", "…")],
        lambda r: [("o", "…·")],
        lambda r: [("o", "ＵＶ")],
        lambda r: [("o", "ＵＶ")],
    ],
    CT.Binary: [
        (lambda i: (
            lambda r: [("o", "⁺⁺⁻⁻××∕∕÷÷﹪﹪⁼‹›＆｜"[i])]
        ))(i)
        for i in range(17)
    ] + [
        (lambda i: lambda r: [("o", [
            "…·", "…", "…", "…", "Ｘ", "Ｘ", "Ｘ", "§", "⊞Ｏ", "⪫", "⪪",
            "⌕Ａ"
        ][i])])(i)
        for i in range(12)
    ] + [
        (lambda i: lambda r: [("o", "⌕◧◨№➙⧴？⍘↨"[i])])(i)
        for i in range(9)
    ] + [
        lambda r: [("o", "✂"), ("!", "e"), ("!", "e"), ("!", "e")]
    ],
    CT.Infix: [
        (lambda i: (
            lambda r: lambda left, right: (
                [("o", "Ｘ⁺⁻×∕÷﹪⁼‹›＆｜≔"[i])] + left + right
            )
        ))(i)
        for i in range(12)
    ] + [
        lambda r: lambda left, right: (
            [("o", "≔")] + right + left
        )
    ],
    CT.Prefix: [
        (lambda i: (
            lambda r: lambda item: [("o", "⊖±～⊕⊗⊘"[i])] + item
        ))(i)
        for i in range(6)
    ],
    CT.Fix: [
        lambda r: r
    ],
    CT.FixOrEOF: [
        lambda r: r[0],
        lambda r: []
    ],
    CT.Ternary: [lambda r: [("o", "✂"), ("!", "e"), ("!", "e")]],
    CT.Quarternary: [lambda r: [("o", "✂")]],
    CT.LazyUnary: [],
    CT.LazyBinary: [
        (lambda i: lambda r: [("o", "∧∨∧∨"[i])])(i) for i in range(4)
    ],
    CT.LazyTernary: [lambda r: [("o", "⎇")]],
    CT.LazyQuarternary: [],
    CT.OtherOperator: [
        (lambda i: lambda r: [("o", [
            "ＫＤ", "Ｅ", "Ｅ", "⊙", "⊙", "⬤", "⬤", "⭆", "⭆", "Φ",
            "▷", "▷", "▷", "▷"
        ][i])] + r[2] + r[3])(i)
        for i in range(14)
    ] + [lambda r: [("o", "▷" )] + r[2] + [("!", "e")]] * 2,

    CT.Program: [lambda r: r[0] + r[1], lambda r: []],
    CT.NonEmptyProgram: [lambda r: r[0] + r[1], lambda r: r[0]],
    CT.Body: [
        lambda r: [("<", "«")] + r[1] + [(">", "»")],
        lambda r: r[0],
    ],
    CT.Command: [
        lambda r: [("$", "Ｓ")] + r[2],
        lambda r: [("$", "Ｎ")] + r[2],
        lambda r: [("$", "Ａ")] + r[2],
        lambda r: [("$", "Ｖ")] + r[2],
        lambda r: [("$", "Ｖ")] + r[2],
        lambda r: r[2] + r[4],
        lambda r: r[2],
        lambda r: r[2] + r[4],
        lambda r: r[2],
        lambda r: [("$", "Ｐ")] + r[2] + r[4],
        lambda r: [("$", "Ｐ")] + r[2],
        lambda r: [("$", "Ｇ")] + r[2] + r[4] + r[5],
        lambda r: [("$", "Ｇ")] + r[2] + r[4],
        lambda r: [("$", "ＧＨ")] + r[2] + r[4] + r[5],
        lambda r: [("$", "ＧＨ")] + r[2] + r[4],
        lambda r: [("$", "ＵＲ")] + r[2] + r[3],
        lambda r: [("$", "ＵＲ")] + r[2] + [("!", "e")] * 2,
        lambda r: [("$", "ＵＯ")] + r[2] + r[3] + r[4],
        lambda r: [("$", "ＵＯ")] + r[2] + r[3] + [("!", "e")] * 2,
        lambda r: [("$", "Ｂ")] + r[2] + r[3] + r[4],
        lambda r: [("$", "Ｂ")] + r[2] + r[3] + [("!", "e")] * 2,
        lambda r: [("$", "Ｍ")] + r[2],
        lambda r: [("$", "Ｍ")] + r[2] + r[3],
        lambda r: [("$", "Ｍ")] + r[2] + r[3],
        lambda r: [("$", "Ｍ")] + r[2] + r[3],
        lambda r: [("$", "↶")] + r[2],
        lambda r: [("$", "↶")],
        lambda r: [("$", "↷")] + r[2],
        lambda r: [("$", "↷")],
        lambda r: [("$", "Ｊ")] + r[2] + r[3],
        lambda r: [("$", "⟲Ｔ")] + r[2],
        lambda r: [("$", "⟲Ｔ")],
        lambda r: [("$", "‖Ｔ")] + r[2],
        lambda r: [("$", "‖Ｔ")] + r[2],
        lambda r: [("$", "‖Ｔ")],
        lambda r: [("$", "⟲Ｐ")] + r[2] + r[4],
        lambda r: [("$", "⟲Ｐ")] + r[2],
        lambda r: [("$", "⟲Ｐ")] + r[2],
        lambda r: [("$", "⟲Ｐ")],
        lambda r: [("$", "‖Ｍ")] + r[2],
        lambda r: [("$", "‖Ｍ")] + r[2],
        lambda r: [("$", "‖Ｍ")],
        lambda r: [("$", "⟲Ｃ")] + r[2] + r[4],
        lambda r: [("$", "⟲Ｃ")] + r[2],
        lambda r: [("$", "⟲Ｃ")] + r[2],
        lambda r: [("$", "⟲Ｃ")],
        lambda r: [("$", "‖Ｃ")] + r[2],
        lambda r: [("$", "‖Ｃ")] + r[2],
        lambda r: [("$", "‖Ｃ")],
        lambda r: [("$", "⟲ＯＯ")] + r[2] + r[4] + r[6],
        lambda r: [("$", "⟲ＯＯ")] + r[2] + r[4] + r[6],
        lambda r: [("$", "⟲ＯＯ")] + r[2] + r[4] + [("!", "e")] * 2,
        lambda r: [("$", "⟲ＯＯ")] + r[2] + r[4],
        lambda r: [("$", "⟲ＯＯ")] + r[2] + r[4],
        lambda r: [("$", "⟲ＯＯ")] + r[2] + [("!", "e")] * 2,
        lambda r: [("$", "⟲Ｏ")] + r[2] + r[4],
        lambda r: [("$", "⟲Ｏ")] + r[2],
        lambda r: [("$", "⟲Ｏ")] + r[2],
        lambda r: [("$", "⟲Ｏ")],
        lambda r: [("$", "⟲ＳＯ")] + r[2] + r[4] + r[6],
        lambda r: [("$", "⟲ＳＯ")] + r[2] + r[4] + r[6],
        lambda r: [("$", "⟲ＳＯ")] + r[2] + r[4] + [("!", "e")] * 2,
        lambda r: [("$", "⟲ＳＯ")] + r[2] + r[4],
        lambda r: [("$", "⟲ＳＯ")] + r[2] + r[4],
        lambda r: [("$", "⟲ＳＯ")] + r[2] + [("!", "e")] * 2,
        lambda r: [("$", "⟲Ｓ")] + r[2] + r[4],
        lambda r: [("$", "⟲Ｓ")] + r[2],
        lambda r: [("$", "⟲Ｓ")] + r[2],
        lambda r: [("$", "⟲Ｓ")],
        lambda r: [("$", "‖ＯＯ")] + r[2] + r[3] + r[4],
        lambda r: [("$", "‖ＯＯ")] + r[2] + r[4],
        lambda r: [("$", "‖ＯＯ")] + r[2],
        lambda r: [("$", "‖Ｏ")] + r[2],
        lambda r: [("$", "‖Ｏ")] + r[2],
        lambda r: [("$", "‖Ｏ")],
        lambda r: [("$", "‖ＢＯ")] + r[2] + r[3] + r[4],
        lambda r: [("$", "‖ＢＯ")] + r[2] + r[4],
        lambda r: [("$", "‖ＢＯ")] + r[2],
        lambda r: [("$", "‖Ｂ")] + r[2],
        lambda r: [("$", "‖Ｂ")] + r[2],
        lambda r: [("$", "‖Ｂ")],
        lambda r: [("$", "⟲")] + r[2],
        lambda r: [("$", "⟲")],
        lambda r: [("$", "‖")] + r[2],
        lambda r: [("$", "‖")],
        lambda r: [("$", "Ｃ")] + r[2] + r[3],
        lambda r: [("$", "Ｆ")] + r[2] + r[4],
        lambda r: [("$", "Ｗ")] + r[2] + r[4],
        lambda r: [("$", "¿")] + r[2] + r[4] + r[6],
        lambda r: [("$", "¿")] + r[2] + r[4],
        lambda r: [("$", "§≔")] + r[2] + r[3] + r[4],
        lambda r: [("$", "≔")] + r[2] + r[3],
        lambda r: [("$", "≔")] + r[2] + r[3],
        lambda r: [("$", "≔")] + r[2] + r[3],
        lambda r: [("$", "¤")] + r[2],
        lambda r: [("$", "ＵＢ")] + r[2],
        lambda r: [("$", "ＵＢ")] + r[2],
        lambda r: [("$", "Ｄ")],
        lambda r: [("$", "ＲＦ")] + r[2] + r[3] + r[5],
        lambda r: [("$", "ＲＷ")] + r[2] + r[3] + r[5],
        lambda r: [("$", "Ｒ")] + r[2],
        lambda r: [("$", "Ｒ")],
        lambda r: [("$", "ＵＴ")],
        lambda r: [("$", "Ｔ")] + r[2] + r[3],
        lambda r: [("$", "Ｔ")] + r[2] + [("!", "e")] * 2,
        lambda r: [("$", "⎚")],
        lambda r: [("$", "ＵＥ")] + r[2] + r[3],
        lambda r: [("$", "ＵＥ")] + r[2],
        lambda r: [("$", "⊞")] + r[2] + r[3],
        lambda r: [("$", "≡"), ("<", "«")] + r[2] + r[5] + r[8] + [(">", "»")],
        lambda r: [("$", "≡"), ("<", "«")] + r[2] + r[5] + [(">", "»")],
        # TODO: autoremove braces
        lambda r: [("$", "≡")] + r[2] + r[5] + r[8],
        lambda r: [("$", "≡")] + r[2] + r[5],
        lambda r: [("$", "ＵＭ")] + r[2] + r[3],
        lambda r: [("$", "▶")] + r[2] + r[3],
        lambda r: [("$", "▶")] + r[2] + r[3],
        lambda r: [("$", "▶")] + r[2] + r[3],
        lambda r: [("$", "▶")] + r[2] + r[3],
        lambda r: [("$", "≦")] + r[2] + r[4] + r[5],
        lambda r: [("$", "≧")] + r[2] + r[4] + r[5],
        lambda r: [("$", "≦")] + r[2] + r[4],
        lambda r: [("$", "ＵＸ")] + r[2],
        lambda r: [("$", "ＵＸ")] + r[2],
        lambda r: r[0] + r[2],
        lambda r: r[0],
    ]
}
