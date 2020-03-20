from telegram import InlineKeyboardButton

# Hour keyboard


numbers_emoji = [
    '0️⃣',
    '1⃣',
    '2️⃣',
    '3️⃣',
    '4️⃣',
    '5️⃣',
    '6️⃣',
    '7️⃣',
    '8️⃣',
    '9️⃣',
]


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
