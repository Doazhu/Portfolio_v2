from sqladmin import Admin, ModelView, BaseView, expose
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse
from markupsafe import Markup
from wtforms import StringField, TextAreaField
from wtforms.widgets import TextInput

from core.config import settings
from db.models import Project, Skill, Message, Admin as AdminModel, Settings, GalleryImage
from core.widgets import TypeSelectorWidget, CodeEditorWidget, StatusToggleWidget, ZipUploadWidget


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
            </div>
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


# Preview modal HTML/CSS/JS for iframe preview
# Requirements: 3.2
PREVIEW_MODAL_HTML = """
<style>
.preview-modal-overlay {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.8);
    z-index: 10000;
    backdrop-filter: blur(4px);
}
.preview-modal-overlay.active {
    display: flex;
    align-items: center;
    justify-content: center;
}
.preview-modal {
    background: #1f2937;
    border-radius: 12px;
    width: 90%;
    max-width: 1200px;
    height: 85vh;
    display: flex;
    flex-direction: column;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    border: 1px solid #374151;
}
.preview-modal-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 20px;
    border-bottom: 1px solid #374151;
    background: #111827;
    border-radius: 12px 12px 0 0;
}
.preview-modal-title {
    display: flex;
    align-items: center;
    gap: 12px;
    color: #e5e7eb;
    font-size: 1.1rem;
    font-weight: 600;
}
.preview-modal-title .type-badge {
    font-size: 0.75rem;
    padding: 4px 10px;
    border-radius: 4px;
    font-weight: 500;
}
.preview-modal-title .type-badge.static {
    background: #6366f1;
    color: white;
}
.preview-modal-title .type-badge.external {
    background: #8b5cf6;
    color: white;
}
.preview-modal-actions {
    display: flex;
    gap: 10px;
}
.preview-modal-btn {
    background: #374151;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
    color: #e5e7eb;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.875rem;
    transition: all 0.2s ease;
}
.preview-modal-btn:hover {
    background: #4b5563;
}
.preview-modal-btn.close {
    background: #dc2626;
}
.preview-modal-btn.close:hover {
    background: #b91c1c;
}
.preview-modal-body {
    flex: 1;
    padding: 0;
    overflow: hidden;
}
.preview-modal-body iframe {
    width: 100%;
    height: 100%;
    border: none;
    background: white;
}
.preview-loading {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    color: #9ca3af;
}
.preview-loading i {
    font-size: 2rem;
    animation: spin 1s linear infinite;
}
@keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}
</style>
<div id="previewModalOverlay" class="preview-modal-overlay" onclick="closePreviewModal(event)">
    <div class="preview-modal" onclick="event.stopPropagation()">
        <div class="preview-modal-header">
            <div class="preview-modal-title">
                <i class="fa-solid fa-eye"></i>
                <span id="previewModalTitle">Project Preview</span>
                <span id="previewModalTypeBadge" class="type-badge"></span>
            </div>
            <div class="preview-modal-actions">
                <button class="preview-modal-btn" onclick="openInNewTab()" title="Open in new tab">
                    <i class="fa-solid fa-external-link-alt"></i>
                    New Tab
                </button>
                <button class="preview-modal-btn" onclick="refreshPreview()" title="Refresh preview">
                    <i class="fa-solid fa-sync-alt"></i>
                    Refresh
                </button>
                <button class="preview-modal-btn close" onclick="closePreviewModal()">
                    <i class="fa-solid fa-times"></i>
                    Close
                </button>
            </div>
        </div>
        <div class="preview-modal-body">
            <div id="previewLoading" class="preview-loading">
                <i class="fa-solid fa-spinner"></i>
            </div>
            <iframe id="previewIframe" style="display:none;" onload="onPreviewLoad()"></iframe>
        </div>
    </div>
</div>
<script>
let currentPreviewId = null;
let currentPreviewUrl = null;
function openPreviewModal(projectId, title, projectType) {
    currentPreviewId = projectId;
    currentPreviewUrl = '/admin/api/preview/' + projectId;
    document.getElementById('previewModalTitle').textContent = title;
    const badge = document.getElementById('previewModalTypeBadge');
    badge.textContent = projectType === 'static' ? '📦 Static' : '🔗 External';
    badge.className = 'type-badge ' + projectType;
    document.getElementById('previewLoading').style.display = 'flex';
    document.getElementById('previewIframe').style.display = 'none';
    document.getElementById('previewModalOverlay').classList.add('active');
    document.getElementById('previewIframe').src = currentPreviewUrl;
    document.body.style.overflow = 'hidden';
}
function closePreviewModal(event) {
    if (event && event.target !== document.getElementById('previewModalOverlay')) {
        return;
    }
    document.getElementById('previewModalOverlay').classList.remove('active');
    document.getElementById('previewIframe').src = '';
    currentPreviewId = null;
    currentPreviewUrl = null;
    document.body.style.overflow = '';
}
function onPreviewLoad() {
    document.getElementById('previewLoading').style.display = 'none';
    document.getElementById('previewIframe').style.display = 'block';
}
function refreshPreview() {
    if (currentPreviewUrl) {
        document.getElementById('previewLoading').style.display = 'flex';
        document.getElementById('previewIframe').style.display = 'none';
        document.getElementById('previewIframe').src = currentPreviewUrl;
    }
}
function openInNewTab() {
    if (currentPreviewUrl) {
        window.open(currentPreviewUrl, '_blank');
    }
}
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closePreviewModal();
    }
});
</script>
"""


