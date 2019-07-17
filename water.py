# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22 13:16:58 2019
Script Name:water.py
Script parse data from outputwater.txt to execute the steps of the waterplanner.
"""


# Open the file with read only permit

#Import all the necessary packages
from plugwise import Stick
from plugwise import Circle
import pymysql
import time

s=Stick(port="/dev/ttyUSB0")
c1,c2=Circle("000D6F0005692784",s),Circle("000D6F000416E6F4",s)


#Database Connection
moisturecontentold=list()
host="mydbinstance.c1arr1firswu.us-east-2.rds.amazonaws.com"
port=3306
dbname="smartGardenDB"
user="root"
password="smartgarden"

conn = pymysql.connect(host, user=user,port=port,
                           passwd=password, db=dbname)
cursorObject = conn.cursor() 
                          
#Read the planner output                          
f = open('outputwater.txt', "r+")
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
    n=(line2[i].split(" "))

    line3.append(n[1])
    line4.append(n[2])
    line5.append(n[3])

for i in range(len(line2)):
    if line3[i]=='WATERING':
        if line5[i]=='PLANT1\n':
            c1.switch_on()
            updateStatement = "UPDATE PlantDatabase SET last_watered = now() WHERE Plant_ID =1"
            # Execute the SQL UPDATE statement to insert the time of watering
            cursorObject.execute(updateStatement)
            conn.commit()
            
        elif line5[i]=='PLANT2\n':
            c2.switch_on()
            updateStatement = "UPDATE PlantDatabase SET last_watered = now() WHERE Plant_ID =2"
            # Execute the SQL UPDATE statement to insert the time of watering
            cursorObject.execute(updateStatement)
            conn.commit()
    elif line3[i]=='AFTERWATERING':
        if line5[i] == 'PLANT1\n':
            c1.switch_off()
        elif line5[i] == 'PLANT2\n':
            c2.switch_off()
time.sleep(10)
c1.switch_off()
c2.switch_off()






