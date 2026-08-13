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

    def update_matrix(self, matrix: dict):

        current_matrix = self.get_matrix()

        # Validate categories
        if set(matrix.keys()) != set(
            current_matrix.keys()
        ):
            raise ValueError(
                "Invalid risk matrix categories"
            )

        # Validate scores
        for category, score in matrix.items():

            if not isinstance(score, int):
                raise ValueError(
                    f"Score for '{category}' must be an integer"
                )

            if score < 0:
                raise ValueError(
                    f"Score for '{category}' cannot be negative"
                )

        # Save complete matrix
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


    def update_score(
        self,
        category: str,
        score: int
    ):

        matrix = self.get_matrix()

        if category not in matrix:
            raise ValueError(
                f"Unknown category: {category}"
            )

        matrix[category] = score

        return self.update_matrix(matrix)