import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

col_names = ['Preg', 'Glucose', 'BP', 'Skin T', 'Insulin', 'BMI', 'D Pedigree',
             'Age', 'Outcome']

data = pd.read_csv('pima-indians-diabetes.csv', names=col_names)
correlations = data.corr()

# define a figure using the pyplot class
fig = plt.figure()
ax = fig.add_subplot(111)  # define 111 subplots
cax = ax.matshow(correlations, vmin=-1, vmax=1) # define vertical max and min for the graph
fig.colorbar(cax)

ticks = np.arange(start=0, stop=9, step=1)
ax.set_xticks(ticks)
ax.set_yticks(ticks)
ax.set_xticklabels(col_names)
ax.set_yticklabels(col_names)
plt.show()