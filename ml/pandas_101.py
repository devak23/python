import numpy as np
import pandas as pd

# construct a series
my_array = np.array([1, 2, 3, 4])
row_names = ['a', 'b', 'c', 'd']

my_series = pd.Series(data=my_array, index=row_names)
print(my_series)
print(f"3rd element is: {my_series['c']}")

# construct a DataFrame

my_array = np.array([[1, 2, 3], [4, 5, 6]])
row_names = ['a', 'b']
column_names = ['one', 'two', 'three']

my_dataframe = pd.DataFrame(data=my_array, index=row_names, columns= column_names)
print(my_dataframe)
# prints the following:
#    one  two  three
# a    1    2      3
# b    4    5      6

print(f"3b corresponds to: {my_dataframe['three']['b']}")