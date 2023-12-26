from datetime import datetime
from typing import List

from app.db.base_class import Base
from sqlalchemy import Column, Unicode
from sqlmodel import Field, Relationship


class Event(Base, table=True):

    name: str = Field(sa_column=Column(Unicode(255), nullable=False))
    description: str = Field(sa_column=Column(Unicode(500), nullable=False))
    longitude: float = Field(nullable=False)
    latitude: float = Field(nullable=False)
    location: str = Field(sa_column=Column(Unicode(255), nullable=False))
    aditional_location_description: str = Field(sa_column=Column(Unicode(255), nullable=True))
    start_datetime: datetime = Field(nullable=False)
    end_datetime: datetime = Field(nullable=False)
    published: bool = Field(nullable=False, default=True)
    private: bool = Field(nullable=False, default=True)
    picture_url: str = Field(sa_column=Column(Unicode(255), nullable=False))
    info_before_confirm_ticket: str = Field(sa_column=Column(Unicode(255), nullable=True))

    questions: List["Question"] = Relationship(back_populates="event")
    responses: List["Response"] = Relationship(back_populates="event")
    ticket_options: List["TicketOption"] = Relationship(back_populates="event")

    def __repr__(self):
        return self.name

    @property
    def is_active(self):
        now = datetime.now()
        return self.start_datetime > now > self.end_datetime
