from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from foodshare.bdd.tables_declaration import User, Meal, Community, \
    Transaction, Base, Pending_meal_job
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
        print('coming=', coming, 'pending=', pending)
        community_users = meal.who_cooks.community.members
        # community_users.sort(
        #     key = lambda user : user.meal_balance)
        contacted = [pj.to_whom for pj in meal.pending_meal_jobs if pj.message_sent]
        if datetime.now() <= deadline:
            if len(coming) + len(pending) <= meal.how_many:
                user = next((user for user in community_users if user not in
                 contacted), None)
                if user != None:
                    pending_meal_job = Pending_meal_job(type=0) #type 0 for
                    # normal asking
                    pending_meal_job.to_whom = user
                    pending_meal_job.from_whom = meal.who_cooks
                    pending_meal_job.meal = meal
                    message = create_meal_message(meal)
                    keyboard = InlineKeyboardMarkup(
                        [
                            [
                                IKB('Yes',
                                    callback_data='secret_key_yes'),
                                IKB('No', callback_data='secret_key_no'),
                            ],
                        ]
                    )
                    message_id=bot.send_message(
                        chat_id=user.telegram_id, text=message,
                        reply_markup=keyboard
                    ).message_id
                    pending_meal_job.message_id = message_id
                    pending_meal_job.message_sent = True
                    pending_meal_job.has_answered = False
                    pending_meal_job.job_done = False
                    session.add(pending_meal_job)
                    session.commit()
                return(False)
            else:
                return(True)
