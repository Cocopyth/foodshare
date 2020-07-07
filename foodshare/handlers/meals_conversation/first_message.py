from emoji import emojize
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import ConversationHandler
from foodshare.bdd.database_communication import get_user_from_chat_id
from foodshare.utils import datetime_format
from datetime import datetime
from foodshare.utils import create_meal_message
from foodshare.keyboards.meal_selection import cancel_meal_keyboard,\
    cancel_participation_keyboard, process_meal_selection
from . import ConversationStage


def ask_to_chose_action(update, context):
    chat_id = update.effective_chat.id
    user = get_user_from_chat_id(chat_id)
    meals_as_cook = [meal_job.meal for meal_job in user.message_giver
                     if not meal_job.job_done]
    meals_as_participant = [meal_job.meal for meal_job in user.message_giver
                            if (meal_job.answer and not meal_job.job_done)]
    # initialize some variables in `context.user_data` when the keyboard is
    # first called
    all_meals = meals_as_cook + meals_as_participant
    all_meals.sort(key=lambda meal: datetime.strptime(meal.when,
                                                      datetime_format))
    print(len(all_meals))
    bot = context.bot
    if len(all_meals)>0:
        meal = all_meals[0]
        keyboard = cancel_meal_keyboard if meal in meals_as_cook \
            else cancel_participation_keyboard
        message = create_meal_message(meal)
        bot.send_message(chat_id=chat_id, text=message,
                         reply_markup=keyboard)
        return ConversationStage.CHOSING_MEAL
    else:
        bot.send_message(chat_id=chat_id,
                         text='No meals where you cook ' \
                                                'or you participate')
        return ConversationHandler.END

def action_chosing_handler(update,context):
    (
        action_is_selected,
        want_back,
        meal,
        cancel_meal,
    ) = process_meal_selection(update, context)
    if want_back:
        return ConversationHandler.END
    elif not action_is_selected:
        return ConversationStage.CHOSING_MEAL
    elif cancel_meal:
        return ConversationHandler.END
    return ConversationHandler.END