from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from .digit_list import digit_buttons
from emoji import emojize
# Hour keyboard


number_buttons = digit_buttons.copy()
number_buttons.append([])
number_buttons[3].append(InlineKeyboardButton(emojize(":keycap_0:"), callback_data=str(0)))
number_buttons[3].append(InlineKeyboardButton(emojize(':left_arrow:️'), callback_data=emojize(':left_arrow:️')))
number_buttons[3].append(
    InlineKeyboardButton('Back to date', callback_data=emojize(':right_arrow:'))
)
number_keyboard = InlineKeyboardMarkup(number_buttons)
pos = [0, 5, 11, 17]


def process_number_selection(update, context):
    ret_data = (False, False, None)
    ud = context.user_data
    query = update.callback_query
    action = query.data
    if 'number' in ud:
        number = ud['number']
        indexn = ud['indexn']
    else:
        number = 0
        ud['number'] = number
        indexn = 0
        ud['indexn'] = indexn
    if emojize(':left_arrow:️') in action:
        indexn = max(0, indexn - 1)
        ud['indexn'] = indexn
        number = number // 10
        ud['number'] = number
        if number == 0:
            messages[-1] = ' '
        else:
            messages[-1] = str(number)
        reply = '\n'.join(messages)
        bot.edit_message_text(
            text=reply,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            reply_markup=number_keyboard,
        )
    elif emojize(':right_arrow:') in action:
        ret_data = True, True, number
    elif '+' in action:
        numberf = number
        ud['number'] = 0
        indexn = 0
        ud['indexn'] = indexn
        ret_data = True, False, numberf
    else:
        numberkey = int(action)
        indexn = indexn + 1
        ud['indexn'] = indexn
        number = 10 * number + numberkey
        ud['number'] = number
        if number == 0:
            messages[-1] = ' '
        else:
            messages[-1] = str(number)
        reply = '\n'.join(messages)
        if number != 0:
            if len(number_buttons) <= 4:
                number_buttons.append(
                    [InlineKeyboardButton('Confirm', callback_data='+')]
                )
            new_keyboard = InlineKeyboardMarkup(number_buttons)
            bot.edit_message_text(
                text=reply,
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                reply_markup=new_keyboard,
            )
        else:
            bot.edit_message_text(
                text=reply,
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                reply_markup=number_keyboard,
            )
    return ret_data
