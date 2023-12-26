from datetime import datetime
from typing import List, Optional
from urllib.parse import urljoin
from uuid import UUID

from app.api.utils.date import get_day_of_week
from app.core.config import settings
from app.schemas.core import CoreModel, IDModelMixin
from app.schemas.question import QuestionCreate, QuestionResponse
from app.schemas.ticket import TicketOptionCreate, TicketOptionResponse
from pydantic import validator
from pydantic import root_validator


class EventBase(CoreModel):
    name: str = ""
    location: str = ""
    start_datetime: datetime = datetime.now()
    end_datetime: datetime = datetime.now()

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class EventCreate(EventBase):
    longitude: float
    latitude: float
    description: str = ""
    private: Optional[bool] = False
    ticket_options: List[TicketOptionCreate]
    questions: List[QuestionCreate]
    info_before_confirm_ticket: Optional[str] = ""

    @validator('description', pre=True)
    def description_lenght(cls, v, values, **kwargs):
        if len(v) > 1000:
            raise ValueError('description cannot exceed 1000 characters')
        return v

    @root_validator
    def check_dates(cls, values):
        start_datetime = values['start_datetime']
        end_datetime = values['end_datetime']
        if start_datetime > end_datetime:
            raise ValueError('Fecha de fin no puede ser mayor a fecha de inicio')
        if start_datetime < datetime.now():
            raise ValueError('Fecha de inicio debe ser futura')
        return values

    @validator("name", pre=True)
    def check_name_lenght(cls, value):
        if len(value) > 30:
            raise ValueError('TicketOption name: max length 30 characters')
        return value


class EventResponseList(EventBase):
    id: Optional[UUID]
    picture_url: Optional[str] = ''
    start_datetime_short: Optional[str] = ''
    long_datetime: Optional[str] = ''

    @validator('start_datetime_short', always=True)
    def ab(cls, v, values) -> str:
        value = values['start_datetime']
        day_of_week = get_day_of_week(value)
        return f"{day_of_week} {value.strftime('%d/%m')}"

    @validator("long_datetime", always=True)
    def parse_long_datetime(cls, v, values):
        value = values['start_datetime']
        day_of_week = get_day_of_week(value)
        return f'{day_of_week} {value.strftime("%d/%m/%Y %H:%M")}'

    @validator("end_datetime")
    def parse_end_date(cls, value):
        day_of_week = get_day_of_week(value)
        return f'{day_of_week} {value.strftime("%d/%m/%Y %H:%M")}'

    @validator("picture_url", pre=True)
    def parse_picture_url(cls, value):
        if value is not None:
            value = urljoin(f'{settings.BASE_URL}/{settings.MEDIA_FOLDER}/', value)
        return value


class EventResponseDetail(EventResponseList):
    ticket_options: List[TicketOptionResponse] = []
    questions: List[QuestionResponse] = []
    description: str
    aditional_location_description: Optional[str] = None
    info_before_confirm_ticket: Optional[str]


class EventUpdate(IDModelMixin, EventBase):
    pass



