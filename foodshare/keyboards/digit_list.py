from telegram import InlineKeyboardButton
from emoji import emojize
# Hour keyboard


numbers_emoji = [emojize(f':keycap_{str(i)}:') for i in range(10)]


def emojify_numbers(number):
    return ''.join(numbers_emoji[int(digit)] for digit in str(number))


digits_layout = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

digit_buttons = [
    [
        InlineKeyboardButton(emojify_numbers(x), callback_data=str(x))
        for x in row
    ]
    for row in digits_layout
]
