'use strict';

function PassThrough (result) {
    return result;
}

var ASTProcessor = Array(CharcoalToken.MAXIMUM + 1);

ASTProcessor[CharcoalToken.Arrow] = [
    function (result) { return 'Left'; },
    function (result) { return 'Up'; },
    function (result) { return 'Right'; },
    function (result) { return 'Down'; },
    function (result) { return 'Up Left'; },
    function (result) { return 'Up Right'; },
    function (result) { return 'Down Right'; },
    function (result) { return 'Down Left'; }
];

ASTProcessor[CharcoalToken.Multidirectional] = (function () {
    var result = Array(UnicodeGrammars[CharcoalToken.Multidirectional.length]).fill(
        function (result) {
            var returns = result[1].slice(1);
            returns.unshift(result[1][0], result[0]);
            return returns;
        }
    );
    result.push(function (result) { return ['Multidirectional']; });
    result.unshift(function (result) { result.unshift('Multidirectional'); return result; });
})();

ASTProcessor[CharcoalToken.Side] = [
    function (result) { return ['Side'] + result; }
];

ASTProcessor[CharcoalToken.String] = [
    function (result) { return ['String "' + result[0] + '"']; }
];

ASTProcessor[CharcoalToken.Number] = [
    function (result) { return ['Number ' + result[0]]; }
];

ASTProcessor[CharcoalToken.Name] = [
    function (result) { return ['Identifier ' + result[0]]; }
];

ASTProcessor[CharcoalToken.Separator] = [
    function (result) { return null; },
    function (result) { return null; }
];

ASTProcessor[CharcoalToken.Arrows] = [
    function (result) {
        var returns = result[1].slice(1);
        returns.unshift(result[1][0], result[0]);
        return returns;
    },
    function (result) { return ['Arrows', result[0]]; }
];

ASTProcessor[CharcoalToken.Sides] = [
    function (result) {
        var returns = result[1].slice(1);
        returns.unshift(result[1][0], result[0]);
        return returns;
    },
    function (result) { return ['Sides', result[0]]; }
];

ASTProcessor[CharcoalToken.Expressions] = [
    function (result) {
        var returns = result[1].slice(1);
        returns.unshift(result[1][0], result[0]);
        return returns;
    },
    function (result) { return ['Expressions', result[0]]; }
];

ASTProcessor[CharcoalToken.PairExpressions] = [
    function (result) {
        var returns = result[2].slice(1);
        returns.unshift(result[2][0], [result[0], result[1]]);
        return returns;
    },
    function (result) { return ['PairExpressions', [result[0], result[1]]; }
];

ASTProcessor[CharcoalToken.List] = [
    function (result) {
        result[1].shift();
        result[1].unshift('List');
        return result[1];
    },
    function (result) {
        return ['List'];
    }
];

ASTProcessor[CharcoalToken.ArrowList] = [
    function (result) {
        result[1].shift();
        result[1].unshift('Arrow list');
        return result[1];
    },
    function (result) {
        return ['Arrow list'];
    }
];

ASTProcessor[CharcoalToken.Dictionary] = [
    function (result) {
        result[1].shift();
        result[1].unshift('Dictionary');
        return result[1];
    },
    function (result) {
        return ['Dictionary'];
    }
];

ASTProcessor[CharcoalToken.Expression] = [
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
    function (result) { return result; },
    function (result) { return result[0]; }
];

ASTProcessor[CharcoalToken.Nilary] = [
    function (result) { return 'Input string'; },
    function (result) { return 'Input number'; },
    function (result) { return 'Random'; },
    function (result) { return 'Peek all'; },
    function (result) { return 'Peek'; }
];

ASTProcessor[CharcoalToken.Unary] = [
    function (result) { return 'Negative'; },
    function (result) { return 'Length'; },
    function (result) { return 'Not'; },
    function (result) { return 'Cast'; },
    function (result) { return 'Random'; },
    function (result) { return 'Evaluate'; },
    function (result) { return 'Pop'; },
    function (result) { return 'To lowercase'; },
    function (result) { return 'To uppercase'; },
    function (result) { return 'Minimum'; },
    function (result) { return 'Maximum'; }
];

ASTProcessor[CharcoalToken.Binary] = [
    function (result) { return 'Sum'; },
    function (result) { return 'Difference'; },
    function (result) { return 'Product'; },
    function (result) { return 'Quotient'; },
    function (result) { return 'Modulo'; },
    function (result) { return 'Equals'; },
    function (result) { return 'Less than'; },
    function (result) { return 'Greater than'; },
    function (result) { return 'Inclusive range'; },
    function (result) { return 'Mold'; },
    function (result) { return 'Exponentiate'; },
    function (result) { return 'At index'; },
    function (result) { return 'Push'; },
    function (result) { return 'Join'; },
    function (result) { return 'Split'; },
    function (result) { return 'Find all'; },
    function (result) { return 'Find'; }
];

ASTProcessor[CharcoalToken.Ternary] = [
];

ASTProcessor[CharcoalToken.LazyUnary] = [
];

ASTProcessor[CharcoalToken.LazyBinary] = [
    function (result) { return 'And'; },
    function (result) { return 'Or'; }
];

ASTProcessor[CharcoalToken.LazyTernary] = [
    function (result) { return 'Ternary'; }
];

ASTProcessor[CharcoalToken.OtherOperator] = [
    function (result) {
        var returns = result.slice(1);
        returns.unshift('Peek direction');
        return returns;
    }
];

ASTProcessor[CharcoalToken.Program] = [
    function (result) {
        var returns = result[1].slice(1);
        returns.unshift(result[1][0], result[0]);
        return returns;
    },
    function (result) { return ['Program']; }
];

ASTProcessor[CharcoalToken.Body] = [
    function (result) { return result[1]; },
    function (result) { return result[0]; }
];

ASTProcessor[CharcoalToken.Command] = [
    function (result) { return ['Input String', result[1]]; },
    function (result) { return ['Input Number', result[1]]; },
    function (result) { return ['Evaluate', result[1]]; },
    function (result) { result.unshift('Print'); return result; },
    function (result) { result.unshift('Print'); return result; },
    function (result) { result.unshift('Multiprint'); return result; },
    function (result) { result.unshift('Multiprint'); return result; },
    function (result) { result.unshift('Polygon'); return result; },
    function (result) { result.unshift('Polygon'); return result; },
    function (result) { result.unshift('Hollow Polygon'); return result; },
    function (result) { result.unshift('Hollow Polygon'); return result; },
    function (result) { result.unshift('Rectangle'); return result; },
    function (result) { result.unshift('Box'); return result; },
    function (result) { result.unshift('Move'); return result; },
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

