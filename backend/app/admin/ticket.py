from app.models.ticket import Ticket, TicketOption
from sqladmin import ModelView


class TicketAdmin(ModelView, model=Ticket):
    column_list = [Ticket.code, Ticket.id]
    form_excluded_columns = []
    can_create = False
    can_edit = False
    can_delete = False
    can_view_details = True
    icon = "fa-sharp fa-solid fa-ticket"
    column_searchable_list = [Ticket.code]


class TicketOptionAdmin(ModelView, model=TicketOption):
    column_list = [TicketOption.id, TicketOption.name, TicketOption.price]
    form_excluded_columns = []
    can_create = False
    can_edit = True
    can_delete = True
    can_view_details = True
    icon = "fa-solid fa-dollar-sign"
    column_searchable_list = [TicketOption.name]