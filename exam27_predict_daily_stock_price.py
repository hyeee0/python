import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from keras.models import *
from keras.layers import *
from sklearn.model_selection import train_test_split
from keras.callbacks import EarlyStopping
from sklearn.preprocessing import MinMaxScaler

raw_data = pd.read_csv('./datasets/samsung19_22.csv')
print(raw_data.head())
raw_data.info()

print(raw_data.isnull().sum())
raw_data['Date'] = pd.to_datetime(raw_data['Date'])
raw_data.set_index('Date', inplace=True)

data_close = raw_data[['Close']]
print(data_close.head())

print(data_close.max())
print(data_close.min())

minmaxscaler = MinMaxScaler()
scaled_data = minmaxscaler.fit_transform(data_close)
print(scaled_data[:5])
print(scaled_data.shape)

sequence_X = []
Y = []
for i in range(len(scaled_data)-30):
    x = scaled_data[i:i+30]
    y = scaled_data[i+30]
    sequence_X.append(x)
    Y.append(y)
sequence_X = np.array(sequence_X)
sequence_Y = np.array(Y)
print(sequence_X.shape)
print(sequence_Y.shape)
print(sequence_X[:5])
print(sequence_Y[:5])

X_train, X_test, Y_train, Y_test = train_test_split(
    sequence_X, sequence_Y, test_size=0.2)
print(X_train.shape, Y_train.shape)
print(X_test.shape, Y_test.shape)

model = Sequential()
model.add(LSTM(50, input_shape=(30, 1), activation='tanh'))
model.add(Flatten())
model.add(Dense(1))
model.summary()

model.compile(loss='mse', optimizer='adam')
early_stopping = EarlyStopping(monitor='val_loss', patience=7)
fit_hist = model.fit(X_train, Y_train, epochs=100, validation_data=(X_test, Y_test),
                     shuffle=False, callbacks=[early_stopping])
model.save('./samsung_close_predict.h5')
plt.plot(fit_hist.history['loss'], label='loss')
plt.plot(fit_hist.history['val_loss'], label='val_loss')
plt.legend()
plt.show()

pred = model.predict(X_test)
plt.plot(Y_test[:30], label='actual')
plt.plot(pred[:30], label='predict')
plt.legend()
plt.show()

last_data_30 = scaled_data[-30:].reshape(-1, 30, 1)
next_close = model.predict(last_data_30)
print(next_close)

next_close_value = minmaxscaler.inverse_transform(next_close)
print(next_close_value)