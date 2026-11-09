
import pytest

import database


@pytest.fixture
def test_database(tmp_path, monkeypatch):
    """Create an isolated temporary database for each test."""

    test_db = tmp_path / "test_careerpilot.db"

    monkeypatch.setattr(database, "DB_PATH", test_db)

    database.initialize_database()

    return test_db
