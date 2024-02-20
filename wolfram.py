from math import (
    exp, log, log2, log10, sqrt, sin, cos, tan, asin, acos, atan, floor, ceil,
    isinf
)
from functools import reduce, lru_cache
import unicodedata as ud
try:
    from regex import (
        match, search, split, sub as re_sub, findall, finditer,
        compile as re_compile, escape as re_escape,
        M as multiline_flag
    )

    def multilineify(function):
        def wrap_function(*args, **kwargs):
            kwargs['flags'] = multiline_flag
            return function(*args, **kwargs)
        return wrap_function
    match, search, split, re_sub, findall, finditer = (
        multilineify(match),
        multilineify(search),
        multilineify(split),
        multilineify(re_sub),
        multilineify(findall),
        multilineify(finditer)
    )
except Exception as e:
    print("Please install the 'regex' module: 'sudo -H pip3 install regex'")
    __import__("sys").exit()

# TODO: chain plus/minus for less precision needed
# TODO: tests for rational ops
# TODO: feature parity for stringsplit, stringreplace and stringcases
# TODO: handle infinite precision in arithmetic
# TODO: complex
# TODO: get literal for number creation whenever possible
# TODO: not infinite precision Rational * and /


generator = type(i for i in [])
r_whitespace = re_compile(r"\s+")
prime_cache = [2, 3]


def take(generator, n):
    if n:
        for _ in range(n):
            try:
                yield next(generator)
            except:
                break
    else:
        while True:
            try:
                yield next(generator)
            except:
                break


def prime_gen():
    global prime_cache
    for number in prime_cache:
        yield number
    n = prime_cache[-1]
    while True:
        if all(n % number for number in prime_cache):
            prime_cache += [n]
            yield n
        n += 2


def flatten(iterable):
    return [item for element in iterable for item in (
        flatten(element)
        if hasattr(element, "__iter__") and not isinstance(element, str) else
        [element]
    )]


def remove_diacritics(string):
    return ''.join(
        (c for c in ud.normalize("NFD", string) if ud.category(c) != "Mn")
    )

rd = remove_diacritics
heads = []
headifies = []


def headify(cls):
    global heads
    global headifies
    if cls not in heads:
        heads += [cls]

        def fn(leaves, precision=None):
            return cls(*leaves)
        headifies += [fn]
        return fn
    return headifies[heads.index(cls)]


def create_expression(value):
    value_type = type(value)
    if value is None:
        return None
    elif callable(value):
        return value
    elif isinstance(value, Expression):
        return value
    elif value_type == complex:
        return Complex(value)
    elif value_type == str:
        return String(value)
    elif value_type == list or value_type == tuple or value_type == generator:
        return List(*[create_expression(item) for item in value])
    elif value_type != int and value % 1:
        value = round(value, 15)
        exponent = 0
        while value % 1:
            value *= 10
            exponent -= 1
        return Real(int(value), exponent, float("inf"))
    else:
        exponent = 0
        if value:
            while not value % 10:
                value //= 10
                exponent += 1
        return Integer(value, exponent)

cx = create_expression


def boolean(value):
    return _True if value else _False

def simplify(left, right, fn, repeat=False):
    if type(left) == Expression:
        left = left.run()
    if type(right) == Expression:
        right = right.run()
    if isinstance(left, List):
        if isinstance(right, List):
            if len(left.leaves) != len(right.leaves):
                raise Exception("Lists have different length")
            return SymbolicList(
                *(simplify(l, r, fn, True) for l, r in zip(left, right))
            )
        return SymbolicList(*(simplify(l, right, fn, True) for l in left))
    if isinstance(right, List):
        return SymbolicList(*(simplify(left, r, fn, True) for r in right))
    if repeat:
        return fn(left, right)

def simplify_multiple(items, fn):
    items = list(items)
    i, l = 0, len(items) - 1
    while i < l:
        simple = simplify(items[i], items[i + 1], fn)
        if simple and isinstance(simple, List):
            items[:2] = [SymbolicOperation(add, *simple.leaves)]
            l -= 1
        else:
            i += 1
    return items


class Operation(object):
    __slots__ = ("symbol", "precedence", "commutative", "simplify", "function")

    def __init__(self, symbol, precedence, commutative, simplify, function):
        self.symbol = symbol
        self.precedence = precedence
        self.commutative = commutative
        self.simplify = lambda items: simplify(
            simplify_multiple(items, function)
        )
        self.function = function

def _pow_simplify(items):
    if len(items) == 1:
        return items
    if items[0] == One or items[1] == One:
        return (items[0],)
    if items[1] == Zero:
        return (One,)
    return items
pow = Operation("^", 4, False, _pow_simplify, lambda l, r: l ** r)

def _mul_simplify(items):
    if any(item == Zero for item in items):
        return (Zero,)
    return list(sorted(filter(lambda item: item != One, items)))
mul = Operation("", 3, True, _mul_simplify, lambda l, r: l * r)

def _div_simplify(items):
    if items[0] == Zero:
        return (Zero,)
    if len(items) == 1:
        return items
    if items[1] == One:
        return (items[0],)
    return items
div = Operation("/", 3, False, _div_simplify, lambda l, r: l / r)

def _add_simplify(items):
    return list(sorted(filter(lambda item: item != Zero, items)))
add = Operation("+", 2, True, _add_simplify, lambda l, r: l + r)

def _sub_simplify(items):
    if items[0] == Zero:
        if len(items) == 1:
            return items
        return (items[1],)
    if items[1] == Zero:
        return (items[0],)
    return items
sub = Operation("-", 2, False, _sub_simplify, lambda l, r: l - r)

def is_exactly_int(item, numeral, value, exponent):
    if isinstance(item, int):
        if item == numeral:
            return True
    elif (
        isinstance(item, Integer) and
        item.leaves[1] == exponent and
        item.leaves[0] == value
    ):
        return True
    return False


class Comparable(object):
    def cmp(self, other):
        pass

    def __eq__(self, other):
        return self.cmp(other) == 0

    def __lt__(self, other):
        return self.cmp(other) == -1

    def __gt__(self, other):
        return self.cmp(other) == 1

    def __ne__(self, other):
        return self.cmp(other) != 0

    def __le__(self, other):
        return self.cmp(other) < 1

    def __ge__(self, other):
        return self.cmp(other) > -1


class Expression(object):
    __slots__ = ("head", "leaves", "run", "op")

    def __init__(
        self, head=None, leaves=[], run=None, op=None
    ):
        self.head = head
        self.leaves = [create_expression(leaf) for leaf in leaves]
        self.run = run or (lambda precision=None: self.head(
            self.leaves, precision
        ))
        self.op = op

    def __add__(self, other):
        if is_exactly_int(other, 0, 0, 0):
            return self
        if is_exactly_int(self, 0, 0, 0):
            return other
        if (
            isinstance(self, Symbolic) or
            isinstance(other, Symbolic)
        ):
            return SymbolicOperation(add, self, other)
        return Expression(
            None, [],
            lambda precision=10: self.run(precision + 2) + (
                create_expression(other).run(precision + 2)
            )
        )

    def __radd__(self, other):
        return Expression.__add__(other, self)

    def __sub__(self, other):
        if is_exactly_int(other, 0, 0, 0):
            return self
        if (
            isinstance(self, Symbolic) or
            isinstance(other, Symbolic)
        ):
            return SymbolicOperation(sub, self, other)
        return Expression(
            None, [],
            lambda precision=10: self.run(precision + 2) - (
                create_expression(other).run(precision + 2)
            )
        )

    def __rsub__(self, other):
        if is_exactly_int(self, 0, 0, 0):
            return other
        if (
            isinstance(self, Symbolic) or
            isinstance(other, Symbolic)
        ):
            return SymbolicOperation(sub, other, self)
        return Expression(
            None, [],
            lambda precision=10: (
                create_expression(other).run(precision + 2)
            ) - self.run(precision + 2)
        )

    def __mul__(self, other):
        if is_exactly_int(self, 0, 0, 0) or is_exactly_int(other, 0, 0, 0):
            return Integer(0)
        if is_exactly_int(self, 1, 1, 0):
            return other
        if is_exactly_int(other, 1, 1, 0):
            return self
        if (
            isinstance(self, Symbolic) or
            isinstance(other, Symbolic)
        ):
            return SymbolicOperation(mul, self, other)
        return Expression(
            None, [],
            lambda precision=10: self.run(precision + 2) * (
                create_expression(other).run(precision + 2)
            )
        )

    def __rmul__(self, other):
        return Expression.__mul__(other, self)

    def __truediv__(self, other):
        if is_exactly_int(self, 0, 0, 0):
            return Integer(0)
        if is_exactly_int(other, 1, 1, 0):
            return self
        if (
            isinstance(self, Symbolic) or
            isinstance(other, Symbolic)
        ):
            return SymbolicOperation(div, self, other)
        return Expression(
            None, [],
            lambda precision=10: self.run(precision + 2) / (
                create_expression(other).run(precision + 2)
            )
        )

    def __rtruediv__(self, other):
        if is_exactly_int(other, 0, 0, 0):
            return Integer(0)
        if is_exactly_int(self, 1, 1, 0):
            return other
        if (
            isinstance(self, Symbolic) or
            isinstance(other, Symbolic)
        ):
            return SymbolicOperation(div, other, self)
        return Expression(
            None, [],
            lambda precision=10: (
                create_expression(other).run(precision + 2)
            ) / self.run(precision + 2)
        )

    def __pow__(self, other):
        if is_exactly_int(other, 0, 0, 0):
            return Integer(1)
        if is_exactly_int(other, 1, 1, 0):
            return self
        if is_exactly_int(self, 0, 0, 0):
            return Integer(0)
        if is_exactly_int(self, 1, 1, 0):
            return Integer(1)
        if (
            isinstance(self, Symbolic) or
            isinstance(other, Symbolic)
        ):
            return SymbolicOperation(pow, self, other)
        return Expression(
            None, [],
            lambda precision=10: self.run(precision + 2) ** (
                create_expression(other).run(precision + 2)
            )
        )
    
    def __rpow__(self, other):
        if (
            isinstance(self, Symbolic) or
            isinstance(other, Symbolic)
        ):
            return SymbolicOperation(pow, other, self)
        return Expression(
            None, [],
            lambda precision=10: (
                create_expression(other).run(precision + 2)
            ) ** self.run(precision + 2),
            op=pow
        )

    def __str__(self):
        result = self.run()
        if type(result) == Expression:
            raise Exception("Expression evaluates to Expression")
        return str(result)

    def to_number(self):
        result = self.run()
        if type(result) == Expression:
            raise Exception("Expression evaluates to Expression")
        return result.to_number()

    def __int__(self):
        return int(self.to_number())

    def to_precision(self, precision=None):
        return self.run().to_precision(precision)

    def is_integer(self):
        return self.run().is_integer()

    def is_odd(self):
        return self.run().is_odd()

    def is_even(self):
        return self.run().is_even()


class Symbol(Expression):
    pass


class Symbolic(Expression):
    pass


