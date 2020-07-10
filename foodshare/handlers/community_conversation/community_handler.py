from telegram.ext import CallbackQueryHandler as CQH
from telegram.ext import CommandHandler, ConversationHandler

from foodshare.utils import hard_break, hard_restart

from . import ConversationStage as CS
from .community_action import (
    back_end,
    community_action,
    quit,
    quit_end,
    send_token,
)

community_handler = ConversationHandler(
    entry_points=[
        CommandHandler('community', community_action),
        CQH(community_action, pattern='community_asked0523'),
        CQH(community_action, pattern='invite_asked0523'),
    ],
    states={
        CS.ACTION: [
            CQH(send_token, pattern='invite'),
            CQH(quit, pattern='quit'),
            CQH(back_end, pattern='back'),
        ],
        CS.QUITTING: [
            CQH(community_action, pattern='back'),
            CQH(quit_end, pattern='confirm'),
        ],
    },
    fallbacks=[
        CommandHandler('stop', hard_break),
        CommandHandler('start', hard_restart),
    ],
    # developpment to know sticker id
)
