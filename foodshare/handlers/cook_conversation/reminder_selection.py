from datetime import datetime, timedelta

from telegram import ParseMode

from foodshare.handlers.cook_conversation import ConversationStage, get_message
from foodshare.keyboards.reminder_keyboard import reminder_keyboard_build

from .conclusion_selection import ask_for_conclusion


def hours_until_meal(date):
    time_delta = (date - datetime.now()).total_seconds()
    return time_delta / 3600


def ask_for_reminder(update, context):
    epilog = 'How much time in advance do you want to know who\'s coming?'
    ud = context.user_data
    selected_datetime = datetime.combine(ud['date'], ud['time'])
    time_left = hours_until_meal(selected_datetime)
    update.callback_query.edit_message_text(
        text=get_message(context, epilog=epilog, highlight='cost'),
        reply_markup=reminder_keyboard_build(time_left),
        parse_mode=ParseMode.MARKDOWN,
    )

    return ConversationStage.SELECTING_REMINDER


def get_deadline(update, context):
    query_data = update.callback_query.data
    time_list = query_data.split(':')
    ud = context.user_data
    selected_datetime = datetime.combine(ud['date'], ud['time'])
    deadline = selected_datetime - timedelta(
        hours=int(time_list[0]), minutes=int(time_list[1])
    )
    ud['deadline'] = deadline
    print(deadline)
    return ask_for_conclusion(update, context)
