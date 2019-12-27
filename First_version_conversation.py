# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 12:23:33 2019

@author: Coretib
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 22:03:04 2019

@author: Coretib
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple inline keyboard bot with multiple CallbackQueryHandlers.
This Bot uses the Updater class to handle the bot.
First, a few callback functions are defined as callback query handler. Then, those functions are
passed to the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot that uses inline keyboard that has multiple CallbackQueryHandlers arranged in a
ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line to stop the bot.
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ChatAction
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackQueryHandler,
)
import logging
import datetime
import calendar

import telegramcalendar
from telegramhour import hour_keyboard, process_time_selection
from telegramnumber import number_keyboard, process_number_selection, emojify
from telegramcost import cost_keyboard, process_cost_selection
from gif_test import first_gif
from telegram.ext.dispatcher import run_async

d = 1

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


def get_weekday(date_datetime):
    weekday = date_datetime.weekday()
    return calendar.day_name[weekday]


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
pattern_date = "^" + Today + "$|^" + Tomorrow + "$|^" + Dayp2 + "$"

# helping bool
START_OVER = "start_over"
buttonstest = [
    [
        InlineKeyboardButton(text="Today", callback_data=Today),
        InlineKeyboardButton(text="Tomorrow", callback_data=Tomorrow),
    ],
    [
        InlineKeyboardButton(text="On", callback_data=Dayp2),
        InlineKeyboardButton(text="Show calendar", callback_data=Calendargo),
    ],
    [InlineKeyboardButton(text="Change name of the meal", callback_data=back)],
]
keyboardtest = InlineKeyboardMarkup(buttonstest)


def transform_date(when):
    date = datetime.date.today()
    times = [Today, Tomorrow, Dayp2]
    datecook = date + datetime.timedelta(days=times.index(when))
    return (get_weekday(datecook), datecook)


def meal_name(update, context):
    """Prompt user to input data for selected feature."""
    if START_OVER not in context.user_data:
        context.user_data[START_OVER] = True
    text = "Tell me what you want to cook! (just type it as an answer to this message)"
    if context.user_data[START_OVER]:
        update.message.reply_text(text=text)
    else:
        update.callback_query.edit_message_text(text=text)
    context.user_data[START_OVER] = True
    return TYPING


def save_input(update, context):
    ud = context.user_data
    ud["name"] = update.message.text
    bot = context.bot
    context.bot.send_chat_action(
        chat_id=update.effective_message.chat_id, action=ChatAction.TYPING
    )
    url = first_gif(ud["name"])
    if url != None:
        bot.send_document(chat_id=update.message.chat_id, document=url)
    return date_choosing(update, context)


def date_choosing(update, context):
    date = datetime.date.today()
    weekdayp2 = get_weekday(date + datetime.timedelta(days=2))
    ud = context.user_data
    buttons = [
        [
            InlineKeyboardButton(text="Today", callback_data=Today),
            InlineKeyboardButton(text="Tomorrow", callback_data=Tomorrow),
        ],
        [
            InlineKeyboardButton(text="On " + weekdayp2, callback_data=Dayp2),
            InlineKeyboardButton(text="Show calendar", callback_data=Calendargo),
        ],
        [InlineKeyboardButton(text="Change name of the meal", callback_data=back)],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    if not context.user_data.get(START_OVER):
        text = "🍌 You're cooking " + ud["name"] + "\n When do you want to cook?"
        update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    # But after we do that, we need to send a new message
    else:
        text = "🍌 You're cooking " + ud["name"] + "🍌 \n When do you want to cook? "
        update.message.reply_text(text=text, reply_markup=keyboard)
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
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Please select a date:",
        reply_markup=telegramcalendar.create_calendar(),
    )
    return SELECTING_DATE_CALENDAR


def date_handler(update, context):
    bot = context.bot
    query = update.callback_query
    when = query.data
    weekday, date = transform_date(when)
    ud = context.user_data
    ud["date"] = date
    text = "\n".join(query.message.text.split("\n")[:1])
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=text
        + "\n 🕒 on "
        + get_weekday(date)
        + " "
        + ud["date"].strftime("%d/%m/%Y")
        + "\n at what time?"
        + "\n❔ ❔:❔ ❔"
        + "\n ⬆️",
        reply_markup=hour_keyboard,
    )
    return SELECTING_HOUR


def inline_calendar_handler(update, context):
    bot = context.bot
    query = update.callback_query
    selected, date = telegramcalendar.process_calendar_selection(bot, update)
    if selected:
        ud = context.user_data
        if "cost_selected" in ud and ud["cost_selected"]:
            ud["date_limit"] = date
            text = "\n".join(query.message.text.split("\n")[:4])
            bot.edit_message_text(
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                text=text
                + "⏰ You will have an answer and know how many people are coming"
                + "\n on "
                + get_weekday(date)
                + " "
                + ud["date_limit"].strftime("%d/%m/%Y")
                + "\n at what time?"
                + "\n❔ ❔:❔ ❔"
                + "\n ⬆️",
                reply_markup=hour_keyboard,
            )
            return SELECTING_HOUR
        else:
            ud = context.user_data
            ud["date"] = date
            text = "\n".join(query.message.text.split("\n")[:1])
            bot.edit_message_text(
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                text=text
                + "\n 🕒 on "
                + get_weekday(date)
                + " "
                + ud["date"].strftime("%d/%m/%Y")
                + "\n at what time?"
                + "\n❔ ❔:❔ ❔"
                + "\n ⬆️",
                reply_markup=hour_keyboard,
            )
            return SELECTING_HOUR
    return SELECTING_DATE_CALENDAR


