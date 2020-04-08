from emoji import emojize
from telegram import ParseMode
from telegram.ext import ConversationHandler

from foodshare.handlers.cook_conversation import ConversationStage, get_message
from foodshare.keyboards.confirmation_keyboard import confirmation_keyboard


def ask_for_conclusion(update, context, highlight=None):
    epilog = (
        'Now I will send a message to people if you want'
        + ' to add a text message just send it to me. '
        + 'Press confirm when you\'re ready!'
    )
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

    return ConversationStage.CONFIRMATION


def end(update, context):
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over"""

    update.callback_query.edit_message_text(
        text=emojize(
            f'Messages sent : I will update you on the answers '
            f':nerd_face: '
        ),
        parse_mode=ParseMode.MARKDOWN,
    )
    sticker_id = (
        'CAACAgIAAxkBAAIJNF6N7Cj5oZ7qs9hrRce8HdLTn'
        '7FdAAKcAgACa8TKChTuhP744omRGAQ'
    )  # Lazybone ID
    bot = context.bot
    chat_id = context.user_data['chat_id']
    bot.send_sticker(chat_id, sticker_id)
    # save data in the database + send messages
    context.user_data.clear()
    return ConversationHandler.END
