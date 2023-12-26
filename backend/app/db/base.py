# Add here your models to be detected by Alembic 
from app.db.base_class import Base
from app.models.event import Event
from app.models.question import Question
from app.models.ticket import Order, Ticket, TicketOption
from app.models.user import User
