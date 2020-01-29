def reminder_keyboard_build(time_left):
    if time left > 6:
        buttons = [
    [
        InlineKeyboardButton(text="30 minutes before", callback_data=Today),
        InlineKeyboardButton(text="3 hours before ", callback_data=Tomorrow),
    ],
    [
        InlineKeyboardButton(text="On "+weekdayp2, callback_data=Dayp2),
        InlineKeyboardButton(text="Show calendar", callback_data=Calendargo),
    ],
    [InlineKeyboardButton(text="Change cost of the meal", callback_data=back)],
    ]
    keyboard = InlineKeyboardMarkup(buttons)