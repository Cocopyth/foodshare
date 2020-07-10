from telegram.ext import CallbackQueryHandler as CQH
from telegram.ext import ConversationHandler, Filters, MessageHandler

from foodshare.handlers.registering_conversation.join_community import (
    ask_community_description,
    creating,
    creating_end,
    creating_joining,
    joining,
    joining_end,
    save_community_description,
    save_community_name,
    verify_token,
)

from . import ConversationStage as CS
from .register_name import ask_for_name, save_name

registering_handler = ConversationHandler(
    entry_points=[
        CQH(ask_for_name, pattern='register_asked0523'),
        CQH(creating_joining, pattern='joining_asked0523'),
    ],
    states={
        CS.TYPING_NAME: [MessageHandler(Filters.text, save_name)],
        CS.NAME_SAVED: [
            CQH(creating_joining, pattern='confirm'),
            CQH(ask_for_name, pattern='back'),
        ],
        CS.CREATING_JOINING: [
            CQH(creating, pattern='create'),
            CQH(joining, pattern='join'),
        ],
        CS.CREATING: [
            CQH(creating_joining, pattern='back'),
            MessageHandler(Filters.text, save_community_name),
        ],
        CS.DESCRIBING: [
            CQH(creating, pattern='back'),
            MessageHandler(Filters.text, save_community_description),
        ],
        CS.CONFIRMING: [
            CQH(ask_community_description, pattern='back'),
            CQH(creating_end, pattern='confirm'),
        ],
        CS.JOINING: [
            CQH(creating_joining, pattern='back'),
            MessageHandler(Filters.text, verify_token),
        ],
        CS.VERIFYING: [
            CQH(joining, pattern='back'),
            CQH(joining_end, pattern='confirm'),
        ],
    },
    fallbacks=[],
)
