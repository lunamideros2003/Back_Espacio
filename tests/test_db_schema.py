import app.db_schema as schema_module
from app.db_schema import apply_schema, read_schema, schema_statements


def test_schema_defines_every_table():
    sql = read_schema().lower()
    for table in (
        "users",
        "celestial_objects",
        "quiz_questions",
        "quiz_attempts",
        "observations",
        "chat_messages",
    ):
        assert f"create table if not exists {table}" in sql


def test_schema_is_not_destructive():
    sql = read_schema().lower()
    for token in ("drop table", "drop index", "truncate", "delete from", "alter table"):
        assert token not in sql


def test_schema_statements_ignore_comments():
    sql = "-- uno\nCREATE TABLE IF NOT EXISTS x (id SERIAL);\n-- dos\nCREATE INDEX IF NOT EXISTS ix_x ON x (id);\n"
    statements = schema_statements(sql)
    assert len(statements) == 2
    assert all("--" not in statement for statement in statements)
    assert statements[1].startswith("CREATE INDEX IF NOT EXISTS ix_x")


def test_apply_schema_executes_every_statement():
    class Recorder:
        def __init__(self):
            self.statements = []

        def execute(self, statement):
            self.statements.append(str(statement))

    recorder = Recorder()
    sql = "CREATE TABLE IF NOT EXISTS a (id SERIAL);\nCREATE INDEX IF NOT EXISTS ix_a ON a (id);"
    assert apply_schema(recorder, sql) == 2
    assert len(recorder.statements) == 2
    assert recorder.statements[0].startswith("CREATE TABLE")


def test_every_create_is_idempotent():
    for statement in schema_statements(read_schema()):
        upper = statement.upper()
        if upper.startswith("CREATE TABLE") or upper.startswith("CREATE INDEX"):
            assert "IF NOT EXISTS" in upper


def test_ensure_schema_uses_the_engine(monkeypatch):
    class Connection:
        def __init__(self):
            self.statements = []

        def execute(self, statement):
            self.statements.append(str(statement))

    class Engine:
        def __init__(self):
            self.connection = Connection()

        def begin(self):
            return self

        def __enter__(self):
            return self.connection

        def __exit__(self, *_args):
            return False

    engine = Engine()
    monkeypatch.setattr(schema_module, "engine", engine)
    assert schema_module.ensure_schema() == 9
    assert len(engine.connection.statements) == 9


def test_schema_declares_foreign_keys_and_indexes():
    sql = read_schema().lower()
    assert sql.count("references") == 5
    assert sql.count("create index if not exists") == 3
    assert "on delete cascade" in sql
    assert "on delete set null" in sql


def test_schema_is_split_into_statements():
    statements = schema_statements(read_schema())
    assert len(statements) == 9
    assert statements[0].startswith("CREATE TABLE IF NOT EXISTS users")
