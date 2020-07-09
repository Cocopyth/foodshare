from telegram.ext import CallbackQueryHandler as CQH
from telegram.ext import CommandHandler, ConversationHandler

from . import ConversationStage as CS
from .community_action import community_action, quit, quit_end, send_token

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
        ],
        CS.QUITTING: [
            CQH(community_action, pattern='back'),
            CQH(quit_end, pattern='confirm'),
        ],
    },
    fallbacks=[],  # Only for
    # developpment to know sticker id
)
