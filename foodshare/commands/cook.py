import calendar
import datetime
import logging

from telegram import (
    ChatAction,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ParseMode,
)
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    Filters,
    MessageHandler,
)

from foodshare.commands.gif_test import first_gif
from foodshare.keyboards import telegram_calendar
from foodshare.keyboards.confirmation_keyboard import (
    confirm,
    confirmation_keyboard,
    what,
)
from foodshare.keyboards.reminder_keyboard import (
    back2,
    chose,
    pattern_reminder,
    reminder_keyboard_build,
    transform_limit,
)
from foodshare.keyboards.telegram_cost import (
    cost_keyboard,
    process_cost_selection,
)
from foodshare.keyboards.telegram_hour import (
    hour_keyboard,
    process_time_selection,
)
from foodshare.keyboards.telegram_number import (
    emojify,
    number_keyboard,
    process_number_selection,
)


def get_weekday(date_datetime):
    weekday = date_datetime.weekday()
    return calendar.day_name[weekday]


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)

logger = logging.getLogger(__name__)
# Stages
(
    SELECTING_DATE,
    TYPING,
    SELECTING_DATE_CALENDAR,
    NUMBER_SELECTION,
    SELECTING_HOUR,
    SELECTING_NUMBER,
    SELECTING_COST,
    SELECTING_REMINDER,
    CONFIRMATION,
) = map(chr, range(9))
# Callback data
Today, Tomorrow, Dayp2, Calendargo, back = map(chr, range(5))
pattern_date = '^' + Today + '$|^' + Tomorrow + '$|^' + Dayp2 + '$'

# helping bool
START_OVER = 'start_over'


def construct_message(ud, highlight=None):
    message = []
    if 'name' in ud:
        name_text = '🍌 You\'re cooking ' + ud['name'] + '🍌 '
        if highlight == 'name':
            name_text = '<b>' + name_text + '</b>'
        message.append(name_text)
    if 'date' in ud:
        date = ud['date']
        date_hour_text = '🕒 on ' + get_weekday(date) + ' '
        if 'hour_selected' in ud and ud['hour_selected']:
            date_hour_text += ud['date'].strftime('%d/%m/%Y at %H:%M')
        else:
            date_hour_text += ud['date'].strftime('%d/%m/%Y')
        if highlight == 'date':
            date_hour_text = '<b>' + date_hour_text + '</b>'
        message.append(date_hour_text)
    if 'number' in ud:
        number = ud['number']
        number_text = '👪 for ' + emojify(number) + ' persons'
        if highlight == 'number':
            number_text = '<b>' + number_text + '</b>'
        message.append(number_text)
    if 'cost' in ud:
        cost = ud['cost']
        cost_text = 'for ' + emojify(cost) + '€ in total'
        if highlight == 'cost':
            cost_text = '<b>' + cost_text + '</b>'
        message.append(cost_text)
    if 'date_limit' in ud:

        date_limit = ud['date_limit']
        print('before')
        date_limit_text = (
            '⏰ You will have an answer and know how many people are coming'
            + 'on '
            + get_weekday(date)
            + ' '
            + date_limit.strftime('%d/%m/%Y at %H:%M')
        )
        print('after')
        if highlight == 'date_limit':
            date_limit_text = '<b>' + date_limit_text + '</b>'
        message.append(date_limit_text)
    return '\n'.join(message)


def transform_date(whenn):
    date = datetime.date.today()
    times = [Today, Tomorrow, Dayp2]
    datecook = date + datetime.timedelta(days=times.index(whenn))
    return (get_weekday(datecook), datecook)


def meal_name(update, context):
    """Prompt user to input data for selected feature."""
    ud = context.user_data
    if START_OVER not in context.user_data:
        ud[START_OVER] = True
    text = 'Tell me what you want to cook! (just type it as an answer to this message)'
    if ud[START_OVER]:
        update.message.reply_text(text=text)
    else:
        update.callback_query.edit_message_text(text=text)
    ud[START_OVER] = True
    return TYPING


def meal_name_confirm(update, context):
    ud = context.user_data
    bot = context.bot
    query = ud['last_query']
    ud['name'] = '❔'
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=construct_message(ud, 'name')
        + '\n Send me a message to tell me what you want to cook',
        reply_markup=confirmation_keyboard,
        parse_mode=ParseMode.HTML,
    )
    return TYPING


def save_input(update, context):
    ud = context.user_data
    ud['name'] = update.message.text
    bot = context.bot
    context.bot.send_chat_action(
        chat_id=update.effective_message.chat_id, action=ChatAction.TYPING
    )
    bot.deleteMessage(update.message.chat_id, update.message.message_id)
    if 'confirmation_phase' in ud and ud['confirmation_phase']:
        query = ud['last_query']
        text = construct_message(ud, 'name')
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text=text
            + '\n Now I will send a message to people if you want'
            + ' to add a text message just send it to me. '
            + 'Press confirm when you\'re ready!',
            reply_markup=confirmation_keyboard,
            parse_mode=ParseMode.HTML,
        )
        return CONFIRMATION
    else:
        try:
            url = first_gif(ud['name'])
        except:
            print('Problem with gif')
        if url != None:
            bot.send_document(chat_id=update.message.chat_id, document=url)
    return date_choosing(update, context)


