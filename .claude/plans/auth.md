# Auth + CQRS — план реализации

## Context

FastAPI backend с готовым скелетом (зависимости, `core/security.py`, структура папок). Нужно добавить авторизацию (register/login/refresh), User-модель и CQRS-медиатор для изоляции модулей (auth не импортирует UserRepository напрямую — только DTOs команд/запросов).

---

## Чек-лист задач

### Шаг 1 — User ORM-модель
- [x] `app/models/user.py` — добавить поля: `id` (UUID PK, `default=uuid.uuid4`), `name`, `email` (unique, indexed), `hashed_password`, `created_at` (DateTime timezone)

### Шаг 2 — UserRepository
- [x] `app/repositories/user.py` — методы: `create(name, email, hashed_password) → User` (flush), `get_by_email → User | None`, `get_by_id → User | None`

### Шаг 3 — CQRS-инфраструктура
- [x] `app/cqrs/base.py` — `BaseCommand`, `BaseQuery`, `CommandHandler`, `QueryHandler`
- [x] `app/cqrs/mediator.py` — `Mediator`: `register(type, handler)`, `async send(message)`
- [x] `app/cqrs/__init__.py` — реэкспорт

### Шаг 4 — User-модуль (commands/queries/handlers)
- [x] `app/users/commands.py` — `CreateUserCommand(name, email, password)`
- [x] `app/users/queries.py` — `GetUserByEmailQuery(email)`, `GetUserByIdQuery(user_id)`
- [x] `app/users/handlers.py` — `CreateUserHandler` (проверка дубля email → 409), `GetUserByEmailHandler`, `GetUserByIdHandler`
- [x] `app/users/__init__.py` — пустой

### Шаг 5 — Auth-модуль (без прямых импортов user-логики)
- [x] `app/auth/commands.py` — `RegisterCommand(name, email, password)`, `LoginCommand(email, password)`
- [x] `app/auth/handlers.py` — `RegisterHandler(mediator)`, `LoginHandler(mediator)`. Используют только `mediator.send()` + DTOs из `users/commands.py` и `users/queries.py`. Не импортируют `UserRepository`, `CreateUserHandler` и т.д.
- [x] `app/auth/__init__.py` — пустой

### Шаг 6 — Схемы
- [x] `app/schemas/user.py` — добавить `name: str` в `UserCreate`; `id: UUID` в `UserRead`
- [x] `app/schemas/auth.py` — добавить `LoginRequest(email, password)` (без поля name)

### Шаг 7 — database.py
- [x] `app/database.py` — обернуть `get_db()` с `commit()` на выходе и `rollback()` при исключении

### Шаг 8 — dependencies.py
- [x] `app/core/dependencies.py` — `get_current_user_id` возвращает `UUID` (не `int`)
- [x] Добавить `get_mediator(session = Depends(get_db)) → Mediator` — регистрирует все хэндлеры per-request; импорты хэндлеров — внутри функции (предотвращает circular imports)

### Шаг 9 — API-роуты
- [x] `app/api/v1/auth.py`:
  - `POST /auth/register` → `RegisterCommand` → `TokenPair` (201)
  - `POST /auth/login` → `LoginCommand` → `TokenPair`
  - `POST /auth/refresh` → `decode_token` → новая пара (без DB, без медиатора)
- [x] `app/api/v1/users.py`:
  - `GET /users/me` → `GetUserByIdQuery` → `UserRead`

### Шаг 10 — Alembic
- [x] `migrations/env.py` — добавить `import app.models.user  # noqa: F401` перед `target_metadata`
- [ ] `uv run alembic revision --autogenerate -m "add users table"` *(требует запущенный PostgreSQL)*
- [ ] `uv run alembic upgrade head` *(требует запущенный PostgreSQL)*

---

## Ключевые файлы

| Файл | Роль |
|------|------|
| `app/cqrs/mediator.py` | Диспетчер команд/запросов |
| `app/core/dependencies.py` | Фабрика `get_mediator` (wiring per-request) |
| `app/auth/handlers.py` | **CQRS-граница**: auth не знает о user-репозитории |
| `app/users/handlers.py` | Бизнес-логика создания пользователя |
| `migrations/env.py` | Регистрация модели в Alembic |

---

## Проверка

```bash
# Применить миграцию
uv run alembic upgrade head

# Запустить сервер
uv run fastapi dev app/main.py

# Register
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice","email":"alice@example.com","password":"secret123"}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@example.com","password":"secret123"}'

# /me
curl http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer <access_token>"
```

Ожидаемые edge-cases:
- Дубль email → `409 Conflict`
- Неверный пароль → `401 Unauthorized`
- Невалидный токен → `401 Unauthorized`
