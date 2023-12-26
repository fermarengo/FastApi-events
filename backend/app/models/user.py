from typing import List

from app.db.base_class import Base
from sqlalchemy import Column, Unicode
from sqlmodel import Field, Relationship


class User(Base, table=True):

    password: str = Field(sa_column=Column(Unicode(255)), nullable=False)
    email: str = Field(sa_column=Column(Unicode(255)), nullable=False)
    nickname: str = Field(sa_column=Column(Unicode(255)), nullable=True)
    full_name: str = Field(sa_column=Column(Unicode(255)), nullable=True)
    is_admin: bool = Field(default=False)

    orders: List["Order"] = Relationship(back_populates="user")

    def __repr__(self):
        return "<User(id='%s', email='%s', full_name='%s'>" % (self.id, self.email, self.full_name)
