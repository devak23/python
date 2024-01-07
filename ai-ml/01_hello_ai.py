import numpy as np
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense

# we are defining simplest possible neural network. There is only 1 layer and it contains only 1 neuron.
model = Sequential([Dense(units=1, input_shape=[1])])
# When using TensorFlow, you define your layers using Sequential. Inside the Sequential, you then specify what each
# layer looks like. We only have one line inside our Sequential, so we have only one layer.

# You then define what the layer looks like using the keras.layers API. There are lots of different layer types, but
# here we’re using a Dense layer. “Dense” means a set of fully (or densely) connected neurons. Our Dense layer has
# units=1 specified, so we have just one dense layer with one neuron in our entire neural network.

# Finally, when you specify the first layer in a neural network (in this case, it’s our only layer), you have to tell it
# what the shape of the input data is. In this case our input data is our X, which is just a single value, so we specify
# that that’s its shape.

model.compile(optimizer='sgd', loss='mean_squared_error')
# In a scenario such as this one, the computer has no idea what the relationship between X and Y is. So it will make a
# guess. Say for example it guesses that Y = 10X + 10. It then needs to measure how good or how bad that guess is.
# That’s the job of the loss function. It already knows the answers when X is –1, 0, 1, 2, 3, and 4, so the loss
# function can compare these to the answers for the guessed relationship. If it guessed Y = 10X + 10, then when X is –1,
# Y will be 0. The correct answer there was –3, so it’s a bit off. But when X is 4, the guessed answer is 50, whereas
# the correct one is 7. That’s really far off.
# Armed with this knowledge, the computer can then make another guess. That’s the job of the optimizer. This is where
# the heavy calculus is used, but with TensorFlow, that can be hidden from you. You just pick the appropriate optimizer
# to use for different scenarios. In this case we picked one called sgd, which stands for stochastic gradient descent
# —a complex mathematical function that, when given the values, the previous guess, and the results of calculating the
# errors (or loss) on that guess, can then generate another one. Over time, its job is to minimize the loss, and by
# so doing bring the guessed formula closer and closer to the correct answer.


# Next, we simply format our numbers into the data format that the layers expect.
xs = np.array([-1.0, 0.0, 1.0, 2.0, 3.0, 4.0], dtype=float)
ys = np.array([-3.0, -1.0, 1.0, 3.0, 5.0, 7.0], dtype=float)

# The learning process will then begin with the model.fit command
model.fit(xs, ys, epochs=500)
# You can read this as “fit the Xs to the Ys, and try it 500 times.” So, on the first try, the computer will guess the
# relationship (i.e., something like Y = 10X + 10), and measure how good or bad that guess was. It will then feed those
# results to the optimizer, which will generate another guess. This process will then be repeated, with the logic being
# that the loss (or error) will go down over time, and as a result the “guess” will get better and better.


print(model.predict([10.0]))

# What do you think the answer will be when we ask the model to predict Y when X is 10? You might instantly think 19,
# but that’s not correct. It will pick a value very close to 19. There are several reasons for this. First of all, our
# loss wasn’t 0. It was still a very small amount, so we should expect any predicted answer to be off by a very small
# amount. Secondly, the neural network is trained on only a small amount of data—in this case only six pairs of (X,Y)
# values.

# The model only has a single neuron in it, and that neuron learns a weight and a bias, so that Y = WX + B. This looks
# exactly like the relationship Y = 2X – 1 that we want, where we would want it to learn that W = 2 and B = –1. Given
# that the model was trained on only six items of data, the answer could never be expected to be exactly these values,
# but something very close to them.