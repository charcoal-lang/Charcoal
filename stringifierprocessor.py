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
        lambda result: result[0] + result[1] + result[2],
        lambda result: "+" + result[1] + result[2],
        lambda result: "X" + result[1] + result[2],
        lambda result: "*" + result[1] + result[2],
        lambda result: "|" + result[1] + result[2],
        lambda result: "-" + result[1] + result[2],
        lambda result: "\\" + result[1] + result[2],
        lambda result: "/" + result[1] + result[2],
        lambda result: "<" + result[1] + result[2],
        lambda result: ">" + result[1] + result[2],
        lambda result: "^" + result[1] + result[2],
        lambda result: "K" + result[1] + result[2],
        lambda result: "L" + result[1] + result[2],
        lambda result: "T" + result[1] + result[2],
        lambda result: "V" + result[1] + result[2],
        lambda result: "Y" + result[1] + result[2],
        lambda result: "7" + result[1] + result[2],
        lambda result: "¬" + result[1] + result[2],
        lambda result: "⟦" + result[1] + "⟧",
        lambda result: result[0]
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
        lambda result: [Compressed(
            rCommand.sub(r"´\1", result[0])
                .replace("\n", "¶")
                .replace("\r", "⸿")
        )]
    ],
    CharcoalToken.Number: [
        lambda result: ["".join(
            ("·" if n == "." else SuperscriptToNormal[int(n)])
            for n in str(result[0])
        )]
    ],
    CharcoalToken.Name: [
        lambda result: "αβγδεζηθικλμνξπρσςτυφχψω"[
            "abgdezhqiklmnxprsvtufcyw".index(result[0])
        ]
    ],
    CharcoalToken.Span: [
        lambda result: result[0] + "；" + result[2] + "；" + result[4],
        lambda result: result[0] + "；；" + result[3],
        lambda result: result[0] + "；" + result[2],
        lambda result: result[0] + "；",
        lambda result: "；" + result[1] + "；" + result[3],
        lambda result: "；" + result[1],
        lambda result: "；；" + result[2],
        lambda result: "；；"
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
    CharcoalToken.WolframExpressions: [
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
    CharcoalToken.WolframList: [
        lambda result: "⟦" + result[1] + "⟧",
        lambda result: "⟦⟧"
    ],
    CharcoalToken.Dictionary: [
        lambda result: "⦃" + result[1] + "⦄",
        lambda result: "⦃⦄"
    ],

    CharcoalToken.WolframExpression: [
        lambda result: result[0] + result[1],
        lambda result: result[0],
    ],
    CharcoalToken.Expression: [
        lambda result: result[0] + result[1],
        lambda result: result[0] + result[1],
        lambda result: result[0] + result[1],
        lambda result: result[0] + result[1],
        lambda result: result[0] + result[1],
        lambda result: "«" + result[1] + "»" + result[3],
        lambda result: result[0] + result[1],
        lambda result: (
            result[0] + result[2] + result[3] + result[4] + result[5] +
            result[6]
        ),
        lambda result: (
            result[0] + result[2] + result[3] + result[4] + result[5] +
            result[6]
        ),
        lambda result: (
            result[0] + result[2] + result[3] + result[4] + result[6]
        ),
        lambda result: (
            result[0] + result[2] + result[3] + result[4] + result[6]
        ),
        lambda result: result[0] + result[2] + result[3] + result[5],
        lambda result: result[0] + result[2] + result[3] + result[5],
        lambda result: result[0] + result[2] + result[4],
        lambda result: result[0] + result[2] + result[4],
        lambda result: result[0] + result[3]
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
        lambda result: "±",
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
        lambda result: "⮌",
        lambda result: "≕",
        lambda result: "″",
        lambda result: "‴",
        lambda result: "✂",
        lambda result: "…·",
        lambda result: "…",
        lambda result: "～",
        lambda result: "～"
    ],
    CharcoalToken.Binary: [
        lambda result: "Ｘ",
        lambda result: "⁺",
        lambda result: "⁺",
        lambda result: "⁺",
        lambda result: "⁻",
        lambda result: "⁻",
        lambda result: "⁻",
        lambda result: "×",
        lambda result: "×",
        lambda result: "×",
        lambda result: "÷",
        lambda result: "∕",
        lambda result: "∕",
        lambda result: "÷",
        lambda result: "÷",
        lambda result: "﹪",
        lambda result: "﹪",
        lambda result: "⁼",
        lambda result: "⁼",
        lambda result: "‹",
        lambda result: "‹",
        lambda result: "›",
        lambda result: "›",
        lambda result: "＆",
        lambda result: "＆",
        lambda result: "｜",
        lambda result: "｜",
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
        lambda result: "№",
        lambda result: "➙",
        lambda result: "⧴",
        lambda result: "？",
        lambda result: "✂"
    ],
    CharcoalToken.Ternary: [
        lambda result: "✂"
    ],
    CharcoalToken.Quarternary: [
        lambda result: "✂"
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
    CharcoalToken.LazyQuarternary: [
    ],
    CharcoalToken.OtherOperator: [
        lambda result: "ＫＤ" + result[2] + result[3],
        lambda result: "Ｅ" + result[2] + result[3],
        lambda result: "Ｅ" + result[2] + result[3],
        lambda result: "ＵＰ" + result[2] + result[3],
        lambda result: "ＵＰ" + result[2],
        lambda result: "▷" + result[2] + result[3],
        lambda result: "▷" + result[2] + result[3]
    ],

    CharcoalToken.Program: [
        lambda result: result[0] + ("¦" if result[2] else "") + result[3],
        lambda result: ""
    ],
    CharcoalToken.Body: [
        lambda result: "«" + result[1] + "»",
        lambda result: result[0]
    ],
    CharcoalToken.Command: [
        lambda result: "ＵＰ" + result[2] + result[3],
        lambda result: "ＵＰ" + result[2],
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
        lambda result: "ＵＲ" + result[2] + "¦¦",
        lambda result: "ＵＯ" + result[2] + result[3] + result[4],
        lambda result: "ＵＯ" + result[2] + result[3] + "¦¦",
        lambda result: "Ｂ" + result[2] + result[3] + result[4],
        lambda result: "Ｂ" + result[2] + result[3] + "¦¦",
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
        lambda result: "‖Ｔ" + result[2],
        lambda result: "‖Ｔ",
        lambda result: "⟲Ｐ" + result[2] + result[4],
        lambda result: "⟲Ｐ" + result[2],
        lambda result: "⟲Ｐ" + result[2],
        lambda result: "⟲Ｐ",
        lambda result: "‖Ｍ" + result[2],
        lambda result: "‖Ｍ" + result[2],
        lambda result: "‖Ｍ",
        lambda result: "⟲Ｃ" + result[2] + result[4],
        lambda result: "⟲Ｃ" + result[2],
        lambda result: "⟲Ｃ" + result[2],
        lambda result: "⟲Ｃ",
        lambda result: "‖Ｃ" + result[2],
        lambda result: "‖Ｃ" + result[2],
        lambda result: "‖Ｃ",
        lambda result: "⟲ＯＯ" + result[2:-1],
        lambda result: "⟲ＯＯ" + result[2:-1],
        lambda result: "⟲ＯＯ" + result[2] + result[4] + result[5],
        lambda result: "⟲ＯＯ" + result[2] + result[3],
        lambda result: "⟲ＯＯ" + result[2],
        lambda result: "⟲Ｏ" + result[2] +  result[4],
        lambda result: "⟲Ｏ" + result[2],
        lambda result: "⟲Ｏ" + result[2],
        lambda result: "⟲Ｏ",
        lambda result: "⟲ＳＯ" + result[2:-1],
        lambda result: "⟲ＳＯ" + result[2:-1],
        lambda result: "⟲ＳＯ" + result[2] + result[4] + result[5],
        lambda result: "⟲ＳＯ" + result[2] + result[3],
        lambda result: "⟲ＳＯ" + result[2],
        lambda result: "⟲Ｓ" + result[2] + result[4],
        lambda result: "⟲Ｓ" + result[2],
        lambda result: "⟲Ｓ" + result[2],
        lambda result: "⟲Ｓ",
        lambda result: "‖ＯＯ" + result[2] + result[3] + result[4],
        lambda result: "‖ＯＯ" + result[2] + result[4],
        lambda result: "‖ＯＯ" + result[2],
        lambda result: "‖Ｏ" + result[2],
        lambda result: "‖Ｏ" + result[2],
        lambda result: "‖Ｏ",
        lambda result: "‖ＢＯ" + result[2] + result[3] + result[4],
        lambda result: "‖ＢＯ" + result[2] + result[4],
        lambda result: "‖ＢＯ" + result[2],
        lambda result: "‖Ｂ" + result[2],
        lambda result: "‖Ｂ" + result[2],
        lambda result: "‖Ｂ",
        lambda result: "⟲" + result[2],
        lambda result: "⟲",
        lambda result: "‖" + result[2],
        lambda result: "‖",
        lambda result: "Ｃ" + result[2] + result[3],
        lambda result: "Ｆ" + result[2] + result[4],
        lambda result: "Ｗ" + result[2] + result[4],
        lambda result: "¿" + result[2] + result[4] + result[6],
        lambda result: "¿" + result[2] + result[4],
        lambda result: "Ａ§" + result[2] + result[3] + result[4],
        lambda result: "Ａ" + result[2] + result[3],
        lambda result: "Ａ" + result[2] + result[3],
        lambda result: "¤" + result[2],
        lambda result: "ＵＢ" + result[2],
        lambda result: "Ｄ",
        lambda result: "ＲＦ" + result[2] + result[3] + result[5],
        lambda result: "ＲＷ" + result[2] + result[3] + result[5],
        lambda result: "Ｒ" + result[2],
        lambda result: "Ｒ",
        lambda result: "ＵＴ",
        lambda result: "Ｔ" + result[2] + result[3],
        lambda result: "Ｔ" + result[2] + "¦¦",
        lambda result: "⎚",
        lambda result: "ＵＥ" + result[2] + result[3],
        lambda result: "ＵＥ" + result[2],
        lambda result: "⊞" + result[2] + result[3],
        lambda result: "≡" + result[2] + result[5] + result[8],
        lambda result: "≡" + result[2] + result[5],
        lambda result: "ＵＭ" + result[2] + result[3],
        lambda result: "▶" + result[2] + result[3],
        lambda result: "≔" + result[2] + result[3]
    ]
}

