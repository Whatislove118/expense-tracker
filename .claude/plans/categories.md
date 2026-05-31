# Categories Feature Plan

## Context

Auth и User-модули реализованы. Нужно добавить модуль Categories с CRUD, JWT-защитой и взаимодействием с User-модулем через CQRS.

Сущность Category: `id`, `name`, `color`, `icon`, `user_id` (FK → users).

---

## Checklist

### Model & Schema
- [ ] `backend/app/models/category.py` — SQLAlchemy-модель (`id`, `name`, `color`, `icon`, `user_id` FK)
- [ ] `backend/app/schemas/category.py` — Pydantic v2 схемы: `CategoryCreate`, `CategoryUpdate` (Optional-поля), `CategoryRead`

### Repository
- [ ] `backend/app/repositories/category.py` — `CategoryRepository` с методами:
  - `create(name, color, icon, user_id) -> Category`
  - `get_all_by_user(user_id) -> list[Category]`
  - `get_by_id(category_id) -> Category | None`
  - `update(category, ...) -> Category`
  - `delete(category) -> None`

### CQRS — Commands & Queries
- [ ] `backend/app/categories/commands.py` — `CreateCategoryCommand`, `UpdateCategoryCommand`, `DeleteCategoryCommand`
- [ ] `backend/app/categories/queries.py` — `GetCategoriesByUserIdQuery`

### CQRS — Handlers
- [ ] `backend/app/categories/handlers.py`:
  - `CreateCategoryHandler` — проверяет существование пользователя через `GetUserByIdQuery` (CQRS-взаимодействие с User-модулем), создаёт категорию
  - `GetCategoriesByUserIdHandler` — возвращает все категории пользователя
  - `UpdateCategoryHandler` — проверяет владельца (HTTP 403), обновляет
  - `DeleteCategoryHandler` — проверяет владельца (HTTP 403), удаляет

### API Router
- [ ] `backend/app/api/v1/categories.py` — FastAPI-роутер, все эндпоинты через `Depends(get_current_user_id)`:
  - `POST   /categories` → `CategoryRead` (201)
  - `GET    /categories` → `list[CategoryRead]`
  - `PATCH  /categories/{id}` → `CategoryRead`
  - `DELETE /categories/{id}` → 204

### Wiring
- [ ] `backend/app/api/v1/router.py` — подключить `categories.router` с prefix `/categories`
- [ ] `backend/app/core/dependencies.py` — зарегистрировать все handlers в `get_mediator()`
- [ ] `backend/migrations/env.py` — добавить `import app.models.category  # noqa: F401`

### Migration
- [ ] `uv run alembic revision --autogenerate -m "add categories table"`
- [ ] `uv run alembic upgrade head`

---

## Verification

1. `uv run fastapi dev app/main.py`
2. Открыть `http://localhost:8000/docs`
3. Register/login → получить токен
4. `POST /api/v1/categories` `{"name":"Food","color":"#FF5733","icon":"🍕"}` → 201
5. `GET /api/v1/categories` → список с созданной категорией
6. `PATCH /api/v1/categories/{id}` → обновлённые данные
7. `DELETE /api/v1/categories/{id}` → 204
8. PATCH/DELETE с токеном другого пользователя → 403
