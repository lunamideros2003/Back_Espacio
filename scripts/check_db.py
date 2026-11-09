from sqlalchemy import text

from app.database import engine


def main() -> None:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    url = engine.url
    target = f"{url.host or 'local'}:{url.port or '-'}/{url.database or '-'}"
    print(f"Database OK ({engine.dialect.name}) at {target}.")


if __name__ == "__main__":
    main()
