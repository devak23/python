import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix

col_names = ['Preg', 'Glucose', 'BP', 'Skin T', 'Insulin', 'BMI', 'D Pedigree',
             'Age', 'Outcome']

data = pd.read_csv("pima-indians-diabetes.csv", names=col_names)
scatter_matrix(data)
plt.show()