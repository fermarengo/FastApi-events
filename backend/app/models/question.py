
import enum
import uuid
from typing import List, Optional

from app.db.base_class import Base
from sqlalchemy import Column, Enum
from sqlmodel import Field, Relationship

"""
Those models reprensent the user data requested in order to get the tickets entrance. 
Each event can request diffrent data to the users.

For example: an event can request only the the full name of the user 
an another event can request more details like email, location, street, birth_date.
So we need to support dynamic questions.
"""

class InputTypes(enum.Enum):
    date = 'Date'
    text = 'Text'
    boolean = 'Boolean'
    number = 'Number'
    long_text = 'LongText'
    select = 'select' # Not abailable yet


class Question(Base, table=True):
    input_type: InputTypes = Field(     # Used to create the html input
        sa_column=Column(Enum(InputTypes)),
        default=InputTypes.text,
        nullable=False
    ) 
    label: str = Field(nullable=False)
    order_number: int = Field(nullable=True)
    is_required: bool = Field(default=True) # User cannot get tickets without complete the question
    input_placeholder: str = Field(nullable=True)

    event_id: uuid.UUID = Field(foreign_key="event.id")
    event: Optional["Event"] = Relationship(back_populates="questions")

    response: List["Response"] = Relationship(back_populates="question")

    def __str__(self):
        return f"<Question>: {self.label}"


class Response(Base, table=True):
    response_text: str = Field(nullable=False)
    
    event_id: uuid.UUID = Field(foreign_key="event.id")
    event: Optional["Event"] = Relationship(back_populates="responses")

    question_id: uuid.UUID = Field(foreign_key="question.id")
    question: Optional["Question"] = Relationship(back_populates="response")
