from telegram import ParseMode

from foodshare.handlers.cook_conversation import ConversationStage, get_message
from foodshare.keyboards.confirmation_keyboard import confirmation_keyboard

def ask_for_conclusion(update, context):
    epilog = 'Now I will send a message to people if you want'\
             + ' to add a text message just send it to me. '\
             + 'Press confirm when you\'re ready!'
    update.callback_query.edit_message_text(
        text=get_message(context, epilog=epilog, highlight='deadline'),
        reply_markup=confirmation_keyboard,
        parse_mode=ParseMode.MARKDOWN,
    )

    return ConversationStage.CONFIRMATION
