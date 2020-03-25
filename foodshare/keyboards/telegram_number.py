from emoji import emojize
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from foodshare.handlers.cook_conversation import get_message

from .digit_list import digit_buttons, emojify_numbers


# Hour keyboard
def get_epilog(suffix):
    if suffix == '€':
        return 'Please select a price in €'
    else:
        return 'Please select a number'


number_buttons = digit_buttons.copy()
number_buttons.append(
    [
        InlineKeyboardButton(emojize(':keycap_0:'), callback_data='0'),
        InlineKeyboardButton(
            emojize(':left_arrow:️'), callback_data='left_arrow'
        ),
        InlineKeyboardButton('Back to date', callback_data='back'),
    ]
)

number_keyboard = InlineKeyboardMarkup(number_buttons)

confirm_buttons = number_buttons.copy()
confirm_buttons.append(
    [InlineKeyboardButton('Confirm', callback_data='confirm')]
)
confirm_keyboard = InlineKeyboardMarkup(confirm_buttons)


def number_to_text(number, context, suffix):
    if number == 0:
        emojies = ' '
    else:
        emojies = emojify_numbers(number) + suffix
    epilog = get_epilog(suffix)
    general_message = get_message(context, epilog=epilog)
    return '\n'.join((general_message, emojies))


def process_number_selection(update, context, suffix=''):
    ud = context.user_data
    action = update.callback_query.data

    # initialize some variables in user_data
    if '_number' not in ud:
        number = 0
    else:
        number = ud.get('_number')

    if action == 'left_arrow':
        number = number // 10
    elif action == 'back':
        ud.pop('_number')
        return False, True, -1
    elif action == 'confirm':
        ud.pop('_number')
        return True, False, number
    else:
        number_key = int(action)
        number = 10 * number + number_key

    ud['_number'] = number

    message = number_to_text(ud['number_process'], context, suffix)

    update.callback_query.edit_message_text(
        text=message,
        reply_markup=confirm_keyboard if number > 0 else number_keyboard,
    )

    return False, False, -1
