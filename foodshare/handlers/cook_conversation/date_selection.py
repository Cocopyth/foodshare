import datetime

from telegram import InlineKeyboardButton as IKB
from telegram import InlineKeyboardMarkup

from foodshare.keyboards import telegram_calendar

from ... import get_weekday
from . import ConversationStage, get_message
from .reminder_selection import ask_for_reminder
from .time_selection import ask_for_time


def ask_for_date(update, context):
    chat_id = update.effective_chat.id
    bot = context.bot
    weekday_in_two_days = get_weekday(
        datetime.date.today() + datetime.timedelta(days=2)
    )
    keyboard = InlineKeyboardMarkup(
        [
            [
                IKB('Today', callback_data='today'),
                IKB('Tomorrow', callback_data='tmo'),
            ],
            [
                IKB(f'On {weekday_in_two_days}', callback_data='in_2_days'),
                IKB('Show calendar', callback_data='show_calendar'),
            ],
            [IKB('Back', callback_data='back')],
        ]
    )
    message = get_message(
        context,
        epilog='I advise you to hide your '
        'keyboard now to better '
        'see my messages! \n \n'
        'When do '
        'you '
        'want to cook?',
    )
    last_message = context.user_data['last_message']
    bot.edit_message_text(
        message_id=last_message.message_id,
        chat_id=chat_id,
        text=message,
        reply_markup=keyboard,
    )

    return ConversationStage.SELECTING_WEEKDAY_OR_SHOW_CALENDAR


def get_date_from_weekday(update, context):
    query_data = update.callback_query.data
    if query_data == 'today':
        date = datetime.date.today()
    elif query_data == 'tmo':
        date = datetime.date.today() + datetime.timedelta(days=1)
    elif query_data == 'in_2_days':
        date = datetime.date.today() + datetime.timedelta(days=2)

    context.user_data['date'] = date
    if 'confirmation_stage' in context.user_data:
        ud = context.user_data
        selected_date, time = ud['date'], ud['time']
        selected_datetime = datetime.datetime.combine(selected_date, time)
        if selected_datetime < datetime.datetime.now():
            return ask_for_time(
                update, context, selected_time_in_the_past=True
            )
        else:
            return ask_for_reminder(update, context)
    return ask_for_time(update, context)


def get_date_from_calendar(update, context, selected_date_in_the_past=False):
    if selected_date_in_the_past:
        epilog = (
            'The chosen date was in the past, please select a date in the '
            'future:'
        )
    else:
        epilog = 'Please select a date:'

    update.callback_query.edit_message_text(
        text=get_message(context, epilog=epilog),
        reply_markup=telegram_calendar.create_calendar(),
    )

    return ConversationStage.SELECTING_DATE_CALENDAR


def calendar_selection_handler(update, context):
    date_is_selected, date = telegram_calendar.process_calendar_selection(
        context.bot, update
    )

    # if no date was selected
    if not date_is_selected:
        return ConversationStage.SELECTING_DATE_CALENDAR

    # if the selected date is in the past
    if date.date() < datetime.date.today():
        return get_date_from_calendar(
            update, context, selected_date_in_the_past=True
        )

    context.user_data['date'] = date
    if 'confirmation_stage' in context.user_data:
        return ask_for_reminder(update, context)
    return ask_for_time(update, context)
