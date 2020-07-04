from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# association table
meals_users = Table(
    'meals_users',
    Base.metadata,
    Column('meal_id', ForeignKey('users.id'), primary_key=True),
    Column('user_id', ForeignKey('meals.id'), primary_key=True),
)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    telegram_id = Column(String)
    money_balance = Column(Float)
    meal_balance = Column(Float)
    community = relationship("Community", back_populates="members")
    admin = Column(Integer)
    meals = relationship(
        'Meal', secondary=meals_users, back_populates='participants'
    )
    transaction_giver = relationship(
        'Transaction',
        backref="from_whom",
        foreign_keys='Transaction.from_whom_id',
    )
    transaction_receiver = relationship(
        'Transaction', backref="to_whom", foreign_keys='Transaction.to_whom_id'
    )
    message_giver = relationship(
        'Pending_meal_job',
        backref="from_whom",
        foreign_keys='Pending_meal_job.from_whom_id',
    )
    message_receiver = relationship(
        'Pending_meal_job',
        backref="to_whom",
        foreign_keys='Pending_meal_job.to_whom_id',
    )

    def __repr__(self):
        return "<User(name='%s', telegram_id='%s')>" % (
            self.name,
            self.telegram_id,
        )


class Pending_meal_job(Base):
    __tablename__ = 'pending_job'

    id = Column(Integer, primary_key=True)
    meal_id = Column(Integer, ForeignKey('meals.id'))
    meal = relationship("Meal", back_populates='pending_meal_jobs')
    type = Column(Integer)
    from_whom_id = Column(Integer, ForeignKey('users.id'))
    to_whom_id = Column(Integer, ForeignKey('users.id'))
    message_sent = Column(Integer)
    has_answered = Column(Integer)
    answer = Column(Integer)
    job_done = Column(Integer)
    message_id = Column(Integer)

    def __repr__(self):
        return (
            "<Pending_meal_job(type='%s', answer='%s',"
            "from_whom='%s', "
            "to_whom='%s')>"
            % (self.type, self.answer, self.from_whom, self.to_whom)
        )


class Meal(Base):
    __tablename__ = 'meals'

    id = Column(Integer, primary_key=True)
    who_cooks_id = Column(Integer, ForeignKey('users.id'))
    who_cooks = relationship("User", back_populates="meal_where_cook")
    community = relationship("Community", back_populates='meals')
    participants = relationship(
        'User', secondary=meals_users, back_populates='meals'
    )
    pending_meal_jobs = relationship(
        "Pending_meal_job", order_by=Pending_meal_job.id, back_populates='meal'
    )
    what = Column(String)
    when = Column(String)
    how_many = Column(Integer)
    how_much = Column(Float)
    deadline = Column(String)
    is_done = Column(Integer)
    cancelled = Column(Integer)
    additional_info = Column(String)
    confirmation_sent = Column(Integer)

    def __repr__(self):
        return "<Meal(What='%s', participants='%s',how many='%s')>" % (
            self.what,
            self.participants,
            self.how_many,
        )


User.meal_where_cook = relationship(
    "Meal", order_by=Meal.id, back_populates="who_cooks"
)


class Token(Base):
    __tablename__ = 'tokens'
    id = Column(Integer, primary_key=True)
    token = Column(String)
    community = relationship("Community", back_populates='tokens')

    def __repr__(self):
        return "<Tokens(token='%s', community='%s')>" % (
            self.token,
            self.community,
        )


class Community(Base):
    __tablename__ = 'communities'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    access = Column(Integer)
    description = Column(Integer)
    meals = relationship("Meal", order_by=Meal.id, back_populates='community')
    tokens = relationship(
        "Token", order_by=Token.id, back_populates='community'
    )
    members = relationship(
        "User", order_by=User.id, back_populates="community"
    )

    def __repr__(self):
        return "<Community(name='%s', description='%s')>" % (
            self.name,
            self.description,
        )


User.community_id = Column(Integer, ForeignKey('communities.id'))
Meal.community_id = Column(Integer, ForeignKey('communities.id'))
Token.community_id = Column(Integer, ForeignKey('communities.id'))


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    date_time = Column(String)
    what = Column(Integer)
    how_much = Column(Integer)
    community_id = Column(Integer, ForeignKey('communities.id'))
    from_whom_id = Column(Integer, ForeignKey('users.id'))
    to_whom_id = Column(Integer, ForeignKey('users.id'))

    def __repr__(self):
        return (
            "<Transaction(what='%s', how_much='%s',from_whom='%s', "
            "to_whom='%s')>"
            % (self.what, self.how_much, self.from_whom, self.to_whom)
        )
