import csv
import numpy
import pandas


# Reading a CSV file in 3 ways
filename = 'pima-indians-diabetes.csv'

# traditional python way
raw_data = open(filename, "rt")  # open the file in text mode
reader = csv.reader(raw_data, delimiter=',', quoting=csv.QUOTE_NONE)
x = list(reader)
data = numpy.array(x)
print(data.shape)

# using numpy
from numpy import loadtxt

raw_data = open(filename, "rt")  # open the file in text mode
data = loadtxt(raw_data, delimiter=",")
print(data.shape)

# using pandas
col_names = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction',
             'Age', 'Outcome']
data = pandas.read_csv(filename, names=col_names)
print(data.shape)

