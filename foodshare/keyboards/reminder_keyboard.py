from datetime import datetime, timedelta

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

short, middle, long, chose, back2 = map(chr, range(5, 10))
pattern_reminder = '^' + short + '$|^' + middle + '$|^' + long + '$'


def make_labels(time_left):
    return ()


def reminder_keyboard_build(time_left):
    if time_left > 48:
        buttons = [
            [
                InlineKeyboardButton(
                    text='30 minutes before', callback_data=short
                ),
                InlineKeyboardButton(
                    text='3 hours before ', callback_data=middle
                ),
            ],
            [
                InlineKeyboardButton(
                    text='24 hours before', callback_data=long
                ),
                InlineKeyboardButton(
                    text='Chose date and hour', callback_data=chose
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Change cost of the meal', callback_data=back2
                )
            ],
        ]
    else:
        buttons = [
            [
                InlineKeyboardButton(
                    text='30 minutes before', callback_data=short
                ),
                InlineKeyboardButton(
                    text='3 hours before ', callback_data=middle
                ),
            ],
            [
                InlineKeyboardButton(
                    text='24 hours before', callback_data=long
                ),
                InlineKeyboardButton(
                    text='Chose date and hour', callback_data=chose
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Change cost of the meal', callback_data=back2
                )
            ],
        ]
    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard


times48 = {short: 0.5, middle: 3, long: 24}


def transform_limit(pushed, time_left):
    if time_left > 48:
        return (
            datetime.now()
            + timedelta(hours=time_left)
            - timedelta(hours=times48[pushed])
        )
    else:
        return (
            datetime.now()
            + timedelta(hours=time_left)
            - timedelta(hours=times48[pushed])
        )
