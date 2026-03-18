from pathlib import Path
from sqlalchemy import text
from typing import Any


async def run_sql_migrations(engine: Any):
    # Directory where this Python file is located
    current_dir = Path(__file__).resolve().parent

    # Look for .sql files in the same directory
    for file in sorted(current_dir.glob("*.sql")):
        sql = file.read_text(encoding="utf-8")
        async with engine.begin() as conn:
            await conn.execute(text(sql))
