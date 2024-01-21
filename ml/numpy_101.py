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
print(f"my_array = {my_array}")
print(f"my_array.shape = {my_array.shape}")

print(f"First row: {my_array[0]}")
print(f"Second row: {my_array[1]}")
print(f"Last row: {my_array[-1]}")
print(f"Specific row: {my_array[0, 2]}")
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

# you can also create a predetermined numpy array using arange:
print (f"np.arange(0,10) = {np.arange(0,10)}")
print (f"np.arange(0,11,2) = {np.arange(0,11,2)}")

# many a times you just need an array of zero's or ones. Numpy has a convenient way of doing this:
print(f"np.zeros(3) = {np.zeros(3)}")
# Prints: np.zeros(3) = [0. 0. 0.]

# you could also pass in a shape object to the zeros function
print(f"np.zeros((4,4)) = {np.zeros((4,4))}")

# Prints: np.zeros((4,4)) = [[0. 0. 0. 0.]
#  [0. 0. 0. 0.]
#  [0. 0. 0. 0.]
#  [0. 0. 0. 0.]]

print (f"np.ones((4,5)) = {np.ones((4,5), dtype=int)}")
# Prints: np.ones((4,5)) = [[1 1 1 1 1]
#  [1 1 1 1 1]
#  [1 1 1 1 1]
#  [1 1 1 1 1]]

# np.linspace also creates the array but with a starting point, stopping point and a bunch of evenly placed points
# between start to end
print (f"np.linspace(0,10,3) = {np.linspace(0,10,3)}")
# Prints: np.linspace(0,10,3) = [ 0.  5. 10.]

# if we ask for say 21 evenly points this is what it does:
print (f"np.linspace(0,10,21) = {np.linspace(0,10,21)}")
# Prints: np.linspace(0,10,21) = [ 0.   0.5  1.   1.5  2.   2.5  3.   3.5  4.   4.5  5.   5.5  6.   6.5
#   7.   7.5  8.   8.5  9.   9.5 10. ]

# Numpy can also create an identity matrix using the following:
print(f"np.eye(5) = {np.eye(5)}") # will create an identity matrix of 5x5 with the diagonal column being all ones
# Prints: np.eye(5) = [[1. 0. 0. 0. 0.]
#  [0. 1. 0. 0. 0.]
#  [0. 0. 1. 0. 0.]
#  [0. 0. 0. 1. 0.]
#  [0. 0. 0. 0. 1.]]

# np.random.rand(2) gives us 2 random numbers with "uniform distribution"
print(f"np.random.rand(2) = {np.random.rand(2)}")
# Prints: np.random.rand(2) = [0.84808011 0.51534289]

# You could also pull something off of the normal distribution
print(f"np.random.randn(3) = {np.random.randn(3)}") # mean = 0, variance=1
# Prints: np.random.randn(3) = [ 0.54066396  0.14694954 -0.78950803]

# We can grab some random integers too
print(f"np.random.randint(-5, 5, 2) = {np.random.randint(-5, 5, 2)}") # the 2 specifies how many numbers are to be generated
# Prints: np.random.randint(5) = [0 4]

# You could also specify the shape as such
print(f"np.random.randint(1,100, (2,3)) = {np.random.randint(0, 100, (2, 3))}")
# Prints: np.random.randint(1,100, (2,3) = [[78 80  3]
#  [43 37 54]]

# Let's do some math operations
my_array1 = np.array([1, 2, 3])
my_array2 = np.array([11, 22, 33])
print(f"Addition = {my_array1 + my_array2}")
print(f"Multiplication = {my_array1 * my_array2}")
# Prints:
# Addition = [12 24 36]
# Multiplication = [11 44 99]

# Let's generate random numbers from 0 to 50
print(f"np.random.randint(0,50,10) = {np.random.randint(0,50,10)}" )
# Prints: np.random.randint(0,50,10) = [14 40 40 12 30 10  8 21 18 32]