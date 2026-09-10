# NutriTrack: backend SWE → MLE curriculum

Start with [CURRENT.md](CURRENT.md). The complete queue is in [TICKETS.md](TICKETS.md); recurring fundamentals and review rules are in [LEARNING.md](LEARNING.md).

## Target and product

Build the habits and demonstrable skills needed for an early-career backend SWE role, then extend the same system into MLE. “FAANG associate level” is a preparation target here, not a standardized credential or a hiring guarantee. Project work, coding interviews, SQL, debugging, and explaining design decisions all need practice.

NutriTrack will let someone record meals and ingredients, retrieve their history, and calculate nutrition from a versioned food catalog. Later it will propose food matches or photo-derived ingredients, measure those predictions against labeled examples, and let the user correct them before saving. Keep deterministic nutrition calculations separate from uncertain model predictions.

Build a working slice, use it, then improve it. The first pass should be small. Required correctness checks still belong to that slice; optional polish can go into a follow-up ticket.

## Verified starting point — September 9, 2026

Repository: `/Users/dongwookkim/code/nutritrack`.

- The app has a browser meal-entry page, `/health`, `POST /meals`, `GET /meals`, and `GET /meals/{meals_id}`.
- `IngredientCreate` and `MealCreate` live in `app/main.py`. They have type annotations but no constraints on empty names, empty ingredients, or nonpositive grams.
- Meals live in `meals_content`, a dictionary with two seeded meals. New IDs are UUID strings. Preserve this contract while learning schemas; the integer-ID recipe exercise was a separate exercise.
- `tests/test_health.py` and `tests/test_meals.py` contain **3 tests**, all passing in the repository's current environment. That command covers the application tests, not the separate practice/tool suites.
- The current API tests mutate shared storage without a reset fixture. There are no direct schema tests under `tests/`.
- Python 3.14.5, FastAPI 0.141.1, Pydantic 2.13.5, and pytest 9.1.1 were observed locally. Keep the existing lockfile and environment for the current tickets.
- Existing uncommitted work includes the app, README, frontend, practice material, and tools. Curriculum setup does not imply those changes have been reviewed or committed.

An implementation exists for the basic API. Independent mastery of it is still to be demonstrated. Previously viewing a worked solution does not count as completing a ticket.

## Route through the project

| Phase | Tickets | Working result / exit demonstration |
|---|---|---|
| 1. Schemas and testing | NT-01–05 | Reject invalid meals; show schema and HTTP tests, independent storage, and a reproducible bug fix. |
| 2. Python and backend structure | NT-06–09 | Search and paginate meals; import validated records; explain routes, services, and repositories. |
| 3. SQL and persistence | NT-10–14 | Save a meal and its ingredients atomically in PostgreSQL; survive restart; demonstrate a migration and an index decision. |
| 4. A useful, private tracker | NT-15–18 | Track dated meal logs, enforce ownership, and calculate daily totals with documented units. |
| 5. Production engineering | NT-19–23 | Build and test a container; diagnose a failure; demonstrate measured performance, deployment, and rollback. |
| 6. MLE bridge | NT-24–29 | Build a versioned dataset, compare a learned food matcher with a baseline, serve it, and monitor/roll it back. |
| 7. AI extensions, later | NT-30–32 | Evaluate optional photo extraction and retrieval, then implement a bounded stateful workflow if it adds value. |

DSA, Git, terminal/Linux, Python fundamentals, and systems reasoning run alongside these phases. Use the recurring drills in [LEARNING.md](LEARNING.md). Do not postpone them until the ML phase.

## Ticket workflow

Status values: `Ready`, `In progress`, `Review`, `Done`, `Backlog`, `Blocked`.

1. Keep one implementation ticket in progress. Read its behavior and acceptance checks.
2. Attempt a small working slice; ask for a concept explanation or one hint when stuck.
3. Run the relevant checks, show a visible result, and explain one design choice.
4. Record evidence and unresolved follow-ups. Mark `Done` only after the required checks work and you can explain the change.

No fixed weekly pace is assumed. Early tickets are roughly one or two focused sessions; later tickets may need several. Split a later ticket into a thin vertical slice if it becomes too large. Use successful demonstrations, rather than elapsed weeks, to advance.

Current status: **NT-01 Ready**. NT-02 follows immediately. Nothing new is marked completed by this setup.
