from app.db_schema import read_schema, schema_statements


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


def test_schema_is_split_into_statements():
    statements = schema_statements(read_schema())
    assert len(statements) == 9
    assert statements[0].startswith("CREATE TABLE IF NOT EXISTS users")
