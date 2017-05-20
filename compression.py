from codepage import OrdinalLookup, Codepage
from string import ascii_lowercase, ascii_uppercase, digits
import re

symbols = ".!\"#$%&'()*+,-/:;<=>?@[\]^_`{|}~"
whitespace = "\n "
default_order = "wslnu"
charset_fragment_lookup = {
    "w": whitespace, "s": symbols, "l": ascii_lowercase, "n": digits,
    "u": ascii_uppercase
}
default_charset = (
    whitespace + symbols + ascii_lowercase + digits + ascii_uppercase
)
Codepage.remove("”")
gap = OrdinalLookup["”"]


def Compressed(string):
    if not string:
        return "””"
    if not all(
        character == "¶" or character >= " " and character <= "~"
        for character in string
    ):
        return string
    original_string, string = string, re.sub("¶", "\n", string)
    compressed_permuted = CompressPermutations(string)
    compressed = CompressString(string)
    string_length = len(original_string) - 2
    if (
        string_length < len(compressed_permuted) and
        string_length < len(compressed)
    ):
        return original_string
    if len(compressed_permuted) < len(compressed):
        return "”" + compressed_permuted + "”"
    else:
        return "“" + compressed + "”"


def CompressPermutations(string):
    numeric = lowercase = uppercase = whitespace = symbol = 0
    for character in string:
        if character >= "0" and character <= "9":
            numeric -= .1
        elif character >= "a" and character <= "z":
            lowercase -= 0.03846
        elif character >= "A" and character <= "Z":
            uppercase -= 0.03846
        elif character == "\n" or character == " ":
            whitespace -= .5
        else:
            symbol -= .03125
    result = "".join(map(lambda t: t[1], sorted([
        (whitespace, "w"), (symbol, "s"), (lowercase, "l"), (numeric, "n"),
        (uppercase, "u")
    ])))
    index, base = 0, 5
    charset = "".join(
        charset_fragment_lookup[character] for character in result
    )
    for character in default_order[:-1]:
        index = index * base + result.index(character)
        result = result.replace(character, "", 1)
        base -= 1
    return Codepage[index] + Compress([
        charset.index(character) for character in string
    ])


def CompressString(string):
    return Compress([
        default_charset.index(character) for character in string
    ])


def Compress(ordinals):
    base, result, number = max(ordinals) + 1, "", 1
    if base == 1:
        number = len(ordinals)
    else:
        for ordinal in ordinals:
            number = number * base + ordinal
    while number:
        result = Codepage[number % 255] + result
        number //= 255
    return Codepage[base - 1] + result


def Decompressed(string):
    if string == "””":
        return ""
    if string[-1] != "”":
        return string
    if string[0] == "”":
        return DecompressPermutations(string[1:-1])
    elif string[0] == "“":
        return DecompressString(string[1:-1])


def DecompressPermutations(string):
    index = OrdinalLookup.get(string[0], ord(string[0]))
    if index > gap:
        index -= 1
    base = 2
    letters = ["u"]
    while index:
        letters.insert(index % base, default_order[5 - base])
        index //= base
        base += 1
    while base <= 5:
        letters.insert(0, default_order[5 - base])
        base += 1
    charset = "".join(
        charset_fragment_lookup[character] for character in letters
    )
    return "".join([
        charset[ordinal] for ordinal in Decompress(string[1:])
    ])


def DecompressString(string):
    return "".join([
        default_charset[ordinal] for ordinal in Decompress(string)
    ])


def Decompress(string):
    number, result = 0, []
    base = OrdinalLookup.get(string[0], ord(string[0])) + 1
    if base > gap:
        base -= 1
    for character in string[1:]:
        ordinal = OrdinalLookup.get(character, ord(character))
        number = (number * 255) + ordinal - (ordinal > gap)
    if base == 1:
        return [ord("\n")] * number
    while number > 1:
        remainder = number % base
        result = [remainder] + result
        number //= base
    return result