def _render_preview_button(project):
    """
    Render preview button with modal injection for ProjectAdmin.
    Requirements: 3.2
    """
    escaped_title = (project.title or '').replace("'", "\\'").replace('"', '\\"')
    project_type = project.project_type or 'external'
    
    # Escape the modal HTML for JavaScript template literal
    escaped_modal = PREVIEW_MODAL_HTML.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')
    
    button_html = (
        '<button type="button" '
        f'onclick="openPreviewModal({project.id}, \'{escaped_title}\', \'{project_type}\')" '
        'style="background:#6366f1;border:none;border-radius:6px;padding:6px 12px;'
        'color:white;cursor:pointer;display:inline-flex;align-items:center;gap:6px;'
        'transition:all 0.2s ease;font-size:0.875rem;" '
        'onmouseover="this.style.background=\'#4f46e5\'" '
        'onmouseout="this.style.background=\'#6366f1\'" '
        'title="Preview project">'
        '<i class="fa-solid fa-eye"></i> Preview'
        '</button>'
        '<script>'
        'if (!document.getElementById("previewModalOverlay")) {'
        'const c = document.createElement("div");'
        f'c.innerHTML = `{escaped_modal}`;'
        'document.body.appendChild(c);'
        '}'
        '</script>'
    )
    return Markup(button_html)


