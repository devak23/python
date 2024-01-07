# following plotting gives us nature of data distribution. These are univariate plots

import matplotlib.pyplot as plt
import pandas as pd

col_names = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction',
             'Age', 'Outcome']

data = pd.read_csv('pima-indians-diabetes.csv', names=col_names)
# histogram plot
data.hist()
plt.show()

# density plot
data.plot(kind='density', subplots=True, layout=(3,3), sharex=False)
plt.show()

# box and whisker plot
data.plot(kind='box', subplots=True, layout=(3,3), sharex=False, sharey=False)
plt.show()