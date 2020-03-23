from collections import OrderedDict
from enum import Enum, auto


def get_weekday(date):
    return date.strftime('%A')


class ConversationStage(Enum):
    TYPING_MEAL_NAME = auto()
    SELECTING_WEEKDAY_OR_SHOW_CALENDAR = auto()
    SELECTING_DATE_CALENDAR = auto()
    SELECTING_HOUR = auto()
    SELECTING_NUMBER_OF_PERSON = auto()
    SELECTING_COST = auto()
    SELECTING_REMINDER = auto()
    CONFIRMATION = auto()


def get_message(context, epilog='', highlight=None):
    ud = context.user_data
    message = OrderedDict()

    if 'meal_name' in ud:
        message['meal_name'] = f'🍌 You\'re cooking {ud["meal_name"]}'
    if 'date' in ud:
        date = ud['date']
        message[
            'date'
        ] = f'📆 On {get_weekday(date)} {date.strftime("%d/%m/%Y")}'
    if 'time' in ud:
        time = ud['time']
        message['time'] = f'🕔 At {time.strftime("%H:%M")}'

    if highlight in message.keys():
        message[highlight] = f'*{message[highlight]}*'

    return '\n'.join(message.values()) + f'\n\n{epilog}'