class ProjectAdmin(ModelView, model=Project):
    column_list = [
        Project.id, Project.title, Project.slug, 
        Project.project_type, Project.status,
        Project.is_featured, Project.order, "actions", Project.created_at
    ]
    column_searchable_list = [Project.title, Project.slug, Project.tech_stack]
    column_sortable_list = [Project.id, Project.title, Project.slug, Project.order, Project.created_at, Project.status]
    column_default_sort = [(Project.order, False)]
    form_excluded_columns = [Project.created_at, Project.updated_at, Project.gallery_images]
    
    column_labels = {
        Project.id: "ID",
        Project.title: "Название",
        Project.slug: "Slug (URL)",
        Project.description: "Описание",
        Project.project_type: "Тип",
        Project.static_content: "HTML/CSS/JS код",
        Project.static_path: "Путь к файлам",
        Project.image_url: "Изображение",
        Project.github_url: "GitHub",
        Project.live_url: "Демо URL",
        Project.tech_stack: "Технологии",
        Project.status: "Статус",
        Project.is_featured: "Избранное",
        Project.order: "Порядок",
        Project.created_at: "Создано",
        "actions": "Действия",
    }
    
    column_formatters = {
        Project.image_url: lambda m, a: Markup(
            f'<img src="{m.image_url}" style="max-height:50px;border-radius:4px;">'
        ) if m.image_url else "-",
        Project.is_featured: lambda m, a: "⭐" if m.is_featured else "",
        Project.slug: lambda m, a: Markup(f'<code style="color:#6366f1;">{m.slug}</code>') if m.slug else "-",
        Project.project_type: lambda m, a: Markup(
            f'<span style="background:{("#6366f1" if m.project_type == "static" else "#8b5cf6")};'
            f'color:white;padding:2px 8px;border-radius:4px;font-size:0.75rem;">'
            f'{"📦 Static" if m.project_type == "static" else "🔗 External"}</span>'
        ) if m.project_type else "-",
        Project.status: lambda m, a: Markup(
            f'<span style="background:{("#22c55e" if m.status == "live" else "#374151")};'
            f'color:white;padding:2px 8px;border-radius:4px;font-size:0.75rem;">'
            f'{"🟢 Live" if m.status == "live" else "⚫ Draft"}</span>'
        ) if m.status else "-",
        "actions": lambda m, a: _render_preview_button(m),
    }
    
    form_overrides = {
        "image_url": StringField,
        "project_type": StringField,
        "static_content": TextAreaField,
        "static_path": StringField,
        "status": StringField,
    }
    
    form_widget_args = {
        "image_url": {"widget": ImageUploadWidget()},
        "project_type": {"widget": TypeSelectorWidget()},
        "static_content": {"widget": CodeEditorWidget()},
        "static_path": {"widget": ZipUploadWidget()},
        "status": {"widget": StatusToggleWidget()},
    }
    
    form_args = {
        "slug": {"description": "Уникальный URL-идентификатор (только a-z, 0-9, -)"},
        "image_url": {"widget": ImageUploadWidget()},
        "project_type": {"widget": TypeSelectorWidget()},
        "static_content": {"widget": CodeEditorWidget()},
        "static_path": {"widget": ZipUploadWidget()},
        "status": {"widget": StatusToggleWidget()},
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
    
    # Custom list template with drag-drop reorder functionality
    # Requirements: 3.3
    list_template = "admin/project_list.html"


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


class GalleryImageAdmin(ModelView, model=GalleryImage):
    """
    Admin view for managing gallery images.
    Supports image preview, inline editing, and project linking.
    Requirements: 4.1, 4.3, 4.4
    """
    
    column_list = [
        GalleryImage.id, 
        "image_preview",
        GalleryImage.description, 
        GalleryImage.likes,
        GalleryImage.project_id, 
        GalleryImage.created_at
    ]
    
    column_searchable_list = [GalleryImage.description]
    column_sortable_list = [
        GalleryImage.id, 
        GalleryImage.likes, 
        GalleryImage.project_id, 
        GalleryImage.created_at
    ]
    column_default_sort = [(GalleryImage.created_at, True)]
    
    # Enable inline editing for description, likes, and project_id
    # Requirements: 4.3, 4.4
    column_editable_list = ["description", "likes", "project_id"]
    
    form_excluded_columns = [GalleryImage.created_at]
    
    column_labels = {
        GalleryImage.id: "ID",
        "image_preview": "Превью",
        GalleryImage.image_url: "URL изображения",
        GalleryImage.description: "Описание",
        GalleryImage.likes: "Лайки",
        GalleryImage.project_id: "Проект",
        GalleryImage.created_at: "Создано",
    }
    
    column_formatters = {
        # Image preview with thumbnail
        "image_preview": lambda m, a: Markup(
            f'<div style="position:relative;">'
            f'<img src="{m.image_url}" style="max-height:80px;max-width:120px;border-radius:8px;'
            f'border:2px solid #374151;object-fit:cover;cursor:pointer;" '
            f'onclick="window.open(\'{m.image_url}\', \'_blank\')" '
            f'title="Click to view full size">'
            f'</div>'
        ) if m.image_url else Markup('<span style="color:#6b7280;">No image</span>'),
        
        # Likes with heart icon
        GalleryImage.likes: lambda m, a: Markup(
            f'<span style="color:#ef4444;font-size:1.1rem;">❤️</span> '
            f'<span style="color:#e5e7eb;font-weight:500;">{m.likes or 0}</span>'
        ),
        
        # Project link with badge
        GalleryImage.project_id: lambda m, a: Markup(
            f'<span style="background:#6366f1;color:white;padding:2px 8px;border-radius:4px;'
            f'font-size:0.75rem;">📁 {m.project.title if m.project else "—"}</span>'
        ) if m.project_id else Markup('<span style="color:#6b7280;">Standalone</span>'),
    }
    
    form_overrides = {
        "image_url": StringField,
    }
    
    form_args = {
        "image_url": {
            "widget": ImageUploadWidget(),
            "description": "URL изображения или загрузите файл"
        },
        "description": {"description": "Описание изображения для галереи"},
        "likes": {"description": "Количество лайков"},
        "project_id": {"description": "Привязать к проекту (опционально)"},
    }
    
    name = "Изображение"
    name_plural = "Галерея"
    icon = "fa-solid fa-images"
    
    page_size = 20
    page_size_options = [10, 20, 50, 100]
    can_export = True
    export_types = ["csv", "json"]
    
    # Custom list template with bulk upload button
    # Requirements: 4.2
    list_template = "admin/gallery_list.html"
    
    async def on_model_delete(self, model: GalleryImage) -> None:
        """
        Override delete to remove image file from storage.
        Requirements: 4.5
        """
        import os
        from pathlib import Path
        
        if model.image_url:
            # Extract filename from URL (e.g., /uploads/filename.jpg -> uploads/filename.jpg)
            file_path = model.image_url.lstrip('/')
            
            # Check if file exists and delete it
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except (OSError, PermissionError) as e:
                    # Log error but don't prevent deletion of database record
                    print(f"Warning: Could not delete file {file_path}: {e}")


class StatsView(BaseView):
    """
    Custom admin view for statistics dashboard.
    Displays project, gallery, and message statistics with recent activity timeline.
    Requirements: 1.1, 1.2, 7.1, 7.2, 7.3
    """
    
    name = "Статистика"
    icon = "fa-solid fa-chart-line"
    
    @expose("/stats", methods=["GET"])
    async def stats_page(self, request: Request):
        """
        Render the statistics dashboard page.
        Requirements: 7.1, 7.2, 7.3
        """
        return await self.templates.TemplateResponse(
            request,
            "admin/stats.html",
            context={}
        )


def setup_admin(app, engine):
    from pathlib import Path
    
    auth = AdminAuth(secret_key=settings.SECRET_KEY)
    
    # Custom templates directory
    templates_dir = Path(__file__).parent.parent / "templates"
    templates_dir.mkdir(exist_ok=True)
    (templates_dir / "admin").mkdir(exist_ok=True)
    
    admin = Admin(
        app,
        engine,
        authentication_backend=auth,
        title="Doazhu Portfolio",
        base_url="/admin",
        templates_dir=str(templates_dir),
    )
    admin.add_view(ProjectAdmin)
    admin.add_view(GalleryImageAdmin)
    admin.add_view(SkillAdmin)
    admin.add_view(MessageAdmin)
    admin.add_view(SettingsAdmin)
    # Add Statistics dashboard page
    # Requirements: 1.1, 1.2
    admin.add_view(StatsView)
    return admin
