# DRF Vocabulary API

A beginner-friendly Django REST Framework project for serving English vocabulary data from a Neon PostgreSQL database.

The API exposes vocabulary entries with:

- `headword`
- `part of speech`
- `CEFR level`

The project is intentionally small and clean, focused on learning the normal DRF flow:

```text
model -> serializer -> viewset -> router -> API endpoint
```

## Tech Stack

- Python 3.13
- Django 6
- Django REST Framework
- PostgreSQL / Neon
- `psycopg`
- `dj-database-url`
- `python-dotenv`

## Project Structure

```text
drf-vocabulary-api/
├── apps/
│   └── vocabulary/
│       ├── models.py
│       ├── serializers.py
│       ├── views.py
│       └── urls.py
├── config/
│   ├── settings.py
│   └── urls.py
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

Create a local `.env` file:

```bash
cp .env.example .env
```

Fill in your local values:

```env
DATABASE_URL=postgresql://USER:PASSWORD@HOST/DATABASE?sslmode=require
SECRET_KEY=your-local-django-secret-key
DEBUG=True
```

Run migrations:

```bash
python manage.py migrate
```

Start the development server:

```bash
python manage.py runserver
```

## API Endpoints

Vocabulary endpoints are available under:

```text
/api/vocabulary/
```

The router provides standard REST actions:

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/api/vocabulary/` | List vocabulary entries |
| `POST` | `/api/vocabulary/` | Create a vocabulary entry |
| `GET` | `/api/vocabulary/<id>/` | Retrieve one entry |
| `PUT` | `/api/vocabulary/<id>/` | Replace one entry |
| `PATCH` | `/api/vocabulary/<id>/` | Partially update one entry |
| `DELETE` | `/api/vocabulary/<id>/` | Delete one entry |

List responses are paginated by default:

```text
/api/vocabulary/?page=2
```

Vocabulary entries can be filtered by CEFR level and part of speech:

```text
/api/vocabulary/?cefr=A1
/api/vocabulary/?pos=verb
/api/vocabulary/?cefr=B1&pos=noun
```

Vocabulary entries can be searched by headword:

```text
/api/vocabulary/?search=abandon
/api/vocabulary/?search=well
```

## API Documentation

Generated API documentation is available through drf-spectacular:

| Endpoint | Description |
| --- | --- |
| `/api/schema/` | OpenAPI schema |
| `/api/docs/` | Swagger UI |
| `/api/redoc/` | ReDoc documentation |

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

The `data/` folder contains exported vocabulary data in three formats:

| File | Purpose |
| --- | --- |
| `vocabulary.csv` | Main import-friendly dataset |
| `vocabulary.json` | JSON export of the same vocabulary records |
| `vocabulary.xlsx` | Spreadsheet copy for inspection |

The current dataset contains `7974` vocabulary rows.

## Database Notes

The current Neon database uses PostgreSQL enum types for stricter validation:

- `cefr_level`
- `pos_type`

Django also mirrors these values with `TextChoices` in the `Vocabulary` model, so invalid values are rejected at the API/application layer before reaching the database.

The initial Django migration uses normal `CharField` columns with choices. On a fresh database, migrations will create valid application-level constraints, but they will not recreate the manual PostgreSQL enum types unless a custom SQL migration is added.

More details are documented in:

```text
docs/database-structure.md
```

## Import Script

The helper script imports rows from `data/vocabulary.csv`:

```bash
python scripts/import_vocabulary.py
```

Use it carefully. It inserts rows into the configured database and does not clear existing data first.

## Development Checks

Run Django's system check:

```bash
python manage.py check
```

## Current Limitations

- No authentication or permissions are configured yet.
- Filtering/search is not implemented yet.
- Duplicate `(headword, pos)` pairs should be reviewed before adding a unique constraint.
