import pytest

import database.db as db
from app import app as flask_app

# Note: importing `app` runs init_db()/seed_db() against the real
# expense_tracker.db. Both are idempotent, so this is harmless.


@pytest.fixture
def client(tmp_path, monkeypatch):
    """Test client backed by a fresh temporary database (with the demo user)."""
    monkeypatch.setattr(db, "DB_PATH", str(tmp_path / "test.db"))
    db.init_db()
    db.seed_db()
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client


@pytest.fixture
def user_count():
    def count():
        conn = db.get_db()
        try:
            return conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        finally:
            conn.close()
    return count
