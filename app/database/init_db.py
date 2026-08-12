from app.database.base import Base
from app.database.database import engine

# Import all models so SQLAlchemy registers them.
from app.models import (
    Email,
    ComplianceResult,
)


def init_database() -> None:
    """
    Create all SQLite tables.
    """

    Base.metadata.create_all(
        bind=engine
    )

    print(
        "SQLite database initialized successfully."
    )


if __name__ == "__main__":
    init_database()