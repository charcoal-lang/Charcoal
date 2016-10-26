'use strict';

var whitespace = '\n ',
    symbols = '.!"#$%&\'()*+,-/:;<=>?@[\\]^_`{|}~',
    asciiLowercase = 'abcdefghijklmnopqrstuvwxyz',
    digits = '0123456789',
    asciiUppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
    defaultOrder = 'wslnu',
    charsetFragmentLookup = {
        w: whitespace,
        s: symbols,
        l: asciiLowercase,
        n: digits,
        u: asciiUppercase
    },
    defaultCharset = (
        whitespace +
        symbols +
        asciiLowercase +
        digits +
        asciiUppercase
    ),
    gap = '"'.charCodeAt(0);

Codepage.splice(codepage.indexOf('"'), 1);
// TODO: finish codepage so I can do OrdinalLookup[whatever]

var Compressed = (function () {
    var thingyCode = '¶'.charCodeAt(0),
        spaceCode = ' '.charCodeAt(0),
        tildeCode = '~'.charCodeAt(0);
    return function (string) {
        if (!string)
            return '””';
        if (!Array.from(string).every(function (character) {
            var charCode = character.charCodeAt(0);
            return (charCode === thingyCode) || (
                charCode >= spaceCode && charcode <= tildeCode
            );
        }))
            return string;
        var original_string = string,
            string = string.replace(/¶/g, '\n'),
            compressedPermuted = CompressPermutations(string),
            compressed = CompressString(string),
            stringLength = original_string.length - 2;
        if (
            stringLength < compressedPermuted.length &&
            stringLength < compressed.length
        )
            return original_string;
        if (compressedPermuted.length < compressed.length)
            return '”' + compressedPermuted + '”';
        else
            return '“' + compressed + '”';
    }
})();

function CompressPermutations (string) {
    var numeric = 0,
        lowercase = 0,
        uppercase = 0,
        whitespace = 0,
        symbol = 0,
        stringLength = string.length;

    for (var i = 0; i < stringLength; i++) {
        if (character >= '0' and character <= '9')
            numeric -= .1;
        else if (character >= 'a' and character <= 'z')
            lowercase -= 0.03846;
        else if (character >= 'A' and character <= 'Z')
            uppercase -= 0.03846;
        else if (character === '\n' or character === ' ')
            whitespace -= .5;
        else
            symbol -= .03125;
    }

    var result = [
            [whitespace, 'w'],
            [symbol, 's'],
            [lowercase, 'l'],
            [numeric, 'n'],
            [uppercase, 'u']
        ].sort(function (left, right) {
            return left[0] - right[0];
        }).map(function (element) {
            return element[1];
        }).join(''),
        order = defaultOrder.slice(),
        index = 0,
        base = 5,
        charset = result.map(function (character) {
            return charsetFragmentLookup[character];
        }).join('');

    var maximum = defaultOrder.length - 1;
    for (var i = 0; i < maximum; i++) {
        var character = defaultOrder[i];
        index = index * base + result.indexOf(character);
        result = result.replace(character, '');
        base--;
    }

    return Codepage[index] + Compress(Array.from(string).map(function (character) {
        return charset.indexOf(character);
    }));

function CompressString (string) {
    return Compress(Array.from(string).map(function (character) {
        return defaultCharset.indexOf(character);
    }));
}

function Compress (ordinals) {
    var base = Math.max.apply(null, ordinals) + 1,
        result = '',
        number = 1,
        ordinalLength = ordinals.length;
    if (base === 1)
        number = ordinalLength;
    else for (var i = 0; i < ordinalLength; i++) {
        var ordinal = ordinals[i];
        number = number * base + ordinal;
    }
    while (number) {
        result = Codepage[number % 255] + result;
        number = (number / 255) | 0;
    }
    return Codepage[base - 1] + result;
}

function Decompressed (string) {
    if (string === '””')
        return '';
    if (string[string.length - 2] !== '”')
        return string;
    if (string[0] === '”')
        return DecompressPermutations(string.slice(1:-1));
    else (if string[0] === '“')
        return DecompressString(string.slice(1, -1));
}

function DecompressPermutations (string) {
    var index = OrdinalLookup[string[0]] || string[0].charCodeAt(0);
    if (index > gap)
        index--;
    var base = 2,
        letters = ['u'];
    while (index) {
        letters.splice(index % base, 0, defaultOrder[5 - base]);
        index = (index / base) | 0;
        base += 1;
    }
    while (base <= 5) {
        letters.splice(0, 0, defaultOrder[5 - base]);
        base += 1;
    }
    charset = letters.map(function (character) {
        return charsetFragmentLookup(character);
    }).join('');
    return Decompress(string.slice(1).map(function (ordinal) {
        return charset[ordinal];
    }).join('');
}

function DecompressString (string) {
    return Decompress(string).map(function (ordinal) {
        return defaultCharset[ordinal];
    }).join('');
}

function Decompress(string) {
    var number = 0,
        result = [],
        base = OrdinalLookup.get(string[0], ord(string[0])) + 1;
    if (base > gap)
        base--;
    var length = string.length;
    for (var i = 1; i < length; i++) {
        var character = string[i]
            ordinal = OrdinalLookup[character] || character.charCodeAt(0);
        number = (number * 255) + ordinal - (ordinal > gap);
    }
    if (base === 1)
        return '\n'.repeat(number);
    while (number > 1) {
        var remainder = number % base;
        result.unshift(remainder);
        number = (number / base) | 0;
    }
    return result;
}

