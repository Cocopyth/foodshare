from collections import OrderedDict
from datetime import datetime

from emoji import emojize

from foodshare import datetime_format, get_weekday


def emojize_number(number):
    return ''.join(emojize(f':keycap_{digit}:') for digit in str(number))


def create_meal_message(meal, suffix=''):
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
    if len(meal.additional_info) > 0:
        message2others = meal.additional_info
        message['message2others'] = emojize(
            f'he added the following message : \n' f'*{message2others}*'
        )

    return '\n'.join(message.values()) + '\n' + suffix
