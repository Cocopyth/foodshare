from telegram.ext import CallbackQueryHandler

from foodshare.bdd.database_communication import update_meal


def invitation_answer(update, context):
    message_id = update.callback_query.message.message_id
    query_data = update.callback_query.data
    update_meal(message_id, query_data)
    update.callback_query.edit_message_text(
        text='Very well, type /meals to see all meals where you\'re going'
    )


invitation_handler = CallbackQueryHandler(
    invitation_answer, pattern='secret_key_yes|secret_key_no'
)
