from direction import Direction, Pivot
from charcoaltoken import CharcoalToken
from unicodegrammars import UnicodeGrammars

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

    CharcoalToken.List: [
        lambda result: lambda charcoal: result[1](charcoal)
    ],
    CharcoalToken.ArrowList: [
        lambda result: result[1]
    ],

    CharcoalToken.Expression: [
        lambda result: lambda charcoal: result[0],
        lambda result: lambda charcoal: result[0],
        lambda result: lambda charcoal: charcoal.scope[result[0]],
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
        lambda result: lambda charcoal: charcoal.Random()
    ],
    CharcoalToken.Unary: [
        lambda result: lambda item, charcoal: -item,
        lambda result: lambda item, charcoal: len(item),
        lambda result: lambda item, charcoal: int(not item),
        lambda result: lambda item, charcoal: charcoal.Cast(item),
        lambda result: lambda item, charcoal: charcoal.Random(item),
        lambda result: lambda item, charcoal: charcoal.Evaluate(item)
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
        lambda result: lambda left, right, charcoal: charcoal.CycleChop(
            left, right
        ),
        lambda result: lambda left, right, charcoal: left ** right,
        lambda result: lambda left, right, charcoal: left[right]
    ],
    CharcoalToken.Ternary: [
    ],
    CharcoalToken.LazyUnary: [
    ],
    CharcoalToken.LazyBinary: [
        lambda result: lambda left, right, charcoal: int(
            left(charcoal) and right(charcoal)
        ),
        lambda result: lambda left, right, charcoal: int(
            left(charcoal) or right(charcoal)
        )
    ],
    CharcoalToken.LazyTernary: [
        lambda result: lambda first, second, third, charcoal: charcoal.Ternary(
            first, second, third
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
            result[1](charcoal),
            directions={Direction.right}
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
        lambda result: lambda charcoal: charcoal.ReflectTransform(result[1]),
        lambda result: lambda charcoal: charcoal.ReflectMirror(result[1]),
        lambda result: lambda charcoal: charcoal.ReflectMirror(result[1]),
        lambda result: lambda charcoal: charcoal.RotateCopy(
            result[1](charcoal),
            result[2]
        ),
        lambda result: lambda charcoal: charcoal.RotateCopy(
            result[1](charcoal)
        ),
        lambda result: lambda charcoal: charcoal.ReflectCopy(result[1]),
        lambda result: lambda charcoal: charcoal.ReflectCopy(result[1]),
        lambda result: lambda charcoal: charcoal.RotateOverlap(
            result[1](charcoal)
        ),
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
            result[2],
            result[1](charcoal)
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
        lambda result: lambda charcoal: charcoal.Crop(
            result[1](charcoal),
            result[2](charcoal)
        ),
        lambda result: lambda charcoal: charcoal.Clear(),
        lambda result: lambda charcoal: charcoal.Extend(
            result[1](charcoal),
            result[2](charcoal)
        ),
        lambda result: lambda charcoal: charcoal.Extend(result[1](charcoal))
    ]
}
