import os
from datetime import datetime

from telegram import Bot
from telegram import InlineKeyboardButton as IKB
from telegram import InlineKeyboardMarkup

from foodshare.bdd.database_communication import (
    create_pending_meal_job,
    get_meals,
)
from foodshare.utils import (
    create_meal_message,
    datetime_format,
    emojize_number,
)
from foodshare.utils.gif_test import get_gif_url

bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
bot = Bot(token=bot_token)


def handle_meals():
    from foodshare.bdd.database_communication import session

    meals = get_meals()
    finished = True
    for meal in meals:
        deadline = datetime.strptime(meal.deadline, datetime_format)
        meal_time = datetime.strptime(meal.when, datetime_format)
        coming = [
            pj
            for pj in meal.pending_meal_jobs
            if (pj.answer and not pj.job_done)
        ]
        pending = [
            pj
            for pj in meal.pending_meal_jobs
            if (pj.message_sent and not pj.has_answered and not pj.job_done)
        ]
        community_users = meal.who_cooks.community.members
        # community_users.sort(
        #     key = lambda user : user.meal_balance)
        contacted = [
            pj.to_whom for pj in meal.pending_meal_jobs if pj.message_sent
        ]
        if datetime.now() <= deadline:
            if len(coming) + len(pending) < meal.how_many - 1:
                finished = False
                user = next(
                    (
                        user
                        for user in community_users
                        if user not in (contacted + [meal.who_cooks])
                    ),
                    None,
                )
                if user is not None:
                    suffix = 'Do you want to come?'
                    message = create_meal_message(meal, suffix)
                    keyboard = InlineKeyboardMarkup(
                        [
                            [
                                IKB('Yes', callback_data='secret_key_yes'),
                                IKB('No', callback_data='secret_key_no'),
                            ],
                        ]
                    )
                    gif_url = get_gif_url(meal.what)
                    if gif_url is not None:
                        document_id = bot.send_document(
                            chat_id=user.telegram_id, document=gif_url
                        ).message_id
                    else:
                        document_id = None
                    message_id = bot.send_message(
                        chat_id=user.telegram_id,
                        text=message,
                        reply_markup=keyboard,
                    ).message_id
                    create_pending_meal_job(
                        user, meal.who_cooks, meal, message_id, document_id
                    )
                else:
                    finished = True
        else:  # after the deadline
            if not meal.confirmation_sent:
                send_confirmation(meal)
                meal.confirmation_sent = True
                for pj in coming:
                    user = pj.to_whom

                    user.meal_balance -= 1
                    session.add(user)
                who_cooks = meal.who_cooks
                who_cooks.meal_balance += len(coming)
                session.add(who_cooks)
                session.add(meal)
        if datetime.now() > meal_time:
            meal.is_done = True
            for pj in coming:
                pj.job_done = True
                pj.to_whom.money_balance -= meal.how_much / (len(coming) + 1)
            for pj in pending:
                pj.job_done = True
                session.add(pj)
                session.commit()
                bot.delete_message(
                    chat_id=pj.to_whom.telegram_id, message_id=pj.message_id
                )
                bot.delete_message(
                    chat_id=pj.to_whom.telegram_id, message_id=pj.document_id
                )
                session.add(pj)
            meal.who_cooks.money_balance += meal.how_much * (
                1 - 1 / (len(coming) + 1)
            )
            meal.is_done = True
            session.add(meal)
            session.add(meal.who_cooks)
    session.commit()
    return finished


def send_confirmation(meal):
    coming = [pj for pj in meal.pending_meal_jobs if pj.answer]
    message = (
        f'{len(coming)} people confirmed they will come to your meal:\n'
        f'{create_meal_message(meal)}\n'
        f'Here is the list of the people coming \n'
    )
    message += '\n'.join(
        [
            emojize_number(i + 1) + pj.to_whom.name
            for (i, pj) in enumerate(coming)
        ]
    )
    bot.send_message(chat_id=meal.who_cooks.telegram_id, text=message)


def send_meal_cancellation_notification(meal):
    coming = [pj for pj in meal.pending_meal_jobs if pj.answer]
    pending = [
        pj
        for pj in meal.pending_meal_jobs
        if (pj.message_sent and not pj.has_answered)
    ]
    message_coming = (
        f'Sorry the meal the meal: {create_meal_message(meal)}\n'
        f'was cancelled'
    )
    for pj in coming:
        bot.send_message(chat_id=pj.to_whom.telegram_id, text=message_coming)
    for pj in pending:
        bot.delete_message(
            chat_id=pj.to_whom.telegram_id, message_id=pj.message_id
        )
        bot.delete_message(
            chat_id=pj.to_whom.telegram_id, message_id=pj.document_id
        )


def send_participation_cancellation_notification(chat_id, meal):
    from foodshare.bdd.database_communication import get_user_from_chat_id

    canceller = get_user_from_chat_id(chat_id)
    message = (
        f'User {canceller.name} cancelled his participation to the '
        f'meal {meal.what} on {meal.when}'
    )
    bot.send_message(chat_id=meal.who_cooks.telegram_id, text=message)
