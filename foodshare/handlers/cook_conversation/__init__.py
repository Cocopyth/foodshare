from collections import OrderedDict
from enum import Enum, auto


def get_weekday(date):
    return date.strftime('%A')


class ConversationStage(Enum):
    TYPING_MEAL_NAME = auto()
    SELECTING_DATE = auto()
    SELECTING_DATE_CALENDAR = auto()
    SELECTING_HOUR = auto()
    SELECTING_NUMBER = auto()
    SELECTING_COST = auto()
    SELECTING_REMINDER = auto()
    CONFIRMATION = auto()


def get_message(context, question='', highlight=None):
    ud = context.user_data
    message = OrderedDict()

    if 'meal_name' in ud:
        message['meal_name'] = f'🍌 You\'re cooking {ud["meal_name"]}'
    if 'date' in ud:
        date = ud['date']
        date_format = '%d/%m/%Y'
        # if 'hour_selected' in ud:
        #     date_format += ' at %H:%M'
        message[
            'date'
        ] = f'📆 On {get_weekday(date)} {date.strftime(date_format)}'

    if highlight in message.keys():
        message[highlight] = f'*{message[highlight]}*'

    return '\n'.join(message.values()) + f'\n\n{question}'
