import uuid
from typing import List, Optional

from app.db.base_class import Base
from sqlalchemy import Column, Unicode
from sqlmodel import Field, Relationship


class TicketOption(Base, table=True):
    """
    This model respresent the diferent type of tickets.
    For example, "General Ticket" , "Camp Ticket", "VIP Ticket"
    Those kind of entrance can have a maximum number of tickets that can be sold.

    Use price = 0 for free tickets.
    """
    __tablename__ = 'ticket_option'

    order_number: int = Field(nullable=True)
    price: float = Field(nullable=False)
    name: str = Field(sa_column=Column(Unicode(30), nullable=False))
    description: str = Field(sa_column=Column(Unicode(120), nullable=True))
    max_limit: int = Field(nullable=True)

    event_id: uuid.UUID = Field(foreign_key="event.id", nullable=False)
    event: Optional["Event"] = Relationship(back_populates="ticket_options")

    tickets: List["Ticket"] = Relationship(back_populates="ticket_options")

    def __repr__(self):
        return f"Ticket: {self.name} | Event: {self.event.name}"


class Ticket(Base, table=True):
    """
    This model represent the entrance itself
    """
    code: str = Field(sa_column=Column(Unicode(7), nullable=False, unique=True))

    ticket_option_id: uuid.UUID = Field(foreign_key="ticket_option.id", nullable=False)
    ticket_options: Optional["TicketOption"] = Relationship(back_populates="tickets")

    order_id: uuid.UUID = Field(foreign_key="order.id", nullable=False)
    order: Optional["Order"] = Relationship(back_populates="tickets")


class Order(Base, table=True):
    """
    Reprensent a purchase of a user,
    An order can have multiple tickets requested by the user.
    """
    number: str= Field(index=True, unique=True)
    
    tickets: List["Ticket"] = Relationship(back_populates="order")

    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    user: Optional["User"] = Relationship(back_populates="orders")
