from telegram.ext import CommandHandler, ConversationHandler

from .first_message import first_message

help_handler = ConversationHandler(
    entry_points=[CommandHandler('help', first_message)],
    states={},
    fallbacks=[],
)
