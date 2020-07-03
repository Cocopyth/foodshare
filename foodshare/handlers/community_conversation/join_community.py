from foodshare.bdd.database_communication import get_user_from_chat_id
from . import ConversationStage, get_message
from telegram import InlineKeyboardButton as IKB
from telegram import InlineKeyboardMarkup
from foodshare.bdd.database_communication import add_community

back_keyboard = InlineKeyboardMarkup(
        [
            [
                IKB('Back',
                    callback_data='back'),
            ],
        ]
    )

def creating_joining(update, context):
    message = "Do you want to join an existing community or create your own?"
    keyboard = InlineKeyboardMarkup(
        [
            [
                IKB('Join existing community',
                    callback_data='join'),
            ],
            [
                IKB('Create my own',
                    callback_data='create'),
            ],
            [
                IKB('Back',
                    callback_data='back'),
            ],
        ]
    )
    bot = context.bot
    chat_id = update.effective_chat.id
    bot.send_message(
        chat_id=chat_id, text=message, reply_markup=keyboard
    )
    return ConversationStage.CREATING_JOINING

def creating(update,context):
    message = "Type a name for your community!"
    update.callback_query.edit_message_text(
        text=message, reply_markup=back_keyboard,
    )
    return ConversationStage.CREATING

def save_community_name(update,context):
    name = update.message.text
    ud = context.user_data
    ud['community_name'] = name
    bot = context.bot
    chat_id = update.effective_chat.id
    message= get_message(context, epilog='Give a short description of the '
                                         'community')
    bot.send_message(
        chat_id=chat_id, text=message, reply_markup=back_keyboard
    )
    return ConversationStage.DESCRIBING

def save_community_description(update,context):
    description = update.message.text
    ud = context.user_data
    ud['community_description'] = description
    bot = context.bot
    chat_id = update.effective_chat.id
    message= get_message(context, epilog='If you\'re satisfied with this '
                                         'community description you can '
                                         'confirm')
    back_keyboard = InlineKeyboardMarkup(
        [
            [
                IKB('Confirm',
                    callback_data='confirm'),
            ],
            [
                IKB('Back',
                    callback_data='back'),
            ],
        ]
    )
    bot.send_message(
        chat_id=chat_id, text=message, reply_markup=back_keyboard
    )
    return ConversationStage.CONFIRMING

def creating_end(update, context):
    from .first_message import first_message #to avoid circular dependency
    ud = context.user_data
    name = ud['community_name']
    description = ud['community_description']
    chat_id = update.effective_chat.id
    add_community(name, description, chat_id)
    ud.clear()
    return first_message(update, context)

def joining(update, context):
    pass