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
        lambda result: [ Direction.right, Direction.down, Direction.left, directio.up ] + result[1],
        lambda result: [ Direction.up_right, Direction.down_right, Direction.down_left, Direction.up_left ] + result[1],
        lambda result: [ Direction.right, Direction.down_right, Direction.down, Direction.down_left, Direction.left, Direction.up_left, Direction.up, Direction.up_right ] + result[1],
        lambda result: [ result[0] ] + result[1]
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
        lambda result: None
    ],

    CharcoalToken.Arrows: [
        lambda result: [ result[0] ] + result[1],
        lambda result: [ result[0] ]
    ],
    CharcoalToken.Sides: [
        lambda result: lambda charcoal: [ result[0](charcoal) ] + result[1](charcoal),
        lambda result: lambda charcoal: [ result[0](charcoal) ]
    ],
    CharcoalToken.Expressions: [
        lambda result: lambda charcoal: [ result[0](charcoal) ] + result[2](charcoal),
        lambda result: lambda charcoal: [ result[0](charcoal) ]
    ],

    CharcoalToken.List: [
        lambda result: lambda charcoal: result[1](charcoal)
    ],

    CharcoalToken.Expression: [
        lambda result: lambda charcoal: result[0],
        lambda result: lambda charcoal: result[0],
        lambda result: lambda charcoal: charcoal.scope[result[0]],
        lambda result: lambda charcoal: result[1](charcoal),
        lambda result: lambda charcoal: result[0](result[1](charcoal), result[2](charcoal), charcoal),
        lambda result: lambda charcoal: result[0](result[1](charcoal), charcoal),
        lambda result: lambda charcoal: result[0](charcoal)
    ],
    CharcoalToken.Niladic: [
        lambda result: lambda charcoal: charcoal.InputString(),
        lambda result: lambda charcoal: charcoal.InputNumber(),
        lambda result: lambda charcoal: charcoal.Random()
    ],
    CharcoalToken.Monadic: [
        lambda result: lambda item, charcoal: -item,
        lambda result: lambda item, charcoal: len(item),
        lambda result: lambda item, charcoal: int(not item),
        lambda result: lambda item, charcoal: charcoal.Cast(item),
        lambda result: lambda item, charcoal: charcoal.Random(item),
        lambda result: lambda item, charcoal: Parse(result[1](charcoal), processor=InterpreterProcessor)(charcoal)
    ],
    CharcoalToken.Dyadic: [
        lambda result: lambda left, right, charcoal: (str(left) + str(right)) if isinstance(left, str) or isinstance(right, str) else (left + right),
        lambda result: lambda left, right, charcoal: left - right,
        lambda result: lambda left, right, charcoal: left * right,
        lambda result: lambda left, right, charcoal: int(left / right),
        lambda result: lambda left, right, charcoal: left % right,
        lambda result: lambda left, right, charcoal: left == right,
        lambda result: lambda left, right, charcoal: left < right,
        lambda result: lambda left, right, charcoal: left > right,
        lambda result: lambda left, right, charcoal: int(left and right),
        lambda result: lambda left, right, charcoal: int(left or right)
    ],

    CharcoalToken.Program: [
        lambda result: lambda charcoal: (result[0](charcoal) or True) and result[1](charcoal),
        lambda result: lambda charcoal: None
    ],
    CharcoalToken.Command: [ lambda result: lambda charcoal: result[0](charcoal) ] * len(UnicodeGrammars[CharcoalToken.Command]),
    CharcoalToken.Body: [
        lambda result: lambda charcoal: result[1](charcoal),
        lambda result: lambda charcoal: result[0](charcoal)
    ],
    CharcoalToken.Print: [
        lambda result: lambda charcoal: charcoal.Print(result[1](charcoal), directions={result[0]}),
        lambda result: lambda charcoal: charcoal.Print(result[0](charcoal))
    ],
    CharcoalToken.Multiprint: [
        lambda result: lambda charcoal: charcoal.Multiprint(result[2](charcoal), directions=set(result[1])),
        lambda result: lambda charcoal: charcoal.Multiprint(result[1](charcoal), directions={Direction.right})
    ],
    CharcoalToken.Box: [
        lambda result: lambda charcoal: charcoal.Rectangle(result[1](charcoal), result[2](charcoal), result[3](charcoal))
    ],
    CharcoalToken.Rectangle: [
        lambda result: lambda charcoal: charcoal.Rectangle(result[1](charcoal), result[2](charcoal))
    ],
    CharcoalToken.Polygon: [
        lambda result: lambda charcoal: charcoal.Polygon(result[1](charcoal), result[2](charcoal)),
        lambda result: lambda charcoal: charcoal.Polygon([[(side, length) for side in result[1]] for length in [ result[2](charcoal)]][0], result[3](charcoal))
    ],
    CharcoalToken.Move: [
        lambda result: lambda charcoal: charcoal.Move(result[0]),
        lambda result: lambda charcoal: charcoal.Move(result[1]),
        lambda result: lambda charcoal: charcoal.Move(result[2], result[1](charcoal))
    ],
    CharcoalToken.Pivot: [
        lambda result: lambda charcoal: charcoal.Pivot(Pivot.left, result[1](charcoal)),
        lambda result: lambda charcoal: charcoal.Pivot(Pivot.left),
        lambda result: lambda charcoal: charcoal.Pivot(Pivot.right, result[1](charcoal)),
        lambda result: lambda charcoal: charcoal.Pivot(Pivot.right)
    ],
    CharcoalToken.Jump: [
        lambda result: lambda charcoal: charcoal.Jump(result[1](charcoal), result[2](charcoal))
    ],
    CharcoalToken.Rotate: [
        lambda result: lambda charcoal: charcoal.Rotate(result[1](charcoal))
    ],
    CharcoalToken.Reflect: [
        lambda result: lambda charcoal: charcoal.Reflect(result[1])
    ],
    CharcoalToken.Copy: [
        lambda result: lambda charcoal: charcoal.Copy(result[1](charcoal), result[2](charcoal))
    ],
    CharcoalToken.For: [
        lambda result: lambda charcoal: charcoal.For(result[1], result[2])
    ],
    CharcoalToken.While: [
        lambda result: lambda charcoal: charcoal.While(result[1], result[2])
    ],
    CharcoalToken.If: [
        lambda result: lambda charcoal: charcoal.If(result[1], result[2], result[3])
    ],
    CharcoalToken.Assign: [
        lambda result: lambda charcoal: charcoal.Assign(result[1], result[2](charcoal))
    ],
    CharcoalToken.Fill: [
        lambda result: lambda charcoal: charcoal.Fill(result[1](charcoal))
    ],
    CharcoalToken.SetBackground: [
        lambda result: lambda charcoal: charcoal.SetBackground(result[1](charcoal))
    ],
    CharcoalToken.Dump: [
        lambda result: lambda charcoal: charcoal.Dump()
    ],
    CharcoalToken.RefreshFor: [
        lambda result: lambda charcoal: charcoal.RefreshFor(result[1](charcoal), result[2], result[3])
    ],
    CharcoalToken.RefreshWhile: [
        lambda result: lambda charcoal: charcoal.RefreshWhile(result[1](charcoal), result[2], result[3])
    ],
    CharcoalToken.Refresh: [
        lambda result: lambda charcoal: charcoal.Refresh(result[1](charcoal)),
        lambda result: lambda charcoal: charcoal.Refresh()
    ],
    CharcoalToken.InputString: [
        lambda result: lambda charcoal: charcoal.InputString(result[1])
    ],
    CharcoalToken.InputNumber: [
        lambda result: lambda charcoal: charcoal.InputNumber(result[1])
    ]
}