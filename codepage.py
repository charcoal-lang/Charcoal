import re

UnicodeLookup, ReverseLookup, OrdinalLookup = {}, {}, {}


def add_character(character, result):
    UnicodeLookup[result] = character

for fullwidth, upper in zip(
    "ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ",
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
):
    add_character(fullwidth, chr(ord(upper) + 128))
for superscript, number in zip("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789"):
    add_character(superscript, chr(ord(number) + 128))
for greek, lower in zip(
    "αβγδεζηθικλμνξπρσςτυφχψω",
    "abgdezhqiklmnxprsvtufcyw"
):
    add_character(greek, chr(ord(lower) + 128))  # h and j are free
for double_bracket, bracket in zip("⟦⟧⦃⦄«»", "[]{}()"):  # not sure about ()
    add_character(double_bracket, chr(ord(bracket) + 128))
for symbol, operator in zip("⁺⁻×÷∕﹪¬⁼‹›", "+-*/\\%!=<>"):
    add_character(symbol, chr(ord(operator) + 128))
for arrow, ascii_equivalent in zip(
    "←↑→↓↖↗↘↙↶↷⟲",
    "\x11\x12\x13\x14\x1C\x1D\x1E\x1F\x0E\x0F\x10"
):
    add_character(arrow, ascii_equivalent)
for other, ascii_character in zip("¿‖´·¤¦⎚…§", "?;`.o: _$"):
    # not sure about ;
    add_character(other, chr(ord(ascii_character) + 128))
for replacement, replaced in zip(
    "¶⎇‽；∧∨“”↧↥⌊⌈±⊞⊟➙⧴″‴＆｜�⭆",
    "\n\x15\x16\x00\x01\x02\x03\x04\x17\x18\x19\x1A\x1B\x05\x06\x07\x08\x09\x0B\
\x0C\x0D\xFF\x7F"
):
    add_character(replacement, replaced)
for high, low in zip(
    "⸿？⪫⪪℅◧◨⮌⌕≡№≔≕▷▶✂⊙⬤✳～↔≦≧ⅈⅉΣΠ↨⍘⊕⊖⊗⊘₂Φ",
    "\n\x00\x01\x02\x03\x04\x05\x06\x1B\x07\x08\x0C\x0D\x0E\x0F\x10\x09\x0B\
\x15~\x16\x17\x18\x19\x1A\x11\x12\x13\x14\x1C\x1D\x1E\x1F\x22\x23"
):
    add_character(high, chr(ord(low) + 128))
keys = list(UnicodeLookup.keys())
values = list(UnicodeLookup.values())
for character in range(256):
    char = chr(character)
    value = char
    if char not in keys:
        if char in values:
            while value in values:
                value = keys[values.index(value)]
            UnicodeLookup[char] = value
        else:
            UnicodeLookup[char] = char
keys = list(UnicodeLookup.keys())
values = list(UnicodeLookup.values())
for character in values:
    value = character
    if character not in keys:
        while value in values:
            value = keys[values.index(value)]
        UnicodeLookup[character] = value
keys = list(UnicodeLookup.keys())
values = list(UnicodeLookup.values())
for key in UnicodeLookup:
    ReverseLookup[UnicodeLookup[key]] = key
for ordinal in range(256):
    OrdinalLookup[UnicodeLookup[chr(ordinal)]] = ordinal
Codepage = [UnicodeLookup.get(chr(code), chr(code)) for code in range(0, 256)]


def InCodepage(character):
    return character in Codepage

UnicodeCommands = "ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ\
⁰¹²³⁴⁵⁶⁷⁸⁹αβγδεζηθικλμνξπρσςτυφχψω⟦⟧⦃⦄«»⁺⁻×÷∕﹪∧∨¬⁼‹›＆｜～←↑→↓↖↗↘↙\
↶↷⟲¿‽‖·¤¦“”⎚…§⎇↥↧⌊⌈±⊞⊟➙⧴″‴？⪫⪪⌕℅◧◨⮌≡№≔≕▷▶✂⊙⬤✳�≦≧ⅈⅉ；ΣΠ⊕⊖⊗⊘⭆↨⍘₂↔Φ"
UnicodeCommandRegex = "Ａ-Ｚ⸿¶⁰¹²³⁴-⁹α-ξπ-ω⟦⟧⦃⦄«»⁺⁻×÷∕﹪∧∨¬⁼‹›＆｜～←-↓↖-↙\
↶↷⟲¿‽‖´·¤¦“”⎚…§⎇↥↧⌊⌈±⊞⊟➙⧴″‴？⪫⪪⌕℅◧◨⮌≡№≔≕▷▶✂⊙⬤✳�≦≧ⅈⅉ；ΣΠ⊕⊖⊗⊘⭆↨⍘₂↔Φ"
sCommand = "[%s]" % UnicodeCommandRegex
sOperator = """\
[ＳＮ‽¬Ｉ‽Ｖ⊟➙⧴″‴↧↥⌊⌈℅⮌⁺⁻×÷∕﹪⁼‹›＆｜～…Ｘ§？⪫⪪⌕◧◨№⎇Ｅ∧∨▷≕✂⊙⬤ⅈⅉ；ΣΠ⊕⊖⊗⊘⭆↨⍘₂↔Φ]\
|Ｋ.|±Ｌ|⊞Ｏ|⌕Ａ|ＵＶ"""
rCommand = re.compile("(%s)" % sCommand)
rOperator = re.compile("(%s)" % sOperator)
