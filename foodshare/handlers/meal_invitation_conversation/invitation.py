from . import ConversationStage

def invitation(update, context):
    ud = context.user_data
    bot = context.bot
    message = 'v'
    chat_id = update.message.chat_id
    update.message.reply_text(message)
    infos = bot.get_chat(chat_id)
    print(infos)
    return ConversationStage.DEBUG_STAGE_1
