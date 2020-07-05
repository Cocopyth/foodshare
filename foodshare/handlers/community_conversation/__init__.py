from collections import OrderedDict
from enum import Enum, auto

from emoji import emojize


class ConversationStage(Enum):
    REGISTERING = auto()
    REGISTERED = auto()
    CREATING_JOINING = auto()
    CREATING = auto()
    DESCRIBING = auto()
    CONFIRMING = auto()
    ACTION = auto()
    JOINING = auto()
    VERIFYING = auto()
    QUITTING = auto()


def get_message(context, epilog='', highlight=None):
    ud = context.user_data
    message = OrderedDict()

    if 'community_name' in ud:
        message['community_name'] = emojize(
            f':family: The name of the community is {ud["community_name"]}'
        )
    if 'community_description' in ud:
        message['description'] = emojize(
            f':desert_island: {ud["community_description"]}'
        )
    if highlight in message.keys():
        message[highlight] = f'*{message[highlight]}*'

    return '\n'.join(message.values()) + f'\n\n{epilog}'
