from enum import Enum, auto


class ConversationStage(Enum):
    TYPING_MEAL_NAME = auto()
    SELECTING_DATE = auto()
    SELECTING_DATE_CALENDAR = auto()
    SELECTING_HOUR = auto()
    SELECTING_NUMBER = auto()
    SELECTING_COST = auto()
    SELECTING_REMINDER = auto()
    CONFIRMATION = auto()
