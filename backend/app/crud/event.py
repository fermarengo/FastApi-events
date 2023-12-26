from datetime import datetime
from typing import List, TypeVar

from app import models, schemas
from app.crud.base import CRUDBase
from app.db.base_class import Base
from app.models.question import Question
from app.models.ticket import TicketOption
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)


class CRUDEvent(CRUDBase[models.Event, schemas.EventCreate, schemas.EventUpdate]):

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return db.query(self.model).filter(
            models.Event.end_datetime >= datetime.now()
        ).offset(
            skip
        ).limit(
            limit
        ).all()

    def create(self,
               db: Session,
               obj_in: CreateSchemaType,
               picture_url: str = None
               ) -> ModelType:

        
        obj_in_data = jsonable_encoder(obj_in)
        ticket_options = obj_in_data.pop('ticket_options')
        questions = obj_in_data.pop('questions')

        # Create event object
        db_obj = self.model(**obj_in_data, picture_url=picture_url)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        # Create related ticket optios
        tickets_options_to_bulk = []
        for ticket_op in ticket_options:
            ticket_op['event_id'] = db_obj.id.hex
            ticket = TicketOption(**ticket_op)
            tickets_options_to_bulk.append(ticket)
        db.add_all(tickets_options_to_bulk)
        db.commit()

        # Create data requested to user when create event
        questions_to_bulk = []
        for question in questions:
            question['event_id'] = db_obj.id.hex
            question_obj = Question(**question)
            questions_to_bulk.append(question_obj)
        db.add_all(questions_to_bulk)
        db.commit()

        return db_obj


event = CRUDEvent(models.Event)
