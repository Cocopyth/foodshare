import datetime
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import ConversationHandler

from foodshare.handlers.cook_conversation import ConversationStage
from foodshare.keyboards import telegram_calendar
from foodshare.keyboards.confirmation_keyboard import confirmation_keyboard
from foodshare.keyboards.reminder_keyboard import (
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


def get_weekday(date):
    return date.strftime('%A')


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

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
    return ConversationStage.TYPING_MEAL_NAME


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
            return ConversationStage.SELECTING_HOUR
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
                return ConversationStage.SELECTING_DATE_CALENDAR
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
                return ConversationStage.SELECTING_HOUR
    return ConversationStage.SELECTING_DATE_CALENDAR


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
                return ConversationStage.SELECTING_DATE
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
            return ConversationStage.SELECTING_COST
    return ConversationStage.SELECTING_NUMBER


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
            return ConversationStage.SELECTING_NUMBER
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
            return ConversationStage.SELECTING_REMINDER
    return ConversationStage.SELECTING_COST


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
    return ConversationStage.CONFIRMATION


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
    return ConversationStage.CONFIRMATION


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
