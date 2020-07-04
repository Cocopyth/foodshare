from telegram import ChatAction

from foodshare.utils.gif_test import get_gif_url

from . import ConversationStage
from .conclusion_selection import ask_for_conclusion
from .date_selection import ask_for_date


def ask_for_meal_name(update, context):
    ud = context.user_data
    if 'confirmation_stage' not in ud:
        ud.clear()
    message = (
        'Tell me what you want to cook! '
        '(just type the name of the meal as an answer to this message)'
    )
    if (
        update.message is None
    ):  # reply doesn't work if there is no message to reply to
        update.callback_query.edit_message_text(
            text=message, highlight='meal_name'
        )
    else:
        update.message.reply_text(message)
    return ConversationStage.TYPING_MEAL_NAME


def save_meal_name(update, context):
    ud = context.user_data
    bot = context.bot
    chat_id = update.message.chat_id
    ud['chat_id'] = chat_id
    ud['meal_name'] = update.message.text
    if 'confirmation_stage' in ud:
        return ask_for_conclusion(update, context, highlight='meal_name')
    bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    bot.deleteMessage(chat_id=chat_id, message_id=update.message.message_id)

    gif_url = get_gif_url(ud['meal_name'])
    if gif_url is not None:
        bot.send_document(chat_id=chat_id, document=gif_url)
    else:
        update.message.reply_text(f'No gif found for {ud["meal_name"]}')

    return ask_for_date(update, context)
