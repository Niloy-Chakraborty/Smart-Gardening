# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22 13:16:58 2019
Script Name:telegramapp.py
"""
#Import all the necessary packages
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, Dispatcher,BaseFilter
import threading
import os
from iotcontrol import iotcontrol
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from openzwave.option import ZWaveOption
from openzwave.network import ZWaveNetwork


darkskyKey = '09fe86ac7768a3e47d9a26b7a1998edc'
control = iotcontrol(821193235,darkskyKey,48.933,8.9612)

New_Plant= {}



def start(bot,update): #display menu
    #BotFunction: First function using which users are supposed to interact with this bot

    
        
    keyboard = [[InlineKeyboardButton("Instructions", callback_data='1')], 
                    [InlineKeyboardButton("Take Picture", callback_data='2')],
                    [InlineKeyboardButton("Water Plants", callback_data='3')],
                    [InlineKeyboardButton("Led Lights on", callback_data='4')],
                    [InlineKeyboardButton("Led Lights off", callback_data='5')],
                    [InlineKeyboardButton("Subscribe to Garden Status", callback_data='7')],
                    [InlineKeyboardButton("Local Weather", callback_data='8')],
                    [InlineKeyboardButton("Know Your Plant", callback_data='9')],
                    [InlineKeyboardButton("Add a new Plant", callback_data='10')]
                    ]
    
    message="Hello {} (telegram_id:{}).\nType& send:/start again to pull up menu at any time.\n*Disclaimer: Bot logs all user commands. \nPlease Choose: \n".format(update.message.from_user.first_name,update.message.from_user.id)
    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.send_message(chat_id=update.message.chat_id,text=message, reply_markup=reply_markup)
    
    
        


def button(bot,update):
    # BotFunction: Function that implements the button 
    query = update.callback_query
    bot.answer_callback_query(callback_query_id=query.id, text="Choice registered,processing request..")
    
    if(query.data=='1'):
        control.instructions(bot,update)

    if(query.data=='2'):
        control.camera(bot,update)
        
    if(query.data=='3'):
        control.water(bot,update)
            
    if(query.data=='4'):
        control.ledlighton(bot,update)
        
    if(query.data=='5'):
        control.ledlightoff(bot,update)    
    
    if(query.data=='7'):
         threading.Thread(target= control.gardenstatus, args= (bot,update)).start()

    if(query.data=='8'):
        control.localweather(bot,update)

    if(query.data=='9'):
        threading.Thread(target= control.knowPlant, args= (bot,update)).start()

    if(query.data=='10'):

        bot.send_message(chat_id=update.callback_query.message.chat.id,text='Please type "/Plant" to start the Plant Addition Bot')
        
        
       
        
############# Plant Addition Chat Bot ####################
def Plant(bot,update):
    print("Plant called")
    bot.send_message(chat_id=update.message.chat_id,text='Hi I am your Plant Adder Bot.... To add a new plant, Please type the \n 1)Plant Name \n 2)the Max Temperature Withstand (in Celcius)\n 3) Min Humidity \n 4) Min Soil Moisture \n ....that are required for this plant.\n Type as comma-separated values')
    echo_handler = MessageHandler(Filters.text, echo)
    dispatcher.add_handler(echo_handler)
    
    
def echo(bot, update):
    print(update.message['text'])
   
    lis= update.message['text'].split(",")
    if len(lis)==4 and isinstance(lis[0], str) and lis[1].isdigit() and lis[2].isdigit and lis[3].isdigit():
        New_Plant["Name"]= lis[0]
        New_Plant["temp"]= lis[1]
        New_Plant["humidity"]= lis[2]
        New_Plant["moisture"]= lis[3]
    else:
        bot.send_message(chat_id=update.message.chat_id,text='Wrong input!!!')
        bot.send_message(chat_id=update.message.chat_id,text='Hi I am your Plant Adder Bot.... To add a new plant, Please type the \n 1)Plant Name \n 2)the Max Temperature Withstand (in Celcius)\n 3) Min Humidity \n 4) Min Soil Moisture \n ....that are required for this plant.\n Type as comma-separated values')
        return
    print(New_Plant)
         
    bot.send_message(chat_id=update.message.chat_id,text='You just typed Plant Name: '+New_Plant["Name"]+"\nTemperature: " +New_Plant["temp"]+"\n Min Humidity: "+ New_Plant["humidity"]+"\n Moisture: " +New_Plant["moisture"])
    
    
    bot.send_message(chat_id=update.message.chat_id,text='Please type "/addToDB" command to add these data to the DB')
    addToDB_handler = CommandHandler('addToDB',addToDB)
    dispatcher.add_handler(addToDB_handler)
    
def addToDB(bot, update):
    if update.message.text == "/addToDB" :
        control.addPlant(bot,update, New_Plant)
        bot.send_message(chat_id=update.message.chat_id,text='The data has been added to DB')
        
        bot.send_message(chat_id=update.message.chat_id,text='Please type "/start" command to show the main menu')
    else:
        bot.send_message(chat_id=update.message.chat_id,text='Wrong Command!!! \n Please type "/addToDB" command to add these data to the DB')
        return 
    
    
    
############# Admin only program functions####################
def unknown(bot, update, message):
    #Unkwown command handler
    logging.info('/unknown,{},{}'.format(update.message.from_user.first_name,update.message.from_user.id))
    bot.send_message(chat_id=update.message.chat_id, text="Sorry Command Not Recognized! Type: /start for all user actions.")            
    
def shutdown():
    
    updater.stop()
    updater.is_idle=False

def stop(bot, update): #hardcoded for security only admin can issue this command
    """ 
    Admin Command: stop the bot
    Usage:
        /stop
        
    """
    #global adminId
    logging.info('/stop,{},{}'.format(update.message.from_user.first_name,update.message.from_user.id))
    if(update.message.from_user.id==control.getAdminId()):
        bot.send_message(chat_id=update.message.chat_id, text="Stopping Server!")    
        threading.Thread(target=shutdown).start()
    else:
        bot.send_message(chat_id=update.message.chat_id, text="ERROR: Unauthorized User!")

def addIoTUser(bot,update,args):
    """ 
    Admin Command: add users manually
    Usage:
        /add 12345 324567 8726251
        
        The numbers are ids of users
        
    """
    control.addIoTUser(bot,update,args)

        
        
def removeIoTUser(bot,update,args):
    """ 
    Admin Command: remove users manually
    Usage:
        /rm all
        /rm 123445
    """
    control.removeIoTUser(bot,update,args)

        

def fetchIoTUserList(bot,update):
    
    """ 
    Admin Command: add users manually
    Usage:
        /fetch
        
    """
    control.fetchIoTUserList(bot,update)
    
    



                    
 
        



############# Directing the telegram bot on how to treat commands ####################  
updater = Updater('809471934:AAFjmcrJrzxbBpsMVReiWr37Hx_htFJvU38')
dispatcher = updater.dispatcher
print("Bot started") 
start_handler = CommandHandler('start',start)
stop_handler = CommandHandler('stop', stop)
addHandler = CommandHandler('add',addIoTUser, pass_args=True)
removeHandler = CommandHandler('rm',removeIoTUser,pass_args=True)
fetchHandler = CommandHandler('fetch',fetchIoTUserList)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(CallbackQueryHandler(button))
dispatcher.add_handler(stop_handler)
dispatcher.add_handler(addHandler)
dispatcher.add_handler(removeHandler)
dispatcher.add_handler(fetchHandler)

   
Plant_handler = CommandHandler('Plant',Plant)
dispatcher.add_handler(Plant_handler)


updater.start_polling()

updater.idle()

