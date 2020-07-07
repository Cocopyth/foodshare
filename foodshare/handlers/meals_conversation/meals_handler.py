from telegram.ext import CallbackQueryHandler as CQH
from telegram.ext import CommandHandler, ConversationHandler
from .first_message import ask_to_chose_action, action_chosing_handler


from . import ConversationStage as CS

meals_handler = ConversationHandler(
    entry_points=[CommandHandler('meals', ask_to_chose_action)],
    states={
        CS.CHOSING_MEAL: [CQH(action_chosing_handler)],
    },
    fallbacks=[CommandHandler('meals', ask_to_chose_action)],
)