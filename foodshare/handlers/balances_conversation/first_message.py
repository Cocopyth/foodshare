from datetime import datetime

from emoji import emojize
from telegram import InlineKeyboardButton as IKB
from telegram import InlineKeyboardMarkup, ParseMode
from telegram.ext import ConversationHandler

from foodshare.bdd.database_communication import (
    add_transaction,
    get_user_from_chat_id,
)
from foodshare.keyboards import telegram_number, user_selection
from foodshare.utils import emojize_number

from . import ConversationStage


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


def ask_for_user(update, context):
    chat_id = update.effective_chat.id
    user = get_user_from_chat_id(chat_id)
    callback_data = update.callback_query.data
    context.user_data['money_or_meal'] = callback_data == 'money'
    prolog = (
        'Please type the number corresponding to the user '
        'you want '
        'to make a transaction with'
    )
    update.callback_query.edit_message_text(
        text=user_selection.construct_message(
            user, (callback_data == 'money'), prolog=prolog
        ),
        reply_markup=user_selection.user_keyboard,
        parse_mode=ParseMode.MARKDOWN,
    )
    return ConversationStage.SELECTING_USER


def user_selection_handler(update, context):
    (
        user_is_selected,
        want_back,
        user,
    ) = user_selection.process_user_selection(update, context)
    ud = context.user_data
    if want_back:
        return first_message(update, context)
    elif not user_is_selected:
        return ConversationStage.SELECTING_USER
    ud['user_transaction'] = user
    return ask_for_amount(update, context)


def ask_for_amount(update, context):
    ud = context.user_data
    epilog = emojize('What amount do you want to give? \n :question_mark:')
    to_whom = ud['user_transaction']
    money = ud['money_or_meal']
    balance = (
        str(to_whom.money_balance) + '€'
        if money
        else str(to_whom.meal_balance) + 'meals'
    )
    message = (
        f'You\'re about to give  {to_whom.name} '
        f'whose balance is: \n {balance}. '
    )
    update.callback_query.edit_message_text(
        text=message + epilog,
        reply_markup=telegram_number.number_keyboard,
        parse_mode=ParseMode.MARKDOWN,
    )
    return ConversationStage.SELECTING_AMOUNT


def amount_selection_handler(update, context):
    ud = context.user_data
    money = ud['money_or_meal']
    suffix = '€' if money else 'meals'
    (
        cost_is_selected,
        want_back,
        amount,
    ) = telegram_number.process_number_selection(update, context, suffix)
    if want_back:
        return ask_for_user(update, context)
    elif not cost_is_selected:
        return ConversationStage.SELECTING_AMOUNT
    context.user_data['amount'] = amount
    return ask_for_confirmation(update, context)


def ask_for_confirmation(update, context):
    ud = context.user_data
    money = ud['money_or_meal']
    to_whom = ud['user_transaction']
    amount = emojize_number(ud['amount'])
    amount += '€' if money else ' meals'
    balance = (
        str(to_whom.money_balance) + '€'
        if money
        else str(to_whom.meal_balance) + 'meals'
    )
    message = (
        f'You\'re about to give  {amount} \n'
        f'to  {to_whom.name}\n'
        f'whose balance is: {balance}. \n'
        f'This user should give you the equivalent amount in real '
        f'life in '
        f'exchange\n'
        f'Do you confirm?'
    )
    keyboard = InlineKeyboardMarkup(
        [
            [IKB('Confirm', callback_data='confirm')],
            [IKB('Back', callback_data='back')],
        ]
    )
    update.callback_query.edit_message_text(
        text=message, reply_markup=keyboard,
    )
    return ConversationStage.CONFIRMING


def transaction_end(update, context):
    ud = context.user_data
    money = ud['money_or_meal']
    to_whom = ud['user_transaction']
    amount = ud['amount']
    date_time = datetime.now()
    chat_id = update.effective_chat.id
    new_balance = add_transaction(chat_id, money, to_whom, amount, date_time)
    ud.clear()
    message = f'Your balance is now {new_balance}'
    message += '€' if money else ' meals'
    update.callback_query.edit_message_text(
        text=message, parse_mode=ParseMode.MARKDOWN,
    )
    return ConversationHandler.END
