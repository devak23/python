#!/usr/bin/env python
# coding: utf-8


import matplotlib.pyplot as plt
from scipy import stats
import numpy as np



# define x an y arrays
age_x = [4,6,7,6,1,16,1,8,3,10,11,5]
capacity_y = [98,85,86,89,112,85,101,84,93,79,76,82]



# calculating the linear regression using linregress function
slope, intercept, r, p, std_error = stats.linregress(age_x, capacity_y)
print (f"slope = {slope}, intercept = {intercept}, r = {r}, p = {p} and std_error = {std_error}")



def new_y(x):
    return slope * x + intercept



regressed_values = list(map(new_y, age_x))

plt.scatter(age_x, capacity_y, label="Original data")
plt.plot(age_x, regressed_values, "r", label="fitted line")
plt.xlabel("machine age")
plt.ylabel("machine capacity")
plt.legend()

print(f"regression coefficient: {r}")
