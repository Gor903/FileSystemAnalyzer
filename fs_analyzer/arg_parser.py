import argparse
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from .exceptions import InvalidArgumentError


@dataclass
class Config:
    """Configuration object for the file system analyzer."""

    directory: str = "."
    log_level: int = logging.INFO
    large_file_threshold: Optional[float] = None  # in MB
    ignore_list: List[str] = field(default_factory=list)
    save_path: Optional[str] = None
    detail: bool = True

    def __post_init__(self):
        if self.large_file_threshold is not None:
            self.large_file_threshold = self.large_file_threshold * 1024 * 1024


def parse_arguments() -> Config:
    parser = argparse.ArgumentParser(
        description="Analyze and categorize files in a directory",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Directory to analyze (default: current directory)",
    )

    parser.add_argument(
        "-s", "--size", type=float, help="Flag files larger than SIZE MB as large files"
    )

    parser.add_argument(
        "-i",
        "--ignore",
        type=str,
        help="Comma-separated list of files/directories to ignore",
    )

    parser.add_argument(
        "-l",
        "--log-level",
        choices=["debug", "info", "warning", "error", "critical"],
        default="info",
        help="Set logging level (default: info)",
    )

    parser.add_argument("--save", type=str, help="Save results to file")

    parser.add_argument("--detail", action="store_true", help="Log categories items")

    args = parser.parse_args()

    if not Path(args.directory).exists():
        raise InvalidArgumentError(f"Directory '{args.directory}' does not exist")

    ignore_list = []
    if args.ignore:
        ignore_list = [item.strip() for item in args.ignore.split(",")]

    log_level = getattr(logging, args.log_level.upper())

    return Config(
        directory=args.directory,
        log_level=log_level,
        large_file_threshold=args.size,
        ignore_list=ignore_list,
        save_path=args.save,
        detail=args.detail,
    )
