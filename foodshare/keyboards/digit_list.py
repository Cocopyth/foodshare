from telegram import InlineKeyboardButton

from foodshare.utils import emojize_number

digits_layout = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

digit_buttons = [
    [
        InlineKeyboardButton(emojize_number(x), callback_data=str(x))
        for x in row
    ]
    for row in digits_layout
]
