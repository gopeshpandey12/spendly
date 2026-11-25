import database.db as db

VALID = {"name": "Asha Rao", "email": "asha@example.com", "password": "secret123"}


def post(client, **overrides):
    return client.post("/register", data={**VALID, **overrides})


def test_get_register_page(client):
    resp = client.get("/register")
    assert resp.status_code == 200
    assert b"Create your account" in resp.data


def test_register_success_redirects_to_login(client):
    resp = post(client)
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/login")


def test_register_creates_user_with_hashed_password(client, user_count):
    before = user_count()
    post(client, email="  Asha@Example.COM ")
    assert user_count() == before + 1

    user = db.get_user_by_email("asha@example.com")
    assert user is not None
    assert user["name"] == "Asha Rao"
    assert user["password_hash"].startswith("pbkdf2:sha256")
    assert user["password_hash"] != VALID["password"]


def test_success_message_shown_on_login(client):
    resp = client.post("/register", data=VALID, follow_redirects=True)
    assert resp.status_code == 200
    assert b"Account created. Please sign in." in resp.data
    assert b"auth-success" in resp.data


def _assert_rejected(resp, message, user_count, before):
    assert resp.status_code == 400
    assert message.encode() in resp.data
    assert user_count() == before


def test_missing_name(client, user_count):
    before = user_count()
    _assert_rejected(post(client, name="   "), "Please enter your name.", user_count, before)


def test_invalid_email(client, user_count):
    before = user_count()
    for bad in ["", "no-at-sign", "a@b", "@example.com"]:
        _assert_rejected(
            post(client, email=bad), "Please enter a valid email address.", user_count, before
        )


def test_short_password(client, user_count):
    before = user_count()
    _assert_rejected(
        post(client, password="short"), "Password must be at least 8 characters.", user_count, before
    )


def test_duplicate_email(client, user_count):
    before = user_count()
    _assert_rejected(
        post(client, email="demo@spendly.com"),
        "An account with that email already exists.",
        user_count,
        before,
    )


def test_duplicate_email_case_insensitive(client, user_count):
    before = user_count()
    _assert_rejected(
        post(client, email="DEMO@Spendly.com"),
        "An account with that email already exists.",
        user_count,
        before,
    )


def test_form_repopulated_on_error(client):
    resp = post(client, password="short")
    assert b'value="Asha Rao"' in resp.data
    assert b'value="asha@example.com"' in resp.data
    assert b"short" not in resp.data
