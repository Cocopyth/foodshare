import os
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from telegram import Bot
from telegram import InlineKeyboardButton as IKB
from telegram import InlineKeyboardMarkup

from foodshare.bdd.tables_declaration import Base, Meal, Pending_meal_job
from foodshare.utils import create_meal_message, datetime_format

absolute_path = 'home/coco/db/foodshare_test.db'
engine = create_engine('sqlite:////' + absolute_path, echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
bot = Bot(token=bot_token)


def handle_meals():
    meals = session.query(Meal).filter_by(cancelled=False, is_done=False)
    finished = True
    for meal in meals:
        deadline = datetime.strptime(meal.deadline, datetime_format)
        coming = [pj for pj in meal.pending_meal_jobs if pj.answer]
        pending = [
            pj
            for pj in meal.pending_meal_jobs
            if (pj.message_sent and not pj.has_answered)
        ]
        print('coming=', coming)
        print('pending=', pending)
        community_users = meal.who_cooks.community.members
        # community_users.sort(
        #     key = lambda user : user.meal_balance)
        contacted = [
            pj.to_whom for pj in meal.pending_meal_jobs if pj.message_sent
        ]
        if datetime.now() <= deadline:
            if len(coming) + len(pending) < meal.how_many:
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
                    pending_meal_job = Pending_meal_job(type=0)  # type 0 for
                    # normal asking
                    pending_meal_job.to_whom = user
                    pending_meal_job.from_whom = meal.who_cooks
                    pending_meal_job.meal = meal
                    message = create_meal_message(meal)
                    keyboard = InlineKeyboardMarkup(
                        [
                            [
                                IKB('Yes', callback_data='secret_key_yes'),
                                IKB('No', callback_data='secret_key_no'),
                            ],
                        ]
                    )
                    message_id = bot.send_message(
                        chat_id=user.telegram_id,
                        text=message,
                        reply_markup=keyboard,
                    ).message_id
                    pending_meal_job.message_id = message_id
                    pending_meal_job.message_sent = True
                    pending_meal_job.has_answered = False
                    pending_meal_job.job_done = False
                    session.add(pending_meal_job)
                    session.commit()
                else:
                    finished = True
        else:
            if not meal.confirmation_sent:
                send_confirmation(meal)
                meal.confirmation_sent = True
                session.add(meal)
                session.commit()
    return finished


def send_confirmation(meal):
    coming = [pj for pj in meal.pending_meal_jobs if pj.answer]
    message = (
        f'{len(coming)} people confirmed they will come to your meal'
        f'at {meal.when}. \n'
        f'Here is the list of the people coming '
        f'{[pj.to_whom for pj in coming]}'
    )
    bot.send_message(chat_id=meal.who_cooks.telegram_id, text=message)
