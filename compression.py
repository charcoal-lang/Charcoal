from codepage import OrdinalLookup, Codepage, rCommand
from string import ascii_lowercase, ascii_uppercase, digits
import re
import lzma
try:
    import brotli
except:
    print("Please install the 'brotli' module: 'sudo -H pip3 install brotli'")
    __import__("sys").exit()

symbols = ".!\"#$%&'()*+,-/:;<=>?@[\]^_`{|}~\r"
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
RAW_ENCODING = 120
DICTIONARY_ENCODING = 121
CHARSET_ENCODING = 122
RLE_ENCODING = 123
BROTLI_ENCODING = 124
LZMA_ENCODING = 125


def Compressed(string, escape=False):
    """
    Compressed(string) -> str
    Returns the shortest Charcoal compressed literal of the given string.

    """
    if not string:
        return "””"
    if not all(
        character == "¶" or character == "⸿" or
        character >= " " and character <= "~"
        for character in string
    ):
        if not escape:
            return string
        if len(re.findall("[^ -~¶⸿]", string)) > 3:
            return "”" + Codepage[RAW_ENCODING] + string + "”"
        return (
            "´" * (string[0] in "+X*|-\\/<>^KLTVY7¬") +
            rCommand.sub("´\1", string)
        )
    original_string, string = string, re.sub(
        "¶", "\n", re.sub("⸿", "\r", string)
    )
    compressed_charset = CompressCharset(string)
    compressed_rle = CompressRLE(string)
    compressed_brotli = CompressBrotli(string)
    compressed_lzma = CompressLZMA(string)
    compressed_permuted = CompressPermutations(string)
    compressed = CompressString(string)
    string_length = len(original_string) - 2
    minimum_length = min(
        len(compressed_charset), len(compressed_rle), len(compressed_brotli),
        len(compressed_lzma), len(compressed_permuted), len(compressed),
        string_length
    )
    if string_length == minimum_length:
        if not escape:
            return original_string
        if len(re.findall("[^ -~¶⸿]", original_string)) > 3:
            return "”" + Codepage[RAW_ENCODING] + original_string + "”"
        return (
            "´" * (original_string[0] in "+X*|-\\/<>^KLTVY7¬") +
            rCommand.sub("´\1", original_string)
        )
    if len(compressed) == minimum_length:
        return "“" + compressed + "”"
    if len(compressed_permuted) == minimum_length:
        return "”" + compressed_permuted + "”"
    if len(compressed_charset) == minimum_length:
        return "”" + compressed_charset + "”"
    if len(compressed_rle) == minimum_length:
        return "”" + compressed_rle + "”"
    if len(compressed_brotli) == minimum_length:
        return "”" + compressed_brotli + "”"
    return "”" + compressed_lzma + "”"


def CompressCharset(string):
    """
    CompressPermutations(string) -> str
    Returns without delimiters the given string compressed \
using a character set of only the characters in the string.

    """
    occurrences = [0] * 97
    for c in string:
        occurrences[0 if c == "\n" else 1 if c == "\r" else ord(c) - 30] += 1
    items = sorted([i for i, n in enumerate(occurrences) if n])[::-1]
    charset = "".join([chr(n + 30) if n > 1 else "\n\r"[n] for n in items])
    base = len(charset)
    result = ""
    number = 1
    if base == 1:
        number = len(string)
    else:
        for character in string:
            number = number * base + charset.index(character)
    while number:
        result = Codepage[number % 255] + result
        number //= 255
    number = 1
    length = 0
    for character in charset:
        number = number * 97 + default_charset.index(character)
    while number:
        result = Codepage[number % 255] + result
        length += 1
        number //= 255
    return Codepage[CHARSET_ENCODING] + Codepage[length] + result


def CompressRLE(string):
    """
    CompressRLE(string) -> str
    Returns without delimiters the given string compressed \
using run-length encoding.

    """
    number, previous, count = 1, string[0], -1
    for character in string:
        if character != previous or count == 32:
            number = number * 97 + default_charset.index(previous)
            number = number * 32 + count
            count = 0
            previous = character
        else:
            count += 1
    number = number * 97 + default_charset.index(string[-1])
    number = number * 32 + count
    result = ""
    while number:
        result = Codepage[number % 255] + result
        number //= 255
    return Codepage[RLE_ENCODING] + result


def CompressBrotli(string):
    """
    CompressBrotli(string) -> str
    Returns without delimiters the given string compressed \
using Google's brotli compression method.

    """
    compressed = brotli.compress(string.encode("ascii"))
    number = 1
    for c in compressed:
        number = number * 256 + c
    result = ""
    while number:
        result = Codepage[number % 255] + result
        number //= 255
    return Codepage[BROTLI_ENCODING] + result


def CompressLZMA(string):
    """
    CompressBrotli(string) -> str
    Returns without delimiters the given string compressed \
using the lzstring compression method.

    """
    compressed = lzma.compress(
        string.encode("ascii"),
        format=lzma.FORMAT_RAW,
        filters=[{'id': lzma.FILTER_LZMA2, 'preset': 9 | lzma.PRESET_EXTREME}]
    )
    number = 1
    for c in compressed:
        number = number * 256 + c
    result = ""
    while number:
        result = Codepage[number % 255] + result
        number //= 255
    return Codepage[LZMA_ENCODING] + result


