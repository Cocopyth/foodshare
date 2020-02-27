from telegram import ChatAction
from telegram.ext import ConversationHandler

from foodshare.commands.gif_test import get_gif_url

from . import ConversationStage


def ask_for_meal_name(update, _):
    update.message.reply_text(
        'Tell me what you want to cook! (just type the name of the meal as '
        'an answer to this message)'
    )

    return ConversationStage.TYPING_MEAL_NAME


def save_meal_name(update, context):
    ud = context.user_data
    bot = context.bot
    chat_id = update.message.chat_id

    ud['meal_name'] = update.message.text

    bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    bot.deleteMessage(chat_id=chat_id, message_id=update.message.message_id)

    gif_url = get_gif_url(ud['meal_name'])
    if gif_url is not None:
        bot.send_document(chat_id=chat_id, document=gif_url)
    else:
        update.message.reply_text(f'No gif found for {ud["meal_name"]}')

    return ConversationHandler.END
