"""
Admin API endpoints for the portfolio admin panel.
Provides endpoints for project reordering, bulk gallery upload, statistics, and preview.
"""
from typing import List
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from db.session import get_db
from db.models import Project, GalleryImage, Message

router = APIRouter(prefix="/admin/api", tags=["admin"])


# ============== Schemas ==============

class ReorderRequest(BaseModel):
    """Request body for reordering projects."""
    project_ids: List[int]


class ProjectStats(BaseModel):
    """Statistics about projects."""
    total: int
    live: int
    draft: int
    static_count: int
    external_count: int


class GalleryStats(BaseModel):
    """Statistics about gallery images."""
    total: int
    linked_to_projects: int
    standalone: int


class MessageStats(BaseModel):
    """Statistics about messages."""
    total: int
    unread: int


class ActivityItem(BaseModel):
    """A single activity item."""
    type: str
    description: str
    timestamp: datetime


class StatsResponse(BaseModel):
    """Full statistics response."""
    projects: ProjectStats
    gallery: GalleryStats
    messages: MessageStats
    recent_activity: List[ActivityItem]


class GalleryImageOut(BaseModel):
    """Output schema for gallery images."""
    id: int
    image_url: str
    description: str | None
    likes: int
    project_id: int | None
    created_at: datetime | None

    class Config:
        from_attributes = True


# ============== Endpoints ==============

@router.put("/reorder")
async def reorder_projects(
    request: ReorderRequest,
    db: AsyncSession = Depends(get_db)
) -> dict:
    """
    Reorder projects by updating their order field.
    
    Accepts a list of project IDs in the desired order.
    Updates the order field for each project in a transaction.
    
    Requirements: 3.3
    """
    project_ids = request.project_ids
    
    if not project_ids:
        raise HTTPException(status_code=400, detail="Project IDs list cannot be empty")
    
    try:
        # Update order for each project in a single transaction
        for idx, project_id in enumerate(project_ids):
            result = await db.execute(
                select(Project).where(Project.id == project_id)
            )
            project = result.scalar_one_or_none()
            
            if not project:
                raise HTTPException(
                    status_code=404, 
                    detail=f"Project with ID {project_id} not found"
                )
            
            project.order = idx
        
        await db.commit()
        
        return {"message": "Projects reordered successfully", "count": len(project_ids)}
    
    except HTTPException:
        await db.rollback()
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to reorder projects: {str(e)}")


@router.post("/gallery/bulk")
async def bulk_upload_gallery(
    files: List[UploadFile] = File(...),
    db: AsyncSession = Depends(get_db)
) -> dict:
    """
    Bulk upload images to the gallery.
    
    Accepts multiple image files and creates GalleryImage records for each.
    Returns list of created images.
    
    Requirements: 4.2
    """
    import uuid
    from pathlib import Path
    
    UPLOAD_DIR = Path("uploads")
    ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"}
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
    
    created_images = []
    errors = []
    
    for file in files:
        try:
            # Validate file extension
            ext = Path(file.filename).suffix.lower()
            if ext not in ALLOWED_EXTENSIONS:
                errors.append({
                    "filename": file.filename,
                    "error": f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
                })
                continue
            
            # Read and validate file size
            content = await file.read()
            if len(content) > MAX_FILE_SIZE:
                errors.append({
                    "filename": file.filename,
                    "error": "File too large (max 5MB)"
                })
                continue
            
            # Generate unique filename and save
            filename = f"{uuid.uuid4().hex}{ext}"
            file_path = UPLOAD_DIR / filename
            
            with open(file_path, "wb") as f:
                f.write(content)
            
            # Create GalleryImage record
            image_url = f"/uploads/{filename}"
            gallery_image = GalleryImage(
                image_url=image_url,
                description=None,
                likes=0,
                project_id=None
            )
            db.add(gallery_image)
            await db.flush()  # Get the ID
            
            created_images.append({
                "id": gallery_image.id,
                "image_url": image_url,
                "original_name": file.filename
            })
            
        except Exception as e:
            errors.append({
                "filename": file.filename,
                "error": str(e)
            })
    
    await db.commit()
    
    return {
        "created": created_images,
        "errors": errors,
        "total_created": len(created_images),
        "total_errors": len(errors)
    }


