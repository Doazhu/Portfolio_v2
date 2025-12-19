from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.session import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text)
    
    # Project type: 'static' or 'external'
    project_type = Column(String(20), default='external')
    
    # For static projects
    static_content = Column(Text, nullable=True)  # HTML/CSS/JS code
    static_path = Column(String(500), nullable=True)  # Path to extracted ZIP files
    
    image_url = Column(String(500))
    github_url = Column(String(500))
    live_url = Column(String(500))  # For external projects
    tech_stack = Column(String(500))
    
    # Status: 'live' or 'draft'
    status = Column(String(20), default='draft')
    
    is_featured = Column(Boolean, default=False)
    order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship to gallery images
    gallery_images = relationship("GalleryImage", back_populates="project")

    def __str__(self):
        return self.title


class GalleryImage(Base):
    __tablename__ = "gallery_images"

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    likes = Column(Integer, default=0)
    
    # Optional link to project
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship back to Project
    project = relationship("Project", back_populates="gallery_images")

    def __str__(self):
        return f"GalleryImage {self.id}: {self.description or 'No description'}"


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category = Column(String(100))
    level = Column(Integer, default=50)
    icon = Column(String(100))
    order = Column(Integer, default=0)

    def __str__(self):
        return self.name


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(200), nullable=False)
    subject = Column(String(300))
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __str__(self):
        return f"{self.name} - {self.subject or 'No subject'}"


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(200), nullable=False)

    def __str__(self):
        return self.username


class Settings(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, nullable=False)
    value = Column(Text)
    description = Column(String(300))

    def __str__(self):
        return self.key
