import os
import uuid
from pathlib import Path
from typing import List

from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"}
MAX_FILE_SIZE = 5 * 1024 * 1024

router = APIRouter(prefix="/api/uploads", tags=["uploads"])


def validate_file(file: UploadFile) -> None:
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Недопустимый формат файла. Разрешены: {', '.join(ALLOWED_EXTENSIONS)}"
        )


@router.post("")
async def upload_file(file: UploadFile = File(...)):
    validate_file(file)
    
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="Файл слишком большой (макс. 5MB)")
    
    ext = Path(file.filename).suffix.lower()
    filename = f"{uuid.uuid4().hex}{ext}"
    file_path = UPLOAD_DIR / filename
    
    with open(file_path, "wb") as f:
        f.write(content)
    
    return JSONResponse({
        "filename": filename,
        "url": f"/uploads/{filename}",
        "size": len(content)
    })


@router.post("/multiple")
async def upload_multiple_files(files: List[UploadFile] = File(...)):
    results = []
    for file in files:
        validate_file(file)
        content = await file.read()
        if len(content) > MAX_FILE_SIZE:
            continue
        
        ext = Path(file.filename).suffix.lower()
        filename = f"{uuid.uuid4().hex}{ext}"
        file_path = UPLOAD_DIR / filename
        
        with open(file_path, "wb") as f:
            f.write(content)
        
        results.append({
            "original_name": file.filename,
            "filename": filename,
            "url": f"/uploads/{filename}",
            "size": len(content)
        })
    
    return JSONResponse({"files": results})


@router.delete("/{filename}")
async def delete_file(filename: str):
    file_path = UPLOAD_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Файл не найден")
    
    if ".." in filename or "/" in filename:
        raise HTTPException(status_code=400, detail="Недопустимое имя файла")
    
    os.remove(file_path)
    return JSONResponse({"message": "Файл удалён"})


