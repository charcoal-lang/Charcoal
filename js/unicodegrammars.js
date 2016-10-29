'use strict';

var UnicodeGrammars = new Array(CharcoalToken.Maximum + 1);

UnicodeGrammars[CharcoalToken.Arrow] = [
    ['←'],
    ['↑'],
    ['→'],
    ['↓'],
    ['↖'],
    ['↗'],
    ['↘'],
    ['↙']
];

UnicodeGrammars[CharcoalToken.Multidirectional] = [
    [CharcoalToken.Arrows],
    ['+', CharcoalToken.Multidirectional],
    ['X', CharcoalToken.Multidirectional],
    ['*', CharcoalToken.Multidirectional],
    ['|', CharcoalToken.Multidirectional],
    ['-', CharcoalToken.Multidirectional],
    ['\\', CharcoalToken.Multidirectional],
    ['/', CharcoalToken.Multidirectional],
    ['<', CharcoalToken.Multidirectional],
    ['>', CharcoalToken.Multidirectional],
    ['^', CharcoalToken.Multidirectional],
    ['K', CharcoalToken.Multidirectional],
    ['L', CharcoalToken.Multidirectional],
    ['T', CharcoalToken.Multidirectional],
    ['V', CharcoalToken.Multidirectional],
    ['Y', CharcoalToken.Multidirectional],
    ['7', CharcoalToken.Multidirectional],
    ['¬', CharcoalToken.Multidirectional],
    []
];

UnicodeGrammars[CharcoalToken.Side] = [
    [CharcoalToken.Arrow, CharcoalToken.Expression]
];

UnicodeGrammars[CharcoalToken.Separator] = [
    ['¦'],
    []
];

UnicodeGrammars[CharcoalToken.Arrows] = [
    [CharcoalToken.Arrow, CharcoalToken.Arrows],
    [CharcoalToken.Arrow]
];

UnicodeGrammars[CharcoalToken.Sides] = [
    [CharcoalToken.Side, CharcoalToken.Sides],
    [CharcoalToken.Side]
];

UnicodeGrammars[CharcoalToken.Expressions] = [
    [
        CharcoalToken.Expression,
        CharcoalToken.Expressions
    ],
    [CharcoalToken.Expression]
];

UnicodeGrammars[CharcoalToken.PairExpressions] = [
    [
        CharcoalToken.Expression,
        CharcoalToken.Expression,
        CharcoalToken.PairExpressions
    ],
    [CharcoalToken.Expression, CharcoalToken.Expression]
];

UnicodeGrammars[CharcoalToken.List] = [
    ['⟦', CharcoalToken.Expressions, '⟧'],
    ['⟦', '⟧']
];

UnicodeGrammars[CharcoalToken.ArrowList] = [
    ['⟦', CharcoalToken.Multidirectional, '⟧'],
    ['⟦', '⟧']
];

UnicodeGrammars[CharcoalToken.Dictionary] = [
    ['⦃', CharcoalToken.PairExpressions, '⦄'],
    ['⦃', '⦄']
];

UnicodeGrammars[CharcoalToken.Expression] = [
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
];

UnicodeGrammars[CharcoalToken.Nilary] = [
    ['Ｓ'],
    ['Ｎ'],
    ['‽'],
    ['ＫＡ'],
    ['Ｋ']
];

UnicodeGrammars[CharcoalToken.Unary] = [
    ['⁻'],
    ['Ｌ'],
    ['¬'],
    ['Ｉ'],
    ['‽'],
    ['Ｖ'],
    ['⊟'],
    ['↧'],
    ['↥'],
    ['⌊'],
    ['⌈']
];

UnicodeGrammars[CharcoalToken.Binary] = [
    ['⁺'],
    ['⁻'],
    ['×'],
    ['÷'],
    ['﹪'],
    ['⁼'],
    ['‹'],
    ['›'],
    ['…·'],
    ['…'],
    ['Ｘ'],
    ['§'],
    ['⊞'],
    ['⪫'],
    ['⪪'],
    ['⌕Ａ'],
    ['⌕']
];

UnicodeGrammars[CharcoalToken.Ternary] = [
];

UnicodeGrammars[CharcoalToken.LazyUnary] = [
];

UnicodeGrammars[CharcoalToken.LazyBinary] = [
    ['∧'],
    ['∨']
];

