# TODO: direction list operator?

from direction import Direction, Pivot
from charcoaltoken import CharcoalToken
from unicodegrammars import UnicodeGrammars
from wolfram import (
    String, Rule, DelayedRule, Span, Repeated, RepeatedNull, PatternTest,
    Number
)
import re


def FindAll(haystack, needle):
    r = []
    if isinstance(haystack, str):
        index = haystack.find(needle)
        while True:
            if ~index:
                r += [index]
            else:
                return r
            index = haystack.find(needle, index + 1)
    else:
        return [i for i, item in enumerate(haystack) if item == needle]


def ListFind(haystack, needle):
    return haystack.index(needle) if needle in haystack else -1


def direction(dir):
    if isinstance(dir, String):
        dir = str(dir)
    cls = type(dir)
    if cls == Direction:
        return dir
    elif cls == int:
        return [
            Direction.right, Direction.up_right, Direction.up,
            Direction.up_left, Direction.left, Direction.down_left,
            Direction.down, Direction.down_right
        ][dir % 8]
    elif cls == str:
        return {
            "r": Direction.right,
            "ri": Direction.right,
            "rig": Direction.right,
            "righ": Direction.right,
            "right": Direction.right,
            "ur": Direction.up_right,
            "upr": Direction.up_right,
            "upri": Direction.up_right,
            "uprig": Direction.up_right,
            "u": Direction.up,
            "up": Direction.up,
            "ul": Direction.up_left,
            "upl": Direction.up_left,
            "uple": Direction.up_left,
            "uplef": Direction.up_left,
            "l": Direction.left,
            "le": Direction.left,
            "lef": Direction.left,
            "left": Direction.left,
            "dl": Direction.down_left,
            "downl": Direction.down_left,
            "d": Direction.down,
            "do": Direction.down,
            "dow": Direction.down,
            "down": Direction.down,
            "dr": Direction.down_right,
            "downr": Direction.down_right
        }[re.sub("[^a-z]", "", dir.lower()[:5])]

