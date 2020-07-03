from telegram.ext import CallbackQueryHandler as CQH
from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    Filters,
    MessageHandler,
)
from foodshare.handlers.registering_conversation.registering_handler import registering_handler
from . import ConversationStage as CS
from .first_message import first_message
community_handler = ConversationHandler(
    entry_points=[CommandHandler('community', first_message)],
    states={
        CS.REGISTERING : [registering_handler],
    },
    fallbacks=[
        CommandHandler('community', first_message),
    ],  # Only for
    # developpment to know sticker id
)