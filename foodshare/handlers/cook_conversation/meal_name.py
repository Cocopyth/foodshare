from . import ConversationStage


def ask_for_meal_name(update, _):
    update.message.reply_text(
        text=(
            'Tell me what you want to cook! (just type the name of the meal '
            'as an answer to this message)'
        )
    )

    return ConversationStage.TYPING_MEAL_NAME
