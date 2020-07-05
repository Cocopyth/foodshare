from telegram import InlineKeyboardButton as IKB
from telegram import InlineKeyboardMarkup
from foodshare.keyboards import user_selection
from foodshare.bdd.database_communication import get_user_from_chat_id

from . import ConversationStage
from telegram import ParseMode

def first_message(update, context):
    chat_id = update.effective_chat.id
    user = get_user_from_chat_id(chat_id)
    bot = context.bot
    if user is None:
        message = (
            "Hello there! First time we meet isn't it? "
            "I just need a few information about you!"
        )
        keyboard = InlineKeyboardMarkup(
            [[IKB('Register', callback_data='register_asked0523')]]
        )

        bot.send_message(chat_id=chat_id, text=message, reply_markup=keyboard)
        return ConversationStage.REGISTERING
    else:
        keyboard = InlineKeyboardMarkup(
            [
                [IKB('Give money', callback_data='money')],
                [IKB('Give meal points', callback_data='meal')],
            ]
        )
        message = 'What kind of transaction do you want to make?'
        bot.send_message(chat_id=chat_id, text=message, reply_markup=keyboard)
        return ConversationStage.MONEY_OR_MEAL

def ask_for_user(update,context):
    chat_id = update.effective_chat.id
    user = get_user_from_chat_id(chat_id)
    callback_data = update.callback_query.data
    update.callback_query.edit_message_text(
        text=user_selection.construct_message(user.community,
                                              (callback_data=='money')),
        reply_markup=user_selection.user_keyboard,
        parse_mode=ParseMode.MARKDOWN,
    )
    return ConversationStage.SELECTING_USER

def user_selection_handler(update, context):
    (
        user_is_selected,
        want_back,
        user,
    ) = user_selection.process_user_selection(update, context, '€')
    ud = context.user_data
    if want_back:
        return first_message(update, context)
    elif not user_is_selected:
        return ConversationStage.SELECTING_USER
    ud['user_transaction'] = user
    return ask_for_confirmation(update, context)

def ask_for_confirmation(update,context):
    return None