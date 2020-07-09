from telegram.ext import CommandHandler, ConversationHandler

from .first_message import first_message_alternative

start_handler = ConversationHandler(
    entry_points=[CommandHandler('start', first_message_alternative)],
    states={},
    fallbacks=[CommandHandler('start', first_message_alternative)],  # Only for
    # developpment to know sticker id
)
