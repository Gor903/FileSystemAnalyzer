import signal
import sys

from .arg_parser import parse_arguments
from .exceptions import InvalidArgumentError
from .logger import setup_logger
from .report import ReportGenerator
from .scanner import FileSystemScanner


def main():
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)

    try:
        config = parse_arguments()

        logger = setup_logger(config.log_level)

        scanner = FileSystemScanner(config, logger)
        result = scanner.scan()

        report_generator = ReportGenerator(
            logger=logger,
            detail=config.detail,
        )

        report_content = report_generator.generate_text_report(result)

        if config.save_path:
            report_generator.save_report(report_content, config.save_path)
        else:
            print(report_content)

    except InvalidArgumentError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
