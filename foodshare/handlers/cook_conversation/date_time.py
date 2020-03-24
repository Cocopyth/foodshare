import datetime

from telegram import InlineKeyboardButton as IKB
from telegram import InlineKeyboardMarkup, ParseMode

from foodshare.keyboards import telegram_calendar
from foodshare.keyboards.telegram_hour import hour_keyboard, process_time_selection

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


def calendar_handler(update, context):
    update.callback_query.edit_message_text(
        text=get_message(context, epilog='Please select a date:'),
        reply_markup=telegram_calendar.create_calendar(),
    )

    return ConversationStage.SELECTING_DATE_CALENDAR


def ask_for_hour(update, context):
    update.callback_query.edit_message_text(
        text=get_message(context, epilog='At what time? \n ', highlight='date'),
        reply_markup=hour_keyboard,
        parse_mode=ParseMode.MARKDOWN,
    )

    return ConversationStage.SELECTING_HOUR

def inline_time_handler(update, context):
    bot = context.bot
    query = update.callback_query
    selected, time = process_time_selection(update, context)
    if selected:
        ud = context.user_data
        if 'cost_selected' in ud and ud['cost_selected']:
            ud = context.user_data
            date = ud['date_limit']
            ud['date'] = datetime.datetime.combine(date, time)
            text = '\n'.join(query.message.text.split('\n')[:4])
            bot.edit_message_text(
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                text=text
                + '⏰ You will have an answer and know how many people are coming'
                + '\n on '
                + get_weekday(date)
                + ' '
                + ud['date_limit'].strftime('%d/%m/%Y at %H:%M')
                + '\n Now I will send a message to people if you want'
                + ' to add a text message just send it to me.'
                + 'Press confirm when you\'re ready!',
                reply_markup=hour_keyboard,
                parse_mode=ParseMode.HTML,
            )
            return ConversationStage.CONFIRMATION
        else:
            date = ud['date']
            if datetime.datetime.combine(date, time) < datetime.datetime.now():
                date = datetime.date.today()
                weekdayp2 = get_weekday(date + datetime.timedelta(days=2))
                buttons = [
                    [
                        InlineKeyboardButton(
                            text='Today', callback_data=Today
                        ),
                        InlineKeyboardButton(
                            text='Tomorrow', callback_data=Tomorrow
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text='On ' + weekdayp2, callback_data=Dayp2
                        ),
                        InlineKeyboardButton(
                            text='Show calendar', callback_data=Calendargo
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text='Change name of the meal', callback_data=back
                        )
                    ],
                ]
                keyboard = InlineKeyboardMarkup(buttons)
                text = '\n'.join(query.message.text.split('\n')[:1])
                bot.edit_message_text(
                    chat_id=query.message.chat_id,
                    message_id=query.message.message_id,
                    text=text
                    + '\n The date chosen was in the past, please select a date in the future :',
                    reply_markup=keyboard,
                    parse_mode=ParseMode.HTML,
                )
                return ConversationStage.SELECTING_WEEKDAY_OR_SHOW_CALENDAR
            else:
                ud = context.user_data
                ud['date'] = datetime.datetime.combine(date, time)
                ud['hour_selected'] = True
                text = construct_message(ud, 'number')
                bot.edit_message_text(
                    chat_id=query.message.chat_id,
                    message_id=query.message.message_id,
                    text=text
                    + '\n for how many people? (including yourself)'
                    + '\n ',
                    reply_markup=number_keyboard,
                    parse_mode=ParseMode.HTML,
                )
                return ConversationStage.SELECTING_NUMBER
    return ConversationStage.SELECTING_HOUR