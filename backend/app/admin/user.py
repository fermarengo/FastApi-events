from app.models.user import User
from sqladmin import ModelView


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email, User.full_name, User.is_admin]
    can_create = True
    can_edit = True
    can_delete = False
    can_view_details = True
    icon = "fa-solid fa-user"
    column_searchable_list = [User.email, User.full_name]
    column_default_sort = [(User.id, True), (User.full_name, True)]
    form_excluded_columns = [User.password, User.orders]