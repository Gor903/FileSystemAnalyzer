class FileSystemAnalyzerError(Exception):
    """Base exception for file system analyzer."""

    pass


class PermissionError(FileSystemAnalyzerError):
    """Raised when permission is denied."""

    pass


class InvalidArgumentError(FileSystemAnalyzerError):
    """Raised when invalid arguments are provided."""

    pass
