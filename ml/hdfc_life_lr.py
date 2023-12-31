import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("datasets/HDFCLIFE.NS.csv")

# figure out the dependent and independent variables
data_y = data["Open"].values.reshape(-1, 1)
dates = pd.to_datetime(data["Date"], errors='coerce').values.astype(np.float64).reshape(-1, 1)

data_x = np.stack((dates, data["Volume"].values.reshape(-1,1)), axis=1).reshape(-1,1)

from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X=data_x, y=data_y)

plt.plot(data_x, data_y)
plt.plot(data_x, model.predict(data_x))
plt.show()