def CompressPermutations(string):
    """
    CompressPermutations(string) -> str
    Returns without delimiters the given string compressed \
using a permuted codepage.

    """
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
    """
    CompressString(string) -> str
    Returns without delimiters the given string compressed.

    """
    return Compress([
        default_charset.index(character) for character in string
    ])


def Compress(ordinals):
    """
    Compress(ordinals) -> str
    Returns without delimiters the given string compressed.

    """
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
    """
    Decompressed(string) -> str
    Returns the decompressed form of the given Charcoal string.

    """
    if string == "””":
        return ""
    if string[-1] != "”":
        return string
    if string[0] == "”":
        ordinal = OrdinalLookup.get(string[1], ord(string[1]))
        alphabet_id = ordinal - (ordinal > gap)
        if alphabet_id < 120:
            return DecompressPermutations(string[1:-1])
        return [
            lambda string: string,
            lambda string: "", # TODO
            lambda string: DecompressCharset(string),
            lambda string: DecompressRLE(string),
            lambda string: DecompressBrotli(string),
            lambda string: DecompressLZMA(string)
        ][alphabet_id - 120](string[2:-1])
    elif string[0] == "“":
        return DecompressString(string[1:-1])


def DecompressCharset(string):
    """
    DecompressCharset(string) -> str
    Returns the original form of the given string compressed \
using a given character set, passed without delimiters.

    """
    length = OrdinalLookup.get(string[0], ord(string[0]))
    length += length <= gap
    number = 0
    for character in string[1:length]:
        ordinal = OrdinalLookup.get(character, ord(character))
        number = number * 255 + ordinal - (ordinal > gap)
    charset = ""
    while number > 1:
        charset = default_charset[number % 97] + charset
        number //= 97
    number = 0
    for character in string[length:]:
        ordinal = OrdinalLookup.get(character, ord(character))
        number = number * 255 + ordinal - (ordinal > gap)
    base = len(charset)
    if base == 1:
        return charset[0] * number
    result = ""
    while number > 1:
        result = charset[number % base] + result
        number //= base
    return result


def DecompressRLE(string):
    """
    DecompressRLE(string) -> str
    Returns the original form of the given string compressed \
using run-length encoding, passed without delimiters.

    """
    number = 0
    for character in string:
        ordinal = OrdinalLookup.get(character, ord(character))
        number = number * 255 + ordinal - (ordinal > gap)
    result = ""
    while number > 1:
        count = number % 32
        number //= 32
        result = default_charset[number % 97] * (count + 1) + result
        number //= 97
    return result


def DecompressBrotli(string):
    """
    DecompressBrotli(string) -> str
    Returns the original form of the given string compressed \
using Google's brotli compression method., passed without delimiters.

    """
    number = 0
    for character in string:
        ordinal = OrdinalLookup.get(character, ord(character))
        number = number * 255 + ordinal - (ordinal > gap)
    compressed = []
    while number > 1:
        compressed = [number % 256] + compressed
        number //= 256
    return brotli.decompress(bytes(compressed)).decode("ascii")


def DecompressLZMA(string):
    """
    DecompressBrotli(string) -> str
    Returns the original form of the given string compressed \
using Google's brotli compression method., passed without delimiters.

    """
    number = 0
    for character in string:
        ordinal = OrdinalLookup.get(character, ord(character))
        number = number * 255 + ordinal - (ordinal > gap)
    compressed = []
    while number > 1:
        compressed = [number % 256] + compressed
        number //= 256
    return lzma.decompress(bytes(compressed)).decode("ascii")


def DecompressPermutations(string):
    """
    DecompressPermutations(string) -> str
    Returns the original form of the given string compressed \
using a permuted codepage, passed without delimiters.

    """
    index = OrdinalLookup.get(string[0], ord(string[0]))
    if index > gap:
        index -= 1
    base, letters = 2, ["u"]
    while index:
        letters.insert(index % base, default_order[5 - base])
        index //= base
        base += 1
    while base <= 5:
        letters.insert(0, default_order[5 - base])
        base += 1
    charset = "".join(charset_fragment_lookup[c] for c in letters)
    return "".join([charset[n] for n in Decompress(string[1:])])


def DecompressString(string):
    """
    DecompressString(string) -> str
    Returns the original form of the given string compressed, \
passed without delimiters.

    """
    return "".join([default_charset[n] for n in Decompress(string)])


def Decompress(string):
    """
    Decompress(string) -> list
    Returns the ordinals in the original form of the given string compressed.

    """
    number, result = 0, []
    base = OrdinalLookup.get(string[0], ord(string[0])) + 1
    if base > gap:
        base -= 1
    for character in string[1:]:
        ordinal = OrdinalLookup.get(character, ord(character))
        number = (number * 255) + ordinal - (ordinal > gap)
    if base == 1:
        return [0] * number
    while number > 1:
        remainder = number % base
        result = [remainder] + result
        number //= base
    return result
