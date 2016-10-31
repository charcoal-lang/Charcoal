'use strict';

var InterpreterProcessor = new Array(CharcoalToken.MAXIMUM + 1);

InterpreterProcessor[CharcoalToken.Arrow] = [
    function (result) {
        return Direction.left;
    },
    function (result) {
        return Direction.up;
    },
    function (result) {
        return Direction.right;
    },
    function (result) {
        return Direction.down;
    },
    function (result) {
        return Direction.up_left;
    },
    function (result) {
        return Direction.up_right;
    },
    function (result) {
        return Direction.down_right;
    },
    function (result) {
        return Direction.down_left;
    }
];

InterpreterProcessor[CharcoalToken.Multidirectional] = [
    function (result) {
        return result[0];
    },
    function (result) {
        result[1].unshift(
            Direction.right,
            Direction.down,
            Direction.left,
            Direction.up
        );
        return result[1];
    },
    function (result) {
        result[1].unshift(
            Direction.up_right,
            Direction.down_right,
            Direction.down_left,
            Direction.up_left
        );
        return result[1];
    },
    function (result) {
        result[1].unshift(
            Direction.right,
            Direction.down_right,
            Direction.down,
            Direction.down_left,
            Direction.left,
            Direction.up_left,
            Direction.up,
            Direction.up_right
        );
        return result[1];
    },
    function (result) {
        result[1].unshift(
            Direction.up,
            Direction.down
        );
        return result[1];
    },
    function (result) {
        result[1].unshift(
            Direction.left,
            Direction.right
        );
        return result[1];
    },
    function (result) {
        result[1].unshift(
            Direction.up_left,
            Direction.down_right
        );
        return result[1];
    },
    function (result) {
        result[1].unshift(
            Direction.up_right,
            Direction.down_left
        );
        return result[1];
    },
    function (result) {
        result[1].unshift(
            Direction.up_right,
            Direction.down_right
        );
        return result[1];
    },
    function (result) {
        result[1].unshift(
            Direction.down_left,
            Direction.up_left
        );
        return result[1];
    },
    function (result) {
        result[1].unshift(
            Direction.down_right,
            Direction.down_left
        );
        return result[1];
    },
    function (result) {
        result[1].unshift(
            Direction.up,
            Direction.up_right,
            Direction.down_right,
            Direction.down
        );
        return result[1];
    },
    function (result) {
        result[1].unshift(
            Direction.up,
            Direction.right
        );
        return result[1];
    },
    function (result) {
        result[1].unshift(
            Direction.right,
            Direction.down,
            Direction.left
        );
        return result[1];
    },
    function (result) {
        result[1].unshift(
            Direction.up_left,
            Direction.up_right
        );
        return result[1];
    },
    function (result) {
        result[1].unshift(
            Direction.up_left,
            Direction.up_right,
            Direction.down
        );
        return result[1];
    },
    function (result) {
        result[1].unshift(
            Direction.down_left,
            Direction.left
        );
        return result[1];
    },
    function (result) {
        result[1].unshift(
            Direction.down,
            Direction.left
        );
        return result[1];
    },
    function (result) {
        return [];
    }
];

InterpreterProcessor[CharcoalToken.Side] = [
    function (result) {
        return function (charcoal) {
            return [result[0], result[1](charcoal)];
        }
    }
];

InterpreterProcessor[CharcoalToken.String] = [
    function (result) { return result; }
];

InterpreterProcessor[CharcoalToken.Number] = [
    function (result) { return result; }
];

InterpreterProcessor[CharcoalToken.Name] = [
    function (result) { return result; }
];

InterpreterProcessor[CharcoalToken.Separator] = [
    function (result) { return null; },
    function (result) { return null; }
];

InterpreterProcessor[CharcoalToken.Arrows] = [
    function (result) { return [result[0]] + result[1]; },
    function (result) { return result; }
];

InterpreterProcessor[CharcoalToken.Sides] = [
    function (result) {
        return function (charcoal) {
            var returns = result[1](charcoal);
            returns.unshift(result[0](charcoal));
        }
    },
    function (result) {
        return function (charcoal) {
            return [result[0](charcoal)];
        }
    }
];

InterpreterProcessor[CharcoalToken.Expressions] = [
    function (result) {
        return function (charcoal) {
            var returns = result[1](charcoal);
            returns.unshift(result[0](charcoal));
        }
    },
    function (result) {
        return function (charcoal) {
            return [result[0](charcoal)];
        }
    }
];

InterpreterProcessor[CharcoalToken.PairExpressions] = [
    function (result) {
        return function (charcoal) {
            var returns = result[2](charcoal);
            returns.unshift([result[0](charcoal), result[1](charcoal)]);
        }
    },
    function (result) {
        return function (charcoal) {
            return [[result[0](charcoal), result[1](charcoal)]];
        }
    }
];

