from math import log, log2, log10, sqrt

# TODO: arbitrary precision, don't round until value requested
# to do this, overload int() in interpreterprocessor, import into charcoal

class WolframObject:
	def __init__(self, value):
		self.value = value

	def to_int(self):
		pass

# TODO: trig functions

def IntegerQ(number):
	return int(
		isinstance(number, int) or
		(isinstance(number, float) and not (number % 1))
	)

def OddQ(number):
	return int(IntegerQ(number) and number % 2)

def EvenQ(number):
	return int(IntegerQ(number) and not (number % 2))

def Log(base, number=None):

	if number is None:
		return log(base)

	return round(log(number, base), 10)

iq = IntegerQ
oq = OddQ
eq = EvenQ
l2 = Log2 = log2
la = Log10 = log10
ln = log = Log
rt = Sqrt = sqrt