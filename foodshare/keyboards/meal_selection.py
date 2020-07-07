from emoji import emojize
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode

from foodshare.bdd.database_communication import get_user_from_chat_id
from foodshare.utils import emojize_number
from datetime import datetime
from foodshare.utils import create_meal_message, datetime_format


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
basic_buttons.append(
    [InlineKeyboardButton('Back', callback_data='back')]
)
cancel_meal_buttons = basic_buttons.copy()
cancel_meal_buttons.append(
    [InlineKeyboardButton('Cancel meal', callback_data='cancel_meal')]
)
cancel_meal_keyboard = InlineKeyboardMarkup(cancel_meal_buttons)
cancel_participation_buttons = basic_buttons.copy()
cancel_participation_buttons.append(
    [InlineKeyboardButton('Cancel participation',
                          callback_data='cancel_participation')]
)
cancel_participation_keyboard = InlineKeyboardMarkup(
    cancel_participation_buttons)

def process_meal_selection(update, context):
    ud = context.user_data
    callback_data = update.callback_query.data
    chat_id = update.effective_chat.id
    user = get_user_from_chat_id(chat_id)
    meals_as_cook = [meal_job.meal for meal_job in user.message_giver
                    if not meal_job.job_done]
    meals_as_participant = [meal_job.meal for meal_job in user.message_giver
                    if (meal_job.answer and not meal_job.job_done)]
    # initialize some variables in `context.user_data` when the keyboard is
    # first called
    all_meals = meals_as_cook+meals_as_participant
    print(len(all_meals))
    all_meals.sort(key= lambda meal: datetime.strptime(meal.when,
                                                   datetime_format))
    if '_page' not in ud:
        page = 0
        ud['_page'] = 0
    else:
        page = ud.get('_page')
    # process the keyboard callback data
    meal = all_meals[page % len(all_meals)]
    if callback_data == 'forward_page':
        page += 1
    elif callback_data == 'backward_page':
        page -= 1
    elif callback_data == 'back':
        ud.pop('_page')
        return False, True, -1, -1
    elif callback_data == 'cancel_meal':
        ud.pop('_page')
        return True, False, meal, True
    else:
        return True, False, meal, False
    keyboard = cancel_meal_keyboard if meal in meals_as_cook \
        else cancel_participation_keyboard
    message = create_meal_message(meal)
    update.callback_query.edit_message_text(
        text=message, reply_markup=keyboard,
    )
    return False, False, -1, -1

