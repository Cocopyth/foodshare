from telegram import InlineKeyboardButton as IKB
from telegram import InlineKeyboardMarkup
from telegram.ext import ConversationHandler

from foodshare.bdd.database_communication import (
    add_token,
    get_user_from_chat_id,
    remove_user_from_community,
)
from foodshare.handlers.start_conversation.first_message import first_message

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
    ud = context.user_data
    if 'last_message' in ud:
        last_message = ud['last_message']
        bot.edit_message_text(
            message_id=last_message.message_id,
            chat_id=chat_id,
            text=message,
            reply_markup=keyboard,
        )
    else:
        ud['last_message'] = bot.send_message(
            chat_id=chat_id, text=message, reply_markup=keyboard
        )
    return ConversationStage.ACTION


def send_token(update, context):
    bot = context.bot
    chat_id = update.effective_chat.id
    ud = context.user_data
    last_message = ud['last_message']
    user = get_user_from_chat_id(chat_id)
    community = user.community
    token = add_token(community)
    message = (
        f'Here is your token to invite one person, it will only work '
        f'once : {token}'
    )
    bot.edit_message_text(
        message_id=last_message.message_id, chat_id=chat_id, text=message
    )
    ud.clear()
    first_message(update, context)
    return ConversationHandler.END


def quit(update, context):
    chat_id = update.effective_chat.id
    bot = context.bot
    user = get_user_from_chat_id(chat_id)
    members = user.community.members
    ud = context.user_data
    last_message = ud['last_message']
    # admins = [member for member in user.community.members if member.admin]
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
        bot.edit_message_text(
            message_id=last_message.message_id,
            chat_id=chat_id,
            text=message,
            reply_markup=keyboard,
        )
        return ConversationStage.QUITTING
    # elif len(admins) < 2 and user.admin:
    #     bot.edit_message_text(message_id=last_message.message_id,
    #         chat_id=chat_id, text='To quit this community you need to name '
    #                               'another administrator'
    #     )  # propose
    #     # to name another admin
    #     return ConversationHandler.END
    elif user.money_balance < 0:
        bot.edit_message_text(
            message_id=last_message.message_id,
            chat_id=chat_id,
            text='To quit the community you need to '
            'have a balance superior to zero.'
            '\n Ask another user to make a '
            'transaction to you using /transaction',
        )
        # U
        # need
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
        bot.edit_message_text(
            message_id=last_message.message_id,
            chat_id=chat_id,
            text=message,
            reply_markup=keyboard,
        )
        return ConversationStage.QUITTING


def quit_end(update, context):
    chat_id = update.effective_chat.id
    ud = context.user_data
    last_message = ud['last_message']
    remove_user_from_community(chat_id)
    context.bot.delete_message(
        message_id=last_message.message_id, chat_id=chat_id,
    )
    first_message(update, context)
    return ConversationHandler.END
