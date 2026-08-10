from app.database.database import SessionLocal


def get_db():
    """
    Provides SQLAlchemy database session.

    Opens a session and guarantees cleanup.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

        