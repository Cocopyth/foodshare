from telegram import ParseMode

from . import ConversationStage, get_message
from foodshare.keyboards.telegram_hour import hour_keyboard

def ask_for_time(update, context):
    update.callback_query.edit_message_text(
        text=get_message(context, epilog='At what time?', highlight='date'),
        reply_markup=hour_keyboard,
        parse_mode=ParseMode.MARKDOWN,
    )

    return ConversationStage.SELECTING_HOUR
