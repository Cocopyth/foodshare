from telegram.ext import ConversationHandler


def first_message(update, context):
    chat_id = update.effective_chat.id
    bot = context.bot
    message = (
        'This bot is to make the organisation of meals with friends, '
        'roomates or even neighboors easy and flexible.\n'
        'Press /start to begin!\n'
        'You can invite your friends with this link\n'
        'https://t.me/Meuhon_bot'
    )
    bot.send_message(chat_id=chat_id, text=message)
    return ConversationHandler.END
