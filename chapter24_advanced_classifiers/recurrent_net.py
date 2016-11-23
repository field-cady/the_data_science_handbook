import sklearn.datasets
from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.layers.recurrent import LSTM, GRU

import statsmodels as sm

df = sm.datasets.elnino.load_pandas().data
X = df.as_matrix()[:,1:-1]
X = (X-X.min()) / (X.max()-X.min())
Y = df.as_matrix()[:,-1].reshape(61)
Y = (Y-Y.min()) / (Y.max()-Y.min())

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=.1)

model = Sequential()
model.add(GRU(20, input_shape=(11,1)))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='mean_squared_error', optimizer='adadelta')
model.fit(X_train.reshape((54,11,1)), Y_train, nb_epoch=5)

proba = model.predict_proba(X_test.reshape((7,11,1)), batch_size=32)
pred = pd.Series(proba.flatten())
true = pd.Series(Y_test.flatten())
print "Corr. of preds and truth:", pred.corr(true)
