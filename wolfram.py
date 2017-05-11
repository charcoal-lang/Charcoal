from math import (
    log, log2, log10, sqrt, sin, cos, tan, asin, acos, atan,
    floor, ceil
)
from functools import reduce, lru_cache

# TODO: overload int() in interpreterprocessor + import into charcoal
# TODO: make sure everything is lazily evaluated
# TODO: conservative precision
# e.g. operations for rounded values
# TODO: chain plus/minus for less precision needed
# TODO: implement precision (log10, idk fastest way to do)
# currently we only have exponent

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

def headify(clazz):
    return lambda leaves, precision=10: clazz(*leaves)

def create_expression(value):

    if isinstance(value, Expression):
        return value

    elif isinstance(value, complex):
        return Complex(value)

    elif value % 1:
        exponent = 0
        
        while value % 1:
            value *= 10
            exponent -= 1

        return Real(value, exponent)

    else:
        exponent = 0
        
        while not value % 10:
            value //= 10
            exponent += 1

        return Integer(value, exponent)

class Expression:
    def __init__(self, head=None, leaves=[], run=None):
        self.head = head
        self.leaves = [create_expression(leaf) for leaf in leaves]

        if run:
            self.run = lambda precision=10: run(precision)

        else:
            self.run = lambda precision=10: self.head(self.leaves, precision)
            
    def __add__(self, other):

        return Expression(
            None,
            [],
            lambda precision=10: (
                self.run(precision + 2) + (
                    create_expression(other).run(precision + 2)
                )
            ).to_precision(precision)
        )

    def __sub__(self, other):

        return Expression(
            None,
            [],
            lambda precision=10: (
                self.run(precision + 2) - (
                    create_expression(other).run(precision + 2)
                )
            ).to_precision(precision)
        )

    def __mul__(self, other):

        return Expression(
            None,
            [],
            lambda precision=10: (
                self.run(precision + 2) * (
                    create_expression(other).run(precision + 2)
                )
            ).to_precision(precision)
        )
    
    def __truediv__(self, other):

        return Expression(
            None,
            [],
            lambda precision=10: (
                self.run(precision + 2) / (
                    create_expression(other).run(precision + 2)
                )
            ).to_precision(precision)
        )

    def to_number(self):
        return self.run().to_number()

    def to_precision(self, precision=10):
        return self.run().to_precision(precision)

    def is_integer(self):
        return self.run().is_integer()

    def is_odd(self):
        return self.run().is_odd()

    def is_even(self):
        return self.run().is_even()

class Number(Expression):
    def __init__(self, head=None):
        super().__init__(head=head)

class Real(Number):
    def __init__(self, value, exponent=0):
        super().__init__(head=headify(Real))
        self.leaves = [value, exponent]

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
        
        if type(other) == Expression:
            return other + self

    def __mul__(self, other):
        
        if type(other) == Expression:
            return other * self

        if type(other) == Real:
            return Real(
                self.leaves[0] * other.leaves[0],
                self.leaves[1] + other.leaves[1]
            )

        if type(other) == Rational or type(other) == Complex:
            return other * self

        return self * Real(other)

    def __truediv__(self, other):

        if isinstance(other, Real):
            # TODO: multiply by 10**n
            return Real(
                self.leaves[0] // other.leaves[0],
                self.leaves[1] - other.leaves[1]
            )

        if type(other) == Rational:
            pass
            
        if type(other) == Complex:
            pass # TODO

    def to_number(self):
        return self.leaves[0] * 10 ** self.leaves[1]
    
    def to_precision(self, precision=10):
        return Real(
            self.leaves[0] // (10 ** (self.leaves[1] + precision)),
            -precision
        )

    def is_integer(self):
        return Integer(self.leaves[1] >= 0)

    def is_odd(self):
        return Integer(
            self.leaves[1] > 0 or self.leaves[1] == 0 and (
                self.leaves[0] % 2 == 1
            )
        )

    def is_even(self):
        return Integer(
            self.leaves[1] > 0 or self.leaves[1] == 0 and (
                self.leaves[0] % 2 == 0
            )
        )

class Integer(Real):
    def __init__(self, value, exponent=0):
        super().__init__(value, exponent)
        self.head = headify(Integer)

    def __str__(self):
        string = str(self.leaves[0])
        return (
            string + "0" * self.leaves[1]
            if self.leaves[1] != 0 else
            string
        )

    def __repr__(self):
        return str(self)
    
    def to_number(self):
        return self.leaves[0] * 10 ** self.leaves[1]
    
    def to_precision(self, precision=10):
        return Real(
            self.leaves[0] * 10 ** precision,
            self.leaves[1] - precision
        )

    def is_integer(self):
        return One

    def is_odd(self):
        return Integer(
            self.leaves[1] > 0 or self.leaves[1] == 0 and (
                self.leaves[0] % 2 == 1
            )
        )

    def is_even(self):
        return Integer(
            self.leaves[1] > 0 or self.leaves[1] == 0 and (
                self.leaves[0] % 2 == 0
            )
        )

One = Integer(1)

