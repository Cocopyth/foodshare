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
from.join_community import creating, joining, save_community_name,\
    creating_joining, save_community_description, creating_end
community_handler = ConversationHandler(
    entry_points=[CommandHandler('community', first_message)],
    states={
        CS.REGISTERING : [registering_handler],
        CS.REGISTERED : [CQH(first_message, pattern='start_community')],
        CS.CREATING_JOINING : [CQH(creating, pattern='create'),
                               CQH(joining, pattern='join'),
                               CQH(first_message, pattern='back')],
        CS.CREATING : [CQH(creating_joining, pattern='back'),
                       MessageHandler(Filters.text, save_community_name)],
        CS.DESCRIBING: [CQH(creating, pattern='back'),
                       MessageHandler(Filters.text,
                                      save_community_description)],
        CS.CONFIRMING: [CQH(save_community_name, pattern='back'),
                        CQH(creating_end, pattern='confirm')],
    },
    fallbacks=[
        CommandHandler('community', first_message),
    ],  # Only for
    # developpment to know sticker id
)