InterpreterProcessor = {
    CharcoalToken.Arrow: [
        lambda r: lambda c: Direction.left,
        lambda r: lambda c: Direction.up,
        lambda r: lambda c: Direction.right,
        lambda r: lambda c: Direction.down,
        lambda r: lambda c: Direction.up_left,
        lambda r: lambda c: Direction.up_right,
        lambda r: lambda c: Direction.down_right,
        lambda r: lambda c: Direction.down_left,
        lambda r: lambda c: direction(r[1](c))
    ],
    CharcoalToken.Multidirectional: [
        lambda r: lambda c: r[0](c) + r[1](c),
        lambda r: lambda c: [
            Direction.right, Direction.down, Direction.left, Direction.up
        ] + r[1](c),
        lambda r: lambda c: [
            Direction.up_right, Direction.down_right, Direction.down_left,
            Direction.up_left
        ] + r[1](c),
        lambda r: lambda c: [
            Direction.right, Direction.down_right, Direction.down,
            Direction.down_left, Direction.left, Direction.up_left,
            Direction.up, Direction.up_right
        ] + r[1](c),
        lambda r: lambda c: [Direction.up, Direction.down] + r[1](c),
        lambda r: lambda c: [Direction.left, Direction.right] + r[1](c),
        lambda r: lambda c: [
            Direction.up_left, Direction.down_right
        ] + r[1](c),
        lambda r: lambda c: [
            Direction.up_right, Direction.down_left
        ] + r[1](c),
        lambda r: lambda c: [
            Direction.up_right, Direction.down_right
        ] + r[1](c),
        lambda r: lambda c: [Direction.down_left, Direction.up_left] + r[1](c),
        lambda r: lambda c: [
            Direction.down_right, Direction.down_left
        ] + r[1](c),
        lambda r: lambda c: [
            Direction.up, Direction.up_right, Direction.down_right,
            Direction.down
        ] + r[1](c),
        lambda r: lambda c: [Direction.up, Direction.right] + r[1](c),
        lambda r: lambda c: [
            Direction.right, Direction.down, Direction.left
        ] + r[1](c),
        lambda r: lambda c: [Direction.up_left, Direction.up_right] + r[1](c),
        lambda r: lambda c: [
            Direction.up_left, Direction.up_right, Direction.down
        ] + r[1](c),
        lambda r: lambda c: [Direction.down_left, Direction.left] + r[1](c),
        lambda r: lambda c: [Direction.down, Direction.left] + r[1](c),
        lambda r: lambda c: r[1](c),
        lambda r: lambda c: [direction(item) for item in r[1](c)],
        lambda r: lambda c: []
    ],
    CharcoalToken.Side: [lambda r: lambda c: (r[0](c), r[1](c))],
    CharcoalToken.String: [lambda r: r],
    CharcoalToken.Number: [lambda r: r],
    CharcoalToken.Name: [lambda r: r],
    CharcoalToken.Separator: [lambda r: None] * 2,
    CharcoalToken.Span: [
        lambda r: lambda c: Span(r[0](c), r[2](c), r[4](c)),
        lambda r: lambda c: Span(r[0](c), None, r[3](c)),
        lambda r: lambda c: Span(r[0](c), r[2](c)),
        lambda r: lambda c: Span(r[0](c)),
        lambda r: lambda c: Span(None, r[1](c), r[3](c)),
        lambda r: lambda c: Span(None, r[1](c)),
        lambda r: lambda c: Span(None, None, r[2](c)),
        lambda r: lambda c: Span()
    ],

    CharcoalToken.Arrows: [
        lambda r: lambda c: [r[0](c)] + r[1](c),
        lambda r: lambda c: [r[0](c)]
    ],
    CharcoalToken.Sides: [
        lambda r: lambda c: [r[0](c)] + r[1](c),
        lambda r: lambda c: [r[0](c)]
    ],
    CharcoalToken.Expressions: [
        lambda r: lambda c: [r[0](c)] + r[1](c),
        lambda r: lambda c: [r[0](c)]
    ],
    CharcoalToken.WolframExpressions: [
        lambda r: lambda c: [r[0](c)] + r[1](c),
        lambda r: lambda c: [r[0](c)]
    ],
    CharcoalToken.PairExpressions: [
        lambda r: lambda c: [(r[0](c), r[1](c))] + r[2](c),
        lambda r: lambda c: [(r[0](c), r[1](c))]
    ],
    CharcoalToken.Cases: [
        lambda r: lambda c: [(r[0](c), r[1])] + r[2](c),
        lambda r: lambda c: []
    ],

    CharcoalToken.List: [
        lambda r: lambda c: r[1](c),
        lambda r: lambda c: []
    ],
    CharcoalToken.WolframList: [
        lambda r: lambda c: r[1](c),
        lambda r: lambda c: []
    ],
    CharcoalToken.Dictionary: [
        lambda r: lambda c: dict(r[1](c)),
        lambda r: lambda c: {}
    ],

    CharcoalToken.WolframExpression: [
        lambda r: lambda c: r[0](c),
        lambda r: lambda c: r[0](c)
    ],
    CharcoalToken.Expression: [
        lambda r: lambda c: r[0],
        lambda r: lambda c: r[0],
        lambda r: lambda c: c.Retrieve(r[0]),
        lambda r: lambda c: r[0](c),
        lambda r: lambda c: r[1](c),
        lambda r: lambda c: r[0](c),
        lambda r: lambda c: c.Lambdafy(r[1]),
        lambda r: lambda c: r[0](c),
        lambda r: lambda c: r[0](r[1], r[2], r[3], r[4], c),
        lambda r: lambda c: r[0](r[1](c), r[2](c), r[3](c), r[4](c), c),
        lambda r: lambda c: r[0](r[1], r[2], r[3], c),
        lambda r: lambda c: r[0](r[1](c), r[2](c), r[3](c), c),
        lambda r: lambda c: r[0](r[1], r[2], c),
        lambda r: lambda c: r[0](r[1](c), r[2](c), c),
        lambda r: lambda c: r[0](r[1], c),
        lambda r: lambda c: r[0](r[1](c), c),
        lambda r: lambda c: r[0](c)
    ],
    CharcoalToken.Nilary: [
        lambda r: lambda c: c.InputString(),
        lambda r: lambda c: c.InputNumber(),
        lambda r: lambda c: c.Random(),
        lambda r: lambda c: c.PeekAll(),
        lambda r: lambda c: c.PeekMoore(),
        lambda r: lambda c: c.PeekVonNeumann(),
        lambda r: lambda c: c.Peek(),
        lambda r: lambda c: c.x,
        lambda r: lambda c: c.y
    ],
    CharcoalToken.Unary: [
        lambda r: lambda item, c: (
            item[::-1]
            if hasattr(item, "__iter__") else
            (-item)
            if (
                isinstance(item, int) or isinstance(item, float) or
                isinstance(item, Number)
            ) else
            str(item)[::-1]
        ),
        lambda r: lambda item, c: (
            len(item) if hasattr(item, "__iter__") else len(str(item))
        ),
        lambda r: lambda item, c: not item,
        lambda r: lambda item, c: c.Cast(item),
        lambda r: lambda item, c: c.Random(item),
        lambda r: lambda item, c: c.Evaluate(item),
        lambda r: lambda item, c: item.pop(),
        lambda r: lambda item, c: str(item).lower(),
        lambda r: lambda item, c: str(item).upper(),
        lambda r: lambda item, c: min(item),
        lambda r: lambda item, c: max(item),
        lambda r: lambda item, c: c.ChrOrd(item),
        lambda r: lambda item, c: (
            item[::-1]
            if hasattr(item, "__iter__") else
            int(str(item)[::-1])
            if isinstance(item, int) else
            float(
                ("-" + str(item)[:0:-1])
                if item[-1] == "-" else
                str(item)[::-1]
            )
            if isinstance(item, float) else
            str(item)[::-1]
        ),
        lambda r: lambda item, c: c.Retrieve(item),
        lambda r: lambda item, c: Repeated(item),
        lambda r: lambda item, c: RepeatedNull(item),
        lambda r: lambda item, c: item[:],
        lambda r: lambda item, c: (
            list(range(int(item) + 1))
            if isinstance(item, int) or isinstance(item, float) else
            list(map(chr, range(ord(item) + 1)))
        ),
        lambda r: lambda item, c: (
            list(range(int(item)))
            if isinstance(item, int) or isinstance(item, float) else
            list(map(chr, range(ord(item))))
        ),
        lambda r: lambda item, c: (
            ~item
            if isinstance(item, int) or isinstance(item, float) else
            (~(float(str(item)) if "." in item else int(str(item))))
        ),
        lambda r: lambda item, c: eval(item)
    ],
    CharcoalToken.Binary: [
        lambda r: lambda left, right, c: c.Add(left, right),
        lambda r: lambda left, right, c: c.Subtract(left, right),
        lambda r: lambda left, right, c: c.Multiply(left, right),
        lambda r: lambda left, right, c: c.Divide(left, right),
        lambda r: lambda left, right, c: c.Divide(left, right, False),
        lambda r: lambda left, right, c: left % right,
        lambda r: lambda left, right, c: left == right,
        lambda r: lambda left, right, c: left < right,
        lambda r: lambda left, right, c: left > right,
        lambda r: lambda left, right, c: left & right,
        lambda r: lambda left, right, c: (
            String(left) | String(right)
            if isinstance(left, str) and isinstance(right, str) else
            left | right
        ),
        lambda r: lambda left, right, c: (
            list(range(int(left), int(right) + 1))
            if isinstance(left, int) or isinstance(left, float) else
            list(map(chr, range(ord(left), ord(right) + 1)))
        ),
        lambda r: lambda left, right, c: (
            list(range(int(left), int(right)))
            if isinstance(left, int) or isinstance(left, float) else
            list(map(chr, range(ord(left), ord(right))))
            if isinstance(left, str) and isinstance(right, str) else
            c.CycleChop(left, right)
        ),
        lambda r: lambda left, right, c: left ** right,
        lambda r: lambda left, right, c: (
            lambda value: "" if value == "\x00" else value
        )(
            (left[right] if right in left else None)
            if isinstance(left, dict) else
            left[right % len(left)]
            if isinstance(left, list) or isinstance(left, str) else
            (
                getattr(left, right)
                if isinstance(right, str) and hasattr(left, right) else
                left[right % len(left)]  # default to iterable
            )
        ),
        lambda r: lambda left, right, c: left.append(right) or left,
        lambda r: lambda left, right, c: right.join(left),
        lambda r: lambda left, right, c: left.split(right),
        lambda r: lambda left, right, c: FindAll(left, right),
        lambda r: lambda left, right, c: (
            left.find(right)
            if isinstance(left, str) else
            ListFind(left, right)
        ),
        lambda r: lambda left, right, c: " " * (right - len(left)) + left,
        lambda r: lambda left, right, c: left + " " * (right - len(left)),
        lambda r: lambda left, right, c: left.count(right),
        lambda r: lambda left, right, c: Rule(left, right),
        lambda r: lambda left, right, c: DelayedRule(left, right),
        lambda r: lambda left, right, c: PatternTest(left, right),
        lambda r: lambda left, right, c: left[right:],
        lambda r: lambda left, right, c: c.Any(left, right),
        lambda r: lambda left, right, c: c.All(left, right)
    ],
    CharcoalToken.Ternary: [lambda r: lambda x, y, z, c: x[y:z]],
    CharcoalToken.Quarternary: [lambda r: lambda x, y, z, w, c: x[y:z:w]],
    CharcoalToken.LazyUnary: [],
    CharcoalToken.LazyBinary: [
        lambda r: lambda left, right, c: left(c) and right(c),
        lambda r: lambda left, right, c: left(c) or right(c)
    ],
    CharcoalToken.LazyTernary: [
        lambda r: lambda x, y, z, c: c.Ternary(x, y, z)
    ],
    CharcoalToken.LazyQuarternary: [],
    CharcoalToken.OtherOperator: [
        lambda r: lambda c: c.PeekDirection(r[1](c), r[2](c)),
        lambda r: lambda c: c.Map(r[1](c), r[2]),
        lambda r: lambda c: c.EvaluateVariable(r[1](c), r[2](c)),
        lambda r: lambda c: c.EvaluateVariable(r[1](c), [r[2](c)])
    ],

    CharcoalToken.Program: [
        lambda r: lambda c: ((r[0](c) or True) and r[2](c)),
        lambda r: lambda c: None
    ],
    CharcoalToken.Body: [
        lambda r: lambda c: r[1](c),
        lambda r: lambda c: r[0](c)
    ],
    CharcoalToken.Command: [
        lambda r: lambda c: c.InputString(r[1]),
        lambda r: lambda c: c.InputNumber(r[1]),
        lambda r: lambda c: c.Evaluate(r[1](c), True),
        lambda r: lambda c: c.Print(r[1](c), directions={r[0](c)}),
        lambda r: lambda c: c.Print(r[0](c)),
        lambda r: lambda c: c.Multiprint(r[2](c), directions=set(r[1](c))),
        lambda r: lambda c: c.Multiprint(r[1](c)),
        lambda r: lambda c: c.Polygon(r[1](c), r[2](c)),
        lambda r: lambda c: c.Polygon(
            [[(side, length) for side in r[1](c)] for length in [r[2](c)]][0],
            r[3](c)
        ),
        lambda r: lambda c: c.Polygon(r[1](c), r[2](c), fill=False),
        lambda r: lambda c: c.Polygon(
            [[(side, length) for side in r[1](c)] for length in [r[2](c)]][0],
            r[3](c), fill=False
        ),
        lambda r: lambda c: c.Rectangle(r[1](c), r[2](c)),
        lambda r: lambda c: c.Rectangle(r[1](c)),
        lambda r: lambda c: c.Oblong(r[1](c), r[2](c), r[3](c)),
        lambda r: lambda c: c.Oblong(r[1](c), r[2](c)),
        lambda r: lambda c: c.Rectangle(r[1](c), r[2](c), r[3](c)),
        lambda r: lambda c: c.Rectangle(r[1](c), r[2](c)),
        lambda r: lambda c: c.Move(r[0](c)),
        lambda r: lambda c: c.Move(r[1](c)),
        lambda r: lambda c: c.Move(r[2](c), r[1](c)),
        lambda r: lambda c: c.Move(r[1](c), r[2](c)),
        lambda r: lambda c: c.Pivot(Pivot.left, r[1](c)),
        lambda r: lambda c: c.Pivot(Pivot.left),
        lambda r: lambda c: c.Pivot(Pivot.right, r[1](c)),
        lambda r: lambda c: c.Pivot(Pivot.right),
        lambda r: lambda c: c.Jump(r[1](c), r[2](c)),
        lambda r: lambda c: c.RotateTransform(r[1](c)),
        lambda r: lambda c: c.RotateTransform(),
        lambda r: lambda c: c.ReflectTransform(r[1](c)),
        lambda r: lambda c: c.ReflectTransform(r[1](c)),
        lambda r: lambda c: c.ReflectTransform(),
        lambda r: lambda c: c.RotatePrism(r[2], r[1](c), number=True),
        lambda r: lambda c: c.RotatePrism(r[2](c), r[1](c)),
        lambda r: lambda c: c.RotatePrism(anchor=r[1](c)),
        lambda r: lambda c: c.RotatePrism(r[1], number=True),
        lambda r: lambda c: c.RotatePrism(r[1](c)),
        lambda r: lambda c: c.RotatePrism(),
        lambda r: lambda c: c.ReflectMirror(r[1](c)),
        lambda r: lambda c: c.ReflectMirror(r[1](c)),
        lambda r: lambda c: c.ReflectMirror(),
        lambda r: lambda c: c.RotateCopy(r[2], r[1](c), number=True),
        lambda r: lambda c: c.RotateCopy(r[2](c), r[1](c)),
        lambda r: lambda c: c.RotateCopy(anchor=r[1](c)),
        lambda r: lambda c: c.RotateCopy(r[1], number=True),
        lambda r: lambda c: c.RotateCopy(r[1](c)),
        lambda r: lambda c: c.RotateCopy(),
        lambda r: lambda c: c.ReflectCopy(r[1](c)),
        lambda r: lambda c: c.ReflectCopy(r[1](c)),
        lambda r: lambda c: c.ReflectCopy(),
        lambda r: lambda c: c.RotateOverlap(
            r[2], r[1](c), overlap=r[4](c), number=True
        ),
        lambda r: lambda c: c.RotateOverlap(r[2](c), r[1](c), overlap=r[3](c)),
        lambda r: lambda c: c.RotateOverlap(anchor=r[1](c), overlap=r[2](c)),
        lambda r: lambda c: c.RotateOverlap(
            r[1], overlap=r[3](c), number=True
        ),
        lambda r: lambda c: c.RotateOverlap(r[1](c), overlap=r[2](c)),
        lambda r: lambda c: c.RotateOverlap(overlap=r[1](c)),
        lambda r: lambda c: c.RotateOverlap(r[2], r[1](c), number=True),
        lambda r: lambda c: c.RotateOverlap(r[2](c), r[1](c)),
        lambda r: lambda c: c.RotateOverlap(anchor=r[1](c)),
        lambda r: lambda c: c.RotateOverlap(r[1], number=True),
        lambda r: lambda c: c.RotateOverlap(r[1](c)),
        lambda r: lambda c: c.RotateOverlap(),
        lambda r: lambda c: c.RotateShutter(
            r[2], r[1](c), overlap=r[4](c), number=True
        ),
        lambda r: lambda c: c.RotateShutter(r[2](c), r[1](c), overlap=r[3](c)),
        lambda r: lambda c: c.RotateShutter(anchor=r[1](c), overlap=r[2](c)),
        lambda r: lambda c: c.RotateShutter(
            r[1], overlap=r[3](c), number=True
        ),
        lambda r: lambda c: c.RotateShutter(r[1](c), overlap=r[2](c)),
        lambda r: lambda c: c.RotateShutter(overlap=r[1](c)),
        lambda r: lambda c: c.RotateShutter(r[2], r[1](c), number=True),
        lambda r: lambda c: c.RotateShutter(r[2](c), r[1](c)),
        lambda r: lambda c: c.RotateShutter(anchor=r[1](c)),
        lambda r: lambda c: c.RotateShutter(r[1], number=True),
        lambda r: lambda c: c.RotateShutter(r[1](c)),
        lambda r: lambda c: c.RotateShutter(),
        lambda r: lambda c: c.ReflectOverlap(r[1](c), overlap=r[2](c)),
        lambda r: lambda c: c.ReflectOverlap(r[1](c), overlap=r[2](c)),
        lambda r: lambda c: c.ReflectOverlap(overlap=r[1](c)),
        lambda r: lambda c: c.ReflectOverlap(r[1](c)),
        lambda r: lambda c: c.ReflectOverlap(r[1](c)),
        lambda r: lambda c: c.ReflectOverlap(),
        lambda r: lambda c: c.ReflectButterfly(r[1](c), overlap=r[2](c)),
        lambda r: lambda c: c.ReflectButterfly(r[1](c), overlap=r[2](c)),
        lambda r: lambda c: c.ReflectButterfly(overlap=r[1](c)),
        lambda r: lambda c: c.ReflectButterfly(r[1](c)),
        lambda r: lambda c: c.ReflectButterfly(r[1](c)),
        lambda r: lambda c: c.ReflectButterfly(),
        lambda r: lambda c: c.Rotate(r[1](c)),
        lambda r: lambda c: c.Rotate(),
        lambda r: lambda c: c.Reflect(r[1](c)),
        lambda r: lambda c: c.Reflect(),
        lambda r: lambda c: c.Copy(r[1](c), r[2](c)),
        lambda r: lambda c: c.For(r[1], r[2]),
        lambda r: lambda c: c.While(r[1], r[2]),
        lambda r: lambda c: c.If(r[1], r[2], r[3]),
        lambda r: lambda c: c.If(r[1], r[2], lambda c: None),
        lambda r: lambda c: c.Assign(r[1](c), r[2](c), r[3](c)),
        lambda r: lambda c: c.Assign(r[1](c), r[2]),
        lambda r: lambda c: c.Assign(r[1](c), r[2](c)),
        lambda r: lambda c: c.Fill(r[1](c)),
        lambda r: lambda c: c.SetBackground(r[1](c)),
        lambda r: lambda c: c.Dump(),
        lambda r: lambda c: c.RefreshFor(r[1](c), r[2], r[3]),
        lambda r: lambda c: c.RefreshWhile(r[1](c), r[2], r[3]),
        lambda r: lambda c: c.Refresh(r[1](c)),
        lambda r: lambda c: c.Refresh(),
        lambda r: lambda c: c.ToggleTrim(),
        lambda r: lambda c: c.Crop(r[1](c), r[2](c)),
        lambda r: lambda c: c.Crop(r[1](c)),
        lambda r: lambda c: c.Clear(False),
        lambda r: lambda c: c.Extend(r[1](c), r[2](c)),
        lambda r: lambda c: c.Extend(r[1](c)),
        lambda r: lambda c: r[1](c).append(r[2](c)),
        lambda r: lambda c: dict(r[2](c)).get(r[1](c), r[3])(c),
        lambda r: lambda c: dict(r[2](c)).get(
            r[1](c), lambda *arguments: None
        )(c),
        lambda r: lambda c: c.Map(r[1](c), r[2], True),
        lambda r: lambda c: c.ExecuteVariable(r[1](c), r[2](c)),
        lambda r: lambda c: c.ExecuteVariable(r[1](c), [r[2](c)]),
        lambda r: lambda c: c.Assign(r[2](c), r[1](c)),
        lambda r: lambda c: c.MapAssignLeft(r[3], r[2](c), r[1]),
        lambda r: lambda c: c.MapAssign(r[2], r[1]),
        lambda r: lambda c: c.MapAssignRight(r[3], r[2](c), r[1]),
        lambda r: lambda c: c.MapAssign(r[2], r[1]),
        lambda r: lambda c: exec(r[1](c))
    ]
}
