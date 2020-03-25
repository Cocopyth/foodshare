from emoji import emojize
from telegram import ParseMode

from foodshare.handlers.cook_conversation import ConversationStage, get_message
from foodshare.keyboards import telegram_number

from .cost_selection import ask_for_cost


def ask_for_number_of_person(update, context):
    epilog = emojize(
        'For how many people (including yourself)?\nFor :question_mark: '
        'persons'
    )

    update.callback_query.edit_message_text(
        text=get_message(context, epilog=epilog, highlight='time'),
        reply_markup=telegram_number.number_keyboard,
        parse_mode=ParseMode.MARKDOWN,
    )

    return ConversationStage.SELECTING_NB_OF_PERSON


def nb_of_person_selection_handler(update, context):
    (
        nb_is_selected,
        want_back,
        nb_of_person,
    ) = telegram_number.process_number_selection(update, context, 'persons')

    # if no number was selected
    if not nb_is_selected:
        return ConversationStage.SELECTING_NB_OF_PERSON

    context.user_data['nb_of_person'] = nb_of_person

    return ask_for_cost(update, context)
