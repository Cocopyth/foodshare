from telegram import InlineKeyboardButton as IKB
from telegram import InlineKeyboardMarkup
from telegram.ext import ConversationHandler

from foodshare.bdd.database_communication import add_user

from . import ConversationStage


def ask_for_name(update, context):
    message = (
        'What\'s your name? '
        '(just type the name of the meal as an answer to this message)'
    )
    bot = context.bot
    chat_id = update.effective_chat.id
    bot.send_message(
        chat_id=chat_id, text=message,
    )
    return ConversationStage.TYPING_NAME


def save_name(update, context):
    ud = context.user_data
    bot = context.bot
    chat_id = update.effective_chat.id
    name = update.message.text
    ud['name_user'] = name
    message = f'Are you satisfied with the name \'{name}\'?'
    keyboard = InlineKeyboardMarkup(
        [
            [IKB('Confirm', callback_data='confirm')],
            [IKB('Change name', callback_data='back')],
        ]
    )
    bot.send_message(chat_id=chat_id, text=message, reply_markup=keyboard)
    return ConversationStage.NAME_SAVED


def end(update, context):
    ud = context.user_data
    name = ud['name_user']
    chat_id = update.effective_chat.id
    add_user(name, chat_id)
    ud.clear()
    bot = context.bot
    message = f'Okay now let\'s get in a community'
    keyboard = InlineKeyboardMarkup(
        [[IKB('Let\'s go!', callback_data='start_community')]]
    )
    bot.send_message(chat_id=chat_id, text=message, reply_markup=keyboard)
    return ConversationHandler.END
