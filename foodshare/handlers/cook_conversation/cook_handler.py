from telegram.ext import CallbackQueryHandler as CQH
from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    Filters,
    MessageHandler,
)

from foodshare.commands.cook import (
    end,
    inline_calendar_handler,
    inline_cost_handler,
    inline_number_handler,
    inline_time_handler,
    meal_name_confirm,
    reminder_choosing,
    save_input2,
)
from foodshare.keyboards.confirmation_keyboard import confirm, what
from foodshare.keyboards.reminder_keyboard import (
    back2,
    chose,
    pattern_reminder,
)

from . import ConversationStage as CS
from .date import calendar_handler, weekday_handler
from .meal_name import ask_for_meal_name, save_meal_name

cook_handler = ConversationHandler(
    entry_points=[CommandHandler('cook', ask_for_meal_name)],
    states={
        CS.TYPING_MEAL_NAME: [MessageHandler(Filters.text, save_meal_name)],
        CS.SELECTING_DATE: [
            CQH(weekday_handler, pattern='today|tmo|in_2_days'),
            CQH(calendar_handler, pattern='show_calendar'),
            # CQH(ask_for_meal_name, pattern='back'),
        ],
        CS.SELECTING_DATE_CALENDAR: [CQH(inline_calendar_handler)],
        CS.SELECTING_HOUR: [CQH(inline_time_handler)],
        CS.SELECTING_NUMBER: [CQH(inline_number_handler)],
        CS.SELECTING_COST: [CQH(inline_cost_handler)],
        CS.SELECTING_REMINDER: [
            CQH(reminder_choosing, pattern=pattern_reminder),
            CQH(calendar_handler, pattern=f'^{chose}$'),
            CQH(inline_cost_handler, pattern=f'^{back2}$'),
        ],
        CS.CONFIRMATION: [
            MessageHandler(Filters.text, save_input2),
            CQH(end, pattern=confirm),
            CQH(meal_name_confirm, pattern=what),
        ],
    },
    fallbacks=[CommandHandler('start', ask_for_meal_name)],
)
