from telegram import ParseMode

from foodshare.handlers.cook_conversation import ConversationStage, get_message
from foodshare.keyboards import reminder_keyboard


def ask_for_reminder(update, context):
    epilog = 'How much time in advance do you want to kno who\'s coming?'

    update.callback_query.edit_message_text(
        text=get_message(context, epilog=epilog, highlight='cost'),
        # reply_markup=,
        parse_mode=ParseMode.MARKDOWN,
    )

    return ConversationStage.SELECTING_REMINDER
