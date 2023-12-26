from datetime import datetime
from typing import List

from app import crud, models, schemas
from app.api.deps import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/create", response_model=List[schemas.TicketResponse])
def create_tickets(data: schemas.TicketCreate, db: Session = Depends(get_db)):
    """
    Creates order and tickets
    """
    event = crud.event.get(db, id=data.event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The event with this ID does not exist in the system.",
        )
    if datetime.now() > event.end_datetime:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event already finished",
        )
    ticket_options_ids = [dic.ticket_option for dic in data.user_tickets]
    ticket_options = db.query(models.TicketOption).filter(
        models.TicketOption.id.in_(ticket_options_ids))
    if not all([to.event_id == event.id for to in ticket_options]):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Specified TicketOption not belong to the requested event",
        )
    return crud.ticket.create(db, obj_in=data)


@router.get("/my-tickets")
def get_tickets(db: Session = Depends(get_db)):
    """
    Get all tickets for a given user
    """
    tickets_data = crud.ticket.get_user_tickets(db, user_id="9a335378-0804-49b1-8fbf-ebb98221ed82")  # TODO: fix this
    results_as_dict = [row._asdict() for row in tickets_data]
    result = {}
    # Group tickets by event, improve me
    for row in results_as_dict:
        if row.get('id').hex not in result.keys():
            result[row.get('id').hex] = {
                'name': row.get('event_name'),
                'start_datetime': row.get('start_datetime').strftime("%d/%m/%Y %H:%M"),
                'tickets': [{
                    'ticket_name': row.get('ticket_name'),
                    'code': row.get('code'),
                }]
            }
        else:
            result[row.get('id').hex]['tickets'].append(
                {
                    'ticket_name': row.get('ticket_name'),
                    'code': row.get('code'),
                }
            )
    return list(result.values())


@router.get("/event-assistants/{event_id}", response_model=List[schemas.UserAssitant])
def get_event_assistants(event_id: int, db: Session = Depends(get_db)):
    """
    Get all assintant to an event
    """
    return crud.ticket.get_event_assistents(db, event_id=event_id)
