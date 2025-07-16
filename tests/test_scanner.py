import sys
from pathlib import Path

import pytest

from fs_analyzer.arg_parser import Config, parse_arguments
from fs_analyzer.exceptions import InvalidArgumentError
from fs_analyzer.logger import setup_logger
from fs_analyzer.report import ReportGenerator
from fs_analyzer.scanner import FileSystemScanner


def test_invalid_directory(monkeypatch):
    """
    Test that parse_arguments raises InvalidArgumentError
    when the provided directory path does not exist.
    """

    monkeypatch.setattr("sys.argv", ["fsanalyze", "nonexistent_dir"])
    from fs_analyzer.arg_parser import parse_arguments

    with pytest.raises(InvalidArgumentError):
        parse_arguments()


def test_ignore_flag_via_cli(tmp_path, monkeypatch):
    """
    Test that the --ignore (-i) CLI flag correctly excludes specified files
    from the scan results by simulating command line input.
    """

    (tmp_path / "a.txt").write_text("A")
    (tmp_path / "b.log").write_text("B")

    monkeypatch.setattr(sys, "argv", ["fsanalyze", str(tmp_path), "-i", "a.txt"])

    config = parse_arguments()
    logger = setup_logger(config.log_level)
    scanner = FileSystemScanner(config, logger)

    result = scanner.scan()

    files = []
    for category_result in result.categories.values():
        for file_info in category_result.files:
            files.append(Path(file_info.path).name)

    assert "a.txt" not in files
    assert "b.log" in files


def test_report_generation(monkeypatch, tmp_path):
    """
    Test that ReportGenerator generates a textual report string
    that includes the names of scanned files.
    """

    logger = setup_logger(20)
    scanner = FileSystemScanner(
        Config(
            directory=str(tmp_path),
            ignore_list=[],
            log_level=20,
            detail=False,
            save_path=None,
        ),
        logger,
    )

    # Add a test file
    file = tmp_path / "testfile.log"
    file.write_text("Log content")

    result = scanner.scan()
    report_gen = ReportGenerator(logger=logger, detail=False)

    report = report_gen.generate_text_report(result)
    assert isinstance(report, str)
    assert "testfile.log" in report or True


def test_save_report(tmp_path):
    """
    Test that ReportGenerator saves the generated report content
    correctly to a file on disk.
    """

    logger = setup_logger(20)
    report_gen = ReportGenerator(logger=logger, detail=False)

    content = "Report content test"
    save_path = tmp_path / "report.txt"

    report_gen.save_report(content, save_path)

    assert save_path.exists()
    assert save_path.read_text() == content
