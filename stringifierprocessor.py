from charcoaltoken import CharcoalToken as CT
from unicodegrammars import UnicodeGrammars
from compression import Compressed
from codepage import rCommand
import re

def string(s):
    if s == "":
        return "ω"
    if s == "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        return "α"
    if s == "abcdefghijklmnopqrstuvwxyz":
        return "β"
    if s == " !\"#$%&'()*+,-./0123456789:;<=>?@\
ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~":
        return "γ"
    s = Compressed(s.replace("\n", "¶").replace("\r", "⸿"), True)
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
        (lambda i: lambda r: [("a", ("↖↗↘↙←↑→↓" * 2)[i])])(i)
        for i in range(16)
    ] + [
        lambda r: [("$", "✳")] + r[2],
    ],
    CT.Multidirectional: [
        lambda r: r[0] + r[2]
    ] + [
        (lambda i: lambda r: [("a", "+X**||--\\/<>^KLTVY7¬"[i])])(i)
        for i in range(20)
    ] + [
        lambda r: [("<", "⟦")] + r[1] + [(">", "⟧")],
        lambda r: [("$", "✳✳" )] + r[2],
        lambda r: []
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
    CT.Expressions: [lambda r: r[0] + r[1], lambda r: r[0]],
    CT.WolframExpressions: [lambda r: r[0] + r[1], lambda r: r[0]],
    CT.PairExpressions: [lambda r: r[0] + r[1] + r[2], lambda r: r[0] + r[1]],
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
        lambda r: r[0] + r[2] + r[3] + r[4] + r[5],
        lambda r: r[0] + r[2] + r[3] + r[4] + r[5],
        lambda r: r[0] + r[2] + r[3] + r[4],
        lambda r: r[0] + r[2] + r[3] + r[4],
        lambda r: r[0] + r[2] + r[3],
        lambda r: r[0] + r[2] + r[3],
        lambda r: r[0] + r[2],
        lambda r: r[0] + r[2],
        lambda r: r[0],
        lambda r: r[0] + r[2] + r[3] + r[4] + r[5],
        lambda r: r[0] + r[2] + r[3] + r[4] + r[5],
        lambda r: r[0] + r[2] + r[3] + r[4],
        lambda r: r[0] + r[2] + r[3] + r[4],
        lambda r: r[0] + r[2] + r[3],
        lambda r: r[0] + r[2] + r[3],
        lambda r: r[0] + r[2],
        lambda r: r[0] + r[2],
    ],
    CT.ExpressionOrEOF: [lambda r: r[0], lambda r: []],
    CT.Nilary: [
        (lambda i: lambda r: [("$", [
            "Ｓ", "Ｎ", "Ａ", "‽", "‽", "ＫＡ", "ＫＭ", "ＫＶ", "ＫＫ",
            "ⅈ", "ⅉ", "ⅈ", "ⅉ"
        ][i])])(i)
        for i in range(13)
    ],
    CT.Unary: [
        (lambda i: lambda r: [("$", "±±Ｌ¬Ｉ‽‽ＶＶ⊟↧↥⌊⌊⌊⌈⌈⌈⌈℅℅℅℅⮌⮌≕≕″‴～～↔↔\
ΣΠ⊕⊕⊖⊖⊗⊗⊘⊘₂₂"[i])])(i)
        for i in range(45)
    ] + [
        lambda r: [("$", "✂"), ("!", "e")],
        lambda r: [("$", "…")],
        lambda r: [("$", "…·")],
        lambda r: [("$", "ＵＶ")],
        lambda r: [("$", "ＵＶ")],
    ],
    CT.Binary: [
        (lambda i: (
            lambda r: [("$", "Ｘ⁺⁺⁺⁻⁻⁻×××÷∕∕∕÷÷﹪﹪⁼⁼‹‹››＆＆｜｜"[i])]
        ))(i)
        for i in range(28)
    ] + [
        (lambda i: lambda r: [("$", [
            "…·", "…", "…", "…", "Ｘ", "Ｘ", "Ｘ", "§", "⊞Ｏ", "⪫", "⪪",
            "⌕Ａ"
        ][i])])(i)
        for i in range(12)
    ] + [
        (lambda i: lambda r: [("$", "⌕◧◨№➙⧴？⍘↨"[i])])(i)
        for i in range(9)
    ] + [
        lambda r: [("$", "✂"), ("!", "e")]
    ],
    CT.Ternary: [lambda r: [("$", "✂"), ("!", "e")]],
    CT.Quarternary: [lambda r: [("$", "✂"), ("!", "e")]],
    CT.LazyUnary: [],
    CT.LazyBinary: [
        (lambda i: lambda r: ("$", "∧∨∧∨"[i]))(i) for i in range(4)
    ],
    CT.LazyTernary: [lambda r: [("$", "⎇")]],
    CT.LazyQuarternary: [],
    CT.OtherOperator: [
        (lambda i: lambda r: [("$", [
            "ＫＤ", "Ｅ", "Ｅ", "⊙", "⊙", "⬤", "⬤", "⭆", "⭆", "Φ",
            "▷", "▷", "▷", "▷"
        ][i])] + r[2] + r[3])(i)
        for i in range(14)
    ] + [lambda r: [("$", "▷" )] + r[2] + [("!", "e")]] * 2,

    CT.Program: [lambda r: r[0] + r[1], lambda r: []],
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
        lambda r: [("$", "Ｇ")] + r[2] + r[4],
        lambda r: [("$", "Ｇ")] + r[2] + r[4] + r[5],
        lambda r: [("$", "ＧＨ")] + r[2] + r[4],
        lambda r: [("$", "ＧＨ")] + r[2] + r[4] + r[5],
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
        lambda r: [("$", "⟲ＯＯ")] + r[2] + r[4] + r[6] + r[7],
        lambda r: [("$", "⟲ＯＯ")] + r[2] + r[4] + r[6] + [("!", "e")],
        lambda r: [("$", "⟲ＯＯ")] + r[2] + r[4] + r[5],
        lambda r: [("$", "⟲ＯＯ")] + r[2] + r[4] + [("!", "e")],
        lambda r: [("$", "⟲ＯＯ")] + r[2] + r[3],
        lambda r: [("$", "⟲ＯＯ")] + r[2],
        lambda r: [("$", "⟲Ｏ")] + r[2] + r[4],
        lambda r: [("$", "⟲Ｏ")] + r[2],
        lambda r: [("$", "⟲Ｏ")] + r[2],
        lambda r: [("$", "⟲Ｏ")],
        lambda r: [("$", "⟲ＳＯ")] + r[2] + r[4] + r[6] + r[7],
        lambda r: [("$", "⟲ＳＯ")] + r[2] + r[4] + r[6] + [("!", "e")],
        lambda r: [("$", "⟲ＳＯ")] + r[2] + r[4] + r[5],
        lambda r: [("$", "⟲ＳＯ")] + r[2] + r[4] + [("!", "e")],
        lambda r: [("$", "⟲ＳＯ")] + r[2] + r[3],
        lambda r: [("$", "⟲ＳＯ")] + r[2],
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
