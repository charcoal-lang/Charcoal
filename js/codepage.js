'use strict';

var UnicodeLookup = {}
var ReverseLookup = {}
var OrdinalLookup = {}

(function () {
    function CharacterPlus128 (character) {
        return String.fromCharCode(character.charCodeAt(0) + 128);
    }

    var fullwidth = 'ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ';
    var upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    for (var i = 0; i < 26; i++)
        UnicodeLookup[CharacterPlus128(upper)] = fullwidth;
    var superscript = '⁰¹²³⁴⁵⁶⁷⁸⁹';
    var number = '0123456789';
    for (var i = 0; i < 10; i++)
        UnicodeLookup[CharacterPlus128(number)] = superscript;
    var greek = 'αβγδεζηθικλμνξπρσςτυφχψω';
    var lower = 'abgdezhqiklmnxprsvtufcyw';
    for (var i = 0; i < 24; i++)
        UnicodeLookup[CharacterPlus128(lower)] = greek;
    // h, j, o are free
    var doubleBracket = '⟦⟧⦃⦄«»';
    var bracket = '[]{}()';
    for (var i = 0; i < 6; i++)
        UnicodeLookup[CharacterPlus128(bracket)] = doubleBracket;
    // not sure about ()
    var symbol = '⁺⁻×÷﹪¬⁼‹›';
    var operator = '+-*/%!=<>';
    for (var i = 0; i < 6; i++)
        UnicodeLookup[CharacterPlus128(operator)] = symbol;
    var arrow = '←↑→↓↖↗↘↙↶↷⟲';
    var ascii_equivalent = '\x11\x12\x13\x14\x1C\x1D\x1E\x1F\x0E\x0F\x10';
    for (var i = 0; i < 11; i++)
        UnicodeLookup[ascii_equivalent] = arrow;
    // device controls, separators, shift out, shift in, data link escape
    var other = '¿‖´·¤¦⎚…§⎆⎈⌀';
    var asciiCharacter = '?;`.o: _$,&\'';
    for (var i = 0; i < 12; i++)
        UnicodeLookup[CharacterPlus128(ascii_character)] = other;
    // not sure about ;
    var replacement = '¶⎇‽∧∨“”';
    var replaced = '\n\x15\x16\x01\x02\x03\x04';
    for (var i = 0; i < 7; i++)
        UnicodeLookup[replaced] = replacement;
    // negative acknowledge, synchronous idle
    // start of heading, start of text, end of text, end of transmission
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

function InCodepage (character) {
    return true; // TODO
}

var UnicodeCommands = '\
ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ\
⁰¹²³⁴⁵⁶⁷⁸⁹\
αβγδεζηθικλμνξπρσςτυφχψω\
⟦⟧⦃⦄«»⁺⁻×÷﹪∧∨¬⁼‹›\
←↑→↓↖↗↘↙\
↶↷⟲¿‽‖·¤¦“”⎚…§⎇';
