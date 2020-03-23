from telegram import ParseMode

from foodshare.handlers.cook_conversation import ConversationStage, get_message
from foodshare.keyboards import telegram_hour


def ask_for_number_of_person(update, context):
    update.callback_query.edit_message_text(
        text=get_message(
            context,
            epilog='For how many people (including yourself)?',
            highlight='time',
        ),
        reply_markup=telegram_hour.hour_keyboard,
        parse_mode=ParseMode.MARKDOWN,
    )

    return ConversationStage.SELECTING_NUMBER_OF_PERSON
