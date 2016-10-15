from charcoaltoken import CharcoalToken
from unicodegrammars import UnicodeGrammars
import re

SuperscriptToNormal = "⁰¹²³⁴⁵⁶⁷⁸⁹"

StringifierProcessor = {
    CharcoalToken.Arrow: [
        lambda result: "↖",
        lambda result: "↗",
        lambda result: "↘",
        lambda result: "↙",
        lambda result: "←",
        lambda result: "↑",
        lambda result: "→",
        lambda result: "↓"
    ],
    CharcoalToken.Multidirectional: [
        lambda result: result[0],
        lambda result: "+" + result[2],
        lambda result: "X" + result[2],
        lambda result: "*" + result[2],
        lambda result: "|" + result[2],
        lambda result: "-" + result[2],
        lambda result: "\\" + result[2],
        lambda result: "/" + result[2],
        lambda result: "<" + result[2],
        lambda result: ">" + result[2],
        lambda result: "^" + result[2],
        lambda result: "K" + result[2],
        lambda result: "L" + result[2],
        lambda result: "T" + result[2],
        lambda result: "V" + result[2],
        lambda result: "Y" + result[2],
        lambda result: "7" + result[2],
        lambda result: "¬" + result[2],
        lambda result: ""
    ],
    CharcoalToken.Side: [
        lambda result: result[0] + result[2],
        lambda result: result[0]
    ],
    CharcoalToken.Separator: [
        lambda result: "¦",
        lambda result: "¦",
        lambda result: ""
    ],
    CharcoalToken.String: [
        lambda result: [re.sub(
            r"\n",
            r"¶",
            re.sub(
                r"""\
([ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ\
⁰¹²³⁴⁵⁶⁷⁸⁹\
αβγδεζηθικλμνξπρσςτυφχψω\
⟦⟧⦃⦄«»⁺⁻×÷﹪∧∨¬⁼‹›←↑→↓↖↗↘↙↶↷⟲¿‽‖´·¤¦¶])""",
                r"´\1",
                result[0]
            )
        )]
    ],
    CharcoalToken.Number: [
        lambda result: "".join(
            SuperscriptToNormal[int(n)] for n in str(result[0])
        )
    ],
    CharcoalToken.Name: [
        lambda result: "αβγδεζηθικλμνξπρσςτυφχψω"[
            "abgdezhciklmnxprstufko".index(result[0])
        ]
    ],

    CharcoalToken.Arrows: [
        lambda result: result[0] + result[2],
        lambda result: result[0]
    ],
    CharcoalToken.Sides: [
        lambda result: result[0] + result[2],
        lambda result: result[0]
    ],
    CharcoalToken.Expressions: [
        lambda result: result[0] + result[2],
        lambda result: result[0]
    ],

    CharcoalToken.List: [
        lambda result: "⟦" + result[1] + "⟧"
    ],
    CharcoalToken.ArrowList: [
        lambda result: "⟦" + result[1] + "⟧"
    ],

    CharcoalToken.Expression: [
        lambda result: result[0] + result[1],
        lambda result: result[0] + result[1],
        lambda result: result[0] + result[1],
        lambda result: result[0] + result[1],
        lambda result: result[0] + result[2] + result[3],
        lambda result: result[0] + result[2],
        lambda result: result[0]
    ],
    CharcoalToken.Niladic: [
        lambda result: "Ｓ",
        lambda result: "Ｎ",
        lambda result: "‽"
    ],
    CharcoalToken.Monadic: [
        lambda result: "⁻",
        lambda result: "Ｌ",
        lambda result: "¬",
        lambda result: "Ｉ",
        lambda result: "‽",
        lambda result: "Ｖ"
    ],
    CharcoalToken.Dyadic: [
        lambda result: "⁺",
        lambda result: "⁻",
        lambda result: "×",
        lambda result: "÷",
        lambda result: "﹪",
        lambda result: "⁼",
        lambda result: "‹",
        lambda result: "›",
        lambda result: "∧",
        lambda result: "∨",
        lambda result: "…"
    ],

    CharcoalToken.Program: [
        lambda result: result[0] + result[2],
        lambda result: ""
    ],
    CharcoalToken.Command: [
        lambda result: result[0]
    ] * len(UnicodeGrammars[CharcoalToken.Command]),
    CharcoalToken.Body: [
        lambda result: "«" + result[1] + "»",
        lambda result: result[0]
    ],
    CharcoalToken.Print: [
        lambda result: result[2] + result[4],
        lambda result: result[2]
    ],
    CharcoalToken.Multiprint: [
        lambda result: "Ｐ" + result[2] + result[4],
        lambda result: "Ｐ" + result[2]
    ],
    CharcoalToken.Rectangle: [
        lambda result: "ＢＲ" + result[2] + result[3]
    ],
    CharcoalToken.Box: [
        lambda result: "Ｂ" + result[2] + result[3] + result[4]
    ],
    CharcoalToken.Polygon: [
        lambda result: "Ｇ" + result[2] + result[4],
        lambda result: "Ｇ" + result[2] + result[4] + result[5],
    ],
    CharcoalToken.Move: [
        lambda result: "Ｍ" + result[2],
        lambda result: "Ｍ" + result[2] + result[3]
    ],
    CharcoalToken.Pivot: [
        lambda result: "↶" + result[2],
        lambda result: "↶",
        lambda result: "↷" + result[2],
        lambda result: "↷"
    ],
    CharcoalToken.Jump: [
        lambda result: "Ｊ" + result[2] + result[3]
    ],
    CharcoalToken.RotateCopy: [
        lambda result: "⟲Ｃ" + result[2],
        lambda result: "⟲Ｃ" + result[2]
    ],
    CharcoalToken.ReflectCopy: [
        lambda result: "‖Ｃ" + result[2],
        lambda result: "‖Ｃ" + result[2]
    ],
    CharcoalToken.RotateOverlap: [
        lambda result: "⟲Ｏ" + result[2],
        lambda result: "⟲Ｏ" + result[2]
    ],
    CharcoalToken.ReflectOverlap: [
        lambda result: "‖Ｏ" + result[2],
        lambda result: "‖Ｏ" + result[2]
    ],
    CharcoalToken.Rotate: [
        lambda result: "⟲" + result[2]
    ],
    CharcoalToken.Reflect: [
        lambda result: "‖" + result[2]
    ],
    CharcoalToken.Copy: [
        lambda result: "Ｃ" + result[2] + result[3]
    ],
    CharcoalToken.For: [
        lambda result: "Ｆ" + result[2] + result[4]
    ],
    CharcoalToken.While: [
        lambda result: "Ｗ" + result[2] + result[4]
    ],
    CharcoalToken.If: [
        lambda result: "¿" + result[2] + result[4] + result[5],
        lambda result: "¿" + result[2] + result[4]
    ],
    CharcoalToken.Assign: [
        lambda result: "Ａ" + result[2] + result[3]
    ],
    CharcoalToken.Fill: [
        lambda result: "¤" + result[2]
    ],
    CharcoalToken.SetBackground: [
        lambda result: "ＵＢ" + result[2]
    ],
    CharcoalToken.Dump: [
        lambda result: "Ｄ"
    ],
    CharcoalToken.RefreshFor: [
        lambda result: "ＨＦ" + result[2] + result[4] + result[5]
    ],
    CharcoalToken.RefreshWhile: [
        lambda result: "ＨＷ" + result[2] + result[4] + result[5]
    ],
    CharcoalToken.Refresh: [
        lambda result: "Ｈ" + result[2],
        lambda result: "Ｈ"
    ],
    CharcoalToken.Evaluate: [
        lambda result: "Ｖ" + result[2]
    ],
    CharcoalToken.InputString: [
        lambda result: "Ｓ" + result[2]
    ],
    CharcoalToken.InputNumber: [
        lambda result: "Ｎ" + result[2]
    ]
}
