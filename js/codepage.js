'use strict';

var UnicodeLookup = {};
var ReverseLookup = {};
var OrdinalLookup = {};

(function () {
    function CharacterPlus128 (character) {
        return String.fromCharCode(character.charCodeAt(0) + 128);
    }

    var fullwidth = 'ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ';
    var upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    for (var i = 0; i < 26; i++)
        UnicodeLookup[CharacterPlus128(upper[i])] = fullwidth[i];
    var superscript = '⁰¹²³⁴⁵⁶⁷⁸⁹';
    var number = '0123456789';
    for (var i = 0; i < 10; i++)
        UnicodeLookup[CharacterPlus128(number[i])] = superscript[i];
    var greek = 'αβγδεζηθικλμνξπρσςτυφχψω';
    var lower = 'abgdezhqiklmnxprsvtufcyw';
    for (var i = 0; i < 24; i++)
        UnicodeLookup[CharacterPlus128(lower[i])] = greek[i];
    var doubleBracket = '⟦⟧⦃⦄«»';
    var bracket = '[]{}()';
    for (var i = 0; i < 6; i++)
        UnicodeLookup[CharacterPlus128(bracket[i])] = doubleBracket[i];
    var symbol = '⁺⁻×÷﹪¬⁼‹›';
    var operator = '+-*/%!=<>';
    for (var i = 0; i < 6; i++)
        UnicodeLookup[CharacterPlus128(operator[i])] = symbol[i];
    var arrow = '←↑→↓↖↗↘↙↶↷⟲';
    var ascii_equivalent = '\x11\x12\x13\x14\x1C\x1D\x1E\x1F\x0E\x0F\x10';
    for (var i = 0; i < 11; i++)
        UnicodeLookup[ascii_equivalent] = arrow;
    var other = '¿‖´·¤¦⎚…§⎆⎈⌀';
    var asciiCharacter = '?;`.o: _$,&\'';
    for (var i = 0; i < 12; i++)
        UnicodeLookup[CharacterPlus128(asciiCharacter[i])] = other[i];
    var replacement = '¶⎇‽∧∨“”↧↥⌊⌈±⊞⊟';
    var replaced = '\
\n\x15\x16\x01\x02\x03\x04\x17\x18\x19\x1A\x1B\x05\x06';
    for (var i = 0; i < 7; i++)
        UnicodeLookup[replaced] = replacement;
    var high = '⪫⪪℅◧◨⮌⌕';
    var low = '\x01\x02\x03\x04\x05\x06\x1B';
    for (var i = 0; i < 2; i++)
        UnicodeLookup[CharacterPlus128(low[i])] = high[i];
    for (var eightBit in UnicodeLookup) {
        var character = UnicodeLookup[eightBit];
        ReverseLookup[character] = eightBit;
        OrdinalLookup[character] = eightBit.charCodeAt(0);
    }
    for (var printableCode = 32; printableCode < 127; printableCode++) {
        var printable = String.fromCharCode(printableCode);
        ReverseLookup[printable] = printable;
        OrdinalLookup[printable] = printableCode;
    }
})();

var Codepage = Array(256).fill().map(function (_, index) {
    var character = String.fromCharCode(index);
    return UnicodeLookup[character] || character;
});

var InCodepage = (function () {
    var newlineCharCode = '\n'.charCodeAt(0),
        alphaCharCode = 'α'.charCodeAt(0),
        omegaCharCode = 'ω'.charCodeAt(0),
        omicronCharCode = 'ο'.charCodeAt(0),
        fullwidthACharCode = 'Ａ'.charCodeAt(0),
        fullwidthZCharCode = 'Ｚ'.charCodeAt(0),
        otherCharcoalCharacters = '⁰¹²³⁴⁵⁶⁷⁸⁹\
⟦⟧⦃⦄«»⁺⁻×÷﹪∧∨¬⁼‹›\
←↑→↓↖↗↘↙\
↶↷⟲¿‽‖·¤¦“”⎚¶…§⎇↥↧⌊⌈±⊞⊟⪫⪪⌕℅◧◨⮌';
    return function (character) {
        var charcode = character.charCodeAt(0);
        return (
            (charcode <= 128 && character != newlineCharCode) ||
            (charcode >= alphaCharCode && charcode <= omegaCharCode && charcode != omicronCharCode) ||
            (charcode >= fullwidthACharCode && charcode <= fullwidthZCharCode) ||
            otherCharcoalCharacters.includes(character)
        );
    }
})();

var UnicodeCommands = '\
ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ\
⁰¹²³⁴⁵⁶⁷⁸⁹\
αβγδεζηθικλμνξπρσςτυφχψω\
⟦⟧⦃⦄«»⁺⁻×÷﹪∧∨¬⁼‹›\
←↑→↓↖↗↘↙\
↶↷⟲¿‽‖·¤¦“”⎚…§⎇↥↧⌊⌈±⊞⊟⪫⪪⌕℅◧◨⮌';

