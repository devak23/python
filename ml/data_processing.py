# we are rescaling the data between 0 and 1

from numpy import set_printoptions
from pandas import read_csv
from sklearn.preprocessing import MinMaxScaler

col_names = ['Preg', 'Glucose', 'BP', 'Skin T', 'Insulin', 'BMI', 'D Pedigree',
             'Age', 'Outcome']

data = read_csv('pima-indians-diabetes.csv')
array = data.values

## Separate the array into input and output components
X = array[:, 0:8]  # input component
y = array[:, 8]  # output component

print("------------------X----------------------")
print(X)
print("------------------Y----------------------")
print(y)

# Scaling the data
scaler = MinMaxScaler(feature_range=(0, 1))
rescaledX = scaler.fit_transform(X)

# summarize transformed data
set_printoptions(precision=3)
print(rescaledX[0:5, :])
