import datetime

from telegram import InlineKeyboardButton as IKB
from telegram import InlineKeyboardMarkup, ParseMode

from foodshare.keyboards import telegram_calendar
from foodshare.keyboards.telegram_hour import hour_keyboard

from . import ConversationStage, get_message, get_weekday


def ask_for_date(update, context):
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
            # [
            #     IKB('Change name of the meal', callback_data='back')
            # ],
        ]
    )

    update.message.reply_text(
        text=get_message(context, epilog='When do you want to cook?'),
        reply_markup=keyboard,
    )

    return ConversationStage.SELECTING_WEEKDAY_OR_SHOW_CALENDAR


def weekday_handler(update, context):
    query_data = update.callback_query.data
    if query_data == 'today':
        date = datetime.date.today()
    elif query_data == 'tmo':
        date = datetime.date.today() + datetime.timedelta(days=1)
    elif query_data == 'in_2_days':
        date = datetime.date.today() + datetime.timedelta(days=2)

    context.user_data['date'] = date

    return ask_for_hour(update, context)


def calendar_handler(update, context, selected_date_in_the_past=False):
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
        return calendar_handler(
            update, context, selected_date_in_the_past=True
        )

    context.user_data['date'] = date

    return ask_for_hour(update, context)


def ask_for_hour(update, context):
    update.callback_query.edit_message_text(
        text=get_message(context, epilog='At what time?', highlight='date'),
        reply_markup=hour_keyboard,
        parse_mode=ParseMode.MARKDOWN,
    )

    return ConversationStage.SELECTING_HOUR
