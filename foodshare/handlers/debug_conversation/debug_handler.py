from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    Filters,
    MessageHandler,
)

from . import ConversationStage as CS
from .debuging import debug_fun, return_sticker

debug_handler = ConversationHandler(
    entry_points=[CommandHandler('debug', debug_fun)],
    states={CS.DEBUG_STAGE_1: [MessageHandler(Filters.text, debug_fun)]},
    fallbacks=[MessageHandler(Filters.sticker, return_sticker)],  # Only for
    # developpment to know sticker id
)
