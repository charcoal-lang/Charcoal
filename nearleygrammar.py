# Generated automatically by nearley
# http://github.com/Hardmath123/nearley
from re import compile as RegExp
from ast import literal_eval as JSON_parse
null = None

class JSON(object):
    parse = JSON_parse

Grammar = {
    "Lexer": null,
    "ParserRules": [
        [
            [[18, 1, 18], lambda d, l, fail:  d[1]]
        ], [
            [[2], lambda d, l, fail:  [d[0]]],
            [[2, 17, 1], lambda d, l, fail:  [d[0]] + d[2]]
        ], [
            [[10, 18, 33, '>', 18, 3], lambda d, l, fail:  {"name": d[0], "rules": d[5]}],
            [[10, '[', 5, ']', 18, 36, '>', 18, 3], lambda d, l, fail:  {"macro": d[0], "args": d[2], "exprs": d[8]}],
            [['@', 18, 15], lambda d, l, fail:  {"body": d[2]}],
            [['@', 10, 17, 10], lambda d, l, fail:  {"config": d[1], "value": d[3]}],
            [[39, 18, 11], lambda d, l, fail:  {"include": d[2]["literal"], "builtin": False}],
            [[40, 18, 11], lambda d, l, fail:  {"include": d[2]["literal"], "builtin": True}]
        ], [
            [[6]],
            [[3, 18, '|', 18, 6], lambda d, l, fail:  d[0] + [d[4]]]
        ], [
            [[6]],
            [[4, 18, ',', 18, 6], lambda d, l, fail:  d[0] + [d[4]]]
        ], [
            [[10]],
            [[5, 18, ',', 18, 10], lambda d, l, fail:  d[0] + [d[4]]]
        ], [
            [[9], lambda d, l, fail:  {"tokens": d[0]}],
            [[9, 18, 15], lambda d, l, fail:  {"tokens": d[0], "process": d[2]}]
        ], [
            [[10], lambda d, l, fail:  d[0]],
            [['$', 10], lambda d, l, fail:  {"mixin": d[1]}],
            [[10, '[', 4, ']'], lambda d, l, fail:  {"macrocall": d[0], "args": d[2]}],
            [[11], lambda d, l, fail:  d[0]],
            [['%', 10], lambda d, l, fail:  {"token": d[1]}],
            [[12], lambda d, l, fail:  d[0]],
            [['(', 18, 3, 18, ')'], lambda d, l, fail:  {"subexpression": d[2]}],
            [[7, 18, 8], lambda d, l, fail:  {"ebnf": d[0], "modifier": d[2]}]
        ], [
            [[41], lambda d, l, fail:  d[0]],
            [[42], lambda d, l, fail:  d[0]],
            [[43], lambda d, l, fail:  d[0]]
        ], [
            [[7]],
            [[9, 17, 7], lambda d, l, fail:  d[0] + [d[2]]]
        ], [
            [[RegExp('[\\w\\?\\+]')], lambda d, l, fail:  d[0]],
            [[10, RegExp('[\\w\\?\\+]')], lambda d, l, fail:  d[0] + d[1]]
        ], [
            [[25], lambda d, l, fail:  {"literal": d[0]}]
        ], [
            [['.'], lambda d, l, fail:  RegExp(".")],
            [['[', 13, ']'], lambda d, l, fail:  RegExp("[" + "".join(d[1]) + "]")]
        ], [
            [[]],
            [[13, 14], lambda d, l, fail:  d[0] + [d[1]]]
        ], [
            [[RegExp('[^\\\\\\]]')], lambda d, l, fail:  d[0]],
            [['\\', RegExp('.')], lambda d, l, fail:  d[0] + d[1]]
        ], [
            [['{', '%', 16, '%', '}'], lambda d, l, fail:  d[2]]
        ], [
            [[], lambda d, l, fail:  ""],
            [[16, RegExp('[^%]')], lambda d, l, fail:  d[0] + d[1]],
            [[16, '%', RegExp('[^}]')], lambda d, l, fail:  d[0] + d[1] + d[2]]
        ], [
            [[19]],
            [[20, 21, 18]]
        ], [
            [[]],
            [[17]]
        ], [
            [[RegExp('[\\s]')]],
            [[19, RegExp('[\\s]')]]
        ], [
            [[]],
            [[19]]
        ], [
            [['#', 22, '\n']]
        ], [
            [[]],
            [[22, RegExp('[^\\n]')]]
        ], [
            [[]],
            [[23, 24], lambda d, l, fail: d[0] + [d[1]]]
        ], [
            [[RegExp('[^\\\\"\\n]')], lambda d, l, fail:  d[0]],
            [['\\', 31], lambda d, l, fail:  JSON.parse("\"" + "".join(d) + "\"")]
        ], [
            [['"', 23, '"'], lambda d, l, fail:  "".join(d[1])]
        ], [
            [[]],
            [[26, 27], lambda d, l, fail: d[0] + [d[1]]]
        ], [
            [[RegExp('[^\\\\\\n]')], lambda d, l, fail:  d[0]],
            [['\\', 31], lambda d, l, fail:  JSON.parse("\""+d.join("")+"\"")],
            [[32], lambda d, l, fail:  "'"]
        ], [
            [["'", 26, "'"], lambda d, l, fail:  "".join(d[1])]
        ], [
            [[]],
            [[29, RegExp('[^`]')], lambda d, l, fail: d[0] + [d[1]]]
        ], [
            [['`', 29, '`'], lambda d, l, fail:  "".join(d[1])]
        ], [
            [[RegExp('["\\\\/bfnrt]')], lambda d, l, fail:  d[0]],
            [['u', RegExp('[a-fA-F0-9]'), RegExp('[a-fA-F0-9]'), RegExp('[a-fA-F0-9]'), RegExp('[a-fA-F0-9]')], lambda d, l, fail:  "".join(d)]
        ], [
            [['\\', "'"], lambda d, l, fail: ''.join(d)]
        ], [
            [[34]],
            [[33, 35], lambda d, l, fail: d[0] + [d[1]]]
        ], [
            [['-']],
            [['=']]
        ], [
            [['-']],
            [['=']]
        ], [
            [[37]],
            [[36, 38], lambda d, l, fail: d[0] + [d[1]]]
        ], [
            [['-']],
            [['=']]
        ], [
            [['-']],
            [['=']]
        ], [
            [['@', 'i', 'n', 'c', 'l', 'u', 'd', 'e'], lambda d, l, fail: ''.join(d)]
        ], [
            [['@', 'b', 'u', 'i', 'l', 't', 'i', 'n'], lambda d, l, fail: ''.join(d)]
        ], [
            [[':', '+'], lambda d, l, fail: ''.join(d)]
        ], [
            [[':', '*'], lambda d, l, fail: ''.join(d)]
        ], [
            [[':', '?'], lambda d, l, fail: ''.join(d)]
        ]
    ],
    "Names": [
        'final',
        'prog',
        'prod',
        'expression+',
        'expressionlist',
        'wordlist',
        'completeexpression',
        'expr_member',
        'ebnf_modifier',
        'expr',
        'word',
        'string',
        'charclass',
        'charclassmembers',
        'charclassmember',
        'block',
        'code',
        'whit',
        'whit?',
        'whitraw',
        'whitraw?',
        'comment',
        'commentchars',
        'dqstring_ebnf_1',
        'dstrchar',
        'dqstring',
        'sqstring_ebnf_1',
        'sstrchar',
        'sqstring',
        'btstring_ebnf_1',
        'btstring',
        'strescape',
        'sstrchar_str_1',
        'prod_ebnf_1',
        'prod_ebnf_1_sub_1',
        'prod_ebnf_1_sub_2',
        'prod_ebnf_2',
        'prod_ebnf_2_sub_1',
        'prod_ebnf_2_sub_2',
        'prod_str_1',
        'prod_str_2',
        'ebnf_modifier_str_1',
        'ebnf_modifier_str_2',
        'ebnf_modifier_str_3'
    ]
}