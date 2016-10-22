from charcoaltoken import CharcoalToken
from codepage import UnicodeCommands
from unicodegrammars import UnicodeGrammars
from compression import Compressed
import re

rCommand = re.compile("([%s])" % UnicodeCommands)

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
        lambda result: [Compressed(re.sub(
            "\n",
            "¶",
            rCommand.sub(
                r"´\1",
                result[0]
            )
        ))]
    ],
    CharcoalToken.Number: [
        lambda result: ["".join(
            SuperscriptToNormal[int(n)] for n in str(result[0])
        )]
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
        lambda result: "…",
        lambda result: "Ｘ",
        lambda result: "§"
    ],

    CharcoalToken.Program: [
        lambda result: result[0] + result[2],
        lambda result: ""
    ],
    CharcoalToken.Body: [
        lambda result: "«" + result[1] + "»",
        lambda result: result[0]
    ],
    CharcoalToken.Command: [
        lambda result: "Ｓ" + result[2],
        lambda result: "Ｎ" + result[2],
        lambda result: "Ｖ" + result[2],
        lambda result: result[2] + result[4],
        lambda result: result[2],
        lambda result: "Ｐ" + result[2] + result[4],
        lambda result: "Ｐ" + result[2],
        lambda result: "Ｇ" + result[2] + result[4],
        lambda result: "Ｇ" + result[2] + result[4] + result[5],
        lambda result: "ＧＨ" + result[2] + result[4],
        lambda result: "ＧＨ" + result[2] + result[4] + result[5],
        lambda result: "ＢＲ" + result[2] + result[3],
        lambda result: "Ｂ" + result[2] + result[3] + result[4],
        lambda result: "Ｍ" + result[2],
        lambda result: "Ｍ" + result[2] + result[3],
        lambda result: "↶" + result[2],
        lambda result: "↶",
        lambda result: "↷" + result[2],
        lambda result: "↷",
        lambda result: "Ｊ" + result[2] + result[3],
        lambda result: "⟲Ｔ" + result[2],
        lambda result: "‖Ｔ" + result[2],
        lambda result: "‖Ｔ" + result[2],
        lambda result: "‖Ｍ" + result[2],
        lambda result: "‖Ｍ" + result[2],
        lambda result: "⟲Ｃ" + result[2],
        lambda result: "‖Ｃ" + result[2],
        lambda result: "‖Ｃ" + result[2],
        lambda result: "⟲Ｏ" + result[2],
        lambda result: "‖Ｏ" + result[2],
        lambda result: "‖Ｏ" + result[2],
        lambda result: "⟲" + result[2],
        lambda result: "‖" + result[2],
        lambda result: "Ｃ" + result[2] + result[3],
        lambda result: "Ｆ" + result[2] + result[4],
        lambda result: "Ｗ" + result[2] + result[4],
        lambda result: "¿" + result[2] + result[4] + result[5],
        lambda result: "¿" + result[2] + result[4],
        lambda result: "Ａ" + result[2] + result[3],
        lambda result: "¤" + result[2],
        lambda result: "ＵＢ" + result[2],
        lambda result: "Ｄ",
        lambda result: "ＨＦ" + result[2] + result[4] + result[5],
        lambda result: "ＨＷ" + result[2] + result[4] + result[5],
        lambda result: "Ｈ" + result[2],
        lambda result: "Ｈ",
        lambda result: "Ｔ" + result[2] + result[3],
        lambda result: "⎚",
        lambda result: "Ｅ" + result[2] + result[3],
        lambda result: "Ｅ" + result[2]
    ]
}
