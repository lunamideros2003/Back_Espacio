"""Print how many rows exist in each table (useful after Supabase setup)."""

from app.database import SessionLocal
from app.models import CelestialObject, ChatMessage, Observation, QuizAttempt, QuizQuestion, User


def main() -> None:
    db = SessionLocal()
    try:
        rows = {
            "users": db.query(User).count(),
            "celestial_objects": db.query(CelestialObject).count(),
            "quiz_questions": db.query(QuizQuestion).count(),
            "quiz_attempts": db.query(QuizAttempt).count(),
            "observations": db.query(Observation).count(),
            "chat_messages": db.query(ChatMessage).count(),
        }
    finally:
        db.close()
    for name, count in rows.items():
        print(f"{name}: {count}")
    print(f"total: {sum(rows.values())}")


if __name__ == "__main__":
    main()
