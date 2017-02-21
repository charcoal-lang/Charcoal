# Charcoal

<!-- Some kind of intro text here -->
<!-- Mention that Charcoal uses a lot of non-ASCII characters, and point people to the code page. -->

We'll start with examples in the Charcoal REPL.
To use the REPL, simply run the command `./charcoal.py`, `python charcoal.py` or `python3 charcoal.py`. Note that `./charcoal.py` will not work on Windows. Alternatively, you can run `charcoal.py` from Idle.

## Printing
The central concept in Charcoal is printing strings to a canvas using a cursor. Any expression not preceded by a command is implicitly printed left-to-right. An expression preceded by one of the arrows `←↑→↓↖↗↘↙` is printed in that direction. Each print begins from the location where the previous one left off.

    Charcoal> foo
    foo
    Charcoal> ↘bar
    foob  
        a 
         r

Note that the second and third lines are left-padded with spaces, and the first and second lines are right-padded. You can change the background character to something other than space; more on that later.

After a few REPL commands, the canvas can get crowded. To clear it, hit <kbd>Ctrl</kbd>+<kbd>C</kbd> or use the `⎚` Clear command.

    Charcoal> ^C
    Cleared canvas

Any run of printable ASCII--including space (`0x20`)--is a string literal. Strings can also include `¶`, which represents a newline.

    Charcoal> Hello, World!¶123
    Hello, World!
    123

Since the ASCII digits are used in string literals, integer literals consist of the superscript digits `⁰¹²³⁴⁵⁶⁷⁸⁹`. Printing an integer results in a line, using a character selected from `/\|-` based on the direction of printing.

    Charcoal> ⁷
    -------
    Charcoal> ↙³
    -------/
          / 
         /  

## Basic math
To output a number instead of a line, we need the Cast operator `Ｉ`. This converts strings to numbers and vice versa.

    Charcoal> Ｉ⁴
    4

Arithmetic behaves mostly as expected, though the symbols are different: `⁺⁻×÷` and `Ｘ` for exponentiation. Division rounds down to the nearest integer.

All operators are prefix. This sometimes creates the need to use the separator `¦` between operands to prevent them from being parsed as a single literal.

    Charcoal> Ｉ⁺⁴¦⁴
    8
    Charcoal> ,Ｉ⁻⁴¦⁴
    8,0
    Charcoal> ,Ｉ×⁴¦⁴
    8,0,16
    Charcoal> ^C
    Cleared canvas
    Charcoal> Ｉ÷⁶¦⁴
    1
    Charcoal> ,ＩＸ³¦³
    1,27

<!-- section on string overloads of arithmetic operators -->

## Variables

A variable in Charcoal is any Greek lowercase letter from `αβγδεζηθικλμνξπρσςτυφχψω`. (Omicron was omitted because it looks too much like `o`.) You can assign values to them using the `Ａ` command:

    Charcoal> Ａ⁵β
    
    Charcoal> ×$β
    $$$$$

## Input

There are two ways to take input -- to store it as a variable, and to use it directly.

If there is no variable after the command, it is treated as an operator with no arguments, returning the next input:

    Charcoal> Ｎ
    Input number: 5
    -----

If there is a variable, input is instead stored in the variable, and nothing is returned.
    
    Charcoal> Ｎβ
    Input number: 3
    Charcoal> β
    ---

<!-- Only cover user input here. Talk about acceptable input formats. Talk about Ｎ and Ｓ, both in their command and expression usages. -->

## Control flow

`¿` is the `if` command. It is followed by an expression (we shall call this `x`), and two bodies `y` and `z`, which are either an expression or multiple expressions surrounded by the double angle brackets `«»`. `y` gets executed if `x` evaluates to a truthy value, else `y` gets executed.

    Charcoal> ¿⁰foo¦bar
    foo
    Charcoal> ¿a«←ab»cd
    foba

`Ｆ` is the `for` command. It is followed by an expression `x` and a body `y`. If `x` is a number, it is converted to a range from `0` to `x`, excluding `x` itself. Then, `x` is iterated over, `y` being run once for each element in `x`, the element being stored in the first free variable in `ικλμνξπρςστυφχψωαβγδεζηθ`.

    Charcoal> Ｆ²⁴na¦batman
    nanananananananananananananananananananananananabatman
    Charcoal> ^C
    Cleared canvas
    Charcoal> ＦHello, World!×²ι
    HHeelllloo,,  WWoorrlldd!!

