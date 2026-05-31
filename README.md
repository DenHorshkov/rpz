# Handmade Маркетплейс

Навчальний проєкт РПЗ: маркетплейс handmade-товарів на Django.

## Стек

- Python 3.11+, Django 5
- PostgreSQL 16
- Redis + Celery
- Groq API (чат-бот підтримки, Llama 3.3 70B)
- Bootstrap 5 (server-side rendered templates)
- Gunicorn + Nginx, Docker / docker-compose

## Локальний запуск (без Docker)

```bash
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
cp .env.example .env                 # Windows: copy .env.example .env
# відредагувати .env (SECRET_KEY, GROQ_API_KEY, DATABASE_URL)
python manage.py migrate
python manage.py loaddata fixtures/categories.json
python manage.py createsuperuser
python manage.py runserver
```

Окремо запустити Celery воркер:

```bash
celery -A config worker -l info
```

## Запуск через Docker

```bash
cp .env.example .env
docker compose up -d --build
docker compose exec web python manage.py createsuperuser
# відкрити http://localhost/
```

## Тести

```bash
pytest --cov=apps --cov-report=term-missing
```

## Структура

- `config/` — Django проєкт (settings: base/dev/prod, urls, celery)
- `apps/accounts/` — користувачі (custom User) та профілі майстрів
- `apps/catalog/` — товари, категорії, фото
- `apps/cart/` — сесійний кошик
- `apps/orders/` — замовлення, кнопка «Оплатити»
- `apps/reviews/` — відгуки та агрегований рейтинг
- `apps/support/` — чат-бот підтримки (Groq + Celery)
- `templates/`, `static/`, `media/` — Django MVT файли
- `nginx/`, `docker/` — конфіги для розгортання
- `tests/` — pytest-django тести

## Безпека (production-ready)

- `SECRET_KEY` / `DATABASE_URL` / `GROQ_API_KEY` — через `.env` (`django-environ`)
- CSRF middleware + `{% csrf_token %}` в усіх формах
- ORM-only запити (без raw SQL) → захист від SQL-ін'єкцій
- HTTPS-флаги вмикаються через `DJANGO_ENABLE_HTTPS=1` (HSTS, secure cookies, SSL redirect)
- `AUTH_PASSWORD_VALIDATORS`, `X_FRAME_OPTIONS=DENY`, `SECURE_CONTENT_TYPE_NOSNIFF`
- Rate-limit чат-бота (30 повідомлень/год на користувача через `django-ratelimit`)
- Ліміт розміру файлів 5 МБ для фото товарів / 3 МБ для аватарів
