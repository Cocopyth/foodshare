import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from foodshare.bdd.tables_declaration import (
    Base,
    Community,
    Meal,
    Transaction,
    User,
)

absolute_path = (
    os.path.dirname(os.path.abspath(__file__))
    + '/../../../bdd/foodshare_test.db'
)
engine = create_engine('sqlite:////' + absolute_path, echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
community1 = Community(
    name="community1", description="An awesome " "community"
)
community2 = Community(
    name="community2", description="Another awesome " "community"
)

pierre_guilmin = User(name='pierre guilmin', telegram_id='1009446257')
corentin = User(name='corentin bisot', telegram_id='979248731')
tigrou = User(name='pierre tiengou', telegram_id='1195132372')
aurelien = User(name='aurélien gauffre', telegram_id='1162992084')
benoit = User(name='benoit sauty', telegram_id='1225726014')
sophie = User(name='Sophia Melloni', telegram_id='918555937')

pierre_guilmin.community = community2
corentin.community = community1
tigrou.community = community2
aurelien.community = community2
benoit.community = community2
sophie.community = community1

meal1 = Meal(what="pasta")
# meal1.who_cooks = corentin
# meal1.community = meal1.who_cooks.community
# meal1.participants = [pierre_guilmin,tigrou]
# meal2 = Meal(what = "lencils")
# meal2.who_cooks = tigrou
# meal2.community = meal2.who_cooks.community
# meal2.participants = [pierre_guilmin]
# meal3 = Meal(what = "lasagna with ginger")
# meal3.who_cooks = benoit
# meal3.community = meal3.who_cooks.community
# meal3.participants = [aurelien]

transaction1 = Transaction(how_much=1000)
transaction1.from_whom = corentin
transaction1.to_whom = pierre_guilmin
transaction1.community = transaction1.from_whom.community

transaction2 = Transaction(how_much=1000)
transaction1.from_whom = corentin
transaction1.to_whom = tigrou
transaction1.community = transaction1.from_whom.community

session.add_all(
    [
        sophie,
        pierre_guilmin,
        tigrou,
        corentin,
        benoit,
        aurelien,
        community1,
        community2,
        transaction1,
        transaction2,
    ]
)

session.commit()
