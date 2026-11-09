from pathlib import Path

SCHEMA_FILE = Path(__file__).resolve().parents[1] / "supabase" / "schema.sql"


def read_schema(path: Path = SCHEMA_FILE) -> str:
    return path.read_text(encoding="utf-8")
