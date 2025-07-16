import os
from pathlib import Path
from typing import List, Optional

from .constants import FILE_EXTENSIONS
from .models import FileInfo


def human_readable_size(size_bytes: int) -> str:
    """Convert bytes to human readable format."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} PB"


def get_file_info(path: str) -> FileInfo:
    """Get file information including size and permissions."""
    size = os.path.getsize(path)
    readable = os.access(path, os.R_OK)
    writable = os.access(path, os.W_OK)
    executable = os.access(path, os.X_OK)

    return FileInfo(
        path=path,
        size=size,
        readable=readable,
        writable=writable,
        executable=executable,
    )


def get_file_category(path: str) -> str:
    """Determine the category of a file based on its extension."""
    path_obj = Path(path)
    ext = "".join(path_obj.suffixes)[1:].lower()

    for category, extensions in FILE_EXTENSIONS.items():
        if ext in extensions:
            return category

    return "other"


def should_ignore(item: str, ignore_list: List[str]) -> bool:
    """Check if an item should be ignored."""
    return item in ignore_list


def is_large_file(size: int, threshold: Optional[float]) -> bool:
    """Check if a file is considered large."""
    if threshold is None:
        return False
    return size > threshold
