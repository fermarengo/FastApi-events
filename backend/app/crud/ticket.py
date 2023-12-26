import random
from string import ascii_uppercase, digits
from typing import List, TypeVar

from app import models, schemas
from app.crud.base import CRUDBase
from app.db.base_class import Base
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session, joinedload

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)

LEN_CODE = 7


class CRUDTicket(CRUDBase[models.Ticket, schemas.TicketCreate, schemas.TicketUpdate]):

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)

        order = models.Order(
            user_id="9a335378-0804-49b1-8fbf-ebb98221ed82",                                # TODO: FIX
            number=random.randint(1, 99999)
        )
        db.add(order)
        db.commit()
        db.refresh(order)

        # we create a ticket or entrance for the number that user requested
        tickets_to_bulk = []
        for ticket_option in obj_in_data.get("user_tickets", 0):
            for _ in range(ticket_option.get("quantity", 0)):
                obj_data = {
                    "order_id": order.id,
                    "ticket_option_id": ticket_option.get("ticket_option"),
                    "code": ''.join(random.choices(ascii_uppercase + digits, k=LEN_CODE))
                }
                ticket = models.Ticket(**obj_data)
                tickets_to_bulk.append(ticket)
        db.bulk_save_objects(tickets_to_bulk)
        db.commit()
        
        return db.query(
            models.Ticket.code, models.TicketOption.name
        ).join(
            models.TicketOption.tickets
        ).filter(
            models.Ticket.order_id == order.id
        ).all()

    def get_user_tickets(self, db: Session, user_id: int, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """
        Get all tickets for a given user
        """
        return db.query(
            models.Ticket.code,
            models.TicketOption.name.label('ticket_name'),
            models.Event.name.label('event_name'),
            models.Event.start_datetime,
            models.Event.id
        ).select_from(
            models.Ticket
        ).join(
            models.TicketOption
        ).join(
            models.Event
        ).join(
            models.Order
        ).filter(
            models.Order.user_id == user_id
        ).offset(
            skip
        ).limit(
            limit
        ).all()

    def get_event_assistents(self, db: Session, event_id: int, skip: int = 0, limit: int = 100):
        """
        Get all assitant to an event
        """
        return db.query(
            models.User.full_name,
            models.User.id
        ).select_from(
            models.User
        ).join(
            models.Order
        ).join(
            models.Ticket
        ).join(
            models.TicketOption
        ).distinct(
            models.User.id
        ).filter(
            models.TicketOption.event_id == event_id
        ).offset(
            skip
        ).limit(
            limit
        ).all()


ticket = CRUDTicket(models.Ticket)
