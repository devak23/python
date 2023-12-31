import numpy as np
from scipy import stats
from matplotlib import pyplot as plt

# mean
heart_rate_sample = np.array([80, 79, 66, 70, 77, 65, 81, 71, 78, 66, 68, 67, 64, 71, 82, 69])
heart_rate_mean = np.mean(heart_rate_sample)
print(f"mean heart rate = {heart_rate_mean}")

# median
median_heart_rate = np.median(heart_rate_sample)
print(f"median heart rate = {median_heart_rate}")

# mode
mode_heart_rate = stats.mode(heart_rate_sample)
print(f"mode heart rate = {mode_heart_rate}")

# variance
var_heart_rate = np.var(heart_rate_sample)
print(f"variance in heart rates = {var_heart_rate}")

# standard deviation
std_dev_heart_rate = np.std(heart_rate_sample)
print(f"standard deviation in heart rate = {std_dev_heart_rate}")

# percentile
_50_percentile_heart_rate = np.percentile(heart_rate_sample, 50)
print(f"Heart rate of 50 percentile people = {_50_percentile_heart_rate}")

_10_percentile_heart_rate = np.percentile(heart_rate_sample, 10)
print(f"Heart rate of 10 percentile people = {_10_percentile_heart_rate}")

# uniform dataset
heart_rates = np.random.uniform(60, 100, 500)
print("#############################################################################")
print(f"Uniform Dataset: {heart_rates}")
# in this case the distribution is not normal because each point has equal weightage.

plt.hist(heart_rates)
plt.show()


# let's create a normal dataset with a standard deviation of 5 with a mean of 72 having 500 data points
heart_rates = np.random.normal(loc=72, scale=5, size=500)
print("#############################################################################")
print(f"normal dataset = {heart_rates}")
plt.hist(heart_rates)
plt.show()
