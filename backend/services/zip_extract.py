"""
ZipExtractService - Service for extracting ZIP archives for static projects.

Handles extraction of ZIP files to /static-projects/{slug}/ directory
with validation to prevent malicious files.
"""

import os
import zipfile
import shutil
from pathlib import Path
from typing import Set

# Directory where static projects are extracted
STATIC_PROJECTS_DIR = Path("static-projects")

# Allowed file extensions for static projects
ALLOWED_EXTENSIONS: Set[str] = {
    # Web files
    ".html", ".htm", ".css", ".js", ".json",
    # Images
    ".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".ico",
    # Fonts
    ".woff", ".woff2", ".ttf", ".eot", ".otf",
    # Other assets
    ".txt", ".md", ".xml", ".map",
}

# Dangerous file patterns to reject
DANGEROUS_PATTERNS: Set[str] = {
    ".php", ".py", ".rb", ".pl", ".sh", ".bash", ".exe", ".bat", ".cmd",
    ".dll", ".so", ".dylib", ".jar", ".war", ".class",
    ".htaccess", ".htpasswd", ".env",
}

# Maximum file size for extraction (50MB)
MAX_ZIP_SIZE = 50 * 1024 * 1024

# Maximum number of files in archive
MAX_FILES_COUNT = 500


class ZipExtractionError(Exception):
    """Base exception for ZIP extraction errors."""
    pass


class InvalidZipError(ZipExtractionError):
    """Raised when ZIP file is invalid or corrupted."""
    pass


class MaliciousFileError(ZipExtractionError):
    """Raised when ZIP contains potentially malicious files."""
    pass


class ZipTooLargeError(ZipExtractionError):
    """Raised when ZIP file exceeds size limit."""
    pass


class ZipExtractService:
    """Service for extracting ZIP archives for static projects."""
    
    def __init__(self, base_dir: Path = STATIC_PROJECTS_DIR):
        """
        Initialize the service.
        
        Args:
            base_dir: Base directory for extracted projects
        """
        self.base_dir = base_dir
        self.base_dir.mkdir(exist_ok=True)
    
    def validate_zip_contents(self, zip_path: Path) -> None:
        """
        Validate ZIP contents before extraction.
        
        Args:
            zip_path: Path to the ZIP file
            
        Raises:
            InvalidZipError: If ZIP is invalid or corrupted
            MaliciousFileError: If ZIP contains dangerous files
            ZipTooLargeError: If ZIP exceeds size limits
        """
        if not zipfile.is_zipfile(zip_path):
            raise InvalidZipError("File is not a valid ZIP archive")
        
        try:
            with zipfile.ZipFile(zip_path, 'r') as zf:
                # Check for ZIP bomb (too many files)
                file_list = zf.namelist()
                if len(file_list) > MAX_FILES_COUNT:
                    raise ZipTooLargeError(
                        f"ZIP contains too many files ({len(file_list)} > {MAX_FILES_COUNT})"
                    )
                
                # Calculate total uncompressed size
                total_size = sum(info.file_size for info in zf.infolist())
                if total_size > MAX_ZIP_SIZE:
                    raise ZipTooLargeError(
                        f"ZIP uncompressed size exceeds limit ({total_size} > {MAX_ZIP_SIZE})"
                    )
                
                # Check each file
                for filename in file_list:
                    self._validate_filename(filename)
                    
        except zipfile.BadZipFile as e:
            raise InvalidZipError(f"Corrupted ZIP file: {e}")
    
    def _validate_filename(self, filename: str) -> None:
        """
        Validate a single filename from the archive.
        
        Args:
            filename: Name of the file in the archive
            
        Raises:
            MaliciousFileError: If filename is potentially dangerous
        """
        # Check for path traversal attacks
        if ".." in filename or filename.startswith("/"):
            raise MaliciousFileError(
                f"Path traversal detected in filename: {filename}"
            )
        
        # Skip directories
        if filename.endswith("/"):
            return
        
        # Get file extension
        ext = Path(filename).suffix.lower()
        
        # Check for dangerous extensions
        if ext in DANGEROUS_PATTERNS:
            raise MaliciousFileError(
                f"Dangerous file type detected: {filename}"
            )
        
        # Check if extension is allowed (if it has one)
        if ext and ext not in ALLOWED_EXTENSIONS:
            raise MaliciousFileError(
                f"File type not allowed: {filename} (extension: {ext})"
            )
    
    def extract_zip(self, zip_path: Path, slug: str) -> Path:
        """
        Extract ZIP archive to /static-projects/{slug}/.
        
        Args:
            zip_path: Path to the ZIP file
            slug: Project slug for the destination directory
            
        Returns:
            Path to the extracted directory
            
        Raises:
            ZipExtractionError: If extraction fails
        """
        # Validate before extraction
        self.validate_zip_contents(zip_path)
        
        # Create destination directory
        dest_dir = self.base_dir / slug
        
        # Remove existing directory if it exists
        if dest_dir.exists():
            shutil.rmtree(dest_dir)
        
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            with zipfile.ZipFile(zip_path, 'r') as zf:
                # Extract all files
                zf.extractall(dest_dir)
            
            return dest_dir
            
        except Exception as e:
            # Clean up on failure
            if dest_dir.exists():
                shutil.rmtree(dest_dir)
            raise ZipExtractionError(f"Failed to extract ZIP: {e}")
    
    def cleanup_project(self, slug: str) -> bool:
        """
        Remove extracted project directory.
        
        Args:
            slug: Project slug
            
        Returns:
            True if directory was removed, False if it didn't exist
        """
        project_dir = self.base_dir / slug
        
        if project_dir.exists():
            shutil.rmtree(project_dir)
            return True
        
        return False
    
    def get_project_path(self, slug: str) -> Path | None:
        """
        Get the path to an extracted project.
        
        Args:
            slug: Project slug
            
        Returns:
            Path to the project directory, or None if it doesn't exist
        """
        project_dir = self.base_dir / slug
        
        if project_dir.exists() and project_dir.is_dir():
            return project_dir
        
        return None
    
    def list_project_files(self, slug: str) -> list[str]:
        """
        List all files in an extracted project.
        
        Args:
            slug: Project slug
            
        Returns:
            List of relative file paths
        """
        project_dir = self.base_dir / slug
        
        if not project_dir.exists():
            return []
        
        files = []
        for path in project_dir.rglob("*"):
            if path.is_file():
                files.append(str(path.relative_to(project_dir)))
        
        return files