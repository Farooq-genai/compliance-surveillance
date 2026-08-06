from pathlib import Path


class FileLoader():
    """
    Utility class for loading text files.

    Used primarily for reading AI prompts templates
    """

    @staticmethod
    def read(file_path: str) -> str:
        path = Path(file_path)
        