`Ｗ` is the `while` command. It is followed by an expression `x` and a body `y`. While `x` evaluates to truthy, `y` is run, the value of `x` being stored in `ικλμνξπρςστυφχψωαβγδεζηθ`.

    Charcoal>Ａ¹⁰βＷβ«⁺ι Ａ⁻β¹β»
    10 9 8 7 6 5 4 3 2 1 

`ＨＦ` is `RefreshFor` - the same as `for` but with a numeric delay in milliseconds before `x`.

Similarly, `ＨＷ` is `RefreshFor` - the same as `while` but with a numeric delay in milliseconds before `x`.

Finally we have `⎇`, the ternary operator. This accepts three expressions `x`, `y` and `z`, returning `y` if `x` evaluates to true else `z`.

    Charcoal> ×²⎇¹b²
    bb

## More output commands

Multiprint (`Ｐ`) acts the same as print except that it accepts a multidirection instead of a directions, which is either a list of directions multidirections (`+X*|-\/<>^KLTVY7¬`).

Below is a list of directions and the directions they expand to:

|Symbol|Directions|
|-|-|
|`+`|Right, Down, Left, Up|
|`X`|Up Right, Down Right, Down Left, Up Left|
|`*`|Right, Down Right, Down, Down Left, Left, Up Left, Up, Up Right|
|`|`|Up, Down|
|`-`|Left, Right|
|`\`|Up Left, Down Right|
|`/`|Up Right, Down Left|
|`<`|Up Right, Down Right|
|`>`|Down Left, Up Left|
|`^`|Down Right, Down Left|
|`K`|Up, Up Right, Down Right, Down|
|`L`|Up, Right|
|`T`|Right, Down, Left|
|`V`|Up Left, Up Right|
|`Y`|Up Left, Up Right, Down|
|`7`|Down Left, Left|
|`¬`|Down, Left|

The general rule is the directions start from Right, and continue clockwise. The exceptions to this are `V` and `Y`.

    Charcoal> Ｐ*abc
    c c c
     bbb 
    cbabc
     bbb 
    c c c

Rectangle (`ＵＲ`) creates a rectangle with the specified width and height, using `|` and `-` as edges and `+` as corners.

    Charcoal> ＵＲ⁵¦⁵
    +---+
    |   |
    |   |
    |   |
    +---+

Box (`Ｂ`) creates a rectangle with the specified width and height, and using the specified characters as the edge, starting from the top edge. 

    Charcoal> Ｂ⁵¦⁵¦abc
    abcab
    a   c
    c   a
    b   b
    acbac

Polygon (`Ｇ`) accepts a list of sides, which are alternating numbers and directions
<!-- Polygon -->

## Other operators

<!-- Or should this just be a link to the Operators wiki page? -->
<!-- Probably? There are quite a few of them-->

## Other data types

<!-- List, dictionary -->

## Cursor movement

<!-- Move, Pivot, Jump -->

## Canvas operations

<!-- Reflect, Rotate (& versions w/ copy and overlap), SetBackground -->

## Output control and animation

<!-- Dump, Refresh, RefreshFor, RefreshWhile -->

# README
<!-- TODO: make this better -->
Want to be able to write basic Charcoal quickly? Then read on. If you came here looking for help, scroll to the bottom for the FAQ.

## Example REPL session

To use the REPL, simply invoke with `./charcoal.py`, `python charcoal.py` or `python3 charcoal.py`.

    Charcoal> Hello, World!
    Hello, World!
    Charcoal> ^C
    Cleared canvas

## Literals
There are two basic types of literals: strings and numbers. A string is just a run of printable ASCII, and a number is just a run of the superscript digits `⁰¹²³⁴⁵⁶⁷⁸⁹`.

Examples:
`foo` is equivalent to `"foo"`
`foo¶bar` is the same as `"foo\nbar"`.
`¹²³⁴` is `1234`.

## Printing
In a Charcoal program, expressions are implicitly printed. Numbers print a line, and arrows can be used to specify a direction.

Examples:
`foo` prints `foo`
`foo⁴` prints `foo----`
`foo↖⁴` prints:
```
\   
 \  
  \ 
foo\
```

## FAQ
- When I run Charcoal it throws some errors about UTF-8 characters and exits.
	- Maybe you don't have Python 3 installed. Try installing Python 3 from [here](https://www.python.org/downloads/windows/).
- When I run Charcoal it throws some errors and exits.
	- If the message comes with a stack trace, it looks like you have found a bug. File a bug report [here](https://github.com/somebody1234/Charcoal/issues), and we'll come back to you as soon as we can.

<!-- TODO: set up issue template -->
