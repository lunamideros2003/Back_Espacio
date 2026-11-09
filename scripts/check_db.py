"""Verify that the configured database accepts connections."""

from sqlalchemy import text

from app.database import engine


def main() -> None:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    print(f"Database OK ({engine.dialect.name}).")


if __name__ == "__main__":
    main()
