'use strict';

var rCommand = new RegExp('([%s])' % UnicodeCommands),
    SuperscriptToNormal = '⁰¹²³⁴⁵⁶⁷⁸⁹',
    StringifierProcessor = new Array(CharcoalToken.MAXIMUM + 1);

StringifierProcessor[CharcoalToken.Arrow] = [
    function (result) { return '↖'; },
    function (result) { return '↗'; },
    function (result) { return '↘'; },
    function (result) { return '↙'; },
    function (result) { return '←'; },
    function (result) { return '↑'; },
    function (result) { return '→'; },
    function (result) { return '↓'; }
];

StringifierProcessor[CharcoalToken.Multidirectional] = [
    function (result) { return result[0]; },
    function (result) { return '+' + result[2]; },
    function (result) { return 'X' + result[2]; },
    function (result) { return '*' + result[2]; },
    function (result) { return '|' + result[2]; },
    function (result) { return '-' + result[2]; },
    function (result) { return '\\' + result[2]; },
    function (result) { return '/' + result[2]; },
    function (result) { return '<' + result[2]; },
    function (result) { return '>' + result[2]; },
    function (result) { return '^' + result[2]; },
    function (result) { return 'K' + result[2]; },
    function (result) { return 'L' + result[2]; },
    function (result) { return 'T' + result[2]; },
    function (result) { return 'V' + result[2]; },
    function (result) { return 'Y' + result[2]; },
    function (result) { return '7' + result[2]; },
    function (result) { return '¬' + result[2]; },
    function (result) { return ''; }
];

StringifierProcessor[CharcoalToken.Side] = [
    function (result) { return result[0] + result[2]; },
    function (result) { return result[0]; }
];

StringifierProcessor[CharcoalToken.Separator] = [
    function (result) { return '¦'; },
    function (result) { return '¦'; },
    function (result) { return ''; }
];

StringifierProcessor[CharcoalToken.String] = [
    function (result) { return [Compressed(re.sub(; }
        '\n',
        '¶',
        rCommand.sub(
            r'´\1',
            result[0]
        )
    ))]
];

