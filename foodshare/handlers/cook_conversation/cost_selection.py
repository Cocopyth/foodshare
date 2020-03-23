from telegram import ParseMode

from foodshare.handlers.cook_conversation import ConversationStage, get_message
from foodshare.keyboards import telegram_cost


def ask_for_cost(update, context):
    epilog = 'How much is it going to cost in total?'

    update.callback_query.edit_message_text(
        text=get_message(context, epilog=epilog, highlight='nb_of_person'),
        reply_markup=telegram_cost.cost_keyboard,
        parse_mode=ParseMode.MARKDOWN,
    )

    return ConversationStage.SELECTING_COST
