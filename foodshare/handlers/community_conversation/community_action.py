

from telegram import InlineKeyboardButton as IKB
from telegram import InlineKeyboardMarkup
from telegram.ext import ConversationHandler

from foodshare.bdd.database_communication import (
    add_token,
    get_user_from_chat_id,
)

from . import ConversationStage


def community_action(update, context):
    chat_id = update.effective_chat.id
    user = get_user_from_chat_id(chat_id)
    community = user.community
    message = (
        f'You\'re in the community {community.name} whose description '
        f'is : \n {community.description} \n What do you want to do?'
    )
    buttons = [
        [IKB('Quit community', callback_data='quit')],
    ]
    if user.admin:
        buttons.append([IKB('Invite people', callback_data='invite')])
    keyboard = InlineKeyboardMarkup(buttons)
    bot = context.bot
    bot.send_message(chat_id=chat_id, text=message, reply_markup=keyboard)
    return ConversationStage.ACTION


def send_token(update, context):
    bot = context.bot
    chat_id = update.effective_chat.id
    user = get_user_from_chat_id(chat_id)
    community = user.community
    token = add_token(community)
    message = (
        f'Here is your token to invite one person, it will only work '
        f'once : {token}'
    )

    bot.send_message(chat_id=chat_id, text=message)
    return ConversationHandler.END


def quit(update, context):
    return None
