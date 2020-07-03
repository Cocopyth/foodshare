from telegram.ext import CallbackQueryHandler as CQH
from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    Filters,
    MessageHandler,
)
from foodshare.handlers.community_conversation.first_message import \
    ConversationStage as CScom

from . import ConversationStage as CS
from .register_name import ask_for_name, save_name, end

registering_handler = ConversationHandler(
    entry_points=[CQH(ask_for_name,
                      pattern='register_asked0523')],
    states={
        CS.TYPING_NAME: [MessageHandler(Filters.text, save_name)],
        CS.NAME_SAVED: [CQH(end, pattern='confirm'),
            CQH(ask_for_name, pattern='back')]
    },
    fallbacks=[
        CommandHandler('cook', ask_for_name),
    ],  # Only for
    map_to_parent={
            ConversationHandler.END: CScom.REGISTERED,
        }
    # developpment to know sticker id
)