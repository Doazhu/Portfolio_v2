"""
File services for handling ZIP extraction and static project files.
"""
import os
import shutil
import zipfile
from pathlib import Path
from typing import Optional

# Directory for extracted static projects
STATIC_PROJECTS_DIR = Path("static-projects")
STATIC_PROJECTS_DIR.mkdir(exist_ok=True)

# Dangerous file extensions that should not be extracted (server-side scripts)
DANGEROUS_EXTENSIONS = {
    '.exe', '.bat', '.cmd', '.sh', '.ps1', '.vbs',
    '.jar', '.msi', '.dll', '.so', '.dylib', '.php', '.py',
    '.rb', '.pl', '.cgi', '.asp', '.aspx', '.jsp'
}

# Allowed extensions for static projects
ALLOWED_STATIC_EXTENSIONS = {
    '.html', '.htm', '.css', '.js', '.json', '.xml', '.txt', '.md',
    '.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.ico',
    '.woff', '.woff2', '.ttf', '.eot', '.otf',
    '.mp4', '.webm', '.mp3', '.wav', '.ogg',
    '.pdf', '.map'
}

# MIME types for proper content-type headers
MIME_TYPES = {
    '.html': 'text/html',
    '.htm': 'text/html',
    '.css': 'text/css',
    '.js': 'application/javascript',
    '.json': 'application/json',
    '.xml': 'application/xml',
    '.txt': 'text/plain',
    '.md': 'text/markdown',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.png': 'image/png',
    '.gif': 'image/gif',
    '.webp': 'image/webp',
    '.svg': 'image/svg+xml',
    '.ico': 'image/x-icon',
    '.woff': 'font/woff',
    '.woff2': 'font/woff2',
    '.ttf': 'font/ttf',
    '.eot': 'application/vnd.ms-fontobject',
    '.otf': 'font/otf',
    '.mp4': 'video/mp4',
    '.webm': 'video/webm',
    '.mp3': 'audio/mpeg',
    '.wav': 'audio/wav',
    '.ogg': 'audio/ogg',
    '.pdf': 'application/pdf',
    '.map': 'application/json',
}

MAX_ZIP_SIZE = 50 * 1024 * 1024  # 50MB max ZIP size
MAX_EXTRACTED_SIZE = 100 * 1024 * 1024  # 100MB max extracted size


class ZipExtractionError(Exception):
    """Raised when ZIP extraction fails"""
    pass


class InvalidZipContentError(ZipExtractionError):
    """Raised when ZIP contains malicious or invalid files"""
    pass


class ZipExtractService:
    """Service for extracting ZIP archives to static project directories."""
    
    def __init__(self, base_dir: Path = STATIC_PROJECTS_DIR):
        self.base_dir = base_dir
        self.base_dir.mkdir(exist_ok=True)
    
    def validate_zip_contents(self, zip_path: Path) -> list[str]:
        """
        Validate ZIP contents for security issues.
        Returns list of files that will be extracted.
        Raises InvalidZipContentError if malicious content detected.
        """
        validated_files = []
        total_size = 0
        
        try:
            with zipfile.ZipFile(zip_path, 'r') as zf:
                for info in zf.infolist():
                    # Skip directories
                    if info.is_dir():
                        continue
                    
                    filename = info.filename
                    
                    # Check for path traversal attacks
                    if '..' in filename or filename.startswith('/'):
                        raise InvalidZipContentError(
                            f"Path traversal detected: {filename}"
                        )
                    
                    # Check file extension
                    ext = Path(filename).suffix.lower()
                    if ext in DANGEROUS_EXTENSIONS:
                        raise InvalidZipContentError(
                            f"Dangerous file type not allowed: {filename}"
                        )
                    
                    # Track total extracted size
                    total_size += info.file_size
                    if total_size > MAX_EXTRACTED_SIZE:
                        raise InvalidZipContentError(
                            f"Extracted size exceeds limit ({MAX_EXTRACTED_SIZE // 1024 // 1024}MB)"
                        )
                    
                    validated_files.append(filename)
                    
        except zipfile.BadZipFile:
            raise ZipExtractionError("Invalid or corrupted ZIP file")
        
        if not validated_files:
            raise InvalidZipContentError("ZIP archive is empty")
        
        return validated_files
    
    def extract_zip(self, zip_path: Path, slug: str) -> str:
        """
        Extract ZIP archive to /static-projects/{slug}/.
        
        Args:
            zip_path: Path to the ZIP file
            slug: Project slug for the destination directory
            
        Returns:
            Path to the extracted directory (relative)
            
        Raises:
            ZipExtractionError: If extraction fails
            InvalidZipContentError: If ZIP contains malicious files
        """
        # Validate ZIP size
        if zip_path.stat().st_size > MAX_ZIP_SIZE:
            raise ZipExtractionError(
                f"ZIP file too large (max {MAX_ZIP_SIZE // 1024 // 1024}MB)"
            )
        
        # Validate contents before extraction
        self.validate_zip_contents(zip_path)
        
        # Create destination directory
        dest_dir = self.base_dir / slug
        
        # Remove existing directory if it exists
        if dest_dir.exists():
            shutil.rmtree(dest_dir)
        
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            with zipfile.ZipFile(zip_path, 'r') as zf:
                zf.extractall(dest_dir)
        except Exception as e:
            # Cleanup on failure
            if dest_dir.exists():
                shutil.rmtree(dest_dir)
            raise ZipExtractionError(f"Extraction failed: {str(e)}")
        
        return str(dest_dir)
    
    def get_extracted_path(self, slug: str) -> Optional[str]:
        """Get the path to extracted files for a project slug."""
        dest_dir = self.base_dir / slug
        if dest_dir.exists() and dest_dir.is_dir():
            return str(dest_dir)
        return None
    
    def cleanup(self, slug: str) -> bool:
        """
        Remove extracted files for a project.
        
        Args:
            slug: Project slug
            
        Returns:
            True if cleanup was successful, False if directory didn't exist
        """
        dest_dir = self.base_dir / slug
        if dest_dir.exists():
            shutil.rmtree(dest_dir)
            return True
        return False


