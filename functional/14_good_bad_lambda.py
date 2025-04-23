from typing import List


# concise but affects legibility
def sum_square_or_cubes(numbers: List[int]) -> int:
    return sum([n**2 if n%2 == 0 else n**3  for n in numbers])

# legible but not concise.
def complex_function(numbers: List[int]) -> int:
    result = 0
    for n in numbers:
        if n % 2 == 0:
            result += n ** 2
        else:
            result += n ** 3
    return result

# legibility ALWAYS has to be the top precedence.

numbers = [1, 2, 3, 4, 5]
print(sum_square_or_cubes(numbers))
print(complex_function(numbers))

# The point of anonymous/lambda function is to make simpler functions that are easy to read and write.
# if we had to multiply the numbers instead of adding them, then sum_of_square_or_cubes which uses the list
# comprehension doesn't have anything like a product() which will readily give us a product of all numbers. Then, the
# fully blown complex_function is useful! Its not like you cannot do that. There are other libraries like the builtin
# functools which provides the reduce function which achieves the same result.

from functools import reduce

complex_op = lambda n1: reduce(lambda acc, n: acc * (n ** 2 if n%2 == 0 else n**3), n1, 1)
print(complex_op(numbers))

p = lambda anything: print(anything)

p((lambda s: s.upper())("i am a tea pot, short and stout. this is my handle and this is my spout"))