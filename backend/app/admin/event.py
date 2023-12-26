from app.models.event import Event
from sqladmin import ModelView


class EventAdmin(ModelView, model=Event):
    column_list = [Event.name, Event.location, Event.start_datetime, Event.end_datetime]
    form_excluded_columns = []
    can_create = False
    can_edit = True
    can_delete = True
    can_view_details = True
    icon = "fa-solid fa-calendar"
    column_searchable_list = [Event.name]
    column_default_sort = [(Event.id, True), (Event.name, True)]
    form_widget_args = {
        "created_at": {
            "readonly": True,
        },
        "updated_at": {
            "readonly": True,
        },
        "ticket_options": {
            "readonly": True,
        }
    }
