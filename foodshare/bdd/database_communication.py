import datetime
import uuid

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from foodshare.bdd.tables_declaration import (
    Base,
    Community,
    Meal,
    Pending_meal_job,
    Token,
    Transaction,
    User,
)
from foodshare.utils import datetime_format

absolute_path = 'home/coco/db/foodshare_test.db'
engine = create_engine('sqlite:////' + absolute_path, echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def get_user_from_chat_id(chat_id):
    our_user = session.query(User).filter_by(telegram_id=chat_id).first()
    return our_user


def add_meal(who_cooks, ud):
    meal = Meal(what=ud['meal_name'])
    meal.who_cooks = who_cooks
    meal.community = who_cooks.community
    selected_date, time = ud['date'], ud['time']
    selected_datetime = datetime.datetime.combine(selected_date, time)
    whenstr = selected_datetime.strftime(format=datetime_format)
    meal.when = whenstr
    meal.how_much = ud['cost']
    meal.how_many = ud['nb_of_person']
    meal.deadline = ud['deadline']
    meal.additional_info = ud['message2others']
    meal.is_done = False
    meal.cancelled = False
    meal.pending_meal_jobs = []
    session.add(meal)
    session.commit()


def update_meal(message_id, query_data):
    pending_meal_job = (
        session.query(Pending_meal_job)
        .filter_by(message_id=message_id)
        .first()
    )
    pending_meal_job.has_answered = True
    pending_meal_job.answer = True if query_data == 'secret_key_yes' else False
    session.add(pending_meal_job)
    session.commit()


def add_user(name, chat_id):
    user = User(name=name, telegram_id=chat_id)
    user.community = None
    session.add(user)
    session.commit()


def add_community(name, description, chat_id):
    creator = get_user_from_chat_id(chat_id)
    community = Community(name=name, description=description)
    creator.community = community
    creator.admin = 1
    creator.money_balance = 0
    creator.meal_balance = 0
    session.add_all([community, creator])
    session.commit()


def add_token(community):
    token_str = uuid.uuid4().hex[:6].upper()
    while session.query(Token).filter_by(token=token_str).first() is not None:
        # to
        # make sure that every token is unique
        token_str = uuid.uuid4().hex[:6].upper()
    token = Token(token=token_str)
    token.community = community
    session.add(token)
    session.commit()
    return token_str


def get_token(token_str):
    token = session.query(Token).filter_by(token=token_str).first()
    return token


def add_user_to_community(chat_id, token):
    user = get_user_from_chat_id(chat_id)
    community = token.community
    session.delete(token)
    user.community = community
    user.admin = 0
    user.money_balance = 0
    user.meal_balance = 0
    session.add(user)
    session.commit()


def remove_user_from_community(chat_id):
    user = get_user_from_chat_id(chat_id)
    community = user.community
    user.community = None
    user.admin = 0
    user.money_balance = 0
    user.meal_balance = 0
    session.add(user)
    session.commit()
    if len(community.members) < 1:
        session.delete(community)
    session.commit()


def add_transaction(chat_id, money, to_whom, amount, date_time):
    user = get_user_from_chat_id(chat_id)
    whenstr = date_time.strftime(format=datetime_format)
    transaction = Transaction(date_time=whenstr, what=money, how_much=amount)
    transaction.from_whom = user
    transaction.to_whom = to_whom
    if money:
        user.money_balance -= amount
        to_whom.money_balance += amount
    else:
        user.meal_balance -= amount
        to_whom.meal_balance += amount
    session.add_all([transaction, user, to_whom])
    session.commit()
    if money:
        return user.money_balance
    else:
        return user.meal_balance


def process_meal_action(chat_id, cancel_meal, meal, too_late):
    from foodshare.job_manager.meal_manager import (
        send_meal_cancellation_notification,
        send_participation_cancellation_notification,
    )

    user = get_user_from_chat_id(chat_id)
    if cancel_meal:
        meal.cancelled = True
        coming = [pj for pj in meal.pending_meal_jobs if pj.answer]
        pending = [
            pj
            for pj in meal.pending_meal_jobs
            if (pj.message_sent and not pj.has_answered)
        ]
        for pj in coming:
            pj.job_done = True
            session.add(pj)
        for pj in pending:
            pj.job_done = True
            session.add(pj)
        send_meal_cancellation_notification(meal)
        session.add(meal)
    else:
        job = next((job for job in user.message_receiver if job.meal == meal))
        job.answer = 0
        session.add(job)
        if too_late:
            send_participation_cancellation_notification(chat_id, meal)
    session.commit()


def get_meals():
    return session.query(Meal).filter_by(cancelled=False, is_done=False)


def create_pending_meal_job(user, who_cooks, meal, message_id):
    pending_meal_job = Pending_meal_job(type=0)
    pending_meal_job.message_id = message_id
    pending_meal_job.message_sent = True
    pending_meal_job.has_answered = False
    pending_meal_job.job_done = False

    # normal asking
    pending_meal_job.to_whom = user
    pending_meal_job.from_whom = who_cooks
    pending_meal_job.meal = meal
    session.add(pending_meal_job)
    session.commit()
