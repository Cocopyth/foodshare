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
from foodshare.handlers.start_conversation.first_message import first_message
from . import ConversationStage
money_mouth_face = "\U0001f911"

def ask_money_or_meal(update, context):
    chat_id = update.effective_chat.id
    ud = context.user_data
    bot = context.bot
    keyboard = InlineKeyboardMarkup(
        [
            [IKB('Give money', callback_data='money')],
            [IKB('Give meal points', callback_data='meal')],
            [IKB('Back', callback_data='back')]
        ]
    )
    message = 'What kind of transaction do you want to make?'
    if 'last_message' not in ud:
        last_message = bot.send_message(
            chat_id=chat_id, text=message, reply_markup=keyboard
        )
        ud['last_message'] = last_message
    else:
        last_message = ud['last_message']
        bot.edit_message_text(
            message_id=last_message.message_id,
            chat_id=chat_id,
            text=message,
            reply_markup=keyboard,
        )
    return ConversationStage.MONEY_OR_MEAL


def ask_for_user(update, context):
    chat_id = update.effective_chat.id
    user = get_user_from_chat_id(chat_id)
    callback_data = update.callback_query.data
    if callback_data == 'back':
        first_message(update, context)
        return ConversationHandler.END
    money = callback_data == 'money'
    context.user_data['money_or_meal'] = money
    keyboard = user_selection.construct_keyboard(user, money, False)
    update.callback_query.edit_message_text(
        text='Please select a user to make the transaction with',
        reply_markup=keyboard,
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
        return ask_money_or_meal(update, context)
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
        else str(to_whom.meal_balance) + ' meals'
    )
    message = emojize(
        f' You\'re about to give \n {money_mouth_face} {to_whom.name} \n'
        f':balance_scale: whose balance is:  {balance}. \n'
    )
    update.callback_query.edit_message_text(
        text=message + epilog,
        reply_markup=telegram_number.number_keyboard,
    )
    return ConversationStage.SELECTING_AMOUNT


def amount_selection_handler(update, context):
    ud = context.user_data
    money = ud['money_or_meal']
    suffix = '€' if money else 'meal(s)'
    (
        amount_is_selected,
        want_back,
        amount,
    ) = telegram_number.process_number_selection(update, context, suffix)
    if want_back:
        return ask_for_user(update, context)
    elif not amount_is_selected:
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
        else str(to_whom.meal_balance) + ' meals'
    )
    message = emojize(
        f'You\'re about to give  \n :money_bag: {amount} \n'
        f'{money_mouth_face} to {to_whom.name}\n'
        f':balance_scale: whose balance is : {balance}. \n'
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
    last_message = ud['last_message']
    context.bot.delete_message(chat_id=chat_id,
                               message_id=last_message.message_id)
    ud.clear()
    prefix = f'*Your balance is now {new_balance}'
    prefix += '€*\n' if money else ' meals* \n'
    first_message(update, context, prefix)
    return ConversationHandler.END
