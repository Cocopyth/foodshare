import datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from foodshare.handlers.cook_conversation import get_message

from .digit_list import digit_buttons, emojify_numbers

# Hour keyboard


hour_buttons = digit_buttons.copy()
hour_buttons.append([])

hour_buttons[3].append(InlineKeyboardButton('⬅️', callback_data='⬅️'))
hour_buttons[3].append(InlineKeyboardButton('0️⃣', callback_data=str(0)))
hour_buttons[3].append(InlineKeyboardButton('➡️', callback_data='➡️'))
hour_keyboard = InlineKeyboardMarkup(hour_buttons)
hour_buttons2 = hour_buttons.copy()
hour_buttons2.append([InlineKeyboardButton('Confirm', callback_data='+')])
confirm_keyboard = InlineKeyboardMarkup(hour_buttons2)
pos = [0, 5, 11, 17]


def process_hour(context):
    ud = context.user_data
    return (
        ud.get('time', False),
        ud.get('ready_to_complete_time', False),
        ud.get('index', False),
    )


def to_emojy(pattern):
    if type(pattern) == int:
        return emojify_numbers(pattern)
    else:
        return '❔'


def hour_to_text(time, index):
    emojies = [to_emojy(pattern) for pattern in time]
    index_message = pos[index] * ' ' + '⬆️'
    hour_message = f'{emojies[0]}{emojies[1]}:{emojies[2]}{emojies[3]}'
    return '\n'.join((hour_message, index_message))


def get_keyboard(ready_to_confirm):
    if ready_to_confirm:
        keyboard = confirm_keyboard
    else:
        keyboard = hour_keyboard
    return keyboard


def process_time_selection(update, context):
    ret_data = (False, None)
    hour, ready_to_confirm, index = process_hour(context)
    ud = context.user_data
    action = update.callback_query.data
    if hour == False:  # Initialize 'time' in ud
        hour = 4 * ['?']
        ud['time'] = hour
        index = 0
        ud['index'] = index
    else:
        hour = ud['time']
        index = ud['index']
    if '⬅️' in action:
        index = max(0, index - 1)
        ud['index'] = index
        message = (
            get_message(context, epilog='Please select a time')
            + '\n'
            + hour_to_text(ud['time'], index)
        )
        update.callback_query.edit_message_text(
            text=message, reply_markup=get_keyboard(ready_to_confirm),
        )
    elif '➡️' in action:
        index = min(3, index + 1)
        ud['index'] = index
        message = (
            get_message(context, epilog='Please select a time')
            + '\n'
            + hour_to_text(ud['time'], index)
        )
        update.callback_query.edit_message_text(
            text=message, reply_markup=get_keyboard(ready_to_confirm),
        )
    elif '+' in action:
        hour, minute = 10 * hour[0] + hour[1], 10 * hour[2] + hour[3]
        timeday = datetime.time(hour=hour, minute=minute)
        time = 4 * ['?']
        ud['time'] = time
        index = 0
        ud['index'] = index
        return (True, timeday)
    else:
        number = int(action)
        hour[index] = number
        ud['time'] = hour
        index = min(3, index + 1)
        ud['index'] = index
        message = (
            get_message(context, epilog='Please select a time')
            + '\n'
            + hour_to_text(ud['time'], index)
        )
        if '?' in hour:
            ud['ready_to_confirm'] = False
        else:
            ud['ready_to_confirm'] = True
        update.callback_query.edit_message_text(
            text=message, reply_markup=get_keyboard(ud['ready_to_confirm']),
        )
    return ret_data
