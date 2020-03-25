from emoji import emojize
from telegram import ParseMode

from foodshare.handlers.cook_conversation import ConversationStage, get_message
from foodshare.keyboards import telegram_number

from .reminder_selection import ask_for_reminder


def ask_for_cost(update, context):
    epilog = emojize(
        'How much is it going to cost in total?\nFor :question_mark: €'
    )

    update.callback_query.edit_message_text(
        text=get_message(context, epilog=epilog, highlight='nb_of_person'),
        reply_markup=telegram_number.number_keyboard,
        parse_mode=ParseMode.MARKDOWN,
    )

    return ConversationStage.SELECTING_COST


def cost_selection_handler(update, context):
    (
        cost_is_selected,
        want_back,
        cost,
    ) = telegram_number.process_number_selection(update, context, '€')

    # if no cost was selected
    if not cost_is_selected:
        return ConversationStage.SELECTING_COST

    context.user_data['cost'] = cost

    return ask_for_reminder(update, context)
