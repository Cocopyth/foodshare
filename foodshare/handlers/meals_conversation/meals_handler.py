from telegram.ext import CallbackQueryHandler as CQH
from telegram.ext import CommandHandler, ConversationHandler

from . import ConversationStage as CS
from .first_message import (
    action_chosing_handler,
    ask_to_chose_action,
    meal_action_end,
)

meals_handler = ConversationHandler(
    entry_points=[CommandHandler('meals', ask_to_chose_action)],
    states={
        CS.CHOSING_MEAL: [CQH(action_chosing_handler)],
        CS.CANCELING: [
            CQH(ask_to_chose_action, pattern='back'),
            CQH(meal_action_end, pattern='confirm'),
        ],
    },
    fallbacks=[CommandHandler('meals', ask_to_chose_action)],
)
