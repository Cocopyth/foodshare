import datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from .digit_list import digit_buttons, numbers_emoji

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
        hour = 10 * numbers_emoji.index(hourmin[0]) + numbers_emoji.index(
            hourmin[1]
        )
        minute = 10 * numbers_emoji.index(hourmin[2]) + numbers_emoji.index(
            hourmin[3]
        )
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
        hourmin[index] = ' ' + numbers_emoji[number]
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
