from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import ConversationHandler

from foodshare.bdd.database_communication import (
    add_meal,
    get_user_from_chat_id,
)
from foodshare.handlers.cook_conversation import ConversationStage, get_message
from foodshare.handlers.start_conversation.first_message import first_message
from foodshare.job_manager.meal_manager import handle_meals
from foodshare.keyboards.confirmation_keyboard import confirmation_keyboard
from foodshare.utils.gif_test import get_gif_url

buttons = [
    [InlineKeyboardButton(text='Confirm', callback_data='confirm')],
    [InlineKeyboardButton(text='Modify some infos', callback_data='modify')],
]
last_keyboard = InlineKeyboardMarkup(buttons)


def ask_for_conclusion(update, context, highlight=None):
    ud = context.user_data
    query = update.callback_query
    ud['last_query'] = query
    epilog = (
        'Now I will send a message to people if you want'
        + ' to add a text message just send it to me. '
        + 'Press confirm when you\'re ready!'
    )
    context.user_data['confirmation_stage'] = True
    text = get_message(context, epilog=epilog, highlight=highlight)

    if (
        update.message is None
    ):  # reply doesn't work if there is no message to reply to
        update.callback_query.edit_message_text(
            text=text,
            reply_markup=last_keyboard,
            parse_mode=ParseMode.MARKDOWN,
        )
    else:
        update.message.reply_text(
            text=text,
            reply_markup=last_keyboard,
            parse_mode=ParseMode.MARKDOWN,
        )

    return ConversationStage.CONFIRMATION


def additional_message(update, context):
    bot = context.bot
    ud = context.user_data
    ud['message2others'] = update.message.text
    bot.deleteMessage(update.message.chat_id, update.message.message_id)
    query = ud['last_query']
    epilog = (
        'Now I will send a message to people if you want'
        + ' to add a text message just send it to me. '
        + 'Press confirm when you\'re ready!'
    )
    text = get_message(context, epilog=epilog)

    bot.edit_message_text(
        text=text,
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        reply_markup=last_keyboard,
        parse_mode=ParseMode.MARKDOWN,
    )
    return ConversationStage.CONFIRMATION


def end(update, context):
    # sticker_id = (
    #     'CAACAgIAAxkBAAIJNF6N7Cj5oZ7qs9hrRce8HdLTn'
    #     '7FdAAKcAgACa8TKChTuhP744omRGAQ'
    # )  # Lazybone ID
    bot = context.bot
    chat_id = context.user_data['chat_id']
    ud = context.user_data
    bot.deleteMessage(chat_id, ud['last_message'].message_id)
    who_cooks = get_user_from_chat_id(chat_id)
    gif_url = get_gif_url(ud['meal_name'])
    if gif_url is not None:
        bot.send_document(chat_id=chat_id, document=gif_url)
    add_meal(who_cooks, ud, gif_url)
    # bot.send_sticker(chat_id, sticker_id)

    ud.clear()
    prefix = f'Messages sent : I will update you on the answers \n'
    while not handle_meals():
        pass
    first_message(update, context, prefix=prefix)
    return ConversationHandler.END


def modify_infos(update, context):
    ud = context.user_data
    query = update.callback_query
    ud['last_query'] = query
    epilog = 'Chose what information you want to modify!'
    context.user_data['confirmation_stage'] = True
    text = get_message(context, epilog=epilog)

    if (
        update.message is None
    ):  # reply doesn't work if there is no message to reply to
        update.callback_query.edit_message_text(
            text=text,
            reply_markup=confirmation_keyboard,
            parse_mode=ParseMode.MARKDOWN,
        )
    else:
        update.message.reply_text(
            text=text,
            reply_markup=confirmation_keyboard,
            parse_mode=ParseMode.MARKDOWN,
        )
    return ConversationStage.MODIFICATION
