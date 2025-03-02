import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("./large_dataset.csv")
sales_by_region = df.groupby("Region")['Total Revenue'].sum()

print(sales_by_region)

plt.figure(figsize = (12,6))
sales_by_region.plot(kind = 'bar')
plt.title('Sales by Region')
plt.xlabel('Region')
plt.ylabel('Total Revenue')
plt.show()
