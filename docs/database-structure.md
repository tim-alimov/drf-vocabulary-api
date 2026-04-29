# Database Structure

This document describes the current Neon PostgreSQL database used by the DRF vocabulary API.

Last inspected: 2026-04-29

## Overview

The database contains Django's built-in tables plus one project table:

- `vocabulary`

Django-managed system tables currently present:

- `auth_group`
- `auth_group_permissions`
- `auth_permission`
- `auth_user`
- `auth_user_groups`
- `auth_user_user_permissions`
- `django_admin_log`
- `django_content_type`
- `django_migrations`
- `django_session`

The main application data is stored in `vocabulary`.

## Custom PostgreSQL Types

### `cefr_level`

Used by `vocabulary.cefr`.

Allowed values:

| Value | Meaning |
| --- | --- |
| `A1` | Beginner |
| `A2` | Elementary |
| `B1` | Intermediate |
| `B2` | Upper-intermediate |
| `C1` | Advanced |
| `C2` | Proficient |

Current data uses only:

| CEFR | Rows |
| --- | ---: |
| `A1` | 1196 |
| `A2` | 1442 |
| `B1` | 2484 |
| `B2` | 2852 |

### `pos_type`

Used by `vocabulary.pos`.

Allowed values:

| Value |
| --- |
| `noun` |
| `verb` |
| `adjective` |
| `adverb` |
| `preposition` |
| `pronoun` |
| `conjunction` |
| `determiner` |
| `interjection` |
| `number` |

Current distribution:

| Part of speech | Rows |
| --- | ---: |
| `noun` | 4187 |
| `verb` | 1427 |
| `adjective` | 1515 |
| `adverb` | 561 |
| `preposition` | 79 |
| `pronoun` | 83 |
| `conjunction` | 37 |
| `determiner` | 46 |
| `interjection` | 9 |
| `number` | 30 |

## Table: `vocabulary`

Stores vocabulary words and their normalized metadata.

Current row count: `7974`

| Column | PostgreSQL type | Nullable | Notes |
| --- | --- | --- | --- |
| `id` | `integer` | No | Primary key |
| `headword` | `varchar(255)` | No | Vocabulary word or phrase |
| `pos` | `pos_type` | No | Part of speech enum |
| `cefr` | `cefr_level` | No | CEFR level enum |

### Constraints

| Constraint | Type | Column |
| --- | --- | --- |
| `vocabulary_pkey` | Primary key | `id` |
| `vocabulary_id_not_null` | Check / not-null | `id` |
| `vocabulary_headword_not_null` | Check / not-null | `headword` |
| `vocabulary_pos_not_null` | Check / not-null | `pos` |
| `vocabulary_cefr_not_null` | Check / not-null | `cefr` |

### Indexes

| Index | Definition |
| --- | --- |
| `vocabulary_pkey` | `CREATE UNIQUE INDEX vocabulary_pkey ON public.vocabulary USING btree (id)` |


## Data Quality Notes
### Duplicate `(headword, pos)` pairs

These duplicates currently exist:

| Headword | POS | Count |
| --- | --- | ---: |
| `check-in` | `noun` | 2 |
| `emphasize` | `verb` | 2 |
| `need` | `verb` | 2 |
| `to` | `preposition` | 2 |

Do not add a unique constraint on `(headword, pos)` until these are reviewed.

### Lengths

Current maximum values:

| Field | Max length |
| --- | ---: |
| `headword` | 24 |
| `pos` | 12 |
| `cefr` | 2 |

The current Django model uses `headword = CharField(max_length=255)`, which is safe.

## Django Model Mapping

Current Django model should map to the table like this:

```python
class Vocabulary(models.Model):
    headword = models.CharField(max_length=255)
    pos = models.CharField(max_length=55, choices=PartOfSpeech.choices)
    cefr = models.CharField(max_length=2, choices=CefrLevel.choices)

    class Meta:
        db_table = "vocabulary"
```

PostgreSQL enums provide database-level strictness. Django `TextChoices` provide application/API-level validation before data reaches the database.
