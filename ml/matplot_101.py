# we will attempt to plot a basic line chart using matplotlib

import matplotlib.pyplot as plt
import numpy as np

# let's plot fibonacci series
my_array = np.array([1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144])
plt.plot(my_array)
plt.xlabel("units")
plt.ylabel("fibonacci series")
plt.show()

# let's plot histogram
my_array2 = np.array([10, 10, 20, 30, 30, 30, 40, 40, 50, 50, 50, 50])
plt.hist(my_array2)
plt.xlabel("units")
plt.ylabel("frequency")
plt.show()

# let's use a scatter plot
x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
y = np.array(x * (1 + 0.2))
print(y)
plt.scatter(x, y)
plt.xlabel("Months")
plt.ylabel("Gain")
plt.show()
