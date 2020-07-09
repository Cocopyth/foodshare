from emoji import emojize
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode

from foodshare.bdd.database_communication import get_user_from_chat_id

from .digit_list import digit_buttons

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
        InlineKeyboardButton(
            emojize(':reverse_button:'), callback_data='backward_page'
        ),
        InlineKeyboardButton(
            emojize(':play_button:'), callback_data='forward_page'
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


def process_user_selection(update, context):
    ud = context.user_data
    money = ud['money_or_meal']
    callback_data = update.callback_query.data
    chat_id = update.effective_chat.id
    user = get_user_from_chat_id(chat_id)
    members = [
        member for member in user.community.members if member is not user
    ]
    # initialize some variables in `context.user_data` when the keyboard is
    # first called
    if '_number' not in ud:
        number = ''
        ud['_number'] = ''
    else:
        number = ud.get('_number')
    if '_page' not in ud:
        page = 0
        ud['_page'] = 0
    else:
        page = ud.get('_page')

    # process the keyboard callback data
    if callback_data == 'forward_page':
        page += 1
    elif callback_data == 'backward_page':
        page -= 1
    elif callback_data == 'back':
        ud.pop('_number')
        ud.pop('_page')
        return False, True, -1
    elif callback_data == 'confirm':
        user_chosed = members[int(number) - 1]
        ud.pop('_number')
        ud.pop('_page')
        return True, False, user_chosed
    else:
        number = callback_data

    # store number for next callback
    ud['_number'] = number
    ud['_page'] = page

    if number == '':
        message = 'Please select a user to make the transaction with'
    else:
        user_chosed = members[int(number) - 1]
        message = (
            f'You chosed *'
            f' {user_chosed.name}.* \n Press '
            f'confirm to continue. \n'
        )
    # choose keyboard with a confirm button if a valid number was selected
    keyboard = construct_keyboard(user, money, number != '', page)
    update.callback_query.edit_message_text(
        text=message, reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN,
    )
    return False, False, -1


def construct_keyboard(user, money, confirm, page=0, number_per_page=5):
    members = [
        member for member in user.community.members if member is not user
    ]
    number_of_pages = len(members) // number_per_page + (
        len(members) % number_per_page > 0
    )
    page = page % (number_of_pages)
    members_to_show = members[
        number_per_page * page : number_per_page * page + number_per_page
    ]
    i = page + 1
    buttons = []
    for j, member in enumerate(members_to_show):
        balance = (
            str(member.money_balance) + '€'
            if money
            else str(member.meal_balance) + ' meals'
        )
        member_message = f'' f'{member.name}' f', balance :' f' {balance}'
        buttons.append(
            [InlineKeyboardButton(member_message, callback_data=str(i + j))]
        )
    buttons.append(
        [
            InlineKeyboardButton(
                emojize(':reverse_button:'), callback_data='backward_page'
            ),
            InlineKeyboardButton(emojize('Back'), callback_data='back'),
            InlineKeyboardButton(
                emojize(':play_button:'), callback_data='forward_page'
            ),
        ]
    )
    if confirm:
        buttons.append(
            [InlineKeyboardButton('Confirm', callback_data='confirm')]
        )
    return InlineKeyboardMarkup(buttons)