class Rational(Number):
    def __init__(self, numerator, denominator, exponent=0):
        super().__init__(head=headify(Rational))
        gen = prime_gen()
        square = 0
        
        while numerator % 1:
            numerator *= 10
            exponent -= 1
        
        while denominator % 1:
            denominator *= 10
            exponent += 1
        
        numerator, denominator = int(numerator), int(denominator)

        while numerator > square and denominator > square:
            prime = next(gen)
            square = prime * prime

            while (not numerator % prime) and (not denominator % prime):
                numerator //= prime
                denominator //= prime

        self.leaves = [numerator, denominator, exponent]
        # TODO: use Integer for numerator and denominator

        # TODO: make it create integer directly somehow
        if denominator == 1:
            self.run = lambda precision=10: (
                Integer(self.leaves[0], self.leaves[3])
            )

    def __str__(self):
        return str(self.leaves[0]) + "/" + str(self.leaves[1])

    def __repr__(self):
        return str(self)
        
    def __add__(self, other):

        if isinstance(other, Expression):
            return other + self

    def __mul__(self, other):

        if isinstance(other, Expression):
            return other * self
        # TODO: lazy
        if isinstance(other, Rational):
            return Rational(
                self.leaves[0] * other.leaves[0],
                self.leaves[1] * other.leaves[1]
            )
    
    def __truediv__(self, other):
        # TODO: lazy
        if isinstance(other, Rational):
            return Rational(
                self.leaves[0] * other.leaves[1],
                self.leaves[1] * other.leaves[0]
            )

    def to_number(self):
        return float(self.leaves[0]) / self.leaves[1]
        
    def to_precision(self):
        # TODO
        pass

    def is_integer(self):
        return Integer(self.leaves[1] == 1)

    def is_odd(self):
        return Integer(self.leaves[1] == 1 and (self.leaves[0] % 2 == 1))

    def is_even(self):
        return Integer(self.leaves[1] == 1 and (self.leaves[0] % 2 == 0))

class Complex(Number):
    def __init__(self, real, imaginary=0):
        super.__init__(head=headify(Complex))

        if isinstance(real, complex):
            self.real = create_expression(real).run()
            self.imaginary = create_expression(imaginary).run()

        self.real = real
        self.imaginary = imaginary

    def __str__(self):
        return str(self.real) + " + " + str(self.imaginary) + "j"
    
    def __repr__(self):
        return str(self)

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

#TODO: round, log

class Wolfram:

    def Head(leaves, precision=10):
        return leaves[0].head

    def N(leaves, precision=10):
        # Leaves: number, precision (accuracy?)
        return [
            None,
            lambda: leaves[0].run(10),
            lambda: leaves[0].run(leaves[1])
        ][len(leaves)]()
    
    def IntegerQ(leaves, precision=10):
        return leaves[0].is_integer()
    
    def OddQ(leaves, precision=10):
        return leaves[0].is_odd()
    
    def EvenQ(leaves, precision=10):
        return leaves[0].is_even()
    
    def Sqrt(leaves, precision=10):

        def calculate_sqrt(n, precision):
        
            if isinstance(precision, Expression):
                precision = precision.to_number()

            result = int(sqrt(n) * 10 ** precision)
            n *= 10 ** (precision * 2)
            difference = result * result - n
        
            while difference >= result or difference <= -result:
                result = result - int(0.5 + difference / (2 * result))
                difference = result * result - n
        
            while not result % 10:
                result //= 10
                precision -= 1
        
            return Real(result, -precision)

        return Wolfram.calculate_sqrt(leaves[0].to_number(), precision)
    
    ### Constants

    # TODO: hide this function from scope
    def calculate_e(precision):
        
        if isinstance(precision, Expression):
            precision = precision.to_number()

        precision = max(precision - 1, 0)
        number = 0
        numerator = 10 ** (precision + 2)
        denominator = 1
        i = 1
        next_power_of_10 = 10
        j = 1
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
        return Real(number // (10 * next_power_of_10), -precision)

    E = Expression(
        None, # TODO: leaf for E, Pi and Degree
        [],
        lambda precision=10: Wolfram.calculate_e(precision)
    )

    # From https://www.craig-wood.com/nick/pub/pymath/pi_chudnovsky_bs.py

    def calculate_pi(precision):
        
        if isinstance(precision, Expression):
            precision = precision.to_number()
        
        precision = max(precision - 1, 0)
        C = 640320
        C3_OVER_24 = C ** 3 // 24
    
        def pi_sqrt(n, one):
            floating_point_precision = 10**16
            n_float = (
                float((n * floating_point_precision) // one) /
                floating_point_precision
            )
            x = (
                int(floating_point_precision *
                sqrt(n_float)) * one
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
        N = int(precision / DIGITS_PER_TERM + 1)
        _, Q, T = bs(0, N)
        one = 10 ** precision
        sqrtC = pi_sqrt(10005 * one, one)
        return Real((Q * 426880 * sqrtC) // T, -precision)
    
    Pi = Expression(
        None,
        [],
        lambda precision=10: Wolfram.calculate_pi(precision)
    )
    
    Degree = Pi / 180 # TODO: make sure this still accepts precision arg

def functionify(head):
    return lambda *leaves: Expression(head, leaves)

iq = integerQ
oq = oddQ
eq = evenQ
Pi = Wolfram.Pi
E = Wolfram.E
Degree = Wolfram.Degree
Iq = IntegerQ = functionify(Wolfram.IntegerQ)
Oq = OddQ = functionify(Wolfram.OddQ)
Eq = EvenQ = functionify(Wolfram.EvenQ)
N = functionify(Wolfram.N)
# TODO: make capital form arbitrary precision
l2 = Log2 = log2
la = Log10 = log10
ln = log
rt = functionify(Wolfram.Sqrt)
#Sin = sin
#Cos = cos
#Tan = tan
#ArcSin = asin
#ArcCos = acos
#ArcTan = atan