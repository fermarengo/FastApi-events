from typing import List, Optional
from uuid import UUID

from app.api.utils.date import get_day_of_week
from app.schemas.core import CoreModel
from pydantic import validator


class TicketOptionBase(CoreModel):
    price: Optional[float]
    name: str = ""
    description: str = ""
    max_limit: Optional[int] = 0

    @validator("name", pre=True)
    def check_name_lenght(cls, value):
        if len(value) > 30:
            raise ValueError('TicketOption name: max length 30 characters')
        return value

    @validator("description", pre=True)
    def check_description_lenght(cls, value):
        if len(value) > 120:
            raise ValueError('TicketOption description: max length 120 characters')
        return value

    class Config:
        orm_mode = True


class TicketOptionResponse(TicketOptionBase):
    id: UUID


class TicketOptionCreate(TicketOptionBase):
    pass


class TicketBase(CoreModel):
    pass

    class Config:
        orm_mode = True


class TicketDescription(CoreModel):
    ticket_option: str
    quantity: int


class TicketCreate(TicketBase):
    event_id: str
    user_tickets: List[TicketDescription]
    user_data: dict

    @validator("user_tickets", pre=True, always=True)
    def check_user_tickets(cls, user_tickets):
        for element in user_tickets:
            assert element.get("quantity") > 0, "quantity must be greater than 0"
        return user_tickets


class TicketResponse(TicketBase):
    name: str
    code: str


class TicketEventResponse(TicketBase):
    ticket_name: str
    code: str
    event_name: str
    start_datetime: str

    @validator("start_datetime", pre=True)
    def parse_start_date(cls, value):
        day_of_week = get_day_of_week(value)
        return f'{day_of_week} {value.strftime("%d/%m/%Y")}'


class TicketUpdate(TicketBase):
    pass
