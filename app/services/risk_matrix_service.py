import json
from pathlib import Path

from app.core.risk_matrix import DEFAULT_RISK_MATRIX


class RiskMatrixService:

    def __init__(self):

        self.file_path = Path(
            "app/storage/risk_matrix.json"
        )

        self.initialize()


    def initialize(self):

        if not self.file_path.exists():

            self.file_path.parent.mkdir(
                exist_ok=True
            )

            self.file_path.write_text(
                json.dumps(
                    DEFAULT_RISK_MATRIX,
                    indent=4
                )
            )


    def get_matrix(self):

        with open(
            self.file_path,
            "r"
        ) as file:

            return json.load(file)


    def update_score(
        self,
        category,
        score
    ):

        matrix = self.get_matrix()


        if category not in matrix:

            raise Exception(
                f"Unknown category: {category}"
            )


        matrix[category] = score


        with open(
            self.file_path,
            "w"
        ) as file:

            json.dump(
                matrix,
                file,
                indent=4
            )


        return matrix