import numpy as np
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense

l0 = Dense(units=1, input_shape=[1])
model = Sequential([l0])

model.compile(optimizer='sgd', loss='mean_squared_error')

xs = np.array([-1.0, 0.0, 1.0, 2.0, 3.0, 4.0], dtype=float)
ys = np.array([-3.0, -1.0, 1.0, 3.0, 5.0, 7.0], dtype=float)

model.fit(xs, ys, epochs=500)

print(model.predict([10.0])) # prints: [[18.976986]]
print("Here is what I learnt: {}".format(l0.get_weights()))

# Thus, the learned relationship between X and Y was Y = 1.9966644X – 0.9896586. This is pretty close to what we’d
# expect (Y = 2X – 1), and we could argue that it’s even closer to reality, because we are assuming that the
# relationship will hold for other values.