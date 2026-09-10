# Recurring fundamentals and mentoring protocol

## How we work

The learner owns implementation. The mentor clarifies the requirement, explains a concept, gives a small hint, reviews the attempt, and only supplies a full solution when requested. A viewed solution should be followed by a small variant attempted independently. Setup work can create learning documents; it should not silently complete the assigned feature.

Each session: pick a ticket, build something small, run it, and record one result. Spend most time implementing/debugging. Save longer explanations and recall questions for the daily checkpoint so they do not block a usable first version.

## Parallel practice within the same learning journey

These are short exercises, not additional apps to build. Use roughly 15–30 minutes of recall or coding alongside project sessions; adjust to available time.

| Track | Sequence | Demonstrate without a copied solution |
|---|---|---|
| Python | Functions/scope → mutability/copies → classes/dataclasses → typing/exceptions → modules/imports → iterators/generators → context managers → async | Diagnose shared nested-list state; stream records; explain object versus dictionary; close a resource after an exception. |
| DSA | Arrays/strings, maps/sets → two pointers/sliding window → stacks/queues → sorting/binary search → heaps → trees/recursion → graphs/BFS/DFS → greedy → basic dynamic programming | Implement unfamiliar small variants; cover empty/boundary input; state time and space complexity; explain why the algorithm is correct. |
| Git | Status/diff → focused commits → branches → PR review → merge/conflict → revert/reset concepts | Make a ticket branch and focused diff; resolve a conflict in a disposable practice branch; explain when revert preserves shared history. |
| Terminal/Linux | Paths/files → environment and permissions → pipes/redirection → processes/ports/signals → logs | Find the process listening on a development port, inspect an environment setting, and trace a startup failure. Practice Linux-specific behavior in a container later. |
| SQL | CRUD/filters → joins → aggregates → constraints/transactions → indexes/query plans | Write SQL before introducing an ORM; explain duplicate rows in joins and why a transaction must roll back. |
| Systems | CPU/RAM/disk/cache and I/O → process/thread/memory → DNS/TCP/TLS/HTTP → blocking/async → races/locks | Trace a browser save from JSON to durable write and back; explain what TestClient bypasses; diagnose a slow or concurrent request. |
| Communication | Reproduce → isolate → fix → verify → explain tradeoff | Give a two-minute account of a bug, the evidence, and the smallest reliable fix. |

Use NutriTrack examples where natural: dictionaries for ID lookup, sorting meals by time, heaps for top-k foods, queues for imports, graphs for dependency traversal. Some interview patterns need standalone drills; do not force a graph algorithm into the API without a product reason.

## Recurring tickets

- **FND-PY:** Pick one Python concept used by the active ticket. Write a tiny example from memory and fix a deliberately introduced bug. Pass when you can explain the behavior and a changed input.
- **FND-DSA:** Solve one pattern problem, then a related variant on another day. Record time/space complexity and the point where your first approach failed. Revisit weak patterns before adding more topics.
- **FND-GIT:** Review only your ticket diff, stage intended files, and write a behavior-focused commit message. Preserve unrelated uncommitted work. Practice conflicts/reverts on a disposable branch when ready.
- **FND-SYS:** Trace one real request or failure using logs and process/port information. Draw the path only as far as you can explain it, then investigate the first missing step.
- **FND-REVIEW:** Once per study week or every 3–4 tickets, rebuild a small variation without AI-generated code and review one old mistake. Record `independent`, `needed hint`, or `needs revisit`; do not equate test count with mastery.

## Phase gates

**Before PostgreSQL:** independently define a nested input contract, write a schema rejection test, write an API test, and explain test isolation. Finish the small HTTP API slice even if some optional polish remains.

**Before deployment:** create a meal transactionally, write a real database integration test, distinguish validation from database constraints, enforce record ownership, and explain configuration/secrets. A container starting successfully is only one check.

**Before MLE:** demonstrate the backend with persistence, meaningful CI checks, one diagnosed failure, a simple performance measurement, and a rollback procedure. Continue DSA/SQL practice independently of the project.

**Before AI workflow frameworks:** demonstrate a measurable retrieval or prediction baseline, error analysis, and a failure-safe serving boundary. Only add a workflow framework when a real state/retry requirement justifies it.

## Early-career interview evidence

Maintain a small evidence log: a clean multi-file feature, a regression fix, a transaction/SQL explanation, an ownership test, a latency investigation, and an ML baseline comparison. Be able to sketch a client/API/database design and discuss caching, queues, replication, partitioning, availability, and consistency at a basic level. Implement only what NutriTrack needs.

Practice explaining project ownership accurately: which parts you wrote independently, where you received help, and what you learned. This is a portfolio and training path; company-specific interview formats vary.

## Completion record template

```text
Ticket:
Status: Ready / In progress / Review / Done / Blocked
Working behavior:
Relevant checks and results:
One bug or decision I can explain:
Help used:
Commit or diff:
Follow-up / next ticket:
```

## Current evidence

2026-09-09 setup: existing app tests run with the repository interpreter, `python -m pytest tests -q -p no:cacheprovider`: **3 passed**, one dependency deprecation warning. Direct model construction confirmed that blank names/empty ingredients and negative weights are currently accepted. NT-01 remains Ready. No feature completion is claimed.

## Deliberately lower priority

Kubernetes, Terraform, Spark internals, advanced microservices, distributed training, CUDA, deep frontend specialization, and agent frameworks wait until the earlier gates are demonstrated. The current frontend is enough to exercise backend work.
