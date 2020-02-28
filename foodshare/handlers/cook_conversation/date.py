import datetime

from telegram import InlineKeyboardButton as IKB
from telegram import InlineKeyboardMarkup, ParseMode

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

    return ConversationStage.SELECTING_DATE


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


def ask_for_hour(update, context):
    update.callback_query.edit_message_text(
        text=get_message(context, epilog='At what time?', highlight='date'),
        # reply_markup=hour_keyboard,
        parse_mode=ParseMode.MARKDOWN,
    )

    return ConversationStage.SELECTING_HOUR
