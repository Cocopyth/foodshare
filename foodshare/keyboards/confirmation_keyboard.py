# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 17:06:36 2020

@author: Coretib
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
confirm,what, when, howmany, howmuch, reminder = map(chr, range(10,16))

buttons = [
    [
     InlineKeyboardButton(text="Confirm", callback_data=confirm)
    ],
    [
        InlineKeyboardButton(text="Change name of the meal", callback_data=what),
        InlineKeyboardButton(text="Change date and hour of the meal", callback_data=when),
    ],
    [
        InlineKeyboardButton(text="Change number of people involved", callback_data=howmany),
        InlineKeyboardButton(text="Change cost of the meal", callback_data=howmuch),
    ],
    [InlineKeyboardButton(text="Change deadline of confirmation for the participants", callback_data=reminder)],
    ]
confirmation_keyboard = InlineKeyboardMarkup(buttons)