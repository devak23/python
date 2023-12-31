import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

data = pd.read_csv("datasets/oranges.csv")
# figure out the dependent and independent variables
data_y = data["Price"] # --- Dependent variable
data_x = data["Year"] # --- Independent variable


model = LinearRegression()
model_X = data[["Year", "Rainfall"]].values
print(model_X)
model_y = data_y.values.reshape(-1, 1)

model.fit(X=model_X, y=model_y)

# plt.scatter(y=data_Y, x=data_x, label="observed")
plt.plot(data_x, data_y, label="observed")

# plt.scatter(y=model.predict(model_X), x=data_x, label="predicted")
plt.plot(data_x, model.predict(model_X), label="predicted")
plt.xlabel("Year")
plt.ylabel("Price of oranges")
plt.legend(loc="upper left")

plt.show()
