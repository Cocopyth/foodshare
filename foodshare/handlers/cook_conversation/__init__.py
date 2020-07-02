from collections import OrderedDict
from enum import Enum, auto

from emoji import emojize

from foodshare.utils import emojize_number

from datetime import datetime

def get_weekday(date):
    return date.strftime('%A')


class ConversationStage(Enum):
    TYPING_MEAL_NAME = auto()
    SELECTING_WEEKDAY_OR_SHOW_CALENDAR = auto()
    SELECTING_DATE_CALENDAR = auto()
    SELECTING_HOUR = auto()
    SELECTING_NB_OF_PERSON = auto()
    SELECTING_COST = auto()
    SELECTING_REMINDER = auto()
    CONFIRMATION = auto()


def get_message(context, epilog='', highlight=None):
    ud = context.user_data
    message = OrderedDict()

    if 'meal_name' in ud:
        message['meal_name'] = emojize(
            f':banana: You\'re cooking {ud["meal_name"]}'
        )
    if 'date' in ud:
        date = ud['date']
        message['date'] = emojize(
            f':calendar: On {get_weekday(date)} {date.strftime("%d/%m/%Y")}'
        )
    if 'time' in ud:
        time = ud['time']
        message['time'] = emojize(f':one-thirty: At {time.strftime("%H:%M")}')
    if 'nb_of_person' in ud:
        message['nb_of_person'] = emojize(
            f':family: For {emojize_number(ud["nb_of_person"])} persons'
        )
    if 'cost' in ud:
        message['cost'] = emojize(
            f':euro_banknote: For {emojize_number(ud["cost"])}€ in total'
        )
    if 'deadline' in ud:
        deadline = ud['deadline']
        message['deadline'] = emojize(
            f'	:alarm_clock: People have until {get_weekday(deadline)} '
            f'{deadline.strftime("%d/%m/%Y at %H:%M")} to answer'
        )
    if 'message2others' in ud:
        message2others = ud['message2others']
        message['message2others'] = emojize(
            f':calling: I will send the following message to people \n'
            f'*{message2others}*'
        )
    if highlight in message.keys():
        message[highlight] = f'*{message[highlight]}*'

    return '\n'.join(message.values()) + f'\n\n{epilog}'

datetime_format = '%Y-%m-%d %H:%M:%S'

def create_meal_message(meal):
    message = OrderedDict()
    who_cooks = meal.who_cooks.name
    message['meal_name'] = emojize(
            f':banana: {who_cooks} is cooking {meal.what}'
        )
    date = meal.when
    date = datetime.strptime(date, datetime_format)
    message['date'] = emojize(
        f':calendar: On {get_weekday(date)} {date.strftime("%d/%m/%Y")}'
    )
    message['time'] = emojize(f':one-thirty: At {date.strftime("%H:%M")}')
    message['nb_of_person'] = emojize(
        f':family: For {emojize_number(meal.how_many)} persons'
    )
    message['cost'] = emojize(
        f':euro_banknote: For {emojize_number(meal.how_much)}€ in total'
    )
    deadline = meal.deadline
    deadline = datetime.strptime(deadline, datetime_format)
    message['deadline'] = emojize(
        f'	:alarm_clock: People have until {get_weekday(deadline)} '
        f'{deadline.strftime("%d/%m/%Y at %H:%M")} to answer'
    )
    if len(meal.additional_info)>0:
        message2others = meal.additional_info
        message['message2others'] = emojize(
            f'he added the following message : \n'
            f'*{message2others}*'
        )

    return '\n'.join(message.values())+'\n Do you want to come?'