class StaticProjectFileService:
    """Service for serving and managing static project files."""
    
    def __init__(self, base_dir: Path = STATIC_PROJECTS_DIR):
        self.base_dir = base_dir
    
    def get_file_path(self, slug: str, file_path: str) -> Optional[Path]:
        """
        Get the full path to a static project file.
        
        Args:
            slug: Project slug
            file_path: Relative path within the project
            
        Returns:
            Full path to the file, or None if not found/invalid
        """
        # Sanitize file_path to prevent path traversal
        if '..' in file_path or file_path.startswith('/'):
            return None
        
        full_path = self.base_dir / slug / file_path
        
        # Ensure the resolved path is within the project directory
        try:
            full_path = full_path.resolve()
            project_dir = (self.base_dir / slug).resolve()
            
            if not str(full_path).startswith(str(project_dir)):
                return None
        except (OSError, ValueError):
            return None
        
        if full_path.exists() and full_path.is_file():
            return full_path
        
        return None
    
    def get_index_file(self, slug: str) -> Optional[Path]:
        """
        Get the index.html file for a static project.
        
        Args:
            slug: Project slug
            
        Returns:
            Path to index.html, or None if not found
        """
        return self.get_file_path(slug, 'index.html')
    
    def list_files(self, slug: str) -> list[str]:
        """
        List all files in a static project directory.
        
        Args:
            slug: Project slug
            
        Returns:
            List of relative file paths
        """
        project_dir = self.base_dir / slug
        if not project_dir.exists():
            return []
        
        files = []
        for path in project_dir.rglob('*'):
            if path.is_file():
                rel_path = path.relative_to(project_dir)
                files.append(str(rel_path))
        
        return sorted(files)
    
    def cleanup_project(self, slug: str) -> bool:
        """
        Remove all files for a deleted project.
        
        Args:
            slug: Project slug
            
        Returns:
            True if cleanup was successful, False if directory didn't exist
        """
        project_dir = self.base_dir / slug
        try:
            if project_dir.exists() and project_dir.is_dir():
                shutil.rmtree(project_dir)
                return True
        except (OSError, PermissionError):
            # Directory may have been deleted manually or permission issue
            pass
        return False
    
    def get_mime_type(self, file_path: str) -> str:
        """
        Get MIME type for a file based on extension.
        
        Args:
            file_path: Path to the file
            
        Returns:
            MIME type string, defaults to 'application/octet-stream'
        """
        ext = Path(file_path).suffix.lower()
        return MIME_TYPES.get(ext, 'application/octet-stream')
    
    def get_project_size(self, slug: str) -> int:
        """
        Get total size of a static project in bytes.
        
        Args:
            slug: Project slug
            
        Returns:
            Total size in bytes, 0 if project doesn't exist
        """
        project_dir = self.base_dir / slug
        if not project_dir.exists():
            return 0
        
        total_size = 0
        for path in project_dir.rglob('*'):
            if path.is_file():
                total_size += path.stat().st_size
        
        return total_size
