import datetime

from telegram import ParseMode

from foodshare.handlers.cook_conversation import ConversationStage, get_message
from foodshare.handlers.cook_conversation.nb_of_person_selection import (
    ask_for_number_of_person,
)
from foodshare.keyboards import telegram_hour


def ask_for_time(update, context, selected_time_in_the_past=False):
    if selected_time_in_the_past:
        epilog = (
            'The chosen time was in the past, please select a time in the '
            'future:'
        )
    else:
        epilog = 'At what time?'

    update.callback_query.edit_message_text(
        text=get_message(context, epilog=epilog, highlight='date'),
        reply_markup=telegram_hour.hour_keyboard,
        parse_mode=ParseMode.MARKDOWN,
    )

    return ConversationStage.SELECTING_HOUR


def time_selection_handler(update, context):
    from .date_selection import ask_for_date  # to avoid circular import

    time_is_selected, want_back, time = telegram_hour.process_time_selection(
        update, context
    )
    if want_back:
        return ask_for_date(update, context)
    elif not time_is_selected:
        return ConversationStage.SELECTING_HOUR

    # if the selected time is in the past
    selected_date = context.user_data['date']
    selected_datetime = datetime.datetime.combine(selected_date, time)
    if selected_datetime < datetime.datetime.now():
        return ask_for_time(update, context, selected_time_in_the_past=True)

    context.user_data['time'] = time

    return ask_for_number_of_person(update, context)
