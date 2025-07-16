import json
import logging

from .models import AnalysisResult


class ReportGenerator:
    def __init__(self, logger: logging.Logger, detail: bool):
        self.logger = logger
        self.detail = detail

    def generate_text_report(self, result: AnalysisResult) -> str:
        lines = []

        for category_name, category in result.categories.items():
            if category.count <= 0:
                self.logger.debug(f"Category '{category_name}' has no items")
                continue

            lines.append(
                f"Category: {category_name:<15} "
                f"Size: {category.size_formatted:<9} "
                f"Count: {category.count}"
            )

            if self.detail:
                for i, file_info in enumerate(category.files):
                    lines.append(
                        f"\t{i+1}: {file_info.path} {file_info.permissions} "
                        f"{file_info.size_formatted}"
                    )

        return "\n".join(lines)

    def save_report(self, content: str, path: str):
        try:
            with open(path, "w") as f:
                f.write(content)
            self.logger.info(f"Report saved to: {path}")
        except Exception as e:
            self.logger.error(f"Error saving report to {path}: {e}")
