from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from foodshare.bdd.tables_declaration import User, Meal, Community, \
    Transaction, Base, Pending_meal_job
from foodshare.bdd.database_communication import  get_users_to_contact
from datetime import datetime
from foodshare.handlers.cook_conversation import create_meal_message
from telegram import InlineKeyboardButton as IKB
from telegram import InlineKeyboardMarkup
from telegram import Bot
import os
absolute_path ='home/coco/db/foodshare_test.db'
engine = create_engine('sqlite:////'+absolute_path, echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
datetime_format = '%Y-%m-%d %H:%M:%S'

bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
bot = Bot(token=bot_token)

def handle_meals():
    meals = session.query(Meal)
    for meal in meals:
        deadline = datetime.strptime(meal.deadline, datetime_format)
        coming = [pj for pj in meal.pending_meal_jobs if
                                 pj.answer]
        pending = [pj for pj in meal.pending_meal_jobs if (pj.message_sent
                                                           and not
                                 pj.has_answered)]
        to_be_contacted = get_users_to_contact(meal.who_cooks)
        if datetime.now() <= deadline:
            if len(coming) + len(pending) <= meal.how_many:
                user = to_be_contacted[0]
                message = create_meal_message(meal)
                keyboard = InlineKeyboardMarkup(
                    [
                        [
                            IKB('Yes', callback_data='secret_key_yes'),
                            IKB('No', callback_data='secret_key_no'),
                        ],
                    ]
                )
                bot.send_message(
                    chat_id=user.telegram_id, text=message,
                    reply_markup=keyboard
                )

def ask_participation(context, to_contact, how_many, meal_info):
    accepted = 0
    refused = 0
    jq = context.job_queue
    job_list = []
    participants = []
    for user in to_contact[:how_many]:
        job_context = {}
        job_context['pot_participant'] = user
        job_context[
            'meal_info'] = meal_info  # there is more info in there than what's
        # needed
        job_context['has_answered'] = False
        job_context['is_coming'] = False
        ask_user_participation(job_context)
    while accepted < how_many - 1:  # how many includes the cook
        for job in job_list:
            if job.context['has_answered']:
                if job.context['is_coming']:
                    accepted += 1
                    participants.append(job.context['pot_participant'])
                    job_list.remove(job)
                else:
                    user = to_contact[how_many + refused]
                    job_context = create_job_context(user)
                    job_list.append(jq.run_once(ask_user_participation,
                                                context=job_context))
        sleep(60)

def ask_user_participation(context):
    bot = context.bot
    job = context.job
    job_context = job.context
    user = job_context['pot_participant']
    meal_info = job_context['meal_info']
    message = create_meal_message(meal_info)
    keyboard = InlineKeyboardMarkup(
        [
            [
                IKB('Yes', callback_data='secret_key_yes'),
                IKB('No', callback_data='secret_key_no'),
            ],
        ]
    )
    bot.send_message(
        chat_id=user.telegram_id, text=message, reply_markup=keyboard
    )