def date_choosing(update, context):
    date = datetime.date.today()
    weekdayp2 = get_weekday(date + datetime.timedelta(days=2))
    ud = context.user_data
    buttons = [
        [
            InlineKeyboardButton(text='Today', callback_data=Today),
            InlineKeyboardButton(text='Tomorrow', callback_data=Tomorrow),
        ],
        [
            InlineKeyboardButton(text='On ' + weekdayp2, callback_data=Dayp2),
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
    text = construct_message(ud, 'date') + '\n When do you want to cook? '
    if not context.user_data.get(START_OVER):
        update.callback_query.edit_message_text(
            text=text, reply_markup=keyboard, parse_mode=ParseMode.HTML
        )
    else:
        update.message.reply_text(
            text=text, reply_markup=keyboard, parse_mode=ParseMode.HTML
        )
    context.user_data[START_OVER] = False
    return SELECTING_DATE


# def number(update,context):
#
# def cost(update,context):
#
# def advance(update):


def calendar_handler(update, context):
    bot = context.bot
    query = update.callback_query
    ud = context.user_data
    text = construct_message(ud, 'date')
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=text + '\n Please select a date:',
        reply_markup=telegram_calendar.create_calendar(),
    )
    return SELECTING_DATE_CALENDAR


def date_handler(update, context):
    bot = context.bot
    query = update.callback_query
    whenwhen = query.data
    weekday, date = transform_date(whenwhen)
    ud = context.user_data
    ud['date'] = date
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=construct_message(ud, 'date')
        + '\n at what time?'
        + '\n❔ ❔:❔ ❔'
        + '\n ⬆️',
        reply_markup=hour_keyboard,
        parse_mode=ParseMode.HTML,
    )
    return SELECTING_HOUR


def inline_calendar_handler(update, context):
    bot = context.bot
    query = update.callback_query
    selected, date = telegram_calendar.process_calendar_selection(bot, update)
    if selected:
        ud = context.user_data
        if 'cost_selected' in ud and ud['cost_selected']:
            ud['date_limit'] = date
            text = '\n'.join(query.message.text.split('\n')[:4])
            bot.edit_message_text(
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                text=text
                + '⏰ You will have an answer and know how many people are coming'
                + '\n on '
                + get_weekday(date)
                + ' '
                + ud['date_limit'].strftime('%d/%m/%Y')
                + '\n at what time?'
                + '\n❔ ❔:❔ ❔'
                + '\n ⬆️',
                reply_markup=hour_keyboard,
                parse_mode=ParseMode.HTML,
            )
            return SELECTING_HOUR
        else:
            text = '\n'.join(query.message.text.split('\n')[:1])
            if date < datetime.datetime.now():
                bot.edit_message_text(
                    chat_id=query.message.chat_id,
                    message_id=query.message.message_id,
                    text=text
                    + '\n The date chosen was in the past, please select a date in the future :',
                    reply_markup=telegram_calendar.create_calendar(),
                    parse_mode=ParseMode.HTML,
                )
                return SELECTING_DATE_CALENDAR
            else:
                ud = context.user_data
                ud['date'] = date
                text = construct_message(ud, 'date')
                bot.edit_message_text(
                    chat_id=query.message.chat_id,
                    message_id=query.message.message_id,
                    text=text + '\n at what time?' + '\n❔ ❔:❔ ❔' + '\n ⬆️',
                    reply_markup=hour_keyboard,
                    parse_mode=ParseMode.HTML,
                )
                return SELECTING_HOUR
    return SELECTING_DATE_CALENDAR


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
            return CONFIRMATION
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
                return SELECTING_DATE
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
                return SELECTING_NUMBER
    return SELECTING_HOUR


def hours_until_meal(date):
    time_delta = (date - datetime.datetime.now()).total_seconds()
    return time_delta / 3600


def inline_number_handler(update, context):
    bot = context.bot
    query = update.callback_query
    selected, back, number = process_number_selection(update, context)
    ud = context.user_data
    if selected:
        if back:
            ud['hour_selected'] = False
            return date_choosing(update, context)
        else:
            text = '\n'.join(query.message.text.split('\n')[:2])
            ud = context.user_data
            ud['number'] = number
            bot.edit_message_text(
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                text=text
                + '\n 👪 for '
                + emojify(number)
                + ' persons'
                + '\n How much is it going to cost in total?',
                reply_markup=cost_keyboard,
            )
            return SELECTING_COST
    return SELECTING_NUMBER


