from telegram import InlineKeyboardButton as IKB
from telegram import InlineKeyboardMarkup, ParseMode
from telegram.ext import ConversationHandler

from foodshare.bdd.database_communication import get_user_from_chat_id


def first_message(update, context, prefix=''):
    chat_id = update.effective_chat.id
    user = get_user_from_chat_id(chat_id)
    ud = context.user_data
    if user is None:
        message = (
            "Hello there! First time we meet isn't it? "
            "I just need a few information about you!"
        )
        keyboard = InlineKeyboardMarkup(
            [[IKB('Register', callback_data='register_asked0523')]]
        )
        bot = context.bot
        chat_id = update.effective_chat.id
        context.user_data['last_message'] = bot.send_message(
            chat_id=chat_id, text=message, reply_markup=keyboard
        )
        return ConversationHandler.END
    elif user.community is None:
        message = "Before anything you need to join or create a community!"
        keyboard = InlineKeyboardMarkup(
            [
                [
                    IKB(
                        'Join or create a community',
                        callback_data='joining_asked0523',
                    )
                ]
            ]
        )
        bot = context.bot
        chat_id = update.effective_chat.id
        context.user_data['last_message'] = bot.send_message(
            chat_id=chat_id, text=message, reply_markup=keyboard
        )
        return ConversationHandler.END
    elif len(user.community.members) < 2:
        message = (
            "Before anything you need to invite people to your "
            "community or join one with already some people in it!"
        )
        keyboard = InlineKeyboardMarkup(
            [
                [
                    IKB(
                        'Invite people or quit community',
                        callback_data='invite_asked0523',
                    )
                ]
            ]
        )
        bot = context.bot
        chat_id = update.effective_chat.id
        context.user_data['last_message'] = bot.send_message(
            chat_id=chat_id, text=message, reply_markup=keyboard
        )
        return ConversationHandler.END
    else:
        message = prefix + "What do you want to do?"
        keyboard = InlineKeyboardMarkup(
            [
                [
                    IKB('Cook', callback_data='cook_asked0523'),
                    IKB('See meals', callback_data='meals_asked0523'),
                ],
                [
                    IKB(
                        'Make a transaction',
                        callback_data='balances_asked0523',
                    ),
                    IKB(
                        'Manage community', callback_data='community_asked0523'
                    ),
                ],
            ]
        )
        bot = context.bot
        chat_id = update.effective_chat.id
        if 'last_message' not in ud:
            context.user_data['last_message'] = bot.send_message(
                chat_id=chat_id,
                text=message,
                reply_markup=keyboard,
                parse_mode=ParseMode.MARKDOWN,
            )
        else:
            last_message = ud['last_message']
            bot.edit_message_text(
                message_id=last_message.message_id,
                chat_id=chat_id,
                text=message,
                reply_markup=keyboard,
                parse_mode=ParseMode.MARKDOWN,
            )
        return ConversationHandler.END


def first_message_alternative(update, context):
    ud = context.user_data
    if 'last_message' in ud:
        ud.pop('last_message')
    return first_message(update, context)