StringifierProcessor[CharcoalToken.Number] = [
    function (result) { return result[0].toString().map(function (digit) {
        return SuperscriptToNormal[digit];
    }).join('');
];

StringifierProcessor[CharcoalToken.Name] = [
    function (result) {
        return 'αβγδεζηθικλμνξπρσςτυφχψω'['abgdezhciklmnxprstufko'.indexOf(result[0])];
    }
];

StringifierProcessor[CharcoalToken.Arrows] = [
    function (result) { return result[0] + result[2]; },
    function (result) { return result[0]; }
];

StringifierProcessor[CharcoalToken.Sides] = [
    function (result) { return result[0] + result[2]; },
    function (result) { return result[0]; }
];

StringifierProcessor[CharcoalToken.Expressions] = [
    function (result) { return result[0] + result[2]; },
    function (result) { return result[0]; }
];

StringifierProcessor[CharcoalToken.PairExpressions] = [
    function (result) { return result[0] + result[1] + result[2]; },
    function (result) { return result[0] + result[1]; }
];

StringifierProcessor[CharcoalToken.List] = [
    function (result) { return '⟦' + result[1] + '⟧'; },
    function (result) { return '⟦⟧'; }
];

StringifierProcessor[CharcoalToken.ArrowList] = [
    function (result) { return '⟦' + result[1] + '⟧'; },
    function (result) { return '⟦⟧'; }
];

StringifierProcessor[CharcoalToken.Dictionary] = [
    function (result) { return '⦃' + result[1] + '⦄'; },
    function (result) { return '⦃⦄'; }
];

StringifierProcessor[CharcoalToken.Expression] = [
    function (result) { return result[0] + result[1]; },
    function (result) { return result[0] + result[1]; },
    function (result) { return result[0] + result[1]; },
    function (result) { return result[0] + result[1]; },
    function (result) { return result[0] + result[1]; },
    function (result) { return result[0] + result[1]; },
    function (result) { return result[0] + result[2] + result[3] + result[4]; },
    function (result) { return result[0] + result[2] + result[3] + result[4]; },
    function (result) { return result[0] + result[2] + result[3]; },
    function (result) { return result[0] + result[2] + result[3]; },
    function (result) { return result[0] + result[2]; },
    function (result) { return result[0] + result[2]; },
    function (result) { return result[0]; }
];

StringifierProcessor[CharcoalToken.Nilary] = [
    function (result) { return 'Ｓ'; },
    function (result) { return 'Ｎ'; },
    function (result) { return '‽'; },
    function (result) { return 'ＫＡ'; },
    function (result) { return 'Ｋ'; }
];

StringifierProcessor[CharcoalToken.Unary] = [
    function (result) { return '⁻'; },
    function (result) { return 'Ｌ'; },
    function (result) { return '¬'; },
    function (result) { return 'Ｉ'; },
    function (result) { return '‽'; },
    function (result) { return 'Ｖ'; },
    function (result) { return '⊟'; },
    function (result) { return '↧'; },
    function (result) { return '↥'; },
    function (result) { return '⌊'; },
    function (result) { return '⌈'; },
    function (result) { return '℅'; },
    function (result) { return '℅'; }
];

StringifierProcessor[CharcoalToken.Binary] = [
    function (result) { return '⁺'; },
    function (result) { return '⁻'; },
    function (result) { return '×'; },
    function (result) { return '÷'; },
    function (result) { return '﹪'; },
    function (result) { return '⁼'; },
    function (result) { return '‹'; },
    function (result) { return '›'; },
    function (result) { return '…·'; },
    function (result) { return '…'; },
    function (result) { return '…'; },
    function (result) { return 'Ｘ'; },
    function (result) { return '§'; },
    function (result) { return '⊞'; },
    function (result) { return '⪫'; },
    function (result) { return '⪪'; },
    function (result) { return '⌕Ａ'; },
    function (result) { return '⌕'; },
    function (result) { return '◧'; },
    function (result) { return '◨'; }
];

StringifierProcessor[CharcoalToken.Ternary] = [
];

StringifierProcessor[CharcoalToken.LazyUnary] = [
];

StringifierProcessor[CharcoalToken.LazyBinary] = [
    function (result) { return '∧'; },
    function (result) { return '∨'; }
];

StringifierProcessor[CharcoalToken.LazyTernary] = [
    function (result) { return '⎇'; }
];

StringifierProcessor[CharcoalToken.OtherOperator] = [
    function (result) { return 'ＫＤ' + result[1] + result[2]; }
];

StringifierProcessor[CharcoalToken.Program] = [
    function (result) { return result[0] + result[2]; },
    function (result) { return ''; }
];

StringifierProcessor[CharcoalToken.Body] = [
    function (result) { return '«' + result[1] + '»'; },
    function (result) { return result[0]; }
];

StringifierProcessor[CharcoalToken.Command] = [
    function (result) { return 'Ｓ' + result[2]; },
    function (result) { return 'Ｎ' + result[2]; },
    function (result) { return 'Ｖ' + result[2]; },
    function (result) { return result[2] + result[4]; },
    function (result) { return result[2]; },
    function (result) { return 'Ｐ' + result[2] + result[4]; },
    function (result) { return 'Ｐ' + result[2]; },
    function (result) { return 'Ｇ' + result[2] + result[4]; },
    function (result) { return 'Ｇ' + result[2] + result[4] + result[5]; },
    function (result) { return 'ＧＨ' + result[2] + result[4]; },
    function (result) { return 'ＧＨ' + result[2] + result[4] + result[5]; },
    function (result) { return 'ＢＲ' + result[2] + result[3]; },
    function (result) { return 'Ｂ' + result[2] + result[3] + result[4]; },
    function (result) { return 'Ｍ' + result[2]; },
    function (result) { return 'Ｍ' + result[2] + result[3]; },
    function (result) { return '↶' + result[2]; },
    function (result) { return '↶'; },
    function (result) { return '↷' + result[2]; },
    function (result) { return '↷'; },
    function (result) { return 'Ｊ' + result[2] + result[3]; },
    function (result) { return '⟲Ｔ' + result[2]; },
    function (result) { return '‖Ｔ' + result[2]; },
    function (result) { return '‖Ｔ' + result[2]; },
    function (result) { return '‖Ｍ' + result[2]; },
    function (result) { return '‖Ｍ' + result[2]; },
    function (result) { return '⟲Ｃ' + result[2] + result[3]; },
    function (result) { return '⟲Ｃ' + result[2]; },
    function (result) { return '‖Ｃ' + result[2]; },
    function (result) { return '‖Ｃ' + result[2]; },
    function (result) { return '⟲Ｏ' + result[2]; },
    function (result) { return '‖Ｏ' + result[2]; },
    function (result) { return '‖Ｏ' + result[2]; },
    function (result) { return '⟲' + result[2]; },
    function (result) { return '‖' + result[2]; },
    function (result) { return 'Ｃ' + result[2] + result[3]; },
    function (result) { return 'Ｆ' + result[2] + result[4]; },
    function (result) { return 'Ｗ' + result[2] + result[4]; },
    function (result) { return '¿' + result[2] + result[4] + result[5]; },
    function (result) { return '¿' + result[2] + result[4]; },
    function (result) { return 'Ａ' + result[2] + result[3]; },
    function (result) { return '¤' + result[2]; },
    function (result) { return 'ＵＢ' + result[2]; },
    function (result) { return 'Ｄ'; },
    function (result) { return 'ＨＦ' + result[2] + result[4] + result[5]; },
    function (result) { return 'ＨＷ' + result[2] + result[4] + result[5]; },
    function (result) { return 'Ｈ' + result[2]; },
    function (result) { return 'Ｈ'; },
    function (result) { return 'Ｔ' + result[2] + result[3]; },
    function (result) { return '⎚'; },
    function (result) { return 'ＵＥ' + result[2] + result[3]; },
    function (result) { return 'ＵＥ' + result[2]; }
];

