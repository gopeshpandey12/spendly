# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Spendly is a Flask expense tracker built step by step as a training exercise. Much of it is scaffolding: placeholder routes and stub files are marked with the step that implements them ("coming in Step 3", "Students will write this file in Step 1"). When implementing a step, replace the matching placeholder rather than adding a parallel route.

## Commands

The virtual environment lives in `venv/`. Each `!` shell command runs in a fresh shell, so `source venv/bin/activate` does not persist: call the venv binaries directly.

```bash
python3 -m venv venv                      # create the venv (once)
./venv/bin/pip install -r requirements.txt
./venv/bin/python app.py                  # dev server on http://localhost:5001 (debug on)
./venv/bin/pytest                         # run tests (pytest + pytest-flask; no tests yet)
./venv/bin/pytest path/to/test_file.py::test_name   # single test
```

There is no linter or build step configured.

## Architecture

- `app.py`: the whole Flask app with routes only. Page routes (`/`, `/login`, `/register`, `/terms`, `/privacy`) render templates; `/logout`, `/profile` and the `/expenses/...` add/edit/delete routes are string-returning placeholders.
- `database/db.py`: empty stub. It is meant to hold `get_db()` (SQLite connection with `row_factory` and foreign keys enabled), `init_db()` (`CREATE TABLE IF NOT EXISTS`) and `seed_db()` (sample data). The SQLite file `expense_tracker.db` is gitignored.
- `templates/`: Jinja templates extend `base.html`, which provides the navbar, footer (with Terms/Privacy links) and the `title`, `head` and `content` blocks. Links use `url_for(...)` with the route function names, so renaming a view function breaks templates.
- `static/`: `css/style.css` is global; `landing.css` and `landing.js` are used only by the landing page. `js/main.js` is an empty placeholder.

`conversation.md` is a saved chat transcript, not project documentation.

## Conventions

- The currency is Indian rupees (₹), e.g. the tagline "Track every rupee."
- Fonts are DM Serif Display and DM Sans, loaded from Google Fonts in `base.html`.
