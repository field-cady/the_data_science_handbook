import theano
import statsmodels.api as sm
import sklearn.datasets as datasets
import keras
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout, Flatten
import pandas as pd
from matplotlib import pyplot as plt
import sklearn.datasets
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from sklearn.cross_validation import train_test_split

from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, adjusted_rand_score
from sklearn import metrics
from sklearn.cross_validation import train_test_split
from sklearn import datasets
import sklearn
from sklearn.datasets import fetch_mldata

dataDict = datasets.fetch_mldata('MNIST Original')
X = dataDict['data']
Y = dataDict['target']
X_train, X_test, Y_train, Y_test = \
    train_test_split(X, Y, test_size=.1)
X_train = X_train.reshape((63000,1,28,28))
X_test = X_test.reshape((7000,1,28,28))
Y_train = pd.get_dummies(Y_train).as_matrix()

# Convolution layers expect a 4-D input so we reshape our 2-D input
nb_samples = X_train.shape[0]
nb_classes = Y_train.shape[1]

# We set some hyperparameters
BATCH_SIZE = 16
KERNEL_WIDTH = 5
KERNEL_HEIGHT = 5
STRIDE = 1
N_FILTERS = 10

# We fit the model
model = Sequential()
model.add(Convolution2D(
    nb_filter=N_FILTERS,
    input_shape=(1,28,28),
    nb_row=KERNEL_HEIGHT, 
    nb_col=KERNEL_WIDTH,
    subsample=(STRIDE, STRIDE))
)
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(5,5)))
model.add(Dropout(0.5))
model.add(Flatten())
model.add(Dense(nb_classes))
model.add(Activation('softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adadelta')

print 'fitting model'
model.fit(X_train, Y_train, nb_epoch=10)
probs = model.predict_proba(X_test)
preds = model.predict(X_test)
pred_classes = model.predict_classes(X_test)
true_classes = Y_test
(pred_classes==true_classes).sum()
