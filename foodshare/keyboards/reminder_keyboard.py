from datetime import timedelta

from telegram import InlineKeyboardButton as IKB
from telegram import InlineKeyboardMarkup

dic_time_deadline = {
    48: [0.5, 3, 6, 24],
    24: [0.5, 1, 3, 6],
    6: [0.5, 1, 2, 3],
    3: [-1, 0.5, 1, 1.5],
    2: [0.5, 1],
    1: [0.5],
}
dict_key_ordered = list(dic_time_deadline.keys())
dict_key_ordered.sort(reverse=True)


def make_labels(time_left):
    for threshold in dict_key_ordered:
        if time_left > threshold:
            return dic_time_deadline[threshold]
    return [-1, -1, -1, -1]


def make_button(label):
    time = str(timedelta(hours=label)).split(':')
    hour, minute = int(time[0]), int(time[1])
    hour_text = f'{hour} h before' if hour > 0 else ''
    minute_text = f'{minute} minutes before' if minute > 0 else ''
    button = IKB(
        text=hour_text + minute_text, callback_data=str(timedelta(hours=label))
    )
    return button


def transform_limit():
    pass


pattern_reminder = ''


def reminder_keyboard_build(time_left):
    labels = make_labels(time_left)
    button_list = []
    for label in labels:
        button_list.append(make_button(label))
    buttons = [button_list[i : i + 2] for i in range(0, len(button_list), 2)]
    buttons.append([IKB(text="Until last minute", callback_data='00:00:00')])
    buttons.append([IKB(text="Back", callback_data='back')])
    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard
