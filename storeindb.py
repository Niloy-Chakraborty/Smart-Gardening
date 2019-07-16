# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22 13:16:58 2019
Script Name:storeindb.py
This script stores all subscribed data to the database
"""

#Import all the necessary packages

import json
import pymysql

#Checks the topic and sends the data to the required handler
def storeindb(Topic, jsonData):
    if Topic == "Temperature":
      Temp_Data_Handler(jsonData)
    elif Topic == "Relative Humidity":
      Humidity_Data_Handler(jsonData)
    elif Topic == "Luminance":
      Luminance_Data_Handler(jsonData)

   
#Stores Temperature data 
def Temp_Data_Handler(jsonData):
    host="mydbinstance.c1arr1firswu.us-east-2.rds.amazonaws.com"
    port=3306
    dbname="smartGardenDB"
    user="root"
    password="smartgarden"
    conn = pymysql.connect(host, user=user,port=port,passwd=password, db=dbname,autocommit=True)
    temperature_json_dataf = json.loads(jsonData)
    Temp = temperature_json_dataf['Temperature']
    Data_and_Time = temperature_json_dataf['Date_n_Time']
    cur = conn.cursor()
    insert_stmt = ("insert into Temperature_Data (Date_n_Time, Temperature)" 
                   "values (%s, %s)"
                   )
    data = (Data_and_Time, Temp)
    cur.execute(insert_stmt, data)

#Stores Humidity data   
def Humidity_Data_Handler(jsonData):
    host="mydbinstance.c1arr1firswu.us-east-2.rds.amazonaws.com"
    port=3306
    dbname="smartGardenDB"
    user="root"
    password="smartgarden"
    conn = pymysql.connect(host, user=user,port=port,passwd=password, db=dbname,autocommit=True)
    humidity_json_dataf = json.loads(jsonData)
    Data_and_Time = humidity_json_dataf['Date_n_Time']
    Humidity = humidity_json_dataf['Relative_Humidity']
    cur = conn.cursor()
    insert_stmt = ( "insert into Humidity_Data (Date_n_Time, Relative_Humidity)" 
                    "values (%s, %s)"
                    )
    data = (Data_and_Time, Humidity)
    cur.execute(insert_stmt, data)

#Stores Luminance data    
def Luminance_Data_Handler(jsonData):
    host="mydbinstance.c1arr1firswu.us-east-2.rds.amazonaws.com"
    port=3306
    dbname="smartGardenDB"
    user="root"
    password="smartgarden"
    conn = pymysql.connect(host, user=user,port=port,passwd=password, db=dbname,autocommit=True)
    Luminance_json_dataf = json.loads(jsonData)
    Luminance = Luminance_json_dataf['Luminance']
    cur = conn.cursor()
    insert_stmt = ( "insert into Luminance_Data (Luminance)" 
                    "values (%s)"
                    )
    data = (Luminance)
    cur.execute(insert_stmt, data)
    