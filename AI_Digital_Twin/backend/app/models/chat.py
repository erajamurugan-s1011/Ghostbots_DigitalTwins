from sqlalchemy import Column,Integer,String
from app.database import Base


class Chat(Base):

    __tablename__="chats"

    id=Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_email=Column(
        String
    )

    question=Column(
        String
    )

    answer=Column(
        String
    )