@router.get("/manager", response_class=HTMLResponse)
async def upload_manager(request: Request):
    files = []
    for f in UPLOAD_DIR.iterdir():
        if f.is_file():
            files.append({
                "name": f.name,
                "url": f"/uploads/{f.name}",
                "size": f.stat().st_size
            })
    files.sort(key=lambda x: x["name"])
    
    files_html = ""
    for f in files:
        size_kb = f["size"] / 1024
        files_html += f'''
        <div class="file-item">
            <img src="{f['url']}" alt="{f['name']}" onerror="this.style.display='none'">
            <div class="file-info">
                <code>{f['url']}</code>
                <span class="file-size">{size_kb:.1f} KB</span>
            </div>
            <button onclick="copyUrl('{f['url']}')" class="btn-copy">📋 Копировать</button>
            <button onclick="deleteFile('{f['name']}')" class="btn-delete">🗑️</button>
        </div>
        '''
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Загрузка файлов — Doazhu Admin</title>
        <meta charset="utf-8">
        <style>
            * {{ box-sizing: border-box; }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: #0f0f1a;
                color: #e5e5e5;
                margin: 0;
                padding: 2rem;
            }}
            .container {{ max-width: 900px; margin: 0 auto; }}
            h1 {{
                background: linear-gradient(135deg, #6366f1, #a855f7);
                -webkit-background-clip: text;
                background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 2rem;
            }}
            .back-link {{
                color: #6366f1;
                text-decoration: none;
                margin-bottom: 1rem;
                display: inline-block;
            }}
            .back-link:hover {{ text-decoration: underline; }}
            .upload-zone {{
                border: 2px dashed #374151;
                border-radius: 12px;
                padding: 3rem;
                text-align: center;
                margin-bottom: 2rem;
                transition: all 0.3s;
            }}
            .upload-zone:hover, .upload-zone.dragover {{
                border-color: #6366f1;
                background: rgba(99, 102, 241, 0.1);
            }}
            .upload-zone input {{ display: none; }}
            .upload-zone label {{
                cursor: pointer;
                color: #9ca3af;
            }}
            .upload-zone label:hover {{ color: #6366f1; }}
            .btn {{
                background: #6366f1;
                color: white;
                border: none;
                padding: 0.75rem 1.5rem;
                border-radius: 8px;
                cursor: pointer;
                font-size: 1rem;
            }}
            .btn:hover {{ background: #818cf8; }}
            .files-list {{ margin-top: 2rem; }}
            .file-item {{
                display: flex;
                align-items: center;
                gap: 1rem;
                padding: 1rem;
                background: #1a1a2e;
                border-radius: 8px;
                margin-bottom: 0.75rem;
                border: 1px solid #2a2a3e;
            }}
            .file-item img {{
                width: 60px;
                height: 60px;
                object-fit: cover;
                border-radius: 6px;
            }}
            .file-info {{
                flex: 1;
                display: flex;
                flex-direction: column;
                gap: 0.25rem;
            }}
            .file-info code {{
                color: #6366f1;
                font-size: 0.875rem;
            }}
            .file-size {{ color: #6b7280; font-size: 0.75rem; }}
            .btn-copy, .btn-delete {{
                background: transparent;
                border: 1px solid #374151;
                color: #9ca3af;
                padding: 0.5rem;
                border-radius: 6px;
                cursor: pointer;
            }}
            .btn-copy:hover {{ border-color: #6366f1; color: #6366f1; }}
            .btn-delete:hover {{ border-color: #ef4444; color: #ef4444; }}
            .toast {{
                position: fixed;
                bottom: 2rem;
                right: 2rem;
                background: #22c55e;
                color: white;
                padding: 1rem 1.5rem;
                border-radius: 8px;
                display: none;
            }}
            .toast.show {{ display: block; }}
        </style>
    </head>
    <body>
        <div class="container">
            <a href="/admin" class="back-link">← Назад в админку</a>
            <h1>📁 Загрузка файлов</h1>
            
            <div class="upload-zone" id="dropZone">
                <input type="file" id="fileInput" accept="image/*" multiple>
                <label for="fileInput">
                    <p style="font-size:2rem;margin:0;">📤</p>
                    <p>Перетащите файлы сюда или <span style="color:#6366f1;">выберите</span></p>
                    <p style="font-size:0.75rem;color:#6b7280;">JPG, PNG, GIF, WebP, SVG — до 5MB</p>
                </label>
            </div>
            
            <h3>Загруженные файлы ({len(files)})</h3>
            <div class="files-list">
                {files_html if files_html else '<p style="color:#6b7280;">Нет загруженных файлов</p>'}
            </div>
        </div>
        
        <div class="toast" id="toast">Скопировано!</div>
        
        <script>
            const dropZone = document.getElementById('dropZone');
            const fileInput = document.getElementById('fileInput');
            
            ['dragenter', 'dragover'].forEach(e => {{
                dropZone.addEventListener(e, () => dropZone.classList.add('dragover'));
            }});
            ['dragleave', 'drop'].forEach(e => {{
                dropZone.addEventListener(e, () => dropZone.classList.remove('dragover'));
            }});
            
            dropZone.addEventListener('dragover', e => e.preventDefault());
            dropZone.addEventListener('drop', e => {{
                e.preventDefault();
                uploadFiles(e.dataTransfer.files);
            }});
            
            fileInput.addEventListener('change', e => uploadFiles(e.target.files));
            
            async function uploadFiles(files) {{
                for (const file of files) {{
                    const formData = new FormData();
                    formData.append('file', file);
                    try {{
                        await fetch('/api/uploads', {{ method: 'POST', body: formData }});
                    }} catch (e) {{
                        alert('Ошибка: ' + e.message);
                    }}
                }}
                location.reload();
            }}
            
            function copyUrl(url) {{
                navigator.clipboard.writeText(url);
                const toast = document.getElementById('toast');
                toast.classList.add('show');
                setTimeout(() => toast.classList.remove('show'), 2000);
            }}
            
            async function deleteFile(filename) {{
                if (!confirm('Удалить ' + filename + '?')) return;
                await fetch('/api/uploads/' + filename, {{ method: 'DELETE' }});
                location.reload();
            }}
        </script>
    </body>
    </html>
    '''

