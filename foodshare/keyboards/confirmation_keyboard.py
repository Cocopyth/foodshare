# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 17:06:36 2020

@author: Coretib
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

confirm, what, when_date, when_time, howmany, howmuch, reminder = map(
    chr, range(10, 17)
)

buttons = [
    [
        InlineKeyboardButton(text='Change name', callback_data=what),
        InlineKeyboardButton(text='Change date', callback_data=when_date),
    ],
    [
        InlineKeyboardButton(text='Change time', callback_data=when_time),
        InlineKeyboardButton(
            text='Change number of people', callback_data=howmany
        ),
    ],
    [
        InlineKeyboardButton(text='Change cost', callback_data=howmuch),
        InlineKeyboardButton(text='Change deadline', callback_data=reminder,),
    ],
    [InlineKeyboardButton(text='Back', callback_data='back')],
]
confirmation_keyboard = InlineKeyboardMarkup(buttons)
