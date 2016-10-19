from unicodelookup import OrdinalLookup, Codepage
from string import ascii_lowercase, ascii_uppercase, digits
import re

# TODO: reserve chars for string start and end

digits += "."
symbols = "!\"#$%&'()*+,-/:;<=>?@[\]^_`{|}~"
whitespace = "\n "
default_order = "wslnu"
charset_fragment_lookup = {
    "w": whitespace,
    "s": symbols,
    "l": ascii_lowercase,
    "n": digits,
    "u": ascii_uppercase
}
default_charset = (
    whitespace +
    symbols +
    ascii_lowercase +
    digits +
    ascii_uppercase
)
Codepage.remove("\"")
gap = ord("\"")
# TODO: finish codepage so I can do OrdinalLookup[whatever]

def Compressed(string):

    if not all(
        character == "¶" or character > " " and character < "~"
        for character in string
    ):
        return string

    original_string = string

    string = re.sub("¶", "\n", string)

    compressed_permutated = CompressPermutations(string)
    compressed = CompressString(string)

    string_length = len(original_string) - 2

    if (
        string_length < len(compressed_permutated) and
        string_length < len(compressed)
    ):
        return original_string

    if len(compressed_permutated) < len(compressed):
        return "”" + compressed_permutated + "”"

    else:
        return "“" + compressed + "”"

def CompressPermutations(string):
    numeric = lowercase = uppercase = whitespace = symbol = 0

    for character in string:

        if character >= "0" and character <= "9" or character == ".":
            numeric -= 1

        elif character >= "a" and character <= "z":
            lowercase -= 1

        elif character >= "A" and character <= "Z":
            uppercase -= 1

        elif character == "\n" or character == " ":
            whitespace -= 1

        else:
            symbol -= 1

    result = "".join(map(lambda t: t[1], sorted([
        (whitespace, "w"),
        (symbol, "s"),
        (lowercase, "l"),
        (numeric, "n"),
        (uppercase, "u")
    ])))
    order = default_order[:]
    index = 0
    base = 5
    charset = "".join(
        charset_fragment_lookup[character]
        for character in result
    )

    for character in default_order[:-1]:
        index = index * base + result.index(character)
        result = result.replace(character, "", 1)
        base -= 1

    return Codepage[index] + Compress([
        charset.index(character)
        for character in string
    ])

def CompressString(string):
    return Compress([
        default_charset.index(character)
        for character in string
    ])

def Compress(ordinals):
    base = max(ordinals) + 1

    result = ""
    number = ordinals[0] + 1

    if base == 1:
        number = len(ordinals)

    else:

        for ordinal in ordinals[1:]:
            number = number * base + ordinal

    while number:
        result = Codepage[number % 255] + result
        number //= 255

    return Codepage[base - 1] + result

def Decompressed(string):

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

    charset = "".join(
        charset_fragment_lookup[character] for character in letters
    )

    return "".join([
        charset[ordinal]
        for ordinal in Decompress(string[1:])
    ])

def DecompressString(string):
    return "".join([
        default_charset[ordinal]
        for ordinal in Decompress(string)
    ])

def Decompress(string):
    number = 0
    result = []
    base = OrdinalLookup.get(string[0], ord(string[0])) + 1
    if base > gap:
        base -= 1

    for character in string[1:]:
        ordinal = OrdinalLookup.get(character, ord(character))
        number = (number * 255) + ordinal - (ordinal > gap)

    if base == 1:
        return "\n" * number

    base_plus_1 = base + 1

    while number > base_plus_1:
        remainder = number % base
        result = [remainder] + result
        number //= base

    return [number - 1] + result