def inline_time_handler(update, context):
    bot = context.bot
    query = update.callback_query
    selected, time = process_time_selection(update, context)
    if selected:
        ud = context.user_data
        if "cost_selected" in ud and ud["cost_selected"]:
            ud = context.user_data
            date = ud["date_limit"]
            ud["date"] = datetime.datetime.combine(date, time)
            text = "\n".join(query.message.text.split("\n")[:4])
            bot.edit_message_text(
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                text=text
                + "⏰ You will have an answer and know how many people are coming"
                + "\n on "
                + get_weekday(date)
                + " "
                + ud["date_limit"].strftime("%d/%m/%Y at %H:%M")
                + "\n Now I will send a message to people if you want"
                + " to add a text message just send it to me."
                + "Press confirm when you're ready!",
                reply_markup=hour_keyboard,
            )
            return CONFIRMATION
        else:
            ud = context.user_data
            date = ud["date"]
            ud["date"] = datetime.datetime.combine(date, time)
            text = "\n".join(query.message.text.split("\n")[:1])
            bot.edit_message_text(
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                text=text
                + "\n 🕒 on "
                + get_weekday(date)
                + " "
                + ud["date"].strftime("%d/%m/%Y at %H:%M")
                + "\n for how many people? (including yourself)"
                + "\n ",
                reply_markup=number_keyboard,
            )
            return SELECTING_NUMBER
    return SELECTING_HOUR


def inline_number_handler(update, context):
    bot = context.bot
    query = update.callback_query
    selected, back, number = process_number_selection(update, context)
    if selected:
        if back:
            return date_choosing(update, context)
        else:
            text = "\n".join(query.message.text.split("\n")[:2])
            bot.edit_message_text(
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                text=text
                + "\n 👪 for "
                + emojify(number)
                + " persons"
                + "\n How much is it going to cost in total?",
                reply_markup=cost_keyboard,
            )
            return SELECTING_COST
    return SELECTING_NUMBER


def inline_cost_handler(update, context):
    bot = context.bot
    query = update.callback_query
    selected, back, number = process_cost_selection(update, context)
    ud = context.user_data
    ud["cost_selected"] = False
    if selected:
        if back:
            text = "\n".join(query.message.text.split("\n")[:2])
            bot.edit_message_text(
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                text=text + "\n for how many people? (including yourself)" + "\n ",
                reply_markup=number_keyboard,
            )
            return SELECTING_NUMBER
        else:
            ud["cost_selected"] = True
            text = "\n".join(query.message.text.split("\n")[:3])
            bot.edit_message_text(
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                text=text
                + "\n💶 for "
                + emojify(number)
                + "€ in total"
                + "\n How much time in advance do you want to know who's coming?"
                + "\n ",
                reply_markup=keyboardtest,
            )
            return SELECTING_REMINDER
    return SELECTING_COST


def reminder_choosing(update, context):

    if not context.user_data.get(START_OVER):
        text = "You've chosen to cook " + "\n When do you want to cook?"
        update.callback_query.edit_message_text(text=text)
    # But after we do that, we need to send a new message
    else:
        text = "🍌 You've chosen to cook " + "🍌 \n When do you want to cook? "
        update.message.reply_text(text=text)
    context.user_data[START_OVER] = False
    return CONFIRMATION


def end(update, context):
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over"""
    query = update.callback_query
    bot = context.bot
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="See you next time!",
    )
    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater("921706886:AAE8KrSbCPMr1lB1VFZINP_M1s8wibaMkTE", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Setup conversation handler with the states FIRST and SECOND
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", meal_name)],
        states={
            TYPING: [MessageHandler(Filters.text, save_input)],
            SELECTING_DATE: [
                CallbackQueryHandler(date_handler, pattern=pattern_date),
                CallbackQueryHandler(calendar_handler, pattern="^" + Calendargo + "$"),
                CallbackQueryHandler(meal_name, pattern="^" + back + "$"),
            ],
            SELECTING_DATE_CALENDAR: [CallbackQueryHandler(inline_calendar_handler)],
            SELECTING_HOUR: [CallbackQueryHandler(inline_time_handler)],
            SELECTING_NUMBER: [CallbackQueryHandler(inline_number_handler)],
            SELECTING_COST: [CallbackQueryHandler(inline_cost_handler)],
            SELECTING_REMINDER: [
                CallbackQueryHandler(reminder_choosing, pattern=pattern_date),
                CallbackQueryHandler(calendar_handler, pattern="^" + Calendargo + "$"),
                CallbackQueryHandler(inline_cost_handler, pattern="^" + back + "$"),
            ],
        },
        fallbacks=[CommandHandler("start", meal_name)],
    )

    # Add ConversationHandler to dispatcher that will be used for handling
    # updates
    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
