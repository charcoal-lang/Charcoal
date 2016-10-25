function PassThrough (result) {
    return result;
}

var ASTProcessor = {
    CharcoalToken.Arrow: [
        function (result) { return 'Left'; },
        function (result) { return 'Up'; },
        function (result) { return 'Right'; },
        function (result) { return 'Down'; },
        function (result) { return 'Up Left'; },
        function (result) { return 'Up Right'; },
        function (result) { return 'Down Right'; },
        function (result) { return 'Down Left'; }
    ],
    CharcoalToken.Multidirectional: (function () {
        var result = Array(UnicodeGrammars[CharcoalToken.Multidirectional.length]).fill(
            function (result) {
                var returns = result[1].slice(1);
                returns.unshift(result[1][0], result[0]);
                return returns;
            }
        );
        result.push(function (result) { return ['Multidirectional']; });
        result.unshift(function (result) { result.unshift('Multidirectional'); return result; });
    })(),
    CharcoalToken.Side: [
        function (result) { return ['Side'] + result; }
    ],
    CharcoalToken.String: [
        function (result) { return ['String "' + result[0] + '"']; }
    ],
    CharcoalToken.Number: [
        function (result) { return ['Number ' + result[0]]; }
    ],
    CharcoalToken.Name: [
        function (result) { return ['Identifier ' + result[0]]; }
    ],
    CharcoalToken.Separator: [
        function (result) { return null; },
        function (result) { return null; }
    ],

    CharcoalToken.Arrows: [
        function (result) {
            var returns = result[1].slice(1);
            returns.unshift(result[1][0], result[0]);
            return returns;
        },
        function (result) { return ['Arrows', result[0]]; }
    ],
    CharcoalToken.Sides: [
        function (result) {
            var returns = result[1].slice(1);
            returns.unshift(result[1][0], result[0]);
            return returns;
        },
        function (result) { return ['Sides', result[0]]; }
    ],
    CharcoalToken.Expressions: [
        function (result) {
            var returns = result[2].slice(1);
            returns.unshift(result[2][0], result[0]);
            return returns;
        },
        function (result) { return ['Expressions', result[0]]; }
    ],

    CharcoalToken.List: [
        function (result) { return ['List'] + result[1][1:]; }
    ],
    CharcoalToken.ArrowList: [
        function (result) { return ['Arrow list'] + result[1][1:]; }
    ],

    CharcoalToken.Expression: [
        function (result) { return result[0]; },
        function (result) { return result[0]; },
        function (result) { return result[0]; },
        function (result) { return result[0]; },
        function (result) { return result; },
        function (result) { return result; },
        function (result) { return result; },
        function (result) { return result; },
        function (result) { return result; },
        function (result) { return result; },
        function (result) { return result[0]; }
    ],
    CharcoalToken.Nilary: [
        function (result) { return 'Input String'; },
        function (result) { return 'Input Number'; },
        function (result) { return 'Random'; }
    ],
    CharcoalToken.Unary: [
        function (result) { return 'Negative'; },
        function (result) { return 'Length'; },
        function (result) { return 'Not'; },
        function (result) { return 'Cast'; },
        function (result) { return 'Random'; },
        function (result) { return 'Evaluate'; }
    ],
    CharcoalToken.Binary: [
        function (result) { return 'Sum'; },
        function (result) { return 'Difference'; },
        function (result) { return 'Product'; },
        function (result) { return 'Quotient'; },
        function (result) { return 'Modulo'; },
        function (result) { return 'Equals'; },
        function (result) { return 'Less Than'; },
        function (result) { return 'Greater Than'; },
        function (result) { return 'Cycle and chop'; },
        function (result) { return 'Exponentiate'; },
        function (result) { return 'At index'; }
    ],
    CharcoalToken.Ternary: [
    ],
    CharcoalToken.LazyUnary: [
    ],
    CharcoalToken.LazyBinary: [
        function (result) { return 'And'; },
        function (result) { return 'Or'; }
    ],
    CharcoalToken.LazyTernary: [
        function (result) { return 'Ternary'; }
    ],

    CharcoalToken.Program: [
        function (result) { return  [result[1][0]; }, result[0]] + result[1][1:],
        function (result) { return ['Program']; }
    ],
    CharcoalToken.Body: [
        function (result) { return result[1]; },
        function (result) { return result[0]; }
    ],
    CharcoalToken.Command: [
        function (result) { return ['Input String', result[1]]; },
        function (result) { return ['Input Number', result[1]]; },
        function (result) { return ['Evaluate', result[1]]; },
        function (result) { return ['Print'] + result; },
        function (result) { return ['Print'] + result; },
        function (result) { result.unshift('Multiprint'); return result; },
        function (result) { result.unshift('Multiprint'); return result; },
        function (result) { result.unshift('Polygon'); return result; },
        function (result) { result.unshift('Polygon'); return result; },
        function (result) { result.unshift('Hollow Polygon'); return result; },
        function (result) { result.unshift('Hollow Polygon'); return result; },
        function (result) { result.unshift('Rectangle'); return result; },
        function (result) { result.unshift('Box'); return result; },
        function (result) { return ['Move'] + result; },
        function (result) { result.unshift('Move'); return result; },
        function (result) { result.unshift('Move'); return result; },
        function (result) { return ['Pivot Left', result[1]]; },
        function (result) { return ['Pivot Left']; },
        function (result) { return ['Pivot Right', result[1]]; },
        function (result) { return ['Pivot Right']; },
        function (result) { result.unshift('Jump'); return result; },
        function (result) { result.unshift('Rotate transform'); return result; },
        function (result) { result.unshift('Reflect transform'); return result; },
        function (result) { result.unshift('Reflect transform'); return result; },
        function (result) { result.unshift('Reflect mirror'); return result; },
        function (result) { result.unshift('Reflect mirror'); return result; },
        function (result) { result.unshift('Rotate copy'); return result; },
        function (result) { result.unshift('Rotate copy'); return result; },
        function (result) { result.unshift('Reflect copy'); return result; },
        function (result) { result.unshift('Reflect copy'); return result; },
        function (result) { result.unshift('Rotate overlap'); return result; },
        function (result) { result.unshift('Reflect overlap'); return result; },
        function (result) { result.unshift('Reflect overlap'); return result; },
        function (result) { result.unshift('Rotate'); return result; },
        function (result) { result.unshift('Reflect'); return result; },
        function (result) { result.unshift('Copy'); return result; },
        function (result) { result.unshift('For'); return result; },
        function (result) { result.unshift('While'); return result; },
        function (result) { result.unshift('If'); return result; },
        function (result) { result.unshift('If'); return result; },
        function (result) { result.unshift('Assign'); return result; },
        function (result) { result.unshift('Fill'); return result; },
        function (result) { return ['SetBackground', result[1]]; },
        function (result) { return ['Dump']; },
        function (result) { result.unshift('Refresh for'); return result; },
        function (result) { result.unshift('Refresh while'); return result; },
        function (result) { return ['Refresh', result[1]]; },
        function (result) { return ['Refresh']; },
        function (result) { return ['Trim', result[1], result[2]]; },
        function (result) { return ['Clear']; },
        function (result) { return ['Extend', result[1], result[2]]; },
        function (result) { return ['Extend', result[1]]; }
    ]
}
