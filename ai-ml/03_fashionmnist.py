import tensorflow as tf

# Keras has a number of built-in datasets that you can access with a single line of code like this. In this case you
# don’t have to handle downloading the 70,000 images—splitting them into training and test sets, and so on—all it
# takes is one line of code. This methodology has been improved upon using an API called TensorFlow Datasets,
# but for the purposes of these early chapters, to reduce the number of new concepts you need to learn, we’ll just
# use tf.keras.datasets.
data = tf.keras.datasets.fashion_mnist

# We can call its load_data method to return our training and test sets like this
(training_images, training_labels), (test_images, test_labels) = data.load_data()
# Fashion MNIST is designed to have 60,000 training images and 10,000 test images. So, the return from data.load_data
# will give you an array of 60,000 28 × 28-pixel arrays called training_images, and an array of 60,000 values (0–9)
# called training_labels. Similarly, the test_images array will contain 10,000 28 × 28-pixel arrays,
# and the test_labels array will contain 10,000 values between 0 and 9. Our job will be to fit the training images to
# the training labels


# All of the pixels in our images are grayscale, with values between 0 and 255. Dividing by 255 thus ensures that
# every pixel is represented by a number between 0 and 1 instead. This process is called normalizing the image. Often
# your network will not learn and will have massive errors when dealing with non normalized data. The Y = 2X – 1
# example from didn’t require the data to be normalized because it was very simple, but for fun try training it with
# different values of X and Y where X is much larger and you’ll see it quickly fail!
training_images = training_images / 255.0
test_images = test_images / 255.0


# Next we define the neural network that makes up our model. In this case, we have multiple layers. The first,
# Flatten, isn’t a layer of neurons, but an input layer specification. Our inputs are 28 × 28 images, but we want
# them to be treated as a series of numeric values. Flatten takes that “square” value (a 2D array) and turns it into
# a line (a 1D array). The next one, Dense, is a layer of neurons, and we’re specifying that we want 128 of them.
# This is the middle layer. You’ll often hear such layers described as hidden layers. Layers that
# are between the inputs and the outputs aren’t seen by a caller, so the term “hidden” is used to describe them.
# We’re asking for 128 neurons to have their internal parameters randomly initialized. Often the question I’ll get
# asked at this point is “Why 128?” This is entirely arbitrary—there’s no fixed rule for the number of neurons to
# use. As you design the layers you want to pick the appropriate number of values to enable your model to actually
# learn. More neurons means it will run more slowly, as it has to learn more parameters. More neurons could also lead
# to a network that is great at recognizing the training data, but not so good at recognizing data that it hasn’t
# previously seen (this is known as overfitting, and we’ll discuss it later in this chapter). On the other hand,
# fewer neurons means that the model might not have sufficient parameters to learn.

model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28))
    , tf.keras.layers.Dense(128, activation=tf.nn.relu)
    , tf.keras.layers.Dense(10, activation=tf.nn.softmax)
])

model.compile(optimizer='adam'
              , loss = 'sparse_categorical_crossentropy'
              , metrics=['accuracy'])

model.fit(training_images, training_labels, epochs=5)

model.evaluate(test_images, test_labels)

# Prints:
# Downloading data from https://storage.googleapis.com/tensorflow/tf-keras-datasets/train-labels-idx1-ubyte.gz
# 29515/29515 [==============================] - 0s 0us/step
# Downloading data from https://storage.googleapis.com/tensorflow/tf-keras-datasets/train-images-idx3-ubyte.gz
# 26421880/26421880 [==============================] - 22s 1us/step
# Downloading data from https://storage.googleapis.com/tensorflow/tf-keras-datasets/t10k-labels-idx1-ubyte.gz
# 5148/5148 [==============================] - 0s 0us/step
# Downloading data from https://storage.googleapis.com/tensorflow/tf-keras-datasets/t10k-images-idx3-ubyte.gz
# 4422102/4422102 [==============================] - 1s 0us/step
# Epoch 1/5
# 1875/1875 [==============================] - 12s 6ms/step - loss: 0.4966 - accuracy: 0.8257
# Epoch 2/5
# 1875/1875 [==============================] - 17s 9ms/step - loss: 0.3743 - accuracy: 0.8656
# Epoch 3/5
# 1875/1875 [==============================] - 19s 10ms/step - loss: 0.3350 - accuracy: 0.8778
# Epoch 4/5
# 1875/1875 [==============================] - 16s 9ms/step - loss: 0.3119 - accuracy: 0.8851
# Epoch 5/5
# 1875/1875 [==============================] - 15s 8ms/step - loss: 0.2936 - accuracy: 0.8916
# 313/313 [==============================] - 2s 5ms/step - loss: 0.3610 - accuracy: 0.8709