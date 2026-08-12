from pathlib import Path
import openpyxl


class Excel_Doc_Reader:

    def read(self, file_path: Path) -> str:

        workbook = openpyxl.load_workbook(
            filename=file_path,
            data_only=True
        )

        extracted_text = []

        for sheet in workbook.worksheets:

            extracted_text.append(
                f"Sheet: {sheet.title}"
            )

            for row in sheet.iter_rows(
                values_only=True
            ):

                values = [
                    str(value)
                    for value in row
                    if value is not None
                ]

                if values:
                    extracted_text.append(
                        " | ".join(values)
                    )

        return "\n".join(extracted_text)