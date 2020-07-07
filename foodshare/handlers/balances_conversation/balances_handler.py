from telegram.ext import CallbackQueryHandler as CQH
from telegram.ext import CommandHandler, ConversationHandler



from . import ConversationStage as CS
from .first_message import (
    amount_selection_handler,
    ask_for_amount,
    ask_for_user,
    first_message,
    transaction_end,
    user_selection_handler,
)

balances_handler = ConversationHandler(
    entry_points=[CommandHandler('balances', first_message)],
    states={
        CS.MONEY_OR_MEAL: [CQH(ask_for_user, pattern='money|meal')],
        CS.SELECTING_USER: [CQH(user_selection_handler)],
        CS.SELECTING_AMOUNT: [CQH(amount_selection_handler)],
        CS.CONFIRMING: [
            CQH(ask_for_amount, pattern='back'),
            CQH(transaction_end, pattern='confirm'),
        ],
    },
    fallbacks=[CommandHandler('community', first_message)],  # Only for
    # developpment to know sticker id
)
