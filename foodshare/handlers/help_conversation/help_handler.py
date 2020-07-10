from telegram.ext import CommandHandler, ConversationHandler

from foodshare.utils import hard_break, hard_restart

from .first_message import first_message

help_handler = ConversationHandler(
    entry_points=[CommandHandler('help', first_message)],
    states={},
    fallbacks=[
        CommandHandler('stop', hard_break),
        CommandHandler('start', hard_restart),
    ],
)
