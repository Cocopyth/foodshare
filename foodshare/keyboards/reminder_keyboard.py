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


def make_button(float_hour):
    hour = int(float_hour)
    minute = int(60 * (float_hour - hour))
    hour_text = f'{hour} h ' if hour > 0 else ''
    minute_text = f'{minute} minutes ' if minute > 0 else ''
    button = IKB(
        text=hour_text + minute_text + 'before',
        callback_data=f'{hour}:{minute}',
    )
    return button


def transform_limit():
    pass


pattern_reminder = ''


def reminder_keyboard_build(time_left):
    float_hours = make_labels(time_left)
    button_list = []
    for float_hour in float_hours:
        button_list.append(make_button(float_hour))
    buttons = [
        button_list[i : i + 2]  # noqa : E203 whitespace before ':'
        for i in range(0, len(button_list), 2)
    ]
    buttons.append([IKB(text="Until last minute", callback_data='00:00:00')])
    buttons.append([IKB(text="Back", callback_data='back')])
    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard
