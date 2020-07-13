from emoji import emojize
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
from foodshare.handlers.meals_conversation import get_all_meals

def community_action(update, context):
    chat_id = update.effective_chat.id
    user = get_user_from_chat_id(chat_id)
    community = user.community
    message = emojize(
        f'You\'re in the community \n :family: {community.name} \n '
        f':desert_island: whose '
        f'description '
        f'is :  {community.description} \n What do you want to do?'
    )
    buttons = [
        [IKB('Quit community', callback_data='quit')],
    ]
    if user.admin:
        buttons.append([IKB('Invite people', callback_data='invite')])
    buttons.append([IKB('Back', callback_data='back')])
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


def back_end(update, context):
    first_message(update, context)
    return ConversationHandler.END


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
    all_meals = get_all_meals(user)
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
        prefix = (
            '*To quit the community you need to '
            'have a money balance superior to zero.'
            '\nAsk another user to make a '
            'transaction* \n'
        )
        first_message(update, context, prefix)
        return ConversationHandler.END
    elif len(all_meals) ==0:
        prefix = (
            '*To quit the community you need to have no meal ongoing '
            'please cancel your participation and the ones you organize '
            'before leaving.'
        )
        first_message(update, context, prefix)
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
