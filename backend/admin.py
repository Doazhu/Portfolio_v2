from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from config import settings
from models import Project, Skill, Message, Admin as AdminModel, Settings


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username", "")
        password = form.get("password", "")

        if username == settings.ADMIN_USERNAME and password == settings.ADMIN_PASSWORD:
            request.session.update({"admin": True})
            return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        return request.session.get("admin", False)


class ProjectAdmin(ModelView, model=Project):
    column_list = [Project.id, Project.title, Project.is_featured, Project.order, Project.created_at]
    column_searchable_list = [Project.title, Project.tech_stack]
    column_sortable_list = [Project.id, Project.title, Project.order, Project.created_at]
    column_default_sort = [(Project.order, False)]
    form_excluded_columns = [Project.created_at]
    name = "Проект"
    name_plural = "Проекты"
    icon = "fa-solid fa-folder-open"


class SkillAdmin(ModelView, model=Skill):
    column_list = [Skill.id, Skill.name, Skill.category, Skill.level, Skill.order]
    column_searchable_list = [Skill.name, Skill.category]
    column_sortable_list = [Skill.id, Skill.name, Skill.category, Skill.order]
    column_default_sort = [(Skill.order, False)]
    name = "Навык"
    name_plural = "Навыки"
    icon = "fa-solid fa-code"


class MessageAdmin(ModelView, model=Message):
    column_list = [Message.id, Message.name, Message.email, Message.subject, Message.is_read, Message.created_at]
    column_searchable_list = [Message.name, Message.email, Message.subject]
    column_sortable_list = [Message.id, Message.created_at, Message.is_read]
    column_default_sort = [(Message.created_at, True)]
    can_create = False
    name = "Сообщение"
    name_plural = "Сообщения"
    icon = "fa-solid fa-envelope"


class SettingsAdmin(ModelView, model=Settings):
    column_list = [Settings.id, Settings.key, Settings.value, Settings.description]
    column_searchable_list = [Settings.key]
    name = "Настройка"
    name_plural = "Настройки"
    icon = "fa-solid fa-gear"


def setup_admin(app, engine):
    auth = AdminAuth(secret_key=settings.SECRET_KEY)
    admin = Admin(
        app,
        engine,
        authentication_backend=auth,
        title="Doazhu Admin",
        base_url="/admin"
    )
    admin.add_view(ProjectAdmin)
    admin.add_view(SkillAdmin)
    admin.add_view(MessageAdmin)
    admin.add_view(SettingsAdmin)
    return admin
