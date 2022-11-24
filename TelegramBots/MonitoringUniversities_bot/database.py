from sqlalchemy.orm import declarative_base
from sqlalchemy import ForeignKey, create_engine, Column, String, Float, Integer, DateTime
from sqlalchemy.orm import sessionmaker

from typing import Union
from datetime import datetime
from aiogram import types


RESPONSES = {
        'successfully': "✅ Успішно",
        'not_successfully': "🚫 Упс... Щось пішло не так"
}

Base = declarative_base()

engine = create_engine('sqlite:///sqlite.db')


class Chat(Base):
    __tablename__ = 'chats'

    id = Column(Integer, primary_key=True, unique=True)
    type = Column(String, default='private')

    def __repr__(self):
        return "<Chat(id=%s, type=%s)>" % (self.id, self.type)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, unique=True)
    k_bal = Column(Float)
    universities = Column(String)
    first_name = Column(String)
    username = Column(String)
    result_view = Column(String, default='without_list')
    created_date = Column(DateTime, default=datetime.now())
    auto_monitoring = Column(String, default="")
    chat_id = Column(Integer, ForeignKey('chats.id'))


    def __repr__(self):
        return "<User(id=%s, k_bal=%s, universities='%s')>" \
                % (self.id, self.k_bal, self.universities)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


async def save_k_bal_to_db(user_data: dict, k_bal: float, chat_data: dict) -> str:
    """Saves k bal to DB"""
    try:
        k_bal = round(float(k_bal), 3)
    except:
        return RESPONSES['not_successfully']
    if not 100 <= k_bal <= 200:
        return RESPONSES['not_successfully']

    chat = session.query(Chat).filter_by(id=chat_data['id']).first()
    if not chat:
        chat = Chat(
                id=chat_data['id'],
                type=chat_data['type']
        )
        session.add(chat)
        session.commit()

    user = session.query(User).filter_by(id=user_data['id']).first()

    try:
        user.k_bal = k_bal
        user.first_name = user_data['first_name']
        user.username = user_data['username']
        user.chat_id = chat.id
        session.commit()
    except:
        user = User(
            id=user_data['id'], 
            k_bal=k_bal, 
            first_name=user_data['first_name'],
            username=user_data['username'],
            chat_id=chat.id
        )
        session.add(user)
        session.commit()

    return RESPONSES['successfully']


async def get_k_bal(user_data: dict) -> Union[float, None]:
    """Gets user k bal"""
    user = session.query(User).filter_by(id=user_data['id']).first()

    try:
        return user.k_bal
    except:
        return None


async def save_universities_to_db(user_data: dict, universities: str, chat_data: dict) -> str:
    """Saves universities to DB"""
    chat = session.query(Chat).filter_by(id=chat_data['id']).first()
    if not chat:
        chat = Chat(
                id=chat_data['id'],
                type=chat_data['type']
        )
        session.add(chat)
        session.commit()

    user = session.query(User).filter_by(id=user_data['id']).first()

    try:
        user.universities = universities
        user.first_name = user_data['first_name']
        user.username = user_data['username']
        user.chat_id = chat.id
        session.commit()
    except:
        user = User(
            id=user_data['id'], 
            universities=universities,
            first_name=user_data['first_name'],
            username=user_data['username'],
            chat_id=chat.id
        )
        session.add(user)
        session.commit()

    return RESPONSES['successfully']


async def get_universities(user_data: dict) -> Union[str, None]:
    """Gets user universities from DB"""
    user = session.query(User).filter_by(id=user_data['id']).first()

    try:
        return user.universities
    except:
        return None


async def change_result_view(user_data: types.user.User, result_view: str) -> str:
    """Changes result view in DB"""
    user = session.query(User).filter_by(id=user_data['id']).first()

    try:
        user.result_view = result_view
        session.commit()
    except:
        user = User(
            id=user_data['id'],
            result_view=result_view
        )
        session.add(user)
        session.commit()

    return result_view


async def get_result_view(user_data: dict) -> str:
    """Gets user result view"""
    user = session.query(User).filter_by(id=user_data['id']).first()

    try:
        return user.result_view
    except:
        return 'without_list'



async def enable_auto_monitoring(user_data: dict, time) -> str:
    """Enables auto monitoring"""
    try:
        hours, minutes = map(int, time.split(':'))
    except:
        return RESPONSES['not_successfully'] + "\nПеревірте формат введення часу"
    if not (00 <= hours <= 23) or not (00 <= minutes <= 59):
        return RESPONSES['not_successfully'] + "\nПеревірте формат введення часу"

    user = session.query(User).filter_by(id=user_data['id']).first()

    user.auto_monitoring = time
    session.commit()

    return RESPONSES['successfully']


async def get_auto_monitoring(user_data: dict) -> str:
    """Gets auto monitoring from DB"""
    user = session.query(User).filter_by(id=user_data['id']).first()

    try:
        return user.auto_monitoring
    except:
        return ""



async def disable_auto_monitoring(user_data: dict) -> str:
    """Disables auto monitoring"""
    user = session.query(User).filter_by(id=user_data['id']).first()

    try:
        user.auto_monitoring = ""
        session.commit()
    except:
        pass

    return RESPONSES['successfully']


async def start_auto_monitoring(time: str):
    """Starts auto monitoring"""
    users = session.query(User).filter_by(auto_monitoring=time).all()

    return users
