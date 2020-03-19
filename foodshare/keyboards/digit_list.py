import datetime
from copy import copy

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


# Hour keyboard
def create_callback_data(char):
    """ Create the callback data associated to each button"""
    return str(char)


def separate_callback_data(data):
    """ Separate the callback data"""
    return data.split(';')

numbers = ['0️⃣', '1⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']

def emojify(number):
    num = str(number)
    emojified = ''
    for digit in num:
        emojified += numbers[int(digit)]
    return emojified


digit_buttons = [[InlineKeyboardButton(emojify(i), callback_data=create_callback_data((i))) for i in range(3*k+1,3*(k+1)+1)] for k in range(3)]
