from telegram import InlineKeyboardButton as IKB
from telegram import InlineKeyboardMarkup

from . import ConversationStage


def ask_for_name(update, context):
    ud = context.user_data
    message = (
        'What\'s your name? '
        '(just type your name as an answer to this message)'
    )
    bot = context.bot
    chat_id = update.effective_chat.id
    last_message = ud['last_message']

    bot.edit_message_text(
        message_id=last_message.message_id, chat_id=chat_id, text=message
    )
    return ConversationStage.TYPING_NAME


def save_name(update, context):
    ud = context.user_data
    bot = context.bot
    chat_id = update.effective_chat.id
    name = update.message.text
    last_message = ud['last_message']
    bot.delete_message(message_id=update.message.message_id, chat_id=chat_id)
    ud['name_user'] = name
    message = f'Are you satisfied with the name \'{name}\'?'
    keyboard = InlineKeyboardMarkup(
        [
            [IKB('Confirm', callback_data='confirm')],
            [IKB('Change name', callback_data='back')],
        ]
    )
    bot.edit_message_text(
        message_id=last_message.message_id,
        chat_id=chat_id,
        text=message,
        reply_markup=keyboard,
    )
    return ConversationStage.NAME_SAVED
