import datetime

from telegram import InlineKeyboardButton as IKB
from telegram import InlineKeyboardMarkup, ParseMode

from . import ConversationStage


def get_weekday(date):
    return date.strftime('%A')


def set_date_keyboard(update, _):
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

    text = 'When do you want to cook?'
    update.message.reply_text(
        text=text, reply_markup=keyboard, parse_mode=ParseMode.HTML
    )

    return ConversationStage.SELECTING_DATE
