from telegram.ext import CallbackQueryHandler

from foodshare.bdd.database_communication import update_meal


def invitation_answer(update, context):
    message_id = update.callback_query.message.message_id
    query_data = update.callback_query.data
    document_id = update_meal(message_id, query_data)
    chat_id = update.effective_chat.id
    if 'last_message' in context.user_data:
        context.user_data.pop('last_message')
    context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    context.bot.delete_message(chat_id=chat_id, message_id=document_id)


invitation_handler = CallbackQueryHandler(
    invitation_answer, pattern='secret_key_yes|secret_key_no'
)
