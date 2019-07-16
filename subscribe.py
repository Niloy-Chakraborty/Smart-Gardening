# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22 13:16:58 2019
Script Name:subscribe.py
"""

#Import all the necessary packages
import paho.mqtt.client as mqtt
from storeindb import storeindb

#cloud mqttbroker details
broker="postman.cloudmqtt.com"
port=13031
username="rzoshkuo"
password="ke8JKDZUQ2o0"

def on_connect(client, userdata, flags, rc):
   print("Connected With Result Code "+rc)

#calling on_message event and transfering all subscribed data to database
def on_message(client, userdata, message):
   print("Message Recieved: "+message.payload.decode())
   storeindb(message.topic, message.payload.decode())

client = mqtt.Client()
client.username_pw_set(username, password)
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker, port)

#Subscribing to Temperature,Relative Humidity,Luminance topics
client.subscribe("Temperature", qos=1)
client.subscribe("Relative Humidity", qos=1)
client.subscribe("Luminance", qos=1)

client.loop_forever()