class SymbolicOperation(Symbolic, Comparable):
    __slots__ = ("op",)

    def __new__(cls, op, *items):
        i, l = 0, len(items)
        items = list(items)
        if op.commutative:
            while i < l:
                if (
                    isinstance(items[i], SymbolicOperation) and
                    items[i].op.symbol == op.symbol
                ):
                    delta = len(items[i].items)
                    l += delta - 1
                    items[i:i + 1] = items[i].items
                else:
                    i += 1
        simple = op.simplify(items)
        if len(simple) == 1:
            return simple[0]
        return super().__new__(cls)

    def __init__(self, op, *items):
        if hasattr(self, "op"):
            # Already initialized
            return
        super().__init__(head=headify(SymbolicOperation))
        self.op = op
        self.items = items
        i, l = 0, len(items)
        items = list(items)
        while i < l:
            if (
                op.commutative and
                isinstance(items[i], SymbolicOperation) and
                items[i].op.symbol == op.symbol
            ):
                delta = len(items[i].items)
                l += delta - 1
                items[i:i + 1] = items[i].items
            else:
                i += 1
        self.items = op.simplify(items)
        if len(self.items) == 1:
            raise Exception("wat?")
        self.run = lambda precision=10: str(self)

    def __str__(self, str=str):
        return (
            (" " + self.op.symbol + " ") if self.op.symbol else " "
        ).join(
            "(" + str(item) + ")" if (
                isinstance(item, Expression) and
                item.op and
                item.op.precedence < self.op.precedence
            ) else str(item)
            for item in self.items
        ).replace(" + -", " - ")

    def __repr__(self):
        return self.__str__(repr)


class SymbolicVariable(Symbolic, Comparable):
    __slots__ = ("__name__", "name", "op")

    def __init__(self, name):
        super().__init__(head=headify(SymbolicVariable))
        self.__name__ = name
        self.name = name
        self.run = lambda precision=10: str(self)

    def __str__(self):
        return self.name

    def __repr__(self):
        return ":" + self.name

    def __call__(self, leaves):
        return SymbolicFunction(self, leaves)

    def __add__(self, other):
        if not isinstance(other, Expression):
            other = create_expression(other)
        return Expression.__add__(self, other)

    def __radd__(self, other):
        if not isinstance(other, Expression):
            other = create_expression(other)
        return Expression.__radd__(self, other)

    def __sub__(self, other):
        if not isinstance(other, Expression):
            other = create_expression(other)
        return Expression.__sub__(self, other)

    def __rsub__(self, other):
        if not isinstance(other, Expression):
            other = create_expression(other)
        return Expression.__rdub__(self, other)

    def __mul__(self, other):
        if not isinstance(other, Expression):
            other = create_expression(other)
        return Expression.__mul__(self, other)

    def __rmul__(self, other):
        if not isinstance(other, Expression):
            other = create_expression(other)
        return Expression.__rmul__(self, other)

    def __div__(self, other):
        if not isinstance(other, Expression):
            other = create_expression(other)
        return Expression.__div__(self, other)

    def __rdiv__(self, other):
        if not isinstance(other, Expression):
            other = create_expression(other)
        return Expression.__rdiv__(self, other)

    def __pow__(self, other):
        if not isinstance(other, Expression):
            other = create_expression(other)
        return Expression.__pow__(self, other)

    def __rpow__(self, other):
        if not isinstance(other, Expression):
            other = create_expression(other)
        return Expression.__rpow__(self, other)

    def cmp(self, other):
        if isinstance(other, Number):
            return 1
        if isinstance(other, SymbolicVariable):
            return (
                1 if self.name > other.name else
                -1 if self.name < other.name else
                0
            )
        if isinstance(other, SymbolicOperation):
            if other.op == mul:
                for item in other.items:
                    if not isinstance(other, Number):
                        return self.cmp(item)
            return self.cmp(other.items[0])


class SymbolicFunction(Symbolic):
    __slots__ = ("leaves",)

    def __init__(self, head, leaves):
        super().__init__(head=headify(head))
        self.head = head
        self.leaves = leaves
        self.run = lambda: self

    def __str__(self):
        return (
            self.head.__name__ + "[" + ", ".join(map(str, self.leaves)) + "]"
        )

    def __repr__(self):
        return str(self)

# Options
IC = IgnoreCase = Symbol()
A = All = Symbol()
O = Overlaps = Symbol()
In = Indeterminate = Symbol()


class Number(Expression):
    __slots__ = ("size", "sign")

    def __init__(self, head=None):
        super().__init__(head=head)
        self.size = 0
        self.sign = 0

    def __eq__(self, other):
        if isinstance(other, int):
            other = Integer(other)
        elif isinstance(other, float):
            other = create_expression(other)
        if isinstance(other, Number):
            if self.sign != other.sign:
                return False
            if self.size != other.size:
                return False
            self_rational = isinstance(self, Rational)
            other_rational = isinstance(other, Rational)
            if isinstance(self, Real) and isinstance(other, Real):
                self_i = 1 + self_rational
                other_i = 1 + other_rational
                min_exponent = min(self.leaves[1], other.leaves[1])
                new_self = self.leaves[0] * 10 ** (
                    self.leaves[self_i] - min_exponent
                )
                new_other = other.leaves[0] * 10 ** (
                    other.leaves[other_i] - min_exponent
                )
                if self_rational:
                    new_other *= self.leaves[1]
                if other_rational:
                    new_self *= other.leaves[1]
                return new_self == new_other
        return False

    def __gt__(self, other):
        if isinstance(other, int):
            other = Integer(other)
        elif isinstance(other, float):
            other = create_expression(other)
        if isinstance(other, Number):
            if self.sign > other.sign:
                return True
            if self.sign < other.sign:
                return False
            if self.size > other.size:
                return self.sign == 1
            if self.size < other.size:
                return self.sign == -1
            self_rational = isinstance(self, Rational)
            other_rational = isinstance(other, Rational)
            if isinstance(self, Real) and isinstance(other, Real):
                self_i = 1 + self_rational
                other_i = 1 + other_rational
                min_exponent = min(self.leaves[1], other.leaves[1])
                new_self = self.leaves[0] * 10 ** (
                    self.leaves[self_i] - min_exponent
                )
                new_other = other.leaves[0] * 10 ** (
                    other.leaves[other_i] - min_exponent
                )
                if self_rational:
                    new_other *= self.leaves[1]
                if other_rational:
                    new_self *= other.leaves[1]
                return new_self > new_other
        return False

    def __lt__(self, other):
        if isinstance(other, int):
            other = Integer(other)
        elif isinstance(other, float):
            other = create_expression(other)
        if isinstance(other, Number):
            if self.sign < other.sign:
                return True
            if self.sign > other.sign:
                return False
            if self.size < other.size:
                return self.sign == 1
            if self.size > other.size:
                return self.sign == -1
            self_rational = isinstance(self, Rational)
            other_rational = isinstance(other, Rational)
            if isinstance(self, Real) and isinstance(other, Real):
                self_i = 1 + self_rational
                other_i = 1 + other_rational
                min_exponent = min(self.leaves[1], other.leaves[1])
                new_self = self.leaves[0] * 10 ** (
                    self.leaves[self_i] - min_exponent
                )
                new_other = other.leaves[0] * 10 ** (
                    other.leaves[other_i] - min_exponent
                )
                if self_rational:
                    new_other *= self.leaves[1]
                if other_rational:
                    new_self *= other.leaves[1]
                return new_self < new_other
        return False

    def __ne__(self, other):
        return not self == other

    def __ge__(self, other):
        if isinstance(other, int):
            other = Integer(other)
        elif isinstance(other, float):
            other = create_expression(other)
        if isinstance(other, Number):
            if self.sign > other.sign:
                return True
            if self.sign < other.sign:
                return False
            if self.size > other.size:
                return self.sign == 1
            if self.size < other.size:
                return self.sign == -1
            self_rational = isinstance(self, Rational)
            other_rational = isinstance(other, Rational)
            if isinstance(self, Real) and isinstance(other, Real):
                self_i = 1 + self_rational
                other_i = 1 + other_rational
                min_exponent = min(self.leaves[1], other.leaves[1])
                new_self = self.leaves[0] * 10 ** (
                    self.leaves[self_i] - min_exponent
                )
                new_other = other.leaves[0] * 10 ** (
                    other.leaves[other_i] - min_exponent
                )
                if self_rational:
                    new_other *= self.leaves[1]
                if other_rational:
                    new_self *= other.leaves[1]
                return new_self >= new_other
        return False

    def __le__(self, other):
        if isinstance(other, int):
            other = Integer(other)
        elif isinstance(other, float):
            other = create_expression(other)
        if isinstance(other, Number):
            if self.sign < other.sign:
                return True
            if self.sign > other.sign:
                return False
            if self.size < other.size:
                return self.sign == 1
            if self.size > other.size:
                return self.sign == -1
            self_rational = isinstance(self, Rational)
            other_rational = isinstance(other, Rational)
            if isinstance(self, Real) and isinstance(other, Real):
                self_i = 1 + self_rational
                other_i = 1 + other_rational
                min_exponent = min(self.leaves[1], other.leaves[1])
                new_self = self.leaves[0] * 10 ** (
                    self.leaves[self_i] - min_exponent
                )
                new_other = other.leaves[0] * 10 ** (
                    other.leaves[other_i] - min_exponent
                )
                if self_rational:
                    new_other *= self.leaves[1]
                if other_rational:
                    new_self *= other.leaves[1]
                return new_self <= new_other
        return False

