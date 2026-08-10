import sqlite3


def test_database_tables():

    conn = sqlite3.connect(
        "data/compliance_surveillance.db"
    )

    tables = conn.execute(
        "SELECT name FROM sqlite_master "
        "WHERE type='table' "
        "ORDER BY name"
    ).fetchall()

    conn.close()

    table_names = [table[0] for table in tables]

    assert "emails" in table_names
    assert "email_attachments" in table_names
    assert "compliance_results" in table_names

    assert len(table_names) == 3