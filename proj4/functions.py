import config
import math

def threshold( sigma ):
	if sigma > config.THETA:
		return 1
	return 0

def binary_sigmoid( sigma ):
	return (1 / (1 + math.exp(-1 * sigma)))

def bipolar_sigmoid( sigma ):
	return ((2 / (1 + math.exp(-1 * sigma))) - 1)

def hyperbolic_tangent( sigma ):
	num = math.exp(sigma) - math.exp(-1 * sigma)
	den = math.exp(sigma) + math.exp(-1 * sigma)

	return num / den
