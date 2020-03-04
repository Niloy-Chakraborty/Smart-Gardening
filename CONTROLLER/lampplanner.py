# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22 13:16:58 2019
Script Name:lampplanner.py
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

global presentlampstatusold
global lampstatusold
global temperature
global humidity


global requiredluminancelevel
requiredluminancelevel=40
lampstatusold=list()

					   
while True:
   
  host="mydbinstance.c1arr1firswu.us-east-2.rds.amazonaws.com"
  port=3306
  dbname="smartGardenDB"
  user="root"
  password="smartgarden"

  conn = pymysql.connect(host, user=user,port=port,
                           passwd=password, db=dbname)
  #fetching the present luminance level, status of lamp1 and lamp2 from database 
  presentlampstatus=list()      
  df=pd.read_sql('SELECT * FROM Luminance_Data ORDER BY ID DESC LIMIT 1;', con=conn)
  Luminance=int(df.iat[0,1])
  df1=pd.read_sql('SELECT status AS "status1" FROM lamp_status where id =' + str(1), con=conn)
  statusoflamp1 = df1.iat[0,0]
  df2=pd.read_sql('SELECT status AS "status2" FROM lamp_status where id ='+ str(2), con=conn)
  statusoflamp2 = df2.iat[0,0]
  presentlampstatus.append(statusoflamp1)
  presentlampstatus.append(statusoflamp2)
 
  
  #deciding the presentluminancelevel based on sensordata and lampstatus
  if ((Luminance < 20) and (statusoflamp1=='on') and (statusoflamp2=='on')):
    presentluminancelevel = 40
  elif ((Luminance < 20) and (statusoflamp1=='on') and (statusoflamp2=='off')):
    presentluminancelevel = 30
  elif ((Luminance < 20) and (statusoflamp1=='off') and (statusoflamp2=='on')):
    presentluminancelevel = 30
  elif ((Luminance < 20) and (statusoflamp1=='off') and (statusoflamp2=='off')):
    presentluminancelevel = 20
  elif ((Luminance >= 20)and (Luminance < 40) and (statusoflamp1=='on') and (statusoflamp2=='on')):
    presentluminancelevel = 50
  elif ((Luminance >= 20)and(Luminance < 40) and (statusoflamp1=='on') and (statusoflamp2=='off')):
    presentluminancelevel = 40 
  elif ((Luminance >= 20)and (Luminance < 40) and (statusoflamp1=='off') and (statusoflamp2=='on')):
    presentluminancelevel = 40
  elif ((Luminance >= 20)and (Luminance < 40) and (statusoflamp1=='off') and (statusoflamp2=='off')):
    presentluminancelevel = 30
  elif ((Luminance >= 40) and (statusoflamp1=='on') and (statusoflamp2=='on')):
    presentluminancelevel = 60 
  elif ((Luminance >= 40) and (statusoflamp1=='off') and (statusoflamp2=='on')):
    presentluminancelevel = 50 
  elif ((Luminance >= 40) and (statusoflamp1=='on') and (statusoflamp2=='off')):
    presentluminancelevel = 50 
  elif ((Luminance >= 40) and (statusoflamp1=='off') and (statusoflamp2=='off')):
    presentluminancelevel = 40 
 
  #generate problem file and execute if presentluminancelevel is not equal to requiredluminancelevel
  if(presentluminancelevel != requiredluminancelevel):
		  # The written code is generated to the "out" variable.
      out = """
(define (problem metricLight-smartGarden) 
  (:domain metricLight) 
  (:objects lamp1 lamp2 garden)
  (:init (lamp lamp1)
		     (lamp lamp2)
         (garden garden)                    
      	  """
      for i in range(2):
        if (presentlampstatus[i]=='on'):
          out += "       (on lamp{})".format(i+1)
          out += """
      	    """
        else:
          out += "(not(on lamp{}))".format(i+1)
      out += """
          (= (lamp-luminescence-level lamp1) 10) 
          (= (lamp-luminescence-level lamp2) 10)
      	    """
      out += "(=(presentluminescencelevel garden){})".format(presentluminancelevel)  
      out += """
  (= (requiredluminescencelevel garden) 40)
  (= (total-no-lamp-used) 0)
  (= (count)0) 
   )
  (:goal (=(presentluminescencelevel garden)(requiredluminescencelevel garden))
         )
  (:metric minimize (total-no-lamp-used))
  )  
          """ 
        
      filename = "smartGardenlighting_problem"
      with open(filename, "w") as f:
        f.write(out)
       
      #Extract Steps from outputfile and turn on motor accordingly
      myCmd = './ff -o smartGardenlighting_domain.pddl -f smartGardenlighting_problem > outputlamp.txt'
      os.system(myCmd)
      myCmd = 'python lamp.py'
      os.system(myCmd)

  
  time.sleep(10)
  
  
  

  
     
  

  
     

    
