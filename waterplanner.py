# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22 13:16:58 2019
Script Name:waterplanner.py
"""
#Import all the necessary packages
import os
import time
import subprocess
import pymysql
import pandas as pd
import openzwave
from openzwave.node import ZWaveNode
from openzwave.value import ZWaveValue
from openzwave.scene import ZWaveScene
from openzwave.controller import ZWaveController
from openzwave.network import ZWaveNetwork
from openzwave.option import ZWaveOption
import six
import datetime
import spidev # To communicate with SPI devices
from numpy import interp 


global moisturecontentold
global temperature
global humidity
global moisture

global temp
global humid

moisturecontentold=list()
host="mydbinstance.c1arr1firswu.us-east-2.rds.amazonaws.com"
port=3306
dbname="smartGardenDB"
user="root"
password="smartgarden"

now = datetime.datetime.now()
time8pm = now.replace(hour=23, minute=55, second=0, microsecond=0)

# Start SPI connection
spi = spidev.SpiDev() # Created an object
spi.open(0,0) 


# Read MCP3008 data
def analogInput(channel):
  spi.max_speed_hz = 1350000
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data
  
while True:
  conn = pymysql.connect(host, user=user,port=port,
                           passwd=password, db=dbname)
                           
  df5=pd.read_sql('SELECT Temperature FROM Temperature_Data ORDER BY ID DESC LIMIT 1;', con=conn)
  s1=df5.iat[0,0]
  temperature= float(df5.iat[0,0])
  df6=pd.read_sql('SELECT Relative_Humidity FROM Humidity_Data ORDER BY ID DESC LIMIT 1;', con=conn)
  humidity=int(df6.iat[0,0])
 
  Moisture = []
     
  df=pd.read_sql('select count(distinct plant_ID) AS "TotalPlants" from PlantDatabase;', con=conn)
  TotalPlants=df.iat[0,0]
  for i in range(TotalPlants):
    output = analogInput(i) # Reading from CH0
    output = interp(output, [0, 1023], [100, 0])
    output = int(output)
    Moisture.append(output)
    
  #print("Moisturefromsensor:", Moisture)
  
  
  moisturecontent= list()
  for k in range(TotalPlants):
    id=k+1   
    df1 = pd.read_sql('SELECT max_temp_withstand AS "Temp" FROM PlantDatabase where Plant_ID ='+ str(id), con=conn)
    temp = df1.iat[0,0]
    
    df2 = pd.read_sql('SELECT min_humidity AS "humid" FROM PlantDatabase where Plant_ID = '+str(id), con=conn)
    humid=df2.iat[0,0]
    df3 = pd.read_sql('SELECT min_soilmoisture AS "moisture" FROM PlantDatabase where Plant_ID = '+str(id), con=conn)
    moisture=df3.iat[0,0]
    df5 = pd.read_sql('SELECT last_watered AS "lastwatered" FROM PlantDatabase where Plant_ID = '+str(id), con=conn)
    last=df5.iat[0,0]
    df4 = pd.read_sql('SELECT timestampdiff(HOUR,last_watered,NOW()) FROM PlantDatabase where Plant_ID = '+str(id), con=conn)
    lastwatered=df4.iat[0,0]
   
    if ((temperature>= temp) and (humidity <= humid) and (lastwatered >= 8)):
    
      moisturecontent.append('notsufficient')
    elif (Moisture[k]< moisture):
      moisturecontent.append('notsufficient')
    else:
      moisturecontent.append('sufficient')
      
  print(moisturecontent)
	 
  if(len(moisturecontent)==0):
    continue
   

  elif ((moisturecontent[0]=="sufficient") and (moisturecontent[1]=="sufficient")):
    continue 
 
 
  elif(now<time8pm):
		  # The written code is generated to the "out" variable.
    out = """
      (define (problem water-garden)
    	  (:domain smart-garden)
    	  (:objects plant1 plant2 motor1 motor2 )
    	  (:init (plant plant1)
    			 (plant plant2)
    			 (motor motor1)
    			 (motor motor2)
    			 (free motor1)
    			 (free motor2)
    			 
    	  """
    plant_names = list()
    for i in range(TotalPlants):
        if (moisturecontent[i]=='sufficient'):
            out += "       (sufficientmoisturelevel plant{})".format(i+1)
            out += """
        		  """          
    out +=""")
    	  (:goal (and (sufficientmoisturelevel plant1) 
    					   (sufficientmoisturelevel plant2)   
    					   )))
      """
    filename = "smartGarden_problem"
    with open(filename, "w") as f:
      f.write(out)
     
    #Extract Steps from outputfile and turn on motor accordingly
    myCmd = './ff -o smartGarden_domain.pddl -f smartGarden_problem > outputwater.txt'
    os.system(myCmd)
    myCmd = 'python water.py'
    os.system(myCmd)
  moisturecontentold = moisturecontent
  time.sleep(15)