from direction import Direction, Pivot
from charcoaltoken import CharcoalToken
from unicodegrammars import UnicodeGrammars

def FindAll(haystack, needle):
    result = []

    if isinstance(haystack, str):
        index = haystack.find(needle)

        while True:

            if index != -1:
                result += [index]

            else:
                return result

            index = haystack.find(needle, index + 1)

    else:

        try:
            index = haystack.index(needle)

        except:
            return []

        while True:

            result += [index]

            try:
                index = haystack.index(needle, index + 1)

            except:
                return result

def ListFind(haystack, needle):

    try:
        return haystack.index(needle)

    except:
        return -1

InterpreterProcessor = {
    CharcoalToken.Arrow: [
        lambda result: Direction.left,
        lambda result: Direction.up,
        lambda result: Direction.right,
        lambda result: Direction.down,
        lambda result: Direction.up_left,
        lambda result: Direction.up_right,
        lambda result: Direction.down_right,
        lambda result: Direction.down_left
    ],
    CharcoalToken.Multidirectional: [
        lambda result: result[0],
        lambda result: [
            Direction.right,
            Direction.down,
            Direction.left,
            Direction.up
        ] + result[1],
        lambda result: [
            Direction.up_right,
            Direction.down_right,
            Direction.down_left,
            Direction.up_left
        ] + result[1],
        lambda result: [
            Direction.right,
            Direction.down_right,
            Direction.down,
            Direction.down_left,
            Direction.left,
            Direction.up_left,
            Direction.up,
            Direction.up_right
        ] + result[1],
        lambda result: [
            Direction.up,
            Direction.down
        ] + result[1],
        lambda result: [
            Direction.left,
            Direction.right
        ] + result[1],
        lambda result: [
            Direction.up_left,
            Direction.down_right
        ] + result[1],
        lambda result: [
            Direction.up_right,
            Direction.down_left
        ] + result[1],
        lambda result: [
            Direction.up_right,
            Direction.down_right
        ] + result[1],
        lambda result: [
            Direction.down_left,
            Direction.up_left
        ] + result[1],
        lambda result: [
            Direction.down_right,
            Direction.down_left
        ] + result[1],
        lambda result: [
            Direction.up,
            Direction.up_right,
            Direction.down_right,
            Direction.down
        ] + result[1],
        lambda result: [
            Direction.up,
            Direction.right
        ] + result[1],
        lambda result: [
            Direction.right,
            Direction.down,
            Direction.left
        ] + result[1],
        lambda result: [
            Direction.up_left,
            Direction.up_right
        ] + result[1],
        lambda result: [
            Direction.up_left,
            Direction.up_right,
            Direction.down
        ] + result[1],
        lambda result: [
            Direction.down_left,
            Direction.left
        ] + result[1],
        lambda result: [
            Direction.down,
            Direction.left
        ] + result[1],
        lambda result: []
    ],
    CharcoalToken.Side: [
        lambda result: lambda charcoal: (result[0], result[1](charcoal))
    ],
    CharcoalToken.String: [
        lambda result: result
    ],
    CharcoalToken.Number: [
        lambda result: result
    ],
    CharcoalToken.Name: [
        lambda result: result
    ],
    CharcoalToken.Separator: [
        lambda result: None,
        lambda result: None
    ],

    CharcoalToken.Arrows: [
        lambda result: [result[0]] + result[1],
        lambda result: result
    ],
    CharcoalToken.Sides: [
        lambda result: lambda charcoal: [
            result[0](charcoal)
        ] + result[1](charcoal),
        lambda result: lambda charcoal: [result[0](charcoal)]
    ],
    CharcoalToken.Expressions: [
        lambda result: lambda charcoal: [
            result[0](charcoal)
        ] + result[1](charcoal),
        lambda result: lambda charcoal: [result[0](charcoal)]
    ],
    CharcoalToken.PairExpressions: [
        lambda result: lambda charcoal: [
            (
                result[0](charcoal),
                result[1](charcoal)
            )
        ] + result[2](charcoal),
        lambda result: lambda charcoal: [
            (
                result[0](charcoal),
                result[1](charcoal)
            )
        ]
    ],
    CharcoalToken.Cases: [
        lambda result: lambda charcoal: [[
            result[0](charcoal),
            result[1]
        ]] + result[2](charcoal),
        lambda result: lambda charcoal: []
    ],

    CharcoalToken.List: [
        lambda result: lambda charcoal: result[1](charcoal),
        lambda result: lambda charcoal: []
    ],
    CharcoalToken.ArrowList: [
        lambda result: result[1],
        lambda result: []
    ],
    CharcoalToken.Dictionary: [
        lambda result: lambda charcoal: dict(result[1](charcoal)),
        lambda result: lambda charcoal: {}
    ],

    CharcoalToken.Expression: [
        lambda result: lambda charcoal: result[0],
        lambda result: lambda charcoal: result[0],
        lambda result: lambda charcoal: (
            charcoal.scope[result[0]] if
            result[0] in charcoal.scope else
            charcoal.hidden[result[0]] if
            result[0] in charcoal.hidden else
            None
        ),
        lambda result: lambda charcoal: result[0](charcoal),
        lambda result: lambda charcoal: result[0](charcoal),
        lambda result: lambda charcoal: result[0](charcoal),
        lambda result: lambda charcoal: result[0](
            result[1],
            result[2],
            result[3],
            charcoal
        ),
        lambda result: lambda charcoal: result[0](
            result[1](charcoal),
            result[2](charcoal),
            result[3](charcoal),
            charcoal
        ),
        lambda result: lambda charcoal: result[0](
            result[1],
            result[2],
            charcoal
        ),
        lambda result: lambda charcoal: result[0](
            result[1](charcoal),
            result[2](charcoal),
            charcoal
        ),
        lambda result: lambda charcoal: result[0](
            result[1],
            charcoal
        ),
        lambda result: lambda charcoal: result[0](
            result[1](charcoal),
            charcoal
        ),
        lambda result: lambda charcoal: result[0](charcoal)
    ],
    CharcoalToken.Nilary: [
        lambda result: lambda charcoal: charcoal.InputString(),
        lambda result: lambda charcoal: charcoal.InputNumber(),
        lambda result: lambda charcoal: charcoal.Random(),
        lambda result: lambda charcoal: charcoal.PeekAll(),
        lambda result: lambda charcoal: charcoal.PeekMoore(),
        lambda result: lambda charcoal: charcoal.PeekVonNeumann(),
        lambda result: lambda charcoal: charcoal.Peek()
    ],
    CharcoalToken.Unary: [
        lambda result: lambda item, charcoal: -item,
        lambda result: lambda item, charcoal: len(item),
        lambda result: lambda item, charcoal: not item,
        lambda result: lambda item, charcoal: charcoal.Cast(item),
        lambda result: lambda item, charcoal: charcoal.Random(item),
        lambda result: lambda item, charcoal: charcoal.Evaluate(item),
        lambda result: lambda item, charcoal: item.pop(),
        lambda result: lambda item, charcoal: item.lower(),
        lambda result: lambda item, charcoal: item.upper(),
        lambda result: lambda item, charcoal: min(item),
        lambda result: lambda item, charcoal: max(item),
        lambda result: lambda item, charcoal: (
            chr(item) if isinstance(item, int) else ord(item)
        ),
        lambda result: lambda item, charcoal: item[::-1]
    ],
    CharcoalToken.Binary: [
        lambda result: lambda left, right, charcoal: (
            (left + [right]) if
            isinstance(left, list) and not isinstance(right, list) else
            ([left] + right) if
            not isinstance(left, list) and isinstance(right, list) else
            (str(left) + str(right)) if
            isinstance(left, str) or isinstance(right, str) else
            (left + right)
        ),
        lambda result: lambda left, right, charcoal: left - right,
        lambda result: lambda left, right, charcoal: left * right,
        lambda result: lambda left, right, charcoal: (
            (left[:int(len(left) / right)]) if
            isinstance(left, str) or isinstance(left, list) else
            int(left / right)
        ),
        lambda result: lambda left, right, charcoal: left % right,
        lambda result: lambda left, right, charcoal: left == right,
        lambda result: lambda left, right, charcoal: left < right,
        lambda result: lambda left, right, charcoal: left > right,
        lambda result: lambda left, right, charcoal: (
            list(range(left, right + 1))
            if isinstance(left, int) else
            list(map(chr, range(ord(left), ord(right) + 1)))
        ),
        lambda result: lambda left, right, charcoal: (
            list(range(left, right))
            if isinstance(left, int) else
            list(map(chr, range(ord(left), ord(right))))
            if isinstance(left, str) and isinstance(right, str) else
            charcoal.CycleChop(left, right)
        ),
        lambda result: lambda left, right, charcoal: left ** right,
        lambda result: lambda left, right, charcoal: (
            (
                lambda value: "" if value == "\x00" else value
            )(
                left[right] if
                isinstance(left, dict) else
                left[right % len(left)]
            )
        ) if (
            (not isinstance(left, dict)) or right in left
        ) else None,
        lambda result: lambda left, right, charcoal: (
            left.append(right) or left
        ),
        lambda result: lambda left, right, charcoal: right.join(left),
        lambda result: lambda left, right, charcoal: left.split(right),
        lambda result: lambda left, right, charcoal: FindAll(left, right),
        lambda result: lambda left, right, charcoal: (
            left.find(right)
            if isinstance(left, str) else
            ListFind(left, right)
        ),
        lambda result: lambda left, right, charcoal: (
            " " * (right - len(left)) + left
        ),
        lambda result: lambda left, right, charcoal: (
            left + " " * (right - len(left))
        ),
        lambda result: lambda left, right, charcoal: left.count(right)
    ],
    CharcoalToken.Ternary: [
    ],
    CharcoalToken.LazyUnary: [
    ],
    CharcoalToken.LazyBinary: [
        lambda result: lambda left, right, charcoal: (
            left(charcoal) and right(charcoal)
        ),
        lambda result: lambda left, right, charcoal: (
            left(charcoal) or right(charcoal)
        )
    ],
    CharcoalToken.LazyTernary: [
        lambda result: lambda first, second, third, charcoal: charcoal.Ternary(
            first, second, third
        )
    ],
    CharcoalToken.OtherOperator: [
        lambda result: lambda charcoal: charcoal.PeekDirection(
            result[1](charcoal),
            result[2]
        ),
        lambda result: lambda charcoal: charcoal.Map(
            result[1](charcoal),
            result[2]
        )
    ],

    CharcoalToken.Program: [
        lambda result: lambda charcoal: (
            (result[0](charcoal) or True) and
            result[1](charcoal)
        ),
        lambda result: lambda charcoal: None
    ],
    CharcoalToken.Body: [
        lambda result: lambda charcoal: result[1](charcoal),
        lambda result: lambda charcoal: result[0](charcoal)
    ],
    CharcoalToken.Command: [
        lambda result: lambda charcoal: charcoal.InputString(result[1]),
        lambda result: lambda charcoal: charcoal.InputNumber(result[1]),
        lambda result: lambda charcoal: charcoal.Evaluate(
            result[1](charcoal),
            True
        ),
        lambda result: lambda charcoal: charcoal.Print(
            result[1](charcoal),
            directions={result[0]}
        ),
        lambda result: lambda charcoal: charcoal.Print(result[0](charcoal)),
        lambda result: lambda charcoal: charcoal.Multiprint(
            result[2](charcoal),
            directions=set(result[1])
        ),
        lambda result: lambda charcoal: charcoal.Multiprint(
            result[1](charcoal)
        ),
        lambda result: lambda charcoal: charcoal.Polygon(
            result[1](charcoal),
            result[2](charcoal)
        ),
        lambda result: lambda charcoal: charcoal.Polygon(
            [
                [(side, length) for side in result[1]]
                for length in [result[2](charcoal)]
            ][0], result[3](charcoal)
        ),
        lambda result: lambda charcoal: charcoal.Polygon(
            result[1](charcoal),
            result[2](charcoal),
            fill=False
        ),
        lambda result: lambda charcoal: charcoal.Polygon(
            [
                [(side, length) for side in result[1]]
                for length in [result[2](charcoal)]
            ][0], result[3](charcoal),
            fill=False
        ),
        lambda result: lambda charcoal: charcoal.Rectangle(
            result[1](charcoal),
            result[2](charcoal)
        ),
        lambda result: lambda charcoal: charcoal.Oblong(
            result[1](charcoal),
            result[2](charcoal),
            result[3](charcoal)
        ),
        lambda result: lambda charcoal: charcoal.Rectangle(
            result[1](charcoal),
            result[2](charcoal),
            result[3](charcoal)
        ),
        lambda result: lambda charcoal: charcoal.Move(result[0]),
        lambda result: lambda charcoal: charcoal.Move(result[1]),
        lambda result: lambda charcoal: charcoal.Move(
            result[2],
            result[1](charcoal)
        ),
        lambda result: lambda charcoal: charcoal.Pivot(
            Pivot.left,
            result[1](charcoal)
        ),
        lambda result: lambda charcoal: charcoal.Pivot(Pivot.left),
        lambda result: lambda charcoal: charcoal.Pivot(
            Pivot.right,
            result[1](charcoal)
        ),
        lambda result: lambda charcoal: charcoal.Pivot(Pivot.right),
        lambda result: lambda charcoal: charcoal.Jump(
            result[1](charcoal),
            result[2](charcoal)
        ),
        lambda result: lambda charcoal: charcoal.RotateTransform(
            result[1](charcoal)
        ),
        lambda result: lambda charcoal: charcoal.ReflectTransform(result[1]),
        lambda result: lambda charcoal: charcoal.RotatePrism(
            result[2],
            result[1],
            number=True
        ),
        lambda result: lambda charcoal: charcoal.RotatePrism(
            result[2](charcoal),
            result[1]
        ),
        lambda result: lambda charcoal: charcoal.RotatePrism(
            result[2](charcoal),
            result[1]
        ),
        lambda result: lambda charcoal: charcoal.RotatePrism(result[1], number=True),
        lambda result: lambda charcoal: charcoal.RotatePrism(result[1](charcoal)),
        lambda result: lambda charcoal: charcoal.RotatePrism(result[1](charcoal)),
        lambda result: lambda charcoal: charcoal.ReflectMirror(result[1]),
        lambda result: lambda charcoal: charcoal.ReflectMirror(result[1]),
        lambda result: lambda charcoal: charcoal.RotateCopy(
            result[2],
            result[1],
            number=True
        ),
        lambda result: lambda charcoal: charcoal.RotateCopy(
            result[2](charcoal),
            result[1]
        ),
        lambda result: lambda charcoal: charcoal.RotateCopy(
            result[2](charcoal),
            result[1]
        ),
        lambda result: lambda charcoal: charcoal.RotateCopy(
            result[1],
            number=True
        ),
        lambda result: lambda charcoal: charcoal.RotateCopy(
            result[1](charcoal)
        ),
        lambda result: lambda charcoal: charcoal.RotateCopy(
            result[1](charcoal)
        ),
        lambda result: lambda charcoal: charcoal.ReflectCopy(result[1]),
        lambda result: lambda charcoal: charcoal.ReflectCopy(result[1]),
        lambda result: lambda charcoal: charcoal.ReflectOverlap(result[1]),
        lambda result: lambda charcoal: charcoal.ReflectOverlap(result[1]),
        lambda result: lambda charcoal: charcoal.Rotate(result[1](charcoal)),
        lambda result: lambda charcoal: charcoal.Reflect(result[1]),
        lambda result: lambda charcoal: charcoal.Copy(
            result[1](charcoal),
            result[2](charcoal)
        ),
        lambda result: lambda charcoal: charcoal.For(result[1], result[2]),
        lambda result: lambda charcoal: charcoal.While(result[1], result[2]),
        lambda result: lambda charcoal: charcoal.If(
            result[1],
            result[2],
            result[3]
        ),
        lambda result: lambda charcoal: charcoal.If(
            result[1],
            result[2],
            lambda result: lambda charcoal: None
        ),
        lambda result: lambda charcoal: charcoal.Assign(
            result[1](charcoal),
            result[2](charcoal),
            result[3](charcoal)
        ),
        lambda result: lambda charcoal: charcoal.Assign(
            result[1](charcoal),
            result[2]
        ),
        lambda result: lambda charcoal: charcoal.Fill(result[1](charcoal)),
        lambda result: lambda charcoal: charcoal.SetBackground(
            result[1](charcoal)
        ),
        lambda result: lambda charcoal: charcoal.Dump(),
        lambda result: lambda charcoal: charcoal.RefreshFor(
            result[1](charcoal),
            result[2],
            result[3]
        ),
        lambda result: lambda charcoal: charcoal.RefreshWhile(
            result[1](charcoal),
            result[2],
            result[3]
        ),
        lambda result: lambda charcoal: charcoal.Refresh(result[1](charcoal)),
        lambda result: lambda charcoal: charcoal.Refresh(),
        lambda result: lambda charcoal: charcoal.ToggleTrim(),
        lambda result: lambda charcoal: charcoal.Crop(
            result[1](charcoal),
            result[2](charcoal)
        ),
        lambda result: lambda charcoal: charcoal.Clear(),
        lambda result: lambda charcoal: charcoal.Extend(
            result[1](charcoal),
            result[2](charcoal)
        ),
        lambda result: lambda charcoal: charcoal.Extend(result[1](charcoal)),
        lambda result: lambda charcoal: (
            result[1](charcoal).append(result[2](charcoal))
        ),
        lambda result: lambda charcoal: dict(result[2](charcoal)).get(
            result[1](charcoal),
            result[3]
        )(charcoal),
        lambda result: lambda charcoal: charcoal.Map(
            result[1](charcoal),
            result[2]
        )
    ]
}

