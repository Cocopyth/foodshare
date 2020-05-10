from . import ConversationStage as CS
from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    Filters,
    MessageHandler,
)

from .debuging import return_sticker, debug_fun
invitation_handler = ConversationHandler(
    entry_points=[CommandHandler('debug', debug_fun)],
    states={
        CS.DEBUG_STAGE_1 : [MessageHandler(Filters.text, debug_fun)],
    },
    fallbacks=[
        MessageHandler(Filters.sticker, return_sticker),
    ],
)