# Define a single lambda function named ternary that simulates a ternary operation to evaluate the sign of a given number.
# the function should take single argument which is the number to be evaluated and return one of the 3 strings:
# positive, negative or zero depending on the sign of the number

p = lambda anything: print(anything)

ternary = lambda x: "Zero" if x == 0 else "Positive" if x > 0 else "Negative"

p(ternary(5))
p(ternary(0))
p(ternary(-5))