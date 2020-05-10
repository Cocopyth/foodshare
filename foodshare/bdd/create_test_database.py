from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from foodshare.bdd.tables_declaration import User, Meal, Community, \
    Transaction, Base
absolute_path ='home/coco/db/foodshare_test.db'
engine = create_engine('sqlite:////'+absolute_path, echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
community1 = Community(name = "community1", description = "An awesome "
                                                          "community")
community2 = Community(name = "community2", description = "Another awesome "
                                                          "community")

pierre_guilmin = User(name='pierre guilmin', telegram_id = 'to complete')
corentin = User(name='corentin bisot', telegram_id = 'to complete')
tigrou = User(name='pierre tiengou', telegram_id = 'to complete')
aurelien = User(name='aurélien gauffre', telegram_id = 'to complete')
benoit = User(name= 'benoit sauty', telegram_id = 'to complete')
pierre_guilmin.community = community1
corentin.community = community1
tigrou.community = community1
aurelien.community = community2
benoit.community = community2

meal1 = Meal(what = "pasta")
meal1.who_cooks = corentin
meal1.community = meal1.who_cooks.community
meal1.participants = [pierre_guilmin,tigrou]
meal2 = Meal(what = "lencils")
meal2.who_cooks = tigrou
meal2.community = meal2.who_cooks.community
meal2.participants = [pierre_guilmin]
meal3 = Meal(what = "lasagna with ginger")
meal3.who_cooks = benoit
meal3.community = meal3.who_cooks.community
meal3.participants = [aurelien]

transaction1 = Transaction(how_much = 1000)
transaction1.from_whom = corentin
transaction1.to_whom = pierre_guilmin
transaction1.community = transaction1.from_whom.community

transaction2 = Transaction(how_much = 1000)
transaction1.from_whom = corentin
transaction1.to_whom = tigrou
transaction1.community = transaction1.from_whom.community

session.add_all([pierre_guilmin,tigrou,corentin,benoit,aurelien,community1,
                community2, meal1, meal2, meal3, transaction1, transaction2]
                )

session.commit()