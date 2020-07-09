from enum import Enum, auto


class ConversationStage(Enum):
    ACTION = auto()
    QUITTING = auto()
