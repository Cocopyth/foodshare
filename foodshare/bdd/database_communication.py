from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from foodshare.bdd.tables_declaration import User, Meal, Community, \
    Transaction, Base
absolute_path ='home/coco/db/foodshare_test.db'
engine = create_engine('sqlite:////'+absolute_path, echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def add_meal():
    return(None)