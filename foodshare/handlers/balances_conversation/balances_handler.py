from telegram.ext import CallbackQueryHandler as CQH
from telegram.ext import CommandHandler, ConversationHandler

from foodshare.utils import hard_break, hard_restart

from . import ConversationStage as CS
from .balance_action import (
    amount_selection_handler,
    ask_for_amount,
    ask_for_user,
    ask_money_or_meal,
    transaction_end,
    user_selection_handler,
)

balances_handler = ConversationHandler(
    entry_points=[
        CQH(ask_money_or_meal, pattern='balances_asked0523'),
    ],
    states={
        CS.MONEY_OR_MEAL: [CQH(ask_for_user, pattern='money|meal|back')],
        CS.SELECTING_USER: [CQH(user_selection_handler)],
        CS.SELECTING_AMOUNT: [CQH(amount_selection_handler)],
        CS.CONFIRMING: [
            CQH(ask_for_amount, pattern='back'),
            CQH(transaction_end, pattern='confirm'),
        ],
    },
    fallbacks=[
        CommandHandler('stop', hard_break),
        CommandHandler('start', hard_restart),
    ],  # Only for
    # developpment to know sticker id
)
