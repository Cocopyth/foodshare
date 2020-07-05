from telegram import InlineKeyboardButton as IKB
from telegram import InlineKeyboardMarkup

from foodshare.bdd.database_communication import add_community, get_token, \
    add_user_to_community

from . import ConversationStage, get_message

back_keyboard = InlineKeyboardMarkup([[IKB('Back', callback_data='back')]])


def creating_joining(update, context):
    message = "Do you want to join an existing community or create your own?"
    keyboard = InlineKeyboardMarkup(
        [
            [IKB('Join existing community', callback_data='join')],
            [IKB('Create my own', callback_data='create')],
            [IKB('Back', callback_data='back')],
        ]
    )
    bot = context.bot
    chat_id = update.effective_chat.id
    bot.send_message(chat_id=chat_id, text=message, reply_markup=keyboard)
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
    message = get_message(
        context, epilog='Give a short description of the ' 'community'
    )
    bot.send_message(chat_id=chat_id, text=message, reply_markup=back_keyboard)
    return ConversationStage.DESCRIBING


def save_community_description(update, context):
    description = update.message.text
    ud = context.user_data
    ud['community_description'] = description
    bot = context.bot
    chat_id = update.effective_chat.id
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
    bot.send_message(chat_id=chat_id, text=message, reply_markup=keyboard)
    return ConversationStage.CONFIRMING


def creating_end(update, context):
    from .first_message import first_message  # to avoid circular dependency

    ud = context.user_data
    name = ud['community_name']
    description = ud['community_description']
    chat_id = update.effective_chat.id
    add_community(name, description, chat_id)
    ud.clear()
    return first_message(update, context)


def joining(update, context):
    message = "Ask someone who administrate a community to share a token " \
              "with you and type it as an answer to this message!"
    update.callback_query.edit_message_text(
        text=message, reply_markup=back_keyboard,
    )
    return ConversationStage.JOINING

def verify_token(update,context):
    token_str = update.message.text
    token = get_token(token_str)
    bot = context.bot
    chat_id = update.effective_chat.id
    if token is None:
        message = "The token was not right! Try again!"
        bot.send_message(
            chat_id = chat_id, text=message, reply_markup=back_keyboard,
        )
        return ConversationStage.JOINING
    else:
        community = token.community
        message = f'You\'re about to join the community {community.name} ' \
                  f'whose description is: \n {community.description}. ' \
                  f'Do you confirm?'
        keyboard = InlineKeyboardMarkup(
            [
                [IKB('Confirm', callback_data='confirm')],
                [IKB('Back', callback_data='back')],
            ]
        )
        bot.send_message(
            chat_id = chat_id, text=message, reply_markup=keyboard,
        )
        context.user_data['token'] = token
        return ConversationStage.VERIFYING

def joining_end(update, context):
    from .first_message import first_message  # to avoid circular dependency
    ud = context.user_data
    token = ud['token']
    chat_id = update.effective_chat.id
    add_user_to_community(chat_id, token)
    ud.clear()
    return first_message(update, context)