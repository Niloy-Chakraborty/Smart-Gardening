#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script Name:cnn.py
Script Functionality: This script trains a machine learning model using the plant image dataset
                      in offline mode, using a high performing system.
"""

# importing Keras, Library for deep learning
from keras.models import Sequential, load_model
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.utils import np_utils
from keras.preprocessing.image import img_to_array
from keras import backend as K
# Fix for Issue - #3 https://github.com/shreyans29/thesemicolon/issues/3
K.set_image_dim_ordering('th')
from matplotlib import pyplot as plt
#import cv2
import numpy as np
from matplotlib import pyplot as plt

# Image manipulations and arranging data
import os
from PIL import Image
import theano
theano.config.optimizer="None"
#Sklearn to modify the data
from sklearn.model_selection import train_test_split
#os.chdir("/home/adnan/Desktop/Project")

# input image dimensions
m, n = 127, 127


# define the directory name of the image dataset
path2 = "Smart_Garden_Plant_DB1"

classes = os.listdir(path2)
x = []
y = []


for fol in classes:
    print(fol)
    imgfiles = os.listdir(path2+'/'+fol)
    for img in imgfiles:
        im = Image.open(path2+'/'+fol+'/'+img)
        im = im.convert(mode='RGB')
        imrs = im.resize((m, n))
        imrs = img_to_array(imrs)/255
        imrs = imrs.transpose(2, 0, 1)
        imrs = imrs.reshape(3, m, n)
        x.append(imrs)
        y.append(fol)

x = np.array(x)
#print(x)
y = np.array(y)
np.save('values.npy', x)
np.save('predict', y)

x = np.load('values.npy')
y = np.load('predict.npy')
batch_size = 32
nb_classes = len(classes)
nb_epoch = 20
nb_filters = 32
nb_pool = 2
nb_conv = 3

#split training and testing data
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=4)

uniques, id_train = np.unique(y_train, return_inverse=True)
Y_train = np_utils.to_categorical(id_train, nb_classes)
uniques, id_test = np.unique(y_test,return_inverse=True)
Y_test = np_utils.to_categorical(id_test, nb_classes)

print('adding layers')
model = Sequential()
model.add(Convolution2D(nb_filters, nb_conv, nb_conv, border_mode='same', input_shape=x_train.shape[1:]))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(nb_pool, nb_pool)))
#add dropout to avoid overfitting
model.add(Dropout(0.7))
model.add(Flatten())
model.add(Dense(100))
model.add(Dropout(0.7))
model.add(Dense(nb_classes))
model.add(Activation('softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adadelta', metrics=['accuracy'])
print('fitting')
history= model.fit(x_train, Y_train, batch_size=batch_size, epochs=nb_epoch, verbose=1, validation_data=(x_test, Y_test));

model.save('cnnmodel_new.h5')

#plotting the accuracy and loss 

#accuracy
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.savefig('accuracy.png')

plt.show()

#loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.savefig('loss.png')

plt.show()