InterpreterProcessor[CharcoalToken.List] = [
    function (result) {
        return function (charcoal) {
            return result[1](charcoal);
        }
    },
    function (result) {
        return function (charcoal) {
            return [];
        }
    }
];

InterpreterProcessor[CharcoalToken.ArrowList] = [
    function (result) {
        return result[1];
    },
    function (result) {
        return [];
    }
];

InterpreterProcessor[CharcoalToken.Dictionary] = [
    function (result) {
        return function (charcoal) { return new Map(result[1](charcoal)); }
        // TODO: how new is Map
    },
    function (result) {
        return function (charcoal) { return {}; }
    }
];

InterpreterProcessor[CharcoalToken.Expression] = [
    function (result) {
        return function (charcoal) { return result[0]; }
    },
    function (result) {
        return function (charcoal) { return result[0]; }
    },
    function (result) {
        return function (charcoal) {
            return charcoal.scope[result[0]] || charcoal.hidden[result[0]] || null;
        }
    },
    function (result) {
        return function (charcoal) { return result[0](charcoal); }
    },
    function (result) {
        return function (charcoal) { return result[0](charcoal); }
    },
    function (result) {
        return function (charcoal) { return result[0](charcoal); }
    },
    function (result) {
        return function (charcoal) {
            return result[0](result[1], result[2], result[3], charcoal);
        }
    },
    function (result) {
        return function (charcoal) {
            return result[0](
                result[1](charcoal),
                result[2](charcoal),
                result[3](charcoal),
                charcoal
            );
        }
    },
    function (result) {
        return function (charcoal) {
            return result[0](result[1], result[2], charcoal);
        }
    },
    function (result) {
        return function (charcoal) {
            return result[0](result[1](charcoal), result[2](charcoal), charcoal);
        }
    },
    function (result) {
        return function (charcoal) {
            return result[0](result[1], charcoal);
        }
    },
    function (result) {
        return function (charcoal) {
            return result[0](
                result[1](charcoal),
                charcoal
            );
        }
    },
    function (result) {
        return function (charcoal) {
            return result[0](charcoal);
        }
    }
];

InterpreterProcessor[CharcoalToken.Nilary] = [
    function (result) {
        return function (charcoal) { return charcoal.InputString(); }
    },
    function (result) {
        return function (charcoal) { return charcoal.InputNumber(); }
    },
    function (result) {
        return function (charcoal) { return charcoal.Random(); }
    },
    function (result) {
        return function (charcoal) { return charcoal.PeekAll(); }
    },
    function (result) {
        return function (charcoal) { return charcoal.Peek(); }
    }
];

InterpreterProcessor[CharcoalToken.Unary] = [
    function (result) {
        return function (item, charcoal) { return -item; }
    },
    function (result) {
        return function (item, charcoal) { return item.length; }
    },
    function (result) {
        return function (item, charcoal) { return !item; }
    },
    function (result) {
        return function (item, charcoal) { return charcoal.Cast(item); }
    },
    function (result) {
        return function (item, charcoal) { return charcoal.Random(item); }
    },
    function (result) {
        return function (item, charcoal) {
            return charcoal.Evaluate(item);
        }
    },
    function (result) {
        return function (item, charcoal) { return item.pop(); }
    },
    function (result) {
        return function (item, charcoal) { return item.toLowerCase(); }
    },
    function (result) {
        return function (item, charcoal) { return item.toUpperCase(); }
    },
    function (result) {
        return function (item, charcoal) {
            return item.reduce(function (previous, current) {
                return previous < current ? previous : current;
            });
        }
    },
    function (result) {
        return function (item, charcoal) {
            return item.reduce(function (previous, current) {
                return previous > current ? previous : current;
            });
        }
    },
    function (result) {
        return function (item, charcoal) { return typeof item === 'string' ? item.charCodeAt(0) : String.fromCharCode(item); }
    }
];

