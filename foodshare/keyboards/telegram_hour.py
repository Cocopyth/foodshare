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
        ud['time_hour'] = hour
        index = 0
        ud['index'] = index
    else:
        hour = ud['time_hour']
        index = ud['index']
    if '⬅️' in action:
        index = max(0, index - 1)
        ud['index'] = index
        message = hour_to_text(ud['time_hour'], index, context)

        update.callback_query.edit_message_text(
            text=message, reply_markup=get_keyboard(ready_to_confirm),
        )
    elif '➡️' in action:
        index = min(3, index + 1)
        ud['index'] = index
        message = hour_to_text(ud['time_hour'], index, context)

        update.callback_query.edit_message_text(
            text=message, reply_markup=get_keyboard(ready_to_confirm),
        )
    elif '+' in action:
        hour, minute = 10 * hour[0] + hour[1], 10 * hour[2] + hour[3]
        timeday = datetime.time(hour=hour, minute=minute)
        print(timeday)
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
        message = hour_to_text(ud['time_hour'], index, context)
        if '?' in hour:
            ud['ready_to_confirm'] = False
        else:
            ud['ready_to_confirm'] = True
        update.callback_query.edit_message_text(
            text=message, reply_markup=get_keyboard(ud['ready_to_confirm']),
        )
    return ret_data
