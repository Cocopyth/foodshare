from enum import Enum, auto


class ConversationStage(Enum):
    CHOSING_MEAL = auto()
    CANCELING_PARTICIPATION =auto()
    CANCELING_MEAL = auto()