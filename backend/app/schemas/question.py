from typing import Optional
from uuid import UUID

from app.models.question import InputTypes
from app.schemas.core import CoreModel


class QuestionBase(CoreModel):
    label: str = ""
    input_type: InputTypes = InputTypes.text
    order_number: Optional[int]
    is_required: bool = True
    input_placeholder: Optional[str] = ""

    class Config:
        orm_mode = True


class QuestionCreate(QuestionBase):
    pass


class QuestionUpdate(QuestionBase):
    pass


class QuestionResponse(QuestionBase):
    id: UUID