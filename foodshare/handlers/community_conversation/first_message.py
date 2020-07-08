from telegram import InlineKeyboardButton as IKB
from telegram import InlineKeyboardMarkup
from telegram.ext import ConversationHandler

from foodshare.bdd.database_communication import get_user_from_chat_id

from .community_action import community_action


def first_message(update, context):
    chat_id = update.effective_chat.id
    user = get_user_from_chat_id(chat_id)
    if user is None:
        message = (
            "Hello there! First time we meet isn't it? "
            "I just need a few information about you!"
        )
        keyboard = InlineKeyboardMarkup(
            [[IKB('Register', callback_data='register_asked0523')]]
        )
        bot = context.bot
        chat_id = update.effective_chat.id
        bot.send_message(chat_id=chat_id, text=message, reply_markup=keyboard)
        return ConversationHandler.END
    elif user.community is None:
        message = (
            "Hello there! You first need to join a community "
            "I just need a few information about you!"
        )
        keyboard = InlineKeyboardMarkup(
            [
                [
                    IKB(
                        'Join or create a community',
                        callback_data='joining_asked0523',
                    )
                ]
            ]
        )
        bot = context.bot
        chat_id = update.effective_chat.id
        bot.send_message(chat_id=chat_id, text=message, reply_markup=keyboard)
        return ConversationHandler.END
    else:
        print(
            f'user is in community {user.community} that has these other '
            f'members: {user.community.members}'
        )
        return community_action(update, context)
