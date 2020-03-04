# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22 13:16:58 2019
Script Name:iotcontrol.py
Script Methods: 1) instructions, 2)sensorstatus, 3)localweather, 4)getAdminId,5)fetchIoTUserList,6)addIoTUser,7)removeIoTUser,
                8)gardenstatus,9)camera,10)water,11)knowPlant,12)ledlighton,and 13)addPlant
"""

#Import all the necessary packages
import picamera
import os
import time
import subprocess
import numpy as np
import cv2
from urllib.request import urlopen
import urllib.parse
import logging
from openzwave.option import ZWaveOption
from openzwave.network import ZWaveNetwork
from darksky import forecast
import logging
import PlantIdentificationTest
import paho.mqtt.client as mqtt
from time import sleep
import pymysql
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from plugwise import Stick
from plugwise import Circle
import constants
import telebot
import continuemsg
import datetime

s=Stick(port="/dev/ttyUSB0")
c1,c2=Circle("000D6F0005692784",s),Circle("000D6F000416E6F4",s)
options=ZWaveOption("/dev/ttyACM0",config_path='/home/pi/openzwave/openzwave/config',user_path=".")
options.set_console_output(False)
options.lock()
network=ZWaveNetwork(options,log=None)
network.start()

#Database details
moisturecontentold=list()
host="mydbinstance.c1arr1firswu.us-east-2.rds.amazonaws.com"
port=3306
dbname="smartGardenDB"
user="root"
password="smartgarden"
conn = pymysql.connect(host, user=user,port=port,
                           passwd=password, db=dbname)
                           

if not os.path.exists('./files/log/'): #if path does not exist then create it
    os.makedirs('./files/log/')

logging.basicConfig(filename = './files/log/bot.log',  format='%(asctime)s,%(message)s\n',level=logging.INFO)


class iotcontrol:
    def __init__(self,adminId,darkskyKey,lat,longitude):
        self.adminId = adminId
        self.approvedUsers={}
        self.approvedUsers[self.adminId] = 'ADRIKA'

        self.darkskyKey = darkskyKey
        self.weatherTimeLimit=30.0
         
        self.timePic = 0
        self.timeVideo = 0
        self.lat = lat
        self.longitude = longitude
        self.cityWeatherData = forecast(self.darkskyKey,self.lat,self.longitude)

        self.enablePic = True
        self.enableWater = False
        self.enableLight = True
        self.enableAdd = True
        self.enableVideo = True

        self.picTimeLimit =2.0 #mins for users (not admin)
        self.waterTimeLimit = 4.0 #hrs for users (not admin)
        self.lightTimeLimit = 15.0 #mins for users (not admin)
        self.weatherTimeLimit = 30.0 #mins for users (not admin)
        self.vidTimeLimit = 5.0 #mins for users (not admin)
       
       
            
    '''
    Method Name: instructions
    Functionality: This function takes the pleasure of welcoming the newly registerd user
    Returns: None
    '''    
    def instructions(self,bot,update):
        bot.send_message(chat_id=update.callback_query.message.chat.id,text='Have a great experince with Smart Gardening!')
        hello = 'Hello {} ({})\n'.format(update.callback_query.from_user.first_name,update.callback_query.from_user.id)

        autoAdd = '\n\nPlease Type: /start (and send) to be auto-added to IOT control\n\n'
        message = hello+autoAdd
        
        bot.edit_message_text(chat_id=update.callback_query.message.chat_id,message_id=update.callback_query.message.message_id,text=message)
        
        
    '''
    Method Name: instructions
    Functionality: This function lets the user know about different sensor readings from aeon sensor
    Returns: None
    ''' 

    def sensorstatus(self,bot,update):
        while network.state!= network.STATE_READY:
             sleep(1)

    
        for node in network.nodes:
              for sensor in network.nodes[node].get_sensors().items():
                 chat_id=update.callback_query.message.chat_id 
                 bot.sendMessage(chat_id,str("Sensor type:'{0}'".format(sensor[1].label)))
                 bot.sendMessage(chat_id,str("Sensor reading:'{0}'".format(sensor[1].data)))
      
      
      
    '''
    Method Name: localweather
    Functionality: This method connects with the darksky API and collects information of the city weather (temperature, 
                   humidity, precipitation chance etc.), as well as sends this information to the bot user.
    Returns: None
    '''   
    def localweather(self,bot,update):
      
            bot.send_message(chat_id=update.callback_query.message.chat.id,text='Local Weather Report!')
            tNow = time.time()
            limit = self.weatherTimeLimit
            if((tNow-self.cityWeatherData['currently']['time'])/60.0>=limit):
               self.cityWeatherData = forecast(self.darkskyKey,self.lat,self.longitude)
               print('refreshed weather data')
            
            weatherTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(self.cityWeatherData['currently']['time']))
            summary = self.cityWeatherData['currently']['summary']
            temp = self.cityWeatherData['currently']['temperature']
            humid = self.cityWeatherData['currently']['humidity']*100
            precip = self.cityWeatherData['currently']['precipProbability']*100
            message = 'At: {}, it is: {}, with temp :{:.2f}F, humidity: {:.2f}%, precipitation probability: {:.2f}%.'.format(weatherTime,summary,temp,humid,precip)
            bot.sendMessage(chat_id=update.callback_query.message.chat_id,message_id=update.callback_query.message.message_id,text=message)
         
         
    '''
    Method Name: getAdminId
    Functionality: This method returns the admin ID
    Returns: adminID
    '''                 
    def getAdminId(self):
       return self.adminId


    '''
    Method Name: fetchIoTUserList
    Functionality: This method fetches the user List.
    Returns: None
    '''  
    def fetchIoTUserList(self,bot,update):
        
        """ 
        Admin Command: add users manually
        Usage:
            /fetch
            
        """
                 
        logging.info('/fetch,{},{}'.format(update.message.from_user.first_name,update.message.from_user.id))
        try:
            if(update.message.from_user.id==self.adminId):
                msg1 =' '.join(map(str,self.approvedUsers))
                msg2 = ', '.join(map(str,self.approvedUsers.values()))
                
                bot.send_message(chat_id=update.message.chat_id, text="Current IoT controllers are: "+msg1+"\n\n\n"+"["+msg2+"]")
            else:
                bot.send_message(chat_id=update.message.chat_id, text="Unauthorized activity, only admin can issue this command!")
        except:
            bot.send_message(chat_id=update.message.chat_id, text="Unauthorized activity, only admin can issue this command!")
      
                    
    '''
    Method Name: addIoTUser
    Functionality: This method lets the admin add new users.
    Returns: None
    ''' 
    def addIoTUser(self,bot,update,args):
        """ 
        Admin Command: add users manually
        Usage:
            /add 12345 324567 8726251
            
            The numbers are ids of users
            
        """
        
        logging.info('/add,{},{}'.format(update.message.from_user.first_name,update.message.from_user.id))
        try:
            if(update.message.from_user.id==self.adminId): #hardcoded for security only admin can issue this command
                for arg in args:
                    self.approvedUsers[int(arg)]='manually_added'
                    
                msg =' '
                bot.send_message(chat_id=update.message.chat_id, text="User/Users: "+ msg.join(args)  +" added to IoT Control")
            else:
                bot.send_message(chat_id=update.message.chat_id, text="Unauthorized activity, only admin can issue this command!")
        except:
            bot.send_message(chat_id=update.message.chat_id, text="Unauthorized activity, or Bad argument!")
        
        
        
    '''
    Method Name: removeIoTUser
    Functionality: This method lets the admin remove users.
    Returns: None
    '''          
    def removeIoTUser(self,bot,update,args):
        """ 
        Admin Command: remove users manually
        Usage:
            /rm all
            /rm 123445
        """
        
        
        logging.info('/rm,{},{}'.format(update.message.from_user.first_name,update.message.from_user.id))
        
        try:
            if(update.message.from_user.id==self.adminId): #hardcoded for security only admin can issue this command
                if(args[0]=='all'):
                    self.approvedUsers ={}
                    self.approvedUsers[self.adminId] = 'ADRIKA'
                    bot.send_message(chat_id=update.message.chat_id, text="All users removed from IoT control!")
                else:
                    if(self.adminId!=int(args[0])): 
                        self.approvedUsers.pop(int(args[0]))
                        bot.send_message(chat_id=update.message.chat_id, text="User {} removed from IoT Control".format(args[0]))
                    else:
                        bot.send_message(chat_id=update.message.chat_id, text="Unauthorized action: Cannot remove Admin!".format(args[0]))
                
            else:
                bot.send_message(chat_id=update.message.chat_id, text="Unauthorized activity, only admin can issue this command!") 
        except:
            bot.send_message(chat_id=update.message.chat_id, text="Unauthorized activity or Bad argument!")


    '''
    Method Name: gardenstatus
    Functionality: This method takes the sensor data and sends graphical visualization of different data
                   to the user for mainly monitoring purpose.
    Returns: None
    '''   
    def gardenstatus(self,bot,update):
       
      
        
        host="mydbinstance.c1arr1firswu.us-east-2.rds.amazonaws.com"
        port=3306
        dbname="smartGardenDB"
        user="root"
        password="smartgarden"
        conn = pymysql.connect(host, user=user,port=port,passwd=password, db=dbname)
        df1 = pd.read_sql('SELECT Date_n_Time, Temperature FROM Temperature_Data', con=conn)
        df1["Date_n_Time"] = pd.to_datetime( df1["Date_n_Time"], format='%d-%b-%Y %H:%M:%S:%f')
        df1["Temperature"] = pd.to_numeric(df1["Temperature"])
        ax = plt.gca()
        df1.plot(kind='line',x='Date_n_Time',y='Temperature',ax=ax)
        plt.ylabel('Temperature and Relative Humidity')
        df2 = pd.read_sql('SELECT Date_n_Time, Relative_Humidity FROM Humidity_Data', con=conn)
        df2["Date_n_Time"] = pd.to_datetime( df2["Date_n_Time"], format='%d-%b-%Y %H:%M:%S:%f')
        df2["Relative_Humidity"] = pd.to_numeric(df2["Relative_Humidity"])
        df2.plot(kind='line',x='Date_n_Time',y='Relative_Humidity',ax=ax)
        fig = plt.gcf()
        fig.savefig('./teststatus/GardenStatus.png',dpi = 300)
        outpath= './teststatus/GardenStatus.png'
        f= open(outpath,'rb')
        bot.send_photo(chat_id=update.callback_query.message.chat.id,photo=f,caption='Sensor status from Garden',timeout=120)
        f.close()


    '''
    Method Name: camera
    Functionality: This function captures photo of the plant from remote end user's will.
    Returns: None
    '''      
    def camera(self,bot,update,ndvi=False):
        """ Capture Pic and Transmit it to the bot"""
        logging.info('/sendPic {} {} {}'.format(ndvi,update.callback_query.from_user.first_name,update.callback_query.from_user.id))
        print('hi11')
        url="http://192.168.0.100:8080/shot.jpg"  #Enter your IP Webcam URL
        print("hi")
        imgPath=urlopen(url)
        print(imgPath)
        imgNp=np.array(bytearray(imgPath.read()),dtype=np.uint8)
        print(imgNp)
        img=cv2.imdecode(imgNp,-1)
        print('hi3')
        cv2.imwrite('./test/foo.jpg',img)
        inputPath = './test/foo.jpg'
        outPath = inputPath          
        f = open(outPath,'rb')
                    
        bot.send_photo(chat_id=update.callback_query.message.chat.id,photo=f,caption='Current Pic Taken by {} ({})'.format(update.callback_query.from_user.first_name,update.callback_query.from_user.id),timeout=120)
        f.close()

    '''
    Method Name: water
    Functionality: This function enables the watering of all plants in accordance with the remote end user's will.
    Returns: None
    '''       
    def water(self,bot,update):
        bot.send_message(chat_id=update.callback_query.message.chat.id, text="Checking status of last watered")
        cursorObject = conn.cursor() 
        currentDT = datetime.datetime.now()
        df=pd.read_sql('select count(distinct plant_ID) AS "TotalPlants" from PlantDatabase;', con=conn)
        TotalPlants=df.iat[0,0] 
        for i in range(TotalPlants):
          df3 = pd.read_sql('SELECT timestampdiff(HOUR,last_watered,NOW()) FROM smartGardenDB.PlantDatabase where Plant_ID = '+str(i+1), con=conn)
          df3=df3.iat[0,0]
          print(df3)
          df2 = pd.read_sql('SELECT last_watered AS "lasttime" FROM PlantDatabase where Plant_ID = '+str(i+1), con=conn)
          lasttime=df2.iat[0,0]  
          message= 'Plant{}:last-watered {},watered before {}hours'.format(str(i+1),lasttime,df3)
          bot.send_message(chat_id=update.callback_query.message.chat.id, text=message) 
          if ((df3>5) and (i==0)):
              bot.send_message(chat_id=update.callback_query.message.chat.id, text="Switching on Motor{}".format(str(i+1)))
              c1.switch_on()
              updateStatement = "UPDATE PlantDatabase SET last_watered = now() WHERE Plant_ID ="+ str(i+1)
            # Execute the SQL UPDATE statement
              cursorObject.execute(updateStatement)
              conn.commit()
          elif ((df3>5) and (i==1)):
              bot.send_message(chat_id=update.callback_query.message.chat.id, text="Switching on Motor{}".format(str(i+1)))
              c2.switch_on()
              updateStatement = "UPDATE PlantDatabase SET last_watered = now() WHERE Plant_ID ="+ str(i+1)
            # Execute the SQL UPDATE statement
              cursorObject.execute(updateStatement)
              conn.commit()    
          else:      
              bot.send_message(chat_id=update.callback_query.message.chat.id, text="No Watering possible, the plant{} was watered less than 5 hours ago".format(i+1)) 
              
              
    '''
    Method Name: knowPlant
    Functionality: This function takes the last captured photo from local and let the user know about the Name of the 
                   plant by calling the Deep Learning Plant Recognition model
    Returns: None
    '''                                
    def knowPlant(self,bot,update):
        plant= PlantIdentificationTest.Identify()
        print(plant)
        if plant != "Dry":
            bot.send_message(chat_id=update.callback_query.message.chat.id, text= "The captured plant is: "+str(plant))
            bot.send_message(chat_id=update.callback_query.message.chat.id, text= "The Plant is healthy")
        else:
            bot.send_message(chat_id=update.callback_query.message.chat.id, text= "Your Plant is getting Dry!! Please pay some attention")
        outpath= './test/predicted.jpg'
        f= open(outpath,'rb')
        bot.send_photo(chat_id=update.callback_query.message.chat.id,photo=f,caption='Current Pic Taken by {} ({})'.format(update.callback_query.from_user.first_name,update.callback_query.from_user.id),timeout=120)
        f.close()
         
        
        
    '''
    Method Name: ledlighton
    Functionality: This function turns the LED light ON in accordance with the users action and store the current status of the lamps in the database
    Returns: None
    '''      
    def ledlighton(self,bot,update):
        bot.send_message(chat_id=update.callback_query.message.chat.id, text="Checking Status of light")
        df=pd.read_sql('select count(distinct id) AS "TotalLamps" from lamp_status;', con=conn)
        cursorObject = conn.cursor()
        TotalLamps=df.iat[0,0]
        
        for i in range(TotalLamps):
              df3 = pd.read_sql('SELECT status AS "lampstatus" FROM lamp_status where id = '+str(i+1), con=conn)
              lampstatus=df3.iat[0,0]
              print(lampstatus)
              if (lampstatus =='off') and (i==0):
                  bot.send_message(chat_id=update.callback_query.message.chat.id, text="Switching on Lamp{}".format(str(i+1)))
                  c1.switch_on()
                  updateStatement = "UPDATE lamp_status SET status ='on' WHERE id ="+ str(i+1)
                  cursorObject.execute(updateStatement)
                  conn.commit()
              elif (lampstatus =='off') and (i==1): 
                  bot.send_message(chat_id=update.callback_query.message.chat.id, text="Switching on Lamp{}".format(str(i+1))) 
                  c2.switch_on()
                  updateStatement = "UPDATE lamp_status SET status ='on' WHERE id ="+ str(i+1)
                  cursorObject.execute(updateStatement)
                  conn.commit()
              else :
                  bot.send_message(chat_id=update.callback_query.message.chat.id, text="Lamp{} is already on".format(str(i+1)))
                 
    '''
    Method Name: ledlightoff
    Functionality: This function turns the LED light ON in accordance with the users action and store the current status of the lamps in the database
    Returns: None
    ''' 
    def ledlightoff(self,bot,update):
        bot.send_message(chat_id=update.callback_query.message.chat.id, text="Checking Status of light")
        cursorObject = conn.cursor()
        df=pd.read_sql('select count(distinct id) AS "TotalLamps" from lamp_status;', con=conn)
        TotalLamps=df.iat[0,0]
        
        for i in range(TotalLamps):
          df3 = pd.read_sql('SELECT status AS "lampstatus" FROM lamp_status where id = '+str(i+1), con=conn)
          lampstatus=df3.iat[0,0]
          if (lampstatus == 'on') and (i==0):
              bot.send_message(chat_id=update.callback_query.message.chat.id, text="Switching off Lamp{}".format(str(i+1)))
              c1.switch_off()
              updateStatement = "UPDATE lamp_status SET status = 'off' WHERE id ="+ str(i+1)
              cursorObject.execute(updateStatement)
              conn.commit()
          elif (lampstatus == 'on') and (i==1):  
              bot.send_message(chat_id=update.callback_query.message.chat.id, text="Switching off Lamp{}".format(str(i+1)))
              c2.switch_off()
              updateStatement = "UPDATE lamp_status SET status = 'off' WHERE id ="+ str(i+1)
              cursorObject.execute(updateStatement)
              conn.commit()
          else :
             bot.send_message(chat_id=update.callback_query.message.chat.id, text="Lamp{} is already off".format(str(i+1)))
            
             
    '''
    Method Name: addPlant
    Functionality: This function takes the New Plant information as dictionary argument and 
    add the data in Cloud Server
    Returns: None
    '''             
    def addPlant(self,bot,update,New_Plant):
        conn.connect()
        insert_query ="INSERT INTO PlantDatabase(Plant_Name, max_temp_withstand, last_watered, min_humidity, min_soilmoisture)VALUES(%s,%s,SUBTIME(now(), '8:2:5.000001'),%s,%s)"
        data= (New_Plant["Name"],New_Plant["temp"], New_Plant["humidity"],New_Plant["moisture"])
        cursor = conn.cursor()
        cursor.execute(insert_query,data)
        conn.commit()
              
