import os
import numpy as np
from keras.models import Sequential
from keras.layers import *
import matplotlib.pyplot as plt
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image
from keras.models import Sequential

train_horse_dir = os.path.join('./datasets/horse-or-human/horses')
train_human_dir = os.path.join('./datasets/horse-or-human/humans')

train_horse_names = os.listdir(train_horse_dir)
train_human_names = os.listdir(train_human_dir)

print('total training horse images:', len(os.listdir(train_horse_dir)))
print('total training human images:', len(os.listdir(train_human_dir)))

model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3), padding='same',
          input_shape=(64, 64, 3), activation='relu'))
model.add(MaxPool2D(pool_size=(2, 2)))
model.add(Conv2D(32, kernel_size=(3, 3), padding='same',
          activation='relu'))
model.add(MaxPool2D(pool_size=(2, 2)))
model.add(Conv2D(32, kernel_size=(3, 3), padding='same',
          activation='relu'))
model.add(MaxPool2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dense(1, activation='sigmoid')) # 이중분류기 sigmoid
model.summary()
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['binary_accuracy'])

train_datagen = ImageDataGenerator(rescale=1 / 255)

train_generator = train_datagen.flow_from_directory(
    './datasets/horse-or-human/',
    target_size=(64, 64),
    batch_size=128,

    class_mode='binary')

history = model.fit(train_generator,steps_per_epoch=8,epochs=15,verbose=1)

model.save('./datasets/horse-or-human/horse-or-human_model.h5')