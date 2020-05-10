from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from foodshare.bdd.tables_declaration import User, Meal, Community, \
    Transaction, Base
absolute_path ='home/coco/db/foodshare_test.db'
engine = create_engine('sqlite:////'+absolute_path, echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def get_user_from_chat_id(chat_id):
    our_user = session.query(User).filter_by(telegram_id=chat_id).first()
    return(our_user)

def add_meal():
    return(None)