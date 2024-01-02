import pandas as pd

col_names = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction',
             'Age', 'Outcome']

data = pd.read_csv('pima-indians-diabetes.csv', names=col_names)
peek = data.head(20)
print("############## basics #####################")
print(peek)
print(data.shape)
print(data.dtypes)

# to describe the data
from pandas import set_option
print("############## description #####################")
set_option('display.width', 200)
set_option('display.max_columns', 10)
set_option('display.precision', 3)
description = data.describe()
print(description)

print("############## group by outcomes #####################")
outcomes = data.groupby('Outcome').size()
print(outcomes)

# correlation means how much one variable "moves" or gets affected by changing the other variable. In other words, how
# they may or may not change/move together. The degree to which they move together is called the correlation coefficient
# Correlation coefficient (r) values range from -1 to 1 via zero. -1 is negatively correlated. That means both move in
# opposite direction. 0  means they are not correlated at all while 1 means its very much positively correlated i.e. both
# of them move in the same direction. Correlation can be found out via corr() method
print("############## correlation #####################")
print(data.corr(method='pearson'))

# One can find out the skewness of a data using the skew() fuction. Knowing that an attribute has a skew may allow to
# perform data preparation to correct the skew and improve the accuracy of models. Negative skew means that the tail
# is towards the left and the peak of the chart is to the right of the median (ex: Marks chart). Positive skew means
# tail is to the right and the peak (bell curve) is to the left of the median (Ex: Salary chart)
skew = data.skew()
print("############## skewness #####################")
print(skew)
