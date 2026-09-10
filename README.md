# NutriTrack

A Python API project for learning to build and operate a food and nutrition tracker.
The planned product will accept meal photos, estimate nutrition, and track meals
over time. The current version lets you record a meal with one ingredient through
a browser form, then view your meals. The API supports multiple ingredients.

## Requirements

- Python 3.14 or newer (the project currently selects Python 3.14).
- uv for managing dependencies and running commands.

Run the commands below from the repository root.

## Install dependencies

```bash
uv sync --locked
```

This creates the local `.venv` environment and installs application and development
dependencies using the committed `uv.lock` file.

## Run locally

```bash
uv run uvicorn app.main:app --reload
```

The development server listens at http://127.0.0.1:8000. The `--reload` option
restarts it when application code changes. Press Ctrl+C to stop the server.

Open http://127.0.0.1:8000 to use the meal journal. Enter a meal name, ingredient,
and weight in grams, then click **Save meal**. The list refreshes after saving.
Meals are stored in memory: new entries disappear when the server restarts,
including when `--reload` restarts it after a code change. Two sample meals are
loaded at startup.

## Check the API

With the server running, open http://127.0.0.1:8000/health in a browser or run this
command in another terminal:

```bash
curl http://127.0.0.1:8000/health
```

Expected response: HTTP `200 OK` with this JSON body:

```json
{"status": "ok"}
```

Interactive API documentation is available at http://127.0.0.1:8000/docs.

## Run tests

```bash
uv run python -m pytest -q
```

The test uses FastAPI's test client, so you do not need to start the server first.
The tests cover the health endpoint and creating, retrieving, and listing meals.

## Project layout

- `app/main.py`: FastAPI application and routes.
- `app/static/index.html`: meal form and list structure.
- `app/static/style.css`: page styles and mobile layout.
- `app/static/app.js`: form submission and meal listing through the API.
- `tests/test_health.py`: automated health endpoint test.
- `tests/test_meals.py`: meal API tests.
- `pyproject.toml`: project metadata and dependency declarations.
- `uv.lock`: resolved dependency versions; commit changes to this file.
- `main.py`: starter script generated during initialization; the API uses `app/main.py`.

The service currently has no database or photo analysis. The browser checks names
and positive weights; equivalent API validation is a future task.
No API keys or environment variables are required to run it. `.env` and `.venv`
are ignored by Git.

## Learning curriculum

Continue from schemas and pytest with [the current ticket](learning/CURRENT.md).
The [curriculum](learning/README.md) contains 32 staged backend SWE → MLE tickets,
with [the full queue](learning/TICKETS.md) and [fundamentals/review guidance](learning/LEARNING.md).
Current starting ticket: **NT-01 — Define meal schemas**.
