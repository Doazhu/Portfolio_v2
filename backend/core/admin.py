from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse
from markupsafe import Markup
from wtforms import StringField
from wtforms.widgets import TextInput

from core.config import settings
from db.models import Project, Skill, Message, Admin as AdminModel, Settings


class ImageUploadWidget(TextInput):
    """Кастомный виджет для загрузки изображений"""
    
    def __call__(self, field, **kwargs):
        kwargs.setdefault('type', 'text')
        kwargs['class'] = kwargs.get('class', '') + ' form-control'
        kwargs['id'] = field.id
        
        current_value = field.data or ''
        preview_html = ''
        if current_value:
            preview_html = f'''
                <div style="margin-top:10px;">
                    <img src="{current_value}" style="max-height:150px;border-radius:8px;border:1px solid #374151;" 
                         onerror="this.style.display='none'">
                </div>
            '''
        
        return Markup(f'''
            <div class="image-upload-container">
                <div style="display:flex;gap:10px;align-items:center;">
                    <input type="text" name="{field.name}" value="{current_value}" 
                           class="form-control" id="{field.id}" placeholder="/uploads/filename.jpg"
                           style="flex:1;">
                    <label style="background:#6366f1;color:white;padding:8px 16px;border-radius:6px;cursor:pointer;white-space:nowrap;">
                        📤 Загрузить
                        <input type="file" accept="image/*" style="display:none;" 
                               onchange="uploadImage_{field.id}(this)">
                    </label>
                </div>
                <div id="preview_{field.id}">{preview_html}</div>
                <div id="progress_{field.id}" style="display:none;margin-top:10px;">
                    <div style="background:#1f2937;border-radius:4px;overflow:hidden;height:6px;">
                        <div id="progressbar_{field.id}" style="background:#6366f1;height:100%;width:0%;transition:width 0.3s;"></div>
                    </div>
                </div>
            </div>
            <script>
                async function uploadImage_{field.id}(input) {{
                    if (!input.files || !input.files[0]) return;
                    
                    const file = input.files[0];
                    const formData = new FormData();
                    formData.append('file', file);
                    
                    const progress = document.getElementById('progress_{field.id}');
                    const progressBar = document.getElementById('progressbar_{field.id}');
                    const preview = document.getElementById('preview_{field.id}');
                    const urlInput = document.getElementById('{field.id}');
                    
                    progress.style.display = 'block';
                    progressBar.style.width = '30%';
                    
                    try {{
                        const response = await fetch('/api/uploads', {{
                            method: 'POST',
                            body: formData
                        }});
                        
                        progressBar.style.width = '100%';
                        
                        if (response.ok) {{
                            const data = await response.json();
                            urlInput.value = data.url;
                            preview.innerHTML = '<div style="margin-top:10px;"><img src="' + data.url + '" style="max-height:150px;border-radius:8px;border:1px solid #374151;"></div>';
                        }} else {{
                            const err = await response.json();
                            alert('Ошибка: ' + (err.detail || 'Не удалось загрузить'));
                        }}
                    }} catch (e) {{
                        alert('Ошибка загрузки: ' + e.message);
                    }}
                    
                    setTimeout(() => {{ progress.style.display = 'none'; }}, 500);
                }}
            </script>
        ''')


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
            f'<img src="{m.image_url}" style="max-height:50px;border-radius:4px;">'
        ) if m.image_url else "-",
        Project.is_featured: lambda m, a: "⭐" if m.is_featured else "",
        Project.slug: lambda m, a: Markup(f'<code style="color:#6366f1;">{m.slug}</code>') if m.slug else "-",
    }
    
    form_overrides = {
        "image_url": StringField,
    }
    
    form_widget_args = {
        "image_url": {"widget": ImageUploadWidget()},
    }
    
    form_args = {
        "slug": {"description": "Уникальный URL-идентификатор (только a-z, 0-9, -)"},
        "image_url": {"widget": ImageUploadWidget()},
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
