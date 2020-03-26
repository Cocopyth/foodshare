import datetime

from emoji import emojize
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from foodshare.handlers.cook_conversation import get_message
from foodshare.utils import emojize_number

from .digit_list import digit_buttons

# Hour keyboard


hour_buttons = digit_buttons.copy()
hour_buttons.append([])

hour_buttons[3].append(
    InlineKeyboardButton(emojize(':left_arrow:'), callback_data='left_arrow')
)
hour_buttons[3].append(
    InlineKeyboardButton(emojize(':keycap_0: '), callback_data=str(0))
)
hour_buttons[3].append(
    InlineKeyboardButton(emojize(':right_arrow:'), callback_data='right_arrow')
)
hour_keyboard = InlineKeyboardMarkup(hour_buttons)
confirm_buttons = hour_buttons.copy()
confirm_buttons.append(
    [InlineKeyboardButton('Confirm', callback_data='confirm')]
)
confirm_keyboard = InlineKeyboardMarkup(confirm_buttons)
pos = [0, 5, 11, 17]


def to_emojy(pattern):
    if type(pattern) == int:
        return emojize_number(pattern)
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
    ud = context.user_data
    action = update.callback_query.data
    if '_hour' not in ud:  # Initialize '_hour' in ud, : not super clean
        hour = 4 * ['?']
        ud['_hour'] = hour
        index = 0
    else:
        hour = ud['_hour']
        index = ud['_index']
    if action == 'left_arrow':
        index = max(0, index - 1)
    elif action == 'right_arrow':
        index = min(3, index + 1)
    elif action == 'confirm':
        hour, minute = 10 * hour[0] + hour[1], 10 * hour[2] + hour[3]
        timeday = datetime.time(hour=hour, minute=minute)
        ud.pop('_hour')
        ud.pop('_index')
        return True, timeday
    else:
        number = int(action)
        hour[index] = number
        index = min(3, index + 1)
    ud['_index'] = index
    ud['_hour'] = hour
    message = hour_to_text(ud['_hour'], ud['_index'], context)
    update.callback_query.edit_message_text(
        text=message,
        reply_markup=confirm_keyboard if '?' not in hour else hour_keyboard,
    )
    return ret_data
