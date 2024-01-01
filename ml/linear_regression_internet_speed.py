#!/usr/bin/env python
# coding: utf-8

import matplotlib.pyplot as plt
from scipy import stats


# define data X and y arrays
"""
age_x = [4,6,7,6,1,16,1,8,3,10,11,8,5]
capacity_y = [98,85,86,89,112,85,101,84,93,79,76,82,81]
"""
"""
# data with correct fit
age_x = [4,6,7,6,1,16,1,8,3,10,11,8,5]
capacity_y = [14,35,48,36,1,254,2,63,9,99,120,62,25]
"""

# data with worst fit
x_hour = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22]
y_internet_speed = [101,89,81,60,60,53,58,65,70,69,75,76,77,79,90,99,99,89,87,90,92,100]

slope, intercept, r, p, std_error = stats.linregress(x_hour, y_internet_speed)
print (f"slope = {slope}, intercept = {intercept}, r = {r}, p = {p} and std_error = {std_error}")


def new_y(x):
    return slope * x + intercept


regressed_values = list(map(new_y, x_hour))

plt.scatter(x_hour, y_internet_speed, label="Original data")
plt.plot(x_hour, regressed_values, "r", label="Fitted Line")
plt.xlabel("Age of the machine")
plt.ylabel("Capacity of machine")
plt.legend()
plt.show()