class Real(Number):
    __slots__ = ("is_int", "precision")

    def __init__(self, value, exponent=0, precision=0, is_int=False):
        super().__init__(head=headify(Real))
        self.precision = precision or floor(log10(max(1, abs(value))))
        self.is_int = is_int
        self.leaves = [value, exponent]
        self.size = log10(max(1, value)) + exponent
        self.sign = 1 if value > 0 else -1 if value < 0 else 0

    def __str__(self):
        exponent = self.leaves[1]
        string = str(self.leaves[0])
        zeroes = 1 - exponent - len(string)
        if zeroes > 0:
            string = "0" * zeroes + string
        return (
            string + "0" * exponent
            if exponent > 0 else
            (string[:exponent] + "." + string[exponent:])
            if exponent < 0 else
            string
        )

    def __repr__(self):
        return str(self)

    def __add__(self, other):
        if isinstance(other, Symbolic):
            return SymbolicOperation(add, self, other)
        if type(other) == Expression:
            return other + self
        if isinstance(other, Real):
            precision = max(0, min(self.precision, other.precision) - 2)
            exponent_difference = self.leaves[1] - other.leaves[1]
            if exponent_difference > 0:
                value = (
                    self.leaves[0] * 10 ** exponent_difference +
                    other.leaves[0]
                )
            else:
                value = (
                    self.leaves[0] +
                    other.leaves[0] * 10 ** -exponent_difference
                )
            if isinf(precision):
                exponent = min(self.leaves[1], other.leaves[1])
                return (Integer if exponent >= 0 else Real)(
                    value, exponent, precision=precision
                )
            actual_precision = floor(log10(abs(value) or 1))
            return Real(
                (
                    value * 10 ** (precision - actual_precision)
                    if precision - actual_precision > 1 else
                    value // 10 ** (actual_precision - precision) + bool(
                        value < 0 and
                        value % 10 ** (actual_precision - precision)
                    )
                ),
                (
                    min(self.leaves[1], other.leaves[1]) +
                    actual_precision -
                    precision
                ),
                precision=precision
            )

    def __sub__(self, other):
        if isinstance(other, Symbolic):
            return SymbolicOperation(sub, self, other)
        if type(other) == Expression:
            return other.__rsub__(self)
        if type(other) == Real:
            precision = max(0, min(self.precision, other.precision) - 2)
            exponent_difference = self.leaves[1] - other.leaves[1]
            if exponent_difference > 0:
                value = (
                    self.leaves[0] * 10 ** exponent_difference -
                    other.leaves[0]
                )
            else:
                value = (
                    self.leaves[0] -
                    other.leaves[0] * 10 ** -exponent_difference
                )
            if isinf(precision):
                exponent = min(self.leaves[1], other.leaves[1])
                return (Integer if exponent >= 0 else Real)(
                    value,
                    min(self.leaves[1], other.leaves[1]),
                    precision=precision
                )
            actual_precision = floor(log10(abs(value) or 1))
            return Real(
                (
                    value * 10 ** (precision - actual_precision)
                    if precision - actual_precision > 1 else
                    value // 10 ** (actual_precision - precision) + bool(
                        value < 0 and
                        value % 10 ** (actual_precision - precision)
                    )
                ),
                (
                    min(self.leaves[1], other.leaves[1]) +
                    actual_precision -
                    precision
                ),
                precision=precision
            )

    def __mul__(self, other):
        if isinstance(other, Symbolic):
            return SymbolicOperation(mul, self, other)
        if type(other) == Expression:
            return other * self
        if isinstance(other, Real):
            precision = max(0, min(self.precision, other.precision) - 2)
            value = self.leaves[0] * other.leaves[0]
            actual_precision = floor(log10(abs(value) or 1))
            if isinf(precision):
                exponent = min(self.leaves[1], other.leaves[1])
                return (Integer if exponent >= 0 else Real)(
                    value,
                    self.leaves[1] + other.leaves[1],
                    precision=precision
                )
            return Real(
                (
                    value * 10 ** (precision - actual_precision)
                    if precision - actual_precision > 1 else
                    value // 10 ** (actual_precision - precision) + bool(
                        value < 0 and
                        value % 10 ** (actual_precision - precision)
                    )
                ),
                (
                    self.leaves[1] +
                    other.leaves[1] +
                    actual_precision -
                    precision
                ),
                precision=precision
            )
        if type(other) == Rational or type(other) == Complex:
            return other * self
        return self * Real(other)

    def __truediv__(self, other):
        if isinstance(other, Symbolic):
            return SymbolicOperation(div, self, other)
        if type(other) == Expression:
            return other.__rtruediv__(self)
        if isinstance(other, Real):
            # TODO: add precision crap here maybe?
            precision = max(0, min(self.precision, other.precision) - 2)
            if isinf(precision):
                min_exponent = min(self.leaves[1], other.leaves[1])
                self.leaves[1] -= min_exponent
                other.leaves[1] -= min_exponent
                int_self = int(self)
                int_other = int(other)
                if int_self % int_other:
                    return Rational(int(self), int(other))
                return Integer(int(self) // int(other))
            pow10 = 10 ** precision * self.leaves[0]
            return Real(
                pow10 // other.leaves[0] + bool(
                    pow10 < 0 and pow10 % other.leaves[0]
                ),
                self.leaves[1] - other.leaves[1] - precision,
                precision=precision
            )
        other_type = type(other)
        if other_type == Rational:
            return Rational(self.leaves[0], 1, self.leaves[1]) / other
        if other_type == Complex:
            pass  # TODO

    def __neg__(self):
        return Real(
            -self.leaves[0], self.leaves[1], self.precision, self.is_int
        )

    def __invert__(self):
        return Integer(~int(self))

    def __abs__(self):
        return Real(
            abs(self.leaves[0]), self.leaves[1], self.precision, self.is_int
        )

    def __int__(self):
        return int(
            self.leaves[0] * 10 ** self.leaves[1]
            if self.leaves[1] >= 0 else
            self.leaves[0] / 10 ** -self.leaves[1]
        )

    def __float__(self):
        return float(
            self.leaves[0] * 10 ** self.leaves[1]
            if self.leaves[1] >= 0 else
            self.leaves[0] / 10 ** -self.leaves[1]
        )

    def to_number(self):
        result = (
            self.leaves[0] * 10 ** self.leaves[1]
            if self.leaves[1] >= 0 else
            self.leaves[0] / 10 ** -self.leaves[1]
        )
        if not result % 1:
            return int(result)
        return result

    def is_integer(self):
        return boolean(self.is_int or self.leaves[1] >= 0)

    def is_odd(self):
        return boolean(
            self.is_int or 
            self.leaves[1] > 0 or self.leaves[1] == 0 and (
                self.leaves[0] % 2 == 1
            )
        )

    def is_even(self):
        return boolean(
            self.is_int or 
            self.leaves[1] > 0 or self.leaves[1] == 0 and (
                self.leaves[0] % 2 == 0
            )
        )


class Integer(Real):
    def __init__(self, value, exponent=0, precision=None):
        value = int(value)
        super().__init__(
            value, exponent, precision=float("inf"), is_int=True
        )
        self.head = headify(Integer)
        actual_precision = floor(log10(abs(value) or 1))
        self.run = lambda precision=None: Real(
            (
                value * 10 ** (precision - actual_precision - 1)
                if precision - actual_precision > 1 else
                value // 10 ** (1 + actual_precision - precision)
            ),
            self.leaves[1] - precision + actual_precision + 1,
            precision=precision
        ) if precision else self

    def __cmp__(self, other):
        ""

    def __str__(self):
        string = str(self.leaves[0])
        return (
            string + "0" * self.leaves[1]
            if self.leaves[1] != 0 else
            string
        )

    def __repr__(self):
        return str(self)

    def __int__(self):
        return int(self.leaves[0] * 10 ** self.leaves[1])

    def __float__(self):
        return float(self.leaves[0] * 10 ** self.leaves[1])

    def to_number(self):
        return self.leaves[0] * 10 ** self.leaves[1]

    def is_integer(self):
        return _True

    def is_odd(self):
        return boolean(self.leaves[1] > 0 or self.leaves[1] == 0 and (
            self.leaves[0] % 2 == 1
        ))

    def is_even(self):
        return boolean(self.leaves[1] > 0 or self.leaves[1] == 0 and (
            self.leaves[0] % 2 == 0
        ))


class WolframFalse(Integer):
    def __init__(self):
        super().__init__(0)

    def __str__(self):
        return "False"

    def __bool__(self):
        return False


class WolframTrue(Integer):
    def __init__(self):
        super().__init__(1)

    def __str__(self):
        return "True"

    def __bool__(self):
        return True

Zero = Integer(0)
One = Integer(1)
_False = WolframFalse()
_True = WolframTrue()


