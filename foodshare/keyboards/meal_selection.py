from emoji import emojize
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from foodshare.bdd.database_communication import get_user_from_chat_id
from foodshare.handlers.meals_conversation import get_all_meals
from foodshare.utils import create_meal_message

basic_buttons = []

basic_buttons.append(
    [
        InlineKeyboardButton(
            emojize(':reverse_button:'), callback_data='backward_page'
        ),
        InlineKeyboardButton(
            emojize(':play_button:'), callback_data='forward_page'
        ),
    ]
)
basic_buttons.append([InlineKeyboardButton('Back', callback_data='back')])
cancel_meal_buttons = basic_buttons.copy()
cancel_meal_buttons.append(
    [InlineKeyboardButton('Cancel meal', callback_data='cancel_meal')]
)
cancel_meal_keyboard = InlineKeyboardMarkup(cancel_meal_buttons)
cancel_participation_buttons = basic_buttons.copy()
cancel_participation_buttons.append(
    [
        InlineKeyboardButton(
            'Cancel participation', callback_data='cancel_participation'
        )
    ]
)
cancel_participation_keyboard = InlineKeyboardMarkup(
    cancel_participation_buttons
)


def process_meal_selection(update, context):
    ud = context.user_data
    callback_data = update.callback_query.data
    chat_id = update.effective_chat.id
    user = get_user_from_chat_id(chat_id)
    all_meals, meals_as_cook = get_all_meals(user)
    if '_page' not in ud:
        page = 0
        ud['_page'] = 0
    else:
        page = ud.get('_page')

    if callback_data == 'forward_page':
        page += 1
        ud['_page'] = page
    elif callback_data == 'backward_page':
        page -= 1
        ud['_page'] = page
    elif callback_data == 'back':
        ud.pop('_page')
        return False, True, -1, -1
    elif callback_data == 'cancel_meal':
        meal = all_meals[page % len(all_meals)]
        ud.pop('_page')
        return True, False, meal, True
    else:
        meal = all_meals[page % len(all_meals)]
        return True, False, meal, False
    meal = all_meals[page % len(all_meals)]
    print(all_meals)
    print(page)
    print(page)
    print(meal)
    # print(page)
    keyboard = (
        cancel_meal_keyboard
        if meal in meals_as_cook
        else cancel_participation_keyboard
    )
    message = create_meal_message(meal)
    update.callback_query.edit_message_text(
        text=message, reply_markup=keyboard,
    )
    return False, False, -1, -1
