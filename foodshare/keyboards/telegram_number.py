import copy

from emoji import emojize
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from foodshare.utils import emojize_number

from .digit_list import digit_buttons

# number selection keyboard
number_keyboard_buttons = digit_buttons.copy()
number_keyboard_buttons.append(
    [
        InlineKeyboardButton(
            emojize(':left_arrow:️'), callback_data='left_arrow'
        ),
        InlineKeyboardButton(emojize(':keycap_0:'), callback_data='0'),
    ]
)
number_keyboard_buttons.append(
    [InlineKeyboardButton('Back', callback_data='back')]
)
number_keyboard = InlineKeyboardMarkup(number_keyboard_buttons)

# number selection keyboard with a confirm button and a 0 digit key
confirm_keyboard_buttons = copy.deepcopy(number_keyboard_buttons)

confirm_keyboard_buttons.append(
    [InlineKeyboardButton('Confirm', callback_data='confirm')]
)
confirm_keyboard = InlineKeyboardMarkup(confirm_keyboard_buttons)


def process_number_selection(update, context, suffix=''):
    ud = context.user_data
    callback_data = update.callback_query.data

    # initialize some variables in `context.user_data` when the keyboard is
    # first called
    if '_number' not in ud:
        number = ''
        ud['_number'] = ''
    else:
        number = ud.get('_number')

    # process the keyboard callback data
    if callback_data == 'left_arrow':
        number = number[:-1]
    elif callback_data == 'back':
        ud.pop('_number')
        return False, True, -1
    elif callback_data == 'confirm':
        ud.pop('_number')
        return True, False, int(number)
    else:
        number += callback_data

    # store number for next callback
    ud['_number'] = number

    if number == '':
        number_str = emojize(':question_mark:')
    else:
        number_str = emojize_number(number)

    message = update.callback_query.message.text.split('\n')
    message[-1] = f'For {number_str} {suffix}'
    message = '\n'.join(message)

    # choose keyboard with a confirm button if a valid number was selected
    keyboard = confirm_keyboard if number != '' else number_keyboard

    update.callback_query.edit_message_text(
        text=message, reply_markup=keyboard,
    )

    return False, False, -1
