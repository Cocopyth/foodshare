from enum import Enum, auto


class ConversationStage(Enum):
    SELECTING_DATE = auto()
    TYPING = auto()
    SELECTING_DATE_CALENDAR = auto()
    NUMBER_SELECTION = auto()
    SELECTING_HOUR = auto()
    SELECTING_NUMBER = auto()
    SELECTING_COST = auto()
    SELECTING_REMINDER = auto()
    CONFIRMATION = auto()
