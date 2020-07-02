from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from foodshare.bdd.tables_declaration import User, Meal, Community, \
    Transaction, Base
import datetime
absolute_path ='home/coco/db/foodshare_test.db'
engine = create_engine('sqlite:////'+absolute_path, echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
datetime_format = '%Y-%m-%d %H:%M:%S'

def get_user_from_chat_id(chat_id):
    our_user = session.query(User).filter_by(telegram_id=chat_id).first()
    return(our_user)

def get_users_to_contact(who_cooks):
    # members = sorted(who_cooks.community.members,
    #                  key = lambda user: user.meal_balance)
    members = who_cooks.community.members
    return(members)
    # return([who_cooks])

def add_meal(who_cooks, ud):
    meal = Meal(what = ud['meal_name'])
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