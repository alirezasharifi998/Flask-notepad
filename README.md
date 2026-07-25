# Flask Notepad

A note-taking web app built with Flask, featuring a real filesystem-like folder structure — folders (called "Subjects") can be nested to any depth, just like directories on disk.

This is my first Flask project, built to learn the framework's application factory pattern, SQLAlchemy models, and database migrations.

## Features

- **Unlimited nested folders** — folders can contain sub-folders at any depth, mirroring a real filesystem tree
- Notes stored inside folders
- SQLite database via SQLAlchemy, with schema migrations handled by Flask-Migrate
- Flask shell context pre-loaded with `db`, `Subject`, and `Note` for quick debugging (`flask shell`)

## Tech Stack

- **Flask** — web framework
- **Flask-SQLAlchemy** — ORM / database layer
- **Flask-Migrate** — database schema migrations
- SQLite (default, configurable via the `DATABASE_URL` environment variable)

## Project Structure

```
Flask-notepad/
├── app/            // application package: models, routes, templates logic
├── migrations/     // Flask-Migrate schema migration history
├── static/         // CSS/JS/static assets
├── config.py       // app configuration (secret key, database URI)
├── notepad.py       // Flask shell context (exposes db, Subject, Note)
└── run_app.py      // convenience script to launch the dev server
```

## Setup

Requirements: Python 3

```bash
uv sync
```

Set environment variables (optional — sensible defaults are provided):

```bash
export SECRET_KEY="your-secret-key"
export DATABASE_URL="sqlite:///app.db"   # optional, defaults to a local sqlite file
export FLASK_APP=notepad.py
```

Apply database migrations:

```bash
uv run flask db upgrade
```

Run the development server:

```bash
uv run flask run
```

The app will be available at `http://127.0.0.1:5000/`.


