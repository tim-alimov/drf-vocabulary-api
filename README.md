# DRF Vocabulary API

A small Django REST Framework API for browsing English vocabulary entries stored in PostgreSQL.

The API exposes vocabulary records with:

- `headword`
- `pos` - part of speech
- `cefr` - CEFR level

It is intentionally compact, making it useful as a learning project or as a base for a production-ready vocabulary service.

## Tech Stack

- Python 3.13
- Django 6
- Django REST Framework
- PostgreSQL / Neon
- `psycopg`
- `dj-database-url`
- `django-filter`
- `drf-spectacular`
- `python-dotenv`

## Project Structure

```text
drf-vocabulary-api/
├── apps/
│   └── vocabulary/
│       ├── models.py
│       ├── serializers.py
│       ├── views.py
│       ├── urls.py
│       └── migrations/
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── data/
│   ├── vocabulary.csv
│   ├── vocabulary.json
│   └── vocabulary.xlsx
├── docs/
│   └── database-structure.md
├── scripts/
│   └── import_vocabulary.py
├── manage.py
├── requirements.txt
└── .env.example
```

## Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a local environment file:

```bash
cp .env.example .env
```

Fill in the required values:

```env
DATABASE_URL=postgresql://USER:PASSWORD@HOST/DATABASE?sslmode=require
SECRET_KEY=your-local-django-secret-key
DEBUG=True
```

Apply migrations:

```bash
python manage.py migrate
```

Start the development server:

```bash
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/api/vocabulary/
```

## API

Vocabulary endpoints are mounted under:

```text
/api/vocabulary/
```

The current viewset exposes the standard REST actions:

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/api/vocabulary/` | List vocabulary entries |
| `POST` | `/api/vocabulary/` | Create a vocabulary entry |
| `GET` | `/api/vocabulary/<id>/` | Retrieve one entry |
| `PUT` | `/api/vocabulary/<id>/` | Replace one entry |
| `PATCH` | `/api/vocabulary/<id>/` | Partially update one entry |
| `DELETE` | `/api/vocabulary/<id>/` | Delete one entry |

List responses are paginated with a default page size of `20`:

```text
/api/vocabulary/?page=2
```

### Filtering

Entries can be filtered by CEFR level and part of speech:

```text
/api/vocabulary/?cefr=A1
/api/vocabulary/?pos=verb
/api/vocabulary/?cefr=B1&pos=noun
```

### Search

Entries can be searched by `headword`:

```text
/api/vocabulary/?search=abandon
/api/vocabulary/?search=well
```

## API Documentation

OpenAPI documentation is generated with `drf-spectacular`:

| Endpoint | Description |
| --- | --- |
| `/api/schema/` | OpenAPI schema |
| `/api/docs/` | Swagger UI |
| `/api/redoc/` | ReDoc |

## Example Response

```json
{
  "count": 7974,
  "next": "http://127.0.0.1:8000/api/vocabulary/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "headword": "a",
      "pos": "determiner",
      "cefr": "A1"
    }
  ]
}
```

## Data

The `data/` directory contains exported vocabulary data in three formats:

| File | Purpose |
| --- | --- |
| `vocabulary.csv` | Main import-friendly dataset |
| `vocabulary.json` | JSON export of the same records |
| `vocabulary.xlsx` | Spreadsheet copy for inspection |

The current dataset contains `7974` vocabulary rows.

## Database Notes

The current Neon database uses PostgreSQL enum types for stricter validation:

- `cefr_level`
- `pos_type`

Django mirrors these values with `TextChoices` in `apps/vocabulary/models.py`, so invalid values are rejected by the application before insert.

The initial Django migration uses normal `CharField` columns with choices. Fresh databases created only from migrations will get application-level validation, but they will not recreate the manual PostgreSQL enum types unless a custom SQL migration is added.

More details are available in:

```text
docs/database-structure.md
```

## Importing Data

The helper script imports rows from `data/vocabulary.csv` into the configured database:

```bash
python scripts/import_vocabulary.py
```

Use it carefully. The script inserts rows and does not clear or deduplicate existing data first.

## Development Checks

Run Django's system check:

```bash
python manage.py check
```

Run Django's deployment checklist:

```bash
python manage.py check --deploy
```

Run tests:

```bash
python manage.py test
```

At the moment, the project does not include a real test suite.

## Production Readiness

This project is not production ready yet. Before deploying publicly, address at least the following:

- Add authentication and permissions, or make the vocabulary endpoint read-only.
- Configure `ALLOWED_HOSTS`, HTTPS redirects, HSTS, secure cookies, and CSRF trusted origins.
- Use a strong production `SECRET_KEY` and keep `DEBUG=False`.
- Add tests for listing, filtering, searching, validation, and write permissions.
- Add a deployment target such as Gunicorn/Uvicorn, Docker, or platform-specific config.
- Configure static file handling with `STATIC_ROOT` and a production serving strategy.
- Split runtime and development dependencies.
- Add indexes for common filters and search fields if the dataset grows.
- Decide whether Swagger, ReDoc, schema, and Django admin should be public.
- Make the import script idempotent or wrap it in a safer management command.

## License

This project is released under the MIT License. See `LICENSE` for details.
