# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22 13:16:58 2019
Script Name:publish.py
"""

#Import all the necessary packages

from openzwave.option import ZWaveOption
from openzwave.network import ZWaveNetwork
from time import sleep
import paho.mqtt.client as mqtt
from datetime import datetime
import random, threading, json

while True:
 #Connecting to ZWaveNetwork to gather the sensor information.
    options=ZWaveOption("/dev/ttyACM0",config_path='/home/pi/openzwave/openzwave/config',user_path=".")
    options.set_console_output(False)
    options.lock()
    network=ZWaveNetwork(options,log=None)
    network.start()
    
 #Connection details of cloudmqtt broker.

    broker = "postman.cloudmqtt.com"
    port = 13031
    username="rzoshkuo"
    password="ke8JKDZUQ2o0"
    
    client = mqtt.Client()
    client.username_pw_set(username, password)
    client.connect(broker,port)
    
 #Check if network is ready or not
    
    while network.state!= network.STATE_READY:
        sleep(5)
        
 #Collecting Temperature, Relative Humidity and Luminance data.
 
      
    for node in network.nodes:
        for sensor in network.nodes[node].get_sensors().items():
            x=sensor[1].label
            y=sensor[1].data
            if(x == "Temperature"):
               if (y<45):
                 Temperature_Data = {}
                 Temperature_Data['Date_n_Time'] = (datetime.today()).strftime("%d-%b-%Y %H:%M:%S:%f")
                 Temperature_Data['Temperature'] = y
                 temperature_json_data = json.dumps(Temperature_Data)
                 client.publish(topic="Temperature", payload=temperature_json_data, qos=1)
                 y=0
            if(x == "Relative Humidity"):
               Humidity_Data = {}
               Humidity_Data['Date_n_Time'] = (datetime.today()).strftime("%d-%b-%Y %H:%M:%S:%f")
               Humidity_Data['Relative_Humidity'] = y
               humidity_json_data = json.dumps(Humidity_Data)
               client.publish(topic="Relative Humidity", payload=humidity_json_data, qos=1)
               y=0
            if(x == "Luminance"):
               Luminance_Data = {}
               Luminance_Data['Luminance'] = y
               luminance_json_data = json.dumps(Luminance_Data)
               client.publish(topic="Luminance", payload=luminance_json_data, qos=1)
               y=0
            
            sleep(5)
    
    network.stop()        
