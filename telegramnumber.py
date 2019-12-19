# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 11:33:44 2019

@author: Coretib
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup,ReplyKeyboardRemove
import datetime

#Hour keyboard
def create_callback_data(char):
    """ Create the callback data associated to each button"""
    return str(char)
def separate_callback_data(data):
    """ Separate the callback data"""
    return data.split(";")

row1=[]
row2=[]
row3=[]
row1.append(InlineKeyboardButton('7️⃣',callback_data=create_callback_data(7)))
row1.append(InlineKeyboardButton('8️⃣',callback_data=create_callback_data(8)))
row1.append(InlineKeyboardButton('9️⃣',callback_data=create_callback_data(9)))
row2.append(InlineKeyboardButton('4️⃣',callback_data=create_callback_data(4)))
row2.append(InlineKeyboardButton('5️⃣',callback_data=create_callback_data(5)))
row2.append(InlineKeyboardButton('6️⃣',callback_data=create_callback_data(6)))
row3.append(InlineKeyboardButton('1️⃣',callback_data=create_callback_data(1)))
row3.append(InlineKeyboardButton('2️⃣',callback_data=create_callback_data(2)))
row3.append(InlineKeyboardButton('3️⃣',callback_data=create_callback_data(3)))
hour_buttons=[row1,row2,row3]
hour_buttons.append([])
hour_buttons[3].append(InlineKeyboardButton('0️⃣',callback_data=create_callback_data(0)))
hour_buttons[3].append(InlineKeyboardButton('⬅️',callback_data='⬅️'))
hour_buttons[3].append(InlineKeyboardButton('Back to date',callback_data='➡️'))
number_keyboard = InlineKeyboardMarkup(hour_buttons)
pos=[0,5,11,17]

numbers=['0️⃣','1⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣']
def emojify(number):
    num=str(number)
    emojified=''
    for digit in num:
        emojified+=numbers[int(digit)]
    return(emojified)
        
def process_number_selection(update,context):
    ret_data = (False,False,None)
    ud = context.user_data
    bot=context.bot
    query = update.callback_query
    messages=query.message.text.split('\n')
    action = query.data
    if "number" in ud:
        number=ud["number"]
        indexn=ud['indexn']
    else:
        number =0
        ud["number"]=number
        indexn=0
        ud['indexn']=indexn
    if '⬅️' in action:
        indexn=max(0,indexn-1)
        ud['indexn']=indexn
        number=number//10
        ud['number']=number
        if number ==0:
            messages[-1]=' '
        else:
            messages[-1]=str(number)
        reply="\n".join(messages)
        bot.edit_message_text(text=reply,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            reply_markup=number_keyboard)
    elif '➡️' in action:
        ret_data=True,True,number
    elif '+' in action:
        numberf=number
        ud["number"]=0
        indexn=0
        ud['indexn']=indexn
        ret_data=True,False,numberf
    else:
        numberkey=int(action)
        indexn=indexn+1
        ud['indexn']=indexn
        number=10*number+numberkey
        ud["number"]=number
        if number ==0:
            messages[-1]=' '
        else:
            messages[-1]=str(number)
        reply="\n".join(messages)
        if number !=0:
            if len(hour_buttons)<=4:    
                hour_buttons.append([InlineKeyboardButton('Confirm',callback_data='+')])
            new_keyboard = InlineKeyboardMarkup(hour_buttons)
            bot.edit_message_text(text=reply,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            reply_markup=new_keyboard)
        else:
            bot.edit_message_text(text=reply,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            reply_markup=number_keyboard)
    return ret_data