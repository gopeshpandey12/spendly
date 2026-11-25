# Spec: Registration (Step 2)

## Overview
Make the existing `/register` page work: accept the form POST, validate the input,
create a user row with a hashed password, and send the new user to the login page.
Logging in and sessions are Step 3; this step only creates accounts.

## Depends on
- Step 1: database setup (`users` table, `get_db()` in `database/db.py`).

## Routes
- `GET /register` — render `register.html` (already exists).
- `POST /register` — handle the form. Change the existing `register` view to
  `methods=["GET", "POST"]`; do **not** add a parallel route. Keep the function
  name `register` (templates use `url_for('register')`).

## Database changes
None. Uses the existing `users` table (`name`, `email` UNIQUE, `password_hash`).

## Templates
- **Modify** `templates/register.html`:
  - Repopulate `name` and `email` inputs with submitted values on error
    (`value="{{ name or '' }}"`, `value="{{ email or '' }}"`). Never repopulate the password.
  - Change `action="/register"` to `action="{{ url_for('register') }}"`.
  - Add `minlength="8"` to the password input.
- **Modify** `templates/login.html`: show a success message when redirected after
  registration (see below). Reuse existing auth styling; add an `.auth-success`
  class to `static/css/style.css` modelled on `.auth-error` (green instead of red).

## Files to change
- `app.py` — POST handling for `register`; add `request`, `redirect`, `url_for`,
  `flash` imports; set `app.secret_key` (dev value, e.g. from `os.environ.get("SECRET_KEY", "dev")`) so `flash` works.
- `database/db.py` — add helpers:
  - `get_user_by_email(email)` → row or `None`
  - `create_user(name, email, password)` → new user id; hashes the password with
    `generate_password_hash(password, method="pbkdf2:sha256")`
    (the venv's Python lacks scrypt, so the method must be explicit).
- `templates/register.html`, `templates/login.html`, `static/css/style.css` as above.

## Files to create
- `tests/test_registration.py`

## New dependencies
None.

## Rules for implementation
- Parameterised SQL only (`?` placeholders), never string formatting.
- Strip whitespace from `name` and `email`; lowercase `email` before checking and storing.
- Never store or log the plain password.
- Validation errors re-render `register.html` with status 400 and an `error` message;
  the template already displays `{{ error }}`.
- On success: `flash("Account created. Please sign in.")` and
  `redirect(url_for("login"))` (POST/redirect/GET).
- Also handle `sqlite3.IntegrityError` on insert as "email already registered"
  (race between the check and the insert).
- Close DB connections (`try/finally`), as `db.py` already does.

## Validation
| Field    | Rule                                   | Error message                                   |
|----------|----------------------------------------|-------------------------------------------------|
| name     | required, non-blank after strip        | "Please enter your name."                       |
| email    | required, contains `@` and a `.` after it | "Please enter a valid email address."        |
| password | at least 8 characters                  | "Password must be at least 8 characters."       |
| email    | not already in `users`                 | "An account with that email already exists."    |

## Definition of done
- [ ] `GET /register` still renders the form (200).
- [ ] Valid POST creates exactly one `users` row with a lowercased email and a
      `pbkdf2:sha256` hash (not the plain password), then redirects to `/login`.
- [ ] `/login` shows "Account created. Please sign in." after that redirect.
- [ ] Each invalid case returns 400, shows its message, keeps name/email filled, and creates no row.
- [ ] Registering `demo@spendly.com` (seeded) or the same email in different case fails with the duplicate message.
- [ ] `./venv/bin/pytest` passes, with tests using a temporary database (patch `database.db.DB_PATH`), not `expense_tracker.db`.
