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
    [InlineKeyboardButton(text='Confirm', callback_data=confirm)],
    [
        InlineKeyboardButton(
            text='Change name of the meal', callback_data=what
        ),
        InlineKeyboardButton(
            text='Change date of the meal', callback_data=when_date
        ),
    ],
    [
        InlineKeyboardButton(
            text='Change time of the meal', callback_data=when_time
        ),
        InlineKeyboardButton(
            text='Change number of people involved', callback_data=howmany
        ),
    ],
    [
        InlineKeyboardButton(
            text='Change cost of the meal', callback_data=howmuch
        ),
        InlineKeyboardButton(
            text='Change deadline of confirmation for the participants',
            callback_data=reminder,
        ),
    ],
]
confirmation_keyboard = InlineKeyboardMarkup(buttons)
