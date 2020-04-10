from emoji import emojize
from telegram import ParseMode

from foodshare.handlers.cook_conversation import ConversationStage, get_message
from foodshare.keyboards import telegram_number

from .conclusion_selection import ask_for_conclusion
from .reminder_selection import ask_for_reminder


def ask_for_cost(update, context):
    epilog = emojize(
        'How much is it going to cost in total?\nFor :question_mark: €'
    )

    update.callback_query.edit_message_text(
        text=get_message(context, epilog=epilog, highlight='cost'),
        reply_markup=telegram_number.number_keyboard,
        parse_mode=ParseMode.MARKDOWN,
    )

    return ConversationStage.SELECTING_COST


def cost_selection_handler(update, context):
    from .nb_of_person_selection import ask_for_number_of_person

    (
        cost_is_selected,
        want_back,
        cost,
    ) = telegram_number.process_number_selection(update, context, '€')
    ud = context.user_data
    if 'confirmation_stage' in ud and (want_back or cost_is_selected):
        if cost_is_selected:
            context.user_data['cost'] = cost
        return ask_for_conclusion(update, context, highlight='cost')
    elif want_back:
        return ask_for_number_of_person(update, context)
    elif not cost_is_selected:
        return ConversationStage.SELECTING_COST
    context.user_data['cost'] = cost
    return ask_for_reminder(update, context)
