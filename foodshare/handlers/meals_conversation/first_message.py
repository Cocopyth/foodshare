from datetime import datetime

from telegram import InlineKeyboardButton as IKB
from telegram import InlineKeyboardMarkup
from telegram.ext import ConversationHandler

from foodshare.bdd.database_communication import (
    get_user_from_chat_id,
    process_meal_action,
)
from foodshare.handlers.start_conversation.first_message import first_message
from foodshare.keyboards.meal_selection import (
    cancel_meal_keyboard,
    cancel_participation_keyboard,
    process_meal_selection,
)
from foodshare.utils import create_meal_message, datetime_format

from . import ConversationStage


def ask_to_chose_action(update, context):
    chat_id = update.effective_chat.id
    user = get_user_from_chat_id(chat_id)
    ud = context.user_data
    meals_as_cook = [
        meal_job.meal
        for meal_job in user.message_giver
        if not meal_job.job_done
    ]
    meals_as_participant = [
        meal_job.meal
        for meal_job in user.message_receiver
        if (meal_job.answer and not meal_job.job_done)
    ]
    # initialize some variables in `context.user_data` when the keyboard is
    # first called
    all_meals = meals_as_cook + meals_as_participant
    all_meals.sort(
        key=lambda meal: datetime.strptime(meal.when, datetime_format)
    )
    bot = context.bot
    if len(all_meals) > 0:
        meal = all_meals[0]
        keyboard = (
            cancel_meal_keyboard
            if meal in meals_as_cook
            else cancel_participation_keyboard
        )
        message = create_meal_message(meal)
        if 'last_message' not in ud:
            last_message = bot.send_message(
                chat_id=chat_id, text=message, reply_markup=keyboard
            )
            ud['last_message'] = last_message
        else:
            last_message = ud['last_message']
            bot.edit_message_text(
                message_id=last_message.message_id,
                chat_id=chat_id,
                text=message,
                reply_markup=keyboard,
            )
        return ConversationStage.CHOSING_MEAL
    else:
        first_message(
            update,
            context,
            prefix='*No meals where you cook ' 'or ' 'you participate* \n',
        )
        return ConversationHandler.END


def action_chosing_handler(update, context):
    (
        action_is_selected,
        want_back,
        meal,
        cancel_meal,
    ) = process_meal_selection(update, context)
    ud = context.user_data
    ud['meal_being_processed'] = meal
    ud['cancel_meal'] = cancel_meal
    if want_back:
        first_message(update, context)
        return ConversationHandler.END
    elif not action_is_selected:
        return ConversationStage.CHOSING_MEAL
    return cancelling(update, context)


def cancelling(update, context):
    meal = context.user_data['meal_being_processed']
    cancel_meal = context.user_data['cancel_meal']
    too_late = (
        not cancel_meal
        and datetime.strptime(meal.deadline, datetime_format) <= datetime.now()
    )
    context.user_data['too_late'] = too_late
    if too_late:
        message = (
            'The deadline for confirming participation has passed, '
            'are you sure you want to cancel? I will send '
            'a message to the cook and you won\'t be charged for '
            'the meal but you won\'t be '
            'given your meal points back'
        )
    else:
        optional = 'your participation at '
        nothing = ''
        message = (
            f'*Are you sure you want to cancel '
            f'{optional if not cancel_meal else nothing} '
            f'this meal?* \n'
        )
        message += create_meal_message(meal)
    keyboard = InlineKeyboardMarkup(
        [
            [IKB('Confirm', callback_data='confirm')],
            [IKB('Back', callback_data='back')],
        ]
    )
    update.callback_query.edit_message_text(
        text=message, reply_markup=keyboard,
    )
    return ConversationStage.CANCELING


def meal_action_end(update, context):
    chat_id = update.effective_chat.id
    ud = context.user_data
    meal = ud['meal_being_processed']
    cancel_meal = ud['cancel_meal']
    too_late = ud['too_late']
    optional = 'your participation at '
    nothing = ''
    prefix = (
        f'*{optional if not cancel_meal else nothing} '
        f'The meal {meal.what} on {meal.when} has been cancelled* \n'
    )
    process_meal_action(chat_id, cancel_meal, meal, too_late)
    first_message(update, context, prefix=prefix)
    return ConversationHandler.END
