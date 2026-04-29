import csv
import asyncpg
import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "data" / "vocabulary.csv"

# Import configuration from the same .env file Django uses.
load_dotenv(BASE_DIR / ".env")

DATABASE_URL = os.environ["DATABASE_URL"]


async def main():
    conn = await asyncpg.connect(DATABASE_URL)

    # The exported CSV contains ids, but Postgres should generate ids on import.
    with CSV_PATH.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [(row["headword"], row["pos"], row["cefr"]) for row in reader]

    await conn.executemany(
        """
        INSERT INTO vocabulary (headword, pos, cefr)
        VALUES ($1, $2, $3)
        """,
        rows,
    )

    await conn.close()
    print(f"Imported {len(rows)} vocabulary rows from {CSV_PATH}")


asyncio.run(main())
