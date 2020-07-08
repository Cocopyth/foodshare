from enum import Enum, auto


class ConversationStage(Enum):
    TYPING_NAME = auto()
    NAME_SAVED = auto()
    JOINING = auto()
    VERIFYING = auto()
    CREATING_JOINING = auto()
    CREATING = auto()
    DESCRIBING = auto()
    CONFIRMING = auto()
