#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script Name:PlantIdentification.py
Script Methods: 1)Identify
"""


# importing Keras, Library for deep learning
from keras.models import Sequential, load_model
from keras.preprocessing.image import img_to_array
from keras import backend as K
K.set_image_dim_ordering('th')

import numpy as np
import os
import h5py
from PIL import Image
import tensorflow as tf
import cv2

#load the previously trained model
model1= load_model('cnnmodel_new.h5')
global graph,model
graph = tf.get_default_graph()

'''
Method Name:Identify
Functionality: This function loads the keras model for plant name and health detection and fits the last captured
               photo with the model for classification
Returns: Plant Name
'''

def Identify():
    # input image dimensions
    m, n = 127, 127

    path1 = "test" #target image directory
    classes=['Angelonia', 'Bengal Rose', 'Crassula_ovata(Money_Plant)', 'Dry', 'Echeveria', 'Ice Dance']
    x = []
    y = []

    print('RUNNING ML ALGORITHM TO IDENTIFY THE PLANT')
    files = os.listdir(path1)
    imag = files[0]
    gim = Image.open(path1 + '/'+imag)
    gim = gim.convert(mode='RGB')
    gimrs = gim.resize((m, n))
    gimrs = img_to_array(gimrs)/255
    gimrs = gimrs.transpose(2, 0, 1)
    gimrs = gimrs.reshape(3, m, n)

    x.append(gimrs)
    x = np.array(x)
    with graph.as_default():
        
        predictions = model1.predict(x) #prediction 
    c = np.amax(predictions)
    ind = np.argmax(predictions)#taking the highest prediction
    classes = sorted(classes)
    
    imagex = cv2.imread("./test/foo.jpg")
    imagex= cv2.resize(imagex, (300, 300))
    text = classes[ind] + " with "+  str(round(c*100)) +"% prediction"
    cv2.putText(imagex, text, (2, 25), cv2.FONT_HERSHEY_SIMPLEX,0.6, (255, 0, 0), 2)
    cv2.imwrite("./test/predicted.jpg",imagex)

    return classes[ind]