InterpreterProcessor[CharcoalToken.Binary] = [
    function (result) {
        return function (left, right, charcoal) {
        (left + [right]) if
        isinstance(left, list) and not isinstance(right, list) else
        ([left] + right) if
        not isinstance(left, list) and isinstance(right, list) else
        (str(left) + str(right)) if
        isinstance(left, str) or isinstance(right, str) else
        (left + right)
    ),
    function (result) {
        return function (left, right, charcoal) { return left - right; }
    },
    function (result) {
        return function (left, right, charcoal) { return left * right; }
    },
    function (result) {
        return lambda left, right, charcoal: (
        (left[:int(len(left) / right)]) if
        isinstance(left, str) or isinstance(left, list) else
        int(left / right)
    ),
    function (result) {
        return function (left, right, charcoal) { return left % right; }
    },
    function (result) {
        return function (left, right, charcoal) { return left === right; }
    },
    function (result) {
        return function (left, right, charcoal) { return left < right; }
    },
    function (result) {
        return function (left, right, charcoal) { return left > right; }
    },
    function (result) {
        return function (left, right, charcoal) {
            return Charcoal.CycleChop(left, right);
        }
    },
    function (result) {
        return function (left, right, charcoal) { return Math.pow(left, right); }
    },
    function (result) {
        return function (left, right, charcoal) {
            return left[right] ? (function (value) {
                return value === '\x00' ? '' : value;
            })(left[right]) : null;
        }
    },
    function (result) {
        return function (left, right, charcoal) { return left.push(right) || left; }
    },
    function (result) {
        return function (left, right, charcoal) { return left.join(right); }
    },
    function (result) {
        return function (left, right, charcoal) { return left.split(right); }
    },
    function (result) {
        return function (left, right) {
            var result = [];
            var index = left.indexOf(right);
            while (true) {
                if (index !== -1)
                    result.push(index);
                else
                    return result;
                index = left.indexOf(right, index + 1);
            }
        }
    },
    function (result) {
        return function (left, right) { return left.indexOf(right); }
    },
    function (result) {
        return function (left, right) { return ' '.repeat(right - left.length) + left; }
    },
    function (result) {
        return function (left, right) { return left + ' '.repeat(right - left.length); }
    }
];

InterpreterProcessor[CharcoalToken.Ternary] = [
];

InterpreterProcessor[CharcoalToken.LazyUnary] = [
];

InterpreterProcessor[CharcoalToken.LazyBinary] = [
    function (result) {
        return function (left, right, charcoal) {
            return left(charcoal) && right(charcoal);
        }
    },
    function (result) {
        return function (left, right, charcoal) {
            return left(charcoal) || right(charcoal);
        }
    }
];

InterpreterProcessor[CharcoalToken.LazyTernary] = [
    function (result) {
        return function (first, second, third, charcoal) {
            return charcoal.Ternary(first, second, third);
        }
    }
];

InterpreterProcessor[CharcoalToken.OtherOperators] = [
    function (result) {
        return function (charcoal) {
            return charcoal.PeekDirection(result[1](charcoal), result[2]);
        }
    }
];

InterpreterProcessor[CharcoalToken.Program] = [
    function (result) {
        return function (charcoal) {
            return (result[0](charcoal) || true) && result[1](charcoal);
        }
    },
    function (result) {
        return function (charcoal) { return null; }
    }
];

InterpreterProcessor[CharcoalToken.Body] = [
    function (result) {
        return function (charcoal) { return result[1](charcoal); }
    },
    function (result) {
        return function (charcoal) { return result[0](charcoal); }
    }
];

InterpreterProcessor[CharcoalToken.Command] = [
    function (result) {
        return function (charcoal) {
            return charcoal.InputString(result[1]);
        }
    },
    function (result) {
        return function (charcoal) {
            return charcoal.InputNumber(result[1]);
        }
    },
    function (result) {
        return function (charcoal) {
            return charcoal.Evaluate(result[1](charcoal), true);
        }
    },
    function (result) {
        return function (charcoal) {
            return charcoal.Print(result[1](charcoal), {directions:new Set(result[0])});
        }
    },
    function (result) {
        return function (charcoal) {
            return charcoal.Print(result[0](charcoal));
        }
    },
    function (result) {
        return function (charcoal) {
            return charcoal.Multiprint(
        result[2](charcoal),
        {directions: new Set(result[1])}
    ),
    function (result) {
        return function (charcoal) {
            return charcoal.Multiprint(result[1](charcoal));
        }
    },
    function (result) {
        return function (charcoal) {
            return charcoal.Polygon(result[1](charcoal), result[2](charcoal));
        }
    },
    function (result) {
        return function (charcoal) {
            return charcoal.Polygon((function (length) {
                return result[1].map(function (side) {
                    return [side, length];
                });
            })(result[2](charcoal)), result[3](charcoal));
        }
    },
    function (result) {
        return function (charcoal) {
            return charcoal.Polygon(result[1](charcoal), result[2](charcoal), {fill:false});
        }
    },
    function (result) {
        return function (charcoal) {
            return charcoal.Polygon((function (length) {
                return result[1].map(function (side) {
                    return [side, length];
                });
            })(result[2](charcoal)), result[3](charcoal), {fill:false});
        }
    },
    function (result) {
        return function (charcoal) {
            return charcoal.Rectangle(result[1](charcoal), result[2](charcoal));
        }
    },
    function (result) {
        return function (charcoal) {
            return charcoal.Rectangle(result[1](charcoal), result[2](charcoal), result[3](charcoal));
        }
    },
    function (result) {
        return function (charcoal) { return charcoal.Dump(); }
    },
    function (result) {
        return function (charcoal) { return charcoal.Move(result[0]); }
    },
    function (result) {
        return function (charcoal) { return charcoal.Move(result[1]); }
    },
    function (result) {
        return function (charcoal) { return charcoal.Move(result[2], result[1](charcoal)); }
    },
    function (result) {
        return function (charcoal) { return charcoal.Pivot(Pivot.left, result[1](charcoal)); }
    },
    function (result) {
        return function (charcoal) { return charcoal.Pivot(Pivot.left); }
    },
    function (result) {
        return function (charcoal) { return charcoal.Pivot(Pivot.right, result[1](charcoal)); }
    },
    function (result) {
        return function (charcoal) { return charcoal.Pivot(Pivot.right); }
    },
    function (result) {
        return function (charcoal) { return charcoal.Jump(result[1](charcoal), result[2](charcoal)); }
    },
    function (result) {
        return function (charcoal) { return charcoal.RotateTransform(result[1](charcoal)); }
    },
    function (result) {
        return function (charcoal) { return charcoal.ReflectTransform(result[1]); }
    },
    function (result) {
        return function (charcoal) { return charcoal.ReflectTransform(result[1]); }
    },
    function (result) {
        return function (charcoal) { return charcoal.ReflectMirror(result[1]); }
    },
    function (result) {
        return function (charcoal) { return charcoal.ReflectMirror(result[1]); }
    },
    function (result) {
        return function (charcoal) { return charcoal.RotateCopy(result[1](charcoal), result[2]); }
    },
    function (result) {
        return function (charcoal) { return charcoal.RotateCopy(result[1](charcoal)); }
    },
    function (result) {
        return function (charcoal) { return charcoal.ReflectCopy(result[1]); }
    },
    function (result) {
        return function (charcoal) { return charcoal.ReflectCopy(result[1]); }
    },
    function (result) {
        return function (charcoal) { return charcoal.RotateOverlap(result[1](charcoal)); }
    },
    function (result) {
        return function (charcoal) { return charcoal.ReflectOverlap(result[1]); }
    },
    function (result) {
        return function (charcoal) { return charcoal.ReflectOverlap(result[1]); }
    },
    function (result) {
        return function (charcoal) { return charcoal.Rotate(result[1](charcoal)); }
    },
    function (result) {
        return function (charcoal) { return charcoal.Reflect(result[1]); }
    },
    function (result) {
        return function (charcoal) { return charcoal.Copy(result[1](charcoal), result[2](charcoal)); }
    },
    function (result) {
        return function (charcoal) { return charcoal.For(result[1], result[2]); }
    },
    function (result) {
        return function (charcoal) { return charcoal.While(result[1], result[2]); }
    },
    function (result) {
        return function (charcoal) { return charcoal.If(result[1], result[2], result[3]); }
    },
    function (result) {
        return function (charcoal) {
            return charcoal.If(result[1], result[2], function (result) {
                return function (charcoal) { return null; }
            });
        }
    },
    function (result) {
        return function (charcoal) { return charcoal.Assign(result[2], result[1](charcoal)); }
    },
    function (result) {
        return function (charcoal) { return charcoal.Fill(result[1](charcoal)); }
    },
    function (result) {
        return function (charcoal) { return charcoal.SetBackground(result[1](charcoal)); }
    },
    function (result) {
        return function (charcoal) { return charcoal.Dump(); }
    },
    function (result) {
        return function (charcoal) { return charcoal.RefreshFor(result[1](charcoal), result[2], result[3]); }
    },
    function (result) {
        return function (charcoal) { return charcoal.RefreshWhile(result[1](charcoal), result[2], result[3]); }
    },
    function (result) {
        return function (charcoal) { return charcoal.Refresh(result[1](charcoal)); }
    },
    function (result) {
        return function (charcoal) { return charcoal.Refresh(); }
    },
    function (result) {
        return function (charcoal) { return charcoal.Crop(result[1](charcoal), result[2](charcoal)); }
    },
    function (result) {
        return function (charcoal) { return charcoal.Clear(); }
    },
    function (result) {
        return function (charcoal) { return charcoal.Extend(result[1](charcoal), result[2](charcoal)); }
    },
    function (result) {
        return function (charcoal) { return charcoal.Extend(result[1](charcoal)); }
    }
]

