from telegram.ext import CallbackQueryHandler as CQH
from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    Filters,
    MessageHandler,
)

from foodshare.keyboards.confirmation_keyboard import (
    confirm,
    howmany,
    howmuch,
    reminder,
    what,
    when_date,
    when_time,
)

from . import ConversationStage as CS
from .conclusion_selection import additional_message, end
from .cost_selection import ask_for_cost, cost_selection_handler
from .date_selection import (
    ask_for_date,
    calendar_selection_handler,
    get_date_from_calendar,
    get_date_from_weekday,
)
from .meal_name_choice import ask_for_meal_name, save_meal_name
from .nb_of_person_selection import (
    ask_for_number_of_person,
    nb_of_person_selection_handler,
)
from .reminder_selection import ask_for_reminder, get_deadline
from .time_selection import ask_for_time, time_selection_handler

cook_handler = ConversationHandler(
    entry_points=[CommandHandler('cook', ask_for_meal_name)],
    states={
        CS.TYPING_MEAL_NAME: [MessageHandler(Filters.text, save_meal_name)],
        CS.SELECTING_WEEKDAY_OR_SHOW_CALENDAR: [
            CQH(get_date_from_weekday, pattern='today|tmo|in_2_days'),
            CQH(get_date_from_calendar, pattern='show_calendar'),
            CQH(ask_for_meal_name, pattern='back'),
        ],
        CS.SELECTING_DATE_CALENDAR: [CQH(calendar_selection_handler)],
        CS.SELECTING_HOUR: [CQH(time_selection_handler)],
        CS.SELECTING_NB_OF_PERSON: [CQH(nb_of_person_selection_handler)],
        CS.SELECTING_COST: [CQH(cost_selection_handler)],
        CS.SELECTING_REMINDER: [CQH(get_deadline)],
        CS.CONFIRMATION: [
            MessageHandler(Filters.text, additional_message),
            CQH(end, pattern=confirm),
            CQH(ask_for_date, pattern=when_date),
            CQH(ask_for_number_of_person, pattern=howmany),
            CQH(ask_for_cost, pattern=howmuch),
            CQH(ask_for_reminder, pattern=reminder),
            CQH(ask_for_meal_name, pattern=what),
            CQH(ask_for_time, pattern=when_time),
        ],
    },
    fallbacks=[CommandHandler('cook', ask_for_meal_name)],  # Only for
    # developpment to know sticker id
)
