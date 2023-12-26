import random
from typing import Any, List
from uuid import UUID

from app import crud, schemas
from app.api.deps import get_db
from app.api.utils.upload_image import validate_and_upload_image
from app.core.config import DEFAULT_EVENT_IMAGES
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/", response_model=List[schemas.EventResponseList])
def get_events(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """
    Retrieve all events.
    """
    events = crud.event.get_multi(db, skip=skip, limit=limit)
    return events


@router.get("/{event_id}", response_model=schemas.EventResponseDetail)
def get_event_detail(
    event_id: UUID,
    db: Session = Depends(get_db)
) -> Any:
    """
    Retrieve event with given event_id
    """
    event = crud.event.get(db=db, id=event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The event with this ID does not exist in the system.",
        )
    return event


@router.post("/", response_model=schemas.EventResponseDetail)
def create_event(
    event_data: schemas.EventCreate,
    db: Session = Depends(get_db)
) -> Any:
    """
    Create new event. 
    Is not posible to send image and a json list in same api endpoint,
    so to upload an image you will nedd to user another endpoint

    https://stackoverflow.com/questions/69292855/why-do-i-get-an-unprocessable-entity-error-while-uploading-an-image-with-fasta
    """
    file_image_name = random.choice(DEFAULT_EVENT_IMAGES)
    event = crud.event.create(db, obj_in=event_data, picture_url=file_image_name)
    return event


@router.post("/{event_id}/upload_image", response_model=schemas.EventResponseList)
def upload_image(
    event_id: UUID,
    uploaded_file: UploadFile = File(...),
    db: Session = Depends(get_db)
) -> Any:
    """
    Upload image for the given event id.
    """
    file_name = validate_and_upload_image(uploaded_file)
    db_obj = crud.event.get(db, id=event_id)
    data = {'picture_url': file_name }
    event = crud.event.update(db, db_obj=db_obj, obj_in=data)
    return event


# @router.put("/", response_model=schemas.EventResponse)
# def update_event(
#     event_external_id: UUID,
#     event_data: schemas.EventCreate = Depends(),
#     db: Session = Depends(get_db),
# ) -> Any:
#     """
#     Update existing event.
#     """
#     db_obj = crud.event.get(db, model_external_id=event_external_id)
#     if not db_obj:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="The event with this ID does not exist in the system.",
#         )
#     event = crud.event.update(db, db_obj=db_obj, obj_in=event_data)
#     return event
