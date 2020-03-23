from telegram.ext import CallbackQueryHandler as CQH
from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    Filters,
    MessageHandler,
)

from foodshare.commands.cook import (
    end,
    meal_name_confirm,
    reminder_choosing,
    save_input2,
)
from foodshare.keyboards.confirmation_keyboard import confirm, what
from foodshare.keyboards.reminder_keyboard import (
    pattern_reminder,
)

from . import ConversationStage as CS
from .cost_selection import cost_selection_handler
from .date_selection import (
    calendar_selection_handler,
    get_date_from_calendar,
    get_date_from_weekday,
)
from .meal_name_choice import ask_for_meal_name, save_meal_name
from .nb_of_person_selection import nb_of_person_selection_handler
from .time_selection import time_selection_handler

cook_handler = ConversationHandler(
    entry_points=[CommandHandler('cook', ask_for_meal_name)],
    states={
        CS.TYPING_MEAL_NAME: [MessageHandler(Filters.text, save_meal_name)],
        CS.SELECTING_WEEKDAY_OR_SHOW_CALENDAR: [
            CQH(get_date_from_weekday, pattern='today|tmo|in_2_days'),
            CQH(get_date_from_calendar, pattern='show_calendar'),
        ],
        CS.SELECTING_DATE_CALENDAR: [CQH(calendar_selection_handler)],
        CS.SELECTING_HOUR: [CQH(time_selection_handler)],
        CS.SELECTING_NB_OF_PERSON: [CQH(nb_of_person_selection_handler)],
        CS.SELECTING_COST: [CQH(cost_selection_handler)],
        CS.SELECTING_REMINDER: [
            CQH(reminder_choosing, pattern=pattern_reminder),
        ],
        CS.CONFIRMATION: [
            MessageHandler(Filters.text, save_input2),
            CQH(end, pattern=confirm),
            CQH(meal_name_confirm, pattern=what),
        ],
    },
    fallbacks=[CommandHandler('start', ask_for_meal_name)],
)
