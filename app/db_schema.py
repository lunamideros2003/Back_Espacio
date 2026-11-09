from pathlib import Path

SCHEMA_FILE = Path(__file__).resolve().parents[1] / "supabase" / "schema.sql"


def read_schema(path: Path = SCHEMA_FILE) -> str:
    return path.read_text(encoding="utf-8")


def schema_statements(sql: str) -> list[str]:
    lines = [line for line in sql.splitlines() if not line.strip().startswith("--")]
    return [statement.strip() for statement in "\n".join(lines).split(";") if statement.strip()]
