from typing import Any, List

from app import crud, schemas
from app.api.deps import get_db
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/", response_model=List[schemas.QuestionResponse])
def create_event_questions(
    event_id: str,
    questions: List[schemas.QuestionCreate],
    db: Session = Depends(get_db)
) -> Any:
    """
    Create inputs that would be requested to final user before get the tickets:
    For example, ask to user:
    first_name,
    last_name,
    age
    """
    questions = jsonable_encoder(questions)
    questions_data = [{**item, 'event_id': event_id} for item in questions]
    questions = crud.question.bulk_create(db, objects_in_json=questions_data)
    return questions