from charcoaltoken import CharcoalToken
from unicodegrammars import UnicodeGrammars
from compression import Compressed
from codepage import rCommand
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
        lambda result: result[0] + result[1],
        lambda result: result[0]
    ],
    CharcoalToken.PairExpressions: [
        lambda result: result[0] + result[1] + result[2],
        lambda result: result[0] + result[1]
    ],
    CharcoalToken.Cases: [
        lambda result: [result[1], result[3]] + result[4],
        lambda result: []
    ],

    CharcoalToken.List: [
        lambda result: "⟦" + result[1] + "⟧",
        lambda result: "⟦⟧"
    ],
    CharcoalToken.ArrowList: [
        lambda result: "⟦" + result[1] + "⟧",
        lambda result: "⟦⟧"
    ],
    CharcoalToken.Dictionary: [
        lambda result: "⦃" + result[1] + "⦄",
        lambda result: "⦃⦄"
    ],

    CharcoalToken.Expression: [
        lambda result: result[0] + result[1],
        lambda result: result[0] + result[1],
        lambda result: result[0] + result[1],
        lambda result: result[0] + result[1],
        lambda result: result[0] + result[1],
        lambda result: result[0] + result[1],
        lambda result: result[0] + result[2] + result[3] + result[4],
        lambda result: result[0] + result[2] + result[3] + result[4],
        lambda result: result[0] + result[2] + result[3],
        lambda result: result[0] + result[2] + result[3],
        lambda result: result[0] + result[2],
        lambda result: result[0] + result[2],
        lambda result: result[0]
    ],
    CharcoalToken.Nilary: [
        lambda result: "Ｓ",
        lambda result: "Ｎ",
        lambda result: "‽",
        lambda result: "ＫＡ",
        lambda result: "ＫＭ",
        lambda result: "ＫＶ",
        lambda result: "Ｋ"
    ],
    CharcoalToken.Unary: [
        lambda result: "⁻",
        lambda result: "Ｌ",
        lambda result: "¬",
        lambda result: "Ｉ",
        lambda result: "‽",
        lambda result: "Ｖ",
        lambda result: "Ｖ",
        lambda result: "⊟",
        lambda result: "↧",
        lambda result: "↥",
        lambda result: "⌊",
        lambda result: "⌈",
        lambda result: "℅",
        lambda result: "℅",
        lambda result: "℅",
        lambda result: "℅",
        lambda result: "⮌"
    ],
    CharcoalToken.Binary: [
        lambda result: "⁺",
        lambda result: "⁺",
        lambda result: "⁻",
        lambda result: "⁻",
        lambda result: "×",
        lambda result: "×",
        lambda result: "÷",
        lambda result: "﹪",
        lambda result: "⁼",
        lambda result: "‹",
        lambda result: "›",
        lambda result: "…·",
        lambda result: "…",
        lambda result: "…",
        lambda result: "…",
        lambda result: "Ｘ",
        lambda result: "Ｘ",
        lambda result: "Ｘ",
        lambda result: "§",
        lambda result: "⊞Ｏ",
        lambda result: "⪫",
        lambda result: "⪪",
        lambda result: "⌕Ａ",
        lambda result: "⌕",
        lambda result: "◧",
        lambda result: "◨",
        lambda result: "№"
    ],
    CharcoalToken.Ternary: [
    ],
    CharcoalToken.LazyUnary: [
    ],
    CharcoalToken.LazyBinary: [
        lambda result: "∧",
        lambda result: "∨",
        lambda result: "∧",
        lambda result: "∨"
    ],
    CharcoalToken.LazyTernary: [
        lambda result: "⎇"
    ],
    CharcoalToken.OtherOperator: [
        lambda result: "ＫＤ" + result[2] + result[3],
        lambda result: "Ｅ" + result[2] + result[3],
        lambda result: "Ｅ" + result[2] + result[3],
        lambda result: "ＵＰ" + result[2] + result[3]
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
        lambda result: "ＵＰ" + result[2] + result[3],
        lambda result: "Ｓ" + result[2],
        lambda result: "Ｎ" + result[2],
        lambda result: "Ｖ" + result[2],
        lambda result: "Ｖ" + result[2],
        lambda result: result[2] + result[4],
        lambda result: result[2],
        lambda result: "Ｐ" + result[2] + result[4],
        lambda result: "Ｐ" + result[2],
        lambda result: "Ｇ" + result[2] + result[4],
        lambda result: "Ｇ" + result[2] + result[4] + result[5],
        lambda result: "ＧＨ" + result[2] + result[4],
        lambda result: "ＧＨ" + result[2] + result[4] + result[5],
        lambda result: "ＵＲ" + result[2] + result[3],
        lambda result: "ＵＯ" + result[2] + result[3] + result[4],
        lambda result: "Ｂ" + result[2] + result[3] + result[4],
        lambda result: "Ｍ" + result[2],
        lambda result: "Ｍ" + result[2] + result[3],
        lambda result: "Ｍ" + result[2] + result[3],
        lambda result: "Ｍ" + result[2] + result[3],
        lambda result: "↶" + result[2],
        lambda result: "↶",
        lambda result: "↷" + result[2],
        lambda result: "↷",
        lambda result: "Ｊ" + result[2] + result[3],
        lambda result: "⟲Ｔ" + result[2],
        lambda result: "⟲Ｔ",
        lambda result: "‖Ｔ" + result[2],
        lambda result: "⟲Ｐ" + result[2] + result[4],
        lambda result: "⟲Ｐ" + result[2] + result[4],
        lambda result: "⟲Ｐ" + result[2],
        lambda result: "⟲Ｐ" + result[2],
        lambda result: "⟲Ｐ" + result[2],
        lambda result: "⟲Ｐ",
        lambda result: "‖Ｍ" + result[2],
        lambda result: "‖Ｍ" + result[2],
        lambda result: "⟲Ｃ" + result[2] + result[4],
        lambda result: "⟲Ｃ" + result[2] + result[4],
        lambda result: "⟲Ｃ" + result[2],
        lambda result: "⟲Ｃ" + result[2],
        lambda result: "⟲Ｃ" + result[2],
        lambda result: "⟲Ｃ",
        lambda result: "‖Ｃ" + result[2],
        lambda result: "‖Ｃ" + result[2],
        lambda result: "‖Ｏ" + result[2],
        lambda result: "‖Ｏ" + result[2],
        lambda result: "⟲" + result[2],
        lambda result: "⟲",
        lambda result: "‖" + result[2],
        lambda result: "Ｃ" + result[2] + result[3],
        lambda result: "Ｆ" + result[2] + result[4],
        lambda result: "Ｗ" + result[2] + result[4],
        lambda result: "¿" + result[2] + result[4] + result[5],
        lambda result: "¿" + result[2] + result[4],
        lambda result: "Ａ§" + result[2] + result[3] + result[4],
        lambda result: "Ａ" + result[2] + result[3],
        lambda result: "¤" + result[2],
        lambda result: "ＵＢ" + result[2],
        lambda result: "Ｄ",
        lambda result: "ＨＦ" + result[2] + result[3] + result[5],
        lambda result: "ＨＷ" + result[2] + result[3] + result[5],
        lambda result: "Ｈ" + result[2],
        lambda result: "Ｈ",
        lambda result: "ＵＴ",
        lambda result: "Ｔ" + result[2] + result[3],
        lambda result: "⎚",
        lambda result: "ＵＥ" + result[2] + result[3],
        lambda result: "ＵＥ" + result[2],
        lambda result: "⊞" + result[2] + result[3],
        lambda result: "≡" + result[2] + result[5] + result[8],
        lambda result: "≡" + result[2] + result[5],
        lambda result: "ＵＭ" + result[2] + result[3]
    ]
}

