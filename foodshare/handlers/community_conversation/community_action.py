from telegram import InlineKeyboardButton as IKB
from telegram import InlineKeyboardMarkup
from telegram.ext import ConversationHandler

from foodshare.bdd.database_communication import (
    add_token,
    get_user_from_chat_id,
    remove_user_from_community,
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
    chat_id = update.effective_chat.id
    bot = context.bot
    user = get_user_from_chat_id(chat_id)
    members = user.community.members
    admins = [member for member in user.community.members if member.admin]
    if len(members) < 2:
        message = (
            f'Are you sure you want to quit the community? Since you\'re '
            f'the last member this will delete it'
        )
        keyboard = InlineKeyboardMarkup(
            [
                [IKB('Confirm', callback_data='confirm')],
                [IKB('Back', callback_data='back')],
            ]
        )
        bot.send_message(chat_id=chat_id, text=message, reply_markup=keyboard)
        return ConversationStage.QUITTING
    elif len(admins) < 2 and user.admin:
        bot.send_message(
            chat_id=chat_id, text='u need another admin'
        )  # propose
        # to name another admin
        return ConversationHandler.END
    elif user.money_balance < 0:
        bot.send_message(chat_id=chat_id, text='u need balance>0')  # U need
        # balance >0 : show balances to reimburse someone
        return ConversationHandler.END
    else:
        message = f'Are you sure you want to quit the community?'
        keyboard = InlineKeyboardMarkup(
            [
                [IKB('Confirm', callback_data='confirm')],
                [IKB('Back', callback_data='back')],
            ]
        )
        bot.send_message(chat_id=chat_id, text=message, reply_markup=keyboard)
        return ConversationStage.QUITTING


def quit_end(update, context):
    from .first_message import first_message  # to avoid circular dependency

    chat_id = update.effective_chat.id
    remove_user_from_community(chat_id)
    return first_message(update, context)
