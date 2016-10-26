UnicodeLookup = {}
ReverseLookup = {}
OrdinalLookup = {}

for fullwidth, upper in zip(
    "ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ",
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
):
    UnicodeLookup[chr(ord(upper) + 128)] = fullwidth

for superscript, number in zip("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789"):
    UnicodeLookup[chr(ord(number) + 128)] = superscript

for greek, lower in zip(
    "αβγδεζηθικλμνξπρσςτυφχψω",
    "abgdezhqiklmnxprsvtufcyw"
):
    UnicodeLookup[chr(ord(lower) + 128)] = greek
    # h, j, o are free

for double_bracket, bracket in zip("⟦⟧⦃⦄«»", "[]{}()"):
    # TODO: change ()
    UnicodeLookup[chr(ord(bracket) + 128)] = double_bracket

for symbol, operator in zip("⁺⁻×÷﹪¬⁼‹›", "+-*/%!=<>"):
    UnicodeLookup[chr(ord(operator) + 128)] = symbol

for arrow, ascii_equivalent in zip(
    "←↑→↓↖↗↘↙↶↷⟲",
    "\x11\x12\x13\x14\x1C\x1D\x1E\x1F\x0E\x0F\x10"
): # device controls, separators, shift out, shift in, data link escape
    UnicodeLookup[ascii_equivalent] = arrow

for other, ascii_character in zip("¿‖´·¤¦⎚…§⎆⎈⌀", "?;`.o: _$,&'"):
    # TODO: not sure about ;
    UnicodeLookup[chr(ord(ascii_character) + 128)] = other

for replacement, replaced in zip("¶⎇‽∧∨“”", "\n\x15\x16\x01\x02\x03\x04"):
    # negative acknowledge, synchronous idle
    # start of heading, start of text, end of text, end of transmission
    UnicodeLookup[replaced] = replacement

for eight_bit in UnicodeLookup:
    character = UnicodeLookup[eight_bit]
    ReverseLookup[character] = eight_bit
    OrdinalLookup[character] = ord(eight_bit)

for ascii_character in range(32, 128):
    character = chr(ascii_character)
    ReverseLookup[character] = character
    OrdinalLookup[character] = ascii_character

Codepage = [UnicodeLookup.get(chr(code), chr(code)) for code in range(0, 256)]

def InCodepage(character):
    return (
        (character <= "\xFF" and character != "\n") or
                (character >= "α" and character <= "ω" and character != "ο") or
                (character >= "Ａ" and character <= "Ｚ") or
                character in "⁰¹²³⁴⁵⁶⁷⁸⁹\
⟦⟧⦃⦄«»⁺⁻×÷﹪∧∨¬⁼‹›\
←↑→↓↖↗↘↙\
↶↷⟲¿‽‖´·¤¦“”⎚¶…§⎇"
    )

UnicodeCommands = "\
ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ\
⁰¹²³⁴⁵⁶⁷⁸⁹\
αβγδεζηθικλμνξπρσςτυφχψω\
⟦⟧⦃⦄«»⁺⁻×÷﹪∧∨¬⁼‹›\
←↑→↓↖↗↘↙\
↶↷⟲¿‽‖·¤¦“”⎚…§⎇"
