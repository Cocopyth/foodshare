from telegram.ext import CallbackQueryHandler as CQH
from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    Filters,
    MessageHandler,
)

from foodshare.handlers.registering_conversation.registering_handler import (
    registering_handler,
)

from . import ConversationStage as CS
from .first_message import first_message, ask_for_user,\
    user_selection_handler


balances_handler = ConversationHandler(
    entry_points=[CommandHandler('balances', first_message)],
    states={
        CS.REGISTERING: [registering_handler],
        CS.MONEY_OR_MEAL: [CQH(ask_for_user,pattern='money|meal')],
        CS.SELECTING_USER: [CQH(user_selection_handler)]
    },
    fallbacks=[CommandHandler('community', first_message)],  # Only for
    # developpment to know sticker id
)