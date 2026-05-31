# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Expense tracker monorepo with two independent apps:
- `backend/` — Python 3.12, FastAPI async, SQLAlchemy async, PostgreSQL, Alembic, JWT auth
- `frontend/` — Next.js 15, TypeScript, App Router

## Backend

**Package manager:** `uv`

```bash
cd backend
uv sync                        # install dependencies
uv run fastapi dev app/main.py # dev server (port 8000)
uv run pytest                  # run all tests
uv run pytest tests/test_x.py::test_name  # single test
uv run alembic revision --autogenerate -m "description"  # new migration
uv run alembic upgrade head    # apply migrations
```

### Architecture

Strict layered architecture — each layer only calls the one below it:

```
api/v1/     →  Route handlers (FastAPI routers), no business logic
services/   →  Business logic, orchestrates repositories
repositories/ → Raw async SQLAlchemy queries, returns ORM models
models/     →  SQLAlchemy ORM table definitions (inherit from Base in database.py)
schemas/    →  Pydantic v2 request/response models (separate from ORM models)
core/       →  Cross-cutting: security.py (JWT + bcrypt), dependencies.py (FastAPI Depends)
config.py   →  pydantic-settings Settings class, reads from .env
database.py →  async engine, AsyncSessionLocal, Base, get_db() dependency
```

All DB access is async (`AsyncSession`, `asyncpg` driver). New models must inherit from `Base` in `database.py` and be imported in `migrations/env.py` so Alembic detects them.

JWT: access token (30 min) + refresh token (30 days). Auth flow lives in `core/security.py` (encode/decode) and `core/dependencies.py` (`get_current_user_id` FastAPI dependency). Routes that require auth use `Depends(get_current_user_id)`.

Copy `.env.example` → `.env` and set `DATABASE_URL` and `JWT_SECRET` before running.

## Frontend

**Package manager:** npm

```bash
cd frontend
npm install
npm run dev    # dev server (port 3000)
npm run build
npm run lint
```

### Architecture

Next.js App Router with route groups:
- `(auth)/` — public pages: login, register
- `(dashboard)/` — protected pages: dashboard, expenses

```
src/
  app/         # Pages and layouts (App Router)
  components/
    ui/        # Generic reusable components
    features/  # Domain-specific components (auth/, expenses/)
  lib/api/     # API client — apiFetch wrapper in client.ts, endpoint modules alongside
  hooks/       # Custom React hooks
  types/       # TypeScript interfaces mirroring backend Pydantic schemas
```

API base URL is read from `NEXT_PUBLIC_API_URL` (see `.env.local.example`).

## Git Workflow

Use **GitHub Flow**:

1. **Create a feature branch** from `main`: `git checkout -b feature/your-feature-name`
   - Branch naming: `feature/`, `fix/`, `docs/`, `refactor/`, `test/`, `ci/` prefix
   - Use kebab-case: `feature/main-screen`, `fix/auth-bug`

2. **Commit your changes** to the feature branch
   - Push regularly: `git push -u origin feature/your-feature-name`

3. **Create a pull request** when ready for review
   - PR title should match commit convention
   - Describe what changed and why

4. **Review and merge** to `main`
   - Rebase before merging (keep history clean): `git rebase main`
   - Use "Create a merge commit" or "Squash and merge" (no fast-forward)
   - Delete the feature branch after merging

5. **Never force-push** to `main` or shared branches

## Commit convention
Use Conventional Commits:
 - Type: feat, fix, docs, refactor, test, ci 
 - Scope: module or area of changes
 - Description on English, shortly
 - Breaking changes mark with ! symbol