@router.get("/stats", response_model=StatsResponse)
async def get_stats(db: AsyncSession = Depends(get_db)) -> StatsResponse:
    """
    Get statistics about projects, gallery, and messages.
    
    Returns counts and distributions for dashboard display.
    
    Requirements: 7.1, 7.2, 7.3
    """
    # Project statistics
    total_projects = await db.execute(select(func.count(Project.id)))
    total_projects_count = total_projects.scalar() or 0
    
    live_projects = await db.execute(
        select(func.count(Project.id)).where(Project.status == 'live')
    )
    live_count = live_projects.scalar() or 0
    
    draft_projects = await db.execute(
        select(func.count(Project.id)).where(Project.status == 'draft')
    )
    draft_count = draft_projects.scalar() or 0
    
    static_projects = await db.execute(
        select(func.count(Project.id)).where(Project.project_type == 'static')
    )
    static_count = static_projects.scalar() or 0
    
    external_projects = await db.execute(
        select(func.count(Project.id)).where(Project.project_type == 'external')
    )
    external_count = external_projects.scalar() or 0
    
    # Gallery statistics
    total_gallery = await db.execute(select(func.count(GalleryImage.id)))
    total_gallery_count = total_gallery.scalar() or 0
    
    linked_gallery = await db.execute(
        select(func.count(GalleryImage.id)).where(GalleryImage.project_id.isnot(None))
    )
    linked_count = linked_gallery.scalar() or 0
    
    standalone_count = total_gallery_count - linked_count
    
    # Message statistics
    total_messages = await db.execute(select(func.count(Message.id)))
    total_messages_count = total_messages.scalar() or 0
    
    unread_messages = await db.execute(
        select(func.count(Message.id)).where(Message.is_read == False)
    )
    unread_count = unread_messages.scalar() or 0
    
    # Recent activity (last 10 items from projects, gallery, messages)
    recent_activity = []
    
    # Recent projects
    recent_projects_result = await db.execute(
        select(Project).order_by(Project.created_at.desc()).limit(5)
    )
    for project in recent_projects_result.scalars():
        if project.created_at:
            recent_activity.append(ActivityItem(
                type="project_created",
                description=f"Project '{project.title}' created",
                timestamp=project.created_at
            ))
    
    # Recent gallery images
    recent_images_result = await db.execute(
        select(GalleryImage).order_by(GalleryImage.created_at.desc()).limit(5)
    )
    for image in recent_images_result.scalars():
        if image.created_at:
            desc = image.description or "No description"
            recent_activity.append(ActivityItem(
                type="image_uploaded",
                description=f"Image uploaded: {desc[:50]}",
                timestamp=image.created_at
            ))
    
    # Recent messages
    recent_messages_result = await db.execute(
        select(Message).order_by(Message.created_at.desc()).limit(5)
    )
    for message in recent_messages_result.scalars():
        if message.created_at:
            recent_activity.append(ActivityItem(
                type="message_received",
                description=f"Message from {message.name}: {message.subject or 'No subject'}",
                timestamp=message.created_at
            ))
    
    # Sort by timestamp and limit to 10
    recent_activity.sort(key=lambda x: x.timestamp, reverse=True)
    recent_activity = recent_activity[:10]
    
    return StatsResponse(
        projects=ProjectStats(
            total=total_projects_count,
            live=live_count,
            draft=draft_count,
            static_count=static_count,
            external_count=external_count
        ),
        gallery=GalleryStats(
            total=total_gallery_count,
            linked_to_projects=linked_count,
            standalone=standalone_count
        ),
        messages=MessageStats(
            total=total_messages_count,
            unread=unread_count
        ),
        recent_activity=recent_activity
    )


@router.post("/upload-zip")
async def upload_zip(
    file: UploadFile = File(...),
    slug: str = None,
    db: AsyncSession = Depends(get_db)
) -> dict:
    """
    Upload and extract a ZIP archive for a static project.
    
    Accepts a ZIP file and project slug, extracts to /static-projects/{slug}/
    Returns the path and list of extracted files.
    
    Requirements: 6.1
    """
    import tempfile
    from pathlib import Path
    from services.zip_extract import ZipExtractService, ZipExtractionError
    
    if not slug:
        raise HTTPException(status_code=400, detail="Project slug is required")
    
    # Validate file type
    if not file.filename.lower().endswith('.zip'):
        raise HTTPException(status_code=400, detail="File must be a ZIP archive")
    
    try:
        # Save uploaded file to temp location
        content = await file.read()
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as tmp:
            tmp.write(content)
            tmp_path = Path(tmp.name)
        
        try:
            # Extract using ZipExtractService
            service = ZipExtractService()
            extracted_path = service.extract_zip(tmp_path, slug)
            
            # Get list of extracted files
            files = service.list_project_files(slug)
            
            return {
                "path": str(extracted_path),
                "files": files,
                "message": f"Successfully extracted {len(files)} files"
            }
        finally:
            # Clean up temp file
            tmp_path.unlink(missing_ok=True)
            
    except ZipExtractionError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process ZIP: {str(e)}")


@router.get("/preview/{project_id}")
async def preview_project(
    project_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get preview HTML for a project.
    
    For static projects: renders static_content as HTML
    For external projects: redirects to live_url
    
    Requirements: 3.2
    """
    result = await db.execute(
        select(Project).where(Project.id == project_id)
    )
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if project.project_type == 'static':
        # For static projects, return the static content as HTML
        if project.static_content:
            return HTMLResponse(content=project.static_content)
        elif project.static_path:
            # Try to serve index.html from the static path
            from pathlib import Path
            index_path = Path(project.static_path) / "index.html"
            if index_path.exists():
                with open(index_path, "r", encoding="utf-8") as f:
                    return HTMLResponse(content=f.read())
            else:
                return HTMLResponse(
                    content=f"<html><body><h1>Static project: {project.title}</h1>"
                    f"<p>No index.html found at {project.static_path}</p></body></html>"
                )
        else:
            return HTMLResponse(
                content=f"<html><body><h1>{project.title}</h1>"
                f"<p>No static content available</p></body></html>"
            )
    
    elif project.project_type == 'external':
        # For external projects, redirect to live_url
        if project.live_url:
            return RedirectResponse(url=project.live_url)
        else:
            return HTMLResponse(
                content=f"<html><body><h1>{project.title}</h1>"
                f"<p>No external URL configured</p></body></html>"
            )
    
    else:
        return HTMLResponse(
            content=f"<html><body><h1>{project.title}</h1>"
            f"<p>Unknown project type: {project.project_type}</p></body></html>"
        )
