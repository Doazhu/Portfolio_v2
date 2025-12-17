from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from markupsafe import Markup

from core.config import settings
from db.models import Project, Skill, Message, Admin as AdminModel, Settings


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
    column_list = [
        Project.id, Project.title, Project.slug, 
        Project.is_featured, Project.order, Project.created_at
    ]
    column_searchable_list = [Project.title, Project.slug, Project.tech_stack]
    column_sortable_list = [Project.id, Project.title, Project.slug, Project.order, Project.created_at]
    column_default_sort = [(Project.order, False)]
    form_excluded_columns = [Project.created_at, Project.updated_at]
    
    column_labels = {
        Project.id: "ID",
        Project.title: "Название",
        Project.slug: "Slug (URL)",
        Project.description: "Описание",
        Project.image_url: "Изображение",
        Project.github_url: "GitHub",
        Project.live_url: "Демо URL",
        Project.tech_stack: "Технологии",
        Project.is_featured: "Избранное",
        Project.order: "Порядок",
        Project.created_at: "Создано",
    }
    
    column_formatters = {
        Project.image_url: lambda m, a: Markup(
            f'<img src="/uploads/{m.image_url.split("/")[-1]}" style="max-height:50px;border-radius:4px;">'
        ) if m.image_url else "-",
        Project.is_featured: lambda m, a: "⭐" if m.is_featured else "",
        Project.slug: lambda m, a: Markup(f'<code style="color:#6366f1;">{m.slug}</code>') if m.slug else "-",
    }
    
    form_args = {
        "slug": {"description": "Уникальный URL-идентификатор (только a-z, 0-9, -)"},
        "image_url": {"description": "Путь к изображению: /uploads/filename.jpg — загрузите через /api/uploads"},
        "live_url": {"description": "URL для поддомена: https://project.doazhu.pro"},
        "tech_stack": {"description": "Через запятую: React, FastAPI, PostgreSQL"},
    }
    
    name = "Проект"
    name_plural = "Проекты"
    icon = "fa-solid fa-folder-open"
    
    page_size = 20
    page_size_options = [10, 20, 50, 100]
    can_export = True
    export_types = ["csv", "json"]


class SkillAdmin(ModelView, model=Skill):
    column_list = [Skill.id, Skill.name, Skill.category, Skill.level, Skill.icon, Skill.order]
    column_searchable_list = [Skill.name, Skill.category]
    column_sortable_list = [Skill.id, Skill.name, Skill.category, Skill.level, Skill.order]
    column_default_sort = [(Skill.order, False)]
    
    column_labels = {
        Skill.id: "ID",
        Skill.name: "Название",
        Skill.category: "Категория",
        Skill.level: "Уровень (%)",
        Skill.icon: "Иконка",
        Skill.order: "Порядок",
    }
    
    column_formatters = {
        Skill.level: lambda m, a: Markup(
            f'<div style="background:#1f2937;border-radius:4px;overflow:hidden;width:100px;">'
            f'<div style="background:linear-gradient(90deg,#6366f1,#a855f7);width:{m.level}%;height:8px;"></div>'
            f'</div> <span style="color:#9ca3af;">{m.level}%</span>'
        ),
    }
    
    form_args = {
        "level": {"description": "От 0 до 100"},
        "icon": {"description": "CSS класс иконки: fa-brands fa-react"},
    }
    
    name = "Навык"
    name_plural = "Навыки"
    icon = "fa-solid fa-code"


class MessageAdmin(ModelView, model=Message):
    column_list = [Message.id, Message.name, Message.email, Message.subject, Message.is_read, Message.created_at]
    column_searchable_list = [Message.name, Message.email, Message.subject]
    column_sortable_list = [Message.id, Message.created_at, Message.is_read]
    column_default_sort = [(Message.created_at, True)]
    
    column_labels = {
        Message.id: "ID",
        Message.name: "Имя",
        Message.email: "Email",
        Message.subject: "Тема",
        Message.message: "Сообщение",
        Message.is_read: "Прочитано",
        Message.created_at: "Дата",
    }
    
    column_formatters = {
        Message.is_read: lambda m, a: "✓" if m.is_read else Markup('<span style="color:#ef4444;">●</span> Новое'),
        Message.email: lambda m, a: Markup(f'<a href="mailto:{m.email}" style="color:#6366f1;">{m.email}</a>'),
    }
    
    can_create = False
    can_delete = True
    can_edit = True
    
    name = "Сообщение"
    name_plural = "Сообщения"
    icon = "fa-solid fa-envelope"


class SettingsAdmin(ModelView, model=Settings):
    column_list = [Settings.id, Settings.key, Settings.value, Settings.description]
    column_searchable_list = [Settings.key]
    
    column_labels = {
        Settings.id: "ID",
        Settings.key: "Ключ",
        Settings.value: "Значение",
        Settings.description: "Описание",
    }
    
    column_formatters = {
        Settings.key: lambda m, a: Markup(f'<code style="color:#22c55e;">{m.key}</code>'),
    }
    
    name = "Настройка"
    name_plural = "Настройки"
    icon = "fa-solid fa-gear"


def setup_admin(app, engine):
    auth = AdminAuth(secret_key=settings.SECRET_KEY)
    admin = Admin(
        app,
        engine,
        authentication_backend=auth,
        title="Doazhu Portfolio",
        base_url="/admin",
    )
    admin.add_view(ProjectAdmin)
    admin.add_view(SkillAdmin)
    admin.add_view(MessageAdmin)
    admin.add_view(SettingsAdmin)
    return admin
