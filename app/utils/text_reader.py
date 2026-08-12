from pathlib import Path


class TextReader:

    def read(self, file_path: Path) -> str:
        return file_path.read_text(
            encoding="utf-8",
            errors="ignore"
        )