from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class FileInfo:
    path: str
    size: int
    readable: bool
    writable: bool
    executable: bool

    def __post_init__(self):
        self.size_formatted = self._human_readable_size(self.size)
        self.permissions = self._format_permissions()

    def _human_readable_size(self, size_bytes: int) -> str:
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if size_bytes < 1024:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.2f} PB"

    def _format_permissions(self) -> str:
        """Format permissions as rwx string."""
        perms = ""
        perms += "r" if self.readable else "-"
        perms += "w" if self.writable else "-"
        perms += "x" if self.executable else "-"
        return perms


@dataclass
class CategoryResult:
    name: str
    total_size: int = 0
    files: List[FileInfo] = field(default_factory=list)

    @property
    def count(self) -> int:
        return len(self.files)

    @property
    def size_formatted(self) -> str:
        return self._human_readable_size(self.total_size)

    def add_file(self, file_info: FileInfo):
        """Add a file to this category."""
        self.files.append(file_info)
        self.total_size += file_info.size

    def _human_readable_size(self, size_bytes: int) -> str:
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if size_bytes < 1024:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.2f} PB"


@dataclass
class AnalysisResult:
    categories: Dict[str, CategoryResult] = field(default_factory=dict)
    directory: str = "."
    large_file_threshold: Optional[float] = None

    def get_category(self, name: str) -> CategoryResult:
        if name not in self.categories:
            self.categories[name] = CategoryResult(name=name)
        return self.categories[name]
