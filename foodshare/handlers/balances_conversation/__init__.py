from enum import Enum, auto


class ConversationStage(Enum):
    MONEY_OR_MEAL = auto()
    REGISTERING = auto()
    SELECTING_USER = auto()
