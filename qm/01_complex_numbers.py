import numpy as np

z = 3 + 4j
# Phasor equivalent of the complex number a + bi = Re^itheta = Rcos(theta) + Rsin(theta)
R = abs(z) # R = sqrt(sqr(a) + sqr(b))
print("R = {}".format(R))
theta = np.arctan2(z.imag, z.real) # theta = tan^-1(b/a) = tan^-1 (4/3)
print ("theta (in radians) = {}".format(theta)) # 1 radian = 57.2958 degrees
print("theta (in degrees) = {}".format(np.degrees(theta)))

# output:
# R = 5.0
# theta = 53.13010235415598


# Given a complex number: z = 2ei 6 . What is its cartesian form?
# a = R cos θ = 2 cos(π/6) = 2√3/2 = √3
# b = R sin θ = 2 sin(π/6) = 2(1/2) = 1

R1 = 2
theta1 = np.pi / 6
z1 = R * np.exp(1j * theta1)
print("z1 = {}".format(z1))

# output: z1 = (4.330127018922194 + 2.4999999999999996j)


# So, you recall complex number has a real part (a) and an imaginary part (b), or equivalently, a magnitude (R) and a
# phase (θ). Remember that a function is a kind of recipe that converts arguments (inputs) into a value (output).
# Quantum mechanics is built around special functions, called wavefunctions that have real arguments (e.g., position,
# x, or time, t), but whose value (output) is a complex number. One of the most frequently encountered complex functions
# in quantum mechanics is the complex exponential, like so:
#                                       φ(t) = Ae−iωt
# In most cases, ω and t are real numbers and contribute only to the phase angle of the complex number. If we think of
# φ(t) as a phasor, it would be an arrow of fixed length A rotating clockwise in the complex plane with an angular
# velocity of ω radians per second.

#import vpython as vp