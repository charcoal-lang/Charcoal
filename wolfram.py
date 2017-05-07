from math import (
    log, log2, log10, sqrt, sin, cos, tan, asin, acos, atan,
    floor, ceil
)
from functools import reduce, lru_cache

# TODO: overload int() in interpreterprocessor + import into charcoal
# TODO: make sure everything is lazily evaluated

prime_cache = [2, 3]

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


class WolframObject:
    def __init__(self, value, run=None, head=None):
        self.value = value
        self.head = head
        if run:
            self.run = lambda precision=10: run(self, precision)
        else:
            self.run = lambda precision=10: self

    def to_number(self):
        return self.run().to_number()

    def is_integer(self):
        return self.run().is_integer()

    def is_odd(self):
        return self.run().is_odd()

    def is_even(self):
        return self.run().is_even()

class WolframNumber(WolframObject):
    def __init__(self, value, exponent=0, head=None):
        super().__init__([self], head=head)

        if isinstance(value, WolframNumber):
            self.run = lambda precision=10: value

        elif isinstance(value, complex):
            self.run = lambda precision=10: Complex(value)

        elif value % 1:
            self.run = lambda precision=10: Real(value)

        else:
            self.run = lambda precision=10: Integer(value)

class Real(WolframNumber):
    def __init__(self, value, exponent=0):
        super().__init__(self, head=Real)

        if isinstance(value, int):

            while value and not value % 10:
                value //= 10
                exponent += 1

        if isinstance(value, float):

            while value % 1:
                value *= 10
                exponent -= 1

            value = int(value)

        self.value = value
        self.exponent = exponent

    def __str__(self):
        string = str(self.value)
        zeroes = 1 - self.exponent - len(string)

        if zeroes > 0:
            string = "0" * zeroes + string

        return (
            string + "0" * self.exponent
            if self.exponent > 0 else
            (string[:self.exponent] + "." + string[self.exponent:])
            if self.exponent < 0 else
            string
        )

    def __repr__(self):
        return str(self)

    def __mul__(self, other):

        if isinstance(other, Real):
            return Real(
                self.value * other.value,
                self.exponent + other.exponent
            )

        if isinstance(other, Rational) or isinstance(other, Complex):
            return other * self

        return self * Real(other)

    def __div__(self, other):
        if isinstance(other, Real):
            return Rational(
                self.value,
                other.value,
                self.exponent - other.exponent
            )

        if isinstance(other, Rational) or isinstance(other, Complex):
            return other / self

        return self / Real(other)

    def to_number(self):
        return self.value * 10 ** self.exponent

    def is_integer(self):
        return int(self.exponent >= 0)

    def is_odd(self):
        return int(
            self.exponent > 0 or self.exponent == 0 and (self.value % 2 == 1)
        )

    def is_even(self):
        return int(
            self.exponent > 0 or self.exponent == 0 and (self.value % 2 == 0)
        )

class Integer(Real):
    def __init__(self, value, exponent=0):
        super().__init__(value, exponent)
        self.head = Integer

    def __str__(self):
        string = str(self.value)
        return (
            string + "0" * self.exponent
            if self.exponent != 0 else
            string
        )

    def __repr__(self):
        return str(self)

    def is_integer(self):
        return 1

    def is_odd(self):
        return int(
            self.exponent > 0 or self.exponent == 0 and (self.value % 2 == 1)
        )

    def is_even(self):
        return int(
            self.exponent > 0 or self.exponent == 0 and (self.value % 2 == 0)
        )

