from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from foodshare.keyboards.telegram_number import emojify

# Hour keyboard
def create_callback_data(char):
    """ Create the callback data associated to each button"""
    return str(char)


def separate_callback_data(data):
    """ Separate the callback data"""
    return data.split(";")


row1 = []
row2 = []
row3 = []
row1.append(InlineKeyboardButton("7️⃣", callback_data=create_callback_data(7)))
row1.append(InlineKeyboardButton("8️⃣", callback_data=create_callback_data(8)))
row1.append(InlineKeyboardButton("9️⃣", callback_data=create_callback_data(9)))
row2.append(InlineKeyboardButton("4️⃣", callback_data=create_callback_data(4)))
row2.append(InlineKeyboardButton("5️⃣", callback_data=create_callback_data(5)))
row2.append(InlineKeyboardButton("6️⃣", callback_data=create_callback_data(6)))
row3.append(InlineKeyboardButton("1️⃣", callback_data=create_callback_data(1)))
row3.append(InlineKeyboardButton("2️⃣", callback_data=create_callback_data(2)))
row3.append(InlineKeyboardButton("3️⃣", callback_data=create_callback_data(3)))
hour_buttons = [row1, row2, row3]
hour_buttons.append([])
hour_buttons[3].append(
    InlineKeyboardButton("0️⃣", callback_data=create_callback_data(0))
)
hour_buttons[3].append(InlineKeyboardButton("⬅️", callback_data="⬅️"))
hour_buttons[3].append(InlineKeyboardButton("Back", callback_data="➡️"))
cost_keyboard = InlineKeyboardMarkup(hour_buttons)
pos = [0, 5, 11, 17]

numbers = ["0️⃣", "1⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
possibilities = [create_callback_data(i) for i in range(10)] + ["⬅️"+"➡️"+"+"]
def process_cost_selection(update, context):
    ret_data = (False, False, None)
    ud = context.user_data
    bot = context.bot
    query = update.callback_query
    messages = query.message.text.split("\n")
    action = query.data
    if "cost" in ud:
        cost = ud["cost"]
        indexn = ud["indexn"]
    else:
        cost = 0
        ud["cost"] = cost
        indexn = 0
        ud["indexn"] = indexn
#    if action not in possibilities:
#        reply = "\n".join(messages)
#        bot.edit_message_text(
#            text=reply,
#            chat_id=query.message.chat_id,
#            message_id=query.message.message_id,
#            reply_markup=cost_keyboard,
#        )
    if "⬅️" in action:
        indexn = max(0, indexn - 1)
        ud["indexn"] = indexn
        cost = cost // 10
        ud["cost"] = cost
        if cost == 0:
            messages[-1] = "€"
        else:
            messages[-1] = emojify(cost) + "€"
        reply = "\n".join(messages)
        bot.edit_message_text(
            text=reply,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            reply_markup=cost_keyboard,
        )
    elif "➡️" in action:
        ret_data = True, True, cost
    elif "+" in action:
        costf = cost
        ud["cost"] = 0
        indexn = 0
        ud["indexn"] = indexn
        ret_data = True, False, costf
    else:
        costkey = int(action)
        indexn = indexn + 1
        ud["indexn"] = indexn
        cost = 10 * cost + costkey
        ud["cost"] = cost
        messages[-1] = emojify(cost) + "€"
        reply = "\n".join(messages)
        if cost != 0:
            if len(hour_buttons) <= 4:
                hour_buttons.append(
                    [InlineKeyboardButton("Confirm", callback_data="+")]
                )
            new_keyboard = InlineKeyboardMarkup(hour_buttons)
            bot.edit_message_text(
                text=reply,
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                reply_markup=new_keyboard,
            )
        else:
            bot.edit_message_text(
                text=reply,
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                reply_markup=cost_keyboard,
            )
    return ret_data
