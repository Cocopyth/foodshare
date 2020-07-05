import datetime

from emoji import emojize
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from foodshare.handlers.cook_conversation import get_message
from foodshare.utils import emojize_number

from .digit_list import digit_buttons
from foodshare.bdd.database_communication import get_user_from_chat_id
# Hour keyboard


user_buttons = digit_buttons.copy()
user_buttons.append(
    [
        InlineKeyboardButton(emojize(':keycap_0: '), callback_data=str(0)),
        InlineKeyboardButton(
            emojize(':left_arrow:'), callback_data='left_arrow'
        ),
    ]
)
user_buttons.append(
[
        InlineKeyboardButton(emojize(':arrow_backward:'),
                             callback_data='backward_page'),
        InlineKeyboardButton(
            emojize(':arrow_forward:'), callback_data='forward_page'
        ),
    ]
)
user_buttons.append(
    [InlineKeyboardButton(emojize('Back'), callback_data='back')]
)
user_keyboard = InlineKeyboardMarkup(user_buttons)
confirm_buttons = user_buttons.copy()
confirm_buttons.append(
    [InlineKeyboardButton('Confirm', callback_data='confirm')]
)
confirm_keyboard = InlineKeyboardMarkup(confirm_buttons)
pos = [0, 5, 11, 17]


def process_user_selection(update, context, suffix=''):
    ud = context.user_data
    callback_data = update.callback_query.data
    chat_id = update.effective_chat.id
    user = get_user_from_chat_id(chat_id)
    members = user.community.members
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
    keyboard = confirm_keyboard if number != '' else user_keyboard

    update.callback_query.edit_message_text(
        text=message, reply_markup=keyboard,
    )

    return False, False, -1

def construct_message(community,money, page=0, prolog=''):
    members = community.members
    members_to_show = members[10*page:10*page+10]
    member_messages=[prolog]
    i = page+1
    for j,member in enumerate(members_to_show):
        balance = member.money_balance if money else member.meal_balance
        member_messages.append(f'{i+j}. {member.name}, balance : {balance}')
    epilog = 'Type the number corresponding to the user you want to make a ' \
             'transaction to. Navigate with the arrows'
    member_messages.append(epilog)
    message = '\n'.join(member_messages)
    return message