from typing import Optional

from app.schemas.core import CoreModel


class CommentBase(CoreModel):
    text: Optional[str] = None
    user_id: int
    event_id: int

    class Config:
        orm_mode = True


class CommentCreate(CommentBase):
    pass


class CommentUpdate(CommentBase):
    pass


class CommentResponse(CommentBase):
    id: int
