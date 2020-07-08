from telegram.ext import CommandHandler, ConversationHandler

from .first_message import first_message

start_handler = ConversationHandler(
    entry_points=[CommandHandler('start', first_message)],
    states={},
    fallbacks=[CommandHandler('start', first_message)],  # Only for
    # developpment to know sticker id
)
