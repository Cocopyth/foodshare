from foodshare.bdd.database_communication import get_user_from_chat_id
from . import ConversationStage
from telegram import InlineKeyboardButton as IKB
from telegram import InlineKeyboardMarkup


def community_action(update, context):
    message = "What do you want to do from the community"
    keyboard = InlineKeyboardMarkup(
        [
            [
                IKB('Quit community',
                    callback_data='join'),
            ],
            [
                IKB('Invite people',
                    callback_data='create'),
            ],
        ]
    )
    bot = context.bot
    chat_id = update.effective_chat.id
    bot.send_message(
        chat_id=chat_id, text=message, reply_markup=keyboard
    )
    return None