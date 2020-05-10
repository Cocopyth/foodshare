from . import ConversationStage
def debug_fun(update, context):
    ud = context.user_data
    bot = context.bot
    message = 'v'
    chat_id = update.message.chat_id
    update.message.reply_text(message)
    infos = bot.get_chat(chat_id)
    print(infos)
    return ConversationStage.DEBUG_STAGE_1

def return_sticker(
    update, context
):  # Only for developpment to know sticker id
    file_id = update.message.sticker['file_id']
    bot = context.bot
    chat_id = update.message.chat_id
    print(file_id)
    bot.send_sticker(chat_id, file_id)