from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    Filters,
    MessageHandler,
)

from foodshare.commands.cook import (
    Calendargo,
    back,
    calendar_handler,
    date_handler,
    end,
    inline_calendar_handler,
    inline_cost_handler,
    inline_number_handler,
    inline_time_handler,
    meal_name,
    meal_name_confirm,
    pattern_date,
    reminder_choosing,
    save_input,
    save_input2,
)
from foodshare.keyboards.confirmation_keyboard import confirm, what
from foodshare.keyboards.reminder_keyboard import (
    back2,
    chose,
    pattern_reminder,
)

from . import ConversationStage

cook_handler = ConversationHandler(
    entry_points=[CommandHandler('cook', meal_name)],
    states={
        ConversationStage.TYPING_MEAL_NAME: [
            MessageHandler(Filters.text, save_input)
        ],
        ConversationStage.SELECTING_DATE: [
            CallbackQueryHandler(date_handler, pattern=pattern_date),
            CallbackQueryHandler(calendar_handler, pattern=f'^{Calendargo}$'),
            CallbackQueryHandler(meal_name, pattern=f'^{back}$'),
        ],
        ConversationStage.SELECTING_DATE_CALENDAR: [
            CallbackQueryHandler(inline_calendar_handler)
        ],
        ConversationStage.SELECTING_HOUR: [
            CallbackQueryHandler(inline_time_handler)
        ],
        ConversationStage.SELECTING_NUMBER: [
            CallbackQueryHandler(inline_number_handler)
        ],
        ConversationStage.SELECTING_COST: [
            CallbackQueryHandler(inline_cost_handler)
        ],
        ConversationStage.SELECTING_REMINDER: [
            CallbackQueryHandler(reminder_choosing, pattern=pattern_reminder),
            CallbackQueryHandler(calendar_handler, pattern=f'^{chose}$'),
            CallbackQueryHandler(inline_cost_handler, pattern=f'^{back2}$'),
        ],
        ConversationStage.CONFIRMATION: [
            MessageHandler(Filters.text, save_input2),
            CallbackQueryHandler(end, pattern=confirm),
            CallbackQueryHandler(meal_name_confirm, pattern=what),
        ],
    },
    fallbacks=[CommandHandler('start', meal_name)],
)
