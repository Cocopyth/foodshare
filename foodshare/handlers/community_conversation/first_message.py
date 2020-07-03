from telegram import ChatAction

from foodshare.bdd.database_communication import get_user_from_chat_id
from . import ConversationStage
from telegram import InlineKeyboardButton as IKB
from telegram import InlineKeyboardMarkup


def first_message(update, context):
    chat_id = update.message.chat_id
    user = get_user_from_chat_id(chat_id)
    message = "Hello there! First time we meet isn't it? " \
              "I just need a few information about you!"
    if user is None:
        keyboard = InlineKeyboardMarkup(
            [
                [
                    IKB('Register',
                        callback_data='register_asked0523'),
                ],
            ]
        )
        bot = context.bot
        chat_id = update.effective_chat.id
        bot.send_message(
            chat_id=chat_id, text=message, reply_markup = keyboard
        )
        return ConversationStage.REGISTERING

