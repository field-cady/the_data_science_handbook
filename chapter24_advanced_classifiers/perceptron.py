import sklearn.datasets
from keras.models import Sequential
from keras.layers.core import Dense, Activation
import pandas as pd
from sklearn.cross_validation import train_test_split

ds = sklearn.datasets.load_iris()
X = ds['data']
Y = pd.get_dummies(ds['target']).as_matrix()
X_train, X_test, Y_train, Y_test = \
    train_test_split(X, Y, test_size=.2)

model = Sequential([
    Dense(50, input_dim=4, activation='sigmoid'),
    Dense(3, activation='softmax')
])
model.compile(
  loss='categorical_crossentropy', 
  optimizer='adadelta')
model.fit(X_train, Y_train, nb_epoch=5)
proba = model.predict_proba(X_test, batch_size=32)
pred = pd.Series(proba.flatten())
true = pd.Series(Y_test.flatten())
print "Correlation:", pred.corr(true)
