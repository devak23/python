import numpy as np

my_list = [1, 2, 3]
my_array = np.array(my_list)
print(my_array)
print(my_array.shape)  # which prints the rows and columns of an array.

##
# Prints: 
# [1 2 3]
# (3,) - 3 column single dimension array
# 

# Let's see how to create multi dimension array
my_list = [[1, 2, 3], [3, 4, 5]]
my_array = np.array(my_list)
print(my_array)
print(my_array.shape)

print(f"First row: {my_array[0]}")
print(f"Second row: {my_array[1]}")
print(f"Last row: {my_array[-1]}")
print(f"Specfic row: {my_array[0, 2]}")
print(f"Entire Column: {my_array[:, 2]}")

# Prints:
# [[1 2 3]
#  [3 4 5]]
# (2, 3)
# First row: [1 2 3]
# Second row: [3 4 5]
# Last row: [3 4 5]
# Specific row: 3
# Entire Column: [3 5]
#

# Let's do some math operations
my_array1 = np.array([1, 2, 3])
my_array2 = np.array([11, 22, 33])
print(f"Addition = {my_array1 + my_array2}")
print(f"Multiplication = {my_array1 * my_array2}")

# Prints:
# Addition = [12 24 36]
# Multiplication = [11 44 99]
