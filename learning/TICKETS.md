# NutriTrack ticket queue

Only NT-01 is Ready at setup; NT-02–32 are Backlog. Progress is recorded here and in LEARNING.md after review. Dependencies below are minimum prerequisites, and the default order is numerical. Future tickets are scoped work briefs; split them into smaller implementation slices when activated. NT-30–32 are optional extensions after the MLE bridge.

Every ticket includes a working result, behavioral acceptance checks, and something to explain. Read CURRENT.md for the expanded first four tickets.

## Phase 1 — Schemas, pytest, and debugging

### NT-01 — Define meal schemas

**Status:** Ready. **Depends:** current app. **Learn:** nested models, fields, imports, request/response contracts.

**Build:** move schemas to `app/schemas/meal.py`, enforce nonempty names/lists and positive grams, add MealResponse to POST while retaining UUID-string IDs and full ingredient responses.

**Accept:** valid create/get works; invalid model input fails; existing application tests pass. **Explain:** Pydantic instance versus nested dictionary. [Full ticket](CURRENT.md#nt-01--make-valid-meal-input-an-explicit-contract).

### NT-02 — Test schema rules directly

**Depends:** NT-01. **Learn:** assertions, exceptions, parametrization, boundary cases.

**Build:** direct model tests in `tests/test_meal_schemas.py`.

**Accept:** valid nesting/serialization, missing fields, empty fields, zero/negative weights, and a small positive weight are covered; demonstrate a test failing when its constraint is removed. **Explain:** why an expected exception makes a test pass. [Full ticket](CURRENT.md#nt-02--prove-schema-behavior-with-pytest).

### NT-03 — Test HTTP and isolate mutable state

**Depends:** NT-02. **Learn:** TestClient, fixtures, yield/teardown, deep copies, HTTP errors.

**Build:** independent API tests using the seeded dictionary and a restoration fixture.

**Accept:** 201/422/404 behavior, unique IDs, persisted record shape, invalid requests leaving state unchanged, and reliable tests in different file orders. **Explain:** schema exceptions versus HTTP responses. [Full ticket](CURRENT.md#nt-03--prove-the-http-boundary-and-isolate-storage).

### NT-04 — Define edge-case input policy

**Depends:** NT-03. **Learn:** normalization, finite numbers, coercion, unknown fields.

**Build:** trim names, reject blanks and non-finite/nonpositive weights, reject extra request fields; preserve documented numeric-string coercion.

**Accept:** test each new rule directly and applicable valid-JSON cases through HTTP; valid browser flow remains usable. **Explain:** policy versus library defaults. [Full ticket](CURRENT.md#nt-04--harden-the-edge-cases-after-the-first-working-slice).

### NT-05 — Fix a bug through evidence

**Depends:** NT-03. **Learn:** tracebacks, breakpoints/logging, regression tests, code review.

**Build:** reproduce one observed defect, or use a deliberate fixture-aliasing bug in a disposable exercise. Write a failing behavioral test, make the smallest fix, then refactor only if useful.

**Accept:** demonstrate the same test failing before and passing after; review the diff; record the cause. Do not invent a production bug if none exists. **Explain:** why a shallow copy may share nested objects.

## Phase 2 — Python and backend structure

### NT-06 — Search and paginate meals

**Depends:** NT-04. **Learn:** query parameters, optional values, filtering, sorting, complexity.

**Build:** retain the existing case-insensitive exact-name filter; add validated offset/limit pagination with a documented deterministic order. Keep GET /meals returning a list so the page remains compatible.

**Accept:** absent filter, mixed-case name, empty result, invalid bounds, and adjacent pages without overlap work. **Explain:** time/space cost and why insertion order is not a durable database ordering contract.

### NT-07 — Separate routes, services, and storage

**Depends:** NT-06. **Learn:** functions/classes, typed boundaries, dependency injection, exception mapping.

**Build:** a small meal service and in-memory repository; routes handle HTTP, services express behavior, repositories store/retrieve. Add GET response models without changing response shape.

**Accept:** existing contract tests stay green; a service unit test runs without HTTP; API tests receive isolated repository instances. **Explain:** why this separation will allow PostgreSQL to replace memory without rewriting validation. Avoid generic base-class frameworks.

### NT-08 — Import a small meal file safely

**Depends:** NT-07. **Learn:** iterators/generators, context managers, exceptions, modules, command-line arguments.

**Build:** a local JSON-lines import command using the same schemas/service. Define per-record success/failure reporting and stream input instead of loading everything at once.

**Accept:** valid lines import, malformed lines have useful line-number errors, an empty file is handled, and a failed record does not corrupt another. **Explain:** generator laziness and why file resources close after an exception.

### NT-09 — Add useful quality checks

**Depends:** NT-07. **Learn:** types versus runtime checks, linting, formatting, dependency management.

**Build:** a minimal formatter/linter and type-checking setup; declare directly imported libraries explicitly and review the lockfile. Inspect whether both httpx and httpx2 are needed before removing anything.

**Accept:** documented local commands pass for the app and its tests; no blanket ignores conceal type errors; classify separate practice/tool suites rather than accidentally excluding required checks. **Explain:** one bug types catch and one they cannot catch.

## Phase 3 — SQL and persistence

### NT-10 — Model meals in PostgreSQL with SQL first

**Depends:** NT-07. **Learn:** relational modeling, primary/foreign keys, CRUD, joins, constraints.

**Build:** local PostgreSQL tables `meals` and `meal_ingredients`; each ingredient entry stores its amount in that meal. Resolve ID compatibility explicitly: retain text IDs initially because seeded IDs are not UUIDs, or plan a reviewed seed migration before changing types.

**Accept:** insert/read/update/delete using parameterized SQL; query a meal with its ingredients; reject orphan ingredients and invalid weights at the database boundary. **Explain:** why grams belongs on the meal's ingredient entry. No ORM until these queries are understood.

### NT-11 — Make meal writes atomic and durable

**Depends:** NT-10. **Learn:** transactions, commit/rollback, connections, SQL injection prevention.

**Build:** PostgreSQL repository behind the existing service. Save the meal and every ingredient in one transaction.

**Accept:** create/get/list survive an app restart; a forced ingredient-write failure leaves no partial meal; a name containing quotes is stored as data. **Explain:** what changes in memory, what becomes durable, and who owns the transaction.

### NT-12 — Version database changes

**Depends:** NT-11. **Learn:** migrations, schema/model distinction, ORM mapping tradeoffs.

**Build:** introduce a migration tool and one additive change; map the repository through SQLAlchemy if useful, while retaining the ability to read the SQL. Document a safe rollback or roll-forward approach.

**Accept:** a fresh database migrates from zero; upgrading an existing database preserves rows; integration checks cover the resulting schema. **Explain:** why a Pydantic schema cannot replace a database migration.

### NT-13 — Test against real PostgreSQL

**Depends:** NT-12. **Learn:** integration tests, fixtures, cleanup, test database isolation.

**Build:** run repository/API persistence tests against a dedicated test database. Choose transaction rollback or explicit cleanup based on how the app acquires connections.

**Accept:** tests do not touch development records; repeat runs agree; rollback and database constraints are tested; one full HTTP → database → HTTP flow is verified. **Explain:** why mocks or SQLite alone would miss PostgreSQL-specific behavior.

### NT-14 — Measure a query and choose an index

**Depends:** NT-13. **Learn:** JOIN, GROUP BY, indexes, query plans, measurement.

**Build:** an aggregate report and a repeatable synthetic dataset; inspect a query plan before and after one justified index.

**Accept:** aggregates match hand-calculated examples; record row count, plan, and timings; explain any lack of improvement. **Explain:** index read benefit, write/storage cost, and why small datasets can mislead.

## Phase 4 — A useful tracker with ownership

### NT-15 — Record when a meal was eaten

**Depends:** NT-14. **Learn:** domain modeling, migrations, timestamps/time zones, API evolution.

**Build:** separate reusable meal definitions from dated meal-log entries with serving amounts; add history/date filtering without silently changing existing /meals semantics.

**Accept:** the same meal can be logged twice; daily boundaries use a documented user time zone; midnight and a daylight-saving boundary are tested. **Explain:** reusable recipe versus consumption event and which facts must be snapshotted.

### NT-16 — Enforce user ownership

**Depends:** NT-15. **Learn:** authentication versus authorization, dependency boundaries, secrets.

**Build:** choose a maintained authentication approach and derive identity from verified credentials; scope meals/logs by owner. Document token expiry and unauthenticated behavior.

**Accept:** missing/invalid credentials fail; user A cannot read or mutate user B's records; cross-user IDs are tested, not just hidden in the UI. **Explain:** why trusting a request body's user_id does not authorize access.

### NT-17 — Add a versioned food catalog and nutrition calculation

**Depends:** NT-16. **Learn:** units, Decimal/rounding choices, pure functions, provenance, foreign keys.

**Build:** a small food catalog with nutrient amounts per 100 g, source/version metadata, and an explicit ingredient-to-food selection. Compute contribution as nutrient_per_100g × grams / 100.

**Accept:** hand-calculated totals agree; unknown foods are reported rather than assigned invented nutrients; rounding and units are documented; changing catalog data does not silently rewrite historical logged totals. **Explain:** why food identity and portion weight are different uncertainties.

### NT-18 — Return daily totals and update logs safely

**Depends:** NT-17. **Learn:** aggregates, service rules, update semantics, deterministic tests.

**Build:** daily energy/macronutrient summaries and one log-edit flow with explicit missing/null/unchanged field behavior.

**Accept:** empty days, multiple meals, edits/deletes, ownership, and time-zone boundaries produce expected totals. **Explain:** where aggregation belongs and whether storing derived totals introduces consistency work.

## Phase 5 — Production engineering and systems

### NT-19 — Run the app and database in containers

**Depends:** NT-18. **Learn:** image/container distinction, layers, volumes, ports, processes, environment settings.

**Build:** a Dockerfile and local Compose setup with durable database storage and explicit configuration. Handle secrets outside committed files/images.

**Accept:** clean startup is documented; database records survive container replacement with the volume retained; missing configuration has a clear error. **Explain:** host versus container networking and why localhost changes meaning.

### NT-20 — Automate review checks with CI

**Depends:** NT-19, NT-09. **Learn:** CI stages, reproducible installs, builds, PR review.

**Build:** a GitHub Actions workflow for application tests, real database integration tests, quality checks, and image build. Run separate practice suites only under their intended dependencies.

**Accept:** demonstrate a deliberately failing change being caught on a practice branch; a clean checkout can reproduce checks. **Explain:** what CI proves and what still requires deployment verification.

### NT-21 — Make failures diagnosable

**Depends:** NT-20. **Learn:** structured logs, request IDs, metrics, traces, health/readiness, incident reasoning.

**Build:** request correlation, request count/error/latency metrics, a database readiness check, and a minimal dashboard or documented metrics view. Avoid logging tokens or full private meal payloads.

**Accept:** stop the test database, locate the failure from a request ID, and distinguish liveness from readiness; document one actionable alert and runbook. **Explain:** logs versus metrics versus traces and one useful trace boundary.

### NT-22 — Measure concurrency and failure behavior

**Depends:** NT-21. **Learn:** I/O versus CPU, sync/async, threads/processes, races/locks, pools/timeouts.

**Build:** a modest repeatable load scenario and one concurrent-update experiment. Record dataset, request mix, concurrency, latency percentiles, throughput, and errors before changing anything.

**Accept:** identify a measured bottleneck; apply one justified improvement or explain why no change is warranted; reproduce a race and enforce an appropriate transaction/locking rule. **Explain:** why async does not speed CPU work automatically, and when a cache or queue would help.

### NT-23 — Deploy and rehearse rollback

**Depends:** NT-22. **Learn:** compute/storage, managed databases, IAM, TLS/networking, secrets, backups, release operations.

**Build:** a reviewed deployment plan with resource/cost bounds, one chosen environment, least-privilege access, and a release/runbook. Obtain the user's target and budget before any paid provisioning.

**Accept:** in the chosen environment demonstrate smoke checks, logs, restart persistence, a backup restore, and application rollback with database compatibility addressed. Local rehearsal is useful but is not evidence of a completed cloud deployment. **Explain:** trace DNS → TCP → TLS → HTTP → app → database and identify single points of failure.

## Phase 6 — MLE bridge: food matching first

### NT-24 — Define an ML task and curate data

**Depends:** NT-23. **Learn:** datasets, labels, leakage, data validation, ETL/batch jobs.

**Build:** a versioned dataset mapping typed ingredient text to catalog food IDs; document source/permission, duplicate policy, schema, unknown-label handling, and intended users. Use safe sample data rather than exporting private logs by default.

**Accept:** input validation catches bad records; split by food/alias group where needed to prevent near-duplicate leakage; lock a held-out test set. **Explain:** training/validation/test roles and why synthetic examples alone do not establish real-world accuracy.

### NT-25 — Establish a deterministic baseline

**Depends:** NT-24. **Learn:** evaluation design, precision/recall, top-k retrieval, slice analysis.

**Build:** exact/normalized or fuzzy catalog matching and an offline evaluator; define top-1 accuracy, top-k recall, unknown-input handling, and latency measures before training a model.

**Accept:** report sample counts and errors by slice; store dataset/config versions; inspect failures such as raw/cooked and similar names. **Explain:** why a single average score can hide an unusable category.

### NT-26 — Train one small learned matcher

**Depends:** NT-25. **Learn:** features, loss/optimization, overfitting, bias/variance, model selection.

**Build:** a simple text classifier or ranking pipeline appropriate to the available catalog/data; fit preprocessing on training data only. Select settings on validation data and compare with NT-25.

**Accept:** reproducible training command; validation comparison with the baseline; one final held-out evaluation after choices are fixed; report failures and limited-data uncertainty. **Explain:** the objective, model output, and why better training accuracy can mean worse generalization. Do not force a model into production if it loses to the baseline.

### NT-27 — Package a reproducible training artifact

**Depends:** NT-26. **Learn:** serialization, experiment/data/model versions, offline inference, reproducibility.

**Build:** a training command producing preprocessing + model + label mapping + metadata together, plus a batch prediction command. Record code version, seed, environment, dataset hash, parameters, and metrics.

**Accept:** trusted artifact reload gives equivalent predictions within documented tolerance; incompatible versions fail clearly; batch output records the model version. **Explain:** training-serving skew and why untrusted serialized model files must not be loaded.

### NT-28 — Serve suggestions through the API

**Depends:** NT-27. **Learn:** model lifecycle, online inference, batching, latency/throughput, dependency testing.

**Build:** a typed food-suggestion endpoint; load the selected artifact at startup, return versioned candidates, and require user selection before changing a meal's food mapping. Benchmark CPU serving before considering GPU infrastructure.

**Accept:** valid/unknown input, artifact-unavailable behavior, timeout/fallback, deterministic test doubles, and measured latency are covered. **Explain:** why an uncalibrated score is not necessarily a probability and why loading a model per request is costly.

### NT-29 — Monitor and roll back an ML release

**Depends:** NT-28. **Learn:** drift, delayed labels, shadow evaluation, A/B concepts, model rollback.

**Build:** a small version comparison/shadow replay and monitoring for errors, latency, unknown rate, and user corrections with appropriate data minimization. Define when to roll back to a previous model or deterministic matcher.

**Accept:** intentionally bad candidate performance prevents promotion or triggers rollback; record offline versus observed production evidence honestly. **Explain:** distribution shift versus measured quality loss, selection bias in corrections, and why an A/B test needs a sample-size/decision plan.

## Phase 7 — Optional AI extensions after the foundations

### NT-30 — Evaluate photo-to-ingredient drafts

**Depends:** NT-29. **Learn:** multimodal model boundary, structured output, upload validation, evaluation, uncertainty.

**Build:** photo analysis behind a provider interface returning editable ingredient suggestions. Choose a model/provider and cost envelope when activating this ticket. Never treat a photo-derived portion estimate as measured weight.

**Accept:** file size/type checks, malformed provider output, timeouts, an explicit user-confirmation save flow, and a labeled photo evaluation with food/portion error analysis. **Explain:** limitations, latency/cost tradeoffs, and why plausible text is not evidence of accurate nutrition.

### NT-31 — Build and evaluate grounded food search

**Depends:** NT-29. **Learn:** tokens/context, embeddings/cosine similarity, retrieval, chunking, grounding, regression evaluation.

**Build:** retrieval over a small permitted food-reference corpus with source metadata; compare lexical search with semantic/hybrid retrieval before adding generated explanations.

**Accept:** a frozen query set measures retrieval recall and, if generation is used, answer support/citations, failure/abstention, latency, and cost. **Explain:** one chunking/filtering choice and a case where retrieval succeeds but the answer fails. Reranking is added only if evaluation justifies it.

### NT-32 — Make a bounded stateful workflow reliable

**Depends:** NT-30 or NT-31. **Learn:** job queues, state transitions, retries/backoff, idempotency, tool boundaries.

**Build:** one asynchronous import/analysis workflow with explicit states, a retry limit, a durable job record, and a user-confirmation boundary before saving suggested changes. Start with plain code; use a framework only for a demonstrated need.

**Accept:** duplicate delivery does not duplicate meals; retries stop; failed jobs are inspectable; process restart resumes or safely marks unfinished work. **Explain:** at-least-once delivery, retry-safe effects, and the difference between workflow reliability and model answer quality.
