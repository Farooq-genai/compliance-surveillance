from pathlib import Path
from pypdf import PdfReader as PyPdfReader


class PdfReader:

    def read(self, file_path: Path) -> str:
        reader = PyPdfReader(str(file_path))

        text = []

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text.append(page_text)

        return "\n".join(text)


