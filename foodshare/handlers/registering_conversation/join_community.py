from telegram import InlineKeyboardButton as IKB
from telegram import InlineKeyboardMarkup
from telegram.ext import ConversationHandler

from foodshare.bdd.database_communication import (
    add_community,
    add_user,
    add_user_to_community,
    get_token,
)
from foodshare.handlers.community_conversation import get_message
from foodshare.handlers.start_conversation.first_message import first_message

from . import ConversationStage

back_keyboard = InlineKeyboardMarkup([[IKB('Back', callback_data='back')]])


def creating_joining(update, context):
    ud = context.user_data
    chat_id = update.effective_chat.id
    if 'name_user' in ud.keys():
        add_user(ud['name_user'], chat_id)
    message = "Do you want to join an existing community or create your own?"
    keyboard = InlineKeyboardMarkup(
        [
            [IKB('Join existing community', callback_data='join')],
            [IKB('Create my own', callback_data='create')],
        ]
    )
    bot = context.bot
    if 'last_message' not in ud:
        last_message = bot.send_message(
            chat_id=chat_id, text=message, reply_markup=keyboard
        )
        ud['last_message'] = last_message
    else:
        last_message = ud['last_message']
        bot.edit_message_text(
            message_id=last_message.message_id,
            chat_id=chat_id,
            text=message,
            reply_markup=keyboard,
        )
    return ConversationStage.CREATING_JOINING


def creating(update, context):
    message = "Type a name for your community!"
    update.callback_query.edit_message_text(
        text=message, reply_markup=back_keyboard,
    )
    return ConversationStage.CREATING


def save_community_name(update, context):
    name = update.message.text
    ud = context.user_data
    ud['community_name'] = name
    bot = context.bot
    chat_id = update.effective_chat.id
    bot.delete_message(message_id=update.message.message_id, chat_id=chat_id)
    last_message = ud['last_message']
    message = get_message(
        context, epilog='Give a short description of the ' 'community'
    )
    bot.edit_message_text(
        message_id=last_message.message_id,
        chat_id=chat_id,
        text=message,
        reply_markup=back_keyboard,
    )
    return ConversationStage.DESCRIBING


def save_community_description(update, context):
    description = update.message.text
    ud = context.user_data
    ud['community_description'] = description
    last_message = ud['last_message']
    bot = context.bot
    chat_id = update.effective_chat.id
    bot.delete_message(message_id=update.message.message_id, chat_id=chat_id)
    message = get_message(
        context,
        epilog='If you\'re satisfied with this '
        'community description you can '
        'confirm',
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
    return ConversationStage.CONFIRMING


def creating_end(update, context):
    from foodshare.handlers.start_conversation.first_message import (
        first_message,
    )  # to

    # avoid circular
    # dependency

    ud = context.user_data
    chat_id = update.effective_chat.id
    name = ud['community_name']
    description = ud['community_description']
    last_message = ud['last_message']
    bot = context.bot
    bot.delete_message(message_id=last_message.message_id, chat_id=chat_id)
    chat_id = update.effective_chat.id
    add_community(name, description, chat_id)
    ud.clear()
    first_message(update, context)
    return ConversationHandler.END


def joining(update, context):
    message = (
        "Ask someone who administrate a community to share a token "
        "with you and type it as an answer to this message!"
    )
    update.callback_query.edit_message_text(
        text=message, reply_markup=back_keyboard,
    )
    return ConversationStage.JOINING


def verify_token(update, context):
    token_str = update.message.text
    token = get_token(token_str)
    last_message = context.user_data['last_message']
    bot = context.bot
    chat_id = update.effective_chat.id
    bot.delete_message(message_id=update.message.message_id, chat_id=chat_id)
    if token is None:
        message = "The token was not right! Try again!"
        bot.edit_message_text(
            message_id=last_message.message_id,
            chat_id=chat_id,
            text=message,
            reply_markup=back_keyboard,
        )
        return ConversationStage.JOINING
    else:
        community = token.community
        message = (
            f'You\'re about to join the community {community.name} '
            f'whose description is: \n {community.description}. '
            f'Do you confirm?'
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
        context.user_data['token'] = token
        return ConversationStage.VERIFYING


def joining_end(update, context):
    ud = context.user_data
    token = ud['token']
    last_message = ud['last_message']
    chat_id = update.effective_chat.id
    add_user_to_community(chat_id, token)
    ud.clear()
    context.bot.delete_message(
        message_id=last_message.message_id, chat_id=chat_id,
    )
    first_message(update, context)
    return ConversationHandler.END
