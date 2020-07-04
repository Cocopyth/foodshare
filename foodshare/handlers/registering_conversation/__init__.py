from enum import Enum, auto


class ConversationStage(Enum):
    TYPING_NAME = auto()
    NAME_SAVED = auto()
