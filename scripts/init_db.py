"""Create the schema and seed the catalog. Safe to run more than once."""

from app.database import Base, engine
from app.seed import seed_if_empty


def main() -> None:
    Base.metadata.create_all(bind=engine)
    seed_if_empty()
    print(f"Schema ready on {engine.dialect.name}. Seed data checked.")


if __name__ == "__main__":
    main()