UnicodeGrammars[CharcoalToken.LazyTernary] = [
    ['⎇']
];

UnicodeGrammars[CharcoalToken.OtherOperator] = [
    ['ＫＤ', CharcoalToken.Expression, CharcoalToken.Arrow]
];

UnicodeGrammars[CharcoalToken.Program] = [
    [CharcoalToken.Command, CharcoalToken.Program],
    []
];

UnicodeGrammars[CharcoalToken.Body] = [
    ['«', CharcoalToken.Program, '»'],
    [CharcoalToken.Command]
];

UnicodeGrammars[CharcoalToken.Command] = [
    ['Ｓ', CharcoalToken.Name],
    ['Ｎ', CharcoalToken.Name],
    ['Ｖ', CharcoalToken.Expression],
    [CharcoalToken.Arrow, CharcoalToken.Expression],
    [CharcoalToken.Expression],
    ['Ｐ', CharcoalToken.Multidirectional, CharcoalToken.Expression],
    ['Ｐ', CharcoalToken.Expression],
    ['Ｇ', CharcoalToken.Sides, CharcoalToken.Expression],
    [
        'Ｇ',
        CharcoalToken.Multidirectional,
        CharcoalToken.Expression,
        CharcoalToken.Expression
    ],
    ['ＧＨ', CharcoalToken.Sides, CharcoalToken.Expression],
    [
        'ＧＨ',
        CharcoalToken.Multidirectional,
        CharcoalToken.Expression,
        CharcoalToken.Expression
    ],
    ['ＢＲ', CharcoalToken.Expression, CharcoalToken.Expression],
    [
        'Ｂ',
        CharcoalToken.Expression,
        CharcoalToken.Expression,
        CharcoalToken.Expression
    ],
    [CharcoalToken.Arrow],
    ['Ｍ', CharcoalToken.Arrow],
    ['Ｍ', CharcoalToken.Expression, CharcoalToken.Arrow],
    ['↶', CharcoalToken.Expression],
    ['↶'],
    ['↷', CharcoalToken.Expression],
    ['↷'],
    ['Ｊ', CharcoalToken.Expression, CharcoalToken.Expression],
    ['⟲Ｔ', CharcoalToken.Expression],
    ['‖Ｔ', CharcoalToken.ArrowList],
    ['‖Ｔ', CharcoalToken.Arrow],
    ['‖Ｍ', CharcoalToken.ArrowList],
    ['‖Ｍ', CharcoalToken.Arrow],
    ['⟲Ｃ', CharcoalToken.Expression, CharcoalToken.Arrow],
    ['⟲Ｃ', CharcoalToken.Expression],
    ['‖Ｃ', CharcoalToken.ArrowList],
    ['‖Ｃ', CharcoalToken.Arrow],
    ['⟲Ｏ', CharcoalToken.Expression],
    ['‖Ｏ', CharcoalToken.ArrowList],
    ['‖Ｏ', CharcoalToken.Arrow],
    ['⟲', CharcoalToken.Expression],
    ['‖', CharcoalToken.Arrow],
    ['Ｃ', CharcoalToken.Expression, CharcoalToken.Expression],
    ['Ｆ', CharcoalToken.Expression, CharcoalToken.Body],
    ['Ｗ', CharcoalToken.Expression, CharcoalToken.Body],
    [
        '¿',
        CharcoalToken.Expression,
        CharcoalToken.Body,
        CharcoalToken.Body
    ],
    ['¿', CharcoalToken.Expression, CharcoalToken.Body],
    ['Ａ', CharcoalToken.Expression, CharcoalToken.Name],
    ['¤', CharcoalToken.Expression],
    ['ＵＢ', CharcoalToken.Expression],
    ['Ｄ'],
    [
        'ＨＦ',
        CharcoalToken.Expression,
        CharcoalToken.Expression,
        CharcoalToken.Body
    ],
    [
        'ＨＷ',
        CharcoalToken.Expression,
        CharcoalToken.Expression,
        CharcoalToken.Body
    ],
    ['Ｈ', CharcoalToken.Expression],
    ['Ｈ'],
    ['Ｔ', CharcoalToken.Expression, CharcoalToken.Expression],
    ['⎚'],
    ['ＵＥ', CharcoalToken.Expression, CharcoalToken.Expression],
    ['ＵＥ', CharcoalToken.Expression]
];