def inline_cost_handler(update, context):
    bot = context.bot
    query = update.callback_query
    ud = context.user_data
    if 'cost_selected' in ud and ud['cost_selected']:
        ud['cost_selected'] = False
        text = '\n'.join(query.message.text.split('\n')[:2])
        number = ud['number']
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text=text
            + '\n 👪 for '
            + emojify(number)
            + ' persons'
            + '\n How much is it going to cost in total?',
            reply_markup=cost_keyboard,
            parse_mode=ParseMode.HTML,
        )
    selected, goback, number = process_cost_selection(update, context)
    if selected:
        if goback:
            text = '\n'.join(query.message.text.split('\n')[:2])
            bot.edit_message_text(
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                text=text
                + '\n for how many people? (including yourself)'
                + '\n ',
                reply_markup=number_keyboard,
                parse_mode=ParseMode.HTML,
            )
            return SELECTING_NUMBER
        else:
            ud['cost_selected'] = True
            ud['cost'] = number
            text = '\n'.join(query.message.text.split('\n')[:3])
            time_left = hours_until_meal(ud['date'])
            keyboard = reminder_keyboard_build(time_left)
            bot.edit_message_text(
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                text=text
                + '\n💶 for '
                + emojify(number)
                + '€ in total'
                + '\n How much time in advance do you want to know who\'s '
                'coming?' + '\n ',
                reply_markup=keyboard,
                parse_mode=ParseMode.HTML,
            )
            return SELECTING_REMINDER
    return SELECTING_COST


def reminder_choosing(update, context):
    bot = context.bot
    ud = context.user_data
    query = update.callback_query
    pushed, time_left = query.data, hours_until_meal(ud['date'])
    date_limit = transform_limit(pushed, time_left)
    ud['date_limit'] = date_limit
    date = ud['date_limit']
    text = '\n'.join(query.message.text.split('\n')[:4])
    ud['confirmation_phase'] = True
    ud['last_query'] = query  # useful to handle text message
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=text
        + '\n⏰ You will have an answer and know how many people are coming'
        + 'on '
        + get_weekday(date)
        + ' '
        + ud['date_limit'].strftime('%d/%m/%Y at %H:%M')
        + '\n Now I will send a message to people if you want'
        + ' to add a text message just send it to me. '
        + 'Press confirm when you\'re ready!',
        reply_markup=confirmation_keyboard,
        parse_mode=ParseMode.HTML,
    )
    return CONFIRMATION


def save_input2(update, context):
    bot = context.bot
    ud = context.user_data
    query = ud['last_query']
    ud['message2others'] = update.message.text
    bot.deleteMessage(update.message.chat_id, update.message.message_id)
    date = ud['date_limit']
    text = '\n'.join(query.message.text.split('\n')[:4])
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=text
        + '\n⏰ You will have an answer and know how many people are coming'
        + 'on '
        + get_weekday(date)
        + ' '
        + ud['date_limit'].strftime('%d/%m/%Y at %H:%M')
        + '\n Now I will send a message to people with additional information :'
        + ' \''
        + '<b>'
        + ud['message2others']
        + '</b>'
        + ' \' \n'
        + 'Press confirm when you\'re ready or send another message to change '
        + 'the additional information.',
        reply_markup=confirmation_keyboard,
        parse_mode=ParseMode.HTML,
    )
    return CONFIRMATION


def end(update, context):
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over"""
    query = update.callback_query
    bot = context.bot
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text='See you next time!',
    )
    # save data in the database + send messages
    context.user_data.clear()
    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


conv_handler_cook = ConversationHandler(
    entry_points=[CommandHandler('cook', meal_name)],
    states={
        TYPING: [MessageHandler(Filters.text, save_input)],
        SELECTING_DATE: [
            CallbackQueryHandler(date_handler, pattern=pattern_date),
            CallbackQueryHandler(
                calendar_handler, pattern='^' + Calendargo + '$'
            ),
            CallbackQueryHandler(meal_name, pattern='^' + back + '$'),
        ],
        SELECTING_DATE_CALENDAR: [
            CallbackQueryHandler(inline_calendar_handler)
        ],
        SELECTING_HOUR: [CallbackQueryHandler(inline_time_handler)],
        SELECTING_NUMBER: [CallbackQueryHandler(inline_number_handler)],
        SELECTING_COST: [CallbackQueryHandler(inline_cost_handler)],
        SELECTING_REMINDER: [
            CallbackQueryHandler(reminder_choosing, pattern=pattern_reminder),
            CallbackQueryHandler(calendar_handler, pattern='^' + chose + '$'),
            CallbackQueryHandler(
                inline_cost_handler, pattern='^' + back2 + '$'
            ),
        ],
        CONFIRMATION: [
            MessageHandler(Filters.text, save_input2),
            CallbackQueryHandler(end, pattern=confirm),
            CallbackQueryHandler(meal_name_confirm, pattern=what),
        ],
    },
    fallbacks=[CommandHandler('start', meal_name)],
)
