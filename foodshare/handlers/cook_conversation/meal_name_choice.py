from telegram import ChatAction

from . import ConversationStage
from .conclusion_selection import ask_for_conclusion
from .date_selection import ask_for_date


def ask_for_meal_name(update, context):
    ud = context.user_data
    bot = context.bot
    chat_id = update.effective_chat.id
    message = (
        'Tell me what you want to cook! '
        '(just type the name of the meal as an answer to this message)'
    )
    if 'last_message' in ud:
        last_message = ud['last_message']
        bot.edit_message_text(
            message_id=last_message.message_id, chat_id=chat_id, text=message,
        )
    else:
        ud['last_message'] = bot.send_message(chat_id=chat_id, text=message)
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
    return ask_for_date(update, context)
