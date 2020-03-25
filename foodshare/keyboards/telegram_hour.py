import datetime

from emoji import emojize
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from foodshare.handlers.cook_conversation import get_message

from .digit_list import digit_buttons, emojify_numbers

# Hour keyboard


hour_buttons = digit_buttons.copy()
hour_buttons.append([])

hour_buttons[3].append(
    InlineKeyboardButton(
        emojize(':left_arrow:'), callback_data=emojize(':left_arrow:')
    )
)
hour_buttons[3].append(
    InlineKeyboardButton(emojize(':keycap_0: '), callback_data=str(0))
)
hour_buttons[3].append(
    InlineKeyboardButton(
        emojize(':right_arrow:'), callback_data=emojize(':right_arrow:')
    )
)
hour_keyboard = InlineKeyboardMarkup(hour_buttons)
hour_buttons2 = hour_buttons.copy()
hour_buttons2.append([InlineKeyboardButton('Confirm', callback_data='+')])
confirm_keyboard = InlineKeyboardMarkup(hour_buttons2)
pos = [0, 5, 11, 17]


def process_hour(context):
    ud = context.user_data
    return (
        ud.get('time_hour', False),
        ud.get('ready_to_complete_time', False),
        ud.get('index', False),
    )


def to_emojy(pattern):
    if type(pattern) == int:
        return emojify_numbers(pattern)
    else:
        return '❔'


def hour_to_text(time, index, context):
    emojies = [to_emojy(pattern) for pattern in time]
    general_message = get_message(context, epilog='Please select a time')
    index_message = pos[index] * ' ' + '⬆️'
    hour_message = f'{emojies[0]}{emojies[1]}:{emojies[2]}{emojies[3]}'
    return '\n'.join((general_message, hour_message, index_message))


def process_time_selection(update, context):
    ret_data = (False, None)
    hour, ready_to_confirm, index = process_hour(context)
    ud = context.user_data
    action = update.callback_query.data
    if hour is False:  # Initialize 'time_hour' in ud, : not super clean
        hour = 4 * ['?']
        ud['time_hour'] = hour
        index = 0
        ud['index'] = index
    else:
        hour = ud['time_hour']
        index = ud['index']
    if emojize(':left_arrow:') in action:
        index = max(0, index - 1)
        ud['index'] = index
    elif emojize(':right_arrow:') in action:
        index = min(3, index + 1)
        ud['index'] = index
    elif '+' in action:
        hour, minute = 10 * hour[0] + hour[1], 10 * hour[2] + hour[3]
        timeday = datetime.time(hour=hour, minute=minute)
        time = 4 * ['?']
        ud['time_hour'] = time
        index = 0
        ud['index'] = index
        return True, timeday
    else:
        number = int(action)
        hour[index] = number
        ud['time_hour'] = hour
        index = min(3, index + 1)
        ud['index'] = index
        if '?' in hour:
            ud['ready_to_confirm'] = False
        else:
            ud['ready_to_confirm'] = True
    message = hour_to_text(ud['time_hour'], ud['index'], context)
    update.callback_query.edit_message_text(
        text=message,
        reply_markup=confirm_keyboard
        if ud['ready_to_confirm']
        else hour_keyboard,
    )
    return ret_data