class Rational(Number):
    def __new__(cls, numerator, denominator, exponent=0):
        if numerator == 0:
            return Integer(0)
        if not numerator % denominator:
            return Integer(numerator // denominator)
        return super().__new__(cls)

    def __init__(self, numerator, denominator, exponent=0):
        super().__init__(head=headify(Rational))
        if denominator < 0:
            denominator *= -1
            numerator *= -1
        if not numerator:
            denominator = 1
        else:
            while not numerator % 10:
                numerator //= 10
                exponent += 1
        if not denominator:
            raise Exception("divide by zero error")
        while not denominator % 10:
            denominator //= 10
            exponent -= 1
        while numerator % 1:
            numerator *= 10
            exponent -= 1
        while denominator % 1:
            denominator *= 10
            exponent += 1
        numerator, denominator = int(numerator), int(denominator)
        a, b = numerator, denominator
        if b > a:
            a, b = b, a
        while b:
            a, b = b, a % b
        numerator //= a
        denominator //= a
        # TODO: check gcd is actually gcd, i.e. check powers of 2 and 5
        self.leaves = [numerator, denominator, exponent]
        self.size = log10(max(1, abs(numerator / denominator))) + exponent
        self.sign = 1 if numerator > 0 else -1 if numerator < 0 else 0
        # TODO: make it create integer directly somehow
        self.run = lambda precision: (
            Real(numerator, precision=(precision + 2) if precision else None) /
            Real(denominator, precision=(precision + 2) if precision else None)
        )
        if numerator == 0:
            self.run = lambda precision=None: Integer(0)
        elif denominator == 1:
            self.run = lambda precision=None: Integer(numerator, exponent)

    def __str__(self):
        if self.leaves[0] == 0:
            return "0"
        if self.leaves[1] == 1:
            return str(self.leaves[0] * 10 ** self.leaves[2])
        return str(self.leaves[0]) + "/" + str(self.leaves[1])

    def __repr__(self):
        return str(self)

    def __add__(self, other):
        if isinstance(other, Symbolic):
            return SymbolicOperation(add, self, other)
        if isinstance(other, Expression):
            return other + self

    def __mul__(self, other):
        if isinstance(other, Symbolic):
            return SymbolicOperation(mul, self, other)
        if isinstance(other, Expression):
            return other * self
        if isinstance(other, Rational):
            return Rational(
                self.leaves[0] * other.leaves[0],
                self.leaves[1] * other.leaves[1]
            )
        if isinstance(other, Real) and isinf(other.precision):
            return Rational(
                self.leaves[0] * other.leaves[0],
                self.leaves[1],
                self.leaves[2] + other.leaves[1]
            )

    def __truediv__(self, other):
        if isinstance(other, Symbolic):
            return SymbolicOperation(div, self, other)
        if isinstance(other, Expression):
            return Expression.__rtruediv__(other, self)
        if isinstance(other, Rational):
            return Rational(
                self.leaves[0] * other.leaves[1],
                self.leaves[1] * other.leaves[0]
            )
        if isinstance(other, Real) and isinf(other.precision):
            return Rational(
                self.leaves[0],
                self.leaves[1] * other.leaves[0],
                self.leaves[2] - other.leaves[1]
            )

    def __int__(self):
        return int(self.leaves[2] * self.leaves[0] / self.leaves[1])

    def __float__(self):
        return float(self.leaves[2] * self.leaves[0] / self.leaves[1])

    def to_number(self):
        return float(self.leaves[0]) * self.leaves[2] / self.leaves[1]

    def is_integer(self):
        return boolean(self.leaves[1] == 1)

    def is_odd(self):
        return boolean(self.leaves[1] == 1 and (self.leaves[0] % 2 == 1))

    def is_even(self):
        return boolean(self.leaves[1] == 1 and (self.leaves[0] % 2 == 0))


class Complex(Number):
    def __init__(self, real, imaginary=0):
        super.__init__(head=headify(Complex))
        if isinstance(real, complex):
            self.real = create_expression(real).run()
            self.imaginary = create_expression(imaginary).run()
        self.leaves = [real, imaginary]

    def __str__(self):
        return str(self.leaves[0]) + " + " + str(self.leaves[1]) + "j"

    def __repr__(self):
        return str(self)


class List(Expression):
    # TODO: operators
    def __init__(self, *items):
        super().__init__(head=headify(List))
        self.leaves = list(map(create_expression, filter(
            lambda x: x is not None,
            (
                items[0] if
                len(items) == 1 and isinstance(items[0], list) else
                items
            )
        )))

    def __str__(self):
        return "[" + ", ".join(str(item) for item in self.leaves) + "]"

    def __repr__(self):
        return "[" + ", ".join(repr(item) for item in self.leaves) + "]"

    def __len__(self):
        return len(self.leaves)

    def __getitem__(self, i):
        if isinstance(i, slice):
            return List(*self.leaves.__getitem__())
        return self.leaves[i]

    def __setitem__(self, i, value):
        self.leaves.__setitem__(i, value)

    def __iter__(self):
        return iter(self.leaves)


class SymbolicList(List, Symbolic):
    pass


class MixedRadix(Expression):
    # TODO: basic examples cf. Wolfram
    def __init__(self, list):
        super().__init__(head=headify(MixedRadix))
        self.leaves = [create_expression(list)]


class String(Expression):
    def __init__(self, value):
        super().__init__(head=headify(String))
        self.leaves = [value]

    def __str__(self):
        return self.leaves[0]

    def __repr__(self):
        return repr(self.leaves[0])

    def __len__(self):
        return len(self.leaves[0])

    def __getitem__(self, i):
        return self.leaves[0].__getitem__(i)

    def __iter__(self):
        return iter(self.leaves[0])

    def __add__(self, other):
        if isinstance(other, String):
            return String(self.leaves[0] + other.leaves[0])

    def __or__(self, other):
        other_type = type(other)
        if other_type == String:
            return List(self.leaves[0], other.leaves[0])
        if other_type == List:
            return List(*(other.leaves + self.leaves))


class Rule(Expression):
    def __init__(self, match, replacement):
        super().__init__(head=headify(Rule))
        self.leaves = [match, replacement]

    def __str__(self):
        return str(self.leaves[0]) + "→" + str(self.leaves[1])

    def __repr__(self):
        return repr(self.leaves[0]) + "→" + repr(self.leaves[1])


class DelayedRule(Expression):
    def __init__(self, match, replacement):
        super().__init__(head=headify(DelayedRule))
        self.leaves = [match, replacement]

    def __str__(self):
        return str(self.leaves[0]) + ":→" + str(self.leaves[1])

    def __repr__(self):
        return repr(self.leaves[0]) + ":→" + repr(self.leaves[1])


class Pattern(Expression):
    def __init__(self, regex):
        super().__init__(head=headify(Pattern))
        self.leaves = [regex]

    def __str__(self):
        return self.leaves[0]

    def __repr__(self):
        return repr(self.leaves[0])

    def __or__(self, other):
        if isinstance(other, Pattern):
            return Pattern("(?:%s)|(?:%s)" % (str(self), str(other)))
        if isinstance(other, String):
            return Pattern("(?:%s)|%s" % (str(self), re_escape(str(other))))
        if isinstance(other, str):
            return Pattern("(?:%s)|%s" % (str(self), re_escape(other)))

    def __ror__(self, other):
        if isinstance(other, Pattern):
            return Pattern("(?:%s)|(?:%s)" % (str(other), str(self)))
        if isinstance(other, String):
            return Pattern("%s|(?:%s)" % (re_escape(str(other)), str(self)))
        if isinstance(other, str):
            return Pattern("%s|(?:%s)" % (re_escape(other), str(self)))

    def __add__(self, other):
        if isinstance(other, Pattern):
            return Pattern(str(self) + str(other))
        if isinstance(other, String):
            return Pattern(str(self) + re_escape(str(other)))
        if isinstance(other, str):
            return Pattern(str(self) + re_escape(other))

    def __radd__(self, other):
        if isinstance(other, String):
            return Pattern(re_escape(str(other)) + str(self))
        if isinstance(other, str):
            return Pattern(re_escape(other) + str(self))

    def __hash__(self):
        return hash(self.leaves[0])

    def __eq__(self, other):
        return self.leaves[0] == other.leaves[0]

# _p is stripped
_p_ = Pattern(r".")
_p__ = Pattern(r".+")
_p___ = Pattern(r".*")
SOS = StartOfString = Pattern(r"^")
EOS = EndOfString = Pattern(r"$")
SOL = StartOfLine = Pattern(r"\A")
EOL = EndOfLine = Pattern(r"\Z")
Ws = Whitespace = Pattern(r"\s+")
NS = NumberString = Pattern(r"\d+.?\d*")
WC = WordCharacter = Pattern(r"(?:\p{L}|[0-9])")
LC = LetterCharacter = Pattern(r"\p{L}")
DC = DigitCharacter = Pattern(r"[0-9]")
HC = HexadecimalCharacter = Pattern(r"[0-9a-fA-F]")
WsC = WhitespaceCharacter = Pattern(r"\s")
PC = PunctuationCharacter = Pattern(r"\p{P}")
WB = WordBoundary = Pattern(r"\b")

# TODO: PatternTest (_ ? LetterQ)


class RegularExpression(Pattern):
    def __init__(self, regex):
        super().__init__(regex)
        self.head = headify(RegularExpression)


class Repeated(Pattern):
    def __init__(self, item):
        if isinstance(item, Pattern):
            super().__init__("(?:" + str(item) + ")+")
        elif isinstance(item, List):
            super().__init__("(?:" + "|".join(map(str, item)) + ")+")
        else:
            super().__init__("(?:" + re_escape(str(item)) + ")+")
        self.head = headify(Repeated)


class RepeatedNull(Pattern):
    def __init__(self, item):
        if isinstance(item, Pattern):
            super().__init__("(?:" + str(item) + ")*")
        elif isinstance(item, List):
            super().__init__("(?:" + "|".join(map(str, item)) + ")*")
        else:
            super().__init__("(?:" + re_escape(str(item)) + ")*")
        self.head = headify(RepeatedNull)


class Shortest(Pattern):
    def __init__(self, item):
        if isinstance(item, Pattern):
            # TODO: pretty sure this is wrong.
            # to fix, patterns will need to be converted to use internal ast
            super().__init__(str(item) + "?")
        elif isinstance(item, List):
            super().__init__("(?:" + "|".join(map(str, item)) + ")")
        else:
            super().__init__(re_escape(str(item)))
        self.head = headify(RepeatedNull)


class Except(Pattern):
    # TODO: doesn't work for multiple chars atm
    def __init__(self, item):
        if isinstance(item, Pattern):
            super().__init__("[^%s]" % str(item))
        else:
            super().__init__("[^%s]" % re_escape(str(item)))
        self.head = headify(RepeatedNull)

date_pattern_lookup = {
    "S": r"(?:[0-5]\d|60)",
    "Second": r"(?:[0-5]\d|60)",
    "M": r"(?:[0-5]\d|60)",
    "Minute": r"(?:[0-5]\d|60)",
    "H": r"(?:[01]\d|2[0-3])",
    "Hour": r"(?:[01]\d|2[0-3])",
    "AP": "(?i:[ap]m)",
    "AMPM": "(?i:[ap]m)",
    "D": "(?:0[1-9]|[12][0-9]|3[01])",
    "Day": "(?:0?[1-9]|[12][0-9]|3[01])",
    "DN": "\b(?i:(?:Mo(?:n(?:day)?)?|Tu(?:e(?:sday)?)?|\
We(?:d(?:nesday)?)?|Th(?:u(?:rs(?:day)?)?)?|Fr(?:i(?:day)?)?|\
Sa(?:t(?:urday)?)?|Su(?:n(?:Day)?)?)",
    "DayName": "\b(?i:(?:Mo(?:n(?:day)?)?|Tu(?:e(?:sday)?)?|\
We(?:d(?:nesday)?)?|Th(?:u(?:rs(?:day)?)?)?|Fr(?:i(?:day)?)?|\
Sa(?:t(?:urday)?)?|Su(?:n(?:Day)?)?)",
    "M": "(?:[1-9]|1[0-2])",
    "Month": "(?:[1-9]|1[0-2])",
    "Q": "[qQ][1-4]",
    "Quarter": "[qQ][1-4]",
    "Y": r"\d\d(?:\d\d)?",
    "Year": r"\d\d(?:\d\d)?",
}
# TODO: date pattern, need to test on mathematica e.g. feb 30 and hour 24


class DatePattern(Pattern):
    def __init__(self, items, *other):
        if isinstance(items, list):
            items = create_expression(items)
        if isinstance(items, str):
            items, other = create_expression([items] + other), []
        elif isinstance(items, String):
            items, other = List(*([items] + other)), []
        self.leaves = [(str(other[0]) if len(other) else "[/-:.]").join(
            date_pattern_lookup.get(str(leaf), str(leaf))
            for leaf in items.leaves
        )]

pattern_test_lookup = {}


class PatternTest(Pattern):
    def __init__(self, pattern, condition):
        if pattern == _p_:
            if isinstance(condition, String):
                self.leaves = [re_escape(str(condition))]
                return
            self.leaves = [
                pattern_test_lookup.get(condition, str(condition))
            ]
        elif leaves[0] == _p__:
            if isinstance(condition, String):
                self.leaves = [re_escape(str(condition)) + "+"]
                return
            self.leaves = [
                "(?:%s)+" % pattern_test_lookup.get(condition, str(condition))
            ]
        elif leaves[0] == _p___:
            if isinstance(condition, String):
                self.leaves = [re_escape(str(condition)) + "*"]
                return
            self.leaves = [
                "(?:%s)*" % pattern_test_lookup.get(condition, str(condition))
            ]

# TODO: AlphabetData (from lazy ranges)


class Span(Expression):
    __slots__ = ("head", "leaves", "process")

    def __init__(self, start=None, stop=None, step=None):
        super().__init__(head=headify(Span))

        def modify(number, iterable):
            if isinstance(number, Expression):
                number = number.to_number()
            if number == 1:
                return -len(iterable)
            return number + ((len(iterable) + 1) if number < 0 else 0)

        if start is not None:
            if stop is not None:
                if step is not None:
                    self.process = lambda iterable: (lambda start, end: (
                        iterable[start - 1:end:step]
                        if step > 0 else
                        iterable[start:end - 1:step]
                    ))(modify(start, iterable), modify(stop, iterable))
                else:
                    self.process = lambda iterable: iterable[
                        modify(start, iterable) - 1:modify(stop, iterable)
                    ]
            else:
                if step is not None:
                    self.process = lambda iterable: iterable[
                        modify(start, iterable) - 1::step
                    ]
                else:
                    self.process = lambda iterable: iterable[
                        modify(start, iterable) - 1:
                    ]
        else:
            if stop is not None:
                if step is not None:
                    self.process = lambda iterable: iterable[
                        :modify(stop, iterable):step
                    ]
                else:
                    self.process = lambda iterable: iterable[
                        :modify(stop, iterable)
                    ]
            else:
                if step is not None:
                    self.process = lambda iterable: iterable[::step]
                else:
                    # TODO: clone or no
                    self.process = lambda iterable: iterable[:]


def integerQ(number):
    return int(
        isinstance(number, int) or
        (isinstance(number, float) and not (number % 1))
    )


def oddQ(number):
    return int(integerQ(number) and number % 2)


def evenQ(number):
    return int(integerQ(number) and not (number % 2))


def n(number, digits=0):
    return number - number % 10 ** -digits

# TODO: round, log


def perm(n, r):
    result = 1
    for i in range(n - r + 1, n + 1):
        result *= i
    return result


def comb(n, r):
    if r > n // 2:
        r = n - r
    result = 1
    for i in range(n - r + 1, n + 1):
        result *= i
    for i in range(2, r + 1):
        result //= i
    return result


def figurate(n, dim):
    return comb(n + dim - 1, dim)


class Wolfram(object):

    def Head(leaves, precision=None):
        return leaves[0].head
    
    def UpTo(leaves, precision=None):
        return leaves[0]

    # TODO: named (which are chained) operators - these don't use the
    # default + etc
    # change default to use an internal method with precision passable
    # which both e.g. Plus and __add__ can use

    def N(leaves, precision=None):
        # Leaves: number, precision (accuracy?)
        return [
            None,
            lambda: leaves[0].run(10),
            lambda: leaves[0].run(int(leaves[1]))
        ][len(leaves)]()

    def StringQ(leaves, precision=None):
        return boolean(isinstance(leaves[0], str))

    def NumberQ(leaves, precision=None):
        return boolean(isinstance(leaves[0], Number))

    def IntegerQ(leaves, precision=None):
        return boolean(leaves[0].is_integer())

    def OddQ(leaves, precision=None):
        return boolean(leaves[0].is_odd())

    def EvenQ(leaves, precision=None):
        return boolean(leaves[0].is_even())

    def TrueQ(leaves, precision=None):
        return boolean(leaves[0] == _True)

    def FalseQ(leaves, precision=None):
        return boolean(leaves[0] == _False)

    def Sqrt(leaves, precision=None):

        def calculate_sqrt(n, precision):
            # TODO: there's too much precisions
            if isinstance(precision, Expression):
                precision = precision.to_number()
            precision = max(precision, 1)
            digits = int(log10(n) + 1) // 2
            try:  # TODO: avoid try
                result = (
                    int(sqrt(n) * 10 ** (precision - digits))
                    if precision > digits else
                    int(sqrt(n)) // 10 ** (digits - precision)
                )
            except:
                result = (
                    int(exp(log(n) / 2) * 10 ** (precision - digits))
                    if precision > digits else
                    int(exp(log(n) / 2)) // 10 ** (digits - precision)
                )
            if precision > digits:
                n *= 10 ** ((precision - digits) * 2)
            else:
                n //= 10 ** ((digits - precision) * 2)
            difference = result * result - n
            while difference >= result or difference <= -result:
                result = result - ((difference + result) // (2 * result))
                difference = result * result - n
            while not result % 10:
                result //= 10
                precision -= 1
            return Real(result, -precision + digits)

        return calculate_sqrt(leaves[0].to_number(), precision)

    # https://reference.wolfram.com/language/ref/Flatten.html
    # TODO: test, implement fourth overload
    def Flatten(leaves, precision=None):
        n = leaves[1] - 1 if len(leaves) > 1 else -1
        correct_head = (
            (lambda x: x.head == leaves[2])
            if len(leaves) > 2 else
            lambda x: True
        )
        if not n:
            return leaves[0]
        head = leaves[0].head
        if len(leaves) > 1 and isinstance(leaves[1], List):
            pass  # TODO
            # next_indices = [
            #     list(filter(None, map(lambda n: n - 1, sublist)))
            #     for sublist in leaves[1]
            # ]
            # lookup = {}
        if type(head) == type and issubclass(head, Expression):
            return leaves[0].head(*[
                item
                for element in leaves[0].leaves
                for item in (
                    Wolfram.Flatten([element, n - 1] + leaves[2:]).leaves
                    if (
                        isinstance(element, Expression) and
                        len(element.leaves) and correct_head(element)
                    ) else
                    [element]
                )
            ])
        return Expression(
            head, 
            [item for element in leaves[0].leaves for item in (
                Wolfram.Flatten([element, n - 1] + leaves[2:]).leaves
                if (
                    isinstance(element, Expression) and
                    len(element.leaves) and correct_head(element)
                ) else
                [element]
            )]
        )

    def StringJoin(leaves, precision=None):
        return String(
            "".join(map(str, Wolfram.Flatten([List(*leaves)]).leaves))
        )

    def StringLength(leaves, precision=None):
        if isinstance(leaves[0], List):
            return List(*[
                Wolfram.StringLength([item])
                for item in leaves[0].leaves
            ])
        return Integer(len(leaves[0].leaves[0]))

    def StringSplit(leaves, precision=None):
        # TODO
        # StringSplit["a--b c--d e", x : "--" :> x]
        # StringSplit[":a:b:c:", ":", All]
        # This includes zero length ones
        if isinstance(leaves[0], List):
            other_leaves = leaves[1:]
            return create_expression([
                Wolfram.StringSplit([item] + other_leaves)
                for item in leaves[0].leaves
            ])
        ignorecase, maxsplit, dont_return_all = "", 0, True
        for leaf in leaves[2:]:
            if leaf == All:
                dont_return_all = False
            elif isinstance(leaf, Rule) and leaf.leaves == [IgnoreCase, _True]:
                ignorecase = "(?i)"
            elif isinstance(leaf, Number):
                maxsplit = leaves[2].to_number()
        string = str(leaves[0])
        if len(leaves) == 1:
            result = r_whitespace.split(string, maxsplit)
            return create_expression(result[
                (dont_return_all and not result[0]):
                max(1, len(result) - (dont_return_all and not result[-1]))
            ])
        splitter = leaves[1]
        if isinstance(splitter, Pattern):
            result = split(ignorecase + str(splitter), string, maxsplit)
            return create_expression(result[
                (dont_return_all and not result[0]):
                max(1, len(result) - (dont_return_all and not result[-1]))
            ])
        splitter_type = type(leaves[1])
        if splitter_type == String:
            result = (
                split(ignorecase + re_escape(str(splitter)), string, maxsplit)
            )
            return create_expression(result[
                (dont_return_all and not result[0]):
                max(1, len(result) - (dont_return_all and not result[-1]))
            ])
        if splitter_type == List:
            if isinstance(splitter.leaves[0], Pattern):
                result = split(
                    ignorecase + "(" + "|".join(list(map(
                        str, splitter.leaves
                    ))) + ")",
                    string,
                    maxsplit
                )
            if isinstance(splitter.leaves[0], Rule):
                lookup = {}
                for rule in splitter.leaves:
                    lookup[rule.leaves[0]] = rule.leaves[1]
                result = split(
                    ignorecase + "(" + "|".join(list(map(
                        lambda l: re_escape(str(l.leaves[0])),
                        splitter.leaves
                    ))) + ")",
                    string,
                    maxsplit
                )
                for i in range(1, len(result), 2):
                    result[i] = lookup[result[i]]
                return create_expression(result[
                    (dont_return_all and not result[0]):
                    max(1, len(result) - (dont_return_all and not result[-1]))
                ])
            result = split(
                ignorecase + "|".join(list(map(
                    lambda string: re_escape(str(string)),
                    splitter.leaves
                ))),
                string,
                maxsplit
            )
            return create_expression(result[
                (dont_return_all and not result[0]):
                max(1, len(result) - (dont_return_all and not result[-1]))
            ])
        # Assume Rule
        result = []
        splitted = split(
            ignorecase + re_escape(str(splitter.leaves[0])), string, maxsplit
        )
        for string in splitted:
            result += [string, splitter.leaves[1]]
        return create_expression(result[
            (dont_return_all and not result[0]):
            (-1 - (dont_return_all and not result[-1]))
        ])

    def StringTake(leaves, precision=None):
        if type(leaves[0]) == List:
            return List(*[
                Wolfram.StringTake([item, leaves[1]])
                for item in leaves[0].leaves
            ])
        string = str(leaves[0])
        if isinstance(leaves[1], Number):
            n = int(leaves[1].to_number())
            if n < 0:
                return String(string[n:])
            return String(string[:n])
        if leaves[1].head == Wolfram.UpTo:
            return String(string[:int(leaves[1].to_number())])
        # Assume List
        if (
            isinstance(leaves[1].leaves[0], List) or
            leaves[1].leaves[0].head == Wolfram.UpTo
        ):
            return List(*[
                Wolfram.StringTake([leaves[0], item])
                for item in leaves[1].leaves
            ])
        length = len(leaves[1].leaves)
        leaves = list(map(
            lambda n: n + ((len(string) + 1) if n < 0 else 0),
            map(lambda n: n.to_number(), leaves[1].leaves)
        ))
        if length == 1:
            return String(string[leaves[0] - 1])
        if length == 2:
            return String(string[leaves[0] - 1:leaves[1]:])
        return String(string[leaves[0] - 1:leaves[1]:leaves[2]])

    def StringDrop(leaves, precision=None):
        if type(leaves[0]) == List:
            return List(*[
                Wolfram.StringDrop([item, leaves[1]])
                for item in leaves[0].leaves
            ])
        string = str(leaves[0])
        if isinstance(leaves[1], Number):
            n = int(leaves[1].to_number())
            if n < 0:
                return String(string[:n])
            return String(string[n:])
        if leaves[1].head == Wolfram.UpTo:
            return String(string[int(leaves[1].to_number()):])
        # Assume List
        if (
            isinstance(leaves[1].leaves[0], List) or
            leaves[1].leaves[0].head == Wolfram.UpTo
        ):
            return List(*[
                Wolfram.StringDrop([leaves[0], item])
                for item in leaves[1].leaves
            ])
        length = len(leaves[1].leaves)
        leaves = list(map(
            lambda n: n + ((len(string) + 1) if n < 0 else 0),
            map(lambda n: n.to_number(), leaves[1].leaves)
        ))
        if length == 1:
            return String(string[:leaves[0] - 1] + string[leaves[0]:])
        if length == 2:
            return String(string[:leaves[0] - 1] + string[leaves[1]:])
        # TODO: more performant
        middle = list(string[leaves[0] - 1:leaves[1]])
        del middle[::leaves[2]]
        return String(
            string[:leaves[0] - 1] +
            "".join(middle) +
            string[leaves[1]:]
        )

    def StringPart(leaves, precision=None):
        if type(leaves[0]) == List:
            return List(*[
                Wolfram.StringPart([item, leaves[1]])
                for item in leaves[0].leaves
            ])
        if leaves[1] == All:
            return List(*string)
        string = str(leaves[0])
        if isinstance(leaves[1], Number):
            number = int(leaves[1].to_number())
            number += ((len(string) + 1) if number < 0 else 0)
            return String(string[number - 1])
        if isinstance(leaves[1], List):
            leaves = list(map(
                lambda n: n + ((len(string) + 1) if n < 0 else 0),
                map(lambda n: n.to_number(), leaves[1].leaves)
            ))
            return List(*[
                String(string[leaf - 1])
                for leaf in leaves
            ])
        # Assume Span
        return List(*[
            String(char)
            for char in leaves[1].process(string)
        ])
# TODO: Except, StringExtract

    def StringReplace(leaves, precision=None):
        if isinstance(leaves[0], List):
            other_leaves = leaves[1:]
            return List(*[
                Wolfram.StringReplace([item] + other_leaves)
                for item in leaves[0].leaves
            ])
        ignorecase, maxreplace = "", 0
        for leaf in leaves[2:]:
            if isinstance(leaf, Rule) and leaf.leaves == [IgnoreCase, _True]:
                ignorecase = "(?i)"
            elif isinstance(leaf, Number):
                maxreplace = leaves[2].to_number()
        if len(leaves) == 1:
            return lambda items: Wolfram.StringReplace([items, leaves[0]])
        string = str(leaves[0])
        replacer = leaves[1]
        replacer_type = type(leaves[1])
        if replacer_type == String:
            return create_expression(re_sub(
                ignorecase + re_escape(str(replacer)),
                string,
                maxreplace
            ))
        if replacer_type == List:
            # Assume Rule
            lookup = {}
            for rule in replacer.leaves:
                lookup[rule.leaves[0]] = rule.leaves[1]
            result = split(
                ignorecase + "(" + "|".join(list(map(
                    lambda l: re_escape(str(l.leaves[0])),
                    replacer.leaves
                ))) + ")",
                string,
                maxreplace
            )
            for i in range(1, len(result), 2):
                result[i] = lookup[result[i]]
            return String("".join(result))
        # Assume Rule
        result = []
        splitted = split(
            ignorecase + (
                str(replacer.leaves[0])
                if isinstance(replacer.leaves[0], Pattern) else
                re_escape(str(replacer.leaves[0]))
            ), string, maxreplace
        )
        for string in splitted:
            result += [string, replacer.leaves[1]]
        return String("".join(result[:-1]))

    def StringCases(leaves, precision=None):
        if isinstance(leaves[0], List):
            other_leaves = leaves[1:]
            return List(*[
                Wolfram.StringCases([item] + other_leaves)
                for item in leaves[0].leaves
            ])
        ignorecase, maxcase, overlap = "", 0, False
        for leaf in leaves[2:]:
            if isinstance(leaf, Rule):
                if leaf.leaves == [IgnoreCase, _True]:
                    ignorecase = "(?i)"
                elif leaf.leaves == [Overlaps, _True]:
                    overlap = True
            if isinstance(leaf, Number):
                maxcase = leaves[2].to_number()
        string = str(leaves[0])
        if len(leaves) == 1:
            # TODO: does this accept options, check on mmca
            return lambda items: Wolfram.StringCases([items, leaves[0]])
        caser = leaves[1]
        if isinstance(caser, Pattern):
            return create_expression(
                item.group()
                for item in take(finditer(
                    ignorecase + str(caser), string, overlapped=overlap
                ), maxcase)
            )
        caser_type = type(leaves[1])
        if caser_type == String:
            return create_expression(
                item.group()
                for item in take(finditer(
                    ignorecase + re_escape(str(caser)), string,
                    overlapped=overlap
                ), maxcase)
            )
        if caser_type == List:
            if isinstance(caser.leaves[0], str):
                caser.leaves = list(map(String, caser.leaves))
            if isinstance(caser.leaves[0], String):
                return create_expression(
                    item.group()
                    for item in take(finditer(
                        ignorecase + "(" + "|".join(list(map(
                            lambda l: re_escape(str(l)), caser.leaves
                        ))) + ")", string, overlapped=overlap
                    ), maxcase)
                )
            # Assume Rule
            lookup = {}
            for rule in caser.leaves:
                lookup[rule.leaves[0]] = rule.leaves[1]
            return create_expression(
                item.group()
                for item in take(finditer(ignorecase + "(" + "|".join(list(map(
                    lambda l: re_escape(str(l.leaves[0])),
                    caser.leaves
                ))) + ")", string, overlapped=overlap), maxcase)
            )
        # Assume Rule
        result = []
        return create_expression(
            item and caser.leaves[1]
            for item in take(finditer(ignorecase + (
                str(caser.leaves[0])
                if isinstance(caser.leaves[0], Pattern) else
                re_escape(str(caser.leaves[0]))
            ), string, overlapped=overlap), maxcase)
        )

    def StringCount(leaves, precision=None):
        if isinstance(leaves[0], List):
            other_leaves = leaves[1:]
            return List(*[
                Wolfram.StringCount([item] + other_leaves)
                for item in leaves[0].leaves
            ])
        ignorecase, overlap = "", False
        for leaf in leaves[2:]:
            if isinstance(leaf, Rule):
                if leaf.leaves == [IgnoreCase, _True]:
                    ignorecase = "(?i)"
                elif leaf.leaves == [Overlaps, _True]:
                    overlap = True
        string = str(leaves[0])
        if len(leaves) == 1:
            # TODO: does this accept options, check on mmca
            return lambda items: Wolfram.StringCount([items, leaves[0]])
        caser = leaves[1]
        if isinstance(caser, Pattern):
            return Integer(len(findall(
                ignorecase + str(caser), string, overlapped=overlap
            )))
        caser_type = type(leaves[1])
        if caser_type == String:
            return Integer(len(findall(
                ignorecase + re_escape(str(caser)), string, overlapped=overlap
            )))
        if caser_type == List:
            if isinstance(caser.leaves[0], str):
                caser.leaves = list(map(String, caser.leaves))
            return Integer(len(findall(
                ignorecase + "(" + "|".join(list(map(
                    lambda l: re_escape(str(l)), caser.leaves
                ))) + ")",
                string, overlapped=overlap
            )))
        # Assume Rule
        return Integer(str(leaves[0]).count(str(leaves[1])))

    def StringPosition(leaves, precision=None):
        # TODO: Lists of string patterns in StringPosition are sometimes 
        # not the same as pattern alternatives
        if isinstance(leaves[0], List):
            other_leaves = leaves[1:]
            return List(*[
                Wolfram.StringPosition([item] + other_leaves)
                for item in leaves[0].leaves
            ])
        ignorecase, maxposition, overlap = "", 0, True
        for leaf in leaves[2:]:
            if isinstance(leaf, Rule):
                if leaf.leaves == [IgnoreCase, _True]:
                    ignorecase = "(?i)"
                elif leaf.leaves == [Overlaps, _False]:
                    overlap = False
            elif isinstance(leaf, Number):
                maxposition = leaves[2].to_number()
        string = str(leaves[0])
        if len(leaves) == 1:
            # TODO: does this accept options, check on mmca
            return lambda items: Wolfram.StringPosition([items, leaves[0]])
        positioner = leaves[1]
        if isinstance(positioner, Pattern):
            return create_expression(
                (item.start() + 1, item.end())
                for item in take(finditer(
                    ignorecase + str(positioner), string, overlapped=overlap
                ), maxposition)
            )
        positioner_type = type(leaves[1])
        if positioner_type == List:
            if isinstance(positioner.leaves[0], str):
                caser.leaves = list(map(String, positioner.leaves))
            # Assume String
            return create_expression(
                (item.start() + 1, item.end())
                for item in take(finditer(
                    ignorecase + "(" + "|".join(list(map(
                        lambda l: re_escape(str(l)), positioner.leaves
                    ))) + ")", string, overlapped=overlap
                ), maxposition)
            )
        # Assume String
        return create_expression(
            (item.start() + 1, item.end())
            for item in take(finditer(
                ignorecase + str(positioner), string, overlapped=overlap
            ), maxposition)
        )

    def StringRepeat(leaves, precision=None):
        if len(leaves) == 3:
            string = str(leaves[0])
            length = min(
                len(string) * leaves[1].to_number(), leaves[2].to_number()
            )
            times = length // len(string) + 1
            return String((str(leaves[0]) * times)[:length])
        return String(str(leaves[0]) * leaves[1].to_number())

    def StringDelete(leaves, precision=None):
        if isinstance(leaves[0], List):
            other_leaves = leaves[1:]
            return List(*[
                Wolfram.StringDelete([item] + other_leaves)
                for item in leaves[0].leaves
            ])
        ignorecase = ""
        for leaf in leaves[2:]:
            if isinstance(leaf, Rule) and leaf.leaves == [IgnoreCase, _True]:
                ignorecase = "(?i)"
        string = str(leaves[0])
        if len(leaves) == 1:
            return lambda items: Wolfram.StringDelete([items, leaves[0]])
        deleter = leaves[1]
        deleter_type = type(leaves[1])
        if deleter_type == List:
            # Assume String
            lookup = {}
            for rule in deleter.leaves:
                lookup[rule.leaves[0]] = rule.leaves[1]
            return String(re_sub(
                ignorecase + "(?:" + "|".join(list(map(
                    lambda l: str(l) if isinstance(l, Pattern) else (str(l)),
                    deleter.leaves
                ))) + ")", "", string
            ))
        if deleter_type == String:
            return create_expression(re_sub(
                ignorecase + re_escape(str(deleter)), "", string
            ))
        # Assume String or Pattern
        return String(re_sub(
            ignorecase + (
                str(deleter)
                if isinstance(deleter, Pattern) else
                re_escape(str(deleter))
            ), "", string
        ))

    def StringRiffle(leaves, precision=None, count=0):
        if count or len(leaves) == 1:
            if not count:
                current = leaves[0].leaves[0]
                if isinstance(current, List):
                    count += 1
                    current = current.leaves[0]
            if count:
                return String(("\n" * count).join(
                    str(Wolfram.StringRiffle(List(row), precision, count - 1))
                    for row in leaves[0].leaves
                ))
            # Assume List
            return String(" ".join(map(str, leaves[0].leaves)))
        if isinstance(leaves[0], String):
            # Weird nested list, will happen during recursion
            return leaves[0]
        riffler_type = type(leaves[1])
        if riffler_type == List:
            # Assume String[3]
            rifflers = leaves[1].leaves
            if len(leaves) > 2:
                return String(str(rifflers[0]) + str(rifflers[1]).join(map(
                    lambda l: str(Wolfram.StringRiffle([l] + leaves[2:])),
                    leaves[0].leaves
                )) + str(rifflers[2]))
            return String(str(rifflers[0]) + str(rifflers[1]).join(
                map(str, leaves[0].leaves)
            ) + str(rifflers[2]))
        if len(leaves) > 2:
            return String(str(leaves[1]).join(map(
                lambda l: str(Wolfram.StringRiffle([l] + leaves[2:])),
                leaves[0].leaves
            )))
        return String(str(leaves[1]).join(map(str, leaves[0].leaves)))

    def RemoveDiacritics(leaves, precision=None):
        if isinstance(leaves[0], List):
            other_leaves = leaves[1:]
            return List(*[
                Wolfram.RemoveDiacritics([item] + other_leaves)
                for item in leaves[0].leaves
            ])
        # Assume String
        return String(remove_diacritics(str(leaves[0])))

    def StringStartsQ(leaves, precision=None):
        if len(leaves) == 1:
            return lambda *things: Wolfram.StringStartsQ(leaves[0] + things)
        if isinstance(leaves[0], List):
            return List(*[
                Wolfram.StringStartsQ([item] + leaves[1:])
                for item in leaves[0].leaves
            ])
        if (
            len(leaves) > 2 and
            type(leaves[2]) == Rule and
            leaves[2].leaves == [IgnoreCase, _True]
        ):
            return boolean(
                match("(?i)" + re_escape(str(leaves[1])), str(leaves[0]))
            )
        return boolean(str(leaves[0]).startswith(str(leaves[1])))

    def StringEndsQ(leaves, precision=None):
        if len(leaves) == 1:
            return lambda *things: Wolfram.StringStartsQ(leaves[0] + things)
        if isinstance(leaves[0], List):
            return List(*[
                Wolfram.StringEndsQ([item] + leaves[1:])
                for item in leaves[0].leaves
            ])
        if (
            len(leaves) > 2 and
            type(leaves[2]) == Rule and
            leaves[2].leaves == [IgnoreCase, _True]
        ):
            return boolean(search(
                "(?i)" + re_escape(str(leaves[1])) + "$", str(leaves[0])
            ))
        return boolean(str(leaves[0]).endswith(str(leaves[1])))

    def StringContainsQ(leaves, precision=None):
        if len(leaves) == 1:
            return lambda *things: Wolfram.StringContainsQ(leaves[0] + things)
        if isinstance(leaves[0], List):
            other_leaves = leaves[1:]
            return List(*[
                Wolfram.StringContainsQ([item] + other_leaves)
                for item in leaves[0].leaves
            ])
        ignorecase = ""
        for leaf in leaves[2:]:
            if isinstance(leaf, Rule):
                if leaf.leaves == [IgnoreCase, _True]:
                    ignorecase = "(?i)"
        string = str(leaves[0])
        if isinstance(leaves[1], Pattern):
            return boolean(
                search(ignorecase + str(leaves[1]), str(leaves[0]))
            )
        return boolean(
            search(ignorecase + re_escape(str(leaves[1])), str(leaves[0]))
        )

    def PrintableAsciiQ(leaves, precision=None):
        if isinstance(leaves[0], List):
            return List(*[
                Wolfram.PrintableAsciiQ([item])
                for item in leaves[0].leaves
            ])
        return boolean(match("[ -~]*$", str(leaves[0])))

    def LetterQ(leaves, precision=None):
        return boolean(match(r"\p{L}*$", str(leaves[0])))

    def UpperCaseQ(leaves, precision=None):
        return boolean(match(r"\p{Lu}*$", str(leaves[0])))

    def LowerCaseQ(leaves, precision=None):
        return boolean(match(r"\p{Ll}*$", str(leaves[0])))

    def DigitQ(leaves, precision=None):
        return boolean(match(r"\d*$", str(leaves[0])))

    def CharacterRange(leaves, precision=None):
        if isinstance(leaves[0], String):
            start, end = ord(leaves[0]), ord(leaves[1])
            return List(*map(chr, range(start, end)))
        return List(*map(chr, range(leaves[0], leaves[1])))

    # basic math
    def Range(leaves, precision=None):
        if isinstance(leaves[0], List):
            return List(*[Wolfram.Range([item]) for item in leaves[0].leaves])
        # Listable
        if len(leaves) == 1:
            i = One
            result = []
            while i <= leaves[0]:
                result += [i]
                i += One
            return List(*result)
        if len(leaves) == 2:
            i = leaves[0]
            result = []
            while i <= leaves[1]:
                result += [i]
                i += One
            return List(*result)
        if len(leaves) == 3:
            i = leaves[0]
            result = []
            if leaves[2] < Integer(0):
                while i >= leaves[1]:
                    result += [i]
                    i += leaves[2]
            else:
                while i <= leaves[1]:
                    result += [i]
                    i += leaves[2]
            return List(*result)

    # base conversion (in progress)
    
    def FromDigits(leaves, precision=None):
        # TODO: do I need more Indeterminate support
        if isinstance(leaves[0], String):
            if len(leaves) == 2:
                if (
                    isinstance(leaves[1], String) and
                    leaves[1].leaves[0] == "Roman"
                ):
                    if search("\
[^IVXLCDM]|\
I[VX].|X[LC][XLCDM]|C[DM][CDM]|\
I[LCDM]|X[DM]|\
V[LCDM]|L[CDM]", leaves[0].leaves[0]):
                        raise Exception("not valid roman numeral")
                    string = leaves[0].leaves[0]
                    result = 0
                    while string:
                        first = string[0]
                        first_two = string[:2]
                        if first_two in ["IV", "IX", "XL", "XC", "CD", "CM"]:
                            string = string[2:]
                            result += {
                                "IV": 4, "IX": 9, "XL": 40, "XC": 90,
                                "CD": 400, "CM": 900
                            }[first_two]
                        else:
                            string = string[1:]
                            result += {
                                "I": 1, "V": 5, "X": 10, "L": 50,
                                "C": 100, "D": 500, "M": 1000
                            }[first]
                    return Integer(result)
                    # TODO
            leaves[0] = List(*map(
                lambda c: Integer(int(c, 36)), leaves[0].leaves[0]
            ))
        if isinstance(leaves[0], List):
            result, exponent, indeterminate = 0, 0, False
            if Indeterminate in leaves[0].leaves:
                leaves[0].leaves = leaves[0].leaves[
                    :leaves[0].leaves.index(Indeterminate)
                ]
                indeterminate = True
            if (
                isinstance(leaves[0].leaves[0], List) and
                isinstance(leaves[0].leaves[1], Number) # TODO: is this right
            ):
                exponent = int(leaves[0].leaves[1])
                leaves[0] = leaves[0].leaves[0]
            recurring = None
            if len(leaves) == 1:
                if (
                    len(leaves[0].leaves) and
                    isinstance(leaves[0].leaves[-1], List)
                ):
                    recurring = leaves[0].leaves[-1]
                    leaves[0].leaves = leaves[0].leaves[:-1]
                for item in leaves[0].leaves:
                    result = result * 10 + int(item)
                if recurring:
                    recurrer = 0
                    for item in recurring.leaves:
                        recurrer = recurrer * 10 + int(item)
                    denominator =  10 ** len(recurring.leaves) - 1
                    result = Rational(
                        denominator * result + recurrer,
                        denominator
                    )
                    if precision:
                        return result.run(precision)
                    return result
                return Integer(result)
            if len(leaves) == 2:
                if isinstance(leaves[1], Symbolic) or any(
                    isinstance(item, Symbolic)
                    for item in leaves[1].leaves
                ):
                    base = leaves[1]
                    l = len(leaves[0].leaves)
                    if not len(leaves[0].leaves):
                        return Integer(0)
                    if l > 1:
                        result = leaves[0].leaves[0] * base ** (l - 1)
                    else:
                        return leaves[0].leaves[0]
                    for i in range(1, l):
                        item = leaves[0].leaves[i]
                        result += (
                            item * base ** (l - i - 1) if l - i - 1 else item
                        )
                    return result
                if isinstance(leaves[1], Number):
                    base = int(leaves[1])
                    if (
                        len(leaves[0].leaves) and
                        isinstance(leaves[0].leaves[-1], List)
                    ):
                        recurring = leaves[0].leaves[-1]
                        leaves[0].leaves = leaves[0].leaves[:-1]
                    if recurring:
                        recurrer = 0
                        for item in recurring.leaves:
                            recurrer = recurrer * base + int(item)
                        denominator = base ** len(recurring.leaves) - 1
                        result = Rational(
                            denominator * result + recurrer,
                            denominator
                        )
                        if precision:
                            return result.run(precision)
                        return result
                    for item in leaves[0].leaves:
                        result = result * base + int(item)
                    if indeterminate:
                        while not result % 10:
                            result //= 10
                            exponent += 1
                        return Real(result, exponent, len(leaves[0].leaves))
                    return Integer(result)
                if isinstance(leaves[1], MixedRadix):
                    base_list = leaves[1].leaves[0].leaves
                    list = leaves[0].leaves
                    length_difference = (
                        len(leaves[0].leaves) -
                        len(leaves[1].leaves[0].leaves)
                    )
                    if length_difference == 1:
                        result = list[0]
                        list = list[1:]
                    elif length_difference < 0:
                        base_list = base_list[-length_difference:]
                    else:
                        raise Exception("oh noes the error buddy")
                    for base, item in zip(base_list, list):
                        result = result * base + item
                    return result

    # List and Set Operations (in progress)
    def Tuples(leaves, precision=None):
        if len(leaves) == 1:
            if hasattr(leaves[0].leaves[0], "leaves"):
                lists = list(map(lambda i: i.leaves, leaves[0].leaves))
                ls = [len(list) for list in lists]
                result = []
                n = len(lists)
                indices = [0] * n
                while True:
                    result += [[
                        lists[i][indices[i]] for i in range(n)
                    ]]
                    i = n - 1
                    indices[i] += 1
                    while i:
                        if indices[i] == ls[i]:
                            indices[i] = 0
                            i -= 1
                            indices[i] += 1
                        else:
                            break
                    if i == 0 and indices[i] == ls[0]:
                        break
                return List(*result)
        if len(leaves) == 2:
            if isinstance(leaves[1], Number):
                leaves[1] = List(leaves[1])
            lst = (
                leaves[0].leaves
                if len(leaves[1].leaves) == 1 else
                Wolfram.Tuples([leaves[0], List(*leaves[1].leaves[1:])]).leaves
            )
            head = leaves[0].head
            l = len(lst)
            result = []
            n = int(leaves[1].leaves[0])
            indices = [0] * n
            while True:
                result += [head(list(lst[i] for i in indices))]
                i = n - 1
                indices[i] += 1
                while i:
                    if indices[i] == l:
                        indices[i] = 0
                        i -= 1
                        indices[i] += 1
                    else:
                        break
                if i == 0 and indices[i] == l:
                    break
            return List(*result)

    def Subsets(leaves, precision=None):
        limit, result, indices, head = -1, [], None, leaves[0].head
        if len(leaves):
            length_range = range(len(leaves[0].leaves) + 1)
        if len(leaves) == 3:
            if isinstance(leaves[2], Number):
                limit = int(leaves[2])
                if limit == 0:
                    return List()
                leaves = leaves[:2]
            elif isinstance(leaves[2], List):
                length = len(leaves[2].leaves) 
                if length == 1:
                    indices = [int(leaves[2].leaves[0])]
                elif length == 2:
                    start = int(leaves[2].leaves[0])
                    end = int(leaves[2].leaves[1])
                    step = 1 if start <= end else -1
                    end += 1 if start <= end else -1
                    indices = range(start, end, step)
                elif length == 3:
                    step = int(leaves[2].leaves[2])
                    start = int(leaves[2].leaves[0])
                    end = int(leaves[2].leaves[1]) + (1 if step > 0 else -1)
                    indices = range(start, end, step)
        if len(leaves) == 2:
            if leaves[1] == All:
                leaves = leaves[:1]
            elif isinstance(leaves[1], Number):
                length_range = range(int(leaves[1]) + 1)
                leaves = leaves[:1]
            elif isinstance(leaves[1], List):
                if (
                    len(leaves[1].leaves) == 1 and
                    isinstance(leaves[1].leaves[0], Number)
                ):
                    length_range = [int(leaves[1].leaves[0])]
                elif (
                    len(leaves[1].leaves) == 2 and
                    isinstance(leaves[1].leaves[0], Number) and
                    isinstance(leaves[1].leaves[1], Number)
                ):
                    start = int(leaves[1].leaves[0])
                    end = int(leaves[1].leaves[1])
                    step = 1 if start <= end else -1
                    end += 1 if start <= end else -1
                    length_range = range(start, end, step)
                elif (
                    len(leaves[1].leaves) == 3 and
                    isinstance(leaves[1].leaves[0], Number) and
                    isinstance(leaves[1].leaves[1], Number) and
                    isinstance(leaves[1].leaves[2], Number)
                ):
                    step = int(leaves[1].leaves[2])
                    start = int(leaves[1].leaves[0])
                    end = int(leaves[1].leaves[1]) + (1 if step > 0 else -1)
                    length_range = range(start, end, step)
                leaves = leaves[:1]
        if indices:
            # TODO: decide when to enumerate all instead
            result = []
            for index in indices:
                index -= 1 # change to 0-based
                n = len(leaves[0].leaves)
                r = 0
                number = comb(n, r)
                while index >= number:
                    index -= number
                    r += 1
                    number = comb(n, r)
                deltas = []
                for dim in range(r, 0, -1):
                    delta = 0
                    if dim == 1:
                        deltas += [index]
                        continue
                    size = figurate(n - r - delta + 1, dim - 1)
                    while index >= size:
                        index -= size
                        delta += 1
                        size = figurate(n - r - delta + 1, dim - 1)
                    deltas += [delta]
                    n -= delta
                deltas += [0] * (r - len(deltas))
                new = []
                pos = -1
                for delta in deltas:
                    pos += delta + 1
                    new += [create_expression(leaves[0].leaves[pos])]
                result += [head(new)]
            return List(*result)
        if len(leaves) == 1:
            source = leaves[0].leaves
            l = len(source)
            length_range = list(filter(lambda i: i <= l, length_range))
            if 0 in length_range:
                result = [List()]
                if limit == 1:
                    return List(*result)
                length_range.remove(0)
            for i in length_range:
                js = list(range(i))
                indices = list(range(i))
                while True:
                    result += [head([source[indices[j]] for j in js])]
                    if len(result) == limit:
                        return List(*result)
                    if indices[-1] == l - 1:
                        k = len(indices) - 2
                        while k >= 0 and indices[k + 1] - indices[k] == 1:
                            k -= 1
                        if k < 0:
                            break
                        indices[k] += 1
                        while k + 1 < i:
                            indices[k + 1] = indices[k] + 1
                            k += 1
                    else:
                        indices[-1] += 1
            return List(*result)

    # predict (wat)

    def Predict(leaves, precision=None):
        # Assume List<Rule>
        pass

    # Constants

    def ChamperowneNumber(leaves, precision=None):

        def calculate_champerowne(precision, base=10):
            # TODO redo, it's not done at all
            if isinstance(precision, Expression):
                precision = precision.to_number()
            precision = max(precision - 1, 0)
            number = 0
            numerator = 10 ** (precision + 2)
            denominator = base
            multiplier = base
            i = 1
            next_power = base
            j = 1
            division = numerator // denominator
            while division:
                number = number + division
                denominator *= multiplier
                i += 1
                if i >= next_power:
                    number *= base
                    numerator *= base
                    multiplier *= base
                    next_power *= base
                    j += 1
                division = numerator // denominator
            return Real(
                number // (10 * next_power), -precision, precision=precision
            )

        return Expression(
            None, [],
            lambda precision=None: calculate_champerowne(precision, leaves[0])
        ) if len(leaves) else Expression(
            None, [], lambda precision=None: calculate_champerowne(precision)
        )

    # TODO: hide this function from scope
    def calculate_e(precision):
        if isinstance(precision, Expression):
            precision = precision.to_number()
        precision = max(precision - 1, 0)
        number = 0
        numerator = 10 ** (precision + 2)
        denominator = i = j = 1
        next_power_of_10 = 10
        division = numerator // denominator
        while division:
            number = number + division
            denominator *= i
            i += 1
            if i >= next_power_of_10:
                number *= 10
                numerator *= 10
                next_power_of_10 *= 10
                j += 1
            division = numerator // denominator
        return Real(
            number // (10 * next_power_of_10),
            -precision,
            precision=precision
        )

    E = Expression(
        None, [], lambda precision=None: Wolfram.calculate_e(precision)
    )

    # From https://www.craig-wood.com/nick/pub/pymath/pi_chudnovsky_bs.py

    def calculate_pi(precision):
        if isinstance(precision, Expression):
            precision = precision.to_number()
        precision = max(precision - 1, 0)
        # C = 640320,  C ** 3 // 24:
        C3_OVER_24 = 10939058860032000

        def pi_sqrt(n, one):
            floating_point_precision = 10**16
            n_float = (
                float((n * floating_point_precision) // one) /
                floating_point_precision
            )
            x = (
                int(floating_point_precision * sqrt(n_float)) * one
            ) // floating_point_precision
            n_one = n * one
            while 1:
                x_old = x
                x = (x + n_one // x) // 2
                if x == x_old:
                    break
            return x

        def bs(a, b):
            if b - a == 1:
                if a == 0:
                    Pab = Qab = 1
                else:
                    Pab = (6 * a - 5) * (2 * a - 1) * (6 * a - 1)
                    Qab = a * a * a * C3_OVER_24
                Tab = Pab * (13591409 + 545140134 * a)
                if a & 1:
                    Tab = -Tab
            else:
                m = (a + b) // 2
                Pam, Qam, Tam = bs(a, m)
                Pmb, Qmb, Tmb = bs(m, b)
                Pab, Qab, Tab = Pam * Pmb, Qam * Qmb, Qmb * Tam + Pam * Tmb
            return Pab, Qab, Tab

        N = (precision + 1) // 14 + 1
        _, Q, T = bs(0, N)
        one = 10 ** precision
        sqrtC = pi_sqrt(10005 * one, one)
        return Real((Q * 426880 * sqrtC) // T, -precision, precision=precision)

    Pi = Expression(
        None, [], lambda precision=None: Wolfram.calculate_pi(precision)
    )

    Degree = Pi / 180  # TODO: make sure this still accepts precision arg


def functionify(head, run=True):
    return (lambda *leaves: Expression(head, [
        leaf.run() if type(leaf) == Expression else leaf for leaf in leaves
    ])) if run else (lambda *leaves: Expression(head, leaves))


In = Integer
L = List
St = String
Sp = Span
Pa = Pattern
Rp = Repeated
RN = RepeatedNull
RE = RegularExpression
PT = PatternTest
Sh = Shortest
MR = MixedRadix

iq = integerQ
oq = oddQ
eq = evenQ
F = _False
T = _True
IC = IgnoreCase
Pi = Wolfram.Pi
E = Wolfram.E
Deg = Degree = Wolfram.Degree
Rt = Sqrt = functionify(Wolfram.Sqrt)
UT = UpTo = functionify(Wolfram.UpTo)
N = functionify(Wolfram.N, run=False)
SQ = StringQ = functionify(Wolfram.StringQ)
NQ = NumberQ = functionify(Wolfram.NumberQ)
IQ = IntegerQ = functionify(Wolfram.IntegerQ)
OQ = OddQ = functionify(Wolfram.OddQ)
EQ = EvenQ = functionify(Wolfram.EvenQ)
TQ = TrueQ = functionify(Wolfram.TrueQ)
FQ = FalseQ = functionify(Wolfram.FalseQ)
PAQ = PrintableAsciiQ = functionify(Wolfram.PrintableAsciiQ)
LQ = LetterQ = functionify(Wolfram.LetterQ)
LCQ = LowerCaseQ = functionify(Wolfram.LowerCaseQ)
UCQ = UpperCaseQ = functionify(Wolfram.UpperCaseQ)
DQ = DigitQ = functionify(Wolfram.DigitQ)
RD = RemoveDiacritics = functionify(Wolfram.RemoveDiacritics)
Fl = Flatten = functionify(Wolfram.Flatten)
SJ = StringJoin = functionify(Wolfram.StringJoin)
SL = StringLength = functionify(Wolfram.StringLength)
SS = StringSplit = functionify(Wolfram.StringSplit)
ST = StringTake = functionify(Wolfram.StringTake)
SD = StringDrop = functionify(Wolfram.StringDrop)
SP = StringPart = functionify(Wolfram.StringPart)
SR = StringReplace = functionify(Wolfram.StringReplace)
SCa = StringCases = functionify(Wolfram.StringCases)
SC = StringCount = functionify(Wolfram.StringCount)
SRf = StringRiffle = functionify(Wolfram.StringRiffle)
SPo = StringPosition = functionify(Wolfram.StringPosition)
SRe = StringRepeat = functionify(Wolfram.StringRepeat)
SDe = StringDelete = functionify(Wolfram.StringDelete)
SSQ = StringStartsQ = functionify(Wolfram.StringStartsQ)
SEQ = StringEndsQ = functionify(Wolfram.StringEndsQ)
SCQ = StringContainsQ = functionify(Wolfram.StringContainsQ)
RD = RemoveDiacritics = functionify(Wolfram.RemoveDiacritics)
Pr = Predict = functionify(Wolfram.Predict)
Ra = Range = functionify(Wolfram.Range)
FD = FromDigits = functionify(Wolfram.FromDigits)
Tu = Tuples = functionify(Wolfram.Tuples)
Su = Subsets = functionify(Wolfram.Subsets)
# TODO: make capital form arbitrary precision
l2 = Log2 = log2
la = Log10 = log10
ln = Log = log
rt = Rt = Sqrt = functionify(Wolfram.Sqrt)
# Sin = sin
# Cos = cos
# Tan = tan
# ArcSin = asin
# ArcCos = acos
# ArcTan = atan

for key, value in (
    (LetterQ, LetterCharacter),
    (LowerCaseQ, Pattern(r"\p{Ll}")),
    (UpperCaseQ, Pattern(r"\p{Lu}")),
    (DigitQ, DigitCharacter)
):
    pattern_test_lookup[key] = str(value)