class Rational(WolframNumber):
    def __init__(self, numerator, denominator, exponent=0):
        super().__init__([self], head=Rational)
        gen = prime_gen()
        square = 0

        while numerator > square and denominator > square:
            prime = next(gen)
            square = prime * prime

            while (not numerator % prime) and (not denominator % prime):
                numerator //= prime
                denominator //= prime

        self.numerator = numerator
        self.denominator = denominator
        self.exponent = exponent

        if denominator == 1:
            self.run = lambda: Real(self.numerator, self.exponent)

    def __str__(self):
        return str(self.numerator) + "/" + str(self.denominator)

    def __repr__(self):
        return str(self)

    def __mul__(self, other):
        # TODO: lazy
        if isinstance(other, Rational):
            return Rational(
                self.numerator * other.numerator,
                self.denominator * other.denominator
            )
    
    def __div__(self, other):
        # TODO: lazy
        if isinstance(other, Rational):
            return Rational(
                self.numerator * other.numerator,
                self.denominator * other.denominator
            )

    def to_number(self):
        return float(self.numerator) / self.denominator

    def is_integer(self):
        return int(self.denominator == 1)

    def is_odd(self):
        return int(self.denominator == 1 and (self.numerator % 2 == 1))

    def is_even(self):
        return int(self.denominator == 1 and (self.numerator % 2 == 0))

class Complex(WolframNumber):
    def __init__(self, real, imaginary=0):

        if isinstance(real, complex):
            self.real = WolframNumber(real).run()
            self.imaginary = WolframNumber(imaginary).run()

        self.real = real
        self.imaginary = imaginary

    def __str__(self):
        return str(self.real) + " + " + str(self.imaginary) + "j"

math_sqrt = sqrt

# From https://www.craig-wood.com/nick/pub/pymath/pi_chudnovsky_bs.py

def calculate_pi(digits):
    # TODO: memoize of possible
    C = 640320
    C3_OVER_24 = C ** 3 // 24

    def sqrt(n, one):
        floating_point_precision = 10**16
        n_float = (
            float((n * floating_point_precision) // one) /
            floating_point_precision
        )
        x = (
            int(floating_point_precision *
            math_sqrt(n_float)) * one
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
            Pab = Pam * Pmb
            Qab = Qam * Qmb
            Tab = Qmb * Tam + Pam * Tmb

        return Pab, Qab, Tab

    DIGITS_PER_TERM = log10(C3_OVER_24 / 6 / 2 / 6)
    N = int(digits / DIGITS_PER_TERM + 1)
    P, Q, T = bs(0, N)
    one = 10 ** digits
    sqrtC = sqrt(10005 * one, one)
    return Real((Q * 426880 * sqrtC) // T, -digits)

Pi = WolframObject(
    [],
    lambda self, precision=10: calculate_pi(precision)
)

def integerQ(number):
    return int(
        isinstance(number, int) or
        (isinstance(number, float) and not (number % 1))
    )

def IntegerQ(number):
    if not isinstance(number, WolframObject):
        number = WolframNumber(number)

    return WolframObject(
        [number],
        lambda self, precision=10: Integer(
            self.value[0].run(precision).is_integer()
        )
    )

def oddQ(number):
    return int(IntegerQ(number) and number % 2)

def OddQ(number):
    if not isinstance(number, WolframObject):
        number = WolframNumber(number)

    return WolframObject(
        [number],
        lambda self, precision=10: Integer(
            self.value[0].run(precision).is_odd()
        )
    )

def evenQ(number):
    return int(IntegerQ(number) and not (number % 2))

def EvenQ(number):
    if not isinstance(number, WolframObject):
        number = WolframNumber(number)

    return WolframObject(
        [number],
        lambda self, precision=10: Integer(
            self.value[0].run(precision).is_even()
        )
    )

def round(number, digits=0):
    return int(integerQ(number) and not (number % 2))

def Round(number, digits=0):
    if not isinstance(number, WolframObject):
        number = WolframNumber(number)

    return WolframObject(
        [number],
        lambda self, precision=10: self.value[0].run(digits)
    )

def Head(obj):
    # assumes obj is WolframObject

    def _head(obj, precision):
        return obj.head or _head(obj.run(precision))

    return WolframObject(
        [obj],
        lambda self, precision=10: _head(obj)
    )

def Log(base, number=None):

    if number is None:
        return log(base)

    return round(log(number, base), 10)

iq = integerQ
oq = oddQ
eq = evenQ
Iq = IntegerQ
Oq = OddQ
Eq = EvenQ
# TODO: make these arbitrary precision
l2 = Log2 = log2
la = Log10 = log10
ln = log = Log
rt = Sqrt = sqrt
Sin = sin
Cos = cos
Tan = tan
ArcSin = asin
ArcCos = acos
ArcTan = atan
rnd = Round