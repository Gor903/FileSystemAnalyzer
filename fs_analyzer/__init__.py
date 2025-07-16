__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .main import main
from .models import AnalysisResult, CategoryResult, FileInfo
from .report import ReportGenerator
from .scanner import FileSystemScanner

__all__ = [
    "main",
    "FileInfo",
    "CategoryResult",
    "AnalysisResult",
    "FileSystemScanner",
    "ReportGenerator",
]
