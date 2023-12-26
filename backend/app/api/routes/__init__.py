from app.api.routes.events import router as events_router
from app.api.routes.question import router as questions_router
from app.api.routes.tickets import router as tickets_router
from fastapi import APIRouter

router = APIRouter()

router.include_router(events_router, prefix="/events", tags=["Events"])
router.include_router(tickets_router, prefix="/tickets", tags=["Tickets"])
router.include_router(questions_router, prefix="/questions", tags=["Questions"])
