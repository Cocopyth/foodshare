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


row1 = []
row2 = []
row3 = []
row1.append(InlineKeyboardButton('7️⃣', callback_data=create_callback_data(7)))
row1.append(InlineKeyboardButton('8️⃣', callback_data=create_callback_data(8)))
row1.append(InlineKeyboardButton('9️⃣', callback_data=create_callback_data(9)))
row2.append(InlineKeyboardButton('4️⃣', callback_data=create_callback_data(4)))
row2.append(InlineKeyboardButton('5️⃣', callback_data=create_callback_data(5)))
row2.append(InlineKeyboardButton('6️⃣', callback_data=create_callback_data(6)))
row3.append(InlineKeyboardButton('1️⃣', callback_data=create_callback_data(1)))
row3.append(InlineKeyboardButton('2️⃣', callback_data=create_callback_data(2)))
row3.append(InlineKeyboardButton('3️⃣', callback_data=create_callback_data(3)))
hour_buttons = [row1, row2, row3]
hour_buttons.append([])
hour_buttons[3].append(InlineKeyboardButton('⬅️', callback_data='⬅️'))
hour_buttons[3].append(
    InlineKeyboardButton('0️⃣', callback_data=create_callback_data(0))
)
hour_buttons[3].append(InlineKeyboardButton('➡️', callback_data='➡️'))
hour_keyboard = InlineKeyboardMarkup(hour_buttons)
hour_buttons2 = copy(hour_buttons)
hour_buttons2.append([InlineKeyboardButton('Confirm', callback_data='+')])
confirm_keyboard = InlineKeyboardMarkup(hour_buttons2)
pos = [0, 5, 11, 17]

numbers = ['0️⃣', '1⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']


def process_time_selection(update, context):
    ret_data = (False, None)
    ud = context.user_data
    bot = context.bot
    query = update.callback_query
    messages = query.message.text.split('\n')
    action = query.data
    hourmin = messages[-2].replace(':', ' ').split(' ')
    if '❔' in hourmin:
        keyboard = hour_keyboard
    else:
        keyboard = confirm_keyboard
    if 'time' in ud:
        time = ud['time']
        index = ud['index']
    else:
        time = '❔ ❔:❔ ❔'
        ud['time'] = time
        index = 0
        ud['index'] = index

    if '⬅️' in action:
        index = max(0, index - 1)
        ud['index'] = index
        messages[-1] = pos[index] * ' ' + '⬆️'
        reply = '\n'.join(messages)
        bot.edit_message_text(
            text=reply,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            reply_markup=keyboard,
        )
    elif '➡️' in action:
        index = min(3, index + 1)
        ud['index'] = index
        messages[-1] = pos[index] * ' ' + '⬆️'
        reply = '\n'.join(messages)
        bot.edit_message_text(
            text=reply,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            reply_markup=keyboard,
        )
    elif '+' in action:
        hourmin = messages[-2].replace(':', ' ').split(' ')
        hour = 10 * numbers.index(hourmin[0]) + numbers.index(hourmin[1])
        minute = 10 * numbers.index(hourmin[2]) + numbers.index(hourmin[3])
        timeday = datetime.time(hour=hour, minute=minute)
        time = '❔ ❔:❔ ❔'
        ud['time'] = time
        index = 0
        ud['index'] = index
        print(timeday)
        ret_data = True, timeday
    else:
        hourmin = messages[-2].replace(':', ' ').split(' ')
        number = int(action)
        hourmin[index] = ' ' + numbers[number]
        if '❔' in hourmin:
            keyboard = hour_keyboard
        else:
            keyboard = confirm_keyboard
        messages[-2] = ' '.join(hourmin[:2]) + ':' + ' '.join(hourmin[2:])
        ud['time'] = messages[-2]
        index = min(3, index + 1)
        ud['index'] = index
        messages[-1] = pos[index] * ' ' + '⬆️'
        reply = '\n'.join(messages)
        bot.edit_message_text(
            text=reply,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            reply_markup=keyboard,
        )
    return ret_data
