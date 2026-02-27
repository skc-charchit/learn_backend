Project layout
==============

This repository contains a small backend project. The following describes the directory layout, the kinds of files each folder should contain, and the responsibilities for those files.

Root files
----------

- `docker-compose.yml`: Compose configuration for running the development services (Postgres, app containers, etc.). Keep service definitions, environment variable references, volumes, and any local overrides here.
- `Makefile`: Convenience targets for running common tasks (start, stop, build, test, lint). Targets should be small wrappers around the real commands used in development.
- `pyproject.toml`: Python project metadata and dependency configuration (tooling, packages, and build settings). Use this for declaring dependencies, dev dependencies, formatting and linting settings.
- `README.md`: This file — high-level documentation and usage notes.

localdev/
---------

Purpose: Local development-related files and helper data that should not be checked into production images.

- `localdev/data/learn_backend_pgdata/`: Postgres data directory used by the local Docker/Postgres service. This folder contains the database cluster files (configuration and WAL files). It is usually mounted as a Docker volume and should be managed carefully — avoid editing files inside while Postgres is running.

src/
----

All application source lives under `src/`. This repository uses a package named `learn_backend` (top-level package used when running or installing the app).

- `src/learn_backend/main.py`: Application entrypoint (if present). This file wires the app together and starts the server or CLI.
- `src/learn_backend/app/`: Main application package. Subfolders are organized by responsibility:

	- `api/`
		- Purpose: HTTP route and API layer (routers, endpoints, versioned blueprints).
		- Expected files: endpoint modules (for example `v1/`), request/response wiring, dependency injection bindings for route-level concerns, and API documentation (OpenAPI examples or route registration helpers).

	- `core/`
		- Purpose: Application core configuration and cross-cutting utilities.
		- Expected files: `config.py` for environment-based configuration values, `database.py` for DB initialization and session management, application-level constants, logger setup, and other infrastructure integration code.

	- `models/`
		- Purpose: Data model definitions.
		- Expected files: ORM models (SQLAlchemy models, for example) and any database-mapped classes. Keep only persistence-level model definitions here; translation to DTO/schema objects should happen elsewhere.

	- `schemas/`
		- Purpose: Validation and serialization schemas.
		- Expected files: Pydantic (or similar) request/response schemas, input validators, and serialization helpers. These are the boundary objects used by the API layer.

	- `services/`
		- Purpose: Business logic and domain services.
		- Expected files: Services, use-cases, and helper functions that implement application behavior (e.g., `todo_service.py` with create/read/update/delete logic). Services should be independent of transport (HTTP) and orchestrate models, repositories, and other lower-level components.

	- `__pycache__/` and other Python cache files
		- These are generated at runtime and should not be committed. Add them to `.gitignore`.

Notes on separation of concerns
------------------------------

- Keep transport (API layer) thin — it should translate incoming requests into schema objects, call services, and convert service results back to responses.
- Keep `models/` strictly tied to persistence. Do not leak ORM internals into API schemas; map between them in services or dedicated mappers.
- Put environment configuration in `core/config.py` and use a single place to read environment variables and defaults. Avoid scattering environment access across the codebase.

Other common folders
--------------------

- `tests/` (not present — recommended): Unit and integration tests. Typical layout mirrors `src/` (for example `tests/unit/`, `tests/integration/`). Use the same package import style as runtime code (install package in editable mode or configure PYTHONPATH in test runner).
- `scripts/` (optional): One-off scripts and developer helpers (database migrations, data load scripts). Keep them small and documented.

Best practices
--------------

- Keep modules small and focused: a module should group related responsibilities, not all concerns.
- Prefer explicit, well-named functions and classes in `services/` over monolithic modules.
- Document each package with a short `__init__.py` docstring or a short README in the package folder when responsibilities are non-obvious.
- Use `pyproject.toml` for dependency and tooling config and keep reproducible development environments (virtualenv, lockfile, or pinned versions).

What to put where — quick cheat sheet
------------------------------------

- Infrastructure and wiring: `src/learn_backend/app/core/` (config, DB, logging)
- HTTP/transport: `src/learn_backend/app/api/` (routers, endpoints)
- Business logic: `src/learn_backend/app/services/` (use cases)
- Persistence models: `src/learn_backend/app/models/` (ORM models)
- Validation/DTOs: `src/learn_backend/app/schemas/` (Pydantic schemas)
- Local development data: `localdev/data/`
- Project metadata and build: `pyproject.toml`, `Makefile`, `docker-compose.yml`

If you want, I can also:

- Add a short `CONTRIBUTING.md` with development setup steps.
- Add a `tests/` skeleton and a GitHub Actions workflow to run tests on push.

Folder structure — at a glance
-----------------------------

```
.
├── docker-compose.yml
├── Makefile
├── pyproject.toml
├── README.md
├── ruff.toml
├── src
│   └── learn_backend
│       ├── app
│       │   ├── api
│       │   │   ├── __init__.py
│       │   │   └── v1
│       │   │       ├── endpoints
│       │   │       │   ├── __init__.py
│       │   │       │   └── todos.py
│       │   │       ├── __init__.py
│       │   │       └── routers.py
│       │   ├── core
│       │   │   ├── config.py
│       │   │   ├── database.py
│       │   │   └── __init__.py
│       │   ├── models
│       │   │   ├── __init__.py
│       │   │   └── todo.py
│       │   ├── schemas
│       │   │   └── __init__.py
│       │   └── services
│       │       └── __init__.py
│       └── main.py
└── uv.lock

```