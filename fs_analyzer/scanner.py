import logging
import os

from .arg_parser import Config
from .file_utils import get_file_category, get_file_info, is_large_file, should_ignore
from .models import AnalysisResult


class FileSystemScanner:
    """Scanner for analyzing file systems."""

    def __init__(self, config: Config, logger: logging.Logger):
        self.config = config
        self.logger = logger
        self.result = AnalysisResult(
            directory=config.directory, large_file_threshold=config.large_file_threshold
        )

    def scan(self) -> AnalysisResult:
        """Scan the directory and return analysis results."""
        self.logger.info(f"Starting analysis of directory: {self.config.directory}")
        self.logger.info(f"Ignore list: {self.config.ignore_list}")
        if self.config.large_file_threshold:
            self.logger.info(
                f"Large file threshold: {self.config.large_file_threshold / 1024 / 1024:.2f} MB"
            )

        self._process_directory(self.config.directory)

        self.logger.info("Analysis completed")
        return self.result

    def _process_directory(self, path: str):
        """Recursively process directory contents."""
        try:
            items = os.listdir(path)
        except (PermissionError, FileNotFoundError, NotADirectoryError) as e:
            self.logger.error(f"{type(e).__name__}: {e}")
            return

        for item in items:
            if should_ignore(item, self.config.ignore_list):
                continue

            full_path = os.path.join(path, item)

            if os.path.isdir(full_path):
                self._process_directory(full_path)
            elif os.path.isfile(full_path):
                self._process_file(full_path)

    def _process_file(self, path: str):
        """Process a single file."""
        try:
            file_info = get_file_info(path)

            # Check if it's a large file
            if is_large_file(file_info.size, self.config.large_file_threshold):
                category = self.result.get_category("large_files")
                category.add_file(file_info)
                return

            # Categorize by extension
            category_name = get_file_category(path)
            category = self.result.get_category(category_name)
            category.add_file(file_info)

        except Exception as e:
            self.logger.error(f"Error processing file {path}: {e}")
