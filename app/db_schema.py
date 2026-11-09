from pathlib import Path

from sqlalchemy import text

from app.database import engine

SCHEMA_FILE = Path(__file__).resolve().parents[1] / "supabase" / "schema.sql"


def read_schema(path: Path = SCHEMA_FILE) -> str:
    return path.read_text(encoding="utf-8")


def schema_statements(sql: str) -> list[str]:
    lines = [line for line in sql.splitlines() if not line.strip().startswith("--")]
    return [statement.strip() for statement in "\n".join(lines).split(";") if statement.strip()]


def apply_schema(connection, sql: str | None = None) -> int:
    statements = schema_statements(sql if sql is not None else read_schema())
    for statement in statements:
        connection.execute(text(statement))
    return len(statements)


def ensure_schema() -> int:
    with engine.begin() as connection:
        return apply_schema(connection)
