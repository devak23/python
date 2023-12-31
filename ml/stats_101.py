import numpy as np
from scipy import stats

heart_rate_sample = np.array([80, 79, 66, 70, 77, 65, 81, 71, 78, 66, 68, 67, 64, 71, 82, 69])
heart_rate_mean = np.mean(heart_rate_sample)
print(heart_rate_mean)

median_heart_rate = np.median(heart_rate_sample)
print(median_heart_rate)

mode_heart_rate = stats.mode(heart_rate_sample)
print(mode_heart_rate)
