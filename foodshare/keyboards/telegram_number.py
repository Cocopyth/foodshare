from emoji import emojize
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from foodshare.handlers.cook_conversation import get_message

from .digit_list import digit_buttons, emojify_numbers

# Hour keyboard


number_buttons = digit_buttons.copy()
number_buttons.append([])
number_buttons[3].append(
    InlineKeyboardButton(emojize(":keycap_0:"), callback_data=str(0))
)
number_buttons[3].append(
    InlineKeyboardButton(
        emojize(':left_arrow:️'), callback_data=emojize(':left_arrow:️')
    )
)
number_buttons[3].append(
    InlineKeyboardButton('Back to date', callback_data='back')
)
number_keyboard = InlineKeyboardMarkup(number_buttons)
number_buttons2 = number_buttons.copy()
number_buttons2.append([InlineKeyboardButton('Confirm', callback_data='+')])
confirm_keyboard = InlineKeyboardMarkup(number_buttons2)
pos = [0, 5, 11, 17]


def process_context(context):
    ud = context.user_data
    return (
        ud.get('number_process', False),
        ud.get('ready_to_complete_number', False),
        ud.get('indexn', False),
    )


def number_to_text(number, index, context):
    if number == 0:
        emojies = ' '
    else:
        emojies = emojify_numbers(number)
    general_message = get_message(
        context, epilog='Please select a number of people:'
    )
    return '\n'.join((general_message, emojies))


def process_number_selection(update, context):
    ret_data = (False, False, None)
    ud = context.user_data
    action = update.callback_query.data
    number, ready_to_complete, indexn = process_context(context)
    if number is False:  # Initialize 'number_process' in ud, : not super clean
        number = 0
        ud['number_process'] = number
        indexn = 0
        ud['indexn'] = indexn
    if emojize(':left_arrow:️') in action:
        indexn = max(0, indexn - 1)
        ud['indexn'] = indexn
        number = number // 10
        ud['number_process'] = number
    elif 'back' in action:
        ret_data = True, True, number
    elif '+' in action:
        numberf = number
        ud['number_process'] = 0
        indexn = 0
        ud['indexn'] = indexn
        ret_data = True, False, numberf
    else:
        number_key = int(action)
        indexn = indexn + 1
        ud['indexn'] = indexn
        number = 10 * number + number_key
        ud['number_process'] = number
        ud['ready_to_confirm'] = True
    message = number_to_text(ud['number_process'], ud['indexn'], context)
    update.callback_query.edit_message_text(
        text=message,
        reply_markup=confirm_keyboard
        if ud['ready_to_confirm']
        else number_keyboard,
    )
    return ret_data
