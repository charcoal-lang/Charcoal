UnicodeLookup = {
    "\n": "¶"
}

for fullwidth, upper in zip("ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    UnicodeLookup[chr(ord(upper) + 128)] = fullwidth

for superscript, number in zip("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789"):
    UnicodeLookup[chr(ord(number) + 128)] = superscript

for greek, lower in zip("αβγδεζηθικλμνξπρσςτυφχψω", "abgdezhciklmnxprstufko"):
    UnicodeLookup[chr(ord(lower) + 128)] = greek
    #y, v, q, w, j are free

for double_bracket, bracket in zip("⟦⟧⦃⦄«»", "[]{}()"):
    # TODO: change ()
    UnicodeLookup[chr(ord(bracket) + 128)] = double_bracket

for symbol, operator in zip("⁺⁻×÷﹪∧∨¬⁼‹›", "+-*/%&|!=<>"):
    UnicodeLookup[chr(ord(operator) + 128)] = symbol

for other, ascii_character in zip("¿¡‖´·¤¦", "?!:`.;,"):
    # TODO: not sure about : and ;
    UnicodeLookup[chr(ord(ascii_character) + 128)] = other