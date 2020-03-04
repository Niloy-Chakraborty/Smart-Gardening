# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22 13:16:58 2019
Script Name:lamp.py
Script parse data from outputlamp.txt to execute the steps of the lampplanner.
"""


# Open the file with read only permit

#Import all the necessary packages
from plugwise import Stick
from plugwise import Circle
import pymysql
import pandas as pd
import time
s=Stick(port="/dev/ttyUSB0")
c1,c2=Circle("000D6F0005692784",s),Circle("000D6F000416E6F4",s)

host="mydbinstance.c1arr1firswu.us-east-2.rds.amazonaws.com"
port=3306
dbname="smartGardenDB"
user="root"
password="smartgarden"

conn = pymysql.connect(host, user=user,port=port,
                           passwd=password, db=dbname,autocommit=True)

f = open('outputlamp.txt', "r+")
# use readlines to read all lines in the file
# The variable "lines" is a list containing all lines in the file

lines = f.readlines()
# close the file after reading the lines.
f.close()
line1 = []
checkword = 'step'
for i in range(len(lines)):
    if checkword in lines[i]:
        j=i
        break

del lines[0:j]

for i in range(len(lines)):

# check if line is not empty
    if lines[i]=='\n':
        break
        lines.remove(i)
    line1.append(lines[i])
    
del line1[(len(line1)-1):]    
line2=[]
line3=[]
line4=[]
line5=[]
for i in range(len(line1)):
    
    line1[i]=line1[i].split(":")
    line2.append(str(line1[i][1]))

for i in range(len(line2)):
    n=(line2[i].split("\n"))
    line3.append(n[0])
    

for i in range(len(line3)):
    if line3[i]==' SWITCH-ON-LAMP GARDEN LAMP1':
      c1.switch_on()
      cur = conn.cursor()
      #update the lamp1 status to "on" in the database
      updlamp1="update lamp_status set status = 'on' where id= 1"
      cur.execute(updlamp1) 
            
    elif line3[i]==' SWITCH-ON-LAMP GARDEN LAMP2':
      c2.switch_on()
      cur = conn.cursor()
      #update the lamp2 status to "on" in the database
      updlamp2="update lamp_status set status = 'on' where id= 2"
      cur.execute(updlamp2) 
            
    elif line3[i]==' SWITCH-OFF-LAMP GARDEN LAMP1':
      print('OFF LAMP')
      c1.switch_off()
      cur = conn.cursor()
      #update the lamp1 status to "off" in the database
      updlamp3="update lamp_status set status = 'off' where id= 1"
      cur.execute(updlamp3) 
        
    elif line3[i] == ' SWITCH-OFF-LAMP GARDEN LAMP2':
      c2.switch_off()
      cur = conn.cursor()
      #update the lamp2 status to "off" in the database
      updlamp4="update lamp_status set status = 'off' where id= 2"
      cur.execute(updlamp4)






