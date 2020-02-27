from enum import Enum, auto


class ConversationStage(Enum):
    TYPING = auto()
    SELECTING_DATE = auto()
    SELECTING_DATE_CALENDAR = auto()
    SELECTING_HOUR = auto()
    SELECTING_NUMBER = auto()
    SELECTING_COST = auto()
    SELECTING_REMINDER = auto()
    CONFIRMATION = auto()
