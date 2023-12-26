from app.models.question import Question
from sqladmin import ModelView
from sqlalchemy import String


class QuestionAdmin(ModelView, model=Question):
    column_list = [Question.label, Question.event]
    #form_excluded_columns = [Question.input_type]
    form_overrides = dict(input_type=str)
    can_create = False
    can_edit = True
    can_delete = True
    can_view_details = True
    icon = "fa-solid fa-question"
    column_searchable_list = [Question.event]