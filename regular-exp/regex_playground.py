line = 'This is a sample string'
print(1, "is" in line) # True
print(2, "xyz" in line) # false

import re
print(3, bool(re.search(r"is", line))) # true
print(4, bool(re.search(r"xzy", line))) # False

print(5, bool(re.search(r"this", line))) # False
print(6, bool(re.search(r"this", line, flags=re.I))) # true

# As Python evaluates None as False in boolean context,sre.search can be used directly in conditional expressions.
if re.search(r"ring", line):
    print(7, "mission successful!")

if not re.search(r"xyz", line):
    print(8, "mission failed!")

# some generator expression examples
words = ['cat', 'attempt', 'tattle']

filtered_words = [w for w in words if re.search(r"tt", w)]
print(9, filtered_words)

print(10, all(re.search(r"at", w) for w in words))
print(11, any(re.search(r"stat", w) for w in words))

greeting = 'Have a nice weekend'
# replace all occurrences of e with E
print(12, re.sub(r'e', 'E', greeting))