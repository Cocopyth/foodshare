import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import uuid
from foodshare.bdd.tables_declaration import (
    Base,
    Community,
    Meal,
    Pending_meal_job,
    Token,
    User,
)

absolute_path = 'home/coco/db/foodshare_test.db'
engine = create_engine('sqlite:////' + absolute_path, echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
datetime_format = '%Y-%m-%d %H:%M:%S'


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
    user.money_balance = 0
    user.meal_balance = 0
    user.community = None
    session.add(user)
    session.commit()


def add_community(name, description, chat_id):
    creator = get_user_from_chat_id(chat_id)
    community = Community(name=name, description=description)
    creator.community = community
    creator.admin = 1
    session.add_all([community, creator])
    session.commit()


def add_token(community):
    token_str = uuid.uuid4().hex[:6].upper()
    while session.query(Token).filter_by(token=token_str).first() is not None:
        #to
        # make sure that every token is unique
        token_str = uuid.uuid4().hex[:6].upper()
    token = Token(token=token_str)
    token.community = community
    session.add(token)
    session.commit()
    return(token_str)

def get_token(token_str):
    token = session.query(Token).filter_by(token=token_str).first()
    return(token)

def add_user_to_community(chat_id, token):
    user = get_user_from_chat_id(chat_id)
    community = token.community
    session.delete(token)
    user.community = community
    user.admin = 0
    session.add(user)
    session.commit()
