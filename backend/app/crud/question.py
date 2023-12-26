from typing import TypeVar

from app import models, schemas
from app.crud.base import CRUDBase
from app.db.base_class import Base
from pydantic import BaseModel

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)


class CRUDQuestion(CRUDBase[models.Question, schemas.QuestionCreate, schemas.QuestionUpdate]):
    pass


question = CRUDQuestion(models.Question)